# paid-ads-cochalet

DBA verdict: ADAPT (2026-04-09). Generic output scored 7/10 but missing Quebec Bill 101 compliance, SparkToro channel data, Casadora ad intelligence, and seasonal patterns.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: paid-ads

**Model:** sonnet-hermes
**Status:** STAGING (DBA ADAPT → re-execute with Canon injection)
**Original:** coreyhaines31/marketingskills/paid-ads
**CoChalet Adaptation:** Quebec-specific compliance. SparkToro channel hierarchy. Seasonal Laurentian demand. Justin's origin story as ad creative.

### Prompt for Hermes:

```
You are a paid media strategist for a Quebec luxury real estate brand. Design CoChalet's $500/month paid advertising test strategy with FULL Quebec compliance.

QUEBEC COMPLIANCE (MANDATORY):
- Bill 101 (Loi 101): ALL advertising in Quebec must be in French. English allowed as SECONDARY language only.
- French must be "markedly predominant" — larger text, first in sequence, more prominent placement
- All ad copy must be written French-first, English-second
- Platform-specific: Meta allows bilingual ads; LinkedIn can geo-target language
- Real estate advertising in Quebec has specific disclosure requirements (check with legal)

SPARKTORO CHANNEL DATA (from audience research):
- YouTube: 95.7% reach for BOTH personas (DW + PC) — this is the #1 channel
- Reddit: 81.4% reach for Deep Workers
- Facebook: 76.9% reach for Propriétaires Curieux
- LinkedIn: moderate reach but highest intent for professional targeting
- Instagram: visual storytelling channel, not primary conversion
- INSIGHT: YouTube should be the primary channel, NOT LinkedIn (contradicts generic assumption)

SEASONAL LAURENTIAN DEMAND:
- Peak 1 (Dec-Mar): Ski season — highest search volume, "chalet" keywords spike
- Peak 2 (Jun-Aug): Summer lake season — family + remote work retreats
- Peak 3 (Oct): Fall foliage — weekend getaway searches
- Low (Apr-May, Nov): Shoulder seasons — lower CPM, good for testing
- STRATEGY: Heavy spend in peaks, test creative in shoulders

COMPETITIVE AD INTELLIGENCE:
- Casadora: Quebec-based, likely running Meta ads targeting similar audience
- Pacaso: US-focused, no significant Quebec ad presence
- Traditional real estate: high ad spend but generic messaging
- CoChalet advantage: authentic founder story (Justin lost $120K on Airbnb)

FOUNDER STORY AD CREATIVE:
- Justin lost $120K over 3 years hosting on Airbnb with ZERO ownership
- This pain point is REAL and resonates with anyone who rents vacation properties
- "I spent $120K on someone else's dream. Then I built CoChalet."
- This is the highest-performing creative angle (authentic, emotional, specific)

LANDING PAGE REALITY:
- cochalet.co is currently PARKED (not live)
- Ads CANNOT run until a landing page exists
- Options: (a) wait for full site, (b) deploy single landing page on Cloudflare Pages first
- Recommendation: deploy cochalet.co/decouverte as a standalone page BEFORE full site

TARGET AUDIENCE:
- Deep Workers: 35-55, $150K+ HHI, Montreal/Laurentians, remote professionals
- Propriétaires Curieux: 35-55, Quebec homeowners considering second property
- Both personas value: ownership, community, lifestyle, not just investment

DELIVERABLE — produce a single markdown document with:

1. CHANNEL STRATEGY (REVISED based on SparkToro)
   - YouTube: primary awareness + education (60% of strategy focus)
   - Meta (FB/IG): retargeting + community building
   - LinkedIn: professional targeting for DW persona
   - Budget allocation across channels ($500/mo)

2. CREATIVE STRATEGY (BILINGUAL FR-FIRST)
   - 4 creative angles with FR and EN copy
   - Justin's origin story as hero creative
   - Community (Fondateurs Alpins) as social proof
   - Investment/equity as rational anchor
   - Lifestyle transformation as emotional hook

3. QUEBEC COMPLIANCE CHECKLIST
   - Bill 101 requirements per platform
   - French-first creative specs
   - Disclosure requirements for real estate ads
   - Legal review recommendations

4. SEASONAL CAMPAIGN CALENDAR
   - Monthly budget allocation aligned with demand peaks
   - Creative rotation schedule
   - Testing plan for shoulder seasons

5. LANDING PAGE REQUIREMENTS
   - What cochalet.co/decouverte needs before ads run
   - Minimum viable landing page spec
   - Conversion tracking setup (GA4 events)

6. 90-DAY TEST PLAN with weekly milestones

## TUNING GAPS: End with remaining gaps after Canon injection.
```
