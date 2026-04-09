# community-marketing-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: community-marketing

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/community-marketing
**CoChalet Adaptation:** Alpine Circle is the broader community concept. Fondateurs Alpins is the 800-cap exclusive inner circle of actual/prospective co-owners. Community is both online (WhatsApp, events) and in-person (chalet weekends, Montreal meetups). Referral engine is the growth mechanism.

### Prompt for Hermes:

```
You are a community strategist specializing in high-consideration luxury products. Design the community strategy for CoChalet's Alpine Circle and Fondateurs Alpins.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Community names:
  - Alpine Circle: broader community of people interested in Alpine lifestyle, co-ownership, remote work from the mountains
  - Fondateurs Alpins: exclusive inner circle, capped at 800 members, consisting of actual and prospective co-owners (Fondateurs = Founders)
- Current community size: ~0 (building from scratch)
- Target community size: 800 Fondateurs Alpins within 18 months
- Community purpose: belonging, referral generation, owner satisfaction, brand advocacy
- Referral channel LTV:CAC: 35.4:1 (best channel by far -- community IS the growth engine)
- Brand values: belonging (appartenance), pride (fierte), relief (soulagement)
- Martin's directive: "Montrer le reve. Pas expliquer la formule."
- Tone: warm, inclusive, exclusive without being elitist

DELIVERABLE -- produce a single markdown document with:

1. COMMUNITY ARCHITECTURE
   - Alpine Circle (open tier):
     - Purpose and positioning
     - Entry requirements (none -- open to anyone interested)
     - Content and value proposition for members
     - Platforms (newsletter, Instagram community, LinkedIn group)
   - Fondateurs Alpins (exclusive tier):
     - Purpose and positioning (the "inner sanctum")
     - Entry requirements (discovery call completed, genuine interest in co-ownership)
     - 800-cap strategy: how exclusivity drives value
     - Platform (WhatsApp group? Private Slack? App-based?)
     - What members get that non-members do not

2. CONTENT CALENDAR (monthly template)
   - Weekly rhythm for Alpine Circle content
   - Monthly Fondateurs Alpins exclusive content
   - Quarterly in-person event cadence
   - Content themes that reinforce belonging without being cheesy

3. IN-PERSON EVENT STRATEGY
   - Chalet weekends (showcase properties, community bonding)
   - Montreal meetups (accessible, low-commitment entry point)
   - Seasonal events (ski season kickoff, summer BBQ, fall foliage)
   - Event format, frequency, budget estimates
   - How events feed the referral engine

4. ONLINE COMMUNITY MANAGEMENT
   - Platform selection rationale
   - Moderation guidelines
   - Engagement metrics to track
   - How Justin shows up in the community (founder presence, not absentee)
   - Content that sparks conversation vs. content that gets ignored

5. REFERRAL ENGINE DESIGN
   - How community members refer new prospects
   - What triggers a referral (genuine enthusiasm, not incentive gaming)
   - Tracking mechanism (manual at first, systematized later)
   - How referral success reinforces community belonging

6. GROWTH STRATEGY (0 to 800)
   - Phase 1 (Month 1-3): Founding 50 (hand-picked, high-touch)
   - Phase 2 (Month 4-6): First 200 (referral from founding 50 + targeted outreach)
   - Phase 3 (Month 7-12): Scale to 500 (events + content + referrals)
   - Phase 4 (Month 12-18): Approach 800 cap (waitlist, exclusivity)
   - Milestone celebrations at 100, 250, 500, 800

7. COMMUNITY HEALTH METRICS
   - Monthly active members (MAM) targets
   - Referral rate per member
   - Event attendance rate
   - Net Promoter Score for community experience
   - Churn indicators and intervention triggers

QUALITY CHECKS:
- Community strategy feels exclusive but not elitist
- No mention of internal metrics (LTV:CAC, take rate) in any community-facing copy
- Events are achievable for a bootstrapped startup (realistic budgets)
- Justin's founder presence is central, not delegated
- Strategy accounts for bilingual community (FR-primary, EN welcome)
```

### Expected Output:
`Hermes/deliverables/community-marketing-alpine-circle-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) 800-cap logic is sound (why 800, what happens at cap), (3) referral engine is organic not incentive-driven, (4) event strategy is realistic for a bootstrapped company, (5) growth phases are achievable, (6) bilingual community management is addressed.

---
