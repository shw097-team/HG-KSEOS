# FAR 研究 — `HANDOFF-PATCH-v1`：殘留、缺口、阻斷、升格與併入裁決

**輪次**：`FAR-CLOSURE-PROMOTION-20261030` · **基準**：PR #7 head `a3db2b2`、`main` `f6dfb1e5`
**治理**：Fabric＝契約（唯讀）／SBL＝產品工程指揮入口／HG-KSEOS＝原生授權、狀態、驗收平面
**本檔性質**：裁決建議書。不是驗收、不是許可、不是簽章，也不改動任何 claim ceiling。

---

## 0. 方法：這一輪量測了什麼

| 量測 | 結果 | 證據 |
|---|---|---|
| 三車道實跑 | VERIFY rank1 `opencode-go/deepseek-v4.1-flash` **ok 3.21 s**；rank3 `opencode-go/glm-5.3-flash` **死 0.71 s**；PLAN rank1 deepseek **ok 2.33 s**；`openai-codex/gpt-6.1-sol` **401** | 本輪探針 `P5C`、`P10` |
| 指派檔內部一致性 | **同一個檔案裡三種說法**：`assignment` 列 PLAN/VERIFY＝gpt-6.1-sol；`lane_chains` 首位＝deepseek；`declared_by` 說三車道全 deepseek；`user_instruction_revision_2` 說 VERIFY＝GLM-5.3 | `config/model-lane-assignment.json` rev 38 |
| 開放 PR | 6 個：#1 #2 #4 #5 #6 #7，全部 `mergeable_state: clean` | GitHub API |
| 路徑重疊 | **#7 與 #1/#2/#4/#5/#6 重疊＝0**；#5∩#6＝79 檔且**79/79 blob 完全相同**；#1∩#6＝9（7 相同）；#2∩#6＝2（0 相同） | GitHub API 逐檔 sha |
| #5 的獨有內容 | 106 檔，**全部在 `evidence/r18*`**（r18 稽核軌跡），#6 未帶 | 同上 |

---

## 1. 直接結論

**「全部 ALL PASS」在今天不可能達成，而且不是流程問題，是供應問題。**

三車道中，只有 EXECUTE 的模型（deepseek-v4.1-flash）是活的；PLAN 與 VERIFY 只能靠它或它自己。
也就是說：**目前系統上不存在「與執行者不同模型」的驗收臂**。任何今天宣稱的「獨立驗收 PASS」，
只能是執行者自己驗自己——那是 SoD 契約明文禁止的。

可達的是這個：

| 層 | 今天可達？ | 內容 |
|---|---|---|
| **機械層全綠**（M） | **可以，1 輪** | 909/909 payload、BODY 封存 byte-exact、first-work 可重現、35/35 可從乾淨重建重現、DAG 結構、dispatcher/收據/釘選修補 |
| **Owner 接受（T2）** | **可以，1 個簽章窗口** | 8 個已預填決策，機械證據齊備，不需新工作 |
| **Native 驗收（T3）** | **不可以** | 需要真的 Host/Checker/Publisher，目前不存在；建議只做 **WP-FHS-15 一條垂直切片**，不要 22 條 |
| **22/22 WP Native** | **不可以** | 同上，且 22 條 × 同一條管線不增加資訊 |

一句話：**把「ALL PASS」重新定義成「機械全綠 ＋ T2 有界接受」，這個今天就能拿到；剩下的 3 個閘門是
憑證與外部 Checker，不是再跑幾輪就能解決的。**

---

## 2. 尚未 PASS 的完整清單（按「誰能關」分類）

### A 類 — 工程可立即關閉，不需任何簽章（9 項）

