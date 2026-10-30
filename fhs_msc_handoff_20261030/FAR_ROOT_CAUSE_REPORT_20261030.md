# FAR 完整根因報告 — 為什麼同一組缺陷修了很多次還會復發

**輪次**：`FAR-RECURRENCE-ROOTCAUSE-20261030` · **基準**：`HG-KSEOS` HEAD `190df33`（config HEAD rev 33 / 磁碟 rev 38）
**方法**：交叉比對 5 個 `evidence/FAR-*` 回合、2 個前序 session（2026-10-21 `FAR-LANE-VERSION-MIX`、2026-10-29 `SKELETON_SPINE`）、config 的 HEAD 與工作區、以及本輪 15 份回執。

---

## 1. 先講結論

**這既不是路由問題，也不是單純的結構問題。** 兩者都是症狀。跨回合比對後只有一個變數能解釋「為什麼修了還會回來」：

> **所有修復都寫進了「可丟棄的層」——工作區（dirty worktree）、活著的 process、`.bak`、回合收據；
> 而沒有寫進「不可逆的層」——commit、service、registry、gate。**
>
> 可丟棄的層會被下一個 session、下一次重開機、下一次 `git checkout` 自然覆蓋。
> 因此同一缺陷必然以新面貌復發，而每一輪的 FAR 都會「合理地」再發現它一次。

再往上追一層，還有一個更硬的機制：**每一輪的 acceptance 都停在 `NOT_RUN`**。5 個 FAR 回合，5 個 `ACC-*=NOT_RUN`。
沒有 acceptance 的回合，依契約不能把修復升為 binding——於是「已修」永遠只是「已記錄」。

---

## 2. 交叉比對：2026-10-21 的診斷 vs 2026-10-30 的症狀

2026-10-21 的 session（`FAR-LANE-VERSION-MIX-20261021`，PLAN，read-only）已寫出與今天幾乎逐字相同的結構診斷。九天然後，同一組缺陷以新名字重現：

| # | 10-21 的診斷 | 10-30 的實測症狀 | 同一個？ |
|---|---|---|---|
| 1 | 多重權威且語意不一致：registry / assignment / candidate / AGENTS / profile / tests 各自承載政策，同一份 assignment 內同時有「gpt 降級」與「gpt 現行」 | `model-lane-assignment.json` 同檔四種說法；`--require-assigned-arms` 因此選到死臂 | **是** |
| 2 | session plane 與 lane plane 被混用為證據 | 我把 10102（`desktop-model-router`）當成車道 relay，得到 401 | **是（逐字）** |
| 3 | toolchain 缺乏一致、可用、固定版本；lane config 指定的 executable 已不存在 | F-06：canonical binary pin 與實際執行檔不符；每次都要手動指 `codex.exe` | **是** |
| 4 | drift gate 只覆蓋部分一致性；`check_drift` 已有兩筆 error | **今天連工具都沒有**：`scripts/check_drift.py` 不存在，drift 工具只剩 `var/` 裡的散檔 | **是，且更壞** |
| 5 | 修復停在局部重綁，未完成跨面一致性 | relay 手動啟動、無 service、autostart 關閉；一重開機就回到「只剩一顆模型」 | **是** |
| 6 | 大量未結案 WorkOrder；狀態閉環不足 | 5 個 FAR 回合、5 個 acceptance `NOT_RUN`；native 0/22 | **是** |

**六個觀察點，九天，零個改變。** 這不是「修得不夠好」，是「修的東西不會留下來」。

---

## 3. 第二個硬證據：政策基質是一個未提交的工作區

| 讀法 | revision | `assignment` 結構 | PLAN / VERIFY | EXECUTE |
|---|---|---|---|---|
| `git show HEAD:config/model-lane-assignment.json` | **33** | `lane_group` 陣列 | **deepseek**（owner 10-23 理由） | deepseek |
| 磁碟上的同名檔案 | **38** | `role` 陣列（**schema 已變**） | **gpt-6.1-sol**（`owner-order-20261024-s205-od01…`） | deepseek |

四個 routing 檔同時是 dirty：`active-policy.json`、`hermes-codex-lane.json`、`lane-routing-registry.yaml`、`model-lane-assignment.json`。
最後一次 commit 動 config 是 **2026-10-23**——政策領先 commit **5 個 revision、7 天**。

後果是三重的，而且互相放大：

