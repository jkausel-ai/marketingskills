# lead-magnets-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: lead-magnets

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/lead-magnets
**CoChalet Adaptation:** DW-specific content offers that provide genuine value and capture contact information. Each lead magnet must be useful even if the person never becomes a co-owner. Ideas include ROI calculator, ownership guide, and chalet selection quiz. Bilingual.

### Prompt for Hermes:

```
You are a lead generation strategist. Design 5 lead magnets for CoChalet targeting Deep Workers.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Product: deeded co-ownership of luxury chalets
- Target: Deep Workers (DW) -- remote professionals, 30-45, Montreal-based, $120K+
- Conversion goal: email capture -> nurture sequence -> discovery call booking
- Current email list: 0 subscribers
- Brand tone: warm, factual, zero superlatives
- Content quality bar: every lead magnet must be genuinely useful even if the person never becomes a co-owner
- Martin's directive: "Montrer le reve. Pas expliquer la formule." -- Show the dream, not the formula.
- Language: Create in French first, with English adaptation notes
- Slogan: "Arrivez et vivez." / "Deep Work. Deep Play. Your Deed."

DELIVERABLE -- produce a single markdown document with 5 complete lead magnet designs:

### LEAD MAGNET 1: ROI Calculator
"Combien te coute vraiment ta vie en location?" / "What Is Renting Really Costing You?"

- Format: Interactive web calculator (specification for development team)
- What it calculates:
  - Annual rental spending on chalets/cottages
  - 5-year total with zero equity
  - Comparison: same spend applied to deeded co-ownership (equity built)
  - NOT a financial projection or investment return -- purely a cost comparison
- Inputs required from user: annual rental budget, frequency of visits, preferred region
- Output: visual comparison (rental vs. ownership), personalized summary
- Email capture: results delivered by email
- Follow-up: automated email with "Want to see how this works in practice? Book a discovery call."
- Build complexity: medium (requires calculator logic, email integration)
- IMPORTANT: calculator must NOT promise returns, appreciation, or investment performance. It compares COST, not RETURN.

### LEAD MAGNET 2: Guide -- "Le guide du Deep Worker pour la propriete alpine"
"The Deep Worker's Guide to Alpine Ownership"

- Format: 12-15 page PDF guide
- Table of contents:
  1. Why Deep Workers are choosing the Laurentians
  2. The true cost of renting vs. owning (not a sales pitch -- genuine comparison)
  3. What is deeded co-ownership? (plain language, not legal jargon)
  4. How scheduling works (addressing the "but when can I use it?" objection)
  5. The Fondateurs Alpins community
  6. 5 questions to ask before committing to any co-ownership model
  7. A checklist: "Is alpine co-ownership right for you?"
- Tone: educational, not salesy. Genuinely useful.
- Email capture: download in exchange for email
- Follow-up: 3-email nurture sequence after download
- Design direction: clean, minimal, Explorateur aesthetic (mountains, natural light, workspace imagery)
- Build complexity: low (Hermes drafts text, design in Canva)

### LEAD MAGNET 3: Quiz -- "Quel chalet te correspond?"
"Which Chalet Matches Your Style?"

- Format: interactive quiz (5-7 questions)
- Questions:
  1. When you imagine your ideal weekend, you see... (options: deep work in solitude / family adventure / dinner with friends / outdoor sports)
  2. Your perfect morning starts with... (options: coffee overlooking the forest / yoga on the deck / a ski run / sleeping in)
  3. How often would you escape to the mountains? (monthly / bi-weekly / weekly / whenever possible)
  4. What matters most in a retreat? (silence / community / nature / design)
  5. Your work style is... (focused blocks / flexible / meetings-heavy / creative sprints)
- Results: 3-4 chalet personality types (e.g., "Le Contemplatif", "L'Aventurier", "Le Social", "Le Createur")
- Each result: personality description, recommended chalet style, next step (discovery call CTA)
- Email capture: results delivered by email
- Shareability: results designed to be shared on social media ("I'm Le Contemplatif! What are you?")
- Build complexity: medium (quiz logic, email integration, social share cards)

### LEAD MAGNET 4: Checklist -- "10 questions a poser avant de s'engager en copropriete"
"10 Questions to Ask Before Committing to Co-Ownership"

- Format: 1-page downloadable PDF checklist
- Questions (genuinely useful, brand-agnostic):
  1. Is the ownership deeded and registered with the land registry?
  2. What are the total monthly costs (mortgage, maintenance, services)?
  3. How is scheduling managed? Can I book any week I want?
  4. What happens if I want to sell my share?
  5. Who handles maintenance and property management?
  6. What is the legal structure? (indivision, co-op, corporation?)
  7. Are there hidden fees (special assessments, capital calls)?
  8. Can I visit the property before committing?
  9. Who else are the co-owners? Is there a community?
  10. What is the exit process and timeline?
- Why this works: positions CoChalet as transparent and trustworthy. Every question, CoChalet answers well. Competitor comparison happens naturally.
- Email capture: download in exchange for email
- Build complexity: very low (Hermes drafts, design in Canva, 1 page)

### LEAD MAGNET 5: Mini-Course -- "5 jours pour comprendre la copropriete alpine"
"5 Days to Understanding Alpine Co-Ownership"

- Format: 5-email mini-course delivered over 5 days
- Day 1: "Why 67% of cottage renters never build equity" (problem awareness)
- Day 2: "Deeded co-ownership: what it is and what it is NOT" (education, address timeshare misconception)
- Day 3: "A day in the life of a Fondateur Alpin" (aspiration, lifestyle)
- Day 4: "The numbers: what it actually costs" (transparency, $2,634/month in context)
- Day 5: "Is this right for you? A self-assessment" (qualification, CTA to discovery call)
- Each email: ~400 words, one key takeaway, one visual
- Email capture: sign up for mini-course
- Build complexity: low (Hermes drafts all 5 emails, set up in email tool)

### FOR EACH LEAD MAGNET, ALSO SPECIFY:
- Landing page headline (FR and EN)
- Landing page subheadline
- What info to capture (email only? email + first name? email + phone?)
- Recommended capture tool (Tally, Typeform, ConvertKit, custom)
- Promotion strategy (where to promote this lead magnet)
- Expected conversion rate benchmark (realistic for this format and audience)
- Nurture sequence that follows (brief outline)

QUALITY CHECKS:
- Every lead magnet is genuinely useful, not just a gated sales pitch
- No lead magnet promises investment returns or financial performance
- "Deeded co-ownership" is the only term used (never "timeshare" or "fractional")
- ROI calculator compares costs, not returns
- Quiz results are fun and shareable, not corporate
- Checklist is brand-agnostic enough to feel trustworthy (CoChalet wins on answers, not on bias)
- All content directions include FR and EN
- No internal metrics (DSCR, NOI, take rate) appear in any public-facing content
```

