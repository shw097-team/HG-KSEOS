# FAR — 殘留／缺口／阻斷的關閉方案、升格與 MAIN 併入裁決（R20-FHS-20261029）

機械可讀版本：`var/R20-FHS-20261029/receipts/CLOSURE_PLAN.json`（逐項 id／lane／model／驗證命令／ceiling）

研究對象：`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`（凍結輸入）
交付物：`…_r2-revision3.zip` `ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f`
治理三角：**Fabric＝治理契約**、**SBL＝產品工程指揮入口**、**HG-KSEOS＝原生授權／狀態／驗收控制平面**
本文性質：**裁決研究（可執行方案）**，不是驗收；本文任何數字都可重跑，任何「未簽」項目都不計為 PASS。

---

## 0. 三句話裁決

1. **「96 cells 全綠 + 18 stages 有證 + owner 驗收」在現行權責下不可由 agent 達成**；可達的是
   `AUTHOR_SIDE_ALL_GREEN`（本回合可完成）＋ `OWNER_ACCEPTED_LOCAL`（需 8 個簽章事件）。
2. **殘留不是 46+18+11 個問題，而是 5 類 Reader 資格 + 3 個 Stage Owner + 5 類外部權責**。逐項開 ticket
   是過度治理；依 Reader 類別批次簽核才符合「低阻力、不過度治理」。
3. **r18/r19 與 `main` 無共同祖先**（merge-base rc=1），直接併 main 會把 941 檔／214 commit 以
   unrelated-histories 灌進去。低阻力替代＝自 main 建 `publish/r20-subset`（207 檔）再開 PR。

---

## 1. 治理依據（SBL 逐條，file#line）

| 依據 | 條文要旨 | 對本文的作用 |
|---|---|---|
| `SBL_PIPD-LS-PKG_DOC-00.md:1557` | `FORMAL_SOURCE_FREEZE=HOLD, PI/PD=NOT_COMPILED, NATIVE_EFFECT=NOT_RUN, INDEPENDENT_CHECKER=NOT_PERFORMED, RELEASE=NOT_PERFORMED`；所有衝突保持 Open 直到指定合法 Owner 裁決 | 定義 claim ceiling 與「不得自我關閉」 |
| `SBL_PIPD-LS-PKG_DOC-00.md:1582` | N11/N14 未經 Owner 裁決 → `DOC_ROUTE_HOLD`，可讀但**不得 promotion**；缺件保留獨立 TT；必要時只停受影響子流程，**不用放寬 Gate** | 升格與 MAIN 併入的鐵律；也是「不得家族級 waiver」的來源 |
| `SBL_PIPD-LS-PKG_DOC-00.md:1546` | TT-003 由 SBL Doc Owner 以 **signed ChapterRegistry/supersession** 關閉 | 簽章物形式（本文 OR 包即照此格式） |
| `SBL_PIPD-LS-PKG_DOC-00.md:504` | M09 Review：**自簽不能算獨立** | 排除「maker＝checker」；OR-6 必須不同 principal |
| `SBL_PIPD-LS-PKG_DOC-01.md:4906` | 本節**不是獨立驗收報告**；`AUTHOR_SIDE` 只反映語法/ID/ABI；**檔案文字替代不能自動關閉任一 Fxx 的獨立驗收** | 為什麼 2789/0 不等於驗收 |
| `SBL_PIPD-LS-PKG_DOC-01.md:4936` | 複合子義務再開條件（Owner 否決一原子、orphan hash、License/Pin 缺證、Host 缺原始 receipt…）需 first-fail 開 TT，其餘不受影響者保持可用 | 關閉路徑要「逐 scope」，不是整體重來 |
| `SBL_PIPD-LS-PKG_DOC-02.md:10567` | C51.4：**關閉 TT 須真正 Owner Receipt**＋同 subject 原始證據＋重驗＋變更指向先前 ticket；否則 `OWNER_RECEIPT_MISSING` | 本文 OR 包的驗收形式 |
| `SBL_PIPD-LS-PKG_DOC-02.md:10643` | DOC-12 DELIVER manifest/claim ceiling：**release gate 只有 Owner 可核發** | 為何本計畫止於 Phase 4/5，不碰 release |
| `SBL_PIPD-LS-PKG_DOC-04.md:569` | C8 Evidence and claims：raw receipts、SoD、invalidation、claim ceiling；`CROSS_SUBJECT_HASH` 由 Native/Checker 判 | 證據契約（我們的 receipts 已照此） |