1. **不可重現**：本輪所有量測描述的是 rev 38；別人 `git clone` 得到 rev 33，看到的 chain 不一樣。
2. **讀者會讀錯**：rev 33 的 `lane_group` 對上 rev 38 的 `role`——用舊鍵讀新檔會得到空集合，然後靜默 fallback。我自己第一次解析就拿到 `{None: None}`，這正是 dispatcher 會踩的坑。
3. **漂移會複利**：每個 session 為了讓自己那輪能跑，就地再改一次這個檔，revision 繼續加，commit 繼續不發生。

**所以「路由問題」的真正機制不是「選錯模型」，是「政策沒有交易（transaction）」。**

---

## 4. 框架外的第三個根因：診斷—執行斷裂

10-21 那一輪不是沒診斷對。它診斷對了，然後把 P0 寫成：

> 「先由 owner 重確認目標與 SoD 例外……若現有規則不允許擴充本輪，另立實施回合。」

也就是說：**正確的診斷被轉換成一個「等 owner 決定」的政治物件，然後沒有人執行。** 九天後它以 401 的形式回來。

這條路徑在本輪又出現一次（我把 6 個工程選擇寫成「待 owner 決策」），只是這次我當場把它拆掉了。
它是系統性的：**FAR 的產物是 PLAN，PLAN 的產物是「待裁決」，而「待裁決」沒有 SLA、沒有 owner、也沒有預設值。**

---

## 5. 三層判定（回答「是結構性還是路由性」）

| 層 | 內容 | 判定 | 現狀 |
|---|---|---|---|
| **L1 路由層** | arm 選錯、port 用錯、relay 沒起、capacity | 實例性 + 可修 | **本輪已修**（relay 起、gpt-6.1-sol 服務、AO 8/8 ACCEPTED） |
| **L2 結構層** | 多重權威、schema 漂移、plane 混用、control 不落地、acceptance 不授予 | 結構性 | **10-21 已診斷，從未執行** |
| **L3 根因層** | 修復寫在可丟棄層；acceptance 預設 NOT_RUN；缺陷類別無記憶；診斷→執行斷裂 | **框架外** | **本報告首次命名** |

L1 修好不會讓 L2/L3 消失——這正是為什麼「FAR 修了很多次」：每輪都在 L1 拿到一個漂亮的綠燈，然後 L2/L3 把綠燈收回。

---

## 6. 四個根因（可檢驗、可反駁）

**R-1 修復的歸屬錯誤（可逆性）**
修復若寫在 worktree / process / `.bak`，就繼承了它們的生命週期。可逆的修復必然復發。
檢驗：rev 33 vs rev 38；`ocx` 無 service；`.bak` 世代。
反駁條件：任一輪的修復在「重開機 + 新 clone」後仍然有效。

**R-2 acceptance 從不授予**
5/5 FAR 回合 `ACC-*=NOT_RUN`。沒有 acceptance，修復不能升為 binding，於是下一輪必須重新證明同一件事，而證明成本高到只能抽樣，抽樣就會漏。
檢驗：`grep -h "NOT_RUN" evidence/FAR-*/**.md` → 每個回合都有。
反駁條件：出現一個 `ACC-*=ACCEPTED` 且被後續回合引用為前提。

**R-3 缺陷類別沒有記憶**
同一個缺陷每次以新名字出現（10-15 的 owner-gated amend = 10-21 的 toolchain pin = 今天的 F-06）。沒有 class id、沒有 recurrence counter、沒有 regression gate，所以「修過」無法被查詢。
檢驗：本報告第 2 節的六列對照。
反駁條件：存在一份缺陷類別帳本，且新回合開場必須對帳。

**R-4 診斷→執行斷裂**
正確診斷被寫成「待 owner 裁決」，而待裁決沒有預設值、沒有期限、沒有執行者。
檢驗：10-21 PLAN 的 P0；本輪 8 個 OD 中的 6 個。
反駁條件：每個 FAR 產物都帶 `default_if_silent` 與到期日。

---

## 7. 對策：把「可逆」改成「不可逆」（三條鐵律）

**IR-1 政策必須有交易**
`config/*.json|yaml` 不得以 dirty worktree 生效。dispatcher 在 spawn 前檢查：
- `git status --porcelain config/` 必須為空；
- 否則在回執寫 `policy_commit`、`policy_dirty: true`，並把該回合降級為 `ADVISORY_ONLY`（fail-closed，不是 fail-open）。
成本：一個 8 行檢查。效果：消滅「每個 session 各自改一份政策」。

