#!/usr/bin/env python3
"""Generate a self-contained HTML report from SKILL_DASHBOARD.json."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path


def load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Dashboard payload must be an object")
    return payload


def currency(value: object) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"${value:,.2f}"
    return "$0.00"


def number(value: object) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
    return "0"


def pct(value: object) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:.1f}%"
    return "0.0%"


def clamp_percent(value: object) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return max(0.0, min(float(value), 100.0))
    return 0.0


def trend_label(trend: str) -> tuple[str, str]:
    mapping = {
        "improving": ("Improving", "trend-up"),
        "declining": ("Declining", "trend-down"),
        "stable": ("Stable", "trend-stable"),
        "new": ("New", "trend-new"),
    }
    return mapping.get(trend, ("Unknown", "trend-stable"))


def render_summary(summary: dict[str, object]) -> str:
    cards = [
        ("Total Executions", number(summary.get("total_executions"))),
        ("Total Cost", currency(summary.get("total_cost_usd"))),
        ("Avg Quality", pct(summary.get("avg_quality_score"))),
        ("Four Nevers Flags", number(summary.get("four_nevers_violations"))),
    ]
    return "".join(
        f"<div class='summary-card'><span>{escape(label)}</span><strong>{escape(value)}</strong></div>"
        for label, value in cards
    )


def render_skill_cards(per_skill: dict[str, dict[str, object]]) -> str:
    rows = sorted(
        per_skill.items(),
        key=lambda item: (item[1].get("avg_quality", 0), item[1].get("executions", 0)),
        reverse=True,
    )
    cards = []
    for skill, data in rows:
        trend_text, trend_class = trend_label(str(data.get("trend", "stable")))
        score = clamp_percent(data.get("avg_quality"))
        cards.append(
            f"""
            <article class="skill-card">
              <header>
                <h3>{escape(skill)}</h3>
                <span class="trend {trend_class}">{escape(trend_text)}</span>
              </header>
              <div class="bar">
                <div class="bar-fill" style="width: {score:.1f}%"></div>
              </div>
              <dl>
                <div><dt>Avg quality</dt><dd>{pct(data.get("avg_quality"))}</dd></div>
                <div><dt>Executions</dt><dd>{number(data.get("executions"))}</dd></div>
                <div><dt>Total cost</dt><dd>{currency(data.get("total_cost"))}</dd></div>
                <div><dt>Best model</dt><dd>{escape(str(data.get("best_model", "-")))}</dd></div>
                <div><dt>Published</dt><dd>{number(data.get("published"))}</dd></div>
              </dl>
            </article>
            """
        )
    return "".join(cards)


def render_model_rows(per_model: dict[str, dict[str, object]]) -> str:
    rows = sorted(
        per_model.items(),
        key=lambda item: (item[1].get("avg_quality", 0), item[1].get("quality_per_dollar", 0)),
        reverse=True,
    )
    rendered = []
    for model, data in rows:
        rendered.append(
            "<tr>"
            f"<td>{escape(model)}</td>"
            f"<td>{number(data.get('executions'))}</td>"
            f"<td>{pct(data.get('avg_quality'))}</td>"
            f"<td>{currency(data.get('total_cost'))}</td>"
            f"<td>{number(data.get('quality_per_dollar'))}</td>"
            "</tr>"
        )
    return "".join(rendered)


def render_efficiency(per_model: dict[str, dict[str, object]]) -> str:
    rows = sorted(
        per_model.items(),
        key=lambda item: item[1].get("quality_per_dollar", 0),
        reverse=True,
    )
    items = []
    for index, (model, data) in enumerate(rows, start=1):
        items.append(
            f"<li><span>{index}. {escape(model)}</span><strong>{number(data.get('quality_per_dollar'))}</strong></li>"
        )
    return "".join(items)


def build_html(dashboard: dict[str, object]) -> str:
    summary = dashboard.get("summary", {})
    if not isinstance(summary, dict):
        raise ValueError("summary must be an object")
    per_skill = dashboard.get("per_skill", {})
    per_model = dashboard.get("per_model", {})
    if not isinstance(per_skill, dict) or not isinstance(per_model, dict):
        raise ValueError("per_skill and per_model must be objects")

    period = ""
    if dashboard.get("period_start") and dashboard.get("period_end"):
        period = f"{escape(str(dashboard['period_start']))} to {escape(str(dashboard['period_end']))}"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CoChalet Skill Effectiveness Report</title>
  <style>
    :root {{
      --bg: #f4efe5;
      --surface: #fffdf9;
      --ink: #12352d;
      --muted: #58675f;
      --line: #d8cfc2;
      --accent: #c58b45;
      --accent-strong: #9a6632;
      --up: #1d7a5a;
      --down: #b55239;
      --stable: #6d6a64;
      --new: #32669a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Iowan Old Style", "Palatino Linotype", serif;
      background:
        radial-gradient(circle at top right, rgba(197, 139, 69, 0.16), transparent 26%),
        linear-gradient(180deg, #f8f3ea 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 48px 24px 72px; }}
    .hero {{
      background: rgba(255, 253, 249, 0.82);
      backdrop-filter: blur(6px);
      border: 1px solid rgba(216, 207, 194, 0.9);
      border-radius: 24px;
      padding: 32px;
      box-shadow: 0 18px 50px rgba(18, 53, 45, 0.08);
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(2rem, 5vw, 3.5rem); }}
    .subtitle {{ color: var(--muted); max-width: 64ch; line-height: 1.5; }}
    .summary-grid {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      margin-top: 28px;
    }}
    .summary-card, .panel, .skill-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(18, 53, 45, 0.06);
    }}
    .summary-card {{ padding: 18px 20px; }}
    .summary-card span {{ display: block; color: var(--muted); font-size: 0.92rem; }}
    .summary-card strong {{ display: block; margin-top: 8px; font-size: 1.8rem; }}
    .layout {{
      display: grid;
      gap: 24px;
      margin-top: 28px;
      grid-template-columns: 2fr 1fr;
    }}
    .panel {{ padding: 24px; }}
    .panel h2 {{ margin-top: 0; font-size: 1.25rem; }}
    .skill-grid {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }}
    .skill-card {{ padding: 18px; }}
    .skill-card header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .skill-card h3 {{ margin: 0; font-size: 1.1rem; }}
    .bar {{
      height: 10px;
      background: #ece4d7;
      border-radius: 999px;
      overflow: hidden;
      margin-bottom: 14px;
    }}
    .bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--accent), var(--accent-strong));
    }}
    dl {{
      margin: 0;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px 16px;
    }}
    dt {{ color: var(--muted); font-size: 0.86rem; }}
    dd {{ margin: 4px 0 0; font-weight: 600; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.96rem;
    }}
    th, td {{
      padding: 12px 0;
      text-align: left;
      border-bottom: 1px solid var(--line);
    }}
    th {{ color: var(--muted); font-weight: 600; }}
    .trend {{
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .trend-up {{ background: rgba(29, 122, 90, 0.12); color: var(--up); }}
    .trend-down {{ background: rgba(181, 82, 57, 0.12); color: var(--down); }}
    .trend-stable {{ background: rgba(109, 106, 100, 0.12); color: var(--stable); }}
    .trend-new {{ background: rgba(50, 102, 154, 0.12); color: var(--new); }}
    .leaderboard {{ list-style: none; padding: 0; margin: 0; }}
    .leaderboard li {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid var(--line);
    }}
    @media (max-width: 920px) {{
      .layout {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <p class="subtitle">CoChalet skill effectiveness dashboard generated from Hermes execution logs and COS OPS quality reviews.{f" Reporting window: {period}." if period else ""}</p>
      <h1>Skill Effectiveness Report</h1>
      <div class="summary-grid">{render_summary(summary)}</div>
    </section>

    <section class="layout">
      <div class="panel">
        <h2>Per-Skill Performance</h2>
        <div class="skill-grid">{render_skill_cards(per_skill)}</div>
      </div>
      <aside class="panel">
        <h2>Cost Efficiency Leaderboard</h2>
        <ol class="leaderboard">{render_efficiency(per_model)}</ol>
      </aside>
    </section>

    <section class="panel" style="margin-top: 24px;">
      <h2>Per-Model Comparison</h2>
      <table>
        <thead>
          <tr>
            <th>Model</th>
            <th>Executions</th>
            <th>Avg Quality</th>
            <th>Total Cost</th>
            <th>Quality/$</th>
          </tr>
        </thead>
        <tbody>{render_model_rows(per_model)}</tbody>
      </table>
    </section>
  </div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    dashboard = load_json(args.input.expanduser())
    html = build_html(dashboard)
    output = args.output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
