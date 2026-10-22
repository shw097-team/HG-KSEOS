## 1. Single-source routing registry (D1, D9, D13, D14)

- [ ] 1.1 Write `config/lane-routing-registry.yaml` with `epoch`, three `routes[]`, `sod_invariants`, `projections[]`
- [ ] 1.2 Pin every active JSON pointer of `model-lane-assignment.json` and `hermes-codex-lane.json` as a binding
- [ ] 1.3 Record `config/hermes.json` runtime-path/model debt as `debt[]` (warn), never a PASS
- [ ] 1.4 Derive the whole projected policy deterministically from the registry (`project_policy`)
- [ ] 1.5 Acceptance test: `test_registry_and_projection_shape` — three lanes in order, zero fallback arms, projection deterministic, baseline non-fatal

## 2. Strict drift gate (D14, D19, D23, D24)

- [ ] 2.1 Implement `check_drift` returning one finding per disagreement as a JSON pointer
- [ ] 2.2 Implement the `validate` CLI (exit 1 on fatal drift) and `diff-live` (what would change)
- [ ] 2.3 Regression: >=32 drift-injection subcases, each mutating one projection site
- [ ] 2.4 Acceptance test: `test_drift_injection_subcases` — per-case non-vacuity, baseline passes, loud named failure

## 3. Pre-dispatch SoD gate (D1, D2, D6, D17)

- [ ] 3.1 Implement `check_sod(maker, checker)` on the normalized model axis
- [ ] 3.2 Implement `scripts/hgk-lane-guard.py` with exits 0 admit / 2 SoD / 3 not admitted / 4 stale epoch
- [ ] 3.3 Refuse when the arm is not lane-shaped ADMITTED, and when the epoch or source digest is stale
- [ ] 3.4 Acceptance test: `test_sod_and_admission_policy` — equal models collide, empty fails closed

## 4. Lane-shaped admission (D7, D8, D11, D12)

- [ ] 4.1 Implement `src/hg_kseos/lane_admission.py` (ADMITTED / REFUSED / UNPROVEN) and the receipt writer
- [ ] 4.2 Implement `scripts/probe-hgk-lane.py`: direct completion recorded separately, never ADMITTED alone
- [ ] 4.3 Implement `--dry-run` with no network I/O; parse the served arm from the Hermes `agent.log` session line
- [ ] 4.4 Acceptance test: a direct completion stays UNPROVEN; a served-model mismatch is REFUSED

## 5. Repaired artifact gate (D23, D24)

- [ ] 5.1 Freeze the input set before reading; exclude own output and registered producer outputs by resolved identity
- [ ] 5.2 Require `--out` and an input digest; fail on empty denominator, missing artifact, sha mismatch, unresolved citation
- [ ] 5.3 Prove semantic-stability: identical frozen inputs produce identical findings with or without a prior output file

## 6. Relay supervisor (D8, D24)

- [ ] 6.1 Implement `scripts/supervise-hgk-opencodex.ps1` for pwsh 7 with healthz + /v1/models checks
- [ ] 6.2 Bounded restart within a window; emit a JSON lease receipt; fail closed and only start the HG-KSEOS launcher
- [ ] 6.3 Verify: run `-Action Verify`; confirm it reports DEGRADED/BLOCKED rather than looping when the relay is down

## 7. Durable wiring + adoption (D15, D16, D18, D20, D21, D22, D25)

- [ ] 7.1 Document every live integration point (path + symbol + line reference + minimal diff intent) in the adoption guide
- [ ] 7.2 Document rollback per component and the applied-versus-staged split
- [ ] 7.3 Produce the OpenSpec change and validate with `openspec validate lane-sod-enforcement --strict`
- [ ] 7.4 Record the execute receipt (artifacts, bytes, sha256, commands, raw test output, untouched paths, `claim_ceiling: CANDIDATE_ONLY`)
