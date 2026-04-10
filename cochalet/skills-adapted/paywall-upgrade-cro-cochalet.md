# paywall-upgrade-cro-cochalet

DBA verdict: SKIP (2026-04-10). Router model: SKIP. This skill is explicitly excluded from CoChalet's marketing system.

## Why This Skill Is Excluded

CoChalet is NOT a SaaS product. There is no:
- Freemium tier
- Free trial
- In-app paywall
- Feature gate
- Subscription upgrade flow
- Plan tier upsell

The skill targets "convert free users to paid" — a pattern that does not exist in CoChalet's model.

## What To Use Instead

If a task resembles paywall-upgrade-cro, route to the appropriate CoChalet skill:

| Task type | Correct skill |
|-----------|--------------|
| Convert Alpine Circle member to FO (co-owner) | sales-enablement-cochalet |
| Upgrade concierge tier (Essentiel → Noir) | onboarding-cro-cochalet |
| Reduce cancellations / non-renewals | churn-prevention-cochalet |
| Convert website visitor to application | signup-flow-cro-cochalet |
| Optimize the application form | form-cro-cochalet |

## Future Applicability (Phase 2+)

If CoChalet introduces:
- A paid Alpine Circle membership tier (currently free/waitlist)
- A premium content subscription
- A tiered app experience (basic vs. premium FO features)

...then this skill becomes relevant. Until then, it remains SKIP in the router.

## TUNING GAPS

- Concierge tier progression (Essentiel → Confort → Noir) is the closest analog to "upgrade CRO" — this is handled by onboarding-cro-cochalet
- If Alpine Circle ever charges membership fees, revisit this skill
- No action required at this time
