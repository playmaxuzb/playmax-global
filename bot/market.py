"""PLAYMAX Market: sell form in the bot, listings in the market group, offers and moderation."""
import html
import json
import os
import re
import time

from config import LANGS
from market_i18n import m, RULES, WARN, ONLY_REPLIES, WELCOME, TYPES, COND
from moderation import clean
from tg import call, kb

MARKET_CHAT = int(os.environ.get("MARKET_CHAT", "-1004490358064"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_F = os.path.join(ROOT, "data", "market.json")
BOT = "PLAYMAXCatalogBot"

DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

try:
    DB = json.load(open(DB_F, encoding="utf8"))
except Exception:
    DB = {}
DB.setdefault("next", 101)
DB.setdefault("listings", {})
DB.setdefault("by_msg", {})
DB.setdefault("warns", {})

SESS = {}          # user_id -> sell-form state
TO_DELETE = []     # (chat_id, message_id, delete_at)
STATE = {"dirty": False, "owner": None}


def esc(s):
    return html.escape(s or "")


def deep(payload):
    return f"https://t.me/{BOT}?start={payload}"


def number(text):
    t = (text or "").translate(DIGITS).replace(" ", "").replace(",", "")
    found = re.findall(r"\d+(?:\.\d+)?", t)
    if not found:
        return None
    v = float(found[0])
    if re.search(r"\d\s*(k|к)\b", (text or "").lower()):
        v *= 1000
    return int(v)


def owner_id():
    if STATE["owner"] is None:
        admins = call("getChatAdministrators", chat_id=MARKET_CHAT) or []
        STATE["owner"] = next((a["user"]["id"] for a in admins if a["status"] == "creator"), 0)
    return STATE["owner"]


def card(L, lang_hint=None):
    best = L.get("best")
    status = "✅ SOLD · ПРОДАНО · فروخته شد" if L.get("sold") else (
        f"🔥 {best['amount']:,} $ — {esc(best['name'])}".replace(",", " ") if best else "🔥 —")
    return (
        f"🛒 <b>#{L['id']}</b>  {TYPES.get(L['type'], TYPES['other'])}\n"
        f"{COND.get(L['cond'], '')}\n"
        f"📍 {esc(L['city'])}\n"
        f"💰 <b>{L['price']:,} $</b>\n".replace(",", " ") +
        f"\n📝 {esc(L['desc'])}\n\n"
        f"👤 {esc(L['seller_name'])}\n"
        f"⬆️ Best offer · Лучшее предложение · بهترین پیشنهاد:\n{status}\n\n"
        f"💬 Reply with your price · Ответьте своей ценой · قیمت خود را ریپلای کنید"
    )


def listing_kb(L):
    return kb([
        [("📞 " + "Seller · Продавец · فروشنده", deep(f"seller_{L['id']}")), (f"📸 {len(L['photos'])}", deep(f"photos_{L['id']}"))],
        [("➕ Sell yours · Продать свой · بفروشید", deep("sell"))],
    ])


def save():
    os.makedirs(os.path.dirname(DB_F), exist_ok=True)
    with open(DB_F, "w", encoding="utf8") as f:
        json.dump(DB, f, ensure_ascii=False)
    STATE["dirty"] = False


# ---------------- sell form (private chat) ----------------
TYPE_ORDER = ["boxing", "claw", "table", "massage", "vending", "vr", "kids", "other"]


def start_sell(chat, uid, lang):
    today = time.strftime("%Y-%m-%d")
    mine_today = [L for L in DB["listings"].values() if L["seller"] == uid and L.get("day") == today]
    if len(mine_today) >= 3 and uid != owner_id():
        return call("sendMessage", chat_id=chat, text=m("limit", lang))
    SESS[uid] = {"step": "photos", "photos": [], "lang": lang}
    call("sendMessage", chat_id=chat, text=m("ask_photos", lang), parse_mode="HTML",
         reply_markup=kb([[(m("b_done_photos", lang), "cb:mk:photos_done")], [(m("b_cancel", lang), "cb:mk:cancel")]]))


def in_sell(uid):
    return uid in SESS


def sell_message(msg, lang):
    uid = msg["from"]["id"]
    chat = msg["chat"]["id"]
    s = SESS[uid]
    lang = s["lang"]
    text = msg.get("text") or msg.get("caption") or ""
    cancel = [(m("b_cancel", lang), "cb:mk:cancel")]
    if s["step"] == "photos":
        if msg.get("photo"):
            if len(s["photos"]) < 5:
                s["photos"].append(msg["photo"][-1]["file_id"])
            if len(s["photos"]) >= 5:
                return ask_type(chat, s)
            return None
        return call("sendMessage", chat_id=chat, text=m("need_photo", lang),
                    reply_markup=kb([[(m("b_done_photos", lang), "cb:mk:photos_done")], cancel]))
    if s["step"] == "city":
        if not text or not clean(text) or len(text) > 60:
            return call("sendMessage", chat_id=chat, text=m("bad_text", lang))
        s["city"] = text.strip()
        s["step"] = "price"
        return call("sendMessage", chat_id=chat, text=m("ask_price", lang), parse_mode="HTML", reply_markup=kb([cancel]))
    if s["step"] == "price":
        n = number(text)
        if not n or n < 10 or n > 1_000_000:
            return call("sendMessage", chat_id=chat, text=m("bad_price", lang))
        s["price"] = n
        s["step"] = "desc"
        return call("sendMessage", chat_id=chat, text=m("ask_desc", lang), parse_mode="HTML", reply_markup=kb([cancel]))
    if s["step"] == "desc":
        if not text or not clean(text):
            return call("sendMessage", chat_id=chat, text=m("bad_text", lang))
        s["desc"] = text.strip()[:400]
        s["step"] = "preview"
        u = msg["from"]
        s["seller_name"] = (u.get("first_name", "") + " " + u.get("last_name", "")).strip()[:40]
        s["username"] = u.get("username")
        return preview(chat, uid, s)
    return None


def ask_type(chat, s):
    s["step"] = "type"
    lang = s["lang"]
    rows = [[(TYPES[k].split(" · ")[0], f"cb:mk:type:{k}")] for k in TYPE_ORDER]
    rows.append([(m("b_cancel", lang), "cb:mk:cancel")])
    return call("sendMessage", chat_id=chat, text=m("ask_type", lang), parse_mode="HTML", reply_markup=kb(rows))


def preview(chat, uid, s):
    L = dict(s, id="•••", seller=uid)
    call("sendMessage", chat_id=chat, text=m("preview", s["lang"]))
    return call("sendPhoto", chat_id=chat, photo=s["photos"][0], caption=card(L), parse_mode="HTML",
                reply_markup=kb([[(m("b_publish", s["lang"]), "cb:mk:publish")], [(m("b_cancel", s["lang"]), "cb:mk:cancel")]]))


def publish(chat, uid):
    s = SESS.pop(uid, None)
    if not s:
        return
    lid = str(DB["next"])
    DB["next"] += 1
    L = {"id": lid, "seller": uid, "seller_name": s["seller_name"], "username": s.get("username"), "type": s["type"],
         "cond": s["cond"], "city": s["city"], "price": s["price"], "desc": s["desc"], "photos": s["photos"],
         "lang": s["lang"], "day": time.strftime("%Y-%m-%d"), "best": None, "offers": 0}
    res = call("sendPhoto", chat_id=MARKET_CHAT, photo=L["photos"][0], caption=card(L), parse_mode="HTML", reply_markup=listing_kb(L))
    if not res:
        return call("sendMessage", chat_id=chat, text="⚠️ Error, try again later.")
    L["msg"] = res["message_id"]
    DB["listings"][lid] = L
    DB["by_msg"][str(res["message_id"])] = lid
    STATE["dirty"] = True
    call("sendMessage", chat_id=chat, text=m("published", s["lang"]),
         reply_markup=kb([[(m("b_sold", s["lang"]), f"cb:mk:sold:{lid}"), (m("b_delete", s["lang"]), f"cb:mk:del:{lid}")]]))
    own = owner_id()
    if own and own != uid:
        call("sendMessage", chat_id=own, text=f"🆕 Market #{lid} — {esc(s['seller_name'])}\n{TYPES.get(L['type'])}\n💰 {L['price']} $",
             parse_mode="HTML", reply_markup=kb([[("🗑 Delete", f"cb:mk:del:{lid}")]]))


def on_callback(cq, lang):
    uid = cq["from"]["id"]
    chat = (cq.get("message") or {}).get("chat", {}).get("id", uid)
    parts = cq["data"].split(":")[1:]
    act = parts[0]
    s = SESS.get(uid)
    if act == "cancel":
        SESS.pop(uid, None)
        return call("sendMessage", chat_id=chat, text=m("cancelled", lang))
    if act == "photos_done" and s:
        if not s["photos"]:
            return call("sendMessage", chat_id=chat, text=m("need_photo", s["lang"]))
        return ask_type(chat, s)
    if act == "type" and s:
        s["type"] = parts[1]
        s["step"] = "cond"
        return call("sendMessage", chat_id=chat, text=m("ask_cond", s["lang"]), parse_mode="HTML",
                    reply_markup=kb([[(m("b_new", s["lang"]), "cb:mk:cond:new"), (m("b_used", s["lang"]), "cb:mk:cond:used")]]))
    if act == "cond" and s:
        s["cond"] = parts[1]
        s["step"] = "city"
        return call("sendMessage", chat_id=chat, text=m("ask_city", s["lang"]), parse_mode="HTML")
    if act == "publish" and s:
        return publish(chat, uid)
    if act in ("sold", "del"):
        L = DB["listings"].get(parts[1])
        if not L or uid not in (L["seller"], owner_id()):
            return
        if act == "sold":
            L["sold"] = True
            call("editMessageCaption", chat_id=MARKET_CHAT, message_id=L["msg"], caption=card(L), parse_mode="HTML")
            msg = m("marked_sold", lang)
        else:
            call("deleteMessage", chat_id=MARKET_CHAT, message_id=L["msg"])
            DB["listings"].pop(parts[1], None)
            msg = m("deleted", lang)
        STATE["dirty"] = True
        return call("sendMessage", chat_id=chat, text=msg)


def deep_link(chat, uid, arg, lang):
    """Handles /start payloads: sell, seller_<id>, photos_<id>, market, mylist."""
    if arg == "sell":
        return start_sell(chat, uid, lang)
    if arg == "market" or arg == "mylist":
        return show_intro(chat, uid, lang)
    kind, _, lid = arg.partition("_")
    L = DB["listings"].get(lid)
    if not L:
        return call("sendMessage", chat_id=chat, text="—")
    if kind == "seller":
        contact = esc(L["desc"]) + (f"\n\n👤 @{L['username']}" if L.get("username") else "")
        return call("sendMessage", chat_id=chat, text=m("seller_info", lang).format(id=L["id"], desc=contact), parse_mode="HTML")
    if kind == "photos":
        media = [{"type": "photo", "media": p} for p in L["photos"]]
        media[0]["caption"] = f"#{L['id']}"
        return call("sendMediaGroup", chat_id=chat, media=media)


def show_intro(chat, uid, lang):
    mine = [L for L in DB["listings"].values() if L["seller"] == uid]
    rows = [[(m("b_sell", lang), "cb:mk:start")]]
    for L in mine[-5:]:
        rows.append([(f"#{L['id']} · {L['price']} $ " + ("✅" if L.get("sold") else ""), f"cb:mk:sold:{L['id']}"),
                     ("🗑", f"cb:mk:del:{L['id']}")])
    rows.append([("⬅️", "cb:m:menu")])
    return call("sendMessage", chat_id=chat, text=m("market_intro", lang), parse_mode="HTML", reply_markup=kb(rows))


# ---------------- group moderation ----------------
def is_admin(uid):
    if not hasattr(is_admin, "cache") or time.time() - is_admin.ts > 600:
        is_admin.cache = {a["user"]["id"] for a in (call("getChatAdministrators", chat_id=MARKET_CHAT) or [])}
        is_admin.ts = time.time()
    return uid in is_admin.cache


def temp(chat, text, seconds=40, markup=None):
    res = call("sendMessage", chat_id=chat, text=text, parse_mode="HTML", reply_markup=markup, disable_notification=True)
    if res:
        TO_DELETE.append((chat, res["message_id"], time.time() + seconds))


def warn(msg):
    u = msg["from"]
    key = str(u["id"])
    n = DB["warns"].get(key, 0) + 1
    DB["warns"][key] = n
    STATE["dirty"] = True
    call("deleteMessage", chat_id=msg["chat"]["id"], message_id=msg["message_id"])
    name = esc(u.get("first_name", ""))
    if n == 2:
        call("restrictChatMember", chat_id=MARKET_CHAT, user_id=u["id"], until_date=int(time.time()) + 86400,
             permissions={"can_send_messages": False})
    if n >= 3:
        call("banChatMember", chat_id=MARKET_CHAT, user_id=u["id"])
    temp(MARKET_CHAT, WARN.format(name=name, n=min(n, 3)))


def group_message(msg):
    if msg["chat"]["id"] != MARKET_CHAT:
        return
    if msg.get("new_chat_members"):
        call("deleteMessage", chat_id=MARKET_CHAT, message_id=msg["message_id"])
        for u in msg["new_chat_members"]:
            if not u.get("is_bot"):
                temp(MARKET_CHAT, WELCOME.format(name=esc(u.get("first_name", ""))), 60,
                     kb([[("➕ Sell · Продать · فروش", deep("sell"))]]))
        return
    if msg.get("left_chat_member") or msg.get("pinned_message"):
        return call("deleteMessage", chat_id=MARKET_CHAT, message_id=msg["message_id"])
    u = msg.get("from") or {}
    if u.get("is_bot") or msg.get("sender_chat") and msg["sender_chat"]["id"] == MARKET_CHAT or is_admin(u.get("id")):
        return
    text = msg.get("text") or msg.get("caption") or ""
    if msg.get("forward_origin") or msg.get("forward_date") or not clean(text):
        return warn(msg)
    reply = msg.get("reply_to_message")
    lid = DB["by_msg"].get(str(reply["message_id"])) if reply else None
    if not lid:
        call("deleteMessage", chat_id=MARKET_CHAT, message_id=msg["message_id"])
        return temp(MARKET_CHAT, ONLY_REPLIES.format(name=esc(u.get("first_name", ""))), 25,
                    kb([[("➕ Sell · Продать · فروش", deep("sell"))]]))
    L = DB["listings"].get(lid)
    if not L or L.get("sold"):
        return
    n = number(text)
    if n and n >= 10:
        L["offers"] = L.get("offers", 0) + 1
        name = (u.get("first_name") or "")[:20]
        if not L.get("best") or n > L["best"]["amount"]:
            L["best"] = {"amount": n, "name": name, "uid": u["id"]}
            call("editMessageCaption", chat_id=MARKET_CHAT, message_id=L["msg"], caption=card(L), parse_mode="HTML",
                 reply_markup=listing_kb(L))
        who = f"<a href=\"tg://user?id={u['id']}\">{esc(name)}</a>"
        call("sendMessage", chat_id=L["seller"], parse_mode="HTML",
             text=m("new_offer", L.get("lang", "en")).format(id=L["id"], amount=n, name=who))
        STATE["dirty"] = True


def tick():
    """Delete expired temporary messages. Call from the main loop."""
    now = time.time()
    keep = []
    for chat, mid, at in TO_DELETE:
        if at <= now:
            call("deleteMessage", chat_id=chat, message_id=mid)
        else:
            keep.append((chat, mid, at))
    TO_DELETE[:] = keep


def setup_group():
    """Pin the multilingual charter; update it in place when the text changes."""
    import hashlib
    h = hashlib.md5(RULES.encode()).hexdigest()
    markup = kb([[("➕ Sell a machine · فروش ماشین · بيع جهاز", deep("sell"))]])
    if DB.get("rules_msg"):
        if DB.get("rules_hash") != h:
            call("editMessageText", chat_id=MARKET_CHAT, message_id=DB["rules_msg"], text=RULES, parse_mode="HTML", reply_markup=markup)
            DB["rules_hash"] = h
            STATE["dirty"] = True
        return
    DB["rules_hash"] = h
    res = call("sendMessage", chat_id=MARKET_CHAT, text=RULES, parse_mode="HTML",
               reply_markup=kb([[("➕ Sell a machine · Продать · فروش ماشین", deep("sell"))]]))
    if res:
        call("pinChatMessage", chat_id=MARKET_CHAT, message_id=res["message_id"], disable_notification=True)
        DB["rules_msg"] = res["message_id"]
        STATE["dirty"] = True