| # | 項目 | 現狀 | 關閉動作 | 工時 |
|---|---|---|---|---|
| A1 | F-02 書目錄改名（31/909） | 開 | 以 `01_SUBSTANTIVE_BODY` 交付，`verify` 內建 alias→明確報錯 | S |
| A2 | F-02b MAX_PATH（415/909） | 開 | 所有驗證器改用 `\\?\` 走訪；短根交付 | S |
| A3 | F-03 shipped harness 34/35 | 開 | 上移 `sys.path.insert` 一行（`lines_changed: 2`） | S |
| A4 | F-13 `prepare.py` 漏 `fixtures` | 開 | 快照清單加 `fixtures`，從乾淨重建再驗 35/35 | S |
| A5 | F-14 35/0 紀錄時間戳造假跡象 | 開 | 真跑一次、寫入 `generated_at`，舊紀錄標 superseded | S |
| A6 | F-12 封存只蓋 897/911 | **已撤回** | 改以 manifest 分區封存，BODY 已 byte-exact | 已完成 |
| A7 | F-01 EVIDENCE 重封 | BODY 已重現；EVIDENCE 差 4,801 B | 以記錄下 membership 重新封存，新 digest 另立版本列 | S |
| A8 | F-07/F-08/F-06 控制平面 | 本機已修/已記錄 | 落成一個 upstream PR＋回歸測試 | M |
| A9 | 文件內殘留不一致（30 vs 35 links、findings 計數） | 部分已修 | 以回執為準重算一次 | S |

### B 類 — 需要 owner / issuer 決策或簽章（8 項，見 §5）

F-05 closure 邊、F-04 身分作用域、EVIDENCE digest 作廢宣告、r4 版本發布、toolchain 釘選更新、
VERIFY 獨立性方案、22 WP 驗收範圍、合併與 release 政策。

### C 類 — 卡在供應／憑證，工程無法自解（3 項）

| # | 阻塞 | 實測 | 影響 |
|---|---|---|---|
| C1 | `openai-codex/gpt-6.1-sol` 401 | upstream 401、無 usage row、無 nonce | PLAN 與 VERIFY 的指定臂雙雙不可用 |
| C2 | `opencode-go/glm-5.3-flash` 死 | 0.71 s 直接 `ERR_LANE_ALL_ROUTES_EXHAUSTED` | 唯一宣告過的替代臂也不可用 |
| C3 | NVIDIA 臂未測 | `nvidia/deepseek-ai/deepseek-v4.1-flash` 與 EXECUTE 同模型 | 即使可用也不構成獨立性 |

### D 類 — 屬於計畫級，不能在本輪關閉（4 項）

22 WP native 驗收（0/22）、真正的 Registry/Checker/Publisher 收據、74 個既有紅測、OR-1..OR-8 中的
OR-6（需不同 principal）與 OR-8（需外部 SOURCE/ABI/HOST/CHECKER/RELEASE）。

---

## 3. 逐項關閉方案（A 類，可直接執行）

### A1+A2 — 佈局與長路徑

不改 payload、不改 manifest 語義：交付時用 `01_SUBSTANTIVE_BODY`，並在 `verify_package.py` 把
「路徑不存在」拆成兩種具名錯誤——`ERR_LAYOUT_ALIAS`（31 筆）與 `ERR_PATH_TOO_LONG`（415 筆）。
一個驗證器若把這兩者混成「missing 446」，下一個團隊會花一整天找不存在的損壞。

### A3+A4+A5 — 讓 35/35 變成可重現，而不是條件成立

今天 35/35 依賴**交付內附的 READERS 快照**；用出廠工具重建反而掉回 34/1（`prepare.py` 不抓
`fixtures`）。三件事一起做才算關閉：補 `fixtures` 進快照清單 → 乾淨重建 → 真跑一次並寫時間戳。
少做任何一件，35/35 就還是「在我機器上成立」。

### A6+A7 — 封存

BODY 已 byte-exact（114 entries / 4,007,065 B / `5e722cfb…`），這條是真的，保留。
EVIDENCE 差 4,801 B、797 vs 宣告的 entries ⇒ 不要「修」舊 digest，而是**另立一列**：
新 digest＋membership 明細＋`supersedes: <舊 sha>`。舊列標 `WITHDRAWN_NOT_REPRODUCIBLE`。
理由：digest 是可驗證性資產，改一個數字就等於宣告過去所有引用都無效。

### A8 — 控制平面三修

`F-07`（收據建構 `NameError` 讓成功回合的回執全消失）是這輪最危險的缺陷：它讓「有做事但沒證據」
變成常態。三修打包成一個 PR：釘選刷新、`NameError`、`served_arm_assigned` 正規化，附一條
「exit 0 必產出收據」的回歸測試。

### A9 — 一致性

以回執重算，不以文件互相對齊。已被稽核抓到的「429」「2.31 s」「65 blobs」都屬此類，已修；
`30 vs 35 links` 的差異要說明來源（`P1_VERIFIED` 把兩份不在 payload 的報告也計入），不是改數字。

---

## 4. 「ALL PASS」的可達定義（claim ladder）

| 級 | 名稱 | 判準 | 今天 |
|---|---|---|---|
| T0 | `AUTHOR_LOCAL` | 作者自跑、無回執 | 已超越 |
| T1 | `SEALED_REPRODUCIBLE` | 第三方可用指令重現全部數字 | **已達**（payload、BODY seal、first-work、DAG） |
| T2 | `OWNER_ACCEPTED` | owner 對**有界 claim 集**簽章 | **可達**：機械層 9 項 ＋ 3 條 seal 陳述 |
| T3 | `EXTERNAL_ACCEPTED` | 外部 checker 獨立重現 | 不可達（無 checker） |
| T4 | `NATIVE_VERIFIED` | 真 Host/Checker/Publisher 收據 | 不可達 |

**建議的 T2 有界 claim 集**（只這四條，不多不少）：

1. payload 909/909 逐位元組相符（在正規佈局下）；
2. BODY archive 可由 payload 以 manifest 分區 byte-exact 重建；
3. WP-FHS-15 first-work 可重現，且 5 個 artefact byte-identical、4 個差異已具名歸因；
4. 22-WP DAG 無環、clause→atom 24/24 完整。

這四條都不需要 native admission，因此 owner 可以只憑機械證據接受——這正是「不過度治理」的邊界。

---

## 5. Owner / issuer 決策包（8 項，一次窗口簽完）

> 每項都給：問題 → 選項 → **建議** → 理由 → 不決定的後果。標記 🔑 者必須 owner 金鑰；
> 標記 ⚙️ 者我可在預授權下先行執行、事後補簽。

### OD-1 🔑 F-05：宣告 closure 與 typed edges 不一致

- 選項 A：宣告改為 `{00,15}`（承認 01 是同層兄弟，不是前置）。
- 選項 B：DAG 加邊 `01 → 15`（承認 01 是前置，需補 01 的產物為輸入）。
- **建議 A**。理由：first work 實際只用了 00 的輸入；加邊會虛構一個本次沒有發生的依賴，且會讓
  排程器在未來無故等待 01。成本：一行宣告＋重跑 D2。
- 不決定：D2 永遠是 REVIEW，任何「全綠」宣告都會帶著一個已知矛盾。

### OD-2 🔑 F-04：PI 身分綁絕對路徑

- 選項 A：維持絕對根綁定，但在 reader contract 明寫 `source_root_policy: absolute`，並加 `root_id` 欄位。
- 選項 B：改成內容定址（相對根），一次性重寫 hash 鏈。
- **建議 A**。理由：B 會讓本輪所有回執、PI、TaskSpecSeed、ExecutionHandoff 全部失效，
  代價遠大於收益；身分的作用是追溯，不是跨站去重。加 `root_id` 讓未來可選，不必現在付費。
- 不決定：每個新環境的第一輪都要重新解釋「為什麼雜湊不同」，會被誤判為不決定性。

### OD-3 🔑 EVIDENCE digest 作廢與重封

- **建議**：舊列標 `WITHDRAWN_NOT_REPRODUCIBLE`（保留原 digest，不改寫），新增一列新 digest ＋
  membership 明細 ＋ `supersedes`。理由：保留歷史可審計性；改寫等於偽造過去。
- 不決定：manifest 永遠有一列無法驗證，且下一個人會以為是檔案損壞。

### OD-4 🔑 發行 r4（把 5 個缺陷一次收掉）

- **建議**：r3 凍結不動，發 r4，內含 A1/A2/A3/A4/A5/A7 ＋ 新 manifest ＋ 新 readback。
  理由：這 5 項都是「交付物本身的缺陷」，只有在交付物裡修才算關閉；修在我們的副本裡只算代償。
- 不決定：下一個團隊會原封不動再踩一次，而且這次他們沒有我們的回執。

### OD-5 🔑 控制平面三修上架（A8）

- **建議**：一個 PR、附回歸測試、owner 合併。理由：`F-07` 會靜默吞掉證據；這條不修，之後每一輪的
  「有沒有做」都只能靠人記憶。
- 不決定：任何車道回合的成功都無法自證。

### OD-6 🔑🔴 VERIFY 獨立性（**最高優先**）

- 選項 A：為 relay 配置 `gpt-6.1-sol` OAuth 憑證（PLAN 與 VERIFY 一起解鎖）。
- 選項 B：宣告一個**與 EXECUTE 不同模型**且實測活著的臂（今天沒有：GLM-5.3-flash 已死、NVIDIA 臂同模型）。
- 選項 C：外部/人工 checker（只適用 T3）。
- **建議**：A 為主、C 為 T3 路徑；同時在 config 加一條結構性閘門
  `independence_requirement: served_model_must_differ_from_execute`，讓「自己驗自己」在**機器層**
  就不可能通過，而不是靠人記得。
- 理由：B 今天無貨可選；沒有這條閘門，未來任何 agent 都能用 deepseek 跑 VERIFY 拿到 `ok: true`，
  然後把它寫成「獨立驗收」——這是本輪差點發生的錯（我用 `--require-assigned-arms` 才躲過）。
- 不決定：`INDEPENDENT_ACCEPTED` 永遠 NOT_RUN，「ALL PASS」永遠缺一塊。

### OD-7 🔑 22 WP native 驗收範圍

- 選項 A：22 條全做。選項 B：**只做 WP-FHS-15 垂直切片**（permit → WorkOrder → Checker → Publisher
  收據一條通）。
- **建議 B**。理由：未知的是管線，不是數量；22 條跑同一條管線不會多出任何資訊，卻會把一輪變成一個
  季度。切片綠了之後，第 2..22 條是重複勞動，可自動化。
- 不決定：永遠停在「0/22」這個數字上，而這個數字對外部審查的殺傷力遠大於「1/22 但管線已證」。

### OD-8 🔑 合併與 release 政策

見 §7。建議順序 **#7 → #6 → #4 →（#1/#2 判定）→ #5 入 r18 基底**，tag 延後到 native 切片之後。
理由：全部 `mergeable: clean`，而 #7 與所有 PR 路徑重疊為 0——這是最好併的一顆，先併可立刻讓外部團隊
有可讀的交付。

---

## 6. 升格候選：哪些「已檢測」可以升

| 候選 | 目前級 | 可升到 | 判準是否滿足 | 建議 |
|---|---|---|---|---|
| 本輪 payload 完整性（909/909、正規佈局） | T1 | **T2** | 機械可重現、回執齊 | ✅ 升（OD 批簽第 1 條） |
| BODY archive byte-exact 重建 | T1 | **T2** | 已實測 byte-exact | ✅ 升（第 2 條） |
| WP-FHS-15 first-work 可重現 | T1 | **T2** | 5 identical / 4 具名差異 | ✅ 升（第 3 條） |
| 22-WP DAG 無環、24/24 atoms | T1 | **T2** | 結構檢查 6 PASS 1 REVIEW | ✅ 升（第 4 條，D2 待 OD-1） |
| EVIDENCE archive | — | 不可升 | 差 4,801 B | ❌ 先重封（OD-3） |
| 35/35 harness | 條件 T1 | 暫不升 | 依賴不可重建的快照 | ❌ 先做 A3+A4 |
| 22 WP 個別 WP | T0 | 不可升 | 只有文件宣告 | ❌ 只做 WP-15 切片（OD-7） |
| R20 `r2-revision3.zip` | T1 | T2 可討論 | 已封存、外部審計重現 | ⚙️ 建議與本輪同批簽 |
| OR-1..OR-8 | — | 不可升 | 未填未簽 | ❌ 依 §5 逐項裁決 |

**升格鐵律**：T2 只接受「機械可重現」的陳述；任何需要 Host/Checker 的陳述一律留在 T1，不得因為
「看起來沒問題」而升。

---

## 7. 併入 `main` 的候選與分支（實測）

| PR | 目標 | 檔案 | 與 #7 重疊 | 判定 | 建議 |
|---|---|---:|---:|---|---|
| **#7** 本輪 | main | 86 (+53,324/−0) | — | clean | **第 1 併**：純新增、零重疊、對外可讀 |
| **#6** publish/r20-subset | main | 371 (+53,470/−577) | 0 | clean | **第 2 併**：main 導向的 r20 重放 |
| **#4** candidate/r18-openspec | main | 81 (+5,049/−0) | 0 | clean | **第 3 併**：openspec-only，與 #7 不同 change 目錄 |
| **#1** b1-r5-native-admission | main | 10 (+1,153/−19) | 0 | clean | 併前確認 #6 是否已含其內容（#1∩#6＝9 檔、7 檔相同） |
| **#2** b1-r6-artifact-scope | #1 基底 | 2 (+65/−5) | 0 | clean | 併入 #1；`#2∩#6` 兩檔**內容不同**，需先判定誰是修正版 |
| **#5** candidate/r19 | candidate/r18 | 185 (+20,255/−310) | 0 | clean | **不要**併 main；併回 r18 基底保留歷史 |

