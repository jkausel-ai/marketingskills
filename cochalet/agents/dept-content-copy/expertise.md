# Content Copy — Agent Expertise File
**Auto-maintained by pipeline_runner.py after each skill execution**
**Format: append-only. Never manually edit.**
**Purpose: CMO reads this before prompt engineering. Agent learns from own history.**

## Learnings Log

*(No executions yet — expertise builds with each run)*

## [2026-04-10] First Batch Run | Skills: cold-email | Avg CoChalet Score: 5.4/10 | Model: nemotron-120b-free
**What worked:** CoChalet-adapted prompts outperformed generic baseline by avg -0.8 points. Specificity (Laurentides, DW, Fondateurs Alpins) is the single biggest score driver — when the model has CoChalet persona context, emotional resonance and hook scores jump.
**What failed / needed patching:** Generic baselines scored low on specificity (3/10 when no CoChalet context) and brand voice (5/10 — no tutoiement). Some CoChalet outputs violated Four Nevers by using forbidden terms as contrast/comparison language — confirms that prompts need explicit negative-example blocking, not just rule-listing.
**CoChalet insight:** cold-email CoChalet output violated Four Nevers with 'timeshare' and 'fractional ownership' — model used them as contrast/comparison terms when told what CoChalet is not. Fix: add explicit instruction 'do not name forbidden terms even to contrast them.'
---

## [2026-04-10] Skill: cold-email | Score: 8/10 | Model: deepseek/deepseek-chat-v3
**What worked:** French tutoiement cold email with Canon 120k hook and copropriété framing
**What failed / needed patching:** Model included strategic notes in output — needed post-processing to strip
**CoChalet insight:** deepseek reliably self-audits Four Nevers — flags violations in its own notes
---

## [2026-04-11] Skill: cold-email | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: social-content | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: social-content | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: cold-email | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: cold-email | Score: 9/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: social-content | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: cold-email | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---
