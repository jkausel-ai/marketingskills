# sales-enablement-cochalet

DBA verdict: ADAPT (2026-04-10). Generic output builds multi-rep B2B sales decks, objection playbooks, and CRM sequences. CoChalet has exactly one closer: Justin Kausel. His 15-minute discovery call is the entire sales motion. Sales enablement means making Justin's 15 minutes more effective — not building a sales team infrastructure that doesn't exist.

## Canon Context Block (prepended to every prompt via HERMES_KNOWLEDGE_BASE.md)

For reference, every Hermes execution prepends ~800 tokens of Canon context. The prompts below are written to be **standalone** -- they include all necessary context so Hermes can execute without reading additional files.

**Four Nevers (enforced on all output):**
1. Never use "timeshare" or "fractional ownership"
2. Never lead with price
3. Never expose the Engine Room (internal ops, margins, take rate)
4. Never use jargon (DSCR, NOI, LTV:CAC in public-facing output)

---

## Skill: sales-enablement

**Model:** gpt-oss-120b
**Status:** STAGING -> ready for GATE CHECK
**Original:** coreyhaines31/marketingskills/sales-enablement
**CoChalet Adaptation:** Justin is the only closer. 7 hrs/week total on CoChalet. Discovery call is 15 minutes, casual, tutoiement in French. "Let me show you how this works and you decide" — never a pitch. Sales enablement = the app demo script, the objection one-liners, the follow-up sequence after the call, and the materials Justin sends to warm leads. No sales team. No multi-touch CRM sequences. Everything supports one human having better conversations.

### Prompt for Hermes:

