# FAR-R19 研究裁決：殘留／缺口／阻斷的關閉路徑與 OWNER 決策清單

> Decision questions（R0）：Q1 殘留/缺口/阻斷/未關閉項目如何關閉？Q2 哪些待 OWNER 決策？Q3 本包還有哪些未完成項目？
> Owner：本機唯一 OWNER（口令信封 `WIN-254a1c9fbe72`，40 ops，已用 3）｜研究者：Commander/PLAN 車道
> Subject：`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`（44 檔 / 11,664,373 B）
> 裁決優先序（衝突時上位勝）：對齊本包 → Native E2E 閉環 → 無人值守可行性 → 高必要性 → 不過度治理 → 不過度工程化 → 低阻力 → 高效率
> Status：`RESEARCH_PASS_CANDIDATE`（advisory）。非驗收、非 release、非 production。

---

## 1. 分母（全部本回合實測，非引用）

| 量 | 值 | 出處 |
|---|---|---|
| WP-FHS 節點 | 22（SOURCE_READ 5 / HOST_OP 10 / LOCAL_DRAFT_WRITE 4 / REPO_WRITE 2 / RELEASE 1） | `03_TESTS_AND_READBACK/wp_graph.json` |
| ledger 列 | 26（DONE 6 / PARTIAL 13 / PARKED 7），`--audit rc=0` | `var/R18-FHS-SKELETON-SPINE-20261029/ledger.json` |
| 套件自檢 | 2,789 checks；**原樣 2,788/1 FAIL**（`SOURCE-BYTES-UNCHANGED`） | `receipts/WP18_CAUSAL_REPAIR_R19.json` phases[0] |
| 修復後 | **2,789/0**，同一複本可逆證成 | 同上 phases[1..2] |
| 壞 pin | 29 筆（**26** 進 `…\OLD\…`（改名）、**3** 進 `AUDIO` 根層（另一成因）），全部 64-hex 全等改寫 | `RELOCATION_INDEX.json`：rows 172 / in-place 143 / relocated 29 / unresolved 0 |
| 96 格 oracle | 288 assertions：預期 **DENY 192 / PASS_LOCAL_ORACLE 50 / HOLD 46**；27 次真 CLI；`native_case_pass 0` | `receipts/WP21_ORACLE_RERUN_R19.json` |
| WP-15 18 stage | declared 18 / **with evidence 0** | `receipts/WP15_TPM_SPEC_TRACE.json` |
| 15/16 per-ID | 80 列（25 methods / 24 donors / 31 slots），0 個「只引文件就宣稱 INSTALLED」 | `receipts/WP15_16_ID_LEDGER.json` |
| 權限閘 | `authorize()` 在 `REQUEST_SCOPE` 拒；registry rev 34、1 把 owner key、3 互異 SID | `HG-KSEOS/src/hg_kseos/native_admission.py`、`C:\ProgramData\HG-KSEOS\native-admission\registry.json` |
| delegation | 7/22 WP allowlisted；`LOCAL_DRAFT_WRITE` 同時在 `deny` 與 `HARD_DENY` | `governance/delegation_R18_canonical.json`、`tools/delegation_gate.py` |
| 交付 | 分支 `candidate/r19-fhs-implementation`、PR #5、5 commits、101 檔；`main` 無共同歷史（422 實測） | GitHub API |

---

## 2. 研究發現（每條都可被第三方重算）

