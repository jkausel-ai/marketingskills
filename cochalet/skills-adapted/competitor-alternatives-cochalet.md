# competitor-alternatives-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: competitor-alternatives

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/competitor-alternatives
**CoChalet Adaptation:** Casadora is the only real competitive threat (45.5% contested keywords). Pacaso is US-based with 90.8% CoChalet win rate in Canada. Output includes internal battlecard AND public-facing comparison page copy for SEO.

### Prompt for Hermes:

```
You are a competitive positioning strategist. Create a competitive battlecard and comparison page copy for CoChalet.

CONTEXT:
- Company: CoChalet -- deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Competitive intelligence scores:
  - vs. Casadora: 45.5% contested (real threat, Quebec-based, similar model)
  - vs. Pacaso: 90.8% CoChalet win rate (US-based, different market, higher price point)
  - vs. Airbnb/VRBO: not direct competitors (rental vs. ownership) but important comparison for DW audience
  - vs. Traditional cottage purchase: the "do nothing" competitor (buy a $500K+ cottage alone)
- CoChalet differentiators:
  - Deeded ownership (you own a real share of a real property, registered with the land registry)
  - Quebec-specific (Laurentians, local expertise, Quebec legal framework)
  - Fondateurs Alpins community (belonging, not just a transaction)
  - Justin as founder (personal, accessible, not a faceless corporation)
  - Monthly cost: $2,634/month (can mention in comparison context, not as a lead)
- Category: "deeded co-ownership" only
- Casadora positioning: similar model, Quebec-focused, likely targeting same audience
- Current Casadora persona health score: 5.4/10 (CoChalet) vs. Casadora (needs improvement)

DELIVERABLE -- produce a single markdown document with TWO sections:

### SECTION A: INTERNAL BATTLECARD (not for public use)

1. CASADORA BATTLECARD
   - What they offer (factual, not dismissive)
   - Where they win vs. CoChalet (honest assessment)
   - Where CoChalet wins vs. Casadora
   - Common objections when prospect is comparing: "Why CoChalet over Casadora?"
   - Talk tracks for Justin on discovery calls
   - Red flags that a prospect has been talking to Casadora
   - How to respond when asked directly about Casadora

2. PACASO BATTLECARD
   - What they offer (US-focused, higher price point)
   - Why they are not a real threat in Quebec
   - How to position when asked: "Isn't this like Pacaso?"
   - Talk track: "Pacaso is great for US luxury. CoChalet is built for Quebec."

3. "DO NOTHING" BATTLECARD
   - Why prospects stay with Airbnb/VRBO (familiar, no commitment)
   - Why prospects consider buying alone (full ownership appeal)
   - How to reframe: "What did you spend on rentals last year? What do you own from it?"
   - Justin's origin story as proof point (lost $120K on Airbnb with zero ownership)

### SECTION B: PUBLIC COMPARISON PAGE COPY (for cochalet.co/compare)

1. CoChalet vs. Renting (Airbnb/VRBO)
   - Headline (FR and EN)
   - Comparison table (3-4 rows: ownership, equity, maintenance, flexibility)
   - Key paragraph for SEO
   - CTA: "Stop renting. Start owning."

2. CoChalet vs. Buying Alone
   - Headline (FR and EN)
   - Comparison table (cost, maintenance, usage, community)
   - Key paragraph for SEO
   - CTA: "All the joy. A fraction of the burden."

3. CoChalet vs. Casadora
   - Headline (FR and EN) -- respectful, not attack-mode
   - Comparison table (factual, cite-able differences only)
   - Key paragraph for SEO (target: "Casadora alternatives" keyword)
   - CTA: "See how CoChalet compares."
   - IMPORTANT: this page must be factual, fair, and not disparaging

4. CoChalet vs. Pacaso
   - Headline (FR and EN)
   - Why CoChalet is the Quebec choice
   - CTA: "Built for Quebec. Built for you."

QUALITY CHECKS:
- Internal battlecard is honest and balanced (acknowledges where competitors win)
- Public comparison pages are factual, not attack-oriented
- No mention of "timeshare" or "fractional ownership" anywhere
- Casadora comparison is respectful -- no FUD, no dismissiveness
- All public copy includes both FR and EN
- Price appears only in comparison tables, not as a leading element
- No internal metrics (take rate, DSCR, NOI) in any section
```

### Expected Output:
`Hermes/deliverables/competitor-alternatives-battlecard-GPTOSS.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) Casadora comparison is factual and respectful, (3) internal battlecard is honest (does not pretend CoChalet wins everywhere), (4) public comparison pages are SEO-optimized, (5) talk tracks are natural for Justin's voice, (6) "do nothing" competitor is addressed.

---
