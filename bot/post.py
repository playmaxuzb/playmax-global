"""Publish every channel post whose time has come (Tashkent time). Run by cron every 30 min."""
import datetime as dt
import json
import os
import sys

import content
from bot import git_sync
from config import CHANNEL
from tg import call, kb

TZ = dt.timezone(dt.timedelta(hours=5))
POSTED_F = os.path.join(content.ROOT, "data", "posted.json")
WINDOW_H = 6  # don't publish anything more than 6h late


def publish(p):
    url = content.media_url(p)
    markup = kb(content.channel_keyboard(p))
    lang = p["lang"]
    typ = p.get("type")
    base = dict(chat_id=CHANNEL, reply_markup=markup)
    if typ == "poll":
        return call("sendPoll", question=p["poll"]["q"][lang], options=[{"text": o} for o in p["poll"]["o"][lang]],
                    is_anonymous=True, **content.poll_extra(p), **base)
    cap = content.caption(p, lang)
    if typ == "photo":
        return call("sendPhoto", photo=url, caption=cap, parse_mode="HTML", **base)
    if typ in ("video", "animation"):
        return call("sendVideo", video=url, caption=cap, parse_mode="HTML", supports_streaming=True, **base)
    return call("sendMessage", text=cap, parse_mode="HTML", disable_web_page_preview=True, **base)


def broadcast(p):
    """Send the post to every bot subscriber in the language they chose."""
    import time
    try:
        users = json.load(open(os.path.join(content.ROOT, "data", "users.json")))
    except Exception:
        return
    for uid, lang in users.items():
        if lang == "off":
            continue
        content.deliver(int(uid), p, lang, kb(content.bot_keyboard(p, lang)))
        time.sleep(0.06)


def main():
    force = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        posted = json.load(open(POSTED_F))
    except Exception:
        posted = {}
    now = dt.datetime.now(TZ)
    changed = False
    for pid, p in content.load_all().items():
        if pid in posted:
            continue
        when = dt.datetime.fromisoformat(f"{p['date']}T{p['time']}:00").replace(tzinfo=TZ)
        due = force == pid or (when <= now and (now - when).total_seconds() < WINDOW_H * 3600)
        if not due:
            continue
        res = publish(p)
        if res:
            posted[pid] = {"message_id": res.get("message_id"), "at": now.isoformat(timespec="minutes")}
            changed = True
            print("posted", pid)
            broadcast(p)
            if p.get("pin"):
                call("pinChatMessage", chat_id=CHANNEL, message_id=res["message_id"], disable_notification=True)
    if changed:
        os.makedirs(os.path.dirname(POSTED_F), exist_ok=True)
        json.dump(posted, open(POSTED_F, "w"), indent=1)
        git_sync(["data/posted.json"], "post: published")


if __name__ == "__main__":
    main()
