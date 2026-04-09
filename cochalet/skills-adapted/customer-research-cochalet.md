# customer-research-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: customer-research

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/customer-research
**CoChalet Adaptation:** DW and PC persona deepening. CoChalet needs discovery call interview questions, a survey for broader validation, and a methodology for refining personas as real data comes in. Current personas are hypothesis-based, not data-validated.

### Prompt for Hermes:

```
You are a customer research strategist for a pre-launch real estate product. Design the research methodology to deepen and validate CoChalet's target personas.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Current persona status: hypothesis-based, not yet validated with real customer data
- Discovery calls: Justin conducts 15-minute calls. These are the primary research opportunity.
- Target audience 1 -- Deep Workers (DW):
  - Hypothesis: remote professionals, 30-45, Montreal-based, $120K+, seasonal cottage renters
  - Pain (CUT): Context Switching, Unproductive, Time-Consuming
  - Current persona health: unknown (no data yet)
- Target audience 2 -- Proprietaires Curieux (PC):
  - Hypothesis: Quebec homeowners, 35-55, considering cottage purchase, concerned about cost and maintenance
  - Emotions: Soulagement, Fierte, Appartenance
  - Current persona health: 5.4/10 (Casadora comparison)
- Research constraints: bootstrapped, no budget for focus groups or paid panels. Leverage discovery calls, online surveys, and social listening.

DELIVERABLE -- produce a single markdown document with:

1. DISCOVERY CALL INTERVIEW GUIDE
   Design a structured interview guide for Justin's 15-minute discovery calls that serves dual purpose: sales conversation AND research data collection.

   a. Opening (2 min):
   - Rapport-building questions that reveal lifestyle context
   - How did you hear about CoChalet?

   b. Pain exploration (5 min):
   - Questions that validate or invalidate CUT framework
   - "Walk me through your last cottage weekend -- from planning to returning home"
   - "What is the most frustrating part of your current cottage situation?"
   - "If you could change one thing about how you access the mountains, what would it be?"
   - Open-ended questions that reveal pains we have not hypothesized

   c. Solution fit (3 min):
   - "When you hear 'deeded co-ownership,' what comes to mind?"
   - "What concerns you most about this model?"
   - "What would make you say yes today? What would make you say no?"

   d. Persona validation (3 min):
   - Demographic validation questions (age, location, income bracket, remote work status)
   - Media consumption (where do you get information about lifestyle/real estate?)
   - Decision-making: "Who else would be involved in this decision?"

   e. Closing (2 min):
   - Referral prompt: "Who else do you know who might find this interesting?"
   - Permission to follow up

   f. Post-call research notes template
   - Structured form Justin fills out after each call
   - Fields: pain confirmed (Y/N for each CUT dimension), new pains discovered, objections raised, persona fit (DW/PC/Other), referral likelihood (1-5)

2. ONLINE SURVEY DESIGN
   - 10-question survey for broader validation (LinkedIn, email list)
   - Question types: multiple choice, Likert scale, one open-ended
   - Screening question to qualify DW vs. PC vs. other
   - Questions that validate CUT and emotion frameworks
   - Distribution strategy (where to post, how to incentivize completion)
   - Sample size target for statistical relevance
   - Tool recommendation (Typeform, Google Forms, Tally)

3. SOCIAL LISTENING METHODOLOGY
   - Where DW and PC prospects talk about cottages/chalets online (Reddit, Facebook groups, LinkedIn)
   - Specific subreddits, Facebook groups, LinkedIn communities to monitor
   - Keywords to track
   - What to look for: language patterns, pain expressions, competitor mentions
   - How to capture and organize findings

4. PERSONA REFINEMENT METHODOLOGY
   - After N discovery calls, how to update DW and PC personas
   - Persona card template (demographic, psychographic, behavioral, pain, emotion, channel preference)
   - "Jobs to Be Done" framework applied to chalet co-ownership
   - How to identify segments within DW and PC (sub-personas)
   - When to split a persona vs. merge findings

5. COMPETITOR RESEARCH INTEGRATION
   - What to learn from Casadora's apparent customer base
   - Public sources of competitor customer data (reviews, social, press mentions)
   - How to position discovery call questions to understand competitive landscape without being pushy

6. RESEARCH TIMELINE
   - Month 1: Discovery call guide deployed, first 10 calls analyzed
   - Month 2: Survey launched, social listening started
   - Month 3: First persona update based on real data
   - Ongoing: quarterly persona refresh cycle

QUALITY CHECKS:
- Interview questions feel like natural conversation, not interrogation
- Questions do not lead the witness (no "Don't you hate renting?")
- Research methodology is practical for a solo founder (Justin does the calls)
- Survey is short enough to complete in under 3 minutes
- Persona refinement process is clear and repeatable
- No questions expose internal metrics or strategy to prospects
```

### Expected Output:
`Hermes/deliverables/customer-research-dw-pc-methodology-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) interview questions are conversational, not leading, (2) dual purpose (sales + research) is balanced, (3) survey is genuinely completable in 3 minutes, (4) social listening targets are real communities, (5) persona refinement methodology is systematic, (6) research timeline is achievable for solo founder.

---
