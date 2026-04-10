# programmatic-seo-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output builds SaaS integration pages and city-grid comparison pages at scale. CoChalet has a single property in a single region — mass location pages don't apply. The programmatic SEO opportunity is: comparison pages (CoChalet vs. solo ownership in specific scenarios), persona-specific deep work pages (by city, by profession), and FAQ interception pages for the "is this a timeshare?" objection cluster.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: programmatic-seo

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/programmatic-seo
**CoChalet Adaptation:** Three programmatic SEO opportunities: (1) Comparison pages targeting "chalet ownership alternatives" for specific buyer profiles, (2) Deep Work persona pages by city/profession targeting "remote work retreat Quebec" queries, (3) FAQ/objection interception for the Casadora competitor cluster (45.5% keyword contest). Single property means content depth beats content volume.

### Prompt for Hermes:

```
You are a programmatic SEO strategist for a single-property real estate co-ownership company. Design CoChalet's programmatic SEO strategy around content depth and persona specificity — not mass page generation.

IMPORTANT CONSTRAINT: CoChalet has ONE property (370 Mont la Tuque, Laurentides, QC).
This is NOT a multi-location product. Traditional "city + keyword" pSEO doesn't apply.
The opportunity is: persona-specific landing pages + comparison content + objection interception.

COMPETITOR SEO CONTEXT:
- Casadora: 45.5% keyword contest — primary threat on "chalet co-ownership Quebec" queries
- Pacaso: US market — less Quebec presence but brand awareness bleeds over
- Solo ownership content: dominates "acheter chalet laurentides" — must intercept with comparison angle
- The gap: nobody ranks for "deeded co-ownership chalet Quebec" — CoChalet can own this

THREE PROGRAMMATIC OPPORTUNITIES:

OPPORTUNITY 1 — DEEP WORK PERSONA PAGES BY PROFESSION
Template: "Le chalet des [profession] qui travaillent en profondeur"
Target queries: "remote work retreat Quebec," "chalet work from mountains," "télétravail chalet laurentides"
Page variants (5-8 pages):
- /deep-work/tech (CTOs, developers, product managers)
- /deep-work/consultant (independent consultants, coaches)
- /deep-work/creative (writers, filmmakers, musicians, designers)
- /deep-work/entrepreneur (founders, operators)
- /deep-work/executive (VPs, directors, C-suite)
Each page: same CUT pain framework, same product, profession-specific scenarios and language.
Shared elements: Thursday Evening narrative, app demo CTA, "Applique pour te qualifier"

OPPORTUNITY 2 — COMPARISON PAGES (intercept competitor + solo ownership queries)
Template: "CoChalet vs. [alternative]"
Target queries: "casadora vs cochalet," "chalet copropriété alternatives," "acheter chalet vs louer"
Page variants:
- /vs/solo-ownership ("The $101K Buyer Tax" framework — solo ownership costs 2.3x more in Year 1)
- /vs/airbnb-rental ("Three years, $120K, zero equity" — Justin's story as SEO content)
- /vs/casadora (factual comparison — no attacks, just model differences)
- /vs/timeshare (intercept "is this a timeshare?" with definitive answer)
- /vs/vacation-club (same — intercept confusion queries)
CRITICAL: /vs/timeshare and /vs/vacation-club pages MUST lead with clear distinction.
These pages intercept the confusion — they don't avoid the word, they define against it.

OPPORTUNITY 3 — FAQ INTERCEPTION PAGES
Template: Answer one specific objection question per page
Target queries: long-tail objection searches
Page variants:
- /faq/est-ce-que-je-recois-des-revenus-location
- /faq/combien-de-nuits-par-annee
- /faq/comment-fonctionne-la-revente
- /faq/qui-gere-la-propriete
- /faq/difference-avec-timeshare (high priority — intercepts confused searchers)
Each page: 400-600 words, conversational, FR primary, answers directly and honestly

CONTENT TEMPLATE DESIGN:

For each programmatic template, define:
- H1 formula
- Meta title formula (< 60 chars)
- Meta description formula (< 155 chars)
- Introduction paragraph formula (2 sentences, persona-specific)
- 3 core sections (consistent across all pages in template)
- CTA placement (after section 2 — not at the very end)
- Internal linking: always links to /property, /apply, and one persona page
- Word count target: 600-800 words (enough for SEO, not so long it becomes content for content's sake)

DELIVERABLE — produce a single markdown document with:

1. TEMPLATE DESIGNS (3 templates)
   For each template:
   - URL pattern
   - H1 formula
   - Meta title/description formulas
   - Core section outlines
   - Variable vs. fixed content (what changes per page, what stays)
   - Example: one fully written sample page per template

2. PAGE INVENTORY (priority-ordered)
   Full list of pages to build across all 3 templates
   For each: URL, target query, estimated monthly searches (if available), priority (P0/P1/P2)
   P0 pages to build first (launch month): 5-8 pages maximum

3. INTERNAL LINKING STRATEGY
   How programmatic pages link to each other and to core pages
   Anchor text conventions
   Pillar page → spoke page relationship

4. CONTENT FRESHNESS PLAN
   How to update these pages as real data becomes available:
   - When first FO stories are available → add to comparison pages
   - When app demo video is live → embed on deep work persona pages
   - When Alpine Circle grows → add community proof to FAQ pages

COMPLIANCE:
- /vs/timeshare page: may USE the word "timeshare" only to define AGAINST it
  ("CoChalet is NOT a timeshare. Here is why: [factual distinction]")
  This is the ONE exception to the Four Nevers for SEO interception purposes.
  The page body must never IMPLY CoChalet is a timeshare — only define the distinction.
- /vs/casadora: factual only. No attacks. Model differences, not quality judgments.
- All comparison pages: use PUBLIC numbers only ($2,634/month, 37 nights, $71/night effective)
- Never expose DSCR, NOI, FO Stake, or take rate on any public-facing page

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Search volume data: estimates only — Semrush/Ahrefs data not yet pulled for Quebec real estate queries
- Casadora keyword data: "45.5% keyword contest" is from competitor analysis — specific overlapping keywords not yet mapped
- Deep work persona pages: profession-specific scenarios written without real DW customer interview data
- /vs/timeshare page: legal review recommended before publishing (defamation risk if comparison is inaccurate)
- Content production capacity: 15-25 programmatic pages requires production sprint — not a one-session task
- FR vs EN: programmatic pages recommended FR-first for Quebec audience — bilingual versions are Phase 2
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- No keyword research data yet — all target queries are hypothesized from persona profiles
- /vs/timeshare SEO opportunity: confirmed by competitor analysis but specific query volumes unknown
- Deep work persona page variants: 5 professions proposed — actual DW distribution not validated
- Casadora keyword overlap: estimated 45.5% — specific overlapping query list not yet extracted
- Content template: sample pages not yet tested for ranking — schema + internal linking is hypothesis
- Phase 2 scaling: 15-25 pages assumes consistent content quality — production pipeline not yet established
