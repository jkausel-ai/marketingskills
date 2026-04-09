# page-cro-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: page-cro

**Model:** sonnet-hermes
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/page-cro
**CoChalet Adaptation:** Conversion path is awareness -> discovery call booking (not e-commerce checkout). DW audience is skeptical, analytical, and privacy-conscious. Page must work in FR and EN. No price leading. The emotional journey is: curiosity -> understanding -> relief -> desire -> action.

### Prompt for Hermes:

```
You are a conversion rate optimization specialist for high-consideration real estate products. Design the optimal landing page experience for cochalet.co targeting Deep Workers.

CONTEXT:
- Company: CoChalet (cochalet.co)
- Product: Deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Founder: Justin Kausel
- Conversion goal: Visitor -> Discovery Call booking (15-minute call with Justin)
- Target audience: Deep Workers (DW) -- remote professionals, 30-45, Montreal-based, earning $120K+, who want an Alpine retreat but cannot justify full cottage ownership
- DW Pain (CUT framework):
  - Context Switching: juggling city life with escape needs
  - Unproductive: weekends spent on cottage maintenance instead of rest
  - Time-Consuming: searching for rentals, managing logistics every trip
- Emotional resolution: "Arrivez et vivez." (Arrive and live.) -- no logistics, no maintenance, just deep work and deep play
- Slogan EN: "Deep Work. Deep Play. Your Deed."
- Brand archetype: Explorateur (adventure, discovery) + Soignant (care, trust, belonging)
- Tone: warm, factual, zero superlatives, tutoiement in French
- Price mention: NEVER lead with price. Price appears only after value is established, deep in the page or on a separate pricing page.
- Category: "deeded co-ownership" ONLY. Never "timeshare" or "fractional ownership."
- Competitive: Casadora is the only real competitor (45.5% contested). Pacaso is US-based (90.8% CoChalet win rate).

DELIVERABLE -- produce a single markdown document with:

1. LANDING PAGE WIREFRAME (text-based, section by section)
   For each section, specify:
   - Section name and purpose
   - Headline (FR and EN)
   - Subheadline (FR and EN)
   - Body copy direction (not full copy -- that is the copywriting skill's job)
   - CTA button text (FR and EN)
   - Visual direction (what image/video belongs here)
   - Estimated viewport height (above fold, 1 scroll, 2 scrolls, etc.)

   Recommended sections (adapt as needed):
   a. Hero -- emotional hook, "Arrivez et vivez."
   b. Pain agitation -- the CUT framework made visual
   c. Solution reveal -- what deeded co-ownership actually means
   d. How it works -- 3-step process (simple, visual)
   e. The properties -- lifestyle imagery, not floor plans
   f. Social proof -- Fondateurs Alpins community, testimonials
   g. FAQ -- top 5 objections answered
   h. CTA -- discovery call booking with Justin

2. CONVERSION PATH ANALYSIS
   - Primary path: Homepage -> Hero CTA -> Discovery Call booking
   - Secondary path: Homepage -> How It Works -> FAQ -> Discovery Call
   - Tertiary path: Blog/SEO -> Landing page -> Discovery Call
   - Exit intent strategy (what happens when they leave without converting)
   - Mobile vs. desktop conversion considerations

3. TRUST SIGNALS
   - What trust elements to include (not testimonials yet -- CoChalet is pre-launch)
   - Founder story as trust element (Justin's $120K Airbnb loss origin story)
   - Legal/deeded ownership proof elements
   - Community (Fondateurs Alpins) as social proof

4. CRO METRICS AND TARGETS
   - Benchmark conversion rates for high-consideration real estate landing pages
   - Target metrics: time on page, scroll depth, CTA click rate, discovery call booking rate
   - Heatmap and session recording tool recommendations

5. A/B TEST ROADMAP
   - First 5 experiments to run after page launch
   - Variables: headline, CTA text, hero image, social proof placement, price mention depth
   - Sample size requirements

QUALITY CHECKS:
- Price never appears above the fold or in the hero section
- Zero instances of "timeshare" or "fractional ownership"
- CTA is always "discovery call" or "appel decouverte" -- never "buy now" or "invest"
- Emotional journey follows: curiosity -> understanding -> relief -> desire -> action
- All copy directions include both FR and EN
- No superlatives ("best", "premier", "ultimate", "#1")
```

### Expected Output:
`Hermes/deliverables/page-cro-cochalet-landing-SONNET.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) price placement is appropriate (deep, not leading), (3) emotional arc is correct (not hard-sell), (4) wireframe sections are complete and logical, (5) CTA language matches brand tone (warm, invitational, not pushy), (6) mobile path is addressed.

---