三角色對映（不新增治理層）：
**Fabric** 提供 `EvidenceAndClaimContract` / claim ceiling 形式（DOC-04 C8）→ 本計畫的 receipt 已符合；
**SBL** 是產品工程指揮入口（DOC-00..13 與 `WORK_REMAINING.md` 四項產品工作）→ 決定「哪些算完成」；
**HG-KSEOS** 是原生控制平面（lane/assignment/admission/kanban）→ 決定「誰能跑、跑過什麼、憑什麼」。

---

## 2. 現況量測（全部可重跑）

| 項 | 值 | 來源 |
|---|---|---|
| 交付 archive | `ee009117…`，13,578,117 B，89 entries，重建 byte-identical | `receipts/P1D_R20B_CHECKSUM_REPAIR.json` |
| validator（shipped bytes） | **2789 passed / 0 failed** | `receipts/P1C_IDEMPOTENCE.json` |
| checksum 清單 | **88/88** 驗證通過（修復前 1 列過期） | 同上 |
| 閘門測試 | 9 passed；全套 **145**（改動前 136） | worktree pytest（**AUTHOR_SIDE_MEASURED**：唯讀 checker 不可執行） |
| Oracle cells | `PASS_LOCAL_ORACLE 50 / HOLD 46 / DENY 0` | `03_TESTS_AND_READBACK/oracle96_verification_v2.json` |
| HOLD 分類 | CALIBRATION 11・HUMAN_DECISION 11・HUMAN_JUDGE 11・TWO_VERSION 8・PERFORMANCE 5 | `HOLD_DISPOSITION.tsv`（46 列） |
| Stage 軌跡 | **18/18 `ABSENT`**；owner 只有 3 位（ProductOwner 6・ArchitectureOwner 6・ProgramOwner 6，各 T0–T5） | `STAGE18_TRACE.tsv` |
| 套件自帶 holds | **11 筆**：SOURCE 2・ABI 4・HOST 3・CHECKER 1・RELEASE 1 | `03_TESTS_AND_READBACK/holds.json` |
| 產品未完成工作 | 4 項（149 Child oracle／386 TECH-Donor24／R15 949／真實外部缺口） | `WORK_REMAINING.md` |
| repo | `main` 4 commits（root `a2389c13`）；`r19` 214 commits（root `ec58a0be`）；**merge-base rc=1（無共同祖先）** | git |
| 樹差 | origin/main↔r19：**941 檔 +121,019 / −5,438**（evidence 313・openspec 169・eval 94・tests 81・scripts 71・control 60・profiles 43…） | git |
| 窄子集 | `scripts+config+tests+evidence/R20+docs` = **207 檔 +42,745 / −723** | git |
| 分支關係 | `r18 ⊂ r19`；`openspec-only` 自 main `f6dfb1e`（11 commits, 81 檔）**不在** r19 內 | git |
| PR | #5 open `r19 → r18`（base 不是 main）；#4 open `openspec-only → main`；#1/#2 open（b1 lineage）；#3 merged | GitHub API |
| 設定漂移 | 主機 `assignment` rev 36（epoch 36）vs 本分支 rev 35（epoch 34）：PLAN/VERIFY 的 `transport_model` → `gpt-6.1-sol` | `EVIDENCE_INDEX §6b` |
| 車道選路實測（本回合） | 以 `--require-arm openai-codex/gpt-6.1-sol` 且**不加** `--force-rank` 派工 → 實際 served `desktop_router/opencode-go/deepseek-v4.1-flash`（rank 1），呼叫**已花掉**（350.27s）後才以 `ERR_REQUIRED_ARM_NOT_SERVED` 拒收 | `lane/far_verify_stdout.json` |
| nonce 對照（本回合） | 無 `--guard-subject` 的兩次派工 **皆** `nonce_present=true`／`nonce_present_raw_stdout=true`；先前三份 false 皆帶 `--guard-subject`（指向 13.5 MB archive） | `lane/far_verify_stdout.json`、`EVIDENCE_INDEX §6c` |

