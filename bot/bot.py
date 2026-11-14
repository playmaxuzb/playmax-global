"""PlayMax Global bot — long polling. Runs inside GitHub Actions in ~5h50m shifts."""
import json
import os
import subprocess
import time

import content
import market
from config import LANGS, FLAGS, LANG_NAMES, LINKS, OFFICE, FACTORY, map_lang, PHONE_AF
from i18n import t
from tg import call, kb, LAST_ERROR

ROOT = content.ROOT
USERS_F = os.path.join(ROOT, "data", "users.json")
RUN_SECONDS = int(os.environ.get("RUN_SECONDS", str(5 * 3600 + 50 * 60)))


def load_users():
    try:
        with open(USERS_F, encoding="utf8") as f:
            return json.load(f)
    except Exception:
        return {}


USERS = load_users()
CHATS_F = os.path.join(ROOT, "data", "chats.json")
try:
    CHATS = json.load(open(CHATS_F, encoding="utf8"))
except Exception:
    CHATS = {}
STATUS = {"updates": 0, "started": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}


def note_chat(chat):
    global DIRTY
    if chat.get("type") in ("group", "supergroup", "channel") and str(chat["id"]) not in CHATS:
        CHATS[str(chat["id"])] = {"title": chat.get("title"), "type": chat["type"], "username": chat.get("username")}
        DIRTY = True
POSTS = content.load_all()
DIRTY = False


def lang_of(user):
    uid = str(user["id"])
    return USERS.get(uid) or map_lang(user.get("language_code"))


def set_lang(user, lang):
    global DIRTY
    if USERS.get(str(user["id"])) != lang:
        USERS[str(user["id"])] = lang
        DIRTY = True


