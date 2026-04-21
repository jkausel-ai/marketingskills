"""Direct OAuth delegate slash commands for CoChalet.

The point of this plugin is to bypass the Gemini driver for work that should
always execute through the Claude Code OAuth delegates. It returns quickly by
starting the swarm job in the background and writing the full review to CMO
inbox.
"""
from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

SCRIPT = Path("/root/scripts/hermes-sonnet-swarm.sh")
OUT_DIR = Path("/mnt/hermes-output/cmo-inbox/sonnet-swarm")
PREVIEW_CHARS = 4500


def _run_sonnet_swarm(raw_args: str = "") -> str:
    task = raw_args.strip()
    if not task:
        return "Usage: /sonnet-swarm <task or file path>"
    if not SCRIPT.exists():
        return f"Delegate router script missing: {SCRIPT}"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = OUT_DIR / f"{stamp}-sonnet-swarm.log"

    with log_path.open("w", encoding="utf-8") as log:
        subprocess.Popen(
            [str(SCRIPT), task],
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    return (
        "SONNET_SWARM_STARTED\n"
        f"Task: {task[:240]}\n"
        f"Log: {log_path}\n"
        f"Output dir: {OUT_DIR}\n"
        "Gemini has been bypassed; Sonnet OAuth is doing the review."
    )


def _latest_files(pattern: str, limit: int = 5) -> list[Path]:
    if not OUT_DIR.exists():
        return []
    files = [p for p in OUT_DIR.glob(pattern) if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def _format_size(path: Path) -> str:
    size = path.stat().st_size
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f}MB"
    if size >= 1024:
        return f"{size / 1024:.1f}KB"
    return f"{size}B"


def _swarm_status(raw_args: str = "") -> str:
    outputs = _latest_files("*.md", 5)
    logs = _latest_files("*.log", 5)
    if not outputs and not logs:
        return f"No Sonnet swarm runs found yet in {OUT_DIR}"

    lines = ["SONNET_SWARM_STATUS", f"Output dir: {OUT_DIR}"]
    if outputs:
        lines.append("\nLatest outputs:")
        for path in outputs:
            lines.append(f"- {path.name} ({_format_size(path)})")
    if logs:
        lines.append("\nLatest logs:")
        for path in logs:
            lines.append(f"- {path.name} ({_format_size(path)})")
    return "\n".join(lines)


def _swarm_latest(raw_args: str = "") -> str:
    outputs = _latest_files("*.md", 1)
    if not outputs:
        return f"No Sonnet swarm outputs found yet in {OUT_DIR}"
    path = outputs[0]
    text = path.read_text(encoding="utf-8", errors="ignore")
    preview = text[:PREVIEW_CHARS]
    suffix = ""
    if len(text) > PREVIEW_CHARS:
        suffix = f"\n\n[Preview truncated; full file: {path}]"
    return f"SONNET_SWARM_LATEST\nFile: {path}\n\n{preview}{suffix}"


def register(ctx: Any) -> None:
    ctx.register_command(
        "sonnet-swarm",
        _run_sonnet_swarm,
        description="Run a CoChalet org-marketing swarm through Sonnet OAuth",
    )
    ctx.register_command(
        "swarm",
        _run_sonnet_swarm,
        description="Alias for /sonnet-swarm",
    )
    ctx.register_command(
        "swarm-status",
        _swarm_status,
        description="List recent Sonnet swarm outputs and logs",
    )
    ctx.register_command(
        "sonnet-swarm-status",
        _swarm_status,
        description="List recent Sonnet swarm outputs and logs",
    )
    ctx.register_command(
        "swarm-latest",
        _swarm_latest,
        description="Preview the latest Sonnet swarm output",
    )
    ctx.register_command(
        "sonnet-swarm-latest",
        _swarm_latest,
        description="Preview the latest Sonnet swarm output",
    )
    logger.info("cochalet-delegate-router plugin registered")
