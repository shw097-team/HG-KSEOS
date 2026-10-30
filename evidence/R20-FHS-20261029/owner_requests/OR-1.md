# OR-1 — stage_artifacts for ProductOwner

- items: **6**
- verify after signing: `python tools/check_stage_artifacts.py --owner ProductOwner`
- if unsigned: 6/18 stages stay ABSENT; nothing else changes
- claim ceiling: an artifact proves an instance exists; it does not prove the package is accepted

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `PM:T0` | ABSENT | ProductKnownState@1 |
| 2 | `PM:T1` | ABSENT | QuestionPriority@1 |
| 3 | `PM:T2` | ABSENT | ProductSuccess@1 |
| 4 | `PM:T3` | ABSENT | ProductSPECDraft@1 |
| 5 | `PM:T4` | ABSENT | ProductAcceptanceProposal@1 |
| 6 | `PM:T5` | ABSENT | ProductReviewRequest@1 |

## What to fill

`artifact_path_or_waiver_per_stage`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