**決定性事實**：`#5 ∩ #6 = 79 檔，且 79/79 blob 完全相同`。也就是 #6 已經把 #5 的核心內容重放到
main 上；#5 只多 106 檔，且全部是 `evidence/r18*` 稽核軌跡。
⇒ **#6 對 main 取代 #5**；#5 併回 r18 分支即可，兩者不衝突（目標分支不同）。

**#2 的風險**：`src/hg_kseos/native_admission.py` 與 `test_r6_artifact_scope.py` 在 #2 與 #6 中內容
不同。併 #6 前必須確認 #6 的版本是否已含「拒絕 Windows rooted-relative 核准路徑」的修正；
若含 → 關閉 #1/#2 為 superseded；若不含 → 先併 #1+#2，再讓 #6 rebase 解 2 檔衝突。**這是唯一需要
人工判斷的合併風險，其餘皆為零衝突。**

**release**：tag 只在「#6+#7 併入且機械層全綠」後打 `v0.x-mechanical`；正式 release 等 native 切片。

---

## 8. 三車道執行方案（含路由裁決）

### 8.1 現況（實測，非推測）

| 車道 | 指定臂 | 實測 | 可用？ | 與 EXECUTE 同模型？ |
|---|---|---|---|---|
| PLAN | `openai-codex/gpt-6.1-sol`（medium, OAuth） | **401** | ❌ | — |
| PLAN（chain rank1） | `opencode-go/deepseek-v4.1-flash` | ok 2.33 s | ✅ | **是** ⚠️ |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | ok 7.2 s / 27.99 s | ✅ | — |
| VERIFY | `openai-codex/gpt-6.1-sol` | **401** | ❌ | — |
| VERIFY（chain rank1） | `opencode-go/deepseek-v4.1-flash` | ok 3.21 s | ✅ | **是** ⚠️ |
| VERIFY（chain rank3） | `opencode-go/glm-5.3-flash` | 死 0.71 s | ❌ | — |

