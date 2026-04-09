# referral-program-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: referral-program

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/referral-program
**CoChalet Adaptation:** LTV:CAC 35.4:1 proves referral is the best channel. But CoChalet's referral engine must feel organic and community-driven, not incentive-gamed. Fondateurs Alpins community IS the referral engine. Design what referrers get, how it is tracked, and viral coefficient targets.

### Prompt for Hermes:

```
You are a referral program architect for a high-consideration, high-LTV product. Design CoChalet's Fondateur referral engine.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Referral channel performance: LTV:CAC 35.4:1 (vs. 9.6:1 paid). Referral is by far the highest-value channel.
- Product price point: high consideration ($2,634/month ongoing commitment). This is not a $50/month SaaS -- referrals carry real social risk.
- Community: Fondateurs Alpins, capped at 800 members
- Current referral program: none (informal, word-of-mouth only)
- Key insight: people who refer high-consideration products do it for STATUS and BELONGING, not for $50 gift cards
- Brand values: belonging (appartenance), pride (fierte)
- Martin's directive: "Montrer le reve. Pas expliquer la formule."

DELIVERABLE -- produce a single markdown document with:

1. REFERRAL ENGINE PHILOSOPHY
   - Why traditional referral incentives (cash, discounts) fail for high-consideration products
   - The status-based referral model: referrers are motivated by being seen as taste-makers, community builders, and trusted advisors
   - How the Fondateurs Alpins identity reinforces referral behavior ("I brought my friend into this exclusive community")
   - The difference between "referral program" (transactional) and "referral engine" (community-driven)

2. WHAT REFERRERS GET
   Design a 3-tier reward structure based on status, not cash:

   Tier 1: First Referral
   - Recognition (what form? naming? badge?)
   - Community status upgrade
   - Tangible but non-monetary benefit

   Tier 2: 3+ Referrals
   - Enhanced recognition
   - Exclusive access (what?)
   - Community title or role

   Tier 3: 5+ Referrals ("Ambassadeur Alpin")
   - Top-tier status in Fondateurs Alpins
   - Meaningful exclusive benefit (priority property selection? founder dinner? advisory role?)
   - Public recognition (with permission)

   For each tier: what the reward is, why it motivates, how it is delivered, cost to CoChalet

3. REFERRAL MECHANICS
   - How a referral is made (personal intro, shareable link, both?)
   - How a referral is tracked (CRM field, spreadsheet at scale=0, system at scale=100+)
   - Definition of "successful referral" (discovery call booked? co-ownership signed? both tracked separately?)
   - Timeline: when referrer is credited (at booking? at signing?)
   - Double-sided reward: does the referred person get anything? (e.g., "your friend is a Fondateur -- you are pre-approved for a discovery call")

4. VIRAL COEFFICIENT MODELING
   - Current baseline: 0 (no program exists)
   - Target viral coefficient: what is realistic for high-consideration real estate?
   - Model: if each Fondateur refers X people, and Y% convert to discovery call, and Z% become co-owners...
   - Sensitivity analysis: what referral rate is needed for self-sustaining growth?
   - Timeline to reach viral coefficient > 1.0 (if achievable for this product type)

5. REFERRAL MESSAGING
   - What Justin says to prompt referrals (natural, not forced)
   - Post-discovery-call prompt: "Who else might find this interesting?"
   - Post-signing prompt: "Welcome to the Fondateurs. Who should join you?"
   - Community prompt: "Know someone who'd love the Laurentians?"
   - Each with FR and EN versions
   - Shareable content that Fondateurs can send to friends (not a corporate brochure -- a personal recommendation tool)

6. ANTI-GAMING MEASURES
   - How to prevent incentive abuse (if rewards are status-based, this is less of a risk)
   - Quality over quantity: how to ensure referrals are qualified, not random names
   - What disqualifies a referral
   - How to handle awkward situations (referral does not convert, referrer feels embarrassed)

7. IMPLEMENTATION ROADMAP
   - Phase 1 (Month 1): Manual tracking, Justin asks personally
   - Phase 2 (Month 3): Simple tracking system, Tier 1 rewards active
   - Phase 3 (Month 6): Full 3-tier system, community-integrated
   - Tools needed at each phase
   - Budget estimate per phase

QUALITY CHECKS:
- Rewards are status/belonging-based, not primarily monetary
- Referral prompts feel natural, not scripted or pushy
- Program respects the social risk of high-consideration referrals
- Viral coefficient targets are realistic for real estate (not SaaS assumptions)
- Four Nevers compliance in all messaging examples
- Anti-gaming measures are proportionate (not paranoid)
```

### Expected Output:
`Hermes/deliverables/referral-program-fondateur-engine-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) rewards are genuinely status-based not just cash-with-extra-steps, (3) viral coefficient modeling is realistic for real estate (not SaaS), (4) referral messaging matches Justin's voice, (5) implementation roadmap is achievable for bootstrapped startup, (6) anti-gaming measures are proportionate.

---
