# OR-4 — hold_cells for 受保護校準 Reader 指派人

- items: **11**
- verify after signing: `python tools/requalify_hold_cells.py --class CALIBRATION`
- if unsigned: 11 cells stay HOLD (never converted to PASS)
- claim ceiling: requalification re-runs these cells against YOUR reader; it is not an agent verdict

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `AC-C39-EDGE-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 2 | `AC-C39-JOURNEY-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 3 | `AC-C39-MUT-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 4 | `AC-C39-NEG-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 5 | `AC-C39-PARITY-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 6 | `AC-C39-PERF-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 7 | `AC-C39-POS-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 8 | `AC-C39-RECOVERY-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 9 | `AC-C39-ROLLBACK-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 10 | `AC-C39-SEC-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |
| 11 | `AC-C39-UNINSTALL-STATISTICAL` | ORIGINAL_CALIBRATED_THRESHOLD_READER_REQUIRED | 取得原校準門檻 bytes＋Owner 認可後重跑該 cell |

## What to fill

`reader_id`, `reader_authority`, `calibration_source_sha256`, `calibration_value`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