### 8.2 兩個平面，不要混

`config/model-lane-assignment.json` 自己寫得很清楚：`in_hermes_plan_orchestrator_plane` 是**會話內
PLAN 平面**，`gate_scope` 不管它；`scripts/hgk-lane-dispatch.py` 只管 **CODEX-CLI 車道**（EXECUTE /
VERIFY_SECURITY）。**本輪的 PLAN 工作是在會話平面、由 EXECUTE 模型（deepseek）完成的**——這件事要在
回執裡標成 `PLANNED_BY_OPERATOR_SESSION`，不能記成「PLAN 車道已服務」。

### 8.3 路由裁決

1. **PLAN**：以會話平面執行，標註模型；等 OD-6 憑證到位後，用 PLAN 車道對同一份裁決書做一次覆核
   （不是重做，是 review）。
2. **EXECUTE**：照舊，唯一活躍可用臂。
3. **VERIFY**：**在 OD-6 落地前，不得以 deepseek 執行任何「驗收」**。可以跑「復算」（recomputation，
   例如重跑 `verify_package.py`），但必須標成 `RECOMPUTE_BY_EXECUTOR`，不得寫成 acceptance。
4. **結構性防呆**：config 增 `independence_requirement`，dispatcher 在 VERIFY 回合檢查
   `served_model != EXECUTE.assigned_model`，否則 `ERR_VERIFIER_NOT_INDEPENDENT`。這一條讓「自己驗自己」
   在機器層不可能通過——比任何文件提醒都有效，成本一行。

