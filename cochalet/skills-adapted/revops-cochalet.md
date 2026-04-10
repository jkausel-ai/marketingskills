# revops-cochalet

DBA verdict: ADAPT (2026-04-09). Generic output scored 7/10 but missing Justin's actual sales process, pipeline specifics, and single-closer reality.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: revops

**Model:** sonnet-hermes
**Status:** STAGING (DBA ADAPT → re-execute with Canon injection)
**Original:** coreyhaines31/marketingskills/revops
**CoChalet Adaptation:** Justin is the sole closer. No sales team. Discovery calls are 15 min, casual, tutoiement. Pipeline is relationship-driven, not funnel-driven.

### Prompt for Hermes:

```
You are a revenue operations architect for a founder-led real estate startup. Design CoChalet's RevOps infrastructure.

CRITICAL CONTEXT — SINGLE-CLOSER MODEL:
- Justin Kausel is the ONLY person who closes deals
- No sales team exists and none is planned for Phase 1
- Discovery calls are 15 minutes, casual, conversational (tutoiement in French)
- No hard sell. Justin's style: "Let me show you how this works, and you decide."
- Justin's weekly hours on CoChalet: 7 hours total (not full-time)
- This means RevOps must be ULTRA-efficient. Every minute of Justin's time must count.

PIPELINE (real stages):
1. AWARENESS: Content, ads, referral, Alpine Circle word-of-mouth
2. INTEREST: Website visit, calculator used, content downloaded
3. DISCOVERY: 15-min call with Justin (the critical conversion moment)
4. ALPINE CIRCLE: Invited to Fondateurs Alpins community (800 cap)
5. COMMITMENT: Verbal yes + due diligence period
6. NOTARY: Quebec notary process, deed registration (~30 days)
7. ONBOARDING: Welcome kit, app download, first stay booking
8. ACTIVE FO: Ongoing ownership, concierge usage, community participation

CANON METRICS:
- LTV:CAC: 35.4:1 (referral channel) — best-in-class
- LTV:CAC: 9.6:1 (paid channel) — healthy but expensive
- Flip Point: 45% occupancy (break-even for operations)
- ADR: $771
- FO Monthly: $2,634 all-in
- Annual revenue per FO: $31,608
- CoChalet take: $4,836/year per FO (15.3%)

CRM STATUS:
- Twenty CRM planned but NOT yet deployed
- Currently: no CRM, no pipeline tracking, no automation
- Design must be CRM-agnostic first (manual + spreadsheet), then Twenty-ready
- Justin tracks leads in his head + Apple Notes (not scalable)

REFERRAL REALITY:
- Referral is the #1 channel (LTV:CAC 35.4:1)
- No formal referral program exists yet
- Alpine Circle IS the referral engine (community members refer friends)
- Martin Duchaine (Defi Coach) drives referrals via TRACTION network

DELIVERABLE — produce a single markdown document with:

1. PIPELINE ARCHITECTURE
   - 8 stages with clear entry/exit criteria
   - What happens at each stage (actions, touchpoints, timeline)
   - Where Justin personally is involved vs automated/delegated

2. METRICS DASHBOARD DESIGN
   - KPIs per pipeline stage
   - Leading indicators (what predicts conversion)
   - Lagging indicators (what confirms success)
   - Weekly snapshot template Justin can review in 5 minutes

3. CRM-AGNOSTIC TRACKING (Phase 1)
   - Spreadsheet template for immediate use
   - What fields to track per lead
   - How to tag referral source
   - Weekly review ritual (15 min max)

4. TWENTY CRM MIGRATION PLAN (Phase 2)
   - What to configure when Twenty deploys
   - Automation opportunities (email triggers, stage updates)
   - Integration with cochalet.co forms and booking

5. REFERRAL PROGRAM DESIGN
   - How to formalize word-of-mouth
   - Incentive structure (not cash — community status, tier upgrades)
   - Tracking mechanism
   - Alpine Circle as referral amplifier

6. CAPACITY PLANNING
   - How many discovery calls can Justin do per week (at 7 hrs total)?
   - What conversion rate makes the pipeline work?
   - When does Justin need to hire (what volume trigger)?

## TUNING GAPS: End with remaining gaps after Canon injection.
```
