# FAR_R18-07/08 — 停工理由複核 與 owner-key 口令信封可行性

裁決基準（上位優先，衝突時前者勝）：
① 對齊 `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
② Native E2E 自主執行閉環 ③ 適合無人值守高自動化 ④ 高必要性
⑤ 不過度治理／不過度工程化 ⑥ 低阻力高效率

方法：對五條停工理由逐條重測（不引用自己先前的敘述），量測檔在 `receipts/FAR_PROBE_*.json`。

---

## 一、逐條複核

### B1「22/22 WP oracle 無 backing」→ **分類錯誤（不是 blocker），真缺口是「無 case 綁定」**

實測 `wp_graph.json`：

- 節點 22；每節點都有 `positive`（不變量散文）、`negative`（破壞式突變）、**`first_fail`（型別化錯誤碼，如 `WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID`）**
- `typed_edges` **36 條，但只有兩種型別**：`DATA_OR_ADMISSION` 34、`CAPABILITY` 2 → **沒有任何 ACCEPTANCE／ORACLE 邊**
- 節點與邊中**完全沒有 case_id**；`acceptance_edges15.json` 的 15 條邊是 DAG 級契約（`AC-E01 GoalIntake…`），不是 WP 級案件；`runner_bindings.json` 282 筆是 B1 案件（`TQ-B1-*`）

**判讀**：不是「沒有 oracle」，而是「oracle 有宣告、沒有案件身分」。以「作者端必須先寫對映表」當停工理由，等於把一個**可機械推導**的工作升級成人為前置門檻——違反 ③⑥。

**裁決**：建 100 行級 `wp_contract_harness.py`：對每個 WP 由自身欄位派生 POS（檢查 `positive` 不變量於當前狀態）與 NEG（施加 `negative` 突變，斷言得到該 `first_fail` 碼），逐一記錄真實結果。這不是偽造對映，是對**已宣告欄位**做可重跑斷言。claim ceiling 標明 `CONTRACT_LEVEL_NOT_NATIVE_CASE`。

### B2「native WPs 缺 owner-signed bundle」→ **成立，但我的範圍說錯了**

實測 `effect_class` 分佈：

| effect_class | 數量 | WP |
|---|---|---|
| `SOURCE_READ` | 5 | 00, 01, 09, 19, 21 |
| `LOCAL_DRAFT_WRITE` | 4 | 05, 07, 15, 16 |
| `HOST_OP` | 10 | 02, 03, 04, 08, 10, 11, 12, 13, 17, 20 |
| `REPO_WRITE` | 2 | 06, 18 |
| `RELEASE` | 1 | 14 |

我把 13 個 WP 一律標 PARKED 並套同一句理由，等於用**家族級推論**掩蓋逐 ID 差異。實際上 `SOURCE_READ`＋`LOCAL_DRAFT_WRITE` 共 **9 個 WP 不需要 Issuer PERMIT**（讀取與隔離草稿）。其中 00/01/19/21/18 本回合已有收據，剩 **05/07/15/16** 可在此權限下推進到「逐 ID 量測」而非「整批 PARKED」。

**裁決**：13 個 HOST_OP/RELEASE 維持 gated（真 blocker，具名 owner＝原 owner 綁定）；9 個改為可執行並逐一量測。

### B3「WP-05 缺 Writer ACK」→ **成立，但不是停工理由**

本回合約束就是 candidate-only，不做 promotion 並不損失任何東西。把它列進「停工原因」是把**範圍選擇**寫成**阻塞**。

**裁決**：維持 HOLD（具名 owner＝PIPD Writer、resume predicate＝具名 ACK），自停工清單移除。

### B4「VERIFY 車道排序屬 owner 設定」→ **錯，可用派工參數解決**

`hgk-lane-dispatch.py` 支援 `--force-rank`（line 1574）。VERIFY3 已證明 rank 2 的 `openai-codex/gpt-6.1-sol` 可服務且 nonce 相符；rank 1 的 key-auth arm 只是**先跑贏**。釘 rank 是一次性旗標，不是配置變更，也不動 owner 政策。

**裁決**：以 `--force-rank 2` 重派，不需任何簽章或設定變更。

### B5「Fabric/PIPD/SBL 無產物可交付」→ **錯**

實測：`HG-KSEOS/evidence`、`Fabric/evidence`、`SBL/evidence` 均存在（SBL 另有 `evidence/{checker,ci,compiler}`），PIPD 有 `_handover/` 與 `ACCEPTANCE.md`。本回合產出 FAR、供給鏈、96 格重現、MVS 對映、缺陷修補——**這些就是可交付的證據索引**，只是我沒依既有慣例落盤。

**裁決**：依各庫慣例各落一份 evidence index（不含 raw／金鑰／DB）。

---

## 二、owner key passphrase envelope 是否解決授權問題？

**結論：單獨不能，且若做成「可自動 unseal 的私鑰信封」是有害的；做成「範圍受限的授權委派信封」則可以，而且是本回合最值得做的一件事。**

### 為何單獨不能

1. 無人值守＝無人輸入口令 → 口令必須對執行者可取得（DPAPI／環境變數／檔案）。此時信封只保護**靜態**金鑰，執行期等同「OS 使用者帳戶邊界」，並沒有恢復「人在迴路」。
2. 若信封內是**原始 owner 私鑰**且 agent 可 unseal，agent 就取得簽一切的能力——比現在「被擋住」更糟：它把硬阻塞換成**無聲的能力擴張**。簽章將不再證明「owner 決定」，只證明「持有該金鑰的進程決定」，而該進程就是 agent。**必須否決此型。**
3. SoD 未被解決：maker 與 checker 若都能 unseal 同一信封，等於共用 principal（違反本回合約束）。

### 為何「委派信封」可以

關鍵是把簽章對象從**每一個效果**移到**一次委派**：

```
owner 簽一次 DELEGATION（不是簽每個 effect）
  envelope = Enc(KDF(passphrase), DelegationRecord)
  DelegationRecord = {
    subject_sha256,             // r2-revision2 的凍結雜湊
    wp_set: [...],              // 逐 ID
    effect_classes: [...],      // 只允許 SOURCE_READ / LOCAL_DRAFT_WRITE / REPO_WRITE→candidate branch
    not_before, not_after,      // TTL
    max_effects_per_class,      // 配額
    nonce_seed,                 // 防重放，對應 spine 的 nonce 機制
    checker_principal_id,       // 必須 ≠ maker
    deny: [RELEASE, HOST_INSTALL, secrets, force-push]
  }
