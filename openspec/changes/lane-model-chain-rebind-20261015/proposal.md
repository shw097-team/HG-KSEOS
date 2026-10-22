## Why

Owner order (2026-10-15) re-binds the two governance chain faces. Measured today (rev17 / pool rev8):

- PLAN (Hermes engine): default = opencode-go/deepseek-v4.1-flash; gpt-6.1-sol is only FALLBACK2.
- VERIFY_SECURITY (codex-cli checker): primary = opencode-go/glm-5.3-flash; gpt-6.1-sol (OAuth) is demoted, operator-selectable-only.
- EXECUTE (codex-cli writer): default = opencode-go/deepseek-v4.1-flash; fallback1 = NVIDIA DeepSeek (UNREACHABLE_MEASURED_20261011; provider namespace not loaded into the running relay), fallback2 = gpt-6-luna (UNPROVEN / HTTP_400 probe on current CLI account, automatic_selection:false).

The owner wants:
1. PLAN + VERIFY chains become: default GPT 6.1 SOL-MEDIUM (OAuth) -> fallback1 GLM-5.3-Flash (GO) -> fallback2 DeepSeek V4.1 Flash (GO).
2. EXECUTE chain becomes: default DeepSeek V4.1 Flash (GO) -> fallback1 GPT-6-luna (OAuth) -> fallback2 DeepSeek V4.1 Flash (NVIDIA NIM).
3. Per-session-round, user-ordered model selection must be honored on every lane (the mandate consumer from round FAR-LANE-REUSE-RCA-20261015-FIX already provides the enforcement seam).

## What Changes

- Re-order the PLAN / VERIFY_SECURITY / EXECUTE pools and lane_chains to the owner-declared ranking (config-only, candidate change, one authority surface per lane).
- Restore gpt-family admissibility: round_model_exclusions (scope HGK-SOLUTION-APPLY-20261012) lapses with a NEW round scope declaration; no code change needed because check_exclusions is round-scoped.
- Declare re-selection surfaces: PLAN and VERIFY honor a per-round mandate file (existing runtime_role_binding_assert.py); EXECUTE honors ModelChain (existing Resolve-CodexExecuteRoute) and dispatcher --require-arm/--force-rank (existing).
- Record persisted limitations as pre-existing (not introduced here): NVIDIA DeepSeek provider needs a relay-restart window; luna is still UNPROVEN/HTTP-400 on the current CLI account.
- Successor work orders may optionally refresh the stale canonical binary pin (config/hermes-codex-lane.json) — out of scope here.

## Capabilities

### New Capabilities
- lane-model-chain-policy: The declared model chain per lane (default + ordered fallbacks) and the per-session-round user re-selection contract, machine-checked by the existing mandate consumer and resolver.

### Modified Capabilities

(none — this is the first spec for lane chain policy)

## Impact

- Files: config/lane-route-slots.candidate.json (pool order), config/model-lane-assignment.json (assignment + lane_chains + registry_epoch 17->18), config/lane-routing-registry.yaml (source pin refresh + new round exclusions block), records in var/.
- Runtime: no script change required; existing resolver + mandate consumer + launcher resolver already honor re-ordering and per-round selection.
- Tests: tests/test_lane_policy.py assertions on order/epochs need updating; new negative test: mandate for an arm not in its lane pool must refuse (already covered by tests/test_far_lane_fix_20261015.py).
- Risk: gpt-6.1-sol arm on OPENAI OAuth needs relay-side credential health; quota condition the owner flagged is the very reason it was demoted before — the new default will fail-closed via identity gate when quota is out.