---

## 9. 建議執行方案（R21 / R22 / 一個簽章窗口）

### R21 — 機械全綠（不需任何簽章，可無人值守）

| 步驟 | 車道 | 產出 |
|---|---|---|
| 1 | EXECUTE | r4 交付包：A1/A2/A3/A4/A5/A7 + 新 manifest + 新 readback（受限 WriteSet） |
| 2 | 會話 | 三重複算：payload 909/909、BODY byte-exact、35/35 從乾淨重建 |
| 3 | EXECUTE | 控制平面三修 PR（A8），附回歸測試 |
| 4 | 會話 | 併 #7（零重疊、純新增）→ 外部團隊立即可讀 |
| 5 | 會話 | 產出 `R21_CLOSURE_TABLE.tsv`：每項 A 類 → closed/proof，機械可檢 |

**R21 完成的定義**：A 類 9 項全 closed，且每一項都有一行可重跑的指令與一個回執。

### R22 — 有界 T2 接受（一個簽章窗口，8 個決策）

窗口 `--ttl-hours 4 --max-ops 12 --effect-ceiling REPOSITORY_WRITE --scope registry_row_sign,merkle_root_sign`，
8 個 payload 已預填（OD-1..OD-8 中除 OD-6 憑證外全部），owner 一次口令、逐項確認。
**這是把 8 次中斷壓成 1 次的手法，也是「低阻力」的具體做法。**

