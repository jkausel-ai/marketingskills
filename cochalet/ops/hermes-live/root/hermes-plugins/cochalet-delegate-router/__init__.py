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
    logger.info("cochalet-delegate-router plugin registered")