### Expected Output:
`Hermes/deliverables/lead-magnets-dw-content-offers-GPTOSS.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance across all 5 lead magnets, (2) each lead magnet is genuinely useful (not gated sales pitch), (3) ROI calculator does NOT promise returns, (4) quiz is fun and shareable, (5) checklist is fair and positions CoChalet through transparency, (6) email capture requirements are proportionate (not asking for phone number on a checklist download), (7) build complexity estimates are realistic.

---

## Summary Table

| # | Skill | Model | Estimated Cost | Priority |
|---|-------|-------|---------------|----------|
| 1 | seo-audit | sonnet-hermes | ~$0.45 | P1 |
| 2 | ai-seo | sonnet-hermes | ~$0.45 | P1 |
| 3 | page-cro | sonnet-hermes | ~$0.45 | P1 |
| 4 | copy-editing | gpt-oss-120b | ~$0.04 | P1 |
| 5 | cold-email | gpt-oss-120b | ~$0.04 | P1 |
| 6 | community-marketing | sonnet-hermes | ~$0.45 | P1 |
| 7 | ab-test-setup | sonnet-hermes | ~$0.45 | P1 |
| 8 | competitor-alternatives | gpt-oss-120b | ~$0.04 | P1 |
| 9 | launch-strategy | sonnet-hermes | ~$0.45 | P1 |
| 10 | marketing-psychology | sonnet-hermes | ~$0.45 | P1 |
| 11 | customer-research | sonnet-hermes | ~$0.45 | P1 |
| 12 | referral-program | sonnet-hermes | ~$0.45 | P1 |
| 13 | lead-magnets | gpt-oss-120b | ~$0.04 | P1 |
| | **Total Wave 2** | | **~$4.17** | |

## Deployment Sequence

**Recommended execution order (dependencies flow downward):**

1. **customer-research** (informs all other skills with validated personas)
2. **marketing-psychology** (provides the emotional framework for all content)
3. **seo-audit** + **ai-seo** (parallel -- architecture before content)
4. **page-cro** (depends on SEO architecture and psychology framework)
5. **competitor-alternatives** (parallel with page-cro)
6. **launch-strategy** (depends on page-cro and competitor positioning)
7. **community-marketing** + **referral-program** (parallel -- community engine)
8. **ab-test-setup** (depends on launch strategy defining what to test)
9. **cold-email** + **lead-magnets** (parallel -- outbound + inbound)
10. **copy-editing** (runs LAST on every output from skills 1-12)

---

*File generated 2026-04-08 by COS Opus 4.6. All prompts adapted from coreyhaines31/marketingskills (MIT license). Gate check required before any skill moves to PRODUCTION.*
