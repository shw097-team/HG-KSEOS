# VOID：r2-revision2 隨附的驗證報告不可作為現況引用

| 檔案 | 檔案內寫的 | 對同一批位元組實跑 | 判讀 |
|---|---|---|---|
| `03_TESTS_AND_READBACK/static_validation_result.json`（r2 內） | `passed 2789 / failed 0` | `passed 2788 / failed 1`（`SOURCE-BYTES-UNCHANGED`） | **STALE GREEN — DO NOT USE** |

## 為什麼會差一格

r2 的 `source_manifest.json` 有 29 個 locator 釘在當時的目錄名 `…_SKELETON_SPINE_DRAFT\…`；
該目錄後來被改名到 `…_SKELETON_SPINE\OLD\…_SKELETON_SPINE_DRAFT\…`。檢查 `SOURCE-BYTES-UNCHANGED`
因此有 29 列讀不到檔案 → 1 個 case FAIL。檔案 bytes 從未改變，改的是「指標」。

## 本版（revision3）如何處理

1. 只在**全 64-hex 完全相同**時改寫那 29 列 locator（見 `03_TESTS_AND_READBACK/source_manifest.json`
   的 `locator_repaired_from` 與 `locator_repair_rule`）。
2. oracle 完全沒有放寬：仍是「真實位元組 == 同一枚 pinned sha256」。
3. 報告由對「與本版位元組相同」的副本實跑後回填；本版 fresh 結果為 `2789 / 0`。
4. r2 的位元組**未被修改**，它那份 stale 報告仍留在原處 —— 讀 r2 前請先讀本檔。

## 判讀規則

> 任何 `static_validation_result.*` 只有在「產生它的執行能被指出（root、指令、時間）且 root 與被引用
> 位元組相同」時才可引用；否則一律視為 `STALE`，不得當作 PASS 證據。
