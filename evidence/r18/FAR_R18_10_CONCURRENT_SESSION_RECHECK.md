# FAR_R18-10 — 併發 SESSION 複核：我的「解掉／沒解掉」是否還成立

裁決基準（上位優先）：① 對齊 r2-revision2 ② Native E2E 閉環 ③ 無人值守 ④ 高必要性 ⑤ 不過度治理／工程化 ⑥ 低阻力高效率

方法：① 重新量測我的宣稱 ② 搜尋另一 SESSION 的升級／修補（`session_search`）③ 量測共用檔案歸屬與時間戳。

---

## 一、發現另一 SESSION 正在同一工作區施工（這是本輪最重要的發現）

`session_search` 命中 **`20261027_184245_5da4fa`（B1 PIPD 線，仍在活躍）**，其機器與我重疊：

| 事實 | 量測 |
|---|---|
| **owner 金鑰早就存在** | `~/.hgk-owner/owner.key.enc`（2026-10-28 建立）、`window.json` 最後寫入 **15:08**，owner fingerprint **`412b351937be72a1`**，`effect_class_ceiling=REPOSITORY_WRITE`，`max_ops=4`，狀態 CLOSED |
| 他們的簽章機制 | `var/B1-PIPD-PKG-20261027/owner_window.py`：**窗口式**（scope、effect ceiling、max_ops、ttl），我在 R18 另造了一套 |
| PIPD 已被他們推進 | worktree `PIPD_closure_20261029/`，分支 `b1/closure-20261029`，commit `995c7ad`、`d0d748f` |
| 另一 SESSION 的產物樹 | `HG-KSEOS/HG-KSEOS-far-minimax-r2/`（untracked，完整目錄） |
| **HG-KSEOS 工作樹是混合髒的** | 6 檔 M：`active-policy.json`、`hermes-codex-lane.json`＝**我**（pin refresh 13:13）；`lane-routing-registry.yaml`(63)、`model-lane-assignment.json`(157)、`使用說明文件.md`(1079)、**`scripts/hgk-lane-dispatch.py`(47)**＝**不是我** |
| 跨 SESSION 鎖 | `*.lock` **不存在**——沒有任何互斥慣例 |

### 由此產生的三個真問題

- **F1（最嚴重）我造了第二把 owner 金鑰。** 我的信封 fingerprint 是 `be760975…`，而現場既有的 owner 身分是 `412b3519…`。兩個 owner 身分並存＝**治理上的分叉**：任何「owner 已簽」的宣稱都必須指明是哪一把。我上一輪說「owner 簽署完成」在技術上為真，在治理上**降級**為「以一個新建的第二把 owner 金鑰簽署」。
- **F2 我的車道收據不是釘在 commit 上的。** 我用的 `scripts/hgk-lane-dispatch.py` 正被另一 SESSION 修改（+47 行，未提交）。所以 `VERIFY6` 的 `served=gpt-6.1-sol` 只能重現於**當前這棵髒樹**，不能重現於任何 commit。
- **F3 `HG-KSEOS/evidence/EVIDENCE_R18_*.md` 是未追蹤檔**，在他們的 commit 範圍內，隨時可能被掃進別人的分支或被 `git clean` 清掉。

---

## 二、我的宣稱重新量測（在併發狀態下）

| 宣稱 | 重測 | 判定 |
|---|---|---|
| 「B4 解掉：合規 gpt-6.1-sol 判定」 | 收據仍在（`ok=true`、rank 2、nonce ok、83/83 逐位元相符） | 內容成立；**但工具鏈未釘 commit（F2）**，重生性降級 |
| 「B1 解掉：17 OK／5 FAIL」 | 已於 FAR-09 更正為 C4 假陽性 → 重跑 **22/22 CONTRACT_OK** | 更正後成立 |
| 「7 個 WP 有可稽核授權」 | `--mode verify` 仍 `VALID`（簽章、digest、有效期全過） | 密碼學成立；**但 principal 是第二把鑰匙（F1）** |
| 「B5 解掉」 | 三庫索引已落（本輪補），但 HG-KSEOS 那份是 untracked（F3） | 部分成立，交付位置有被洗掉風險 |
| 「撤銷：刪檔或 denylist」 | 已在 FAR-09 修為 `REFUSED_REVOKED`（缺檔與 denylist 兩路徑都具名拒絕，exit 8） | 成立 |
| 「DONE 需 permit」 | ledger 已接（`_permit_for`），WP-16 無 permit → `REFUSED … ERR_NO_DERIVED_PERMIT`；WP-00 有 permit → 放行 | 成立，且修掉了 `recorded` 序列化 bug（7 筆已回填） |

---

## 三、裁決（依基準排序）

**D1（①⑤）單一 owner 身分。** 以既有 `~/.hgk-owner/owner.key.enc`（fp `412b3519…`）為唯一 owner；我在 R18 建的信封標記 `SECOND_OWNER_KEY_DUPLICATE_RETIRED`，其委派在治理上不具權威，只能當**技術演練收據**。不刪檔（保留證據），但閘門加 `owner_identity_is_canonical` 檢查，非 `412b3519…` 一律 `REFUSED_NONCANONICAL_OWNER`。

