# launch-strategy-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: launch-strategy

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/launch-strategy
**CoChalet Adaptation:** DW campaign launch in 3 phases: organic first (LinkedIn/Instagram), paid amplification second, referral engine third. CoChalet is bootstrapped -- no large launch budget. Marketing health is 41/100 with zero posts published. This is starting from zero.

### Prompt for Hermes:

```
You are a go-to-market strategist for a bootstrapped real estate startup. Design the DW campaign launch plan for CoChalet.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Current state: Marketing health 41/100, zero posts published, website minimal
- Budget: Bootstrapped. No large launch budget. Paid spend: $500/month test budget (Phase 2).
- Target: Deep Workers (DW) -- remote professionals, 30-45, Montreal-based, $120K+
- Secondary target: Proprietaires Curieux (PC) -- Quebec homeowners
- Conversion goal: Discovery call bookings with Justin
- Community: Fondateurs Alpins (0 current, 800 cap)
- Channels available: LinkedIn (Justin's personal + CoChalet page), Instagram (@cochalet), Email, cochalet.co
- Content ready: Zero. Content strategy and copywriting skills are in PRODUCTION but no content has been published.
- Competitive timing: Casadora is active. Window to establish positioning is now.
- Slogan: "Arrivez et vivez." / "Deep Work. Deep Play. Your Deed."
- Brand archetype: Explorateur + Soignant

DELIVERABLE -- produce a single markdown document with:

1. LAUNCH TIMELINE (12-week plan)
   Week-by-week milestones, deliverables, and success metrics

2. PHASE 1: ORGANIC FOUNDATION (Weeks 1-4)
   - LinkedIn strategy:
     - Justin personal profile optimization
     - CoChalet company page setup
     - Posting cadence (3x/week minimum)
     - Content pillars: (1) founder story, (2) Laurentian lifestyle, (3) co-ownership education, (4) community building
     - First 10 post concepts (headlines + hooks)
     - Engagement strategy (comments, DMs, group participation)
   - Instagram strategy:
     - @cochalet profile setup and bio
     - Visual identity guidelines (what the feed looks like)
     - Content mix: lifestyle photography, founder behind-the-scenes, property glimpses, community moments
     - Story strategy
     - Posting cadence
     - First 10 post concepts
   - Email strategy:
     - List building approach (no list exists yet)
     - Welcome sequence (3 emails for new subscribers)
     - Newsletter concept and cadence
   - Success metrics for Phase 1:
     - LinkedIn: followers, engagement rate, DM conversations, discovery call bookings
     - Instagram: followers, engagement rate, profile visits
     - Email: list size, open rate

3. PHASE 2: PAID AMPLIFICATION (Weeks 5-8)
   - Budget allocation ($500/month)
   - LinkedIn Ads: targeting parameters, ad formats, creative direction
   - Instagram/Meta Ads: targeting, format, creative
   - Retargeting setup
   - A/B test plan (connects to ab-test-setup skill)
   - Success metrics: cost per discovery call booking, ROAS proxy

4. PHASE 3: REFERRAL ENGINE (Weeks 9-12)
   - Fondateurs Alpins activation
   - Referral mechanism launch
   - Community event (first in-person gathering)
   - Viral coefficient targets
   - Success metrics: referrals per member, discovery calls from referrals

5. CONTENT PRODUCTION SCHEDULE
   - Weekly content calendar template
   - Content batching strategy (produce a week of content in one session)
   - Bilingual content workflow (create in FR, adapt to EN)
   - Content approval flow (Hermes drafts -> copy-editing skill -> Justin review -> publish)

6. RISK MITIGATION
   - What if organic does not gain traction by Week 4?
   - What if paid spend does not convert by Week 8?
   - What if Casadora launches an aggressive campaign during our launch?
   - Pivot triggers and contingency plans

7. LAUNCH METRICS DASHBOARD
   - Weekly tracking template
   - KPIs by phase
   - "North Star" metric: discovery calls booked per week
   - Target: 5 discovery calls/week by end of Week 12

QUALITY CHECKS:
- Plan is realistic for a single founder with AI-assisted marketing (no team of 10)
- Budget is respected ($500/month paid, rest is organic/sweat equity)
- Content concepts are specific to CoChalet, not generic "post about your industry"
- Timeline accounts for content creation time (Hermes handles drafts, Justin reviews)
- Phase transitions have clear trigger criteria
- Four Nevers compliance in all content concepts
```

### Expected Output:
`Hermes/deliverables/launch-strategy-dw-campaign-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) timeline is realistic for solo founder + Hermes, (3) budget is respected, (4) content concepts are specific and on-brand, (5) success metrics are measurable, (6) risk mitigation is practical, (7) phase transitions have clear gates.

---
