"""Set channel / market group photos from media/brand (multipart upload)."""
import os, uuid, urllib.request, json
from config import TOKEN, CHANNEL
from market import MARKET_CHAT
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def set_photo(chat, path):
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat}\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"p.png\"\r\nContent-Type: image/png\r\n\r\n").encode()
    body += open(path, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/setChatPhoto", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        print(chat, json.loads(urllib.request.urlopen(req, timeout=60).read()))
    except Exception as e:
        print(chat, "error", e)


set_photo(CHANNEL, os.path.join(ROOT, "media/brand/av_global.png"))
set_photo(MARKET_CHAT, os.path.join(ROOT, "media/brand/av_market.png"))
