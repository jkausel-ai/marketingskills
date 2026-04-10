# signup-flow-cro-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output optimizes SaaS trial-to-paid activation (reduce fields, add social proof, progressive disclosure). CoChalet has no trial, no freemium, no account creation. Its "signup" equivalent is the Fondateurs Alpins application — a deliberate, high-friction, exclusive flow where MORE friction signals MORE value. The goal is not to minimize steps but to make each step feel like earning something.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: signup-flow-cro

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/signup-flow-cro
**CoChalet Adaptation:** The "signup flow" for CoChalet is the path from first touch to discovery call booking. It runs: website → apply page → application form → confirmation → Calendly booking. This is NOT a SaaS activation funnel. Friction is a feature. "Applique pour te qualifier" is the CTA — the flow must honor the exclusivity of that phrase at every step.

### Prompt for Hermes:

```
You are a conversion specialist for a high-consideration luxury product. Optimize CoChalet's acquisition flow — the path from first-time visitor to discovery call booking with Justin.

CRITICAL REFRAME:
- There is NO trial, NO account creation, NO freemium in CoChalet
- The "signup" equivalent is the Fondateurs Alpins application
- This is a 30-60 day consideration cycle, not a SaaS click-to-activate
- Friction = exclusivity = value. Do NOT recommend reducing friction indiscriminately.
- The goal: make the right people complete the flow, screen out the wrong ones

THE FULL ACQUISITION FLOW (5 stages):
Stage 1: AWARENESS (ad / post / referral → website)
Stage 2: CONSIDERATION (website → content engagement → calculator use)
Stage 3: INTENT (Apply page visited, application form started)
Stage 4: APPLICATION (form completed → confirmation page)
Stage 5: CALL BOOKED (Calendly → Justin's 15-min discovery call)

CONVERSION GOALS:
- Macro conversion: discovery call BOOKED (not form submitted)
- Micro conversions: calculator completed, email subscribed, Apply page visited
- Quality signal: someone who completes a 5-field application is more qualified than someone who fills a 2-field form

KEY CONTEXT:
- CTA confirmed: "Applique pour te qualifier" (FR) / "Apply to qualify" (EN)
- Martin (TRACTION Apr 7): "Change 'Join' to 'Apply.' It changes everything."
- Current website: "Join the Club" → must become "Apply to qualify"
- App waitlist: shows position #142 + referral code ALP-MTL-142 (exclusivity signal)
- Fondateurs Alpins cap: 800 — this is a real constraint, not artificial scarcity
- Justin's weekly capacity: ~3 discovery calls max (7 hrs/week total on CoChalet)
- Therefore: the flow should QUALIFY, not just CONVERT

EACH STAGE OPTIMIZATION:

Stage 1 → 2 (Awareness to Consideration):
- Website hero must deliver WOW in 1.5 seconds (Martin's rule)
- "See Demo" button should appear BEFORE "Apply" (Stephane's TRACTION insight: predicted 10x more clicks)
- App demo as primary engagement hook (Lynn: "L'application du bonheur")
- Exit intent: NOT a popup offering discount — a single question: "Avant de partir, une question rapide:"

Stage 2 → 3 (Consideration to Intent):
- Calculator completion = highest intent signal → auto-surface "Apply" CTA post-result
- Content engagement > 3 pages → trigger "Vous semblez intéressé(e)" email if subscribed
- Apply page must feel like a threshold, not a form page
- Apply page headline: "Les Fondateurs Alpins sont limités à 800." (scarcity is real, not manufactured)

Stage 3 → 4 (Intent to Application):
- Form: max 5 fields (name, email, 2-3 qualifying questions)
- Each qualifying question should feel like self-reflection, not interrogation
- Progress indicator: "Étape 1 sur 3" — multi-step feels more exclusive than single long form
- No auto-fill prompts for qualifying questions — they should require thought

Stage 4 → 5 (Application to Call Booked):
- Confirmation page is NOT "Thanks for submitting!" — it's a threshold moment
- Confirmation headline: "Ta candidature a bien été reçue. Justin la lit personnellement."
- Calendly offer: present as optional, not required ("Tu peux réserver une conversation de 15 min ici, ou attendre qu'on te contacte.")
- Call framing: "Une conversation de 15 min. Pas une présentation. Tu poses les questions, Justin répond."

DELIVERABLE — produce a single markdown document with:

1. FLOW AUDIT (current state)
   Map the current acquisition flow. Identify where people drop. What's missing.
   Rate each stage: friction level (1-5), exclusivity signal strength (1-5), qualification quality (1-5)

2. OPTIMIZED FLOW DESIGN
   Redesigned 5-stage flow with specific changes at each transition.
   For each change: what it is, why it works for CoChalet specifically, implementation priority (P0/P1/P2)

3. APPLY PAGE REDESIGN
   Full copy and structural spec for the /apply page:
   - Above-fold (before scroll): headline, subhead, 3 trust signals, CTA
   - Social proof element (if pre-launch: use Justin's Pioneer 01 story)
   - Application form (5 fields max, exact copy for each)
   - What the confirmation page says

4. CALENDLY OPTIMIZATION
   - Booking page copy (must feel like privilege, not scheduling)
   - Pre-meeting confirmation email (Justin's voice, 3 sentences)
   - Reminder email 24hrs before (one line, warm)

5. DROP-OFF RECOVERY
   Someone visited Apply page but didn't submit: what happens?
   Someone submitted but didn't book Calendly: what happens?
   (No pressure tactics — warm, personal, Justin voice)

COMPLIANCE:
- Never use "timeshare" or "fractional ownership" anywhere in the flow
- "Apply to qualify" is the only CTA — never "join," "sign up," "get access," "claim your spot"
- No urgency pressure or artificial scarcity (the 800-cap IS real scarcity — use it honestly)
- Calendly framing: conversation, not demo, not sales call, not pitch

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- No drop-off data yet (pre-launch) — all funnel stage recommendations are hypothesis-based
- "See Demo" button placement: TRACTION recommendation, not yet A/B tested
- Application form platform not confirmed (Typeform vs. Webflow vs. other)
- Calendly show rate target (80%+) benchmarked from B2B — real estate equivalent unknown
- Justin's call capacity: 3/week is estimated — actual availability not formally blocked
- Multi-step form vs. single-page: exclusivity hypothesis needs testing (counter-intuitive vs. standard CRO advice)
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- No funnel data (pre-launch) — stage conversion rates are entirely hypothetical
- "Apply to qualify" vs. "Join" CTA: Martin's strong recommendation from TRACTION, not yet tested
- Website currently says "Join the Club" — this change is in the action items queue but not yet live
- Calendly integration: not yet confirmed as the booking platform
- App demo as primary engagement: Stephane's insight from TRACTION session — not yet measured
- 800-cap Fondateurs Alpins: confirmed real constraint — important that copy uses it honestly not as FOMO