**D2（②③）重用他們的窗口機制，不要另造。** 他們的 `owner_window.py` 已有 scope／effect ceiling／max_ops／ttl／`WINDOW_ALREADY_OPEN` 互斥——這正是我 FAR-08 提的 T1/T2 的既有實作。下一步不是寫第三套，而是把 R18 的 7 個 WP 委派**登記成他們窗口的一種 scope**（`r18_wp_effect`），沿用同一把鑰匙、同一組互斥與計數。

**D3（①⑥）工具鏈釘版。** 車道收據必須寫入 `git rev-parse HEAD` + `dirty=true/false`，否則不可重現。我的收據補上這兩個欄位；在他們提交 `hgk-lane-dispatch.py` 之後重跑一次 VERIFY 即可去掉這個 caveat。

**D4（③⑥）跨 SESSION 鎖，20 行級。** `var/_locks/<area>.lock`（json：session_id、purpose、ttl、created）；寫共用檔（`HG-KSEOS/config/*`、`*/evidence/*`、`var/B1-*`）前檢查；過期自動失效。不引入服務、不引入資料庫。

**D5（⑤）不做**：不合併兩把金鑰、不複製他們的 `owner.key.enc`、不改他們的 PIPD 分支、不對他們髒樹做 stash／checkout／worktree。

---

## 四、建議執行方案

| 序 | 動作 | 需誰 | 風險 |
|---|---|---|---|
| 1 | 閘門加 `REFUSED_NONCANONICAL_OWNER`（fp≠412b3519… 一律拒） | 我 | 無（收緊） |
| 2 | 車道收據補 `git_head`／`dirty` | 我 | 無 |
| 3 | 建 `var/_locks/` 併發鎖並在用共用檔前檢查 | 我 | 無 |
| 4 | 把 R18 委派改登記為他們窗口的 scope（重用 `owner_window.py`） | **owner 開窗**（他們那套 tkinter 視窗） | 需協調兩個 SESSION 不撞窗 |
| 5 | 待 `hgk-lane-dispatch.py` 提交後重跑 VERIFY6 | 我 | 低 |
| 6 | HG-KSEOS evidence 索引改放回合目錄並在 PR 描述引用，不留在別人的 untracked 區 | 我 | 低 |

**明確不建議**：把我這把第二把鑰匙當成正式 owner（D1 已否決）；在併發髒樹上做 `git checkout`／`stash`／`clean`；把他們的 `HG-KSEOS-far-minimax-r2/` 收進我的 PR。

---

## 五、對「解掉／沒解掉」的最終表述（修正版）

- **解掉**：B1 的分類（22/22 契約可判定）、B4 的車道可服務性（rank 2 可釘）、B5 的交付位置（三庫索引已落）、撤銷路徑（具名拒絕）、DONE 需 permit 的結構強制。
- **未解掉且不冒充**：native bundle、HOST_OP/RELEASE 的 Issuer PERMIT、驗收簽章、**單一 owner 身分（F1）**、**工具鏈釘版（F2）**、**跨 SESSION 互斥（F3/F4）**。
- 一句話：**技術閉環已成形，治理閉環還缺「同一把鑰匙、同一個 commit、同一把鎖」。**

---

## 六、追加量測（併發的兩個新事實）

### F4 同一份 R18 內容已出現在**兩條**候選分支上

| 分支 | commit | 狀態 |
|---|---|---|
| `candidate/r18-openspec-only` | `e7714c6`（base `f6dfb1e`） | 我的 **PR #4** |
| `candidate/r18-fhs-skeleton-spine-20261029` | **`190df33`**「openspec: add fhs-msc-skeleton-spine-revision2 change + round R18 evidence index」 | **主工作樹目前就檢出在這條分支**，且有 6 個未提交的修改檔（含 `scripts/hgk-lane-dispatch.py`） |

判讀：另一 SESSION 把**重疊的 OpenSpec 內容**提交在另一條分支上，而我開了 PR #4。這不是誰對誰錯，是**交付分叉**：同一 subject 有兩個候選尖端，reviewer 會看到兩份相互競爭的變更。**不得 force-push、不得刪分支**；處置＝選定一條為交付尖端，另一條標 `SUPERSEDED_BY` 並在 PR 描述註明（保留歷史）。

### F5 我自己的閘門有 shadowing bug（已修）

`canonical = str(...)` 這個布林區域變數**遮蔽**了模組函式 `canonical(rec)`，使 drill 路徑拋 `TypeError: 'bool' object is not callable` 而不是放行。修正後三項控制重測：非 canonical owner→**rc 9**、drill flag→**rc 0**、drill flag 下的 HOST_OP→**rc 7**。
記錄理由：這是本輪第二次同類自傷（前一次是 `recorded` 序列化順序）。兩者都只有在**負向控制真的去跑**時才會暴露——這正是為什麼控制組不能只寫在文件裡。

### 併發鎖與釘版已落地

- `tools/session_lock.py`：`var/_locks/<area>.lock`（session／purpose／ttl／expires_at）；已取得 `HG-KSEOS/config` 60 分鐘鎖
- `receipts/CONCURRENCY_STAMP.json`：HG-KSEOS `190df334` **dirty 9、dispatcher modified=true**；PIPD `995c7ad0` dirty 231；Fabric `fffcb98b` dirty 13；SBL `826ca066` dirty 47
