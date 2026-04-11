# Strategy — Agent Expertise File
**Auto-maintained by pipeline_runner.py after each skill execution**
**Format: append-only. Never manually edit.**
**Purpose: CMO reads this before prompt engineering. Agent learns from own history.**

## Learnings Log

*(No executions yet — expertise builds with each run)*

## [2026-04-10] First Batch Run | Skills: marketing-psychology, product-marketing-context, content-strategy-d7 | Avg CoChalet Score: 6.3/10 | Model: nemotron-120b-free
**What worked:** CoChalet-adapted prompts outperformed generic baseline by avg +0.3 points. Specificity (Laurentides, DW, Fondateurs Alpins) is the single biggest score driver — when the model has CoChalet persona context, emotional resonance and hook scores jump.
**What failed / needed patching:** Generic baselines scored low on specificity (3/10 when no CoChalet context) and brand voice (5/10 — no tutoiement). Some CoChalet outputs violated Four Nevers by using forbidden terms as contrast/comparison language — confirms that prompts need explicit negative-example blocking, not just rule-listing.
**CoChalet insight:** marketing-psychology output showed strongest emotional resonance when Deep Worker pain (isolation-deprivation, decision fatigue) was named explicitly before solution. content-strategy-d7 violated 'timeshare' — D7 strategy outputs need explicit term guards. product-marketing-context violated 'fractional ownership' — 'fractional' appears in competitive positioning context.
---

## [2026-04-11] Skill: email-sequence | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: email-sequence | Score: 9/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: email-sequence | Score: 9/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 9/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: email-sequence | Score: 9/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 9/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: customer-research | Score: 9/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 8/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: paid-ads | Score: 8/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 8/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: launch-strategy | Score: 9/10 | Model: local:/root/claude-delegate.sh
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 8/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 9/10 | Model: deepseek/deepseek-chat
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---

## [2026-04-11] Skill: content-strategy | Score: 9/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---
