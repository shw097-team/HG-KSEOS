# revision3 修補說明（同一 Subject 的第二版交付）

> 本檔是 `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` 的**修補版說明**。
> r2-revision2 的位元組**未被修改**：它仍是凍結輸入，也是本版的回推點。
> Claim ceiling：`AUTHOR_SIDE + ISOLATED_LOCAL`。`NATIVE_ADMISSION = 0`、`INDEPENDENT_ACCEPTANCE = 見 §6`、
> `RELEASE = NOT_RUN`、`MAIN = MERGED_NO`、`PRODUCTION = NOT_CLAIMED`。

## 1. 為什麼有 revision3

r2 交付時，套件內 `03_TESTS_AND_READBACK/static_validation_result.json` 記 `passed 2789 / failed 0`，
但對**同一批位元組**重新執行 `tools/validate.py` 得到 `2788 / 1`，唯一失敗是 `SOURCE-BYTES-UNCHANGED`。
交付物比實際樂觀一格，屬誤導級（stale green）。本版把三件事一次修掉：

| # | 缺陷 | 量測事實 | 修法 | 是否改動 oracle |
|---|---|---|---|---|
| D-1 | 29 個來源 locator 釘在已改名的目錄（`…_SKELETON_SPINE_DRAFT\…` → `…_SKELETON_SPINE\OLD\…_SKELETON_SPINE_DRAFT\…`） | r2 fresh：`SOURCE-BYTES-UNCHANGED` FAIL，29 列不可讀 | 只在**全 64-hex 完全相同**時改寫該 29 列；寫入 `locator_repaired_from` / `locator_repair_rule` | **沒有**。檢查仍比對真實位元組與同一枚 pinned sha256 |
| D-2 | 套件內含**自己的 ZIP**（13,326,288 B） | r2 檔數 85、位元組 145,944,348 | 本版不含自嵌 ZIP；ZIP 產生在套件**外**，以固定 entry 時戳可重現 | 不適用 |
| D-3 | 交付內驗證報告為 stale green | 出貨檔 2789/0 vs fresh 2788/1 | 報告改由對「與本版位元組相同」的副本實跑後回填，`command` 正規化為相對路徑 | **沒有** |

## 2. 本版實測數字（可重跑）

| 量測 | r2-revision2（凍結） | r3（本版） |
|---|---|---|
| 檔案數 | 85 | 見 `03_TESTS_AND_READBACK/PACKAGE_DENOMINATOR.json` |
| 位元組 | 145,944,348 | 見 `03_TESTS_AND_READBACK/PACKAGE_DENOMINATOR.json` |
| `validate.py` fresh | **2788 / 1**（`SOURCE-BYTES-UNCHANGED`） | **2789 / 0**，rc=0 |
| 連跑兩次 verdict 投影 | n/a | **完全相同**（digest `534fa4c1…`；原始 bytes 只差 `elapsed_ms`） |
| ZIP | 自嵌於套件內 | 套件外、entry 數見同檔；sha256 見套件外 `.zip.sha256`；重建可得**相同 sha256** |

> 本表刻意**不在文字裡複寫** r3 的檔數、位元組與 ZIP sha256：它們由打包步驟實測後寫入
> `PACKAGE_DENOMINATOR.json`，文字只指向該檔。上一版把這些數字寫進說明，結果在加入 HOLD／STAGE
> 兩張表後整段過期（獨立判讀 C1–C7 全 PASS，但把這處列為 finding）—— 這是本版移除的漂移類別。

## 3. 長路徑事實（判讀本版必讀）

本機 Win32 長路徑支援**關閉**：`open()` 在 260 字元後失敗，而本 Subject 的**37/85** 條絕對路徑超過 260
（最長 289 字元）。因此：

- 交付 ZIP 與套件本身沒有問題（解壓後路徑變短）；
- 但 `tools/validate.py` 用 `pathlib`，**必須**在短根（例如 `C:\r20pkg4`）對「位元組完全相同」的副本執行；
- 「在長根就地跑」不是本版的主張，也沒有被宣稱。凍結分母用 Win32 擴充長度前綴（`\\?\`）列舉，並同時斷言
  **檔數**與**最長路徑**，避免 R19 曾發生的 MAX_PATH 截斷誤報（44 檔 vs 實際 85 檔）。

## 4. 重現指令

```bash
# 0) 分母（擴充長度列舉；檔數以 PACKAGE_DENOMINATOR.json 為準，不符即 fail-closed）
python var/R20-FHS-20261029/tools/p0_denominator.py <package_root> DENOMINATOR.json <expected_count>

# 1) 短根副本 + 首次驗證（r3 應為 2789/0）
robocopy <package_root> C:\r20pkg4 /E
cd C:\r20pkg4 && python -B tools/validate.py

# 2) 同一批位元組再跑一次，比對 verdict 投影（不是原始 bytes）
python var/R20-FHS-20261029/tools/p1c_idem.py

# 3) ZIP 可重現性
python var/R20-FHS-20261029/tools/p1e_verify_final.py
```

## 5. 本版**沒有**做的事

1. 沒有放寬 `SOURCE-BYTES-UNCHANGED` 或任何 oracle；29 列是**改 locator，不是改判定**。
2. 沒有動 r2 的任何位元組（含它那份 stale green 報告）。要判讀 r2，請先讀 `VOID_R2_REPORT.md`。
3. 沒有把 46 個 HOLD 說成 PASS；逐格理由見 `HOLD_DISPOSITION.tsv`。
4. 沒有把 18 個 stage 說成已具證；逐列狀態見 `STAGE18_TRACE.tsv`（現況 `EVIDENCED = 0`）。
5. 沒有執行任何 native effect、沒有簽發 Permit、沒有動 `main`、沒有 release。

## 6. 上限與後續

- 本版仍是**作者側**產物；獨立判讀由 VERIFY 車道（不同憑證、fresh context）另行產生，結果另存於回合證據目錄，
  不寫進本套件（避免把 checker 產物當成候選內容自我認證）。
- 149 Child / 386 TECH / 949 R15 的語義債**不在本版範圍**（見 `03_TESTS_AND_READBACK/WORK_REMAINING.md`）。
- 來源仍未正式凍結（`formal_sourcefreeze = HOLD`，9/9 冊）；本版不代簽 SourceFreeze。
