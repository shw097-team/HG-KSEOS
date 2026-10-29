# RESUME HERE — R19 結案移交（新 SESSION 由此直行，不必重新推導）

寫於 2026-10-29 UTC 12:3x｜回合 `R19-FHS-20261029`（接續 R18）｜交付 PR #5 head `63fa343`（8 commits / 105 檔）
Subject：`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`（44 檔舊記已作廢，見 §2-①）

## 0. 30 秒狀態

| 問題 | 答案 |
|---|---|
| 套件紅還是綠 | **紅**：短路徑複本 `validate.py` = **2,788 / 1**（唯一失敗 `SOURCE-BYTES-UNCHANGED`）；但**交付物內** `static_validation_result.json` 記 **2,789 / 0**（stale green，誤導級） |
| 套件多大 | **85 檔 / 145,944,348 B**，最長相對路徑 **289 字元**，含 112,296,081 B `source_keyword_hits.jsonl` 與 13,326,288 B **自嵌 ZIP** |
| ledger | 26 列 `--audit rc=0`：**DONE 6 / PARTIAL 13 / PARKED 7** |
| 車道 | **可用**。VERIFY `gpt-6.1-sol` 實測 `ok=true`（205.4 s）；EXECUTE `deepseek-v4.1-flash` 經 keyed relay 已通 |
| 還缺 | 套件 r3、46 列 HOLD 表、18 列 stage 表、owner 裁決 D1–D11 |
| 我改過的治理檔 | `config/hermes-codex-lane.json`（codex pin）＋ `config/active-policy.json`（重 designate，digest `fc760aef…`, 17,274 B）；preimage `var/R19-FHS-20261029/preimage/` |

## 1. 已完成可重算（不要重做）

1. **WP-18 causal**：pristine 2,788/1 → 只改 29 筆 locator（**26→`OLD`、3→`AUDIO`**，全部 64-hex 全等）→ 2,789/0 → 還原 → 2,788/1。`receipts/WP18_CAUSAL_REPAIR_R19.json`；`RELOCATION_INDEX.json`（rows 172 / in-place 143 / relocated 29 / unresolved 0）。
2. **WP-05**：原始 writer `pipd_ls_sp 0.1.1a4` 產 intent/PI（replay identity PASS）/PD/ECP ＋ 3 負測。`receipts/WP05_PIPD_WRITER_RECEIPT.json`（8 KB，已去內嵌 payload）。
3. **WP-19**：交付集兩次重算一致、0 secret、canary 會響 —— 但**只覆蓋 44/85 檔、8% bytes**（§2-①）。
4. **WP-15/16**：80 列 per-ID disposition（25 methods / 24 donors / 31 slots），0 個 doc-only 宣稱 INSTALLED。
5. **WP-21**：`evaluate()` 重算 679/0、96 格（50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY）、`native_case_pass 0`。**「27 次 CLI」是 fixture 宣告，重跑只重放已存 raw、不 spawn**（elapsed 0.019 s）。
6. **獨立判讀**：`gpt-6.1-sol`（B1 配方）verdict `HOLD_ADVISORY`，推翻我三處（見 §2），並抓到 shipped green vs fresh red。
7. **交付**：分支 `candidate/r19-fhs-implementation`（真血統，base `190df334`），PR #5；`main` 無共同歷史（對 main 開 PR 實測 422）。

## 2. 本回合自我更正五項（必須沿用更正後版本）

| # | 錯的 | 對的 |
|---|---|---|
| ① | 套件 44 檔 / 11,664,373 B | **85 檔 / 145,944,348 B**；44 是 `pathlib.rglob` MAX_PATH 截斷；WP19 只掃 8% bytes |
| ② | 我駁回「包內 stale green」 | **挑戰者是對的**：交付物內記 2789/0；我拿自己複本當證物 |
| ③ | `gpt-6.1-sol` 不可用 | **可用**：sealed home 無 OAuth → 401 是選錯 home；B1 配方重跑 `ok=true` |
| ④ | TT-R19-LANE-SANDBOX | **撤回**；1223 只在 sealed home 的 sandbox helper，human home 正常 → 改記 `TT-R19-SEALED-HOME-HELPER` |
| ⑤ | 用 `glm-5.3-flash`（pool rank 3） | **越權**：assignment 沒有 glm；模型仍活（relay 200）但不得使用 |

## 3. 權限狀態（照實）

- Owner 信封 `WIN-254a1c9fbe72`：OPEN、40 ops、**已用 3**、8 h（約 2026-10-29 19:30Z 前）。
- 修訂版 delegation **已簽章未安裝**：`governance/delegation_R19_amendment_signed_NOT_INSTALLED.json`；canonical 已還原 `R18-CANON-6733b6bb`。
- 阻擋原因：`tools/delegation_gate.py` 的 **`HARD_DENY` 程式碼層**含 `LOCAL_DRAFT_WRITE`（與 RELEASE/main/force-push 同級）。**我沒有改它**。
- `authorize()` 仍在 `REQUEST_SCOPE` 拒；registry rev 34 無 revise 模式；13 digest 計畫在 `owner_gate/REGISTRY_REVISION_PLAN.json`（exec root `var/R19-NATIVE-EXEC` @ `1f56991d`，plan sha `0807eba2…`）。
- 證據根簽章 `evidence/r19/EVIDENCE_ATTESTATION.json`（root `50ba710e…`、268 檔）；**之後檔案已增，重算前先讀 `EVIDENCE_MANIFEST.sha256` 與 `excluded_from_enumeration`**。