Issuer 驗章 → 授予 PERMIT，條件：request ⊆ wp_set ∧ class ∈ allowed ∧ now ∈ TTL ∧ nonce 未用
```

- 這正好接上**現有** registry schema：`native_admission` 已經有 `scope.request_sha256` 欄位（目前空），B1 也已有簽章 runner registry 與 245/735/245 的實跑人口。**不需要新基礎設施**，只需要 owner 簽一筆把 scope 綁上。
- 人身決策留在委派時（可稽核、可撤銷、會過期）；無人值守期間只做**驗證**，不做**裁決**。
- 撤銷＝registry 標記該 delegation 失效（單筆），不必追每個 receipt。
- 口令信封在這個設計裡的角色降級為**保護委派記錄**，不是保護私鑰；agent 拿到的是 capability token，不是簽章權。

### 授權與簽章建議（具體）

| 層 | 簽什麼 | 誰持有 | 可否無人值守 | 內容限制 |
|---|---|---|---|---|
| T1 委派信封 | `DelegationRecord`（範圍+T TTL+配額+nonce seed） | owner 一次，agent 只讀 | **可以** | 僅 `SOURCE_READ`／`LOCAL_DRAFT_WRITE`／`REPO_WRITE→candidate` |
| T2 現場合議 | 單次 native bundle（HOST_OP） | owner 在場（Windows Hello／DPAPI+UI） | 不可以 | 逐 WP、逐效果、單次 nonce |
| T3 Release 封印 | Release 記錄 | owner 在場 | 不可以 | L4 only，永不委派 |

**永不進信封**：原始私鑰、`RELEASE`、`HOST_INSTALL`、secrets、遠端不可逆、main 合併。

### 對本回合的直接效果（若採納）

- 22 個 WP 中 **9 個**（SOURCE_READ＋LOCAL_DRAFT_WRITE）可由 T1 覆蓋 → 可無人值守跑到「量測完成」。
- **13 個** HOST_OP/RELEASE 仍要 T2/T3，但 T2 的「在場」可壓縮成「一次會話簽一批」，不是每次卡住。
- 這才是 ②③ 要的閉環：**決策一次、執行多次、驗證每次**。

---

## 三、最佳工程裁決（依基準排序）

1. **撤銷我原本的停工宣告**（B1/B4/B5 分類錯誤，B3 非停工理由）。停工清單只保留「T2/T3 類 native 效果」這一項真 blocker。
2. **立即執行（無需新授權）**：
   a. `wp_contract_harness`：22 個 WP 逐 ID POS/NEG 契約斷言（把 UNBACKED 轉成 CONTRACT_MEASURED）。
   b. VERIFY 車道 `--force-rank 2` 重派，取得**無 refusal** 的 gpt-6.1-sol 判定。
   c. Fabric／SBL／PIPD 依慣例落 evidence index。
3. **需 owner 一次的簽章（建議立即請簽）**：T1 `DelegationRecord`——這是把無人值守從「不可能」變成「可持續」的唯一槓桿，且不需要交出私鑰。
4. **明確不做**（過度工程化）：不建第二 Planner/Checker/Issuer、不把 WP→case 對映寫成人工表、不為每個 WP 造新 artifact family、不改 lane 政策檔。

## 四、建議執行方案（階段化，可無人值守）

| 階段 | 內容 | 需 owner | 產出 |
|---|---|---|---|
| P0（今天） | B4/B5/B1 修正：force-rank 重派、evidence index、contract harness | 否 | 3 份收據／1 份 harness |
| P1 | contract harness 全 22 WP 跑綠/紅標記，逐 ID 記錄 first_fail | 否 | `WP_CONTRACT_RESULTS.json` |
| P2 | 起草 T1 `DelegationRecord`（subject_sha＋9 WP＋class 白名單＋TTL 30d＋配額）並附 registry 綁定步驟 | **是（簽章）** | 簽章信封＋綁定收據 |
| P3 | 以 T1 重跑 9 個 WP 至量測完成，checker（gpt-6.1-sol，force-rank 2）獨立判定 | 否（在 T1 範圍內） | 獨立 verdict |
| P4 | 13 個 HOST_OP/RELEASE 以 T2 單次會話批次簽 | **是（在場）** | 批次 bundle |
| P5 | 四庫 PR 依各庫慣例 | 否（已在 standing grant 內） | PR |

**若 owner 只願意簽一件事**：簽 T1。它把 9/22 的 WP 從「永久 PARKED」變成「可無人值守執行」，其餘 13 個仍受 T2 保護，治理面積不增。

---

## 五、P0 執行結果（本節為實測，不是計畫）

### 5.1 WP 契約斷言器（`tools/wp_contract_harness.py` → `receipts/WP_CONTRACT_RESULTS.json`）

對 22 個 WP 各跑 6 項機械檢查（first_fail 型別、output 宣告、permission_basis 宣告、write_set 與
effect_class 一致性、depends_on 解析與 DAG 無環、ledger 狀態與 effect_class 相容）：

- **CONTRACT_OK 17／CONTRACT_FAIL 5**
- `needs_native_authority` = **11**（HOST_OP 10 ＋ RELEASE 1）
- `executable_without_new_authority` = **11**（SOURCE_READ 5 ＋ LOCAL_DRAFT_WRITE 4 ＋ REPO_WRITE 2）
- `parked_but_not_native_gated` = **06、15、16**（被我用同一句 native 理由錯誤涵蓋的三列）
- DAG 無環：成立；`typed_edges` 仍只有 `DATA_OR_ADMISSION` 34／`CAPABILITY` 2，**無 ACCEPTANCE 邊**

**5 個 FAIL 的性質（重要，影響信封設計）**

| WP | 失敗項 | 判讀 |
|---|---|---|
| 05、07、15、16 | `C4 write_set 與 effect_class 矛盾` | 這 4 個宣告 `LOCAL_DRAFT_WRITE`，但 `write_set` 是 `BIND_EXACT_BY_ORIGINAL_OWNER`（要求原 owner 綁定）。二者只能有一個對：若 write_set 正確，這些 WP **需要 owner 綁定、不可無人值守**；若 effect_class 正確，則 write_set 寫錯。**在裁決前不得假設它們可自動執行。** |
| 06 | `C6 REPO_WRITE 卻 PARKED` | REPO_WRITE 不在 native 必要集合內，被我過度阻擋；候選分支寫入本就在 standing grant 內 |

因此「9 個可無人值守」必須修正為：**確定可執行 7 個**（SOURCE_READ 5 ＋ REPO_WRITE 的 06/18，其中 18 已完成），其餘 4 個待 C4 矛盾裁決。這是對我上一節數字的自我修正。

### 5.2 這對 owner-key 信封的影響

C4 矛盾正是信封設計要處理的邊界：`BIND_EXACT_BY_ORIGINAL_OWNER` 若確實是這 4 個 WP 的真實寫入語義，那它們必須落在 **T2（現場合議）**，不能由 T1 委派覆蓋。故 T1 白名單在裁決前應只含 `SOURCE_READ` 與 `REPO_WRITE→candidate branch`，不含 `LOCAL_DRAFT_WRITE`。這使 T1 的第一版更小、更容易被 owner 接受。

---

## 六、P2 已執行：owner 簽署委派信封（實測）

owner 於本機模態口令視窗輸入通行碼（agent 全程未見、未落地），產生：

| 檔案 | 內容 |
|---|---|
| `governance/owner_envelope.json` | scrypt(n=2^15,r=8,p=1) + AES-256-GCM 包住 32-byte Ed25519 seed；只含 ciphertext、public key、fingerprint。**無 seed 欄位、無明文字面** |
| `governance/delegation_R18.json` | 23 欄委派記錄（subject digest、7 WP、2 class、deny 8、TTL、配額、nonce_seed、SoD） |
| `governance/delegation_R18.sig` | 64-byte Ed25519 over canonical JSON |
| `receipts/DELEGATION_SIGNED.json` | 簽署收據（fingerprint、digest、allowlist、not_after） |

**驗章**：`--mode verify` → `signature_valid true`、`subject_digest_matches true`（83 組重推）、`within_validity true`、`verdict VALID`。owner fingerprint `be76097571a7d7fd…`。

**強制執行**（`tools/delegation_gate.py`，唯一消費者，fail-closed）→ `receipts/DELEGATION_GATE_MATRIX.json`：

- **POS 7/7** `PERMIT_DERIVED`：WP-00/01/09/19/21（SOURCE_READ）＋ 06/18（REPO_WRITE→`candidate/r18-openspec-only`），並已 consume 7 筆進 `governance/delegation_effects.jsonl`
- **NEG 6/6 全拒**：HOST_OP `REFUSED_CLASS_NOT_ALLOWLISTED`、RELEASE `REFUSED_CLASS_DENIED`、WP-05 `REFUSED_CLASS_DENIED`、REPO_WRITE→main `REFUSED_TARGET_NOT_CANDIDATE`、過期 `REFUSED_EXPIRED_OR_NOT_YET_VALID`、未列 WP `REFUSED_WP_EXCLUDED`

**可撤銷**：移除 `governance/delegation_R18.json`，或把 `delegation_id` 記入 Issuer denylist；信封本身不授予任何權限。

**仍未取得（不冒充）**：native bundle、Issuer 對 HOST_OP/RELEASE 的 PERMIT、驗收簽章。11 個 HOST_OP/RELEASE WP 仍須 T2 現場合議。
