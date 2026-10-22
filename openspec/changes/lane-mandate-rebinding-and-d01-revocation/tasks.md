## 1. T1 — Registry rebinding (C1: PLAN -> opencode-go / deepseek-v4.1-flash)

- [ ] 1.1 Enumerate every site in `config/lane-routing-registry.yaml` that binds PLAN to `gpt-6.1-sol`: `routes[PLAN]` (provider/model/canonical_identity/auth/oauth), `lane_chains.PLAN[0]`, `sod.plan_lane`, and the PLAN entries in `effective_wiring.plan_high.surfaces`; record the exact JSON/YAML pointer of each
- [ ] 1.2 Rebind each enumerated site to `opencode-go / deepseek-v4.1-flash` (`canonical_identity: deepseek-v4.1-flash`, `auth: env_ref:OPENCODE_GO_API_KEY`, `oauth: false`) with no site left declaring `gpt-6.1-sol` for PLAN
- [ ] 1.3 Update the matching PLAN-site `bindings[]` in `projections[]` (model, provider, and any canonical-identity pointer) so the drift expectation equals the new rebinding, not the old
- [ ] 1.4 Advance the registry publication counter `epoch` (15 -> 16) and update its commentary block in the same edit, because the committed content changed
- [ ] 1.5 Synchronize `source_of_routes` (revision/digest) and the projected site `config/model-lane-assignment.json` so the drift gate resolves without a stale pointer
- [ ] 1.6 Re-run the registry drift gate and record the raw output; zero `severity=error` findings is the exit condition

## 2. T2 — Arm reachability and projection fix (C2: close DECLARED_GAP_NOT_FIXED)

- [x] 2.1 Preserve the alternate arm record unchanged (arm B `gpt-6.1-sol` / `openai-codex`) — do NOT delete or demote it further; the fix is reachability, not removal
  — evidence: registry `routes[VERIFY_SECURITY].arms[1] = {canonical_identity: gpt-6.1-sol, provider: openai-codex, role: demoted_alternate_operator_selectable_only_never_auto_selected}`; read raw via `PYTHONPATH=src python var/far-doc-update-20261013/gates.py`
- [x] 2.2 Extend the compact-route projection function (`_compact_route()` or successor) to carry `arms[]` and `selection_authority` so the projected dispatch contains BOTH arms, not only the primary route
  — evidence: LIVE `src/hg_kseos/lane_policy.py` (sha256 `5384116F2CD8568A26B9244CC11A206B25A2DCEC435E2D9E1BA8C4C6F0A089BB`) `_compact_route(VERIFY_SECURITY)` returns `arms[]` (2) + `selection_authority`
- [x] 2.3 Flip `wiring_feasibility.projection_drops_dual_arms.state` from `DECLARED_GAP_NOT_FIXED` to a FIXED/CLOSED state with the evidence that the projection now carries the arms; keep the historical evidence text
  — evidence: site state is now `CLOSED_FIX_APPLIED_TO_LIVE_SRC` with `closed_evidence` recorded; the historical `evidence`/`proposed_change` text is kept verbatim under `state_correction_note` (F18 closed; registry epoch 16→17)
- [x] 2.4 Add an additive round-selection field (e.g. `selected_arm`) and record THIS round's owner mandate there: VERIFY/SECURITY = CODEX CLI, checker model `opencode-go/glm-5.3-flash`, WITHOUT rewriting the existing arm A/arm B records or any historical field
  — evidence: route carries `selected_arm: A`, `selected_arm_identity: glm-5.3-flash`, `selection_authority: owner-adjudication-1-HGK-SOLUTION-APPLY-20261012`; arm A/arm B records unrewritten. NOTE: this round's task-scoped checker deviation (same model as maker/executor, owner-authorised) is recorded in `admission/AMENDMENT_03` and the closure report, NOT in this registry field
- [x] 2.5 Fix the `bindings[]` entry that pins `wiring_feasibility/projection_drops_dual_arms/state` so drift matches the closed state
  — evidence: binding expected value updated; `check_drift()` = 0 findings on the closed state, and exactly 1 `DRIFT_VALUE` on that pointer under a perturbation (negative control), so the pin is live and not vacuous
