# OR-3 — stage_artifacts for ProgramOwner

- items: **6**
- verify after signing: `python tools/check_stage_artifacts.py --owner ProgramOwner`
- if unsigned: 6/18 stages stay ABSENT; nothing else changes
- claim ceiling: an artifact proves an instance exists; it does not prove the package is accepted

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `TPgM:T0` | ABSENT | ProgramIntent@1 |
| 2 | `TPgM:T1` | ABSENT | SchedulingAssumptions@1 |
| 3 | `TPgM:T2` | ABSENT | ProgramDAG@1 |
| 4 | `TPgM:T3` | ABSENT | ProgramSPEC@1 |
| 5 | `TPgM:T4` | ABSENT | HandoffReferral@1 |
| 6 | `TPgM:T5` | ABSENT | ProgramReview@1 |

## What to fill

`artifact_path_or_waiver_per_stage`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
