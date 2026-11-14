"""Send a day's posts privately to the owner for review: ops/preview contains the date."""
import json, os, time
import content, market
from tg import call, kb
ROOT = content.ROOT
date = open(os.path.join(ROOT, "ops", "preview")).read().strip()
own = market.owner_id()
try:
    lang = json.load(open(os.path.join(ROOT, "data", "users.json"))).get(str(own), "ar")
except Exception:
    lang = "ar"
posts = [p for p in content.load_all().values() if p["date"] == date]
call("sendMessage", chat_id=own, text=f"👀 معاينة منشورات {date} — {len(posts)} منشورات (هكذا تظهر في القناة)")
for p in sorted(posts, key=lambda p: p["time"]):
    call("sendMessage", chat_id=own, text=f"🕒 {p['time']} · {p['lang']}")
    pl = p["lang"]
    content.deliver(own, p, pl, kb(content.channel_keyboard(p)))
    time.sleep(1)
