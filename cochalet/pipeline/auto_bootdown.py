#!/usr/bin/env python3
"""
auto_bootdown.py — Hermes COS Bootdown Generator
Canonical format per EM2A mesh directive Apr 10 2026.

Triggers:
  A. systemd ExecStop hook (via hermes-bootdown-hook.sh)
  B. session_guardian.py at 50-message threshold
  C. Manual: python3 auto_bootdown.py [--reason "description"]

Output:
  /mnt/hermes-output/deliverables/BOOTDOWN_HERMES_{DATE}.md
  shared-memory.jsonl entry (type=bootdown)
  Memora memory (metadata={"type":"note"})
  Mesh send to hub

Must exit in <10s when called from ExecStop. Non-blocking on mesh send.
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
DELIVERABLES = Path("/mnt/hermes-output/deliverables")
SHARED_MEM = Path("/mnt/hermes-output/memory/shared-memory.jsonl")
DEPLOYS_LOG = Path("/var/log/dashboard-deploys.jsonl")
PROCESSED_LOG = Path("/var/log/mesh-poll-processed.log")
MEMORA_DB = Path("/root/.local/share/memora/memories.db")
ENV_FILE = Path("/root/.hermes/.env")

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def now_edt():
    # Simple EDT offset (UTC-4 in summer)
    from datetime import timedelta
    return (datetime.now(timezone.utc) - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M EDT")

def now_date():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

def log(msg):
    print(f"[{now_ts()}] BOOTDOWN: {msg}", flush=True)

def read_shared_memory(n=5):
    """Read last N entries from shared-memory.jsonl."""
    if not SHARED_MEM.exists():
        return []
    lines = SHARED_MEM.read_text().strip().splitlines()
    entries = []
    for line in reversed(lines[-n*2:]):
        try:
            entries.append(json.loads(line))
        except: pass
        if len(entries) >= n:
            break
    return list(reversed(entries))

def get_last_deploy():
    """Get last CF Pages deploy record."""
    if not DEPLOYS_LOG.exists():
        return None
    lines = DEPLOYS_LOG.read_text().strip().splitlines()
    for line in reversed(lines):
        try:
            return json.loads(line)
        except: pass
    return None

def get_service_state(service):
    """Check systemd service state."""
    try:
        r = subprocess.run(
            ["systemctl", "--user", "is-active", service],
            capture_output=True, text=True, timeout=3,
            env={**os.environ, "XDG_RUNTIME_DIR": "/run/user/0"}
        )
        return r.stdout.strip()
    except:
        return "unknown"

def get_mesh_processed_count():
    """Count processed mesh messages."""
    if not PROCESSED_LOG.exists():
        return 0
    return len([l for l in PROCESSED_LOG.read_text().splitlines() if l.strip()])

def get_memora_count():
    """Count Memora memories."""
    try:
        import sqlite3
        db = sqlite3.connect(str(MEMORA_DB))
        count = db.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        db.close()
        return count
    except:
        return "unknown"

def get_hermes_version():
    """Get installed hermes-agent version."""
    try:
        import importlib.metadata
        return importlib.metadata.version("hermes-agent")
    except:
        return "unknown"

def write_memora(content):
    """Write bootdown summary to Memora. Always uses metadata type=note to suppress auto-classifier."""
    try:
        import sqlite3
        from datetime import datetime, timezone
        db = sqlite3.connect(str(MEMORA_DB))
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        db.execute(
            "INSERT INTO memories (content, metadata, tags, created_at, importance, access_count) VALUES (?,?,?,?,?,?)",
            (content[:500], json.dumps({"type": "note", "source": "auto_bootdown"}), json.dumps(["note"]), ts, 0.8, 0)
        )
        db.commit()
        db.close()
        return True
    except Exception as e:
        log(f"Memora write failed: {e}")
        return False

def mesh_send_async(subject, body):
    """Fire-and-forget mesh send. Never blocks."""
    try:
        subprocess.Popen(
            ["bash", "/root/scripts/mesh-send.sh", "hub", "status", "P1", subject, body],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    except:
        pass

def generate_bootdown(reason="auto", open_items=None):
    """Generate the canonical bootdown document."""
    ts = now_ts()
    edt = now_edt()
    date_slug = now_date()

    # Gather state
    recent_mem = read_shared_memory(5)
    last_deploy = get_last_deploy()
    gw_state = get_service_state("hermes-gateway.service")
    watcher_state = get_service_state("hermes-dashboard-watcher.service")
    mesh_count = get_mesh_processed_count()
    memora_count = get_memora_count()
    hermes_ver = get_hermes_version()

    # Build recent work summary from shared-memory
    recent_work = []
    for entry in recent_mem:
        t = entry.get("type", "?")
        c = entry.get("content", "")[:100]
        recent_work.append(f"- [{t}] {c}")

    deploy_info = "No recent deploy"
    if last_deploy:
        deploy_info = f"ID={last_deploy.get('deploy_id','?')} | reason={last_deploy.get('reason','?')} | live={last_deploy.get('live_ok','?')}"

    # Default open items if not provided
    if not open_items:
        open_items = [
            "**GitHub token rotation** — revoke ghp_9c1A32...PeTO at github.com/settings/tokens",
            "**cochalet.co Luxary typo** — AWS static deploy, not in GitHub",
            "**7-dept marketing agent build** — SDD ready at docs/plans/",
            "**Empire image DBA** — laptop screen blur + FR version",
        ]

    open_items_md = "\n".join(f"{i+1}. {item}" for i, item in enumerate(open_items))

    content = f"""# BOOTDOWN — HERMES
