"""Direct OAuth delegate slash commands for CoChalet.

The point of this plugin is to bypass the Gemini driver for work that should
always execute through the Claude Code OAuth delegates. It returns quickly by
starting the swarm job in the background and writing the full review to CMO
inbox.
"""
from __future__ import annotations

import logging
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

SCRIPT = Path("/root/scripts/hermes-sonnet-swarm.sh")
OUT_DIR = Path("/mnt/hermes-output/cmo-inbox/sonnet-swarm")
PREVIEW_CHARS = 4500
SECTION_PREVIEW_CHARS = 9000


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
    path = _resolve_output(raw_args)
    if path is None:
        return f"No Sonnet swarm outputs found yet in {OUT_DIR}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    preview = text[:PREVIEW_CHARS]
    suffix = ""
    if len(text) > PREVIEW_CHARS:
        suffix = f"\n\n[Preview truncated; full file: {path}]"
    return f"SONNET_SWARM_LATEST\nFile: {path}\n\n{preview}{suffix}"


def _resolve_output(raw_args: str = "") -> Path | None:
    arg = raw_args.strip()
    outputs = _latest_files("*.md", 20)
    if not outputs:
        return None
    if not arg:
        return outputs[0]

    token = arg.split()[0].strip()
    if token.isdigit():
        idx = max(1, int(token)) - 1
        return outputs[idx] if idx < len(outputs) else None

    candidate = Path(token)
    if candidate.is_file():
        return candidate
    candidate = OUT_DIR / token
    if candidate.is_file():
        return candidate

    for path in outputs:
        if token in path.name:
            return path
    return outputs[0]


def _extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^(##+\s+{re.escape(heading)}\s*)$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""

    level = len(match.group(1)) - len(match.group(1).lstrip("#"))
    next_heading = re.compile(rf"^#{{1,{level}}}\s+", re.MULTILINE)
    next_match = next_heading.search(text, match.end())
    end = next_match.start() if next_match else len(text)
    return text[match.start():end].strip()


def _cap(text: str, limit: int = SECTION_PREVIEW_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[Truncated; use /swarm-latest or the full file path for more.]"


def _swarm_help(raw_args: str = "") -> str:
    return "\n".join([
        "SONNET_SWARM_COMMANDS",
        "/swarm <task or file>          Start a Sonnet OAuth org-marketing review",
        "/swarm-status                  List recent outputs and logs",
        "/swarm-latest [n|filename]     Preview latest output",
        "/swarm-brief [n|filename]      Executive verdict + final next actions",
        "/swarm-backlog [n|filename]    Optimization backlog + final actions",
        "/swarm-compliance [n|filename] Compliance/Four Nevers section",
        "/swarm-section <heading>       Read a named section from latest output",
        "",
        "Tip: run these directly, not through /btw. Direct commands bypass Gemini.",
    ])


def _section_bundle(raw_args: str, title: str, headings: list[str]) -> str:
    path = _resolve_output(raw_args)
    if path is None:
        return f"No Sonnet swarm outputs found yet in {OUT_DIR}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    parts = [section for heading in headings if (section := _extract_section(text, heading))]
    if not parts:
        return f"{title}\nFile: {path}\n\nNo matching sections found."
    return f"{title}\nFile: {path}\n\n" + _cap("\n\n---\n\n".join(parts))


def _swarm_brief(raw_args: str = "") -> str:
    return _section_bundle(
        raw_args,
        "SONNET_SWARM_BRIEF",
        ["Executive Verdict", "Final Next Actions"],
    )


def _swarm_backlog(raw_args: str = "") -> str:
    return _section_bundle(
        raw_args,
        "SONNET_SWARM_BACKLOG",
        ["Optimization Backlog", "Final Next Actions"],
    )


def _swarm_compliance(raw_args: str = "") -> str:
    return _section_bundle(
        raw_args,
        "SONNET_SWARM_COMPLIANCE",
        ["Compliance Check"],
    )


def _swarm_section(raw_args: str = "") -> str:
    heading = raw_args.strip()
    if not heading:
        return "Usage: /swarm-section <section heading>"
    path = _resolve_output("")
    if path is None:
        return f"No Sonnet swarm outputs found yet in {OUT_DIR}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    section = _extract_section(text, heading)
    if not section:
        headings = [
            line.lstrip("#").strip()
            for line in text.splitlines()
            if line.startswith("## ")
        ]
        return "Section not found. Available sections:\n- " + "\n- ".join(headings)
    return f"SONNET_SWARM_SECTION\nFile: {path}\n\n" + _cap(section)


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
    ctx.register_command(
        "swarm-help",
        _swarm_help,
        description="Show Sonnet swarm commands",
    )
    ctx.register_command(
        "swarm-brief",
        _swarm_brief,
        description="Show executive verdict and next actions from latest swarm",
    )
    ctx.register_command(
        "swarm-backlog",
        _swarm_backlog,
        description="Show optimization backlog from latest swarm",
    )
    ctx.register_command(
        "swarm-compliance",
        _swarm_compliance,
        description="Show compliance/Four Nevers section from latest swarm",
    )
    ctx.register_command(
        "swarm-section",
        _swarm_section,
        description="Show a named section from latest swarm",
    )
    logger.info("cochalet-delegate-router plugin registered")
