"""VPS-local file readers for the CoChalet morning dashboard.

Every reader in this module is defensive: it catches all exceptions and
returns None (or an empty list, per function contract). The dashboard must
render even when upstream files are missing, malformed, stale, or have
unexpected schema. That is the entire point.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

HB_PATH = Path("/root/Hermes/comms-out/HERMES.json")
COST_PATH = Path("/mnt/hermes-output/cost_tracking.jsonl")
V2_PATH = Path("/mnt/hermes-output/v2_alignment_tracking.jsonl")
READS_PATH = Path("/root/Hermes/comms-out/reads.jsonl")
VIOLATIONS_PATH = Path("/var/log/gemini-violations.log")


def _today_utc() -> str:
    """Return the current UTC date as YYYY-MM-DD."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _link_state_from_ts(ts_raw: object) -> str:
    """Classify heartbeat freshness. Unparseable timestamps are RED."""
    try:
        ts_str = str(ts_raw)
        # fromisoformat in 3.11 handles most ISO formats; normalize trailing Z
        if ts_str.endswith("Z"):
            ts_str = ts_str[:-1] + "+00:00"
        ts = datetime.fromisoformat(ts_str)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60.0
        if age_min < 10:
            return "GREEN"
        if age_min <= 30:
            return "AMBER"
        return "RED"
    except Exception:
        return "RED"


def read_hb(path: Path = HB_PATH) -> Optional[dict]:
    """Read the Hermes heartbeat file and annotate it with link_state.

    Returns None on any error (missing file, malformed JSON, etc.).
    """
    data = _read_hb_snapshot(path)
    if data is None:
        data = _read_hb_jsonl_fallback()
    if not isinstance(data, dict):
        return None
    data["link_state"] = _link_state_from_ts(data.get("ts"))
    return data


