"""List the chats the bot was added to (from pending updates) and save them to data/chats.json."""
import json, os
from tg import call, LAST_ERROR
import content

ROOT = content.ROOT
F = os.path.join(ROOT, "data", "chats.json")
try:
    chats = json.load(open(F))
except Exception:
    chats = {}
me = call("getMe") or {}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
print("bot:", me.get("username"))

ups = call("getUpdates", timeout=0) or []
dbg = [f"me: {me.get('username')} name={me.get('first_name')} {me.get('can_read_all_group_messages')}", f"webhook: {(call('getWebhookInfo') or {}).get('url')!r}", f"updates: {len(ups)}", f"errors: {LAST_ERROR}"]
for u in ups:
    dbg.append(" ".join(f"{k}:{u[k].get('chat',{}).get('type')}:{u[k].get('chat',{}).get('id')}" for k in u if isinstance(u[k], dict)))
open(os.path.join(ROOT, "data", "debug.txt"), "w").write("\n".join(dbg))
for u in ups:
    for k in ("my_chat_member", "message", "channel_post", "chat_member"):
        if k in u:
            c = u[k]["chat"]
            if c["type"] != "private":
                chats[str(c["id"])] = {"title": c.get("title"), "type": c["type"], "username": c.get("username")}
for cid in list(chats):
    info = call("getChat", chat_id=int(cid)) or {}
    chats[cid]["linked_chat_id"] = info.get("linked_chat_id")
    adm = call("getChatAdministrators", chat_id=int(cid)) or []
    chats[cid]["bot_admin"] = any(a["user"].get("id") == me.get("id") for a in adm)
for ch in ["@PlaymaxUZ_AF"]:
    info = call("getChat", chat_id=ch)
    if info:
        chats[str(info["id"])] = {"title": info.get("title"), "type": info["type"], "username": info.get("username"), "linked_chat_id": info.get("linked_chat_id")}
a = call("getChatMember", chat_id="@PlaymaxUZ_AF", user_id=me.get("id")) or {}
dbg.append(f"errors2: {LAST_ERROR}")
dbg.append(f"main channel status: {a.get('status')}")
open(os.path.join(ROOT, "data", "debug.txt"), "w").write("\n".join(dbg))
os.makedirs(os.path.dirname(F), exist_ok=True)
json.dump(chats, open(F, "w"), indent=1, ensure_ascii=False)
print(json.dumps(chats, indent=1, ensure_ascii=False))
