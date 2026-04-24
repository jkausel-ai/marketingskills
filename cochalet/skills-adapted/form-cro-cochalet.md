# form-cro-cochalet

DBA verdict: ADAPT (2026-04-10). Generic form CRO output optimizes multi-field lead gen forms for SaaS signups. CoChalet has one critical form: the qualification/application form to join the Fondateurs Alpins waitlist. This is NOT a generic lead form — it must communicate exclusivity, qualify intent, and make the applicant feel they are being evaluated (not just captured). Martin's "Applique pour te qualifier" directive governs all form design.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: form-cro

**Model:** qwen-3.6-plus
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/form-cro
**CoChalet Adaptation:** The application form is the only form that matters. It must feel selective, not desperate. "Applique pour te qualifier" is the CTA — the form design must match the energy of that phrase. Qualification questions filter for genuine intent. The thank-you state must feel like an exclusive confirmation, not a generic success message.

### Prompt for Hermes:

```
You are a conversion rate specialist for high-consideration luxury products. Optimize CoChalet's Fondateurs Alpins application form — the single most important form in the acquisition funnel.

FORM CONTEXT:
- CoChalet: deeded co-ownership of luxury Laurentian chalets
- This form is NOT a typical lead gen form — it is an APPLICATION for consideration
- Framing: "We review every application. Not everyone is accepted." (Martin's NASA astronaut analogy)
- CTA confirmed: "Applique pour te qualifier" (FR) / "Apply to qualify" (EN)
- Placement: website (/apply or /founding-8 page), post-email-nurture, post-app-demo
- Target persona: both DW and PC, but form language should feel universal
- Calendly integration: after form submission, discovery call booking is offered (not required)
- Form platform: likely Typeform or native Webflow form (TBD)

THE EXCLUSIVITY PRINCIPLE:
- The form signals that CoChalet is selective
- Each question should feel like it's qualifying the applicant, not capturing a lead
- Questions should require genuine thought — not just name/email
- The experience should feel like applying to join something real
- Confirmed by Martin: "Change 'Join' to 'Apply.' It changes everything." (April 7 TRACTION session)
- Confirmed by Lynn: "Referral privilege system — invite qualified friends" (April 9 TRACTION session)

CURRENT FORM STATE (from app source code):
- WaitlistSignup component exists in mobile app
- Shows waitlist position (#142) and referral code (ALP-MTL-142)
- "Submit waitlist request" CTA (to be replaced with "Apply to qualify")
- ConsultationBooking component for "Request call" — this is the post-form CTA

DELIVERABLE — produce a single markdown document with:

1. APPLICATION FORM DESIGN (the primary form)
   Recommended fields (max 6 — every field beyond 6 kills conversion):
   - Required: First name, Email (standard capture)
   - Qualifying questions (2-3 of these — choose best for intent signal):
     a) "Qu'est-ce qui t'a amené ici aujourd'hui?" (open text, 2-3 sentences max)
     b) "Comment décris-tu ta relation avec les Laurentides?" (multi-choice or open)
     c) "Quel rôle joue la montagne dans ta semaine idéale?" (open text)
     d) "As-tu déjà eu une propriété ou envisagé d'en acheter une?" (yes/no + optional detail)
   - For each recommended field: label copy (FR + EN), placeholder text, validation rules, why it's included
   - For each rejected field: explain why it was cut

2. FORM PAGE COPY (the page surrounding the form)
   - Headline above form (10 words max, exclusivity framing)
   - Sub-headline (25 words, what happens after they apply)
   - Trust signals (3 items beside form: e.g., "application reviewed within 48 hours," "Pioneer 01 is Justin himself," "800 Fondateurs cap")
   - Privacy micro-copy (1 sentence, warm not legal)

3. MULTI-STEP FORM VARIANT
   For higher intent pages, a 3-step form converts better:
   - Step 1: "Tell us about you" (name + email)
   - Step 2: "Tell us about your mountain relationship" (1 qualifying question)
   - Step 3: "Tell us about your timeline" (1 intent question)
   Design the progress indicator copy and transition copy between steps.

4. CONFIRMATION STATE (thank-you page/message)
   - Headline: Must feel like an exclusive confirmation, not a generic "Thanks!"
   - Body: 3 sentences max. What happens next. When to expect a response. What makes this different.
   - CTA: "Book a 15-minute conversation with Justin" (Calendly link — optional, not required)
   - FR primary, EN secondary
   - Tone: warm, specific, personal (Justin's voice)

5. REFERRAL MECHANISM COPY
   Post-confirmation: "You're in the queue. Know someone who belongs here?"
   - Referral share message (FR + EN, 140 chars for social sharing)
   - Referral incentive framing (not monetary — priority queue position or Alpine Circle access)

6. FORM A/B TEST PLAN
   Test 1: "Applique pour te qualifier" vs. "Rejoins les Fondateurs Alpins" (CTA copy)
   Test 2: 3-field form vs. 5-field form (completion rate vs. lead quality trade-off)
   Test 3: Open qualifying question vs. multiple choice (quality signal vs. friction)
   For each test: hypothesis, success metric, minimum sample size, expected outcome

COMPLIANCE:
- Never use "timeshare" or "fractional ownership" in form copy
- Never ask about income, investment budget, or financial qualification (legal risk, brand risk)
- Never imply guaranteed acceptance — "we review every application" is the framing
- CTA must be "Applique pour te qualifier" or "Apply to qualify" — never "Submit," "Sign up," "Join now"

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Form platform not yet confirmed (Typeform vs. Webflow native vs. other)
- Calendly integration: conditional or always shown post-submission?
- Referral incentive: priority position vs. Alpine Circle status vs. other (Justin to decide)
- Application review SLA: 48-hour promise requires Justin bandwidth to fulfill
- DW vs. PC form variants: single form recommended at launch, bifurcation when volume allows
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- Form platform not confirmed — Typeform, Webflow native, and Tally all viable
- No baseline conversion rate — "30% form completion is good" benchmark is from SaaS, not luxury real estate
- Qualifying question performance: which questions signal highest intent unknown (no data)
- Application review process: Justin's bandwidth for reviewing applications not formally scoped
- Referral mechanism: app already shows waitlist position + referral code but mechanism not yet promoted
- "Apply to qualify" vs. "Join" CTA: Martin's recommendation, not yet A/B tested
- Thank-you state: Calendly offer acceptance rate after form completion — unknown
