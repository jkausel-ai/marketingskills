# schema-markup-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output implements SaaS schema types (SoftwareApplication, Organization, FAQPage). CoChalet needs real estate-specific schema (RealEstateListing, LocalBusiness, FAQPage for common objections, Person for Justin) plus AI search optimization schema for Quebec-specific queries. Critical: schema must never expose GATED financial data in structured markup.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)
5. NEVER name forbidden terms even to contrast them. Do not write 'unlike timeshare' or 'not fractional ownership'. Instead use: 'unlike usage-rights products', 'unlike shared vacation clubs', 'unlike partial-access arrangements'.

---

## Skill: schema-markup

**Model:** qwen-3.6-plus
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/schema-markup
**CoChalet Adaptation:** Five schema types needed: Organization (CoChalet Inc.), Person (Justin Kausel), RealEstateListing (370 Mont la Tuque), FAQPage (common objections answered without exposing gated data), and LocalBusiness (Laurentides location). All schema must use PUBLIC facts only — never gated financial metrics in structured data.

### Prompt for Hermes:

```
You are a structured data specialist for a real estate company. Implement schema markup for CoChalet that helps search engines understand the product, builds rich results, and optimizes for AI search (ChatGPT, Perplexity, Google AI Overviews).

COMPANY CONTEXT:
- CoChalet Inc. / EquiVest Properties
- Quebec, Canada
- Website: cochalet.co
- Founder: Justin Kausel (justin@cochalet.co, 514.585.3255)
- Product: deeded co-ownership (copropriété indivise) of luxury chalets
- Property: 370 Chemin du Mont la Tuque, Lac-Supérieur, QC
- Region: Laurentides, Quebec, Canada
- Tagline: "Use It. Own It. Love It."

SCHEMA PRIORITY (P0 = launch-critical):

P0 — Organization schema:
- CoChalet Inc. / EquiVest Properties
- Type: RealEstateAgent + Organization (dual type)
- URL, logo, contact, sameAs (LinkedIn, Instagram, Facebook)
- Area served: Laurentides, Quebec

P0 — Person schema (Justin Kausel):
- Founder + CEO
- jobTitle: "Founder & CEO, CoChalet"
- sameAs: Justin's LinkedIn URL
- Do NOT include: cannabis background, previous companies (LinkedIn scrubbed per Martin's directive)
- DO include: 66-month build, Pioneer 01 status (in description field only)

P0 — FAQPage schema (homepage + /how-it-works):
10 FAQ entries answering the most common objections.
CRITICAL: answers must use PUBLIC language only. Never expose DSCR, NOI, $112,300 stake amount.
Questions to cover:
1. "C'est quoi la différence avec un timeshare?" → Answer using "deeded co-ownership" language
2. "Est-ce que je reçois des revenus de location?" → Answer: non, the STR model funds property operations
3. "Comment fonctionne la propriété légale?" → Quebec notary, deed registered at land registry
4. "Combien ça coûte par mois?" → $2,634 all-in (PUBLIC number, safe to use in schema)
5. "C'est quoi le Fondateurs Alpins?" → 800-cap community of co-owners and prospective owners
6. "Combien de nuits par année?" → 37 nights/year (Model A, Ensemble)
7. "Qui gère la propriété?" → CoChalet Hospitality — professional management, owner never deals with maintenance
8. "Est-ce que je peux revendre ma part?" → Yes, via standard Quebec notarial process
9. "C'est quoi l'application?" → iOS app for booking, concierge, community — owner experience
10. "Comment est-ce que je m'applique?" → Apply at cochalet.co/apply — applications reviewed individually

P1 — RealEstateListing schema (/property page):
- Name: "370 Chemin du Mont la Tuque — CoChalet Ensemble"
- Address: 370 Chemin du Mont la Tuque, Lac-Supérieur, QC J0T 1J0
- Geo: approximate coordinates for Lac-Supérieur area (do not expose exact GPS)
- numberOfRooms: 4 (bedrooms), 3.5 (bathrooms)
- floorSize: 3200 sq ft
- amenityFeature: sauna, hot tub, standing desk, fiber internet, concierge service
- Do NOT include: purchase price, FO stake amount ($112,300), any financial metrics

P1 — LocalBusiness schema:
- Type: LodgingBusiness + RealEstateAgent (dual)
- Region: Laurentides, Quebec
- priceRange: "$$$" (do not expose specific pricing in schema)
- servesCuisine: N/A (replace with amenityFeature or knowsAbout)

P2 — BreadcrumbList (all pages)
P2 — VideoObject (if app demo screen recording is published)
P2 — Event (for Alpine Circle in-person events when they happen)

AI SEARCH OPTIMIZATION (beyond standard schema):
- speakable schema: mark the key value propositions for voice search
- FAQ answers must be conversational — written for "what is CoChalet" type queries in ChatGPT/Perplexity
- mentions schema: link to Quebec real estate regulatory context (AMF)
- knowsAbout: deeded co-ownership, copropriété indivise, Laurentian real estate

DELIVERABLE — produce a single markdown document with:

For each schema type:
- Complete JSON-LD code block (ready to paste into <head>)
- Page it belongs on
- Rich result it enables (if any)
- Validation note (use schema.org validator)
- Any fields that MUST NOT contain gated data (flag explicitly)

Include a validation checklist at the end:
- [ ] No DSCR, NOI, or internal financial metrics in any schema
- [ ] No "timeshare" or "fractional ownership" in any schema property
- [ ] All @type values are valid schema.org types
- [ ] FAQPage answers use only PUBLIC-safe language
- [ ] RealEstateListing price fields either omitted or use PUBLIC $2,634/month

COMPLIANCE:
- NEVER put $112,300, DSCR, NOI, take rate, or any GATED metric in schema markup
- Schema is indexed by Google and read by AI systems — gated data in schema = public data
- "timeshare" must not appear in any schema property value
- FAQPage: question 1 explicitly addresses "is this a timeshare?" — answer must be clear without being defensive

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Exact GPS coordinates for property: approximate used — real coordinates not included for privacy
- Justin's LinkedIn URL: not confirmed in source material — needed for Person schema sameAs
- Social media URLs: Instagram/Facebook/LinkedIn for CoChalet — needed for Organization sameAs
- Logo URL: confirm final logo file is hosted on cochalet.co before adding to schema
- RealEstateListing: property listing schema may need real estate agent license number (AMF registration)
- VideoObject: requires published app demo video URL — not yet available
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- Property GPS coordinates: using approximate Lac-Supérieur area — exact not included
- Justin's social media URLs: not confirmed in CANON_FACTS_LOCKED.json
- CoChalet brand social URLs: needed for Organization schema sameAs
- Real estate agent registration: Quebec AMF status for schema compliance unknown
- App demo video: VideoObject schema ready to add when demo recording is published
- FAQ answers: written with PUBLIC language only — legal review recommended before publishing FAQPage schema
