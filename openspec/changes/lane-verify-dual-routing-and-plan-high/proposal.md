# lane-verify-dual-routing-and-plan-high

## Why

The operator instruction of 2026-10-07 changes two facts about the admitted model SoD scheme:

1. Every HERMES and HG-KSEOS use of the PLAN model **GPT 6.1 SOL (OpenAI OAuth)** must default to
   **GPT 6.1 SOL -HIGH (OpenAI OAuth)**. The live runtime resolves reasoning effort per **model**
   (`hermes_constants.resolve_reasoning_config`: per-model `agent.reasoning_overrides`, then global
   `agent.reasoning_effort`), and before this change nothing declared an effort for the PLAN lane at
   all - the lane silently inherited the global `medium`.
2. The **VERIFY / SECURITY** lane must become a **user-instruction-selected dual model-AND-provider
   route**: `GLM-5.3-Flash (OpenCode Go)` and `GPT 6.1 SOL (OpenAI OAuth)`, both at **Medium**, with
   `GPT 6.1 SOL (OpenAI OAuth)` as the **unspecified default**. The declaration previously carried a
   single primary plus a declared "secondary" arm, which made one arm a fallback of the other - a
   relationship the instruction explicitly replaces with two co-equal, operator-selected arms.

The two clauses interact: because the default VERIFY arm is the same normalized model token as the
PLAN lane, the instruction creates a maker/checker **model-axis collision** for the
PLAN-maker / default-checker pair. That collision is declared, not resolved.

## What Changes

- Declare `reasoning_effort: high` for the PLAN route at every active declaration site and make it the
  live model-level default for `gpt-6.1-sol` (`agent.reasoning_overrides`).
- Recast the VERIFY_SECURITY route as a two-arm co-equal supply selector with
  `selection_authority: operator-instruction-at-dispatch` and the OpenAI OAuth arm as the
  unspecified default; neither arm is a fallback of the other.
- Update every projection site and the registry epoch so the drift gate stays a truthful hard-fail.
- Declare `SOD006-C1`: the PLAN-vs-default-checker model collision, with the required compensating
  control (the per-card reasoning pin, and arm-A checking of PLAN-made artifacts).
- Record the live wiring (before/after) as an observation, never as an authority.

## Non-goals

- No production, release or deploy authorization; `sqs_live_trading: NOT_AUTHORIZED` stands.
- No execution of SQP1 or Stage-3; no Shared Spine schema change; no acceptance receipt change.
- No repair of the unrelated defects this round measured (the `gpt-6.1-sol` tier-prefix mis-classification
  and the legacy `codex_route` prose) - they are reported as findings, not fixed here.
- No claim that the collision is resolved. It is declared and frozen for adjudication.
- No claim of provider separation: the two VERIFY arms differ on BOTH axes from each other, but
  EXECUTE and arm A still share `opencode-go`, so only the model axis is required.

## Impact

Affected: `config/model-lane-assignment.json` (revision 10), `config/lane-routing-registry.yaml`
(epoch 10), the live Hermes `config.yaml` (`agent.reasoning_overrides`, `delegation.provider/model`),
the `far-lane-sod-006` kanban board, and this change.
Not affected: `src/hg_kseos/**`, the Shared Spine, `%LOCALAPPDATA%\HG-KSEOS\**`, the sealed Codex lane
binding, and every acceptance receipt.
