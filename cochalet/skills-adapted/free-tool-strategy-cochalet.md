# free-tool-strategy-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output recommends SaaS-style free tools (calculators, templates, browser extensions). CoChalet already has the highest-intent free tool concept built into the website: the ownership cost calculator. The strategy should expand from there — tools that demonstrate the $101K Buyer Tax insight, the 37-night schedule visualizer, and the concierge tier configurator. Each tool serves dual purpose: lead capture + product education.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: free-tool-strategy

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/free-tool-strategy
**CoChalet Adaptation:** 3 high-value free tools already conceptually available: (1) Ownership Cost Calculator (already referenced in website source), (2) Mountain Rhythm Planner (37-night schedule visualizer), (3) Concierge Tier Configurator (Essentiel → Noir cost builder). Each tool captures email, builds understanding, and makes the discovery call feel obvious.

### Prompt for Hermes:

```
You are a product-led growth strategist for a high-consideration real estate startup. Design CoChalet's free tool suite — interactive tools that educate prospects, demonstrate value, and generate qualified leads.

FREE TOOL PHILOSOPHY FOR COCHALET:
- Tools must be genuinely useful even if the person never becomes a co-owner
- Each tool teaches one insight that generic real estate search doesn't provide
- The insight must be specific to the deeded co-ownership model — not available anywhere else
- Tool output should make the discovery call feel like the obvious next step
- Lead capture: email gate AFTER the tool delivers value (not before)

CONTEXT:
- Company: CoChalet — deeded co-ownership of luxury Laurentian chalets
- Stage: pre-launch (no existing tool traffic — designing from zero)
- Existing website mention: "Calculate Your Stake" CTA links to a calculator
- App has: ModelComparison component with live financial model (Ensemble + Sanctuaire numbers)
- Key insight tools can demonstrate: $101K Buyer Tax, 37-night schedule, concierge tier economics
- Persona: DW (analytical, needs to "see the math") and PC (emotional, needs to "see the life")

THREE CORE TOOL CONCEPTS:

TOOL 1: MOUNTAIN COST CALCULATOR ("Calcule ta part" / "Calculate Your Share")
- Core insight: CoChalet costs ~$28K/year all-in vs. $65K+ for solo ownership (Year 1)
- What it shows: user inputs their "dream chalet" parameters, sees the cost comparison
- Inputs: region (Laurentians), size (2BR/3BR/4BR), usage frequency (nights/year), owned vs. co-owned
- Output: side-by-side cost breakdown (solo ownership vs. CoChalet). Never shows DSCR/NOI.
- Lead gate: "See your personalized breakdown" → email capture → full results delivered
- GATED numbers NOT to show publicly: $112,300 FO stake, DSCR 1.95x, NOI margins
- PUBLIC numbers safe to use: $2,634/month all-in, 37 nights/year, $71/effective night, $28K/year baseline

TOOL 2: MOUNTAIN RHYTHM PLANNER ("Planifie ton rythme" / "Plan Your Mountain Rhythm")
- Core insight: 37 owner nights/year is more than most people think — and it's structured freedom
- What it shows: an interactive calendar showing 37 nights distributed across 4 seasons
- Inputs: work schedule type (standard 9-5, flexible, fully remote), preferred seasons (ski, fall, summer)
- Output: a personalized 37-night annual schedule showing when their mountain would be available
- Secondary output: comparison — "vs. what you'd actually use a solo-owned property"
- Lead gate: "Save your rhythm calendar" → email capture → PDF/iCal export
- Emotional goal: make 37 nights feel like abundance, not scarcity

TOOL 3: CONCIERGE TIER CONFIGURATOR ("Crée ton séjour" / "Build Your Stay")
- Core insight: the service tier system means every stay can be exactly what you need
- What it shows: interactive tier builder (Essentiel → Confort → Confort XL → Noir)
- Inputs: stay type (deep work sprint, family weekend, couple retreat, solo recovery), length (2-7 nights)
- Output: itemized stay package (services included, estimated cost range, what's staged on arrival)
- Lead gate: "Get your personalized stay guide" → email capture → PDF delivered
- COMPLIANCE NOTE: Tier pricing (Confort: $360, XL: $720, Noir: $1,450) are GATED — show ranges only publicly

DELIVERABLE — produce a single markdown document with:

1. TOOL PRIORITIZATION + BUILD ORDER
   Which tool to build first and why. Consider: development complexity, lead quality signal, persona fit.
   For each tool: complexity estimate (1=simple, 5=complex), lead quality score, persona primary

2. DETAILED SPEC FOR TOOL 1 (Calculator — highest priority)
   - User flow: step by step (inputs → processing → results → gate → delivery)
   - Input field design (labels, options, default values)
   - Calculation logic (what formula runs — using only PUBLIC numbers)
   - Results display design (side-by-side, chart, or breakdown table)
   - Email gate placement and copy ("Your breakdown is ready — where should we send it?")
   - Confirmation email content (the results + 1 paragraph Justin voice follow-up)
   - Follow-up sequence: how this tool feeds into the 7-email nurture sequence

3. DISTRIBUTION STRATEGY FOR EACH TOOL
   How to promote each tool:
   - LinkedIn post format for tool launch (Justin voice, 150 words)
   - Facebook ad format (PC persona, lifestyle frame, not financial)
   - SEO angle: what search query does each tool intercept?
   - Embedding: which page(s) each tool lives on

4. LEAD SCORING FROM TOOL USAGE
   Define intent signals from tool behavior:
   - Calculator completed → intent score +3
   - Calculator result shared → intent score +5
   - Rhythm Planner completed → intent score +4
   - Concierge Configurator completed → intent score +3
   - Two tools completed → auto-trigger Calendly invitation email

5. SUCCESS METRICS
   Per tool: monthly unique completions target, email capture rate target, call booking conversion from tool users
   Benchmark: calculator users book discovery calls at 2-3x the rate of non-calculator visitors (hypothesis)

COMPLIANCE:
- GATED numbers (FO Stake: $112,300, DSCR: 1.95x, NOI margin: 37.9%) must NEVER appear in tool output
- PUBLIC numbers safe: $2,634/month, 37 nights, $71/night, $28K/year baseline
- Tool results must include disclaimer: "Based on current CoChalet model A parameters. Subject to change."
- Never imply investment returns from any tool output

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Development resources: no in-house dev — tools need to be built in Webflow, Typeform, or no-code
- Calculator accuracy: $28K/year vs. $65K+ benchmarks need real comp data validation
- Rhythm Planner: 37-night assumption is Model A only — Tool needs to handle Model B (67 nights) variant
- Concierge tier pricing: publicly showing ranges vs. exact numbers — legal/positioning decision pending
- Tool hosting: embedded in website vs. standalone microsites (SEO implications)
- Lead scoring integration: no CRM confirmed yet — scoring system needs a platform to live in
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- No development resources confirmed for tool build — no-code solution required at launch
- Calculator formula using public numbers only — $65K+ solo ownership benchmark needs comp validation
- Rhythm Planner is a new concept — no comparable tool exists to benchmark completion rates
- Concierge pricing display (ranges vs. exact): positioning vs. legal decision not yet made by Justin
- Lead scoring system requires CRM platform — not yet selected
- Tool distribution: LinkedIn + Facebook organic assumed — paid promotion budget not allocated
- Tool 2 (Rhythm Planner) and Tool 3 (Configurator) are Phase 2 — Tool 1 (Calculator) is launch priority
