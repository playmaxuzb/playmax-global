"""Tiny Telegram Bot API client (stdlib only)."""
import json
import time
import urllib.request
import urllib.error
from config import TOKEN

API = f"https://api.telegram.org/bot{TOKEN}/"


LAST_ERROR = {}


def call(method, timeout=70, **params):
    data = json.dumps({k: v for k, v in params.items() if v is not None}).encode()
    req = urllib.request.Request(API + method, data=data, headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                res = json.loads(r.read())
                return res.get("result")
        except urllib.error.HTTPError as e:
            body = json.loads(e.read() or b"{}")
            retry = body.get("parameters", {}).get("retry_after")
            if retry:
                time.sleep(retry + 1)
                continue
            LAST_ERROR[method] = body.get("description")
            print(f"[tg] {method} failed: {body.get('description')}")
            return None
        except Exception as e:  # network hiccup
            print(f"[tg] {method} error: {e}")
            time.sleep(3 * (attempt + 1))
    return None


def kb(rows):
    """rows: list of rows; each button is (text, url) or (text, 'cb:data')."""
    out = []
    for row in rows:
        r = []
        for text, target in row:
            if target.startswith("cb:"):
                r.append({"text": text, "callback_data": target[3:]})
            else:
                r.append({"text": text, "url": target})
        out.append(r)
    return {"inline_keyboard": out}