**IR-2 transport 必須是服務**
`ocx service install`（或等價 keep-alive），`hgk-lane-preflight.py` 先驗 healthz 再 spawn。
成本：一次性。效果：消滅「重開機只剩一顆模型」。

**IR-3 acceptance 必須有預設值**
每輪 charter 必須二選一：**授予**（oracle 先登記、AO 判決、maker 轉錄）或**具名拒絕**（owner 簽名 + 到期日）。
`NOT_RUN` 不再是合法終態。本輪已示範：`AO_ACCEPTANCE.json`，8/8 ACCEPTED，一次定罪（O5）後修正重判。

**配套：缺陷類別帳本（Recurrence Ledger）**
`class_id` / `occurrences[]`（含 round + 日期）/ `last_fix_commit` / `regression_test`。
規則：同一 class 出現 ≥2 次且沒有 regression test，**該回合不得開工**。
這條是唯一能讓「修了很多次」變成「修過一次就不再回來」的機制。

---

## 8. 重新分類『FAR重新研究項目』（修正我上一輪的判斷）

| 項目 | 上輪判斷 | 本輪更正 | 層 |
|---|---|---|---|
| OD-1 F-05 closure | 待 owner 裁決 | 仍是宣告修正，但屬 `DECIDE+RECORD`，不需簽章 | L2 實例 |
| OD-2 F-04 身分範圍 | 待 owner | 同上；維持 root-scoped + 宣告 | L2 實例 |
| OD-3 EVIDENCE digest | 「不可重現、需重封」 | **撤回**：兩個封存皆 byte-exact（`P13`） | 已關 |
| OD-4 發行 r4 | 待簽章 | **已發行**（additive，`r4/`），不需簽章 | 已關 |
| OD-5 控制平面三修 | 一個 PR | 併入 IR-1／IR-2，不再獨立 | L2 |
| OD-6 VERIFY 獨立性 | 最高優先、待憑證 | **已完成**：relay 起、AO 8/8 ACCEPTED | 已關 |
| OD-7 22 WP 範圍 | 只做 WP-15 切片 | 不變；但**先決條件是 IR-3**（否則切片也沒有 acceptance） | L3 |
| OD-8 合併順序 | #7→#6→#4→… | 不變；但 main 落後 5 個 revision，合併前必須先 IR-1 | L2 |
| 「車道只有一個模型活著」 | 供應缺口 | **撤回**：是 relay 沒起 + 平面誤用 | L1 |
| 「native 做不到」 | 結構限制 | 半對：E2E 可用 `LOCAL_CHECKER`，只有**外部** principal 不可自造；本輪 AO 已提供程序性外部性 | L3 |
| F-15 harness 依賴 | 「需釘 jsonschema」 | **更正**：同一 interpreter 可直接 import，是 harness 取用路徑問題，機制未隔離 | L1 |

---

## 9. 建議執行方案（R24，一輪到底）

1. **IR-1**：dispatcher 加 dirty-config gate（8 行）＋ 把 rev 38 commit 成 rev 39（單一真相），刪除其餘三份宣告的重複語意。
2. **IR-2**：`ocx service install`；`hgk-lane-preflight.py` 加 healthz 前置。
3. **IR-3**：把本輪的 oracle/AO 流程固化成 `scripts/ao_accept.py`（登記 oracle → 派 AO → 機械轉錄），任何回合都能一條命令完成。
4. **Recurrence Ledger**：以本報告第 2 節六列為初始六條 class，先補 regression test 再開新回合。
5. 之後才做 OD-7 的 WP-FHS-15 垂直切片。

**裁決建議**：R24 不需要任何簽章；唯一需要簽章的是把 AO 的 ACCEPTED 升為 T2（一個 payload）。

---

## 10. 這份報告對自己的檢驗

- 若 R-1 成立，則 rev 38 在別人機器上不存在 → 可驗：`git show HEAD:config/model-lane-assignment.json` 應為 rev 33。**已驗，成立。**
- 若 R-2 成立，則每個 FAR 回合都有 `NOT_RUN` → 可驗：5/5。**已驗，成立。**
- 若 R-3 成立，則同一缺陷在不同回合以不同名字出現 → 已列六組對照。**成立。**
- 若 L3 不成立（即真的只是路由），則修好 L1 後不應再出現 10-21 的第 1、2、5 項——但本輪三項全中。**故 L3 成立。**
