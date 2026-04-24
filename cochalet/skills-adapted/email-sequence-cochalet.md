# email-sequence-cochalet

DBA verdict: ADAPT (2026-04-10). Generic email sequences follow SaaS activation drips (Day 0: welcome, Day 1: feature tour, Day 3: social proof). CoChalet has a 30-60 day consideration cycle with a single human closer. Email must build trust across that window, never pitch directly, and culminate in Justin's 15-minute discovery call as the natural next step — not a hard close.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: email-sequence

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/email-sequence
**CoChalet Adaptation:** 7-email nurture sequence built for a 30-60 day consideration cycle. Justin is the sender voice. Each email earns trust without pitching. Final email makes booking a 15-minute call feel like the obvious next step, not a sales pressure. Bilingual FR primary.

### Prompt for Hermes:

```
You are an email strategist for a high-consideration luxury real estate product. Write a 7-email nurture sequence for CoChalet that builds trust over 30 days and culminates in a discovery call booking.

SALES CYCLE CONTEXT:
- Average consideration window: 30-60 days from first touch to discovery call
- Justin Kausel is the ONLY closer — 15-minute discovery calls, casual, tutoiement
- Email list source: lead magnet downloads, website signup, LinkedIn DM handoffs
- Email platform: TBD (Brevo or ActiveCampaign most likely)
- List size at launch: near zero — sequence is designed for when list builds
- Sequence goal: build trust → make Justin's call feel like a privilege, not a sales pitch

CRITICAL: THE ANTI-PITCH PRINCIPLE
- Never pitch the product in emails 1-5
- The product sells itself once trust is established and the call is booked
- Every email delivers standalone value — useful even if person never books a call
- The discovery call is framed as a conversation, never as a sales meeting
- Justin's energy: "Let me show you how this works, and you decide" — never pressure

EMAIL SEQUENCE ARCHITECTURE (7 emails over 30 days):

Email 1 (Day 0 — Welcome): Establish Justin's voice. The personal origin story. Why he built this.
Email 2 (Day 3 — The Problem): The CUT construct. What Airbnb trips really cost. No solution yet — just naming the pain.
Email 3 (Day 7 — The Dream): A sensory Thursday Evening scenario. No product, pure lifestyle. "What if this was yours."
Email 4 (Day 12 — The Insight): One surprising fact about deeded co-ownership that most people don't know. Educational, not salesy.
Email 5 (Day 18 — Social Proof): A Fondateurs Alpins member story (or Justin-as-Pioneer-01). Real, specific, not testimonial-template.
Email 6 (Day 24 — The App): "I want to show you something." The app demo offer. Soft invitation.
Email 7 (Day 30 — The Invitation): Justin personally inviting them to a 15-minute conversation. Framed as exclusive access, not sales call.

SENDER VOICE — JUSTIN KAUSEL:
- Register: warm, direct, authentic builder. Never corporate. Never polished-marketer.
- Speaks as: peer to peer, tutoiement in FR
- FR: "tu" not "vous." Quebec French, not France French.
- Sentence length: short declarative openings. Longer narrative in the body.
- Never: superlatives, hype, urgency pressure, FOMO language
- Always: specific details (66 months, Pioneer 01, the actual address), personal admission of struggle

SUBJECT LINE RULES:
- Max 45 characters for mobile preview
- Never open with the product name
- No "RE:" or fake reply tricks
- FR primary, EN secondary
- Strong performers for this product type: temporal ("Thursday, 8 months from now..."), personal ("I almost quit. Here's why I didn't."), question ("What does owning a mountain feel like?")

FOR EACH EMAIL — PRODUCE:
- Subject line (FR + EN)
- Preview text (FR + EN, 90 chars max)
- Email body (FR, 150-300 words — short is better)
- EN adaptation (for bilingual list segmentation)
- Personalization token: [FIRST_NAME] placement
- CTA (only Email 6 and 7 have explicit CTAs — others end with an open question or observation)
- Send timing: day number from sequence trigger

EMAIL 7 — THE DISCOVERY CALL INVITATION (special rules):
- Justin writes this one personally (template but personal voice)
- Frame: "I have 3 spots in my calendar this week for 15-minute conversations..."
- Never: "Book a sales call," "Schedule a demo," "Talk to our team"
- Always: "This is a conversation, not a pitch. You ask, I answer."
- CTA: "Applique pour te qualifier" — makes it feel selective, not desperate
- Calendly link embedded

COMPLIANCE:
- Never use "timeshare" or "fractional ownership" — use "deeded co-ownership" or "copropriété indivise"
- Never mention $2,634 in emails 1-6 (email 7 can reference "what it actually costs" as teaser only)
- Never reference DSCR, NOI, IRR, or internal financial metrics
- Never imply investment returns — "builds equity over time" is the maximum financial claim
- "Own it. Use it. Love it." can appear in email 7 only — not as opener

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Which email platform is confirmed (Brevo vs. ActiveCampaign vs. other)
- Optimal send frequency (7 emails/30 days is hypothesis — may be too frequent)
- Segment logic: DW vs. PC sequences (this is one sequence — needs bifurcation data)
- Justin's actual writing sample to calibrate voice accuracy
- Open rate / click rate benchmarks for Quebec luxury real estate (no local data)
- Discovery call show rate (no data — 15-min casual format is untested at scale)
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- Email platform not yet confirmed — sequence written platform-agnostic
- DW vs. PC segmentation: single sequence works for launch but needs bifurcation when list grows
- Justin has not reviewed/approved the voice — all copy is approximated from public statements and transcripts
- Optimal cadence unknown: 7 emails/30 days may be too aggressive for Quebec market (more reserved)
- Email 5 (social proof): no real Fondateurs Alpins stories yet — will need a real member or Justin-as-pioneer only
- Discovery call show rate target (80%+) is benchmarked from B2B SaaS — real estate equivalent unknown
- FR authenticity: tutoiement register written by non-native — Quebec review required before send