def _read_hb_snapshot(path: Path = HB_PATH) -> Optional[dict]:
    """Read the current heartbeat snapshot."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        return None


def _read_hb_jsonl_fallback(path: Path | None = None) -> Optional[dict]:
    """Return the newest valid heartbeat from JSONL if the snapshot is bad.

    The heartbeat writer is intentionally cron-simple, so a partial or malformed
    snapshot should not blank the whole dashboard.
    """
    try:
        jsonl_path = path or HB_PATH.with_suffix(".jsonl")
        if not jsonl_path.exists():
            return None
        with open(jsonl_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-200:]
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except Exception:
                continue
            if isinstance(data, dict):
                data.setdefault("callsign", "HERMES-VPS")
                return data
        return None
    except Exception:
        return None


def read_cost_today(path: Path = COST_PATH) -> Optional[dict]:
    """Summarize today's cost-tracking entries.

    Returns a dict with total_usd, top_models (top 3 by cost), and calls.
    Malformed lines are skipped. Returns None only if the file is missing
    or unreadable.
    """
    try:
        if not path.exists():
            return None
        today = _today_utc()
        total = 0.0
        calls = 0
        by_model: dict[str, float] = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = str(entry.get("ts", ""))
                    if not ts.startswith(today):
                        continue
                    cost = float(entry.get("cost_usd", 0.0))
                    model = str(entry.get("model", "unknown"))
                    total += cost
                    calls += 1
                    by_model[model] = by_model.get(model, 0.0) + cost
                except Exception:
                    continue
        top = sorted(by_model.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top_rounded = [(m, round(c, 6)) for m, c in top]
        return {
            "total_usd": round(total, 6),
            "top_models": top_rounded,
            "calls": calls,
        }
    except Exception:
        return None


def read_v2_today(path: Path = V2_PATH) -> Optional[dict]:
    """Summarize today's V2 alignment tracking entries.

    Empty file returns a zeros dict (NOT None). Missing file returns None.
    """
    try:
        if not path.exists():
            return None
        today = _today_utc()
        v2_count = 0
        v1_count = 0
        total = 0
        score_sum = 0.0
        score_n = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = str(entry.get("ts", ""))
                    if not ts.startswith(today):
                        continue
                    version = str(entry.get("thesis_version", ""))
                    if version == "v2":
                        v2_count += 1
                    elif version == "v1":
                        v1_count += 1
                    total += 1
                    try:
                        score_sum += float(entry.get("v2_alignment_score", 0.0))
                        score_n += 1
                    except Exception:
                        pass
                except Exception:
                    continue
        avg = round(score_sum / score_n, 3) if score_n else 0.0
        return {
            "v2_today": v2_count,
            "v1_today": v1_count,
            "total_today": total,
            "avg_score_today": avg,
        }
    except Exception:
        return None


def read_recent_activity(path: Path = READS_PATH, n: int = 5) -> list[dict]:
    """Return the last N parsed JSONL entries from the reads log.

    Returns an empty list on missing file, malformed content, or any error.
    """
    try:
        if not path.exists():
            return []
        out: list[dict] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if isinstance(entry, dict):
                        out.append(entry)
                except Exception:
                    continue
        return out[-n:] if n > 0 else []
    except Exception:
        return []


def read_flags(path: Path = VIOLATIONS_PATH) -> list[str]:
    """Return violation-log lines that contain today's UTC date.

    Returns an empty list on missing file or any error.
    """
    try:
        if not path.exists():
            return []
        today = _today_utc()
        out: list[str] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.rstrip("\n")
                if today in stripped:
                    out.append(stripped)
        return out
    except Exception:
        return []
# ---------------------------------------------------------------------------
# 7-day series readers (appended by Task D)
# ---------------------------------------------------------------------------
import os
import time
from datetime import timedelta

_OUTPUT_ROOT = Path("/mnt/hermes-output")
_SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".cache",
    "node_modules",
    "cmo-blocked-rescue-backups",
    "cmo-resolved",
    "cmo-rejected",
}


def _last_7_utc_dates() -> list[str]:
    """Return 7 UTC date strings, oldest -> newest. Day 6 is today."""
    today = datetime.now(timezone.utc).date()
    return [(today - timedelta(days=6 - i)).strftime("%Y-%m-%d") for i in range(7)]


def read_cost_7d(path: Path = COST_PATH) -> list[float]:
    """Return a 7-element list of cost_usd totals for the last 7 UTC days.

    Oldest -> newest (day 6 is today). Empty file -> zeros. Missing -> [].
    """
    try:
        if not path.exists():
            return []
        dates = _last_7_utc_dates()
        buckets = {d: 0.0 for d in dates}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = str(entry.get("ts", ""))
                    day = ts[:10]
                    if day in buckets:
                        buckets[day] += float(entry.get("cost_usd", 0.0))
                except Exception:
                    continue
        return [round(buckets[d], 6) for d in dates]
    except Exception:
        return []


def read_v2_7d(path: Path = V2_PATH) -> list[int]:
    """Return a 7-element list of v2-count-per-day for the last 7 UTC days."""
    try:
        if not path.exists():
            return []
        dates = _last_7_utc_dates()
        buckets = {d: 0 for d in dates}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if str(entry.get("thesis_version", "")) != "v2":
                        continue
                    ts = str(entry.get("ts", ""))
                    day = ts[:10]
                    if day in buckets:
                        buckets[day] += 1
                except Exception:
                    continue
        return [buckets[d] for d in dates]
    except Exception:
        return []


def read_deliverables_7d(
    hb: Optional[dict] = None,
    root: Path = _OUTPUT_ROOT,
    max_files: int = 5000,
    timeout_s: float = 2.0,
) -> list[int]:
    """Return a 7-element list of deliverable counts for the last 7 UTC days.

    Contract:
      - If ``root`` doesn't exist -> return [] (nothing known).
      - Otherwise build a zero-filled 7-slot list FIRST. Try to fill days
        0-5 from an os.walk of ``root``. If the walk hits ``max_files`` or
        ``timeout_s``, keep whatever buckets we have (likely zeros) rather
        than returning []. Finally, if ``hb["deliverables_today"]`` is
        provided, always overwrite ``series[-1]`` with it — even when the
        walk was capped or blew up mid-iteration.
    """
    try:
        if not root.exists() or not root.is_dir():
            return []
    except Exception:
        return []

    # From here on we commit to the 7-slot contract.
    today_utc = datetime.now(timezone.utc).date()
    buckets = [0] * 7  # buckets[offset]: offset 0 = today, 6 = oldest
    scanned = 0
    start = time.monotonic()
    try:
        capped = False
        for dirpath, dirnames, filenames in os.walk(root):
            if capped:
                break
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for fn in filenames:
                scanned += 1
                if scanned > max_files:
                    capped = True
                    break
                if time.monotonic() - start > timeout_s:
                    capped = True
                    break
                try:
                    mtime = os.path.getmtime(os.path.join(dirpath, fn))
                except Exception:
                    continue
                try:
                    fdate = datetime.fromtimestamp(mtime, tz=timezone.utc).date()
                except Exception:
                    continue
                offset = (today_utc - fdate).days
                if 0 <= offset <= 6:
                    buckets[offset] += 1
    except Exception:
        # Walk blew up: keep partial/zero buckets — hb override still applies.
        pass

    # oldest -> newest
    series = list(reversed(buckets))
    # hb override ALWAYS wins for today, even when walk was capped or failed.
    if isinstance(hb, dict) and "deliverables_today" in hb:
        try:
            series[-1] = int(hb["deliverables_today"])
        except Exception:
            pass
    return series