- [ ] 2.6 Prove the compiled dispatch now contains both arms (assert `arms[]` length and `selection_authority` presence; assert the primary route is unchanged) and record the raw output
  — NOT ticked: the raw output IS recorded and reproducible, but the task asks for an ASSERTION and no repo-level test asserts `arms[]`/`selection_authority` (the existing suite only asserts `fallbacks == []`). Ticking it would rest on a manual measurement, not on a deterministic test

## 3. T3 — D-01 revocation record (C3)

- [ ] 3.1 Read the original D-01 artifact and record its absolute path and `sha256` (the two byte-identical files `verify/MODEL_SUBSTITUTION.txt` and `evidence/09_CHALLENGE/MODEL_SUBSTITUTION.txt`, both `f54dec16d48d9432d61d3394b3468cfd2a12ddf5dfecf724a34922c8246e7fc2`) into the revocation record's `original_path` + `original_sha256`
- [ ] 3.2 Write an ADDITIVE revocation record (new companion file beside the round, e.g. `D-01_REVOCATION.json`) with `deviation_id: D-01`, `verdict: REVOKED`, and the falsifying evidence: the same isolated home/auth/model/prompt produced HTTP 400 exit 1 on Codex CLI `0.147.0-alpha.6.5` and `OK` exit 0 on `0.162.0-alpha.17.2`
- [ ] 3.3 Bind the checker lane in the revocation record to the currently mandated model (`opencode-go/glm-5.3-flash`), replacing the revoked substitution's `gpt-5.6-sol` binding for the forward mandate
- [ ] 3.4 Assert the original artifact is byte-unchanged by the change: re-hash both original files and confirm they still equal `f54dec16...e7fc2`; assert no manifest that binds those bytes was edited
- [ ] 3.5 Record the revocation record's own `sha256` and that it is keyed by the original's digest, so a later reader can join revocation to the frozen bytes

## 4. T4 — Exclusion rule (C4)

- [ ] 4.1 Declare the rule in the registry: a model family excluded by the owner for a round MUST NOT be selected by a registry default, a fallback arm, or an inherited child setting
- [ ] 4.2 Enumerate the exclusion for THIS round (the `gpt-*` family, excluded because the GPT quota is nearly exhausted) and record its authority and scope
- [ ] 4.3 Assert the exclusion survives the PLAN default path and the `delegation` inheritance path — no default or inherited child setting may re-enter an excluded family
- [ ] 4.4 Record a check that a dispatch naming an excluded family is refused (not silently downgraded) while a permitted family dispatches normally

## 5. T5 — Tests

- [ ] 5.1 Drift test: the rebinding (C1) leaves zero `severity=error` findings and the `epoch` advance is consistent with the changed bytes
- [ ] 5.2 Projection test: the compact route carries `arms[]` + `selection_authority` and the primary route is byte-identical to pre-change (C2)
- [ ] 5.3 History-preservation test: original D-01 bytes still hash to `f54dec16...e7fc2` and no arm/history record was rewritten (C3)
- [ ] 5.4 Exclusion test: an excluded family cannot be reached via the registry default or an inherited child setting (C4)
- [ ] 5.5 Record all raw test output and exit codes; no test is marked done by this change (candidate only)

## 6. T6 — Docs

- [ ] 6.1 Document the PLAN rebinding and every updated site, with before/after values (C1)
- [ ] 6.2 Document the arm-reachability fix and the round-selection field, stating the projection now carries both arms and the history was preserved (C2)
- [ ] 6.3 Document the D-01 revocation: original path + `sha256`, falsifying A/B evidence, the bound checker lane, and the explicit statement that the original is not mutated (C3)
- [ ] 6.4 Document the exclusion rule and its round-scope authority (C4)
- [ ] 6.5 State the claim ceiling: this change authors the rebinding document; it does not apply the rebinding and is not an acceptance

## 7. T7 — SoD encoding reconciliation and applied status (C5; owner Option 1 step (a), AMENDMENT_03)

