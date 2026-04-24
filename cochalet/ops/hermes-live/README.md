# Hermes Live Patch Set - 2026-04-21

This directory tracks the live VPS Hermes changes that otherwise live outside
the normal repository checkout.

## Deployed live paths

- `/mnt/hermes-output/cochalet-skills/cochalet/pipeline/model_router.py`
  - Sonnet OAuth delegate is first for default, French, speed, manager,
    strategy, and patch verification chains.
  - Adaptive router suggestions are skipped for delegate-first chains.
- `/mnt/hermes-output/cochalet-skills/cochalet/config/skill-router.json`
  - Default, speed, and French routes point at `/root/claude-delegate.sh`.
- `/root/scripts/hermes-sonnet-swarm.sh`
  - Direct Sonnet OAuth review swarm runner for marketing feedback tasks.
- `/root/.hermes/plugins/cochalet-delegate-router/`
  - Adds `/sonnet-swarm` and `/swarm` commands.
- `/root/claude-delegate.sh` and `/root/opus-delegate.sh`
  - Load `CLAUDE_CODE_OAUTH_TOKEN` from
    `/root/.claudeos/secrets/claude-code-oauth-token`.
  - No OAuth token value is stored in the scripts.

## Earlier blocked-files rescue patches

- Pipeline gating now accepts valid high-quality deliverables and keeps
  malformed/captured prompt files out of production.
- Executor repairs missing deterministic metadata headers when it can infer
  skill and stage from the assembled prompt.
- Dispatcher hashes include date, department, skill, model, and task brief to
  avoid duplicate task collisions.
- Dashboard and heartbeat reporting exclude CMO rescue archive directories.

## Operational note

The OAuth token file is intentionally not tracked. Rotate it with Claude Code
auth/setup-token on the VPS, then replace only the contents of
`/root/.claudeos/secrets/claude-code-oauth-token` and keep permissions at
`0640`.
