# Hermes Diff — P1 to P4

Date: 2026-04-10
Reference package: `beb932c`
Consensus path: Option B plus targeted Option A diff

## Summary

Hermes already covers P1 to P4 in production with deeper CoChalet integration than the sandbox reference. The sandbox still adds value as a cleaner generic architecture and as the source for P5 lead/worker prompts.

## P1 — Expertise

- Hermes keeps expertise in live department files under `agents/dept-*/expertise.md` and appends learnings after executions.
- Sandbox P1 originally bootstrapped static expertise snapshots from a single command.
- Result: Hermes is stronger operationally. Sandbox is useful as a template generator, not as the final expertise loop.

## P2 — Till Done Retry

- Hermes runs verify checks against Four Nevers, structure, and quality score, then retries up to 3 times before marking output `BLOCKED`.
- Sandbox P2 retries against missing required sections and minimum word count only.
- Result: Hermes has the stronger production retry loop. Sandbox remains a readable reference implementation of the retry pattern.

## P3 — Orchestrator Prompting

- Hermes injects canon context, department agent context, adapted skill prompt text, and recent expertise through `cmo_prompt_engineer`.
- Sandbox P3 engineers prompts from a generic template plus local expertise and role files.
- Result: Hermes is stronger for live CoChalet execution. Sandbox is cleaner as a portable prompt-engineering reference.

## P4 — Parallel Dispatch

- Hermes runs two real models in parallel for P0 work and scores the winner.
- Sandbox P4 simulates lead/worker fan-out and merges worker slices into one synthesis.
- Result: Hermes is stronger for real execution. Sandbox still contributes a clean lead/worker orchestration pattern that Hermes does not yet package as first-class P5 assets.

## What Sandbox Still Adds

- Explicit `LEAD.md` and `WORKER.md` prompt assets as a reusable split-brain pattern.
- A small, composable reference implementation that is easier to port than the full Hermes production orchestrator.
- A department-aware packaging layer that now maps legacy generic aliases into the seven CoChalet departments.

## P5 Packaging Map

- `seo-audit` -> `dept-seo-content`
- `email-sequence` -> `dept-content-copy`
- `linkedin-post` -> `dept-content-copy`
- `landing-page` -> `dept-cro`
- `ad-copy` -> `dept-paid-measurement`
- `research-brief` -> `dept-strategy`
- `webinar-campaign` -> `dept-growth-retention`

## Time Zone Update

The sandbox support layer now hardwires `America/New_York`, and the Codex consensus watcher now logs and writes state in `America/New_York` as well.
