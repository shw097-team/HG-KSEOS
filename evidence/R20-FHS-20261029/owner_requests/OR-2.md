# OR-2 — stage_artifacts for ArchitectureOwner

- items: **6**
- verify after signing: `python tools/check_stage_artifacts.py --owner ArchitectureOwner`
- if unsigned: 6/18 stages stay ABSENT; nothing else changes
- claim ceiling: an artifact proves an instance exists; it does not prove the package is accepted

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `SE:T0` | ABSENT | SystemReadset@1 |
| 2 | `SE:T1` | ABSENT | OwnershipSeamMap@1 |
| 3 | `SE:T2` | ABSENT | ADRSet@1 |
| 4 | `SE:T3` | ABSENT | ArchitectureSPEC@1 |
| 5 | `SE:T4` | ABSENT | ArchitectureNEGRequest@1 |
| 6 | `SE:T5` | ABSENT | ArchitectureReview@1 |

## What to fill

`artifact_path_or_waiver_per_stage`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