# ---------- screens ----------
def lang_picker():
    rows, row = [], []
    for l in LANGS:
        row.append((f"{FLAGS[l]} {LANG_NAMES[l]}", f"cb:L:{l}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return kb(rows)


def menu_kb(lang):
    return kb([
        [(t("b_catalog", lang), "cb:m:catalog")],
        [(t("b_contacts", lang), "cb:m:contacts"), (t("b_places", lang), "cb:m:places")],
        [(t("b_channels", lang), "cb:m:channels"), (t("b_social", lang), "cb:m:social")],
        [(market.m("b_market", lang), "cb:m:market"), (market.m("b_sell", lang), "cb:mk:start")],
        [(t("b_consult", lang), "cb:m:consult")],
        [(t("b_lang", lang), "cb:m:lang")],
    ])


def back(lang, extra=None):
    rows = list(extra or [])
    rows.append([(t("b_back", lang), "cb:m:menu")])
    return kb(rows)


def phone_rows():
    return [
        [("🇺🇿 Telegram ·99", LINKS["tg_99"]), ("🇺🇿 WhatsApp ·99", LINKS["wa_99"])],
        [("🇺🇿 Telegram ·79", LINKS["tg_79"]), ("🇺🇿 WhatsApp ·79", LINKS["wa_79"])],
        [("🇦🇫 Telegram ·11", LINKS["tg_af"]), ("🇦🇫 WhatsApp ·11", LINKS["wa_af"])],
    ]


SUPPORT_WAIT = set()


def to_team(msg, lang):
    """Forward a customer's message to the owner; remember who to answer."""
    own = market.owner_id()
    u = msg["from"]
    if not own or u["id"] == own:
        return False
    uname = f" @{u['username']}" if u.get("username") else ""
    head = call("sendMessage", chat_id=own, parse_mode="HTML",
                text=f"📩 <b>{(u.get('first_name') or '')} {(u.get('last_name') or '')}</b>{uname} · {FLAGS.get(lang, '')} {lang}\n↩️ Reply to answer")
    cp = call("copyMessage", chat_id=own, from_chat_id=msg["chat"]["id"], message_id=msg["message_id"])
    sup = market.DB.setdefault("support", {})
    for r in (head, cp):
        if r:
            sup[str(r["message_id"])] = [u["id"], lang]
    market.STATE["dirty"] = True
    call("sendMessage", chat_id=msg["chat"]["id"], text=t("received", lang), reply_markup=menu_kb(lang))
    return True


def from_team(msg):
    """Owner replied to a forwarded message -> relay to the customer."""
    reply = msg.get("reply_to_message")
    if not reply or msg["from"]["id"] != market.owner_id():
        return False
    target = market.DB.get("support", {}).get(str(reply["message_id"]))
    if not target:
        return False
    uid, lang = target
    call("sendMessage", chat_id=uid, text=t("team_reply", lang), parse_mode="HTML")
    ok = call("copyMessage", chat_id=uid, from_chat_id=msg["chat"]["id"], message_id=msg["message_id"])
    call("sendMessage", chat_id=msg["chat"]["id"], text="✅ Sent" if ok else "⚠️ Not delivered", reply_to_message_id=msg["message_id"])
    return True


def screen(chat, lang, name, edit_id=None):
    send = dict(chat_id=chat, parse_mode="HTML", disable_web_page_preview=True)
    if name == "menu":
        text, markup = t("welcome", lang), menu_kb(lang)
    elif name == "catalog":
        text, markup = t("catalog", lang), back(lang, [[(t("b_site", lang), LINKS["site"])]])
    elif name == "contacts":
        text, markup = t("contacts", lang), back(lang, phone_rows() + [[("✉️ Email", "https://mail.google.com/mail/?view=cm&to=" + LINKS["email"])]])
    elif name == "places":
        text, markup = t("places", lang), back(lang, [[(t("b_office", lang), LINKS["office_map"])], [(t("b_factory", lang), LINKS["factory_map"])], [("📍 PIN", "cb:m:pins")]])
    elif name == "channels":
        text, markup = t("channels", lang), back(lang, [[(t("b_ch_global", lang), LINKS["tg_global"])], [(t("b_ch_uz", lang), LINKS["tg_uz"])]])
    elif name == "social":
        text, markup = t("social", lang), back(lang, [
            [(t("b_site", lang), LINKS["site"])],
            [("📸 Instagram 🇦🇫", LINKS["ig_af"]), ("📸 Instagram 🇺🇿", LINKS["ig_uz"])],
            [(t("b_ch_global", lang), LINKS["tg_global"]), (t("b_ch_uz", lang), LINKS["tg_uz"])],
        ])
    elif name == "consult":
        text, markup = t("consult", lang), back(lang, [[(t("b_write", lang), "cb:m:write")]] + phone_rows())
    elif name == "write":
        SUPPORT_WAIT.add(int(chat))
        text, markup = t("write_now", lang), back(lang)
    elif name == "market":
        return market.show_intro(chat, int(chat), lang)
    elif name == "lang":
        text, markup = t("choose", lang), lang_picker()
    elif name == "pins":
        call("sendVenue", chat_id=chat, latitude=OFFICE[0], longitude=OFFICE[1], title=t("office_pin", lang), address="Tashkent")
        call("sendVenue", chat_id=chat, latitude=FACTORY[0], longitude=FACTORY[1], title=t("factory_pin", lang), address="Tashkent")
        return call("sendMessage", text=t("fallback", lang), reply_markup=menu_kb(lang), **send)
    else:
        text, markup = t("fallback", lang), menu_kb(lang)

    if edit_id:
        res = call("editMessageText", message_id=edit_id, text=text, reply_markup=markup, **send)
        if res:
            return res
    return call("sendMessage", text=text, reply_markup=markup, **send)


def send_post(chat, pid, lang):
    p = POSTS.get(pid)
    if not p:
        return screen(chat, lang, "menu")
    return content.deliver(chat, p, lang, kb(content.bot_keyboard(p, lang)))


# ---------- handlers ----------

def on_message(msg):
    chat = msg["chat"]["id"]
    if msg["chat"]["type"] != "private":
        return market.group_message(msg)
    user = msg["from"]
    text = msg.get("text", "")
    lang = lang_of(user)
    if market.in_sell(user["id"]) and not text.startswith("/"):
        return market.sell_message(msg, lang)
    if from_team(msg):
        return
    if not text.startswith("/") and (user["id"] in SUPPORT_WAIT or text):
        SUPPORT_WAIT.discard(user["id"])
        if to_team(msg, lang):
            return
    if text.startswith("/start"):
        arg = text.split(" ", 1)[1] if " " in text else ""
        if arg == "sell" or arg == "market" or arg.startswith(("seller_", "photos_")):
            if str(user["id"]) not in USERS:
                set_lang(user, lang)
            return market.deep_link(chat, user["id"], arg, lang)
        if arg.startswith("p_"):
            parts = arg.split("_")
            pl = parts[-1] if parts[-1] in LANGS else lang
            set_lang(user, pl)
            return send_post(chat, "_".join(parts[1:-1]), pl)
        if arg.startswith("consult"):
            parts = arg.split("_")
            if len(parts) > 1 and parts[1] in LANGS and str(user["id"]) not in USERS:
                lang = parts[1]
                set_lang(user, lang)
            return screen(chat, lang, "consult")
        if str(user["id"]) not in USERS:
            return call("sendMessage", chat_id=chat, text=t("choose", lang), reply_markup=lang_picker())
        return screen(chat, lang, "menu")
    cmd = text.lstrip("/").split("@")[0].lower()
    if cmd == "sell":
        return market.start_sell(chat, user["id"], lang)
    if cmd in ("menu", "catalog", "contacts", "places", "channels", "social", "consult", "lang", "market"):
        return screen(chat, lang, cmd)
    if cmd == "language":
        return screen(chat, lang, "lang")
    return screen(chat, lang, "fallback")


def on_callback(cq):
    user = cq["from"]
    data = cq.get("data", "")
    msg = cq.get("message") or {}
    chat = msg.get("chat", {}).get("id", user["id"])
    mid = msg.get("message_id")
    lang = lang_of(user)
    call("answerCallbackQuery", callback_query_id=cq["id"])
    kind, _, rest = data.partition(":")
    if data == "mk:start":
        return market.start_sell(chat, user["id"], lang)
    if kind == "mk":
        return market.on_callback(cq, lang)
    if kind == "L":
        set_lang(user, rest)
        return screen(chat, rest, "menu", edit_id=mid)
    if kind == "m":
        editable = bool(msg.get("text"))
        return screen(chat, lang, rest, edit_id=mid if editable and rest not in ("pins", "market") else None)
    if kind == "tr":
        pid, _, l = rest.rpartition(":")
        set_lang(user, l)
        return send_post(chat, pid, l)


# ---------- persistence ----------
def save_users(push=False):
    global DIRTY
    if market.STATE["dirty"]:
        market.save()
        DIRTY = True
    if not DIRTY:
        return
    os.makedirs(os.path.dirname(USERS_F), exist_ok=True)
    with open(USERS_F, "w", encoding="utf8") as f:
        json.dump(USERS, f)
    with open(CHATS_F, "w", encoding="utf8") as f:
        json.dump(CHATS, f, indent=1, ensure_ascii=False)
    STATUS["errors"] = dict(LAST_ERROR)
    STATUS["saved"] = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    with open(os.path.join(ROOT, "data", "status.json"), "w") as f:
        json.dump(STATUS, f, indent=1)
    DIRTY = False
    if push:
        git_sync(["data/users.json", "data/chats.json", "data/status.json", "data/market.json"], "bot: save state")


def git_sync(files, message):
    try:
        subprocess.run(["git", "add", *files], cwd=ROOT, check=True)
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
            return
        subprocess.run(["git", "commit", "-qm", message], cwd=ROOT, check=True)
        for _ in range(3):
            subprocess.run(["git", "pull", "-q", "--rebase", "-X", "theirs"], cwd=ROOT)
            if subprocess.run(["git", "push", "-q"], cwd=ROOT).returncode == 0:
                return
    except Exception as e:
        print("[git]", e)


def code_hash():
    r = subprocess.run(["git", "rev-parse", "HEAD:bot"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip()


def refresh_content():
    """Pull new content; return True when the bot code itself changed (time to restart)."""
    global POSTS
    subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=ROOT)
    POSTS = content.load_all()
    return code_hash() != START_HASH


START_HASH = code_hash()


def main():
    start = time.time()
    offset = None
    last_refresh = time.time()
    print("bot started, posts:", len(POSTS))
    import setup_bot
    setup_bot.run()
    market.setup_group()
    while time.time() - start < RUN_SECONDS:
        updates = call("getUpdates", offset=offset, timeout=20,
                       allowed_updates=["message", "callback_query", "my_chat_member", "channel_post", "edited_message"]) or []
        for u in updates:
            offset = u["update_id"] + 1
            STATUS["updates"] += 1
            for k in ("message", "my_chat_member", "channel_post", "edited_message"):
                if k in u:
                    note_chat(u[k]["chat"])
            try:
                if "message" in u:
                    on_message(u["message"])
                elif "callback_query" in u:
                    on_callback(u["callback_query"])
            except Exception as e:
                print("[handler]", e)
        market.tick()
        if market.STATE["dirty"] and time.time() - last_refresh > 120:
            last_refresh = 0
        if time.time() - last_refresh > (120 if time.time() - start < 1800 else 900):
            globals()["DIRTY"] = True
            save_users(push=True)
            if refresh_content():
                print("code updated — handing over to the next shift")
                break
            last_refresh = time.time()
    # confirm the last offset so the next shift doesn't repeat updates
    if offset:
        call("getUpdates", offset=offset, timeout=0)
    save_users(push=True)
    print("shift finished")


if __name__ == "__main__":
    main()
