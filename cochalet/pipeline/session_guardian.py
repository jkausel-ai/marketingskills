#!/usr/bin/env python3
"""
session_guardian.py — COS Session Guardian (Hermes VPS adaptation)
Per EM2A mesh directive Apr 10 2026.

Monitors message count per TG session and triggers Memora checkpoints
at 20/30/40/50 message thresholds.

Usage:
  Called by gateway on each message: python3 session_guardian.py --increment
  Called to check current state:     python3 session_guardian.py --status
  Called to reset session count:     python3 session_guardian.py --reset

State file: /tmp/hermes-session-msgcount
Thresholds:
  20 = first checkpoint (Memora save)
  30 = full checkpoint (Memora + shared-memory)
  40 = warning (TG message to user + Memora)
  50 = CRITICAL — trigger auto_bootdown.py immediately
"""

import json
import os
import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("/tmp/hermes-session-msgcount")
MEMORA_DB = Path("/root/.local/share/memora/memories.db")
SHARED_MEM = Path("/mnt/hermes-output/memory/shared-memory.jsonl")
BOOTDOWN_SCRIPT = Path("/mnt/hermes-output/cochalet-skills/cochalet/pipeline/auto_bootdown.py")
ENV_FILE = Path("/root/.hermes/.env")

THRESHOLDS = {
    20: "checkpoint",
    30: "full_checkpoint",
    40: "warning",
    50: "critical_bootdown",
}

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_state():
    if not STATE_FILE.exists():
        return {"count": 0, "session_start": now_ts(), "last_checkpoint": 0}
    try:
        return json.loads(STATE_FILE.read_text())
    except:
        return {"count": 0, "session_start": now_ts(), "last_checkpoint": 0}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state))

def write_memora(content, importance=0.7):
    """Write checkpoint to Memora. Uses metadata type=note to bypass auto-classifier."""
    try:
        db = sqlite3.connect(str(MEMORA_DB))
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        db.execute(
            "INSERT INTO memories (content, metadata, tags, created_at, importance, access_count) VALUES (?,?,?,?,?,?)",
            (content[:500], json.dumps({"type": "note", "source": "session_guardian"}),
             json.dumps(["note"]), ts, importance, 0)
        )
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"Memora write failed: {e}", file=sys.stderr)
        return False

def write_shared_memory(entry):
    try:
        with open(SHARED_MEM, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"shared-memory write failed: {e}", file=sys.stderr)

def tg_send(msg):
    """Send TG warning message via Bot API."""
    import subprocess
    try:
        bot = os.popen("grep '^TELEGRAM_BOT_TOKEN=' /root/.hermes/.env | cut -d= -f2 | tr -d '\"'").read().strip()
        chat = os.popen("grep '^TELEGRAM_HOME_CHANNEL=' /root/.hermes/.env | cut -d= -f2 | tr -d '\"'").read().strip()
        if bot and chat:
            import urllib.parse
            encoded = urllib.parse.quote(msg)
            subprocess.Popen(
                ["curl", "-s", "-X", "POST",
                 f"https://api.telegram.org/bot{bot}/sendMessage",
                 "-d", f"chat_id={chat}&text={encoded}"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                start_new_session=True
            )
    except: pass

def trigger_bootdown():
    """Fire auto_bootdown.py async."""
    import subprocess
    subprocess.Popen(
        [sys.executable, str(BOOTDOWN_SCRIPT), "--reason", "session-guardian-50msg"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True
    )

def handle_threshold(count, level):
    ts = now_ts()
    print(f"[{ts}] GUARDIAN: threshold={level} at msg {count}", flush=True)

    if level == "checkpoint":
        write_memora(
            f"SESSION CHECKPOINT msg=20 at {ts}. Session active, monitoring continued.",
            importance=0.5
        )

    elif level == "full_checkpoint":
        write_memora(
            f"SESSION FULL CHECKPOINT msg=30 at {ts}. Context growing — consider bootdown if complex work done.",
            importance=0.6
        )
        write_shared_memory({
            "ts": ts, "from": "Hermes", "type": "guardian_checkpoint",
            "content": f"Session guardian: 30 messages reached at {ts}. Context checkpoint.",
            "msg_count": count,
        })

    elif level == "warning":
        warning_msg = f"⚠️ Session Guardian: 40 messages in this TG session. Context pressure building. Consider /bootdown soon."
        tg_send(warning_msg)
        write_memora(
            f"SESSION WARNING msg=40 at {ts}. TG warning sent. Bootdown recommended.",
            importance=0.8
        )
        write_shared_memory({
            "ts": ts, "from": "Hermes", "type": "guardian_warning",
            "content": f"Session guardian: 40 messages — context warning at {ts}.",
            "msg_count": count,
        })

    elif level == "critical_bootdown":
        critical_msg = f"🚨 Session Guardian: 50 messages reached. Triggering auto-bootdown NOW."
        tg_send(critical_msg)
        trigger_bootdown()
        write_shared_memory({
            "ts": ts, "from": "Hermes", "type": "guardian_critical",
            "content": f"Session guardian: 50 messages — auto-bootdown triggered at {ts}.",
            "msg_count": count,
        })


def increment():
    state = load_state()
    state["count"] += 1
    count = state["count"]

    # Check if we just hit a threshold
    for threshold, level in sorted(THRESHOLDS.items()):
        if count == threshold:
            handle_threshold(count, level)
            state["last_checkpoint"] = count
            break

    save_state(state)
    return count

def status():
    state = load_state()
    count = state.get("count", 0)
    start = state.get("session_start", "unknown")
    next_threshold = next((t for t in sorted(THRESHOLDS.keys()) if t > count), None)
    print(f"Session messages: {count}")
    print(f"Session start: {start}")
    print(f"Next threshold: {next_threshold} ({THRESHOLDS.get(next_threshold,'none')})")
    return state

def reset():
    save_state({"count": 0, "session_start": now_ts(), "last_checkpoint": 0})
    print("Session count reset to 0")


if __name__ == "__main__":
    if "--increment" in sys.argv:
        count = increment()
        print(f"msg_count={count}")
    elif "--status" in sys.argv:
        status()
    elif "--reset" in sys.argv:
        reset()
    else:
        status()
    sys.exit(0)
