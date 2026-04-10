# CRO — Agent Expertise File
**Auto-maintained by pipeline_runner.py after each skill execution**
**Format: append-only. Never manually edit.**
**Purpose: CMO reads this before prompt engineering. Agent learns from own history.**

## Learnings Log

*(No executions yet — expertise builds with each run)*

## [2026-04-10] First Batch Run | Skills: page-cro, signup-flow-cro, onboarding-cro, form-cro, popup-cro, ab-test-setup, copy-editing | Avg CoChalet Score: 7.1/10 | Model: nemotron-120b-free
**What worked:** CoChalet-adapted prompts outperformed generic baseline by avg +0.1 points. Specificity (Laurentides, DW, Fondateurs Alpins) is the single biggest score driver — when the model has CoChalet persona context, emotional resonance and hook scores jump.
**What failed / needed patching:** Generic baselines scored low on specificity (3/10 when no CoChalet context) and brand voice (5/10 — no tutoiement). Some CoChalet outputs violated Four Nevers by using forbidden terms as contrast/comparison language — confirms that prompts need explicit negative-example blocking, not just rule-listing.
**CoChalet insight:** signup-flow-cro and free-tool-strategy scored highest CoChalet deltas (+0.6). onboarding-cro triggered 'fractional ownership' violation — the model pulled from KB context negatively. CRO prompts need explicit instruction: never mention competitor terms even to contrast.
---