```
You are a sales strategist for a founder-led luxury real estate startup. Build the sales enablement toolkit for Justin Kausel — the sole closer. Everything you produce must be executable by one person with 7 hours per week.

CRITICAL CONTEXT — SINGLE-CLOSER REALITY:
- Justin is the ONLY person who closes deals at CoChalet
- No sales team, no SDRs, no BDRs, no account executives
- Justin's style: "Let me show you how this works, and you decide." — NEVER pressure
- Discovery call format: 15 minutes, casual, conversational, tutoiement in French
- Justin's weekly hours on CoChalet: 7 hours total (including admin, content, calls)
- This means: max 3 calls/week. Every call must be qualified. Every tool must save Justin time.

THE SALES MOTION (real stages):
1. Warm lead arrives (referral, inbound from content, post-application)
2. Justin reviews application (1-2 min) — is this person right?
3. 15-minute discovery call booked
4. Call happens: app demo + "you ask, I answer" format
5. Verbal interest → follow-up email with one document
6. Due diligence period (30-60 days)
7. Commitment → notary process (~30 days)
8. Active FO

CALL INTELLIGENCE (from TRACTION sessions):
- The app is the #1 close accelerator (Stephane: "Tesla analogy")
- Lead with app demo, not deck (TRACTION Apr 9 unanimous)
- Lynn: "L'application du bonheur" — use this framing in post-call follow-up
- Martin (Apr 9): "Tu as 75% du travail fait. La, on va chercher le maximum des vrais humains."

GATED DATA (available to Justin in discovery calls — never in written materials sent to prospects):
- FO Stake: $112,300 (can verbally discuss in call — never in email/doc)
- DSCR: 1.95x (can share in due diligence packet — never in attraction materials)
- NOI margin: 37.9% (investor-grade doc only)
- V31_14 model debate: INTERNAL — do not share with prospects

PUBLIC DATA (safe in all materials):
- $2,634/month all-in (anchor lifestyle first, then this as "the number")
- 37 nights/year, $71 effective nightly cost
- "deeded co-ownership" — always use this, never "fractional"

DELIVERABLE — produce a single markdown document with:

1. DISCOVERY CALL SCRIPT (the 15-minute flow)
   Not a word-for-word script — a flow guide with key moments:
   - Opening (2 min): warm connection, confirm 15 minutes, one question: "What brought you here?"
   - App demo (5 min): mode switcher → Reserve → Concierge (the three power moves)
   - Their questions (5 min): Justin answers, never volunteers financial depth unprompted
   - Close (3 min): next steps, never pressure
   For each segment: what Justin says, what he listens for, what he never says
   Key phrase: "C'est une conversation, pas un pitch. Tu poses les questions, je réponds."

2. OBJECTION ONE-LINERS (10 most common objections)
   Format: Objection → One-sentence response (conversational, never defensive)
   Required objections to cover:
   - "C'est comme un timeshare?" → Clear, warm, factual distinction
   - "Et si je veux revendre?" → Quebec notarial process, standard real estate
   - "Est-ce que je reçois des revenus de location?" → No — and why that's better (stability, simplicity)
   - "C'est quoi le vrai coût par mois?" → $2,634 all-in, here's what that covers
   - "J'ai besoin d'y penser." → "Bien sûr. Qu'est-ce qui t'aidera à décider?"
   - "Comment je sais que CoChalet va durer?" → Justin's 66-month build, Desjardins backing, Pioneer 01
   - "Et si j'ai envie d'y aller plus que 37 nuits?" → Model B option + availability explanation
   - "C'est quoi la différence avec Casadora?" → Model comparison (factual, no attacks)
   - "Est-ce que d'autres personnes utilisent le même chalet?" → Yes, and here's how the schedule works
   - "Pourquoi le cap de 800?" → It's a real community constraint, not marketing

3. POST-CALL FOLLOW-UP SEQUENCE (3 emails)
   Email 1 (within 2 hours of call): warm summary, one link (app store or cochalet.co), no pressure
   Email 2 (Day 3 if no response): one question, no content dump
   Email 3 (Day 10 if still no response): final check-in, genuine, Justin voice ("si c'est pas le bon moment, c'est correct aussi")
   For each: subject line (FR + EN), full body copy, Justin's voice throughout

4. DUE DILIGENCE PACKET (what Justin sends after verbal interest)
   One document. Not a deck — a reference doc.
   Sections: What you own (legal structure, plain language), The property (address, specs, photos), The app (screenshots, feature list), The community (Alpine Circle, Fondateurs Alpins), Next steps (notary process, timeline)
   What it NEVER includes: DSCR, NOI, take rate, V31_14 debate, financial model internals

5. JUSTIN'S PERSONAL BRAND ASSET LIST
   The 5 things Justin should have ready before every call:
   - Phone charged with app logged in (Pioneer 01 account)
   - One recent LinkedIn post to reference ("you might have seen this...")
   - Founding 8 availability status (how many spots remain)
   - The Thursday Evening story (rehearsed, 60 seconds)
   - One question about the prospect (read their application before calling)

COMPLIANCE:
- Discovery call script: never say "investment," "returns," "ROI" — use "builds equity" only
- Objection responses: never say "timeshare" even when addressing the objection — say "it's not that"
- Post-call emails: never attach financial model or any GATED document
- Due diligence packet: clearly labeled "CONFIDENTIEL" on any page with financial specifics
- Justin's voice throughout: warm, specific, never polished-marketer

## TUNING GAPS
End your output with a ## TUNING GAPS section covering:
- Justin has not reviewed or validated the call script — all dialogue is approximated from transcripts
- Objection frequency: which objections come up most is unknown (no call data yet)
- Due diligence packet: what legal documentation Justin is permitted to share pre-AMF guidance
- Post-call email show rate: no data on whether Day 3 or Day 10 follow-ups are optimal
- Casadora comparison: factual model differences researched but not confirmed with Casadora directly
- Call capacity: 3 calls/week is estimated — Justin's actual availability calendar not set up
```

## TUNING GAPS (from skill creation — pre-execution baseline)
- No discovery call transcripts to validate script against real Justin conversations
- Objection one-liners: written from customer research hypotheses — not validated with real call data
- Post-call email sequence: cadence (2 hrs, day 3, day 10) is best-practice estimate for high-consideration real estate
- Due diligence packet: legal review needed before finalizing what can be shared at this stage
- Justin's app demo flow: 5-move script written from app source code analysis — needs Justin's real demo style
- 3 calls/week capacity assumption: based on 7 hrs/week total — may be optimistic depending on call prep/follow-up time