**Date:** {edt} | **Node:** ALPINE-HERMES-01 | **Role:** Marketing Executor + VPS Infra
**Model:** claude-sonnet-4-6 | **Hermes:** v{hermes_ver}
**Trigger:** {reason}

---

## Services State at Bootdown

| Service | Status |
|---------|--------|
| hermes-gateway.service | {gw_state} |
| hermes-dashboard-watcher.service | {watcher_state} |
| Dashboard last deploy | {deploy_info} |
| Mesh messages processed | {mesh_count} |
| Memora memories | {memora_count} |

---

## What Was Done (recent shared-memory entries)

{chr(10).join(recent_work) or "No shared-memory entries found."}

---

## Key Discoveries

1. COS session protocols now implemented (bootdown/bootup/sessionsync + Session Guardian)
2. Hermes-agent updated v0.7.0 → v0.8.0 (110 upstream commits, clean merge)
3. Memora tag validation bug: always pass metadata={{"type":"note"}} to suppress auto-classifier
4. Dashboard feedback loop: never watch deploy-dir files (watcher must watch source only)
5. cochalet.co "Luxary" typo is in AWS static deploy — NOT in any GitHub repo

---

## Open Items for Next Session

### IMMEDIATE
{open_items_md}

### BOOTUP COMMAND
```
bash /root/scripts/mesh-poll.sh --quiet && \\
python3 /mnt/hermes-output/cochalet-skills/cochalet/pipeline/startup_check.py
```

---

## Infrastructure

- hermes-gateway.service: Restart=always, TZ=America/Toronto
- hermes-dashboard-watcher.service: 60s debounce, 120s min-interval
- Cron: watchdog */5, mesh-poll */1, aggregator+sessionsync */6h
- Startup check: 17/17 checks (extended Apr 10)
- Session Guardian: thresholds 20/30/40/50 msgs → Memora checkpoint

---

## Recovery

```bash
# If gateway is down:
XDG_RUNTIME_DIR=/run/user/0 systemctl --user start hermes-gateway.service
# Verify:
python3 /mnt/hermes-output/cochalet-skills/cochalet/pipeline/startup_check.py
# Check latest bootdown:
ls -lt /mnt/hermes-output/deliverables/BOOTDOWN_HERMES_*.md | head -3
```

---

*ALPINE-HERMES-01 | BOOTDOWN COMPLETE | {edt}*
*Generated by auto_bootdown.py | reason={reason}*
"""

    # Write the file
    out_path = DELIVERABLES / f"BOOTDOWN_HERMES_{date_slug}.md"
    DELIVERABLES.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content)
    log(f"Written: {out_path}")

    # Append to shared-memory.jsonl
    summary = f"BOOTDOWN HERMES {edt}: gw={gw_state}, deploy={deploy_info[:50]}, mesh={mesh_count}, memora={memora_count}, reason={reason}"
    entry = {
        "ts": ts,
        "from": "Hermes",
        "type": "bootdown",
        "id": f"bootdown-{date_slug}",
        "content": summary,
        "file": str(out_path),
    }
    with open(SHARED_MEM, "a") as f:
        f.write(json.dumps(entry) + "\n")
    log("Appended to shared-memory.jsonl")

    # Write to Memora
    memora_content = f"BOOTDOWN {edt} reason={reason}: gw={gw_state}, mesh={mesh_count}, memora={memora_count}, deploy={deploy_info[:80]}"
    write_memora(memora_content)
    log("Memora entry written")

    # Send mesh (async, non-blocking)
    mesh_send_async(
        f"HERMES BOOTDOWN — {edt}",
        f"Bootdown written. reason={reason} gw={gw_state} mesh={mesh_count} memora={memora_count} deploy={deploy_info[:60]} file={out_path.name}"
    )
    log("Mesh send queued (async)")

    return str(out_path)


if __name__ == "__main__":
    reason = "manual"
    if "--reason" in sys.argv:
        idx = sys.argv.index("--reason")
        if idx + 1 < len(sys.argv):
            reason = sys.argv[idx + 1]

    log(f"Starting bootdown generation (reason={reason})")
    path = generate_bootdown(reason=reason)
    log(f"COMPLETE: {path}")
    sys.exit(0)
