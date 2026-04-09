# cold-email-cochalet

Split from `WAVE2_SKILL_PROMPTS_2026-04-08.md` into a standalone Hermes-ready prompt for the CoChalet tracker scaffold.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: cold-email

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/cold-email
**CoChalet Adaptation:** DW outreach from Justin personally. Montreal/Laurentians geo-targeted. No corporate voice -- Justin writes like a founder who lost $120K on Airbnb and built something better. 3-email sequence. No price in cold outreach. CTA is always discovery call.

### Prompt for Hermes:

```
You are writing cold outreach emails for Justin Kausel, founder of CoChalet. These emails must sound like Justin wrote them personally -- warm, direct, founder-to-peer, not corporate or salesy.

CONTEXT:
- Sender: Justin Kausel (justin@cochalet.co, founder of CoChalet)
- Product: Deeded co-ownership of luxury chalets in the Laurentians, Quebec
- Justin's origin story: Lost $120K over 3 years renting on Airbnb with zero ownership to show for it. Built CoChalet so professionals can own a piece of the Laurentians without the full cost or the maintenance headache.
- Target recipient: Deep Workers -- remote professionals, 30-45, Montreal-based or Laurentians-adjacent, earning $120K+, who rent cottages or chalets seasonally
- CTA: Book a 15-minute discovery call with Justin (never "buy now", never "invest", never "learn about our investment opportunity")
- Geo-targeting: Montreal, Laval, South Shore, Laurentians
- Language: Write in English. (FR versions will be created separately via translation skill.)
- Tone: peer-to-peer founder voice. Short sentences. Personal. No corporate jargon.
- Martin's directive: "Montrer le reve. Pas expliquer la formule." -- Show the dream, not the formula.

FOUR NEVERS:
1. NEVER say "timeshare" or "fractional ownership"
2. NEVER mention price or financial details in cold outreach
3. NEVER expose internal metrics
4. NEVER use financial jargon

DELIVERABLE -- produce a single markdown document with:

### EMAIL SEQUENCE: Deep Worker Cold Outreach (3 emails)

**Email 1: The Hook (Day 0)**
- Subject line (3 options, A/B testable)
- Preview text
- Body (under 120 words)
- CTA
- Sending context: When to send, what triggers this email (LinkedIn connection accepted, event attendee list, referral)
- P.S. line (optional, personal touch)

**Email 2: The Story (Day 3)**
- Subject line (3 options)
- Preview text
- Body (under 150 words) -- Justin's $120K Airbnb story, briefly
- CTA
- Sending context: Only if Email 1 was opened but not replied

**Email 3: The Nudge (Day 7)**
- Subject line (3 options)
- Preview text
- Body (under 100 words) -- short, casual, last touch
- CTA
- Sending context: Only if Email 2 was opened but not replied

### SEQUENCE RULES
- If no open on Email 1 -> stop sequence (do not spam)
- If reply at any point -> exit sequence, respond personally
- Cool-down: 90 days before re-entering sequence
- Opt-out: every email must include easy unsubscribe

### PERSONALIZATION TOKENS
- {first_name} -- recipient first name
- {company} -- recipient company (if known)
- {connection_point} -- how Justin knows them (LinkedIn, event, referral from {referrer_name})
- {neighborhood} -- Montreal neighborhood or Laurentian town

### COMPLIANCE NOTES
- CASL compliance requirements for Canadian cold email
- Required sender identification and unsubscribe mechanism
- What constitutes "implied consent" in Quebec

QUALITY CHECKS:
- Every email sounds like Justin, not a marketing team
- No email mentions price, returns, or financial specifics
- CTA is always a low-pressure discovery call
- Subject lines are personal, not clickbait
- Total sequence is 3 emails max -- no "drip campaign" of 12 emails
```

### Expected Output:
`Hermes/deliverables/cold-email-dw-sequence-GPTOSS.md`

### Quality Gate:
COS Opus verifies: (1) Four Nevers compliance, (2) Justin's voice is authentic (founder-peer, not corporate), (3) CASL compliance is addressed, (4) no email exceeds word count limits, (5) CTA is consistently discovery call, (6) sequence logic is respectful (stops on no open), (7) subject lines are A/B testable.

---
