# FAR-DURABILITY-20261030 — the six recurrences and what now stops them

This round did not add findings. It removed the conditions that let the same findings come back.

## What changed, and where it lives

| Class | Cure | Durable home | Fails when |
|---|---|---|---|
| RC-DISPOSABLE-REPAIR — fixes left in `var/`, `.bak`, live processes | `ir4_subject_gate.py` | `HG-KSEOS/scripts/` (commit) | the subject has no commit, or has uncommitted changes |
| RC-POLICY-WITHOUT-TRANSACTION — policy effective from a dirty worktree | `ir1_policy_gate.py` + registry promoted to `IN_FORCE`, `contract_epoch: 34` | `AGENTS.md`, `config/lane-routing-registry.yaml` | any of the four routing files is dirty |
| RC-LANE-NOT-BOUND — a lane declares a model it need not serve | `lane_policy_reconcile.py` projects registry → `lane_chains` and `ordered_pool` | `scripts/`, `tests/test_lane_policy.py` | a projection drifts from the registry |
| RC-ACCEPTANCE-NEVER-GRANTED — rounds end `NOT_RUN` | `acceptance_default.py` (GRANTED / REFUSED_NAMED; `NOT_RUN` exits 2) | `scripts/` | a round has neither a verdict nor a named refusal with an expiry |
| RC-VACUOUS-PASS — a comparator reports success on missing input | `durable_import.py --assert-files`, `recurrence_gate.py` | `scripts/`, `tests/test_durable_gates.py` | the walk is short, empty, or the named test does not exist |
| RC-TRANSPORT-DIES — the relay is a process | `relay_preflight.py` + Startup entry (service install needs UAC) | `scripts/` + `%APPDATA%\...\Startup` | `/healthz` on the loopback relay does not answer |

All six are wired into `hgk-lane-dispatch.py` behind `--require-durable-gates`, so a round that has not
committed its policy, has no committed subject, or has no live transport is refused **before** a model
is called (`ERR_DURABLE_GATE_NO_GO`, exit 9).

## The policy contradiction this round found and fixed

`config/lane-routing-registry.yaml` declared the 2026-10-24 owner order while its own `fallbacks` list
began with the same rank-1 model and **dropped the demoted primary entirely**. `model-lane-assignment.json`
meanwhile still carried the pre-order chains, and `lane-route-slots.candidate.json` carried a third
version. One policy, three declarations, one red conformance test.

Fixed by making the registry authoritative and generating the other two from it. The lane policy suite
(`13 tests, 116 subtests`) now passes against the epoch-34 policy.

## Verification

- `tests/test_durable_gates.py` — 6 tests, one per class, each naming its `class_id`.
- Independent acceptance (gpt-6.1-sol, nonce `NONCE-AO-20261030-D`, 404.74 s, 1,032,949 input tokens):
  `overall: PASS`, claims `O1-neg`, `O6-neg`, `O7` all PASS, `convictions: []`.
- The first pass (`NONCE-AO-20261030-C`) returned INCONCLUSIVE **and convicted the recurrence gate of
  failing open** — a real defect, fixed in `2285193`, with the regression test that now holds it down.
- Registry rows: B1 `PASS`; SKELETON and HANDOFF originally `FAIL` (manifest only), now `PASS` under
  `-V2` after the archives were published as release assets and re-downloaded to verify the digest.
  The original FAILs are kept: the denominator should show what was not done at the time.
- Release: `fhs-msc-deliveries-20261030` — B1 141 entries, SKELETON 86, HANDOFF 911; all three
  re-hashed from the download URL and matched.

## What is still not done (kept visible, not hidden)

1. `ocx service install` requires UAC; login-survival is provided instead. Restart safety is
   user-level, not machine-level.
2. The 22-WP closure mismatch (`{00,01,15}` declared vs `{00,15}` typed) still needs a decision.
3. Fabric and PIPD were not touched this round; their 13/231 pre-existing dirty files remain.
