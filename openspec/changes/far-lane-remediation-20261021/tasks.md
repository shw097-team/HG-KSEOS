# Tasks — FAR lane/model declaration remediation (epoch 23)

- [x] 1.1 Apply P0/P1/P2 declaration alignment via `var/FAR-REMEDIATION-20261021/apply_far_remediation.py --apply` (receipt: `var/FAR-REMEDIATION-20261021/apply_receipt.json`; local commit `c442f07`)
- [x] 1.2 Verify `check_drift` returns `[]` and the owner-chain test is green (receipt: `var/FAR-REMEDIATION-20261021/selfcheck_receipt.json`, GATE_PASS 18/18; pytest 3 passed / 90 subtests)
- [x] 1.3 Declare `SOD006-C4 OPEN_OWNER_ORDERED` and supersede `SOD006-C3` (registry `sod_invariants.declared_conflicts`; assignment `sod_conflicts`)
- [x] 2.1 Toolchain pin names the installed 0.163.0-alpha.10.2 build with measured sha256 (sha256 f6dbf48c…, verified by `codex --version` and by digest recomputation)
- [x] 2.2 Hermes `model.codex_bin` unified to the same binary
- [x] 3.1 Pool rank/role labels agree with rank order for all three lanes
- [x] 3.2 In-Hermes PLAN-plane profile binds `openai-codex/gpt-6.1-sol` (fresh-session one-shot served gpt-6.1-sol via openai-codex)
- [x] 4.1 Run the self-check harness and the bounded repair loop to green (GATE_PASS 18/18)
- [ ] 4.2 Independent AO lane (gpt-6.1-sol, read-only) re-derives every gate claim — NOT OBTAINED: the Codex-CLI arm returned HTTP 400 `Model is unavailable`; no verdict, no WO result recorded. Local green is NOT acceptance.
- [x] 5.1 Bring the four routing files under git (local commit `c442f07`, no remote action)
- [x] 5.2 Fresh-session PLAN default verified from the profile's own state.db row (row: model=gpt-6.1-sol, billing_provider=openai-codex, source=oneshot)
