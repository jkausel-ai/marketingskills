# seo-audit-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: seo-audit

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/seo-audit
**CoChalet Adaptation:** Audit targets cochalet.co specifically. Site is minimal/early-stage, so focus shifts from fixing existing issues to recommending architecture before build. Quebec bilingual requirements (FR-primary). Category term is "deeded co-ownership" (never "fractional ownership" or "timeshare"). Competitive SEO context includes Casadora (45.5% contested keywords).

### Prompt for Hermes:

```
You are a technical SEO strategist. Perform a comprehensive SEO audit and architecture recommendation for cochalet.co.

CONTEXT:
- Company: CoChalet (cochalet.co)
- Product: Deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel (justin@cochalet.co)
- Current site state: Minimal, early-stage. Not fully built yet.
- Primary language: French (Quebec). Secondary: English.
- Category term: "deeded co-ownership" -- NEVER use "fractional ownership" or "timeshare"
- Target audiences: (1) Deep Workers (DW) -- remote professionals seeking Alpine retreats, (2) Proprietaires Curieux (PC) -- curious homeowners in Quebec
- Primary competitor for SEO: Casadora (45.5% contested keyword overlap)
- Secondary competitors: Pacaso (US-based, 90.8% CoChalet win rate in Canada)

DELIVERABLE -- produce a single markdown document with these sections:

1. TECHNICAL SEO FOUNDATIONS
   - Recommended URL structure for a bilingual FR/EN site (hreflang, subdirectory vs. subdomain)
   - Page speed requirements and hosting recommendations
   - Mobile-first indexing checklist
   - Core Web Vitals targets
   - XML sitemap structure
   - robots.txt recommendations
   - SSL and security headers

2. ON-PAGE SEO ARCHITECTURE
   - Recommended page hierarchy (home, property pages, about, blog, FAQ, contact)
   - Title tag templates for each page type (FR and EN)
   - Meta description templates
   - Header (H1/H2/H3) structure per page type
   - Internal linking strategy
   - Image alt-text conventions (bilingual)

3. KEYWORD STRATEGY
   - Primary keyword clusters for CoChalet (FR and EN)
   - Long-tail opportunities around "copropriete chalet Laurentides" and "co-ownership chalet Quebec"
   - Content gap analysis vs. Casadora
   - Keywords to AVOID (anything suggesting timeshare, fractional ownership, investment returns)
   - Local SEO keywords (Mont-Tremblant, Laurentians, Sainte-Adele, etc.)

4. CONTENT ARCHITECTURE FOR SEO
   - Blog/resource hub structure (topics that attract DW searchers)
   - FAQ schema opportunities
   - Property listing page SEO requirements
   - Pillar page + cluster model recommendation

5. LOCAL SEO
   - Google Business Profile setup for Laurentians service area
   - NAP consistency requirements
   - Local citation strategy (Quebec real estate directories)
   - Review acquisition plan

6. COMPETITIVE SEO POSITIONING
   - How to outrank Casadora on shared keywords
   - Differentiation in SERP (what makes CoChalet snippets click-worthy)
   - Content Casadora publishes that CoChalet should counter

7. PRIORITY ROADMAP
   - Phase 1 (Week 1-2): Must-have technical foundations before site launch
   - Phase 2 (Month 1): Content publishing cadence for SEO traction
   - Phase 3 (Month 2-3): Link building and authority building

QUALITY CHECKS before submitting:
- Zero instances of "timeshare" or "fractional ownership"
- All keyword examples include both FR and EN versions
- No mention of internal financial metrics (NOI, DSCR, take rate, LTV:CAC)
- Recommendations are actionable, not generic SEO advice
- Casadora analysis is factual, not dismissive
```

### Expected Output:
`Hermes/deliverables/seo-audit-cochalet-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) bilingual keyword coverage is real and searchable, (3) recommendations are specific to Quebec real estate market, not generic SEO boilerplate, (4) Casadora competitive analysis is accurate, (5) roadmap is sequenced correctly for a pre-launch site.

---
