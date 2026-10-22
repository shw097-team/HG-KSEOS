# lane-mandate-rebinding-and-d01-revocation

## Why

The lane registry binds the PLAN lane to `openai-codex / gpt-6.1-sol`, which collides with the owner's mandated independent checker on gpt-6.1-sol: the registry's own SoD text says the alternate arm 'still collides with PLAN and must be refused for PLAN-made artifacts', so a mandated checker can be legitimately refused. The owner's model plan binds PLAN to `opencode-go / deepseek-v4.1-flash`.

The VERIFY/SECURITY alternate arm is declared `NON-DEFAULT operator-selectable ... never auto-selected`, and the registry self-declares `wiring_feasibility.projection_drops_dual_arms.state = DECLARED_GAP_NOT_FIXED` (the projected dispatch carries only the primary route), so no governed dispatcher can reach the alternate arm even when the owner names it.

A declared model deviation `D-01` (declared gpt-6.1-sol -> actual gpt-5.6-sol) was recorded on the strength of an HTTP 400 that a single-variable A/B measurement later showed to be manufactured by a stale local Codex CLI build; the substitution therefore rested on a false blocker and must be revoked.

## What Changes

Four bounded, checkable pieces. Each is a candidate declaration change only; none of them is applied by this change.

- **C1 — PLAN lane rebinding.** The PLAN lane is rebound to the owner's mandated `opencode-go / deepseek-v4.1-flash`. Every stale `PLAN = gpt-6.1-sol` reference in the registry is updated (the `routes[PLAN]` binding, `lane_chains.PLAN[0]`, `sod.plan_lane`,
  `sod.plan_reasoning_effort` consumers, `effective_wiring.plan_high.surfaces`, and the `projections[]` bindings that pin the PLAN site), and the registry's publication counter (`epoch`, the registry's own declared self-advancing counter) is advanced because the registry's committed content changes.
- **C2 — VERIFY/SECURITY arm reachability.** The alternate arm is preserved AND made visible in the projected dispatch, closing `wiring_feasibility.projection_drops_dual_arms.state = DECLARED_GAP_NOT_FIXED`. `_compact_route()` (or its successor) must carry `arms[]` and
  `selection_authority`, not only the primary route. The owner mandate for THIS round — VERIFY/SECURITY run by CODEX CLI with checker model `opencode-go/glm-5.3-flash` — must be expressible as the selected arm through a new additive selection field, without rewriting the historical arm records.
- **C3 — D-01 revocation.** An ADDITIVE revocation record names the original D-01 artifact path plus its `sha256` (so the frozen bytes and any manifest that binds them stay valid), states the falsifying A/B evidence, and binds the checker lane to the currently mandated model. The original D-01 artifact is not mutated.
- **C4 — Exclusion rule.** A model family excluded by the owner for a round must not be restorable by a registry default or by an inherited child setting. This is the invariant that makes the PLAN rebinding and the round exclusion actually held, not just declared.
- **C5 — SoD encoding reconciliation.** The registry's static `sod_invariants.pairs` declared a strict pair `{maker: EXECUTE, checker: PLAN, distinct_required: true}` while the SAME registry recorded `declared_conflicts: SOD-APPLY-01` with `pairs: [[EXECUTE, PLAN]]` and `status: OPEN` — i.e. an accepted identity overlap enforced as a refusal. C5 removes the un-reconciled strict pair, keeps `SOD-APPLY-01` recorded as a fact with a named compensating control, and aligns the encoding with the owner's 2026-10-10 slot semantics (`selection_semantics.sod`: NOT enforced at this revision; identity overlaps recorded as facts, not refusals). It is an ENCODING fix, not a model change: PLAN stays on the owner's rank-1 default.

## Status — applied this round (NOT an acceptance)

C1–C4 were **applied to the live tree** under owner authorisation `AMENDMENT_02` (see the round's `admission/`), after a first, unreconciled attempt failed conformance gate 2 (`tests/test_lane_policy.py::test_registry_and_projection_shape`, `EXECUTE!=PLAN must hold: SOD_VIOLATION`) and was rolled back; C5 was applied under `AMENDMENT_03` (owner Option 1, step (a)). Post-application gates: drift 0, `3 passed / 90 subtests passed`, every declared SoD pair resolves clean. Live facts: `epoch: 16`, `routes[PLAN] = opencode-go/deepseek-v4.1-flash`, `sod_invariants.pairs` = `[EXECUTE/VERIFY_SECURITY, PLAN/VERIFY_SECURITY]`, `SOD-APPLY-01` still recorded, `round_model_exclusions` present, `revocation_sidecars` present and its three round-relative files present. **Applying this change is not an acceptance of it**; the acceptance claim remains the owner's, and an independent checker lane's verdict is required for closure.


## Non-goals

- This change was authored as a CANDIDATE and was later **applied** to the live tree under explicit owner authorisation (see *Status* above); it still does not promote, archive, write the main specs, or make any acceptance claim. The applied state is recorded here so the change is not misread as un-applied.
- As authored, no edit to `config/`, no registry mutation, no route/credential edit, no `src/**` change, no git write — the mechanism edits C1–C5 require were described, not performed. **Superseded by the applied Status above:** `config/lane-routing-registry.yaml`, `config/model-lane-assignment.json`, `config/hermes-codex-lane.json` and `src/hg_kseos/lane_policy.py` were edited by `candidate/apply_rebinding.py` under AMENDMENT_02/03, with backups and a receipt. No credential, no `PIPD/` write, and no git write were performed at any point.
- No claim about the GPT-quota state beyond the owner's stated exclusion; no provider-liveness claim.
- No rewriting or deletion of historical arm records, the D-01 artifact, or any frozen evidence byte.

## Impact

Affected (once applied, outside this change): `config/lane-routing-registry.yaml` (routes[PLAN], lane_chains, sod block, projections, `epoch`), `config/model-lane-assignment.json` (the projected site), the compact-route projection function, the D-01 record's additive revocation companion under the round, and this change's capability spec.

Not affected: the frozen D-01 artifact bytes, `src/**` behaviour other than the single projection function named in C2, provider credentials, the Shared Spine schema, and every acceptance receipt. This change writes only the planning artifacts under
`openspec/changes/lane-mandate-rebinding-and-d01-revocation/`.
