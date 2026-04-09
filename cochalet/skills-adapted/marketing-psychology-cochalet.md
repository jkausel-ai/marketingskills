# marketing-psychology-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: marketing-psychology

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/marketing-psychology
**CoChalet Adaptation:** Applies behavioral science to CoChalet's specific emotional frameworks: CUT pain construct for DW, Soulagement/Fierte/Appartenance for PC. Maps psychological triggers to specific channels and touchpoints. Stays warm and ethical (no dark patterns).

### Prompt for Hermes:

```
You are a behavioral science strategist applying psychological principles to ethical marketing. Design the psychological framework for CoChalet's messaging.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Brand archetype: Explorateur (adventure, discovery) + Soignant (care, trust, belonging)
- Tone: warm, factual, zero superlatives. NEVER manipulative or fear-based.
- Martin's directive: "Montrer le reve. Pas expliquer la formule." (Show the dream, not the formula.)

TARGET AUDIENCES AND THEIR PSYCHOLOGICAL PROFILES:

Deep Workers (DW):
- Pain framework: CUT
  - Context Switching: constantly switching between "work mode" and "trying to relax" -- never fully in either
  - Unproductive: weekends consumed by cottage logistics (searching, booking, packing, driving, unpacking) instead of rest or deep work
  - Time-Consuming: annual cottage rental search, no continuity, no "home base" in the mountains
- Decision-making style: analytical, skeptical of hype, needs data and social proof, researches extensively before committing
- Identity: sees themselves as builders, creators, thoughtful -- not impulse buyers

Proprietaires Curieux (PC):
- Emotion framework:
  - Soulagement (relief): "I can stop worrying about cottage costs and maintenance"
  - Fierte (pride): "I own a piece of the Laurentians -- I am a Fondateur"
  - Appartenance (belonging): "I am part of something exclusive and meaningful"
- Decision-making style: more emotional, community-driven, influenced by peers, values exclusivity

DELIVERABLE -- produce a single markdown document with:

1. PSYCHOLOGICAL PRINCIPLES MAPPED TO COCHALET
   For each principle, provide: definition, how it applies to CoChalet specifically, example copy (FR and EN), channel where it works best, ethical guardrails

   a. LOSS AVERSION
   - Application: "$120K lost on Airbnb with zero ownership" -- Justin's origin story IS loss aversion
   - Example: "Chaque dollar en location est un dollar sans propriete." / "Every rental dollar builds someone else's equity."
   - Channel: LinkedIn long-form, email sequence
   - Guardrail: present as factual comparison, not fear-mongering

   b. SOCIAL PROOF
   - Application: Fondateurs Alpins community, 800-cap exclusivity
   - Example: "Rejoins 47 fondateurs qui ont choisi de vivre autrement." / "Join 47 founders who chose a different path."
   - Channel: Instagram, landing page
   - Guardrail: only cite real numbers, never inflate

   c. SCARCITY
   - Application: 800 Fondateur cap, limited properties, seasonal availability
   - Guardrail: scarcity must be REAL, never artificial

   d. IDENTITY/BELONGING
   - Application: "You are a Fondateur Alpin" -- identity transformation
   - Channel: community, email, onboarding

   e. ANCHORING
   - Application: anchor against full cottage purchase price ($500K+), not against rental cost
   - Guardrail: never anchor against "timeshare" or "fractional" competitors

   f. ENDOWMENT EFFECT
   - Application: discovery call creates mental ownership before financial commitment
   - Channel: discovery call structure, follow-up emails

   g. RECIPROCITY
   - Application: free value (ROI calculator, guide, community access) before asking for commitment
   - Channel: lead magnets, content marketing

   h. COMMITMENT AND CONSISTENCY
   - Application: small yeses leading to big yes (newsletter -> community -> discovery call -> co-ownership)
   - Channel: email nurture sequence

2. CUT PAIN MESSAGING GUIDE
   For each CUT dimension:
   - Primary emotion it triggers
   - Best channel to address it
   - Example headline (FR and EN)
   - Example body copy direction
   - CTA that resolves this specific pain

3. SOULAGEMENT/FIERTE/APPARTENANCE GUIDE
   For each PC emotion:
   - When in the journey this emotion peaks
   - How to activate it authentically
   - Example messaging (FR and EN)
   - Visual direction that reinforces this emotion

4. CHANNEL-SPECIFIC PSYCHOLOGY
   - LinkedIn: what psychological triggers work best here (authority, social proof, loss aversion)
   - Instagram: what works here (aspiration, belonging, visual endowment)
   - Email: what works here (reciprocity, commitment/consistency, scarcity)
   - Landing page: what works here (anchoring, social proof, loss aversion, endowment)
   - Discovery call: what works here (endowment, identity, reciprocity)

5. ETHICAL GUARDRAILS
   - Dark patterns to NEVER use (false urgency, hidden costs, bait-and-switch)
   - How CoChalet's warm + factual tone naturally prevents manipulation
   - The line between "showing the dream" and "creating false expectations"
   - Martin's directive as ethical compass

QUALITY CHECKS:
- All psychological principles are applied ethically (no dark patterns)
- Example copy is warm and factual, not manipulative
- CUT and Soulagement/Fierte/Appartenance frameworks are correctly applied
- Four Nevers compliance in all example copy
- Principles are mapped to specific channels, not generic
- No superlatives or hype in any example messaging
```

### Expected Output:
`Hermes/deliverables/marketing-psychology-behavioral-framework-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) all psychological principles are applied ethically, (3) CUT and PC emotion frameworks are correctly mapped, (4) example copy matches brand voice (warm, factual, no superlatives), (5) channel-specific recommendations are practical, (6) ethical guardrails are genuine, not performative.

---
