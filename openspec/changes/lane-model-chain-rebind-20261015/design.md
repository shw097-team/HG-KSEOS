## Context

Round FAR-LANE-ROUTE-REBIND-20261015. Owner re-declares the two governance chains and adds an
per-session-round user re-selection contract. All enforcement seams already exist and were
proven in round FAR-LANE-REUSE-RCA-20261015-FIX (tests/test_far_lane_fix_20261015.py, 158 OK):

- resolver `scripts/hgk-lane-route.py` reads ordered_pool per lane
- identity gate `hgk-lane-dispatch.py` (relay OAuth health) + require_arm==served_arm receipt
- launcher `Resolve-CodexExecuteRoute` (EXECUTE single-model selection from binding + additional_routes)
- mandate consumer `scripts/runtime_role_binding_assert.py` (P1-A) refuses undeclared/unresolvable arms
- round exclusion `lane_policy.check_exclusions` is round-scoped and lapses naturally with a new round block

## Goals / Non-Goals

Goals: re-order two chains to owner ranking; make re-selection an explicit, gate-consumed contract.
Non-Goals: fixing luna HTTP-400 backend admission; loading the nvidia provider namespace into the running relay (needs one relay-restart window the owner must authorize); refreshing the stale canonical binary pin (separate owner decision).

## Decisions

### D1: Re-order by config-only changeset (candidate)
Update ordered_pool ranks + role labels in lane-route-slots.candidate.json and lane_chains order in model-lane-assignment.json; bump registry_epoch 17 -> 18; refresh registry source pin. Alternative (adding new fallback machinery) rejected: violates no-over-engineering — the ordered list IS the chain.

### D2: Per-round selection reuses the mandate file, not a new channel
The owner order is already written down per round in var/<round>/FIX/role_mandate.json; the existing
consumer compiles it against pool+toolchain. Extending it to read the chain is a one-field addition
(intent ranking), NOT a new control plane.

### D3: gpt re-admission via replacement of the exclusion block
Replace `round_model_exclusions` (scope HGK-SOLUTION-APPLY-20261012, excluded gpt-*) with the new
round's scope and no family exclusion. No code change: check_exclusions is data-driven.

### D4: default-chain OAuth health is enforced by existing gates, not promises
openai-codex arms route through the relay OAuth pool: the identity gate refuses with
ERR_RELAY_OAUTH_NEEDS_REAUTH when the credential cannot refresh, so a quota/dry OAuth not health
turns into a typed refusal + fallback attempt, exactly the behavior the owner asked for ("fallback").

### D5: reason records preserved
Keep the old chain as `lane_chains<...>_previous_revision_*` style records so the rebind is auditable.

## Risks / Trade-offs

- Quota asymmetry: making gpt-6.1-sol the DEFAULT for PLAN/VERIFY means a quota exhaustion is now
  hit on the happy path. Mitigation: the fallback arms are dispatched automatically by the existing
  ARM fallback loop (OK RFC: ERR_RELAY_OAUTH_NEEDS_REAUTH -> next ordered arm), each refusal typed.
- luna UNPROVEN/HTTP-400 stays an accepted limitation, recorded in the pool entry it lives in.
- Task-local toolchain declaration (sources/task_local_toolchain.json) remains the binary identity
  source until the owner approves the canonical pin refresh.

## Migration Plan

1. Apply the two config changesets (candidate), each with .bak; refresh registry source pin.
2. Bump registry_epoch and revision pointers; run lane_policy.load_registry() readback.
3. Positive tests: resolver order readback; lane_policy projections; mandate consumer OK for new default.
4. Negative tests: exclusion-lapse admission; unresolvable mandate refuse (exists).
5. E2E: one EXECUTE lane turn (DeepSeek) + one VERIFY lane turn (mandated GLM) + one PLAN lane readback in Hermes; all receipts archived under var/<round>/.
6. HGK lifecycle: candidate -> (owner) -> apply -> acceptance NOT managed by agents.

## Open Questions

- Does the owner want PLAN per-round re-selection to also write a persisted receipt (session model
  readback) every turn? Default answer: no — Hermes session model is user-controlled state, and
  runtime_role_binding_assert already provides the pre-dispatch check for codex lanes; the PLAN lane
  in-Hermes check remains an advisory比对 unless HGK admission later requires more.

## What was deferred

- Real relay-restart window for nvidia provider: owner-gated.
- Canonical binary pin refresh: owner-gated.
