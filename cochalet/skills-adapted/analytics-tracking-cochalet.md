# analytics-tracking-cochalet

DBA verdict: ADAPT (2026-04-10). Generic analytics output maps SaaS funnels (signup, activation, retention) that don't apply to a high-consideration real estate product with a 30-60 day sales cycle and a single human closer. Needs CoChalet-specific funnel stages, Justin's discovery call as the conversion event, and pre-launch measurement strategy.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: analytics-tracking

**Model:** qwen-3.6-plus
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/analytics-tracking
**CoChalet Adaptation:** CoChalet has a 30-60 day consideration cycle, not a SaaS click-to-activate funnel. The primary conversion event is Justin's 15-minute discovery call booking. Analytics must track awareness -> interest -> call booked -> close, with special attention to the calculator tool as a mid-funnel engagement signal.

### Prompt for Hermes:

```
You are an analytics architect for a high-consideration real estate startup. Design CoChalet's analytics tracking infrastructure for a pre-launch product with a 30-60 day sales cycle.

PRODUCT CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury Laurentian chalets
- Stage: Pre-launch (first FOs being onboarded)
- Sales model: Justin Kausel is the ONLY closer. No sales team.
- Primary conversion event: 15-minute discovery call with Justin
- Secondary conversion: Calculator tool engagement (mid-funnel signal)
- Funnel timeline: Awareness -> Interest -> Calculator use -> Call booked -> Call completed -> Commitment -> Notary -> Active FO
- Average sales cycle: 30-60 days from first touch to deed signing

REAL FUNNEL STAGES (NOT SaaS activation — these are the actual stages):
1. AWARENESS: First touch (ad click, organic, referral, social)
2. INTEREST: Page engagement > 45 seconds, scrolled to pricing section, returned visitor
3. CONSIDERATION: Calculator used, content downloaded, email subscribed
4. INTENT: Call booking page visited
5. DISCOVERY CALL BOOKED: Calendly/booking confirmation (PRIMARY CONVERSION)
6. DISCOVERY CALL COMPLETED: Justin marks as attended (SECONDARY CONVERSION)
7. COMMITMENT: Verbal yes, due diligence period initiated
8. NOTARY PROCESS: Deed registration in progress (~30 days)
9. ACTIVE FO: First stay booked, app downloaded, onboarding complete

TECH STACK (real/planned):
- Website: cochalet.co (likely Webflow or similar)
- Analytics: GA4 (primary)
- CRM: to be determined (Justin currently uses manual tracking)
- Booking: Calendly (discovery calls)
- Email: to be determined (nurture sequences)
- App: CoChalet mobile app (post-purchase onboarding)
- Calculator tool: embedded on website

PERSONAS TO TRACK SEPARATELY:
- Deep Workers (DW): Source = LinkedIn, Google search (work-related queries), referral from network
- Propriétaires Curieux (PC): Source = Facebook/Instagram, real estate content, word of mouth
- Tracking should enable persona segmentation by source/behavior

DELIVERABLE -- produce a single markdown document with:

1. GA4 EVENT TAXONOMY
   Complete list of events to track, with:
   - Event name (snake_case, GA4 compliant)
   - Trigger condition (what user action fires it)
   - Parameters to capture (e.g., persona_type, source, calculator_result)
   - Funnel stage it maps to
   - Priority: P0 (launch-critical), P1 (first month), P2 (scale)

2. CONVERSION GOALS SETUP
   Primary conversions (macro): discovery_call_booked, active_fo_onboarded
   Secondary conversions (micro): calculator_completed, email_subscribed, content_downloaded, pricing_section_viewed
   For each: GA4 goal configuration, expected volume at launch, benchmark CTR from similar products

3. ATTRIBUTION MODEL RECOMMENDATION
   - Standard last-click vs. data-driven (when to switch)
   - First-touch tracking (critical for long 30-60 day cycles)
   - Cross-device considerations (DW persona switches desktop/mobile)
   - UTM parameter convention: define the standard utm_source/medium/campaign/content/term structure

4. DASHBOARD SPECIFICATION
   Two dashboards:
   a) Justin's weekly 5-minute dashboard (executive view: calls booked, pipeline stage, cost per call)
   b) Hermes agent weekly analytics report (full funnel: by persona, by channel, by content piece)
   For each widget: metric name, calculation, target threshold, alert trigger

5. CALCULATOR TOOL TRACKING
   The calculator is the highest-intent mid-funnel signal.
   Track: calculator_started, calculator_completed, result_shared, call_booked_post_calculator
   Segment by: monthly_result_range ($1K-$2K, $2K-$3K, $3K+), persona type
   Expected insight: what calculator result correlates most with call booking?

6. IMPLEMENTATION PLAN
   Phase 1 (Launch day): GA4 base, call booking, calculator events (P0 only)
   Phase 2 (Week 2-4): Full event taxonomy, UTM standards, persona segmentation
   Phase 3 (Month 2): Dashboard automation, Hermes weekly report integration

COMPLIANCE:
- NEVER expose FO Stake ($112,300) or internal financial metrics in any analytics dashboard
- NEVER use "timeshare" or "fractional ownership" in any tracking labels or event names
- Cost-per-acquisition tracking: use "cost_per_call_booked" not "cost_per_lead" (more accurate)

## TUNING GAPS
End your output with a ## TUNING GAPS section identifying:
- Which analytics tools are confirmed vs. still TBD in the tech stack
- What historical benchmarks are unavailable (pre-launch = no baseline data)
- Which funnel stages lack clear tracking mechanisms today
- CRM integration gaps (Justin's manual process vs. automated pipeline)
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- CRM platform not yet selected — pipeline tracking is manual today
- No baseline conversion rates (pre-launch) — all benchmarks are from comparable products
- Calculator tool tracking requires dev implementation — not yet instrumented
- App analytics separate from web analytics — no unified tracking plan yet
- Justin's current call booking tool (Calendly vs. other) not confirmed
- Persona segmentation by source is hypothetical — needs 30-day data to validate
- Cost-per-call-booked unknown until paid campaigns launch
