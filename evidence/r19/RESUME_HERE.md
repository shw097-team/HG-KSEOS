# RESUME HERE — R19 (round R19-FHS-20261029, continuation of R18)

Written at the end of the R19 session. Read this first; do not re-derive anything below.

## 30 秒狀態

- 回合根：`C:\Projects\Agent_Workspace\var\R19-FHS-20261029`（R19 產物）＋ `var\R18-FHS-SKELETON-SPINE-20261029`（ledger、delegation、R18 收據）
- ledger 26 列：**DONE 6 / PARTIAL 13 / PARKED 7**，`tools/ledger_driver.py --audit` **rc=0**
- 交付：分支 `candidate/r19-fhs-implementation` @ `db88f372`，**PR #5**（base = `candidate/r18-fhs-skeleton-spine-20261029`，92 檔，`mergeable: true`）
- 主體完整性：交付套件 44/44 檔逐位元組一致（`SUBJECT_INTEGRITY.json`）
- 驗證器：`validate.py` 在修好 locator 的隔離副本上 **2789/0**；原封不動的副本 **2788/1**（same defect, 已證明為 stale locator，不是環境漂移）

## 這一回合真正改變的事實

| WP | R18 | R19 |
|---|---|---|
| 18 | repair causality `NOT PROVEN` + 被記成「環境不穩定」 | **causal 證明**：red 2788/1 → 29 個 locator 依 64-hex 全等改寫 → green 2789/0 → 還原 → red。`29/29 relocated, 0 unresolved, 0 name-matched`，oracle 位元組未改 |
| 05 | `HOLD_NO_WRITER_ACK` | 由**原始 writer** `pipd_ls_sp 0.1.1a4` 產出 intent/PI（replay identity PASS）/PD/ECP ＋ 3 個負測；ledger 仍 PARTIAL，因為 signed delegation 把 `LOCAL_DRAFT_WRITE` 列在 deny |
| 19 | 只有 hash inventory | 對**交付套件**重算兩次一致（44 檔、11,664,373 bytes）、0 secret、canary 會響、LICENSE/NOTICE 以 named finding 記錄 |
| 15/16 | 聚合計數、invoked 0 | **80 列 per-ID disposition**（25 methods/24 donors/31 slots），0 個 doc-only 列宣稱 INSTALLED，plugin manifest 現場重算相符（11 個實際 operation） |
| 21 | 引用 50/46/0 | 用 `evaluate()` **重算**：679 checks 0 fail、50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY、27 次真實 CLI process |

## 下一手（照序，最小阻力優先）

1. **Owner step A**：安裝 `var\R19-FHS-20261029\owner_gate\REGISTRY_REVISION_PLAN.json`
   （plan sha256 `0807eba282724591ae5963a59529843d12b2f026f618fe28caf02f1404720202`；
   epoch 34→35；13 個 request digest；exec root `var\R19-NATIVE-EXEC` @ `1f56991d`；
   root_identity `32165637:002d0000000a80e0`）。安裝後 13 列可被 agent 機械執行。
2. **Owner step B**：簽一份修訂 delegation，把 `LOCAL_DRAFT_WRITE`（write-set 限 `var/R19-*/**`）加入 allowlist → 可關 WP-05/07/15/16。
3. **Owner step D**：決定 `main`（`f6dfb1e5`）與 lineage（`190df334`）哪個是 canonical；PR #5 目前只能對 lineage 開。
4. 上述任一完成後：跑 `tools/ledger_driver.py --set ...` 更新列，重跑 `--audit`，第二批證據再上推（新增 commit，不 force）。

## 不要做的事（本回合已驗證的教訓）

- 不要為了讓 `SOURCE-BYTES-UNCHANGED` 變綠而改 `validate.py` 的判準；它是 stale locator，修 locator 就好（本回合做法）。
- 不要把 `expected` 字串當成 leak 證據：PI 的 oracle 定義本來就有 `expected` 欄位（R19 第一輪誤報，已更正為 content_hash 比對）。
- 不要用 `shutil.copytree` 複製含 CJK 長路徑的套件（會 `[Errno 2]`）；用 `tar cf - | tar xf -`。
- 不要用 `--intent <ID>`；`compile-pi` 的 `--intent` 是**檔案路徑**。
- 不要在 `main` 上開 PR：remote `main` 與 lineage 無共同歷史（422）。
- 不要用 owner 簽章宣稱獨立驗收；不要把 `AUTHOR_SIDE` 收據寫成 native。

## 檔案地圖

```
var/R19-FHS-20261029/
├─ FAR_R19_DELEGATION_AND_NATIVE_GAP.md   # 為什麼 13 列是權限不是證據問題 + A/B/C/D 選項
├─ SUBJECT_INTEGRITY.json                 # 44/44
├─ RELOCATION_INDEX.json                  # 29 筆 relocate（舊路徑→新路徑＋sha256）
├─ copy_a_source_manifest.repaired.json   # 修好的 manifest（可重生）
├─ owner_gate/{REGISTRY_REVISION_PLAN.json,REQUEST_DIGESTS.json,OWNER_STEP.md}
├─ receipts/{WP05_PIPD_WRITER_RECEIPT,WP18_CAUSAL_REPAIR_R19,WP19_SUPPLY_CHAIN_R19,WP15_16_ID_LEDGER}.json
├─ pipd_out/                              # 原始編譯器輸出（intent_card/pi/pd/ecp）
└─ tools/{locator_repair_r19,wp05_pipd_writer,wp19_supply_chain,wp15_16_id_ledger,owner_gate_plan}.py
```
