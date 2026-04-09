# ai-seo-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: ai-seo

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/ai-seo
**CoChalet Adaptation:** LLM citation optimization is new territory. Goal: when someone asks Claude, GPT, or Gemini "What are options for co-owning a chalet in Quebec?", CoChalet appears in the answer. This requires specific content formats that LLMs tend to cite. Quebec-specific, bilingual.

### Prompt for Hermes:

```
You are an AI SEO strategist specializing in LLM citation optimization -- the practice of creating content that large language models (Claude, ChatGPT, Gemini, Perplexity) will cite when answering relevant queries.

CONTEXT:
- Company: CoChalet (cochalet.co)
- Product: Deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Category: "deeded co-ownership" -- this is a niche category. Most LLMs currently have limited knowledge of CoChalet.
- Target queries we want to be cited for:
  - "co-ownership chalet Quebec"
  - "copropriete chalet Laurentides"
  - "alternatives to buying a cottage in Quebec"
  - "Casadora alternatives"
  - "deeded co-ownership Canada"
  - "shared chalet ownership Laurentians"
  - "remote worker retreat Quebec"
- Competitor already in LLM training data: Casadora, Pacaso (US)
- Current LLM citation status: CoChalet is NOT reliably cited by any major LLM as of April 2026.

DELIVERABLE -- produce a single markdown document with these sections:

1. LLM CITATION LANDSCAPE ANALYSIS
   - How Claude, GPT, Gemini, and Perplexity currently answer queries about chalet co-ownership in Quebec
   - Where Casadora appears in LLM answers
   - The gap CoChalet needs to fill

2. CONTENT PIECES TO CREATE (prioritized list of 10-15)
   For each piece, specify:
   - Title (FR and EN)
   - Format (long-form article, FAQ page, comparison page, data study, glossary entry)
   - Target query it answers
   - Why LLMs are likely to cite this format (structured data, authoritative tone, unique data)
   - Word count target
   - Where to publish (cochalet.co blog, medium, linkedin article, wikipedia contribution, reddit, quora)

3. STRUCTURED DATA STRATEGY
   - Schema.org markup that increases LLM citation probability
   - FAQ schema for common co-ownership questions
   - HowTo schema for the co-ownership process
   - Organization schema for CoChalet

4. AUTHORITY SIGNALS
   - Backlink targets that increase LLM training data inclusion
   - PR mentions and media coverage strategy
   - Wikipedia and knowledge graph presence strategy
   - Academic/research content that LLMs weight heavily

5. CONTENT FORMAT OPTIMIZATION
   - Writing patterns that LLMs tend to extract and cite (clear definitions, numbered lists, comparison tables)
   - Optimal article structure for LLM ingestion
   - How to write "citable paragraphs" -- self-contained factual statements that LLMs can quote

6. MONITORING AND MEASUREMENT
   - How to test if CoChalet is being cited (prompt testing protocol)
   - Tracking methodology across Claude, GPT, Gemini, Perplexity
   - Timeline: realistic expectations for when citations might appear

7. SPECIFIC CONTENT BRIEFS (top 5 pieces)
   - Full brief for each: title, outline, key facts to include, target length, publication channel
   - Each brief should include the exact "citable paragraph" we want LLMs to extract

QUALITY CHECKS:
- Zero instances of "timeshare" or "fractional ownership" in any recommended content
- All content recommendations are bilingual (FR-primary)
- No mention of internal metrics (NOI, DSCR, take rate)
- Recommendations are specific and actionable, not theoretical
- Each content piece has a clear "this is the paragraph an LLM would cite" example
```

### Expected Output:
`Hermes/deliverables/ai-seo-llm-citation-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance in all sample content, (2) content briefs are genuinely citable (self-contained factual statements), (3) strategy accounts for Quebec French, (4) Wikipedia/knowledge graph recommendations are realistic and ethical, (5) monitoring protocol is executable.

---