**F19-1（最高必要性，作者可關）** 交付出去的包**過不了自己的 `validate.py`**：2788/1（失敗 case `SOURCE-BYTES-UNCHANGED`）。根因是 29 筆 `source_manifest.json` locator 失效，且**成因混合**：26 筆被搬進 `\OLD\`（改名），3 筆落在 `AUDIO` 根層路徑（非改名所致）。以 64-hex 全等重定位後 2789/0，還原即回紅。任何外部團隊第一步就撞牆。
**F19-2（權限阻斷，10 列）** 10 個 HOST_OP WP 需要 native PERMIT；`authorize()` 在 `REQUEST_SCOPE` 就拒，且 registry 無 revise 模式（`Enable` 對既有 registry 直接 throw）→ 目前**沒有**可執行的 owner 安裝程序，我只有計畫（`owner_gate/REGISTRY_REVISION_PLAN.json`，13 個 request digest）。
**F19-3（設計阻斷，4 列）** `LOCAL_DRAFT_WRITE` 被**程式碼層** `HARD_DENY` 硬拒；owner 已簽過的修訂版 delegation 也 lift 不了（本回合實測簽章有效但 `REFUSED_CLASS_DENIED`）。
**F19-4（證據缺口，46/96 格）** HOLD 不是失敗，是 fixtures 本身就宣告「本機無校準 Reader／人類判定」；缺的是逐格理由表，不是模型。
**F19-5（宣告漂移，18 stage）** WP 標題含「18Stage」，實測 0/18 有 per-stage 收據 → 名稱的主張大於證據。
**F19-6（語義債，不可在本回合關）** 包的 `WORK_REMAINING.md` 自承：149 Child 無逐 Child oracle、386 TECH/Donor24 未逐 ID 核源、R15 949 需逐域語義反證、629 保留重入承諾。
**F19-7（血統缺陷）** repo `main` 與 lineage 無共同歷史 → PR #5 對 `main` 不可 merge（PR #4 同樣永不可 merge）。
**F19-8（工具缺口）** HGK 缺「既有 registry 的修訂 installer」，是產品級 TT，不是本包缺陷。
**F19-9（原權責阻斷）** ProviderOff label 矛盾、13/14 CLI 原裁決、DOC07↔legacy DOC03 oracle 衝突、risk 12↔context 9 —— 只能由原權責解除，作者不得補造 ACK/Permit。

---

## 3. Q1 — 如何關閉（逐類別，含成本與可無人值守性）

| 類別 | 列數 | 關閉動作 | 權限 | 成本 | 無人值守 |
|---|---|---|---|---|---|
| A. 包自檢紅（F19-1） | 1 檢查 | 以 repaired manifest 產生 `r2-revision3`，重跑 2,789 checks 期望 0 fail，並附 `RELOCATION_INDEX` 逐筆 | 無（作者） | ~1h | ✅ 全自動 |
| B. 46 HOLD 格（F19-4） | 46 cell | 產 `HOLD_DISPOSITION.tsv`：cell / 預期 / 為何 hold / 需要哪個 Reader 才能判 | 無 | ~2h | ✅ |
| C. 18 stage（F19-5） | 18 row | 產 `STAGE18_TRACE.tsv`：stage / 對應 artifact / `EVIDENCED` 或 `ABSENT`（不得補造） | 無 | ~3h | ✅ |
| D. HOST_OP（F19-2） | 10 WP（4 PARTIAL + 6 PARKED） | registry 修訂 → 以 driver 逐列跑，失敗 park 續跑 | **OWNER 提權** | installer + 佇列 | ✅ 修訂後 |
| E. 4 LOCAL_DRAFT（F19-3） | 4 WP | 不改 `HARD_DENY`；ledger 增列 `AUTHOR_COMPLETE` 狀態呈現（additive），如實顯示「工程完成、治理未授」 | 無（但需 owner 認可語義） | ~30m | ✅ |
| F. 149/386/949（F19-6） | 3 群 | 本包 `SCOPED_OUT_WITH_REASON`，移入產品 backlog；不假裝完成 | OWNER 認可 | 0 | — |
| G. 原權責（F19-9） | 4 項 | 交回原權責裁決；作者僅登記 open | 原權責 | 0 | — |
| H. `main`/lineage（F19-7） | 1 | owner 宣告 lineage canonical；`main` 重根另案 | OWNER | 決策 | — |

**關鍵裁決：停止追求「22 個 WP 全綠」。** 分母要說清楚：13 個 PARTIAL 中只有 **4 個 HOST_OP**（02/03/04/17）是權限阻斷，另 4 個是 `LOCAL_DRAFT_WRITE`（工程已完成但狀態無法呈現）、2 個 `REPO_WRITE`、3 個 `SOURCE_READ`；真正純權限阻斷的是 **7 個 PARKED（6 HOST_OP + 1 RELEASE）**。因此 A/B/C/E 四項（作者可關、外部團隊真正消費）在任何權限裁決之前就能落地 —— 這是排序理由，不是報酬率估算；本文件不提供未經量測的 ROI 數字。

---

## 4. Q2 — 待 OWNER 決策（建議裁決 ← 供直接採納）

| # | 決策 | 建議裁決 | 若不採納的後果 |
|---|---|---|---|
| D1 | 是否安裝 registry 修訂（13 digest） | **先補 installer 再安裝**（見 §10 挑戰 R-2）：把 installer＋rollback＋一次乾跑寫進 plan，才做一次性提權 | 10 列永遠停在 PARTIAL/PARKED，本包永無 native 證據 |
| D2 | `HARD_DENY` 是否移除 `LOCAL_DRAFT_WRITE` | **否**（保留）；改採 `AUTHOR_COMPLETE` 呈現 | 為 2 列綠燈拆掉與 `RELEASE`/`main` 同級的硬拒，代價 > 收益 |
| D3 | 交付天花板 | **接受** `candidate-only`，WP-14 RELEASE 維持 PARKED | 需 release 證據鏈，本包無（無獨立驗收、無 promotion） |
| D4 | `main` 與 lineage 誰 canonical | **lineage canonical**；PR #5 即正式交付面 | PR #5/#4 皆不可 merge，交付面懸空 |
| D5 | 46 HOLD 格 | **接受 HOLD 為設計**，加逐格理由表 | 需在無 Reader 情況下硬判，等於造假 |
| D6 | 149/386/949 語義債 | **本包 scope out**，移產品 backlog | 無上限工時，且無外部消費者 |

---

## 5. Q3 — 本包未完成項目（依可交付性排序）

1. **套件自我驗證**：r2-revision2 原樣紅（2788/1）→ 未修（僅在複本修復）。
2. **manifest 正確性**：29 筆 locator 仍錯在交付物內（外部團隊會踩）。
3. **46 格判定理由**：無逐格表。
4. **18 stage 追蹤**：0/18 有證據，且 WP 標題主張 18Stage。
5. **10 個 HOST_OP WP**：需 native PERMIT（未取得）。
6. **4 個 LOCAL_DRAFT_WRITE WP**：工程完成但治理狀態無法反映。
7. **2 個 REPO_WRITE**：WP-18 已 DONE；WP-06 未執行（需 DEV ECP + HGK admission）。
8. **1 個 RELEASE**：WP-14 PARKED（無 release 授權）。
9. **原生證據 subject binding**：本包全部證據為 author-side，無 native admission 收據。
10. **語義債**：149 Child / 386 TECH / 949 R15 / 629 重入（包自承）。
11. **原權責 4 項**：ProviderOff、CLI 13/14、DOC07↔DOC03、risk12↔ctx9。
12. **交付面**：PR #5 未 merge；`main` 血統未裁決。

---

## 6. 建議執行方案（P0–P5，可無人值守，逐階段 exit criteria）

| 階段 | 內容 | 車道 | 出口條件 | 失敗處理 |
|---|---|---|---|---|
| **P0** | 本裁決凍結（此文件）＋ mandate 收據 | PLAN (gpt-6.1-sol) | 本檔 hash 固定、mandate 收據 ok | 重跑一次，仍敗則記錄 `EDITED_NOT_ATTRIBUTED` |
| **P1** | 產 `r2-revision3`：套 repaired manifest（29 筆）＋ 重算全鏈 hash；`validate.py` 目標 2,789/0；連跑兩次同 hash | EXECUTE (deepseek-v4.1-flash) | 0 fail、兩次一致、`SUBJECT_INTEGRITY` 44/44 | 任一不符 → park，publish 失敗面 |
| **P2** | 產 `HOLD_DISPOSITION.tsv`（46 列）、`STAGE18_TRACE.tsv`（18 列） | EXECUTE | 列數 = 46 / 18，全列有 disposition | park |
| **P3** | 對 P1+P2 做**對抗式獨立判讀**（試圖推翻 29 筆 pin、46 列理由、18 列 stage） | VERIFY (gpt-6.1-sol, fresh ctx) | verdict 記錄（advisory；PASS/HOLD 皆接受） | 記 disagreement，不重寫事實 |
| **P4** | （OWNER）registry 修訂 → driver 跑 10 個 HOST_OP 列 | OWNER + EXECUTE | 每列 PERMIT + 收據；失敗 park | 停用該列，續跑下一列 |
| **P5** | 交付收束：`r2-revision3` + 兩張表 + P3 verdict 進 PR #5；`AUTHOR_COMPLETE` 呈現 | EXECUTE | PR 更新、attestation 重簽 | — |

**不做**：不改 `HARD_DENY`、不動 `main`、不 force push、不補造 ACK/Permit、不把 HOLD 當 PASS、不以 149/386/949 的「宣稱」換綠燈。

---

## 7. 授權與簽章建議（一次 load-once 提示可全批）

| 簽章/授權 | 範圍 | 解鎖 | 明確**不**授權 |
|---|---|---|---|
| S1：registry 修訂安裝（提權，非簽章） | 13 digest、policy_epoch 34→35、exec root `var/R19-NATIVE-EXEC` | 10 個 HOST_OP 列 | RELEASE、main、secrets |
| S2：`r2-revision3` 產出授權（delegation 增列 `PACKAGE_REVISION_WRITE`，或由 S1 的 scope 覆蓋） | 只寫 `…_r2-revision3` | P1 | 改 r2 原檔、改 oracle |
| S3：`AUTHOR_COMPLETE` 語義認可（書面裁決即可） | ledger 呈現層 | E 類 4 列 | 不得當 DONE／不得促升 |
| S4：交付面裁決（D4） | repo 血統 | PR #5 可 merge | 不授權重寫 `main` 歷史 |
| S5：release 與否（D3） | WP-14 | — | 建議本次不簽，維持 PARKED |

**建議一句話授權**：「核准 D1–D6 建議裁決；S1 一次性提權安裝、S2/S3 依建議執行；S5 不簽。」

---

## 8. 三車道派工（lane ≠ session）

- **PLAN**：`openai-codex/gpt-6.1-sol`（owner OAuth）— 產出本裁決、凍結分母、裁決建議。
- **EXECUTE**：`opencode-go/deepseek-v4.1-flash`（Codex CLI）— P1/P2/P5 的實際寫入，bounded write-set = `r2-revision3` 與 `var/R19-FHS-20261029/**`。
- **VERIFY/SECURITY**：`openai-codex/gpt-6.1-sol`，fresh context，read-only 對抗式判讀，`--guard-subject` 包住 subject，輸出落在 guard root 之外。
- 三者收據分離，`mandate_gate audit` 必須過；會話（session）模型 `deepseek-v4.1-flash` 與車道模型無關，不得把會話答案升格為車道判定。

## 9. Non-claims

`PRODUCTION/NOT_CLAIMED`、`RELEASE/NOT_RUN`、`NATIVE_ADMISSION/0`、`INDEPENDENT_ACCEPTANCE/NOT_RUN`、`MAIN/MERGED_NO`。本文件是決策建議，不是驗收憑證；P3 的 verdict 亦僅 advisory。

---

## 10. 獨立判讀車道（VERIFY）與 Disagreement ledger

**車道收據**：`scripts/hgk-lane-dispatch.py` 三次派工（rank2 `openai-codex/gpt-6.1-sol` ×2、rank3 `opencode-go/glm-5.3-flash` ×1）全部失敗，兩個不同根因已量測：
- `openai-codex/gpt-6.1-sol` → `401 Unauthorized`（`wss://chatgpt.com/backend-api/codex/responses`），human-home OAuth 對該後端不可用；
- relay `:10101` 目錄中**沒有** `gpt-6.1-sol`（只有 `gpt-5.6-sol`），且 relay 對 `openai-chat` provider 回 `502 non-empty credential required`。

**實際完成判讀的車道**：`codex exec`（human home、`model_provider=desktop_router`、**served model `gpt-5.6-sol`**、113,342 tokens、owner OAuth 付費、nonce 到位）。此為**不同模型家族**，故模型軸獨立性成立；但**不是**指定的 `gpt-6.1-sol`，不得寫成指定車道。

**挑戰結果（advisory）**：`HOLD_ADVISORY`，並推翻本文件兩處：

| # | 挑戰 | 本文件處置 |
|---|---|---|
| R-1 | 29 筆 locator **不是**單一改名成因：26 進 `OLD`、3 進 `AUDIO` | **接受**，已改 F19-1 與分母列 |
| R-2 | 「13 列權限阻斷」把狀態分母當權限分母；且不應在 installer／rollback／native 收據不存在時就核准 D1 | **接受**，已改 §3 尾段與 D1（改為「先補 installer 再安裝」） |
| R-3 | 包內 `static_validation_result.json` 是 stale green（記 2789/0） | **駁回**：實讀為 `passed 2788 / failed 1`，與現況一致。checker 此項誤判，記錄不改事實 |

R-1/R-2 已按證據修訂；R-3 以 bytes 為準駁回。三條全部落在 `DISAGREEMENT_LEDGER_R19.json`。
