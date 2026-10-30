# Tasks — durable lane gates (epoch 34)

- [x] Promote the 2026-10-24 owner order to in force (`contract_epoch: 34`, registry `status: IN_FORCE`)
- [x] Repair the registry's own contradiction: rank-1 no longer repeats inside its fallback list
- [x] Project `lane_chains` and `ordered_pool` from the registry, with the epoch digest recorded
- [x] IR-1: `ir1_policy_gate.py` refuses uncommitted routing policy
- [x] IR-4: `ir4_subject_gate.py` refuses a subject with no commit (file subjects resolved via their worktree)
- [x] IR-2: `relay_preflight.py` + loopback health check wired into the dispatcher gate
- [x] IR-2: user-level startup entry (`ocx-relay-start.cmd`) so the relay survives login
- [ ] IR-2: `ocx service install` — needs UAC elevation; operator action, recorded not skipped
- [x] IR-3: `acceptance_default.py`; NOT_RUN is no longer a terminal state
- [x] Recurrence ledger + `recurrence_gate.py`; six classes, each naming its test
- [x] Regression tests: `tests/test_durable_gates.py` (5) and `tests/test_lane_policy.py` (13 pass)
- [x] Dispatcher gate: `--require-durable-gates`, fail-closed, `ERR_DURABLE_GATE_NO_GO`
- [x] EXECUTE lane bounded write with the gates on (CODEX CLI, deepseek-v4.1-flash)
- [ ] VERIFY/AO independent re-derivation of O1..O8
- [ ] Acceptance record (GRANTED or REFUSED_NAMED) written through `acceptance_default.py`
- [ ] Push the branch and read back the remote head
