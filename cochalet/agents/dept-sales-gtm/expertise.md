# Sales GTM — Agent Expertise File
**Auto-maintained by pipeline_runner.py after each skill execution**
**Format: append-only. Never manually edit.**
**Purpose: CMO reads this before prompt engineering. Agent learns from own history.**

## Learnings Log

*(No executions yet — expertise builds with each run)*

## [2026-04-10] First Batch Run | Skills: revops, sales-enablement, launch-strategy, pricing-strategy, competitor-alternatives, customer-research | Avg CoChalet Score: 7.4/10 | Model: nemotron-120b-free
**What worked:** CoChalet-adapted prompts outperformed generic baseline by avg +1.3 points. Specificity (Laurentides, DW, Fondateurs Alpins) is the single biggest score driver — when the model has CoChalet persona context, emotional resonance and hook scores jump.
**What failed / needed patching:** Generic baselines scored low on specificity (3/10 when no CoChalet context) and brand voice (5/10 — no tutoiement). Some CoChalet outputs violated Four Nevers by using forbidden terms as contrast/comparison language — confirms that prompts need explicit negative-example blocking, not just rule-listing.
**CoChalet insight:** launch-strategy and competitor-alternatives both scored +2.0 delta — context about Casadora and Pacaso competition drove strong specificity. sales-enablement +1.8 with deep DW persona framing. pricing-strategy had 'fractional' violation — avoid price-adjacent comparisons without explicit term blocking.
---

## [2026-04-11] Skill: content-strategy | Score: 8/10 | Model: google/gemini-2.5-flash
**What worked:** Execution completed — qualitative review pending
**What failed / needed patching:** None noted
**CoChalet insight:** Review deliverable for patterns to capture here
---
