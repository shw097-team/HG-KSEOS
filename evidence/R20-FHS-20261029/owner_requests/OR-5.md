# OR-5 — hold_cells for OWNER（人類決策）

- items: **16**
- verify after signing: `python tools/requalify_hold_cells.py --class HUMAN_DECISION`
- if unsigned: 11 cells stay HOLD (never converted to PASS)
- claim ceiling: requalification re-runs these cells against YOUR reader; it is not an agent verdict

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `AC-C39-EDGE-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 2 | `AC-C39-JOURNEY-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 3 | `AC-C39-MUT-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 4 | `AC-C39-NEG-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 5 | `AC-C39-PARITY-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 6 | `AC-C39-PERF-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 7 | `AC-C39-POS-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 8 | `AC-C39-RECOVERY-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 9 | `AC-C39-ROLLBACK-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 10 | `AC-C39-SEC-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 11 | `AC-C39-UNINSTALL-HUMAN` | ORIGINAL_HUMAN_DECISION_READER_REQUIRED | 由原 Owner 出具判定收據；作者不得代簽 |
| 12 | `AC-C39-PERF-COMPOSITE` | PERFORMANCE_SOURCE_THRESHOLD_NOT_BOUND | PERFORMANCE_UNOBSERVED waiver |
| 13 | `AC-C39-PERF-DETERMINISTIC` | PERFORMANCE_SOURCE_THRESHOLD_NOT_BOUND | PERFORMANCE_UNOBSERVED waiver |
| 14 | `AC-C39-PERF-PROPERTY` | PERFORMANCE_SOURCE_THRESHOLD_NOT_BOUND | PERFORMANCE_UNOBSERVED waiver |
| 15 | `AC-C39-PERF-REFERENCE_OUTPUT` | PERFORMANCE_SOURCE_THRESHOLD_NOT_BOUND | PERFORMANCE_UNOBSERVED waiver |
| 16 | `AC-C39-PERF-STATE_READBACK` | PERFORMANCE_SOURCE_THRESHOLD_NOT_BOUND | PERFORMANCE_UNOBSERVED waiver |

## What to fill

`decision_per_case`, `performance_waiver_accepted (true/false)`, `waiver_basis`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