**判讀**：`--require-arm` 目前只做「事後否決」，不是選路約束 → 要拿到指定車道模型仍必須 `--force-rank`（pass 2 的
`used_rank=2` 就是這樣成功的）。這正是 owner 提醒的「車道模型 ≠ 會話模型」風險的機械版本：**必填 arm 卻先打錯模型，
才事後拒收**。列為 TT-R20-11／A8。

### 2b. 本回合的獨立 VERIFY 回合（已回条化，advisory）

派工：`--lane VERIFY_SECURITY --force-rank 2 --require-arm openai-codex/gpt-6.1-sol --identity-source codex-rollout`
（OAuth relay，owner 登入 home + `--allow-human-home-transport`）。
回条：`ok=true`、`served_arm = required_arm = openai-codex/gpt-6.1-sol`、`used_rank=2`、136.93s、
`nonce_present=true`、`nonce_present_raw_stdout=true` → `var/R20-FHS-20261029/lane/far_verify2_stdout.json`。

判讀（`lane/FAR_CHALLENGE_20261029.json`，**overall = HOLD**，6 PASS / 4 HOLD）：

| claim | 結果 | 說明 |
|---|---|---|
| C1 archive sha | PASS | 獨立重算相符 |
| C2 bytes/entries | PASS | 13,578,117 / 89 / 0 directory / 0 CRC 錯 |
| C3 validator 2789/0 | **HOLD** | 唯讀沙箱無法在新鮮解壓上執行 validator → 不可測即 HOLD（正確行為） |
| C4 checksum 88/88 | PASS | 88 列、88 驗證、0 mismatch、0 self-reference |
| C5 HOLD 46 分類 | PASS | CALIBRATION 11 / HUMAN_DECISION 11 / HUMAN_JUDGE 11 / TWO_VERSION 8 / PERFORMANCE 5 |
| C6 stage 18 | PASS | 18 列全 ABSENT；ProductOwner 6 / ArchitectureOwner 6 / ProgramOwner 6 |
| C7 holds 11 | PASS | SOURCE 2 / ABI 4 / HOST 3 / CHECKER 1 / RELEASE 1 |
| C8 repo 拓樸 | **HOLD** | 見下：**本機沒有 `main` ref**，`git merge-base main …` 回 rc=128；改用 `origin/main` 才回 rc=1 |
| C9 樹差 941/207 | **HOLD** | 同上（rc=128）；以 `origin/main` 重算，941 與 207 的 +/− 數字相符 |
| C10 閘門 9 passed | **HOLD** | 唯讀沙箱不能跑 pytest（需要 temp 目錄）→ 只能數到 9 個 test function |

**兩個 disagreement 是我的文件缺陷，不是 checker 的錯**：我把重現命令寫成 `main`，但這個 clone 只有
`origin/main`（`main` 不存在 → rc=128）。已全文改為 `origin/main`。
**另一個教訓**：`9 passed` 是作者在本機跑的數字，唯讀 checker 不可重現 → 這類數字要標 `AUTHOR_SIDE_MEASURED`，
不可寫成好像任何讀者都能重跑。

---

