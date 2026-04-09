# Hermes Self-Routing Instructions
# Read this + skill-router.json at the start of every task.

## How to Route

When you receive a task:

1. **Read `skill-router.json`** — it maps 34 marketing skills to optimal models
2. **Match the task** — find which skill(s) the task maps to
3. **Select model** — use the model assigned to that skill
4. **Prepend Canon** — always read first 80 lines of HERMES_KNOWLEDGE_BASE.md
5. **Execute** — run the task with the selected model
6. **Verify** — check Four Nevers, brand voice, gated terms
7. **Save** — write output to `deliverables/` with model suffix

## Quick Reference: Model Selection

| If task involves... | Use | Why |
|---|---|---|
| Strategy, analysis, competitive, pricing, architecture | **Sonnet** | Complex reasoning needed |
| Ad copy, emails, landing pages, social posts | **gpt-oss-120b** | Best creative at $0.19/M |
| Brainstorming, ideas, angles, hooks | **Gemma 4** | Good ideation at $0.10/M |
| Bulk drafts, translations, schema, forms | **Qwen 3.6 Plus** | 23x faster than gpt-oss |
| Reading docs, extracting data, parsing files | **Gemini Flash** | Free, good reader |

## Rules

1. **Never use Sonnet for first drafts** — gpt-oss drafts, Sonnet reviews
2. **Never use Gemini Flash for creative writing** — 2/10 quality proven
3. **Always log model used** in iteration files
4. **$0.50/day ceiling** — if approaching, switch to Qwen/Gemini
5. **Quality < 7/10 → escalate** to Sonnet for revision
6. **One Canon read per session** — don't re-read for every task

## Four Nevers (AUTO-REJECT if present)

- "timeshare" 
- "fractional ownership" (use "deeded co-ownership")
- "investment returns guaranteed"
- "Engine Room"

## Gated Terms (NEVER in public-facing content)

$112,300 | FO Stake | NOI | DSCR | take rate | LTV:CAC

## File Naming Convention

`YYYY-MM-DD-{task-name}-{MODEL}.md`

Examples:
- `2026-04-08-email-nurture-GPTOSS.md`
- `2026-04-08-competitor-analysis-SONNET.md`
- `2026-04-08-marketing-ideas-GEMMA4.md`
