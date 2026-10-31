# FAR-DURABILITY-20261030 — what changed, and what this round learned about itself

## 1. The diagnosis this round acted on

Six defect classes recurred at least twice between 2026-10-21 and 2026-10-30. All six had been
diagnosed in prose before; none had been converted into something that fails when the defect returns.
The mechanism was the same every time: the repair landed in a **disposable layer** — a working tree,
a live process, a `.bak`, a round's receipts — and the round closed with `ACC = NOT_RUN`, so nothing
was promoted and the next round began from the same state.

## 2. What is now in the durable layer

| Class | Gate | What fails when the defect returns |
|---|---|---|
| RC-POLICY-DRIFT | `scripts/lane_policy_reconcile.py` | `--check` exits 2 when `lane_chains` or `ordered_pool` diverges from `registry.routes` |
| RC-POLICY-WITHOUT-TRANSACTION | `scripts/ir1_policy_gate.py` | `POLICY_DIRTY` — a turn may not run against uncommitted routing policy |
| RC-DISPOSABLE-REPAIR | `scripts/ir4_subject_gate.py` | `NO_REPO` — a subject outside a git worktree can only be ADVISORY_ONLY |
| RC-TRANSPORT-DEATH (folded into IR-2) | `scripts/relay_preflight.py` | `RELAY_DOWN` instead of a 401 that looks like a credential fault |
| RC-ACCEPTANCE-NEVER-GRANTED | `scripts/acceptance_default.py` | the closing step has two exits: GRANTED or REFUSED_NAMED; NOT_RUN exits 2 |
| RC-VACUOUS-PASS | `scripts/durable_import.py` | `WALK_INCOMPLETE` / `FILE_COUNT_MISMATCH` / `EMPTY` instead of a green manifest over 10 % of a tree |
| RC-LANE-NOT-BOUND | registry epoch 34 + `--require-durable-gates` | the dispatcher refuses before the spawn; rank-1 is the mandated model, and the reconciliation keeps the declaration equal to the route |

`config/recurrence-ledger.json` is the index: every class names the test that holds it down, and
`scripts/recurrence_gate.py --all` refuses a class that recurred twice without one.

## 3. The policy defect that was hiding inside the policy

Promoting the 2026-10-24 owner order surfaced a contradiction nobody had measured: the same policy
was declared in four places — `lane-routing-registry.yaml` (routes), `model-lane-assignment.json`
(`lane_chains` and `assignment` rows), `lane-route-slots.candidate.json` (`ordered_pool`), and the
registry's own `projections[].bindings[].expected`. On 2026-10-30 the registry said PLAN rank-1 =
`gpt-6.1-sol` while `lane_chains` and the pool still said `deepseek`, so
`tests/test_lane_policy.py` failed **against the file it was supposed to certify**. Worse, the new
rank-1 was repeated inside its own fallback list and the demoted arm had been dropped entirely: a lane
that lost its primary would have silently skipped the only other live model.

That is now one authority plus three projections, with the epoch digest recorded in each projection.

## 4. Self-critique: the round caught itself twice

1. **The vacuous pass, again.** My own `durable_import.py` reported 95 files / 26 MB with
   `walk_errors: 0` for a 911-file / 236 MB tree, because `os.scandir` silently stops at the first
   path over MAX_PATH. A green receipt for 10 % of the payload — on the same day I was writing a
   report about gates that certify presence rather than correspondence. Fixed by the three
   fail-closed exits above, with a positive control (911 files, byte-identical rollup) and a negative
   control (`--assert-files 9110` → exit 6).
2. **The gate blocked its own round.** `--require-durable-gates` refused the EXECUTE dispatch because
   `scripts/` carried three pre-existing dirty entries from an earlier session. That refusal was
   correct: the round was trying to claim progress on a subject that was not committed. The response
   was to name the actual subject (`config/recurrence-ledger.json`, committed and clean), not to
   weaken the gate.

## 5. What is still not done, stated as not done

- `ocx service install` needs UAC elevation (`schtasks /create` → access denied). A user-level startup
  entry was installed instead, which survives login but not a headless reboot before login. The
  elevated action remains the operator's.
- SKELETON_SPINE (86 files / 33.7 MB) and HANDOFF-PATCH-v1 (911 files / 236 MB) have manifests but no
  published archive. Their acceptance rows are registered as **FAIL** for that reason, so the
  denominator shows them as open rather than as done.
- The round's own acceptance still depends on the independent checker's verdict; this document does
  not grade it.

## 6. The rule this round would keep

> A fix is not the sentence that describes it. It is the test that fails when the sentence stops
> being true.

Everything above is an instance of that one line, applied six times.
