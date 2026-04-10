# popup-cro-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output designs discount popups, email capture overlays, and FOMO urgency banners. All of these would actively damage the CoChalet brand. The brand is trust, exclusivity, and earned belonging — an exit-intent popup offering "10% off" would be brand suicide. CoChalet's one legitimate popup use case is a single, warm, non-interruptive exit-intent that asks one question and offers genuine value.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: popup-cro

**Model:** qwen-3.6-plus
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/popup-cro
**CoChalet Adaptation:** Exactly ONE popup is appropriate for CoChalet: a single exit-intent that asks one question ("Avant de partir, qu'est-ce qui t'a amené ici?") and offers the Mountain Cost Calculator as a value exchange for email. No discount. No urgency. No FOMO. No countdown timer. Nothing that makes CoChalet look like a timeshare promotion.

### Prompt for Hermes:

```
You are a conversion specialist for a luxury trust-first brand. Design ONE popup for CoChalet — the only popup appropriate for this product and brand positioning.

BRAND CONSTRAINT — POPUP ANTI-PATTERNS FOR COCHALET:
The following popup types are EXPLICITLY FORBIDDEN for CoChalet:
✗ Discount offer popups ("Save 10%") — no discounts exist, and it cheapens the brand
✗ FOMO/urgency popups ("Only 3 spots left!") — even if true, it reads like timeshare tactics
✗ Countdown timer popups — manipulative, contradicts Explorer archetype
✗ Welcome mat / full-screen popups — too aggressive for a 30-60 day consideration cycle
✗ Chat popup with face photo — too sales-y for the brand
✗ Social proof popups ("Sarah from Montreal just applied") — feels like fake scarcity
✗ Sticky bars saying "Limited spots!" — brand violation

WHY ONLY ONE POPUP:
- CoChalet has a 30-60 day consideration cycle — visitors who leave are NOT lost
- The nurture email sequence does the work after they leave
- An aggressive popup on a luxury product signals desperation
- One well-designed exit-intent captures the email + qualifies intent without pressure

THE ONE APPROVED POPUP — EXIT INTENT:

Trigger: user moves cursor toward browser close/back button
Timing: only fires if user has been on site > 45 seconds (they've seen something)
Frequency: once per session, never again for 30 days
Mobile: slides up from bottom (not full-screen), only on property/apply pages

DESIGN BRIEF:
- Background: dark alpine (not jarring white lightbox)
- No countdown timer. No urgency language.
- One question only — not a form with multiple fields
- Tone: warm curiosity, not desperation

POPUP COPY (FR primary — this is the conversion version):

Headline: "Avant de partir, une question rapide."
Sub-headline: [none — let the question breathe]
Question (dropdown or text): "Qu'est-ce qui t'a amené ici aujourd'hui?"
Options (if dropdown):
  - "Je loue des chalets et je me pose des questions sur la propriété"
  - "J'envisage d'acheter un chalet mais le coût me freine"
  - "J'ai vu un post de Justin et je voulais en savoir plus"
  - "Je cherche un espace de deep work hors de la ville"
  - "Autre chose"

After selection, reveal email field:
"Laisse-nous ton email — Justin t'envoie personnellement le Calculateur de Part."
[Email field] [Bouton: Envoyer]

CTA button: "Recevoir le Calculateur" — never "Submit" or "Sign up"

Post-submission message:
"Merci. Justin te contacte d'ici 48 heures."
(This sets an expectation Justin must fulfill — only use if he can actually do this)

EN VERSION (for English-first visitors):
Headline: "Before you go — one quick question."
Question: "What brought you here today?"
Post-email: "We'll send you the Mountain Cost Calculator. Justin reads every reply."
CTA: "Send me the Calculator"

DELIVERABLE — produce a single markdown document with:

1. THE EXIT-INTENT POPUP (full spec)
   - Trigger conditions (scroll depth, time on page, cursor behavior)
   - Design spec (dimensions, colors using CoChalet brand vars, typography)
   - Full copy (FR + EN)
   - Question options (dropdown vs. open text trade-offs)
   - Email capture integration (what platform, what list it goes to)
   - Post-submission state (what the user sees after submitting)
   - Follow-up automation (what email triggers immediately)

2. PLATFORM RECOMMENDATION
   Best popup tool for CoChalet's likely Webflow site:
   - Option A: Webflow native interaction (no cost, limited features)
   - Option B: Convertflow or Sleeknote (persona-aware, A/B testing)
   - Option C: Custom JS (requires developer, full control)
   Recommend one with rationale.

3. A/B TEST PLAN
   Test 1: Single question (open text) vs. dropdown options — which produces better email quality?
   Test 2: "Calculateur" offer vs. "Justin vous contacte" offer — which has higher opt-in rate?
   Minimum sample: 200 popup shows per variant
   Success metric: email capture rate AND email open rate (not just capture rate)

4. WHAT NOT TO BUILD (decision log)
   Document the 6 forbidden popup types listed above.
   For each: why it was rejected, what it would have cost the brand.
   This prevents future team members from re-proposing them.

COMPLIANCE:
- No "timeshare" or "fractional ownership" in popup copy
- No countdown timers or urgency language
- No financial figures in popup ($2,634 etc.) — this is an awareness capture, not a sales moment
- CTA must be value-forward ("Recevoir le Calculateur") not form-submission language ("Submit")
- 30-day cookie: never show the same person this popup more than once per month

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Justin's capacity to respond to popup submissions within 48 hours: may not be realistic at 7 hrs/week
- Webflow popup integration: native vs. third-party tool decision pending tech stack confirmation
- Mountain Cost Calculator: popup references it as the lead magnet — calculator must be built first
- Exit-intent trigger accuracy: mobile vs. desktop behavior differs significantly
- FR vs EN popup detection: how to identify visitor language preference for correct popup version
- A/B test timing: 200 shows per variant may take weeks to reach at pre-launch traffic levels
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- Webflow popup integration method not yet selected
- Mountain Cost Calculator (the popup offer) not yet built — popup depends on it
- Justin's 48-hour response SLA: may be too aggressive for 7 hrs/week constraint
- Exit-intent mobile behavior: cursor-based trigger doesn't work on mobile — mobile trigger strategy needed
- Traffic volume: pre-launch means 200-show A/B test could take months — launch with single variant first
- Language detection: FR vs EN popup requires visitor language preference signal that may not exist yet