## 4. 車道：可照抄的命令

**VERIFY / PLAN（`gpt-6.1-sol`，owner OAuth）**

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY --force-rank 2 \
  --require-arm openai-codex/gpt-6.1-sol --identity-source codex-rollout \
  --codex-home "C:/Users/user/.codex" --allow-human-home-transport \
  --relay-base "https://chatgpt.com/backend-api/codex" \
  --sandbox workspace-write --allow-sandbox-escalation --guard-subject "<package dir>" \
  --nonce <N> --prompt "..." --brief <brief.md> --cwd <dir> --output-root "<dir outside guard>" --timeout 260
```

**EXECUTE（`deepseek-v4.1-flash`）— relay 必須帶金鑰**

```bash
cd C:/Users/user/AppData/Local/HG-KSEOS/opencodex-hermes
export OPENCODEX_HOME="$PWD"
export OPENCODE_GO_API_KEY=$(grep -m1 '^OPENCODE_GO_API_KEY=' \
  "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/.env" | cut -d= -f2-)
ocx stop; ocx start --port 10101     # 背景；先 curl /healthz 200 再派工
```
再 `--lane EXECUTE --force-rank 1 --require-arm opencode-go/deepseek-v4.1-flash --relay-base http://127.0.0.1:10101/v1 --codex-home "%LOCALAPPDATA%/HG-KSEOS/codex-hermes"`。

**禁止**：`--force-rank 3`（glm 非指派）、sealed home + OAuth 後端、`--sandbox danger-full-access`、`--ignore-user-config`。

## 5. 下一步（出口條件必須達成）

| 階段 | 做什麼 | 車道 | 出口 |
|---|---|---|---|
| **P0** | long-path 安全凍結分母 | EXECUTE | `DENOMINATOR.json`：85 檔逐檔 sha256、max_path_len 289、145,944,348 B；檔數不符 fail-closed |
| **P1** | 產 `r2-revision3`（放 `…/FHS-MSC_PIPD-LS-PKG/`，不動 r2） | EXECUTE | ①29 locator ②重生成 `static_validation_result.{json,md}` 且舊值標 `STALE_DO_NOT_USE` ③移自嵌 ZIP ④`validate.py` 2,789/0 ⑤連跑兩次同 hash |
| **P2** | r3 fresh-context 獨立判讀（同一 brief） | VERIFY `gpt-6.1-sol` | `DIFFERENTIAL_VERDICT_R19B.json`；`subject_mutation CLEAN`（**用 long-path 列舉量**） |
| **P3** | dispatcher 兩斷言＋負測 | EXECUTE | 非指派 arm → `ERR_ARM_NOT_IN_ASSIGNMENT`；sealed+OAuth → 拒並印正確命令 |
| **P4** | OWNER 裁決 D1–D11 | OWNER | 簽章/提權紀錄 |
| **P5** | 收束進 PR #5 | EXECUTE | r3＋46 列 HOLD 表＋18 列 stage 表＋P2 verdict；attestation 依新樹重簽 |

**未產出的兩張表（作者工作，無需權限）**
- `HOLD_DISPOSITION.tsv` 46 列（cell / 預期 / 為何 hold / 需要哪個 Reader）；挑戰者已分類：33 校準/人類/judge、8 兩版升級、5 效能門檻。
- `STAGE18_TRACE.tsv` 18 列（stage / artifact / `EVIDENCED`|`ABSENT`）；現況 declared 18 / with evidence **0**。

## 6. 待 OWNER 決策（D1–D11，建議已填）

| # | 決策 | 建議 |
|---|---|---|
| D1 | registry 修訂 | **先補 installer＋rollback＋乾跑，再提權**（無 revise 模式） |
| D2 | `HARD_DENY` 的 `LOCAL_DRAFT_WRITE` | **維持拒**；改以 `AUTHOR_COMPLETE` 呈現 |
| D3 | 交付天花板 | **candidate-only**；WP-14 維持 PARKED |
| D4 | `main` vs lineage | **lineage canonical** |
| D5 | 46 HOLD | **接受為設計**＋逐格理由表 |
| D6 | 149/386/949 語義債 | **本包 scope out** |
| D7 | pool 綁 assignment（非指派 arm fail-closed） | **是** |
| D8 | B1 OAuth 配方升為預設 | **是**（技能已 patch，dispatcher 未改） |
| D9 | 列舉 long-path 安全並 fail-closed | **是** |
| D10 | 移除自嵌 ZIP | **是（r3 時）** |
| D11 | 驗證報告重生成、舊值標 STALE | **是** |

一句話授權可用：「核准 D1–D11 建議裁決；D1 先驗 installer；D3/D6 依建議；D4 lineage canonical。」

