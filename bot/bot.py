"""PlayMax Global bot — long polling. Runs inside GitHub Actions in ~5h50m shifts."""
import json
import os
import subprocess
import time

import content
from config import LANGS, FLAGS, LANG_NAMES, LINKS, OFFICE, FACTORY, map_lang, PHONE_AF
from i18n import t
from tg import call, kb

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
        [(t("b_consult", lang), "cb:m:consult")],
        [(t("b_lang", lang), "cb:m:lang")],
    ])


def back(lang, extra=None):
    rows = list(extra or [])
    rows.append([(t("b_back", lang), "cb:m:menu")])
    return kb(rows)


def screen(chat, lang, name, edit_id=None):
    send = dict(chat_id=chat, parse_mode="HTML", disable_web_page_preview=True)
    if name == "menu":
        text, markup = t("welcome", lang), menu_kb(lang)
    elif name == "catalog":
        text, markup = t("catalog", lang), back(lang, [[(t("b_site", lang), LINKS["site"])]])
    elif name == "contacts":
        text, markup = t("contacts", lang), back(lang, [[(t("b_wa", lang), LINKS["wa_af"])], [("✉️ Email", "https://mail.google.com/mail/?view=cm&to=" + LINKS["email"])]])
    elif name == "places":
        text, markup = t("places", lang), back(lang, [[(t("b_office", lang), LINKS["office_map"])], [(t("b_factory", lang), LINKS["factory_map"])], [("📍 PIN", "cb:m:pins")]])
    elif name == "channels":
        text, markup = t("channels", lang), back(lang, [[(t("b_ch_global", lang), LINKS["tg_global"])], [(t("b_ch_uz", lang), LINKS["tg_uz"])]])
    elif name == "social":
        text, markup = t("social", lang), back(lang, [
            [("📸 Instagram 🇦🇫", LINKS["ig_af"]), ("📸 Instagram 🇺🇿", LINKS["ig_uz"])],
            [("🎵 TikTok", LINKS["tiktok"]), ("🔗 All links", LINKS["linkbio"])],
        ])
    elif name == "consult":
        text, markup = t("consult", lang), back(lang, [[(t("b_wa", lang), LINKS["wa_af"])], [(t("b_site", lang), LINKS["site"])]])
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
    cap = content.caption(p, lang)
    markup = kb(content.bot_keyboard(p, lang))
    url = content.media_url(p)
    typ = p.get("type")
    if typ == "poll":
        q = p["poll"]["q"].get(lang, p["poll"]["q"]["en"])
        opts = p["poll"]["o"].get(lang, p["poll"]["o"]["en"])
        body = f"📊 <b>{q}</b>\n\n" + "\n".join(f"• {o}" for o in opts)
        return call("sendMessage", chat_id=chat, text=body, parse_mode="HTML", reply_markup=markup)
    if typ == "photo" and url:
        return call("sendPhoto", chat_id=chat, photo=url, caption=cap, parse_mode="HTML", reply_markup=markup)
    if typ in ("video", "animation") and url:
        return call("sendVideo", chat_id=chat, video=url, caption=cap, parse_mode="HTML", reply_markup=markup, supports_streaming=True)
    return call("sendMessage", chat_id=chat, text=cap, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)


# ---------- handlers ----------
def on_message(msg):
    chat = msg["chat"]["id"]
    if msg["chat"]["type"] != "private":
        return
    user = msg["from"]
    text = msg.get("text", "")
    lang = lang_of(user)
    if text.startswith("/start"):
        arg = text.split(" ", 1)[1] if " " in text else ""
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
    if cmd in ("menu", "catalog", "contacts", "places", "channels", "social", "consult", "lang"):
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
    if kind == "L":
        set_lang(user, rest)
        return screen(chat, rest, "menu", edit_id=mid)
    if kind == "m":
        editable = bool(msg.get("text"))
        return screen(chat, lang, rest, edit_id=mid if editable and rest != "pins" else None)
    if kind == "tr":
        pid, _, l = rest.rpartition(":")
        set_lang(user, l)
        return send_post(chat, pid, l)


# ---------- persistence ----------
def save_users(push=False):
    global DIRTY
    if not DIRTY:
        return
    os.makedirs(os.path.dirname(USERS_F), exist_ok=True)
    with open(USERS_F, "w", encoding="utf8") as f:
        json.dump(USERS, f)
    DIRTY = False
    if push:
        git_sync(["data/users.json"], "bot: save language choices")


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


def refresh_content():
    global POSTS
    subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=ROOT)
    POSTS = content.load_all()


def main():
    start = time.time()
    offset = None
    last_refresh = time.time()
    print("bot started, posts:", len(POSTS))
    while time.time() - start < RUN_SECONDS:
        updates = call("getUpdates", offset=offset, timeout=50, allowed_updates=["message", "callback_query"]) or []
        for u in updates:
            offset = u["update_id"] + 1
            try:
                if "message" in u:
                    on_message(u["message"])
                elif "callback_query" in u:
                    on_callback(u["callback_query"])
            except Exception as e:
                print("[handler]", e)
        if time.time() - last_refresh > 900:
            save_users(push=True)
            refresh_content()
            last_refresh = time.time()
    # confirm the last offset so the next shift doesn't repeat updates
    if offset:
        call("getUpdates", offset=offset, timeout=0)
    save_users(push=True)
    print("shift finished")


if __name__ == "__main__":
    main()
