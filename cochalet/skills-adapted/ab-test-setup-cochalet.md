# ab-test-setup-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: ab-test-setup

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/ab-test-setup
**CoChalet Adaptation:** Experiments designed for the Autoresearch program (CoChalet's systematic content testing framework). Low traffic means longer test durations and different statistical approaches. Variables specific to DW/PC audiences, bilingual content, and emotional frameworks.

### Prompt for Hermes:

```
You are an experimentation strategist. Design the A/B testing framework for CoChalet's Autoresearch program -- the systematic testing of marketing messages, formats, and channels.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Current marketing state: Marketing health 41/100. Zero posts published. Starting from scratch.
- Traffic level: LOW. cochalet.co has minimal traffic. Social channels are new.
- Autoresearch program: CoChalet's framework for systematically testing what resonates with target audiences before scaling spend
- Target audiences:
  - Deep Workers (DW): remote professionals, Montreal-based, 30-45, $120K+
  - Proprietaires Curieux (PC): Quebec homeowners curious about co-ownership
- DW Pain framework (CUT): Context Switching, Unproductive, Time-Consuming
- PC Emotion framework: Soulagement (relief), Fierte (pride), Appartenance (belonging)
- Channels to test: LinkedIn (organic), Instagram (organic), Email, Landing page
- Budget constraints: bootstrapped, minimal paid spend initially

DELIVERABLE -- produce a single markdown document with:

1. EXPERIMENT FRAMEWORK
   - Naming convention for experiments (e.g., EXP-DW-LI-001 = Experiment, Deep Worker, LinkedIn, #001)
   - Hypothesis template: "If we [change], then [metric] will [direction] because [rationale]"
   - Minimum viable experiment duration for low-traffic contexts
   - Statistical significance approach for small sample sizes (Bayesian vs. frequentist recommendation)
   - When to call a test (minimum observations, confidence level)

2. VARIABLE MATRIX (what to test)
   For each variable, specify: hypothesis, control vs. variant, measurement method, minimum sample size

   a. HOOK TYPE
   - Pain-led ("Tired of renting with nothing to show?") vs. Dream-led ("Imagine waking up to the Laurentians every weekend")
   - Question hook vs. statement hook vs. story hook
   
   b. LANGUAGE
   - French-only vs. bilingual vs. English-only (by channel)
   - Tutoiement vs. neutral (already decided: tutoiement, but worth validating)
   
   c. FORMAT
   - Single image vs. carousel vs. video vs. text-only (by channel)
   - Short-form (<100 words) vs. long-form (>300 words)
   
   d. EMOTION
   - CUT pain (Context Switching vs. Unproductive vs. Time-Consuming -- which resonates most?)
   - PC emotion (Soulagement vs. Fierte vs. Appartenance -- which converts?)
   - Fear of missing out vs. aspiration vs. social proof
   
   e. CTA
   - "Book a call" vs. "Discover more" vs. "Join the circle" vs. "See the chalets"
   - Button color, placement, urgency language
   
   f. SOCIAL PROOF
   - Community size ("Join 50 Fondateurs") vs. founder story vs. property imagery vs. no social proof

3. EXPERIMENT PRIORITY ROADMAP
   - Experiment 1 (Week 1-2): [most impactful, lowest effort]
   - Experiment 2 (Week 2-3): ...
   - Experiment 3 (Week 3-4): ...
   - Experiment 4 (Month 2): ...
   - Experiment 5 (Month 2): ...
   - Each with: hypothesis, channel, variable, control, variant, success metric, target sample size

4. TOOLING RECOMMENDATIONS
   - A/B testing tools appropriate for low-budget, low-traffic context
   - Analytics setup requirements
   - Results documentation template

5. LEARNING LOOP
   - How results feed back into content strategy
   - How winning variants become default templates
   - How losing variants inform what to avoid
   - Monthly "Autoresearch Report" template

QUALITY CHECKS:
- All experiment examples use CoChalet-specific copy, not generic placeholders
- Statistical approach is appropriate for LOW traffic (not assuming 10K visitors/month)
- Experiments are sequenced by impact and feasibility
- No experiment involves testing pricing or financial details in public
- Four Nevers compliance in all example copy
```

### Expected Output:
`Hermes/deliverables/ab-test-setup-autoresearch-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance in all example copy, (2) statistical methodology is appropriate for low-traffic context, (3) experiment priority is sequenced correctly (highest impact first), (4) variable matrix covers all relevant dimensions, (5) naming convention is practical, (6) learning loop connects to content strategy.

---