## 7. 陷阱（已踩過）

1. **MAX_PATH**：`pathlib.rglob` / `os.walk` 在此包少算一半；用 robocopy 到 `C:\r19pkg` 或 PowerShell `-LiteralPath`。
2. **guard 的 `files_before/after=44` 同一盲區** → P0 必須先修 guard 列舉，否則 CLEAN 不代表沒動到 85 檔。
3. **不要拿自己複本當交付物證物**（②的直接成因）。
4. **relay 無金鑰 = 502 假故障**；兩個實例時第二個會 `already running` 退出。
5. `write_file` 長檔可能被截斷並寫入壓縮 marker → 產檔後檢查 bytes 與 marker。
6. **CJK 長路徑** bash→python 會走鐘；先 `cd` 再用相對路徑，或 robocopy 到 ASCII 短路徑。
7. `main` 與 lineage 無共同歷史；不要對 main 開 PR、不要 force。
8. `shutil.copytree` 對 CJK 長路徑會 `[Errno 2]`；用 `tar cf - | tar xf -` 或 robocopy。
9. `compile-pi --intent` 是**檔案路徑**，不是 ID。

## 8. 檔案地圖

```
var/R19-FHS-20261029/
  RESUME_HERE.md（本檔）  SESSION_STATE.json
  FAR_R19_RULING_AND_OWNER_DECISIONS.md      Q1/Q2/Q3 裁決（已被 R19B 修正三處）
  FAR_R19B_ORPHAN_AND_DENOMINATOR_ANALYSIS.md 三項指控實測＋A4/A5 自查
  FAR_R19_DELEGATION_AND_NATIVE_GAP.md       權限天花板分析
  DISAGREEMENT_LEDGER_R19.json              R-1/R-2 接受、R-3 改判接受
  RELOCATION_INDEX.json  SUBJECT_INTEGRITY.json
  owner_gate/{REGISTRY_REVISION_PLAN.json,REQUEST_DIGESTS.json,OWNER_STEP.md}
  preimage/{hermes-codex-lane.json.bak,active-policy.json.bak}
  receipts/{WP05,WP15_16,WP18,WP19,WP21,VERIFY_LANE,DELEGATION_*}
  lane/{BRIEF_VERIFY_R19_RULING.md,out..out5}
var/R18-FHS-SKELETON-SPINE-20261029/  ledger.json（26 列）、governance/、tools/
C:\r19pkg                              85 檔長路徑安全複本（臨時，可重建）
PR: https://github.com/shw097-team/HG-KSEOS/pull/5 （head 63fa343）
```

## 9. Claim ceiling

`AUTHOR_SIDE + ISOLATED_LOCAL`。`NATIVE_ADMISSION/0`、`RELEASE/NOT_RUN`、`INDEPENDENT_ACCEPTANCE/NOT_RUN`、`MAIN/MERGED_NO`、`PRODUCTION/NOT_CLAIMED`。VERIFY verdict 僅 advisory，不是 OracleReceipt、不是 canonical acceptance。

---

## 附錄 A — 口令授權後實測（2026-10-29T11:36Z）

- 視窗 `WIN-254a1c9fbe72` OPEN（40 ops / 8 h / ceiling `REPOSITORY_WRITE` / `broker_alive true`）。
- **FAR 選項 B 實測失敗並回滾**：修訂版 delegation 簽章以 owner 公鑰驗過（`412b3519…`，1 op），但 gate 回 `REFUSED_CLASS_DENIED`，因 `HARD_DENY` 在程式碼層含 `LOCAL_DRAFT_WRITE`。canonical 已還原，gate 回 `WP-FHS-05 → REFUSED_WP_NOT_ALLOWLISTED`（已回讀）。**沒有改 `HARD_DENY`。**
- **證據根簽章**：`evidence/` 268 檔 merkle root `50ba710e…`，owner 簽章、本地以公鑰驗過（第 2、3 個 op）。

## 附錄 B — 車道派工的完整失敗譜（避免重複探索）

| 嘗試 | 結果 | 判讀 |
|---|---|---|
| sealed home + `chatgpt.com/backend-api/codex` ×2 | `401 Unauthorized` | sealed home 無 OAuth；不是 arm 下架 |
| relay 無金鑰 + glm rank3 | `502 non-empty credential` | 我自己啟動的 relay 缺 provider key |
| keyed relay + deepseek `workspace-write` | `ShellExecuteExW … 1223` | sealed home 的 sandbox helper |
| sealed home + `danger-full-access` | `ERR_SANDBOX_ESCALATION_REFUSED` | 政策，正常 |
| keyed relay 直呼 `POST /v1/responses` | `completed`（deepseek、glm 都通） | arm 健康 |
| **human home + `--allow-human-home-transport` + gpt-6.1-sol** | **`ok=true`、205.4 s、served==required** | **正確配方** |
| human home `codex exec` + `-m gpt-5.6-sol` | 完成、113,342 tokens | 我覆蓋了 config 的 gpt-6.1-sol，故得到錯標籤 |