## 3. 殘留清單與關閉方式（逐項，含驗證命令）

### A. 機器可關閉（不需 owner，本回合可做完）

| ID | 殘留 | 動作 | 驗證命令 | 車道 |
|---|---|---|---|---|
| A1 | TT-R20-8：裸 `pytest tests` 2 個 collection error | 修 import/collect（不修測試語義） | `PYTHONPATH=src python -m pytest tests -q --collect-only \| tail -2` | EXECUTE |
| A2 | TT-R20-9：receipt 的 `nonce_present_raw_stdout` 與自身 bytes 矛盾 | receipt 加 `producer_revision`；把「非 final agent_message 的 nonce」記為 `nonce_present_anywhere`（語義分離，不放寬 `ok`）；跨版本比較一律拒絕 | stub 對照：`HGK_STUB_EMIT_NONCE=<nonce>` → `nonce_present=true`；`pytest tests/test_lane_dispatch_r20_gates.py -q` | EXECUTE |
| A3 | TT-R20-10：主機 rev36／repo rev35 | 產生 `CONFIG_DRIFT.json`（逐欄 diff、受影響 lane、是否影響已出證據），**不回填證據** | `python tools/config_drift.py --repo-rev 35 --host-rev 36` → `same=false, fields=2, affects_issued_evidence=false` | EXECUTE |
| A4 | TT-R20-6 機械半：assignment 無 `fallbacks` 欄位 | schema 加 `fallbacks[]`；strict 只約束「首選 arm」，fallback 需顯式 `alternates_are_operator_selectable` | `pytest tests/test_lane_assignment_fallbacks.py -q` | EXECUTE |
| A5 | 交付未落 main | 自 main 建 `publish/r20-subset`（207 檔），附 `SUBSET_MANIFEST.json`（逐檔來源 commit）；不 force、不動 main | `git diff --shortstat origin/main...publish/r20-subset` = `207 files, 42745 insertions(+), 723 deletions(-)` | EXECUTE |
| A6 | owner 決策包不存在 | 依 §4 產 8 份 `owner_requests/OR-0x.{json,md}`（逐 ID、逐 cell、可勾選、附驗證命令） | `python tools/render_owner_requests.py --check` → 8 包、0 缺欄 | EXECUTE（PLAN 定稿內容） |
| A7 | 文件數字與 receipts 可能漂移 | `tools/evidence_reconcile.py`：讀 receipts → 斷言 EVIDENCE_INDEX 內每個數字 | `python tools/evidence_reconcile.py` → `mismatches=[]` | EXECUTE |
| A8 | **TT-R20-11**：`--require-arm` 不是選路約束，只在呼叫後否決（本回合實測：指定 gpt-6.1-sol 卻先打 rank 1 deepseek，350.27s 已花） | 在選路**之前**以 required/assigned arm 過濾 pool；正規化 rev36 alias（`gpt-6.1-sol` ≡ `openai-codex/gpt-6.1-sol`）；無解則 pre-spawn typed refusal | 不帶 `--force-rank` 派工 → 必須 served 指定 arm 或於 **spawn 前**拒收 | EXECUTE |

### B. 需 OWNER 簽章（8 個事件；每個都附「不簽會怎樣」）