- [x] 7.1 Remove the un-reconciled strict pair `{maker: EXECUTE, checker: PLAN, distinct_required: true}` from `sod_invariants.pairs` — evidence: `candidate/config/lane-routing-registry.rebound.yaml` (pairs now `[EXECUTE/VERIFY_SECURITY, PLAN/VERIFY_SECURITY]`), applied live
- [x] 7.2 Keep `SOD-APPLY-01` recorded (status OPEN) and add a `reconciliation:` block naming the authority, the decision reference (`FAR-RUN-W6-PLAN-SOD-020 / DEC-020-1`) and the compensating control — evidence: the `reconciliation:` block under `SOD-APPLY-01` in the live registry
- [x] 7.3 Exercise the reconciliation by mirror A/B: the same conformance test fails on the unreconciled encoding (`1 failed, 2 passed`) and passes on the reconciled one (`3 passed, 90 subtests passed`) with the PLAN model unchanged — evidence: `candidate/reconcile_sod_pair.py` output (control rc=1 / remedy rc=0) and the live gate run
- [x] 7.4 Apply C1–C4 to the live tree under AMENDMENT_02 after the reconciliation, and record the post-apply gates — evidence: `evidence/APPLY_W1W2_20261013T*.txt`, `candidate/APPLIED_REBINDING_RECEIPT.json`
- [x] 7.5 Record the earlier failed application honestly: the unreconciled apply failed gate 2 (`EXECUTE!=PLAN must hold: SOD_VIOLATION`), was rolled back, and both the failure and the rollback are recorded — evidence: `evidence/APPLY_W1W2_GATE_FAILURE.md`, `var/far-w6-nextstep-decision-20261012/POST_RUN_CORRECTION.md`
- [x] 7.6 Record THIS round's checker override (`opencode-go/deepseek-v4.1-flash`) as a round-scoped deviation with its compensating control and the published arm left readable — evidence: `admission/AMENDMENT_03_owner-option1-and-task-scoped-checker.md`
- [ ] 7.7 Independent verification of 7.1–7.6 by a checker lane — see the round's checker receipt; writer-side claims are not sufficient

### Application status (measured, this round)

| item | state | measured basis |
|---|---|---|
| T1 / C1 rebinding | **APPLIED** | `epoch: 17` (advanced from 16 by the F18 correction); `routes[PLAN] = opencode-go/deepseek-v4.1-flash` |
| T2 / C2 arm reachability | **CLOSED (F18 fixed)** | the live registry/projection carries `arms[]` + `selection_authority` + `selected_arm`; the site's `/wiring_feasibility/projection_drops_dual_arms/state` now reads `CLOSED_FIX_APPLIED_TO_LIVE_SRC` (was `FIX_READY_IN_CANDIDATE_PROJECTION_NOT_APPLIED_TO_LIVE_SRC`) and the `bindings[]` pin matches it (registry epoch 16→17), so the drift gate is a truthful 0 rather than a mutual mis-declaration. Tasks 2.1–2.5 ticked with evidence; **2.6 stays unticked** (no repo-level assertion test for `arms[]`/`selection_authority`) |
| T3 / C3 D-01 revocation | **APPLIED** | the three round-relative sidecar files are present; the original artifact's bytes re-hash to `f54dec16…e7fc2` (244 B) at its real location under the PIPD worktree — unchanged |
| T4 / C4 exclusion rule | **APPLIED** | `round_model_exclusions` present (prefixes `gpt-`; provider `openai-codex`); `src/hg_kseos/lane_policy.py` carries `check_exclusions` |
| T5 / tests | **PARTIAL** | the drift/projection/SoD gates are green; the exclusion- and history-preservation arms are covered by the suite, but no test exercises the stale-state drift of F18 |
| T6 / docs | **PARTIAL** | this file, `proposal.md` and `design.md` are updated for C5 and the applied status; the per-site before/after tables of T6.1 are still owed |

**Claim ceiling:** everything above is a record of what the writer measured, not an acceptance and not an independent verdict. `owner acceptance: NOT_RUN`.

