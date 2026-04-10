# onboarding-cro-cochalet

DBA verdict: ADAPT (2026-04-09). Generic output scored 7/10 but missing iOS app actual capabilities, concierge delivery specifics, and welcome kit design.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: onboarding-cro

**Model:** sonnet-hermes
**Status:** STAGING (DBA ADAPT → re-execute with Canon injection)
**Original:** coreyhaines31/marketingskills/onboarding-cro
**CoChalet Adaptation:** iOS app is LIVE with real features. Concierge tiers have specific service components. Welcome kit is a design opportunity. Pioneer tier recognition matters.

### Prompt for Hermes:

```
You are an onboarding experience designer for a luxury co-ownership brand. Design CoChalet's FO onboarding journey with REAL product data.

IOS APP CAPABILITIES (ACTUALLY BUILT):
- Audience mode switcher: FO Owner / Alpine Circle / Guest — three distinct views
- Property booking calendar with availability
- Concierge service booking (tier selection)
- Usage analytics dashboard (stays, spend, equity)
- Community feed (Alpine Circle interactions)
- Push notifications
- 8 Simulator screenshots available for demo
- App Store: live but not publicly promoted yet

CONCIERGE TIER SERVICE DELIVERY:
- Essentiel ($0/stay): Self-service check-in, digital lock code via app, basic amenities, no personal service
- Confort ($360/stay): Pre-arrival communication, premium linens, stocked kitchen basics, welcome note
- XL ($720/stay): Personal concierge contact, custom grocery list, activity recommendations, mid-stay check-in
- Noir ($1,450/stay): Full white-glove service, private chef option, curated activity itinerary, personal host, departure gift

PIONEER RECOGNITION:
- "Les 8 premiers" — first 8 FOs get special Pioneer status
- Pioneer benefits: permanent recognition in community, priority booking, founding member events
- This is a POWERFUL onboarding hook — early adopters feel part of history

NOTARY PROCESS (Quebec-specific):
- Timeline: ~30 days from verbal commitment to deed registration
- Process: Justin coordinates with notary, FO signs at notary office, deed registered at land registry
- FO receives: copy of registered deed, property documentation package
- This is the LEGAL moment of ownership — make it ceremonial, not bureaucratic

WELCOME KIT (NOT YET DESIGNED — OPPORTUNITY):
- Physical kit delivered to FO's home address
- Potential contents: branded welcome letter from Justin, property guide, Fondateurs Alpins member card, local area guide (Laurentians), digital lock setup instructions, app download QR code
- Budget: TBD (recommend $50-150 per kit for premium feel)

ONBOARDING TIMELINE:
Day 0: Verbal commitment on discovery call
Day 1-7: Due diligence package sent, notary coordination begins
Day 8-30: Notary process, deed registration
Day 30: Ownership confirmed — Welcome Kit ships
Day 31-37: App onboarding sequence (push notifications guiding through features)
Day 38-60: First stay booking encouraged (target: book within 30 days of ownership)
Day 60-90: Community integration (Alpine Circle event invitation, peer introduction)

DELIVERABLE — produce a single markdown document with:

1. ONBOARDING JOURNEY MAP
   - Day-by-day timeline from commitment to first stay
   - Touchpoints (Justin personal, automated, community)
   - Emotional arc design (excitement → confidence → belonging)

2. WELCOME KIT DESIGN
   - Contents list with cost estimates
   - Unboxing experience design
   - Personalization opportunities
   - Production logistics

3. APP ONBOARDING SEQUENCE
   - Push notification schedule (first 30 days)
   - In-app tutorial flow
   - Feature discovery order (what to show first)
   - Concierge tier introduction and first upgrade offer

4. FIRST STAY OPTIMIZATION
   - How to ensure the first stay is exceptional
   - Complimentary Confort upgrade for first visit
   - Feedback collection after first stay
   - Photo opportunity for community content

5. COMMUNITY INTEGRATION
   - Alpine Circle introduction process
   - Buddy system pairing
   - First event invitation timing
   - Contribution opportunities

6. SUCCESS METRICS
   - 30-day activation rate targets
   - First stay booking timeline targets
   - App engagement benchmarks
   - Tier adoption within first 90 days

## TUNING GAPS: End with remaining gaps after Canon injection.
```
