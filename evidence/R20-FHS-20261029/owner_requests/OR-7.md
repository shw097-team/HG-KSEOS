# OR-7 — hold_cells for 前後版 Reader 綁定人

- items: **8**
- verify after signing: `python tools/requalify_hold_cells.py --class TWO_VERSION`
- if unsigned: 8 cells stay HOLD (never converted to PASS)
- claim ceiling: requalification re-runs these cells against YOUR reader; it is not an agent verdict

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `AC-C39-UPGRADE-COMPOSITE` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 2 | `AC-C39-UPGRADE-DETERMINISTIC` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 3 | `AC-C39-UPGRADE-HUMAN` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 4 | `AC-C39-UPGRADE-PROPERTY` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 5 | `AC-C39-UPGRADE-REFERENCE_OUTPUT` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 6 | `AC-C39-UPGRADE-SEMANTIC_JUDGE` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 7 | `AC-C39-UPGRADE-STATE_READBACK` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |
| 8 | `AC-C39-UPGRADE-STATISTICAL` | UPGRADE_TWO_VERSION_BINDING_REQUIRED | 提供前一版與當版可讀 bytes 與升版資格收據 |

## What to fill

`older_reader_id`, `older_version_sha256`, `newer_reader_id`, `newer_version_sha256`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
