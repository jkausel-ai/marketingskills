# pricing-strategy-cochalet

DBA verdict: ADAPT (2026-04-09). Generic output scored 8/10 but missing V31_14 debate, real tier economics, and Casadora pricing.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)
5. NEVER name forbidden terms even to contrast them. Do not write 'unlike timeshare' or 'not fractional ownership'. Instead use: 'unlike usage-rights products', 'unlike shared vacation clubs', 'unlike partial-access arrangements'.

---

## Skill: pricing-strategy

**Model:** sonnet-hermes
**Status:** STAGING (DBA ADAPT → re-execute with Canon injection)
**Original:** coreyhaines31/marketingskills/pricing-strategy
**CoChalet Adaptation:** Deep Canon V31 injection. V31_14 cost-of-service model debate. Real concierge tier economics. Casadora competitive pricing. AMF regulatory moat.

### Prompt for Hermes:

```
You are a pricing strategist for a luxury real estate co-ownership model. Analyze and optimize CoChalet's pricing architecture with FULL Canon data.

CANON V31 LOCKED NUMBERS (do not change these):
- FO Stake: $112,300 (10% equity in property) — GATED, not for public ads
- FO Monthly: $2,634 all-in ($759 P&I + $1,875 service) — PUBLIC number
- CoChalet Annual Take: $28,200 per FO (15.3% of revenue) — GATED
- NOI Margin: 37.9% — GATED
- DSCR: 1.95x (stress test 2.22x) — GATED
- ADR: $771 — GATED
- Flip Point: 45% occupancy — GATED
- AOI: 44.4 (22x valuation multiple) — GATED
- LTV:CAC: 35.4:1 (referral), 9.6:1 (paid) — GATED

V31_14 COST-OF-SERVICE DEBATE (critical context):
- Original model: 70% margin design (CoChalet keeps 70% of service revenue)
- V31_14 revision: 31% margin (cost-of-service model where CoChalet charges actual cost + 31% markup)
- This is an ACTIVE debate. Justin has not finalized which model to use.
- Implications: 70% margin = higher take but harder to justify; 31% = defensible but lower revenue
- Your analysis should model BOTH scenarios and recommend

CONCIERGE TIER ECONOMICS (real numbers):
- Essentiel: $0/stay (base, self-service, included in $2,634 monthly)
- Confort: $360/stay (enhanced amenities, semi-managed)
- XL: $720/stay (premium service, fully managed)
- Noir: $1,450/stay (ultra-premium, white-glove, personalized)
- No uptake data yet (pre-launch) — model expected distribution
- Average stays per FO per year: estimate 6-12

COMPETITIVE PRICING (from comp intel):
- Casadora: $85,000-$150,000 entry, $1,800-$3,200 monthly (45.5% keyword contest)
- Pacaso (US): $200,000-$600,000 USD entry, $2,500-$5,000 USD monthly
- Solo Laurentians cottage: ~$500,000-$1,200,000 purchase, $8,000-$10,000/mo total cost
- Airbnb Laurentians luxury: $800-$1,200/night ($6,400-$9,600/mo at 8 nights)

REGULATORY CONTEXT:
- AMF confirmed CoChalet is NOT a security (regulatory moat)
- Quebec notary process: deed registered at land registry (real property, not usage rights)
- No securities prospectus needed = lower compliance cost than competitors

DELIVERABLE — produce a single markdown document with:

1. PRICING ARCHITECTURE ANALYSIS
   - Breakdown of $2,634 monthly (what each component funds)
   - V31_14 scenario comparison: 70% margin vs 31% cost-of-service
   - Recommendation with reasoning

2. COMPETITIVE PRICE POSITIONING
   - CoChalet vs Casadora (price + value comparison)
   - CoChalet vs solo ownership ("$101K Buyer Tax" framework)
   - Pricing perception map (premium accessible quadrant)

3. CONCIERGE TIER OPTIMIZATION
   - Expected tier distribution modeling (what % at each tier)
   - Revenue uplift calculation from tier adoption
   - Pricing psychology: how to drive Confort as default choice
   - Seasonal adjustment recommendations

4. PRICE ANCHORING STRATEGY
   - Primary anchor: solo ownership monthly cost ($8,000-$10,000)
   - Secondary anchor: luxury rental equivalent ($6,400-$9,600)
   - Messaging framework (never lead with price, always anchor first)

5. IMPLEMENTATION ROADMAP
   - Phase 1: Lock V31_14 decision
   - Phase 2: Tier pricing validation
   - Phase 3: Public messaging rollout

## TUNING GAPS (from first execution to track improvement):
End with a ## TUNING GAPS section. Compare against this list from the generic run — which are now RESOLVED vs still open?
- V31_14 cost-of-service debate ← NOW INJECTED
- Casadora exact pricing ← NOW INJECTED
- Concierge tier real economics ← NOW INJECTED
- AMF regulatory ruling ← NOW INJECTED
- Seasonal usage patterns ← still unknown (pre-launch)
```