| OR | 簽署者 | 範圍 | 簽什麼 | 不簽的後果 |
|---|---|---|---|---|
| OR-1 | ProductOwner | `PM:T0–T5` 6 stages | 發佈 6 個 `@1` output artifacts，或逐 stage typed waiver | 6/18 stage 保持 ABSENT |
| OR-2 | ArchitectureOwner | `SE:T0–T5` 6 stages | 同上 | 同上 |
| OR-3 | ProgramOwner | `TPgM:T0–T5` 6 stages | 同上 | 同上 |
| OR-4 | 受保護 Calibration Reader 指派人 | 11 cells（CALIBRATION） | Reader 身分＋來源校準值 bytes（SHA 釘定） | 11 cells HOLD |
| OR-5 | Owner（人類決策） | 11 cells（HUMAN_DECISION） | 逐 cell 判定值（可一次批次簽＋逐 cell 值） | 11 cells HOLD |
| OR-6 | 第二 principal（≠ maker） | 11 cells（HUMAN_JUDGE） | SoD 宣告＋判定（自簽不算，DOC-00:504） | 11 cells HOLD |
| OR-7 | 前後版 Reader 綁定人 | 8 cells（TWO_VERSION） | 兩版 Reader id＋版本 hash | 8 cells HOLD |
| OR-8 | 5 類外部權責 | 11 筆套件 holds（SOURCE2/ABI4/HOST3/CHECKER1/RELEASE1） | 逐 ID 回覆或 supersession（DOC-00:1546 形式） | 11 holds 全開 |

**PERFORMANCE 5 cells 的特別裁決**：無 bound threshold，重跑不會改變結論。建議由 OR-5 內附一個
**明確 waiver**（`PERFORMANCE_UNOBSERVED` 接受聲明），而不是偽造一個 threshold——這符合 DOC-00:1582
「不放寬 Gate」，因為 waiver 是具名的、可撤銷的，且 claim ceiling 維持。

### C. 需外部權責（agent 不得代簽、不得代造）
真 Host／Repo／Protected Checker／Publisher 的 raw receipts；`CR-ORACLE-001`（DOC-07 ↔ DOC-03 法位，
DOC-00:1549）；`N11/N14` 分冊裁決（DOC-00:1546）。**未裁決前**：`DOC_ROUTE_HOLD`，可讀不得 promotion。

### D. 正確地「不關閉」
46 HOLD cells 與 18 stages 不得以文件名詞替代、不得以作者推論升格（DOC-01:4906）。
把它們關閉＝造假；把它們**編號、分類、指定 reader、給下一步合法動作**＝本輪已完成的處置。

### E. 產品層四項（`WORK_REMAINING.md`）的處置
| 項 | 現況 | 可關閉性 | 建議 |
|---|---|---|---|
| 149 Child 逐 child oracle | 有 Parent 原句＋域 POS/NEG＋設計欄檢查；**多數無可執行 domain oracle** | 機器可擴充，但語義需 Clause Owner | 逐 child 產生 fixture 骨架（96→149 擴充），語義判定留 OR-5 |
| 386 TECH / Donor24 | 有原名/處置/recipe；缺 per-ID source/version/license | 部分可由來源解析 | 先做「可解析者」批次（機器），其餘轉 OR-8 |
| R15 949 atoms | 已真來源逐段比較；Required66/Conditional254 的 trigger 待語義反證 | 語義工作 | 629 保持 Full Product 重入承諾，不冒充完成 |
| 真實外部缺口 | ProviderOff label 矛盾、13/14 CLI Owner 裁定、Oracle 法位、12risk↔9context、Native evidence binding、真 Runner/Checker/Publisher | **不可** | 全部併入 OR-8 與 §C |

---

## 4. 「ALL PASS」的正確重述（三層目標，別混用）

| 層 | 名稱 | 定義 | 現況 | 誰能給 |
|---|---|---|---|---|
| T1 | `AUTHOR_SIDE_ALL_GREEN` | validator 2789/0 + checksum 88/88 + 重建決定性 + 閘門 9/9 + 裸 pytest 全綠 + 證據數字自動對帳 0 mismatch | **已達 4/6**（validator／checksum／決定性／閘門），缺 A1（裸 pytest 全綠）與 A7（自動對帳） | agent（本回合） |
| T2 | `OWNER_ACCEPTED_LOCAL` | T1 + OR-1..7 簽章 + 46 cells 逐項處置（含 PERFORMANCE waiver） | NOT_RUN | OWNER |
| T3 | `EXTERNAL_ACCEPTED` / `RELEASE` | T2 + OR-8 + 真 Host/Checker/Publisher receipts + release gate | NOT_RUN | 外部權責（DOC-02:10643） |

