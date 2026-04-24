# churn-prevention-cochalet

DBA verdict: ADAPT (2026-04-09). Generic output scored 8/10 but missing iOS app analytics schema, concierge tier upgrade economics, and Alpine Circle programming specifics.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: churn-prevention

**Model:** sonnet-hermes
**Status:** STAGING (DBA ADAPT → re-execute with Canon injection)
**Original:** coreyhaines31/marketingskills/churn-prevention
**CoChalet Adaptation:** Year 1 renewal is the critical gate. iOS app is the primary engagement signal. Concierge tier progression is the retention lever. Alpine Circle community is the moat.

### Prompt for Hermes:

```
You are a retention strategist for a luxury co-ownership brand. Design CoChalet's churn prevention system for the YEAR 1 RENEWAL gate.

WHY YEAR 1 IS CRITICAL:
- FOs commit to an initial period (likely 1-3 years with annual renewal option)
- Year 1 is when the relationship is tested — did they use it? Did they feel community? Did they see value?
- No historical churn data exists (pre-launch). We are DESIGNING retention from scratch.
- Goal: 85%+ Year 1 renewal rate

IOS APP AS EARLY WARNING SYSTEM:
- App tracks: bookings made, bookings completed, concierge tier selected, app opens, push notification engagement
- Analytics schema (planned, not yet built):
  - monthly_app_opens: integer
  - bookings_made: integer
  - bookings_completed: integer
  - concierge_tier_used: enum [essentiel, confort, xl, noir]
  - community_interactions: integer (Alpine Circle feed activity)
  - support_tickets: integer
  - last_booking_date: date
  - days_since_last_visit: integer
- HIGH CHURN RISK signals: 0 bookings in 90 days, app opens <2/month, no concierge usage, support tickets with negative sentiment

CONCIERGE TIER AS RETENTION LEVER:
- Essentiel ($0): Low attachment — easy to leave
- Confort ($360): Medium attachment — noticed the difference
- XL ($720): High attachment — lifestyle expectation set
- Noir ($1,450): Very high attachment — can't imagine going back
- STRATEGY: Get every FO to Confort within first 3 stays (complimentary upgrade)
- ECONOMICS: Each tier upgrade increases switching cost AND revenue

ALPINE CIRCLE AS COMMUNITY MOAT:
- Fondateurs Alpins: 800 member cap — exclusivity IS retention
- Planned programming (not yet running):
  - Monthly: virtual coffee chats (15 min, casual, FR)
  - Quarterly: property showcase weekends (in-person, Laurentians)
  - Annually: Founder's Dinner (Justin hosts, Les 8 premiers recognized)
- Community roles: early adopters become ambassadors, contribute to property selection
- Peer connections: FOs who know other FOs are 3x less likely to leave (industry benchmark)

JUSTIN'S PERSONAL TOUCH:
- Justin personally calls every FO at Month 3, Month 6, and Month 10
- Month 3: "How was your first experience?"
- Month 6: "What would make this even better?"
- Month 10: "Let's talk about next year."
- Justin's time: ~15 min per call, max 10 FOs = 150 min/month = feasible at scale < 40 FOs

ROI REPORTING AS RETENTION TOOL:
- Monthly equity statement via app: property value, ownership %, equity growth
- Annual comparison: "You paid $31,608 this year. Solo ownership would have cost $96,000-$110,000."
- Savings visualization: "$64,000+ saved vs solo ownership"
- Equity dashboard: show real property appreciation data

CANON NUMBERS FOR CHURN ROI:
- FO LTV (3 year): $2,634 x 36 = $94,824
- Cost to acquire (referral): $94,824 / 35.4 = $2,678
- Cost to acquire (paid): $94,824 / 9.6 = $9,878
- Churn prevention budget justification: saving 1 FO = saving $2,678-$9,878 in acquisition cost
- Target spend: $500/FO/year on retention activities

DELIVERABLE — produce a single markdown document with:

1. CHURN RISK SCORING MODEL
   - iOS app signals weighted by predictive power
   - Engagement signals from Alpine Circle
   - Financial stress indicators
   - Composite score: Green (0-30) / Yellow (31-60) / Red (61-100)
   - Monthly scoring cadence

2. YEAR 1 INTERVENTION CALENDAR
   - Month-by-month touchpoints (Justin personal + automated)
   - Concierge tier upgrade triggers and offers
   - Alpine Circle integration milestones
   - ROI report delivery schedule

3. CONCIERGE TIER PROGRESSION PROGRAM
   - How to get every FO to Confort within 3 stays
   - Complimentary upgrade strategy and cost
   - Measurement: tier adoption rate by month
   - Upsell path to XL/Noir for high-engagement FOs

4. ALPINE CIRCLE RETENTION PROGRAMMING
   - Monthly/quarterly/annual event calendar
   - Community role assignments (ambassador, advisor, host)
   - Peer connection facilitation
   - Content creation by members (testimonials, photos, stories)

5. WIN-BACK SYSTEM
   - 30/60/90 day intervention protocols for at-risk FOs
   - Justin's personal outreach scripts
   - Re-engagement offers (not discounts — experiences)
   - Exit interview process for learnings

6. NPS AND FEEDBACK LOOP
   - NPS survey at Month 3, 6, 9, 12
   - In-app feedback mechanism
   - How feedback routes to product/service improvements
   - Close-the-loop communication with FOs

## TUNING GAPS: End with remaining gaps after Canon injection.
```
