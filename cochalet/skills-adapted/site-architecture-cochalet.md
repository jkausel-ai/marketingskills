# site-architecture-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output builds SaaS marketing site structures (features, pricing, docs, blog, signup). CoChalet's site architecture must be organized around personas and emotional journeys — not feature lists. The DW persona page (/deep-work), the property page, and the apply page are the three critical paths. Every page leads to one action: book a 15-minute call with Justin.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: site-architecture

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/site-architecture
**CoChalet Adaptation:** Three primary user journeys: DW path (LinkedIn → /deep-work → /apply → call), PC path (Facebook → homepage → /property → /apply → call), and Investor path (referral → /how-it-works → apply). The app demo is now a mandatory page element (TRACTION April 9: "See Demo" before "Apply"). URL structure must be SEO-friendly for Quebec real estate + deep work keywords.

### Prompt for Hermes:

```
You are an information architect for a high-consideration luxury real estate product. Design CoChalet's website structure — page hierarchy, navigation, URL patterns, and internal linking — for a pre-launch product with two primary personas and a single conversion goal.

SITE CONTEXT:
- Company: CoChalet — deeded co-ownership of luxury Laurentian chalets
- Site: cochalet.co (likely Webflow)
- Stage: pre-launch (Founding 8 cohort recruiting)
- Single conversion goal: book a 15-minute discovery call with Justin
- Secondary goal: email capture for nurture sequence
- Current confirmed pages: homepage, property page (/property), how-it-works, /founding-8, /apply

KEY ARCHITECTURAL DIRECTIVES (from TRACTION sessions):
- "See Demo" button must appear BEFORE "Apply" button on homepage
- "Join" → "Apply" everywhere (Martin, TRACTION Apr 7)
- App demo is the #1 conversion asset (TRACTION Apr 9: "Si tu montres ça lundi, ils vont capoter")
- Website must deliver WOW in 1.5 seconds on homepage (Martin's rule)
- No financial numbers on public-facing pages (no $2,634 on attraction pages)
- Each persona needs their own dedicated page

THREE PRIMARY USER JOURNEYS:

Journey 1 — DEEP WORKER (DW):
Entry: LinkedIn post → cochalet.co or /deep-work
Path: /deep-work → property → /apply → Calendly
Intent: "I need a place that's mine, where my desk is where I left it"
Key moment: Thursday Evening narrative on /deep-work page
Exit if not converted: email capture → 7-email nurture sequence

Journey 2 — PROPRIÉTAIRES CURIEUX (PC):
Entry: Facebook/Instagram ad → homepage
Path: homepage → /community or /fondateurs-alpins → /property → /apply → Calendly
Intent: "I've been dreaming of a mountain property for years but can't justify full ownership"
Key moment: Fondateurs Alpins community section (belonging + exclusivity)
Exit if not converted: email capture → FR nurture sequence

Journey 3 — REFERRAL (warm lead from existing Alpine Circle member):
Entry: referral link (personalized) → /founding-8 or /apply directly
Path: /apply → Calendly (short path — already warm)
This journey should skip the awareness/consideration phases entirely

APP DEMO PAGE (new — TRACTION Apr 9 directive):
- Standalone /demo page or embedded section on homepage
- Shows: audience mode switcher, Reserve screen, Concierge tiers
- CTA after demo: "Applique pour te qualifier"
- No Calendly on this page — demo is awareness, not conversion

CURRENT URL STRUCTURE (from app source code):
- / (homepage)
- /property (Mont la Tuque property)
- /how-it-works (ownership mechanism)
- /founding-8 (first cohort)
- /deep-work (DW persona page — exists in source)
- /creative (DW-creative persona page — exists in source)
- /family (PC-family persona page — exists in source)
- /apply (application form)

DELIVERABLE — produce a single markdown document with:

1. FULL SITE MAP
   Complete page hierarchy with:
   - URL slug
   - Page purpose (one sentence)
   - Primary persona served
   - Primary CTA on page
   - Connects to (which pages it links to)
   - Priority: P0 (launch-critical), P1 (month 1), P2 (scale)

2. HOMEPAGE ARCHITECTURE
   Section-by-section breakdown:
   - Section 1: Hero (WOW moment, tagline, primary CTA)
   - Section 2: App demo embed ("See Demo" — before Apply)
   - Section 3: Three persona paths (DW / PC / Fondateur)
   - Section 4: Property showcase (370 Mont la Tuque)
   - Section 5: How it works (3 steps max, no financial detail)
   - Section 6: Community (Alpine Circle / Fondateurs Alpins)
   - Section 7: Justin's story (origin, 66 months, Pioneer 01)
   - Section 8: Apply CTA ("Applique pour te qualifier")
   For each section: headline direction, content summary, CTA if any

3. NAVIGATION STRUCTURE
   Primary nav (max 5 items): what they are and why
   Mobile nav: simplified for DW who arrives via LinkedIn on phone
   Footer nav: secondary pages, legal, Justin's contact
   Internal linking rules: every page must have a path to /apply

4. URL STRUCTURE + SEO RATIONALE
   URL conventions: language (FR vs EN), persona slugs, content slugs
   Target keywords per page:
   - Homepage: "copropriété chalet laurentides," "co-ownership chalet Quebec"
   - /deep-work: "remote work chalet," "chalet travail profond," "mountain office"
   - /property: "370 mont la tuque," "chalet lac superieur"
   - /apply: "rejoindre fondateurs alpins," "apply cochalet"
   Bilingual consideration: single site (EN primary, FR pages or FR-first on specific persona pages?)

5. REDIRECT MAP
   If any current URLs change: what redirects are needed
   Priority: preserve any existing Google indexing on cochalet.co

COMPLIANCE:
- No page should lead with financial figures ($2,634 on homepage is a violation of "never lead with price")
- "timeshare" and "fractional ownership" must not appear anywhere in URL slugs, page titles, or meta descriptions
- /founding-8 page: use "Founding 8" or "Fondateurs Alpins" — never "first 8 investors"
- Every page needs a path to /apply within 2 clicks

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Webflow vs other CMS: architecture recommendations assume Webflow flexibility — may need adjustment
- Bilingual strategy: single site vs. subdomain (cochalet.co/fr/) — SEO implications not yet evaluated
- App demo page: requires dev work (embed or screen recording) — not yet built
- Creative and Family persona pages: exist in app source but marketing copy not yet written
- Current indexing status of cochalet.co: unknown — need Google Search Console data before redirect decisions
- Founding 8 page: may transition to general /apply once first cohort fills
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- Current cochalet.co CMS not confirmed (Webflow assumed based on context)
- Bilingual site structure decision not made — FR primary vs. EN primary with FR versions
- App demo embed requires screen recording or live iOS embed — neither built yet
- Google Search Console not yet set up — no indexing data available
- /founding-8 page lifecycle: when it transitions to /apply is not defined
- Internal linking: current site link structure not audited — existing internal links may contradict new architecture
