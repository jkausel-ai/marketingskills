# P5 Deploy Guide

Date: 2026-04-10
Time zone: America/New_York
Consensus path: Option B reference package plus targeted Option A diff

## Purpose

This package delivers the Codex P5 lead/worker split as Hermes-ready department files.
It does not replace Hermes `AGENT.md` or `expertise.md`.
It adds `LEAD.md` and `WORKER.md` beside the existing department files.

## Delivery Bundle

Local source root:
`/Users/justinkausel/ClaudeOS-Local/v5/04-codex-build/v5.5/sandbox/repo/p5-delivery`

Files included:
- `DIFF_REPORT.md`
- `P5_DEPLOY.md`
- `agents/dept-seo-content/LEAD.md`
- `agents/dept-seo-content/WORKER.md`
- `agents/dept-cro/LEAD.md`
- `agents/dept-cro/WORKER.md`
- `agents/dept-content-copy/LEAD.md`
- `agents/dept-content-copy/WORKER.md`
- `agents/dept-paid-measurement/LEAD.md`
- `agents/dept-paid-measurement/WORKER.md`
- `agents/dept-growth-retention/LEAD.md`
- `agents/dept-growth-retention/WORKER.md`
- `agents/dept-sales-gtm/LEAD.md`
- `agents/dept-sales-gtm/WORKER.md`
- `agents/dept-strategy/LEAD.md`
- `agents/dept-strategy/WORKER.md`

## Locked Mapping

- `seo-audit` -> `dept-seo-content`
- `email-sequence` -> `dept-content-copy`
- `linkedin-post` -> `dept-content-copy`
- `landing-page` -> `dept-cro`
- `ad-copy` -> `dept-paid-measurement`
- `research-brief` -> `dept-strategy`
- `webinar-campaign` -> `dept-growth-retention`

## OneDrive Hand-Off Path

Recommended mirror on OneDrive:
`/Users/justinkausel/Library/CloudStorage/OneDrive-cochalet.co/EquiVest Properties/Hermes/cochalet-skills/cochalet/agents/`

Copy rule:
- copy each `LEAD.md` and `WORKER.md` into the matching department folder
- do not overwrite `AGENT.md`
- do not overwrite `expertise.md`

## Exact VPS Targets

- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-seo-content/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-seo-content/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-cro/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-cro/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-content-copy/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-content-copy/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-paid-measurement/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-paid-measurement/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-growth-retention/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-growth-retention/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-sales-gtm/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-sales-gtm/WORKER.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-strategy/LEAD.md`
- `/mnt/hermes-output/cochalet-skills/cochalet/agents/dept-strategy/WORKER.md`

## Integration Notes

- Hermes production remains the execution owner for P1 to P4.
- This package is the Codex reference layer for P5 lead/worker orchestration.
- The Codex diff report is at:
  `/Users/justinkausel/ClaudeOS-Local/v5/04-codex-build/v5.5/sandbox/repo/p5-delivery/DIFF_REPORT.md`
- Time zone handling on the Codex side is now hardwired to `America/New_York`.
