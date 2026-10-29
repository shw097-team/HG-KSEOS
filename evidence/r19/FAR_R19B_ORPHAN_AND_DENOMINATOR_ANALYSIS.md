# FAR-R19B — 三個指控的實測裁決：孤兒成功經驗、非指定模型殘留、假 sandbox 阻斷

> 觸發：OWNER 對 R19 報告三處直接質問。本文件只做一件事：把每一句指控，用可重算的證據判成「對／錯／部分對」，
> 然後給裁決。**本文件推翻 R19 報告三處，其中一處是我自己駁回了正確的挑戰。**
> Status：`RESEARCH_PASS_CANDIDATE`（advisory）｜Subject：`…_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
> 優先序：對齊本包 → Native E2E → 無人值守 → 高必要性 → 不過度治理 → 不過度工程化 → 低阻力 → 高效率

---

## 判決摘要

| # | OWNER 指控 | 判決 | 一句話 |
|---|---|---|---|
| A1 | glm-5.3-flash 不是指定模型，早被刪除，為何出現 | **對（且是我違規）** | 它不在 `model-lane-assignment.json`；我只因 dispatcher 預設吃 **candidate pool**（rev 23）的 rank 3 就用了。它**沒有**被刪除（relay 實測 200），但**未受指派**＝越權使用 |
| A2 | gpt-6.1-sol 已有成功車道，你為何失敗、是否沒讀成功經驗 | **對** | B1 配方一直在 `var/B1-CONT-20261028/receipts/verify_gates_gpt61sol_final2.json`：`--codex-home ~/.codex --allow-human-home-transport`。我用 **sealed home** 打 OAuth 後端 → 401。照配方重跑 **立刻成功**（`ok=true`、`served_arm == required_arm`、205.4s） |
| A3 | sandbox 1223 與車道無關，是已修復的 BUG，為何又踩 | **對（我的歸因錯）** | 1223 只在 **sealed home** 出現（缺 `[windows] sandbox` 宣告/helper）；human home 下 `workspace-write` 正常（B1 與本次都通）。**TT-R19-LANE-SANDBOX 撤回** |
| A4 | （我方自查追加）分母 44 檔 | **我錯** | 真實套件是 **85 檔 / 145,944,348 B**（最長路徑 289 字元）。44 檔是 MAX_PATH 截斷的假象，只覆蓋 8% bytes |
| A5 | （追加）我駁回了挑戰者的 stale-green 指控 | **我錯** | 交付物內的 `static_validation_result.json` 記 **passed 2789 / failed 0**；我讀的是自己複本的即時結果（2788/1）。**挑戰者是對的** |

---

## A1 — glm-5.3-flash 的殘留：是制度缺口，不是模型下架

**證據**
- 權威指派 `config/model-lane-assignment.json`：`PLAN → openai-codex/gpt-6.1-sol`、`EXECUTE → opencode-go/deepseek-v4.1-flash`、`VERIFY_SECURITY → openai-codex/gpt-6.1-sol`。**沒有任何 glm 條目。**
- dispatcher 預設 pool：`scripts/hgk-lane-dispatch.py` `DEFAULT_POOL = config/lane-route-slots.candidate.json`（`status: CANDIDATE`、`rev 23`、round `ROUND-R14-LANE-REBIND-20261022`）；其 `VERIFY_SECURITY.ordered_pool[]` 的 **rank 3 = opencode-go/glm-5.3-flash**。
- 模型**仍存在**：relay `:10101` 對 `opencode-go/glm-5.3-flash` 回真實 completion（`status: completed`，`model: glm-5.3-flash`）。
- 它為何在 pool 裡：registry `history` 留有 owner order **2026-10-15**「PLAN & Orchestrator rebound to opencode-go/glm-5.3-flash because the OpenAI OAuth GPT arm is exhausted」；該 premise 已被後續 order 取代（`status: SUPERSEDED`），但 pool 的 rank 沒有隨指派收斂。

**判決**：模型沒被刪除（OWNER 這半句不成立，有實測）；**我使用它違反指派**（這半句成立）。根因是 **pool 與 assignment 無綁定**：dispatcher 允許 `--force-rank 3` 命中一個指派未列名的 arm。

**修法（不過度治理）**：`--force-rank` 前先比對 assignment；非指派 arm → `ERR_ARM_NOT_IN_ASSIGNMENT` fail-closed。pool 從 assignment 派生，或把 glm 標 `retired_not_mandated` 並刪 rank。

---

## A2 — 成功經驗成孤兒：三個具體原因，不是「沒有成功經驗」

**成功配方（B1 實證，`var/B1-CONT-20261028/receipts/verify_gates_gpt61sol_final2.json`）**

```text
--codex-home C:/Users/user/.codex          # human home（持有 OAuth）
--allow-human-home-transport               # 必須顯式 ack
--relay-base https://chatgpt.com/backend-api/codex
--require-arm openai-codex/gpt-6.1-sol --identity-source codex-rollout
```

**我這次失敗的確切原因**：`--codex-home %LOCALAPPDATA%\HG-KSEOS\codex-hermes`（sealed home，**沒有 OAuth 憑證**）＋ 同一 OAuth 後端 → `401 Unauthorized`。另外我手動 `codex exec` 時加了 `-m gpt-5.6-sol`，把 config 裡預設的 `gpt-6.1-sol` 覆蓋掉，所以拿到錯的模型標籤。

**照配方重跑（本回合實測）**：`ok=true`、`used_rank=2`、`used_transport_model=gpt-6.1-sol`、`served_arm=required_arm=openai-codex/gpt-6.1-sol`、`usage_receipt_ok=true`、205.4s、`subject_mutation.verdict=CLEAN`（44→44，before/after 以 guard 量測）。

**為何變孤兒（三個可修的原因）**
1. **知識位置錯**：配方只存在於回合 receipt 與 registry 的 `arm_aliases.why` 註解，不是可執行預設值。
2. **技能缺 flag**：`hgk-codex-lane-recipe` 寫了 `HGK_LANE_HUMAN_HOME=~/.codex`，但沒寫 `--codex-home ~/.codex` 與 `--allow-human-home-transport`；照技能做仍會 401。
3. **無前置斷言**：dispatcher 不檢查「sealed home + OAuth 後端」這個必然失敗組合，也不檢查 alias 是否已宣告。

**修法**：把配方寫進 dispatcher 預設（OAuth arm 自動選 human home + ack）＋ skill patch ＋ preflight assert（sealed home + chatgpt backend → 直接拒，附正確命令）。

---

## A3 — 1223 不是 lane 缺陷，也不是 sandbox 政策缺陷

| 情境 | 結果 |
|---|---|
| sealed home + `--sandbox workspace-write` | spawn 失敗 `orchestrator_helper_launch_canceled: ShellExecuteExW failed to launch setup helper: 1223`（260s） |
| sealed home + `--sandbox danger-full-access` | `ERR_SANDBOX_ESCALATION_REFUSED`（政策，正常） |
| **human home + `--sandbox workspace-write`** | **正常**：B1 receipt 與本次 gpt-6.1-sol 成功回合都是這個組合 |
| 手動 `codex exec`（human home, workspace-write） | 正常，能逐行引用包內檔案 |

**判決**：1223 是 **sealed home 的 Windows sandbox helper 啟動失敗**（該 home 沒有 `[windows] sandbox` 宣告/helper 路徑；pool 的 `codex_home_config` 已記載這個坑），與「車道能不能用」無關。**撤回 TT-R19-LANE-SANDBOX**；改記 `TT-R19-SEALED-HOME-HELPER`（低嚴重度、有繞道）。

---

## A4 — 分母：44 檔是 MAX_PATH 假象，真值是 85 檔 / 145.9 MB

| 量 | R19 報告 | 實測（robocopy 到 `C:\r19pkg` 後逐檔量測） |
|---|---|---|
| 檔案數 | 44 | **85** |
| 位元組 | 11,664,373 | **145,944,348** |
| 最長相對路徑 | 未被檢查 | **289 字元**（> MAX_PATH 260） |
| 最大單檔 | 未被掃 | `03_TESTS_AND_READBACK/source_keyword_hits.jsonl` **112,296,081 B** |
| 自帶 ZIP | 未計入 | `…_r2-revision2.zip` **13,326,288 B**（包內自嵌） |

**影響**：WP19 supply-chain 的「44 檔、0 secret」只覆蓋約 **8% bytes**，112 MB 的 `source_keyword_hits.jsonl` 從未掃；R18 的 SBOM/WP19 與 `SUBJECT_INTEGRITY` 同病。**這是本回合最嚴重的結論性缺陷**——它讓所有分母失真，而不是讓某個結論失真。

**修法（高必要性、低阻力）**：任何目錄列舉（integrity/SBOM/分母/guard）必須 long-path 安全（`os.walk("\\\\?\\"+abs)` 或 robocopy 到短路徑，或 PowerShell `-LiteralPath`）；列舉後斷言 `files == 期望值` 且 `max_path_len < 260 或已用長路徑 API`，否則 **fail-closed**。guard 的 `files_before/after = 44` 也必須改，否則守衛本身有盲區。

---

## A5 — 我駁回了一個正確的挑戰（最該記的一條）

- 交付物內 `03_TESTS_AND_READBACK/static_validation_result.json`（530,302 B）：`passed 2789 / failed 0`、`scope AUTHOR_STATIC_FIXTURES_ONLY`、`native_execution NATIVE_NOT_RUN`、`elapsed 3.72s`。
- 我在**短路徑複本**即時重跑：`2788 / 1`（唯一失敗 `SOURCE-BYTES-UNCHANGED`）。
- gpt-6.1-sol 挑戰者說「shipped report 是 green、與現況矛盾」→ **成立**。我當時用「我自己產生的複本」去否定「交付物內的檔案」，是拿錯證物。

**判決**：R-3 由 `REJECTED_BY_BYTES` 改為 **`ACCEPTED`**。交付物同時攜帶 **紅（即時可重現）與綠（歷史）** 兩份互斥證據 → 對外部團隊是誤導級缺陷。

**修法**：`r2-revision3` 必須**重新產生** `static_validation_result.{json,md}` 並標註 `supersedes_stale_green`；舊值保留為歷史但明確標 `STALE_DO_NOT_USE`。

---

## 待 OWNER 決策（新增，與 R19 的 D1–D6 併用）

| # | 決策 | 建議裁決 | 理由 |
|---|---|---|---|
| D7 | pool 是否綁定 assignment（非指派 arm fail-closed） | **是** | 這次 glm 越權就是這個缺口；成本 1 個斷言 |
| D8 | B1 配方是否升為預設＋寫進技能 | **是** | 已實測可成功；不做的話下一回合會再撞 401 |
| D9 | 所有列舉改 long-path 安全並 fail-closed | **是** | 44→85 檔的失真比任何結論錯誤都嚴重 |
| D10 | 套件是否移除自嵌 ZIP（13.3 MB） | **是（r3 時）** | 自嵌造成 hash 遞迴與分母膨脹 |
| D11 | `static_validation_result` 重生成並標記舊值 STALE | **是** | 避免外部團隊讀到綠燈 |

---

## 建議執行方案（車道已可用，可無人值守）

| 階段 | 內容 | 車道（實測） | 出口 |
|---|---|---|---|
| P0 | 套件以 long-path 安全方式重新列舉並凍結分母（85/145,944,348） | EXECUTE `opencode-go/deepseek-v4.1-flash`（relay 已通） | `DENOMINATOR.json` 85 檔逐檔 sha256 |
| P1 | 產 `r2-revision3`：29 筆 locator 修復＋重生成 `static_validation_result`＋移出自嵌 ZIP | EXECUTE | `validate.py` 2789/0、舊綠標 STALE、`subject_mutation CLEAN` |
| P2 | 對 P1 做獨立判讀（同一 brief、fresh context） | VERIFY `openai-codex/gpt-6.1-sol`（配方已證：ok=true, 205s） | advisory verdict 落 `DIFFERENTIAL_VERDICT_R19B.json` |
| P3 | dispatcher 加兩個 fail-closed 斷言（assignment 綁定、sealed+OAuth 拒絕）＋ long-path 列舉守衛 | EXECUTE | 負測：故意用 glm rank3 → 拒；sealed+chatgpt → 拒 |
| P4 | （OWNER）D1–D11 裁決；registry 修訂仍建議先補 installer | OWNER | 簽章/提權紀錄 |
| P5 | 交付收束：r3＋兩張表（46 HOLD／18 stage）＋P2 verdict 進 PR #5 | EXECUTE | PR 更新＋attestation 重簽 |

**不做**：不改 `HARD_DENY`、不動 `main`、不 force push、不用非指派 arm、不再以短路徑複本當交付物證物。

## Non-claims

本文件推翻 R19 報告三處並撤回一條 TT；`NATIVE_ADMISSION/0`、`RELEASE/NOT_RUN`、`INDEPENDENT_ACCEPTANCE/NOT_RUN` 不變。P2 的 verdict 僅 advisory。
