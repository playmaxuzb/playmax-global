"""Load scheduled posts and render them for the channel or the bot."""
import glob
import json
import os
from config import LANGS, BOT_USERNAME, REPO_RAW, LINKS
from i18n import t

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_all():
    posts = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*.json"))):
        with open(f, encoding="utf8") as fh:
            for p in json.load(fh):
                posts[p["id"]] = p
    return posts


def media_url(p):
    m = p.get("media")
    if not m:
        return None
    return m if m.startswith("http") else REPO_RAW + m


def caption(p, lang, footer=True):
    txt = p.get("text", {}).get(lang) or p.get("text", {}).get("en", "")
    if footer and p.get("type") != "poll":
        txt += t("footer", lang)
    return txt


def deep(payload):
    return f"https://t.me/{BOT_USERNAME}?start={payload}"


def channel_keyboard(p):
    lang = p["lang"]
    others = [l for l in LANGS if l != lang]
    rows = [[(t("b_read", l), deep(f"p_{p['id']}_{l}")) for l in others]]
    rows.append([(t("b_order_short", lang), LINKS["site"]), (t("b_ask", lang), deep(f"consult_{lang}"))])
    return rows


def bot_keyboard(p, lang):
    others = [l for l in LANGS if l != lang]
    rows = [[(t("b_read", l), f"cb:tr:{p['id']}:{l}") for l in others]]
    rows.append([(t("b_order_short", lang), LINKS["site"]), (t("b_consult", lang), "cb:m:consult")])
    rows.append([(t("b_back", lang), "cb:m:menu")])
    return rows