**因此「全部實際完成達成 ALL PASS」的正確答案是**：先把 T1 收乾淨（A1–A7），把 T2 壓成 8 個簽章事件，
T3 對外發 5 封請求。宣稱 T2/T3 完成而無簽章＝違反 DOC-02:10567（`OWNER_RECEIPT_MISSING`）。

---

## 5. 升格裁決（候選項目已檢測：哪些可升格實用）

| 候選 | 建議 | 理由 | 前置 |
|---|---|---|---|
| `HOLD_DISPOSITION.tsv`(46) + `STAGE18_TRACE.tsv`(18) | **立即升格**為 `DISPOSITION_REGISTRY@1` | 純機械推導、可重跑、不含判定；外部團隊可據此排工 | 無 |
| dispatcher 5 個 gate codes（含 `ERR_CODEX_EXECUTABLE_NOT_FOUND`） | **升格為程式碼基線**（走 code review，不走 acceptance） | 有 9 個測試與負測；與套件驗收無耦合 | PR 合併核准（owner 按 merge） |
| `…_r2-revision3.zip` | **條件升格**：先給外部工程團隊作 `EXTERNAL_DEV_BASELINE`（可開發、不可驗收），OR-1..7 簽後升 `OWNER_ACCEPTED_LOCAL` | T1 已達、T2 未達 | OR-1..7 |
| 46 HOLD cells | **不升格** | 無 Reader；文件替代不能關閉（DOC-01:4906） | OR-4..7 |
| 18 stages | **不升格** | 無 artifact，狀態就是 ABSENT | OR-1..3 |
| 11 套件 holds | **不升格** | 屬外部權責 | OR-8 |
| `CONFIG_DRIFT`（rev35→36） | 升格為 **known state**（記在校準清單，不回填證據） | 主機已動，證據釘舊版才誠實 | A3 |

---

## 6. MAIN 併入裁決（分支已檢測）

| 分支 / PR | 觀察 | 裁決 | 低阻力做法 |
|---|---|---|---|
| `candidate/r18-openspec-only`（PR #4 → main） | 自 main `f6dfb1e`，11 commits、81 檔、docs+evidence、**不在** r19 內 | **建議併入 main**（唯一血緣乾淨者） | owner 按 merge；不需 rebase |
| `candidate/r19-fhs-implementation`（PR #5 → **r18**） | 與 main **無共同祖先**；樹差 941 檔；#5 base 是 r18 不是 main | **不得直接併 main**；保持 stacked 作 lineage | 併 #4 後，以 `publish/r20-subset`（自 main、207 檔、+42,745）另開 PR；#5 待 owner 以 receipt 標 superseded（DOC-02:10567） |
| `candidate/r18-fhs-skeleton-spine-20261029` | 是 r19 的祖先；同樣無 main 血緣 | 不單獨併 | 同 r19 路徑 |
| `codex/b1-r5-native-admission`（PR #1）、`codex/b1-r6-artifact-scope`（PR #2） | 無共同祖先（rc=1／不可解析） | 不建議直接併 | 若 main 需要該修補，replay `src/hg_kseos/native_admission.py` + 相關 tests 到自 main 的分支 |
| `b1/closure-20261028` | 已 merged（PR #3） | 已完成 | — |

**為何不用 `--allow-unrelated-histories`**：會把 214 個 commit 與 941 檔（含 openspec 169、eval 94、
control 60、profiles 43）一次灌進只有 4 commit 的 main，review 不可行、rollback 不可行、且違反
「低阻力、高效率」。**subsets replay 是同一目的的低風險等價做法**，且每一步都可被外部團隊逐檔驗。

---

## 7. 建議執行方案（三車道，模型照 owner 指定）

