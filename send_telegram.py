#!/usr/bin/env python3
"""Send the latest week's top-5 Claude Code use cases to Telegram. Stdlib only.

Usage:
  python3 send_telegram.py               # send to Telegram (needs config.json)
  python3 send_telegram.py --dry-run     # print the message instead of sending
  python3 send_telegram.py --get-chat-id # after messaging your bot, print chat ids

Setup (once):
  1. In Telegram, message @BotFather -> /newbot -> copy the token.
  2. Copy config.example.json to config.json and paste the token in.
  3. Send your new bot any message (e.g. "hi"), then run --get-chat-id
     and put the printed id into config.json as chat_id.
"""
import json
import sys
import urllib.parse
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "usecases.json"
CONFIG = ROOT / "config.json"

BADGES = [
    ("creative", "\U0001f3a8 creative"),
    ("useful", "✅ useful"),
    ("fun", "\U0001f389 fun"),
    ("painPoint", "\U0001fa79 pain point"),
    ("money", "\U0001f4b0 saves money"),
]


def load_config():
    if not CONFIG.exists():
        sys.exit(
            "config.json not found. Copy config.example.json to config.json,\n"
            "then follow the setup steps in this script's docstring."
        )
    cfg = json.loads(CONFIG.read_text())
    if not cfg.get("bot_token") or "PASTE" in cfg.get("bot_token", ""):
        sys.exit("config.json: bot_token is not set. See setup steps in this script's docstring.")
    return cfg


def api(token, method, params):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as r:
        return json.loads(r.read())


def top5_latest_week():
    doc = json.loads(DATA.read_text())
    usecases = doc["usecases"]
    latest = max(u["week"] for u in usecases)
    weekly = [u for u in usecases if u["week"] == latest]
    weekly.sort(key=lambda u: (-u["score"], u["title"]))
    return latest, weekly[:5]


def build_message():
    week, top5 = top5_latest_week()
    lines = [f"\U0001fa84 <b>Claude Code Personal Spellbooks — {week}: this week's top 5 spells</b>", ""]
    for rank, u in enumerate(top5, 1):
        src = u["sources"][0]
        badges = " · ".join(label for key, label in BADGES if u["criteria"][key])
        lines.append(f'{rank}. <a href="{escape(src["url"], quote=True)}"><b>{escape(u["title"])}</b></a>')
        lines.append(f"   {escape(u['summary'])}")
        lines.append(f"   {badges}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    if "--get-chat-id" in sys.argv:
        cfg = load_config()
        updates = api(cfg["bot_token"], "getUpdates", {})
        chats = {
            (m := upd.get("message", {}).get("chat", {})).get("id"): m.get("first_name") or m.get("title", "?")
            for upd in updates.get("result", [])
            if upd.get("message")
        }
        chats.pop(None, None)
        if not chats:
            sys.exit("No messages seen yet — send your bot a message in Telegram first, then rerun.")
        for cid, name in chats.items():
            print(f"chat_id: {cid}  ({name})")
        return

    message = build_message()
    if "--dry-run" in sys.argv:
        print(message)
        return

    cfg = load_config()
    if not cfg.get("chat_id"):
        sys.exit("config.json: chat_id is not set. Run: python3 send_telegram.py --get-chat-id")
    resp = api(cfg["bot_token"], "sendMessage", {
        "chat_id": cfg["chat_id"],
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    })
    if not resp.get("ok"):
        sys.exit(f"Telegram API error: {resp}")
    print("Sent weekly top 5 to Telegram.")


if __name__ == "__main__":
    main()
