## EXECUTE bounded write

NONCE: NONCE-R25-EXEC-20261030A

Six recurrence classes in `config/recurrence-ledger.json` (RECURRENCE-LEDGER/1), two per bullet:

- `RC-POLICY-DRIFT` — the governing policy exists in more than one file and the copies disagree. `RC-DISPOSABLE-REPAIR` — a repair is written into a worktree, a live process or a .bak instead of a commit, a service or a registry row.
- `RC-POLICY-WITHOUT-TRANSACTION` — the effective policy is an uncommitted edit in one working tree. `RC-ACCEPTANCE-NEVER-GRANTED` — every round ends ACC=NOT_RUN, so no round can promote what it fixed.
- `RC-VACUOUS-PASS` — a comparator reports success on missing input. `RC-LANE-NOT-BOUND` — a lane declares a model it is not required to serve.

Preflight entry point read (read-only): `scripts/ir_gate.py` — IR-GATE-PREFLIGHT/1, exit 0 ok / 2 policy dirty or subject uncommitted / 3 subject not in a repo.

Exact output of `git -C C:/Projects/Agent_Workspace/HG-KSEOS log -1 --format=%h`:

```
8ab2d54
```