| Phase | 車道 | 模型 | 內容 | 完成判準 | 停止條件 |
|---|---|---|---|---|---|
| P1 | **EXECUTE** | `opencode-go/deepseek-v4.1-flash`（Codex CLI） | A1、A2、A3、A7、A8（純機械，無 owner 依賴；A6 由 PLAN 定稿） | T1 六項全綠；`evidence_reconcile` 0 mismatch；8 份 OR 包可勾選 | 任一項驗證紅 → 停在該項並回報，不跨項 |
| P2 | **VERIFY** | `openai-codex/gpt-6.1-sol`（Codex CLI，OAuth） | 對 P1 逐項反證（含 archive 三不變量重算、gate 負測、OR 包欄位完整性） | verdict ≥ PASS_WITH_FINDINGS 且每項有 counter-evidence | 反證成立 → 退回 P1，不放寬 |
| P3 | **EXECUTE** | deepseek | A4（fallback schema）＋ A5（`publish/r20-subset`） | `pytest` 全綠；subset 207 檔、manifest 可逐檔追溯 | 任何檔案無來源 commit → 停止 |
| P4 | **OWNER** | — | OR-1..8 簽章（含 PERFORMANCE waiver） | 8 份 receipt 落 `_handover/.../owner_receipts/` | 任一未簽 → T2 不成立 |
| P5 | **VERIFY** | gpt-6.1-sol | 以 owner receipts 重跑受影響 gates；產 `ACCEPTANCE_RECORD.json` | 只對「已簽 scope」給 PASS；未簽 scope 保持 HOLD | 不得以部分簽章宣稱 T2 |
| P6 | **PLAN** | gpt-6.1-sol | M1（#4 併 main）與 M2（subset PR）之裁決與 PR body | PR 可審、可回滾 | release/tag 一律不做 |

工作量估計（不誇大）：P1 ≈ 半日（機械）、P2 ≈ 1 次車道回合、P3 ≈ 半日、P4 = owner 時間（並行）。

---

## 8. 為什麼這樣「不過度治理、不過度工程化」

1. **不新增治理層**：沿用既有 KANBAN board、FAR、`_handover` 與 lane receipt 格式；不開新 spec、不開新 control plane。
2. **不逐項開 ticket**：46+18+11 壓成 8 個簽章事件（3 stage owner + 5 reader/外部類），符合 DOC-01:4936 的 first-fail scope 原則。
3. **不改證據去迎合現況**：rev 35/36 漂移只記錄、不回填（DOC-01:4906 精神）。
4. **不碰 release/tag/main**：release gate 屬 owner（DOC-02:10643）。
5. **唯一新增的機械件**：`evidence_reconcile.py`、`config_drift.py`、`render_owner_requests.py`（三個小工具，皆可刪，不形成新層）。

**明確不做**：不重跑 r2、不改 r3 bytes、不重簽 oracle、不放寬 TTL/gate、不以 `--allow-unrelated-histories` 併 main、
不把 PERFORMANCE 5 cells 偽造門檻、不把 18 stages 以文字補齊。

---

## 9. Claim ceiling（引用本文時的硬界線）

```text
本計畫本身            = 裁決研究（可執行），非驗收
T1 AUTHOR_SIDE_ALL_GREEN = 4/6 已達（缺 A1 裸 pytest 全綠、A7 自動對帳）
T2 OWNER_ACCEPTED_LOCAL  = NOT_RUN（需 OR-1..7）
T3 EXTERNAL_ACCEPTED     = NOT_RUN（需 OR-8 + 真 Host/Checker/Publisher）
46 cells / 18 stages / 11 holds = 仍 HOLD / ABSENT / OPEN
main 合併 = NOT_DONE（#4 建議併、#5 不直接併）
release/tag = NOT_DONE（owner 專屬）
```

本文所有數字皆可由 §2 的 receipt 重跑；任何與本文衝突的量測，以量測為準，本文須被修正。
