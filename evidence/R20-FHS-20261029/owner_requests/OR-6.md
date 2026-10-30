# OR-6 — hold_cells for 第二 principal（≠ maker，SoD）

- items: **11**
- verify after signing: `python tools/requalify_hold_cells.py --class HUMAN_JUDGE`
- if unsigned: 11 cells stay HOLD (never converted to PASS)
- claim ceiling: requalification re-runs these cells against YOUR reader; it is not an agent verdict

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `AC-C39-EDGE-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 2 | `AC-C39-JOURNEY-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 3 | `AC-C39-MUT-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 4 | `AC-C39-NEG-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 5 | `AC-C39-PARITY-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 6 | `AC-C39-PERF-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 7 | `AC-C39-POS-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 8 | `AC-C39-RECOVERY-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 9 | `AC-C39-ROLLBACK-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 10 | `AC-C39-SEC-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |
| 11 | `AC-C39-UNINSTALL-SEMANTIC_JUDGE` | ORIGINAL_HUMAN_CALIBRATION_AND_JUDGE_READER_REQUIRED | 指定具名 Judge principal 並簽校準；本輪不得以作者自評替代 |

## What to fill

`judge_principal`, `separation_of_duties_statement`, `verdict_per_case`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