### R23 — WP-FHS-15 垂直切片（OD-7 選 B 之後）

一條 WP 走完 permit → WorkOrder → Checker → Publisher，取得第一份**真的** native 收據。
這一輪之後才有資格談 `NATIVE_VERIFIED`，而且只對 WP-15。

### 不可壓縮的三件事

1. `gpt-6.1-sol` 憑證（C1）——沒有它，PLAN/VERIFY 兩條車道永遠只有代理品。
2. 真 Checker/Host（D）——沒有它，T3/T4 永遠是 0。
3. Owner 金鑰（B）——授權不可代簽，這是契約，不是效率問題。

---

## 10. 不建議做的事（防止過度治理／過度工程）

1. **不要**為 22 條 WP 各建一條管線——先一條切片。
2. **不要**改 hash 契約去修 F-04——會讓全部既有回執失效。
3. **不要**重簽已作廢的 archive，或「修正」EVIDENCE 的舊 digest——用 supersedes 新列。
4. **不要**為每個缺陷開一個治理輪次——A 類 9 項一輪收完。
5. **不要**把 VERIFY 換成同模型的「快速通道」——那會讓整個 claim ceiling 失去意義。
6. **不要**引入新平台/新 registry——現有 lane + 回執已足夠表達全部狀態。

---

## 11. FAR 裁決記錄

| 議題 | 裁決 | 依據 |
|---|---|---|
| 「ALL PASS」是否可達 | **不可達（native 層）；機械層可達** | 實測 C 類 3 項全滅、D 類無 Host/Checker |
| 是否用 deepseek 跑 VERIFY 拿綠燈 | **否** | SoD；本輪已用 `--require-assigned-arms` 躲過一次 |
| 是否改 hash 契約 | **否** | 成本/收益；改宣告優於改契約 |
| 22 WP 是否全做 | **否，只做 WP-15** | 未知的是管線不是數量 |
| #5 是否併 main | **否** | #6 已以 79/79 相同 blob 重放其核心；#5 併回 r18 |
| 是否先併 #7 | **是** | 與全部開放 PR 路徑重疊 0、純新增 |
| 8 個 owner 決策是否分批 | **否，一次窗口** | 低阻力、可審計、ops 8/40 |
| 是否宣稱任何 T2/T3 | **否（本輪）** | 無獨立驗收；T2 需 OD-2 窗口後才可宣告 |
