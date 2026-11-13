---
artifact_id: FHS-PIPD-LS-PKG-W0-vNEXT-20261114-r1
artifact_layer: W0
language: zh-TW
version: 2026-11-14_r1
round: W0_R6_W1ENTRY_20261114
supersedes_author_candidate: spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md（受界差異；r8 原件不覆寫）
base_sources:
  - spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md（680998 B，sha256 42546311c3c62ae4c721403740ac675b748f3f66898157fca94c328af592ecc4）
  - _local/FHS_vNEXT_W0_TRANSITION_BASELINE_AND_W1_ENTRY_20261112.md（114616 B，sha256 f1ee542923e3725b8d87040a2ba63f6dc0018a5d7c945a2674d706e13ff62237）
  - _local/W0_AS_BUILT.md（38379 B，sha256 b6f1dbb61484ffbc52350119a91ac4b5fd6e597eb01a4bd4243c9232aa8b3102）
claim_ceiling: SOURCE_READ + HOST_RAW(本次實測) + AUTHOR_DESIGN + LOCAL_CHECK
canonical_compiler: NOT_INVOKED
original_owner_semantic_ack: NOT_OBSERVED
native_host_execution: NOT_PERFORMED
independent_checker: NOT_RUN
release: NOT_GRANTED
source_mutation_of_imported_origin: NONE（本回合一次 LOCATOR 誤改已還原並以 digest 驗證）
paired_appendix: FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_證據型附錄.md
---

# FHS_PIPD-LS-PKG_W0 vNEXT｜W0 過渡基線與 W1 準入・實質正文

**外部正式名稱**：FHS PIPD-LS-PKG W0（vNEXT 線）｜**內部簡稱**：W0 vNEXT r1
**版本**：`2026-11-14_r1`（Asia/Taipei）｜**回合**：`W0_R6_W1ENTRY_20261114`
**配對證據**：`FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_證據型附錄.md`（同目錄；兩檔互記版本，SHA 以外部 manifest `W0_R6_W1ENTRY_20261114/out/MANIFEST_SOURCES.json` 為準，避免互嵌循環）

> **本文件是什麼**：把「已存在的 W0 r8／過渡基線／As-Built」與**本回合實際重跑的量測**合成一份可續工的 W0 實質正文。它不是第二個 Canonical、不是 Issuer、不是 Checker、不是 Release。
> **本文件不是什麼**：不是原生驗收、不是獨立驗收、不是原域語義核簽、不是 W1 已開工。

---

## 1. 身份、法位與來源

### 1.1 三個原域，三種權力（本次只讀）

| 域 | 本回合實際讀到的入口 | 量測 SHA / bytes | 本根可做 | 不可做 |
|---|---|---|---|---|
| Fabric（治理契約） | `Fabric/INTEGRATION/FHS/README.md`、`repository-map.json`；`FHS-NAV/v2`、`effect_permission=NONE`、`unknown_route=HOLD_AFFECTED_WRITE_ONLY`、`source_state=PROPOSED_NOT_OWNER_RATIFIED` | README 5463 B `3c1c2b0ae20f0028…`；map 1558 B `373120f504336772…` | 導航、引用為 mirror | 發 Policy、發 Permit、當 Issuer |
| SBL（產品工程入口） | `SBL/`（`sbl_core`、`sbl_sp`、`integrations`）；PIPD 現役 Canonical 在 `integrations/pipd`；`PIPD` 連結指向該樹 | 由 `gate_corpus` 31/31 與 `selfcheck` POS-03（13 verbs）實測 | 讀、草稿、以原 CLI 驗 | 自造 PI/PD/ECP/TQAEP、第二 Compiler |
| HG-KSEOS（原生授權／狀態／驗收控制平面） | `config/lane-routing-registry.yaml`（epoch 41 / contract_epoch 41，`3583f71bc35ab634…`）、`config/model-lane-assignment.json`（revision 44 / epoch 41，`3a4e9b2ed4a20f30…`）、`config/lane-route-slots.candidate.json`（revision 37 / epoch 41，`7a164911bf89d080…`）、`scripts/hgk-lane-policy.py validate` | validate exit 0、`fatal=False`、`findings=[]`、`debt=[]`、`checked_sites=87`、`status=CANDIDATE` | 讀、受界候選、跑 guard 負例 | 發 WorkID、簽 Grant、冒 Native PASS |

**效力順序（沿用過渡基線 §3）**：原域 Effective Reader／實機 Raw／原授權 ＞ 已核 W0 Transition Current Status ＞ 本 vNEXT 作者端 ＞ r8/r26 未受影原文 ＞ 歷史討論。本文件在第二層以下。

### 1.2 本回合的三條硬邊界

1. **不改進口原樹**：`Fabric/ SBL/ HG-KSEOS/` 的 bytes 有 `provenance/SOURCE_IMPORT_MAP.json` 逐檔 pin（433 entries）。本回合曾為修 locator 動到 `ops/tools/fhs_3lm.py`（該檔本身在 map 內），`selfcheck POS-01` 立刻以 mismatch 抓到；已用 map 指名的來源路徑還原成 `0c5fc66370d9d6f5…`（= map `target_sha256`），改以**另一個 adapter 檔**（`ops/tools/fhs_3lm_hgk_local.py`，3441 B `389f3ab847cfa103…`）承接路徑差異。這條誤改與還原都留在證據附錄，不抹去。
2. **不改分母**：`reregister_check` 的分母由 73 群／394 copies 變為 **41 群／343 copies**，原因是業主 2026-11-13 的知識庫重排（重複的 `(4)` 變體已不在盤上）。本回合以**重宣告**處理（新分母＋lineage），不是把檢查改鬆。
3. **不把「跑得動」寫成 PASS**：本回合唯一真正 served 的車道回執（EXECUTE）在 origin 自己的 identity gate 上是 `ok=false`（usage row 未落地）。照實寫 `SERVED_TRANSPORT_ONLY`。

---

## 2. 使用者可讀入口（一般 Goal 不必貼長 Prompt）

| 入口 | 觸發 | 得到什麼 | 是否需 OPS Permit |
|---|---|---|---|
| 直接問答／`SOURCE_READ` | 一般問題、合法可讀來源 | 帶 SourceSHA／span 的答案 | 不需要 |
| 隔離草稿 `LOCAL_DRAFT_WRITE` | 規格差額、三 SPEC 草案 | `_local/` 或 `deliverables/` 下的可刪檔案 | 不需要 |
| 受界 Repo 變更 `DEV` | 明列 WriteSet＋真 HEAD | 真 diff／test／rollback | 需要原域 ECP＋Grant |
| 長任務 `DURABLE` | 跨重啟、多步 | Kanban／Delegation 續跑 | 視效果 |
| 原生／外部效果 `OPS/USER` | Host、帳戶、外部資料 | 世界讀回＋補償 | 需要原 Issuer＋Consent |
| 獨立驗收／發行 `INDEPENDENT/RELEASE` | 要正式資格化或發布 | 原 Checker／Publisher 收據 | 需要不同 Principal |

**本回合實測的入口**：`selfcheck`（15/16）、`spec_identity_check`（ok=true）、`gate_corpus`（31/31）、`reregister_check`（PASS 41/343）、`lane_pin --check`（exit 0）、`hgk-lane-policy validate`（exit 0）——六條命令都在 FHS_NEXT 根可重跑，指令與 exit code 見附錄 §3。

---

## 3. 設計原意與七痛點（可驗的最低可觀測改善）

沿用 r8／L0 §01.2 的 P01–P07，不新增痛點。本回合為每一痛點留下「這一回合真的動到哪裡」的對應，而不是重新宣稱：

| Pain | 最低可觀測改善 | 本回合狀態 |
|---|---|---|
| P01 選型困難 | `MethodDecision` 列現有 Occupant／NoFit | 車道菜單與三條綁定（§10）＝選型的控制平面事實，不是模型意見 |
| P02 跨工具交接斷裂 | Same Subject／SourceSHA／Typed ABI 交原 Consumer | 三份 SPEC 同 Goal、四項（Artifact／Consumer／ACC±／BodySHA）兩兩相異（`spec_identity` ok=true） |
| P03 重問遺失 | KnownAnswer 以 Subject+Scope+SourceSHA 復用 | 沿用 r8 與過渡基線；本回合未重問已核問題 |
| P04 Writer 碰撞 | 單一原 Writer | SBL `integrations/pipd` 為唯一 Canonical；本回合未寫入 |
| P05 虛假 PASS | 真 POS＋NEG＋原 Consumer | 15 POS／7 NEG 實跑；1 條 POS 以具名 HOLD 呈現（§12） |
| P06 Host 掛載失真 | Install→Load→Invoke→Consumer | Codex pin 由 `4f91ae86…` 更新為 `83f5c2dd…`（§10.3），served 仍只到 transport |
| P07 最後一哩 | CLI 真跑、可回復 | 六條 gate 可重跑；W1 R1–R7 逐列（§14） |

---

## 4. W0 必交產品功能與排除項

**必交（本回合實測有 Raw）**
1. 來源可回查：31 冊 SourceSHA 由 `gate_corpus` 以 SHA 配對 31/31（view `gate_corpus_31`，scanned 76）。
2. 三份異質 SPEC：`_local/W0_SPEC/SPEC-A_PRODUCT_PIPD.md`、`SPEC-B_ARCHITECTURE_SEAM.md`、`SPEC-C_PROGRAM_W0.md`；BodySHA 分別 `e24251fc8a8f…`、`aebcbeed83d3…`、`d8d1c286d6ff…`。
3. 首個 FUO 可索引：`_local/W0_FIRST_FUO/`（r8 已驗；本回合沿用未改）。
4. W0 六 Primary WP：`WP-FHS-00 / 01 / 15 / 16 / 19 / 21`（受界完成，非後波能力）。
5. Lane 控制平面：三車道 menu/bind/assert 三條全綠（§10.1）。
6. 來源清冊與複本台帳：ImportMap 433 entries／423 unique target paths；複本台帳 41 群／343 copies 全數重讀 PASS。
7. 受界 HOLD 帳：3 條原域 HOLD＋本回合新增 4 條具名 HOLD（§12、附錄 §5）。

**排除（本波不做，且不得以文件宣稱）**
- 13 CLI／19 contract families／8 skills 的全面重接（W1）；192 Cell／282 B1／949 原子的全量運行（W2–W3）；Protected Native WorldRaw／Independent PASS（W2）；Cutover 與 Release（W4）。
- 任何「用文件完成度推導世界效果」的聲明。

---

## 5. A／B 兩條 FUO

| | A：建置／升級 | B：常態 Goal |
|---|---|---|
| 首個成果 | `WP15_DRAFT_FUO`：三份相異 SPEC＋SourceSHA／POS/NEG／NonGoal／readback | `SOURCE_BOUND_USABLE_RESULT` / `REVERSIBLE_DRAFT` / `DURABLE_RESUME` 依 Kind／Mode／Host 選 |
| 升格條件 | `WP00→WP01→WP05` 原 DAG 前置閉合且原 PIPD Reader 真 ACK → `WP05_ORIGINAL_READER_ACCEPTED` | 原 Consumer 真讀回；寫入需對應 ECP |
| 本回合狀態 | `DRAFT_FUO`（`spec_identity` ok=true；原 Reader 未 ACK → `ORIGINAL_ACK_PENDING`） | 六條 gate 與三車道綁定即 B 流的可讀入口 |

**不得互推**：`WP15_DRAFT_FUO` 不因本文件完成而變成 `WP05_ORIGINAL_READER_ACCEPTED`；HOLD 是有用診斷，不是 ACK。

---

## 6. 原權威與五條 Typed Seam（唯一映射）

| Seam | Producer → 原 Consumer | 本回合的觀測 |
|---|---|---|
| S1 Source/Intent/Profile→PI | 原 Source/Authority/Profile Reader → SBL-hosted PIPD Writer | 31/31 source 可配對；PI 編譯未由本根執行（`canonical_compiler=NOT_INVOKED`） |
| S2 PI→PD/ECP/TQAEP | 原 PI Writer → PD Reader／ConstructionContract／Oracle Registry | 未觸發（需真 RepoContext） |
| S3 PLAN/Policy→HGK Admission | 原 PLAN／Fabric Policy Consumer → HGK Issuer/SharedSpine | guard 以 `ERR_LANE_STALE_EPOCH` 拒絕（§10.4），fail-closed 正確但阻塞 |
| S4 Work→Hermes/Codex→World | HGK WorkID → Hermes Task／Codex Runner → 原 World Reader | EXECUTE 回執：transport served、usage row 缺 → 不計 served |
| S5 Raw/Oracle→Checker/Publisher | 原 Case Reader → 不同憑證 Checker → 原 Publisher | 未執行；本根不得代簽 |

`FLOW-*` 是規劃投影，不是新 ABI；`AC-ABI-11..15` 的 lookup 只查 §6 這五列。

---

## 7. 三份異質 TPM SPEC 的實質內容

| SPEC | 實質內容（本回合讀回的正文要點） | 原 Consumer | 專屬 NEG |
|---|---|---|---|
| Product（`SPEC-A_PRODUCT_PIPD.md`） | Persona（單一 Human Owner、單機）、JTBD、A/B FUO、8 Kind／3 Mode／4 Host、non-goals、ACC± | SBL Product Owner／PIPD Intake | 三份同文換標題 → 拒 |
| Architecture（`SPEC-B_ARCHITECTURE_SEAM.md`） | 單一權威、S1–S5、EffectClass×Permission、Recovery、SoD | 原 Domain／Host／ABI Reader | ECP 當 Permit、第二控制面 → 拒 |
| Program（`SPEC-C_PROGRAM_W0.md`） | 原 22 WP／36 edge、W0–W4 與動態 n、Stop/Resume/成本、回寫 | 原 Program／DAG Reader | 把 Scheduled 當 Done、改原 edge → 拒 |

三份共享 `Goal`（`spec_identity.shared.Goal.agree=true`），四項兩兩相異（`distinct` 每項 `distinct=true`）。**這是檔案層的量測，不是語義核簽**。

---

## 8. Native／External Reuse 決定（本回合的取捨）

| 需求 | 決定 | 依據 |
|---|---|---|
| 車道路由 | REUSE 原 HGK registry／assignment／pool；本根只寫 binding 記錄 | registry 41／assignment r44／pool r37 同 epoch；`validate` exit 0 |
| Codex Runner | REUSE 安裝版，更新 pin（`alpha.3.2 → alpha.4.1`），origin 宣告不動 | `lane_pin --check` exit 0、digest_match=true、四件 sidecar 齊 |
| Hermes Runtime | REUSE（0.23.1，profile `fhs_next`，CWD `FHS_NEXT`） | `W0_TEST_READBACK.host` 實測 |
| OpenSpec／gstack | 本回合 **NOT_USED**（無受影 Need；不為列名而裝） | 方法只在其 Need 出現時啟用 |
| 第二 Queue／Issuer／Compiler／Checker | REJECT | 控制平面唯一性（P04） |

---

## 9. W0 六 Primary WP 與 22／36 接線

- **六 Primary WP**：`WP-FHS-00`（來源/Host 發現）、`01`（Authority/Oracle/Profile）、`15`（TPM Corpus & SPEC）、`16`（Donor/Method 槽翻譯）、`19`（CI/供應鏈）、`21`（Challenge 96/H4/Seam coverage）。本回合 `19` 與 `21` 只到「可讀、可重跑」層，未做全量掃描。
- **22 WP／36 edge**：沿用 BODY-11 原圖，未新增第 23 個 WP、第 37 條 edge。`WP06`（首個可逆切片）仍在 W2，`WP17` 不反加 `WP06→WP17`。
- **50 CH**：CH-00…CH-49 的接收契約在 L0 §15；本回合不改章號、不壓平。

---

## 10. 差額施工與現況（本回合 E0–E5 實測）

### 10.1 車道平面（FHS-3LM）
- `--menu`：registry_sha256 `3583f71bc35ab634…`、pool `7a164911bf89d080…`。
- `--bind` ＋ `--assert --assert-arm opencode-go/deepseek-v4.1-flash`：**PLAN／EXECUTE／VERIFY 三條全部 `ok=true`**（binding 記錄在 `ops/lanes/bindings/`）。
- 意義：三車道在此 epoch **可被合法選取**，且是用指定臂斷言，不是只選選單。

### 10.2 實派（served 的真相）
| 車道 | 結果 | 實測 |
|---|---|---|
| EXECUTE | `SERVED_TRANSPORT_ONLY` | rank1 = opencode-go/deepseek-v4.1-flash、exit 0、nonce 由模型回聲（`FHS-W0R6-EXEC-D1`）、`turn.completed` 帶 usage（input 8348）；但 `usage_rows_after_offset=0` → origin 判 `ERR_LANE_ALL_ROUTES_EXHAUSTED`、`ok=false` |
| PLAN | `REFUSED_ERR_ARM_NOT_IN_ASSIGNMENT`（exit 4） | deepseek 在 PLAN chain 為 rank 2，`--require-arm` 只認 assigned arm |
| VERIFY_SECURITY | `REFUSED_ERR_ARM_NOT_IN_ASSIGNMENT`（exit 4） | 同上，deepseek 為 rank 3 |

**結論（不升級）**：指定模型「三車道同為 deepseek」在**現行 assignment revision 44 下不可 served**；這是原域的改派問題（W1 R5），不是本根可以用 `--force-rank` 繞過的。EXECUTE 的傳輸層確實跑起來了，但缺 usage row 就不能算 served——這正是 P05 要防的假綠。

### 10.3 Codex pin 更新（可回退）
`lane_pin --check` 首次 exit 3 `ERR_LANE_TOOLCHAIN_BINARY_MISSING`：宣告的 `bin/5449c1f0f26f1f98/codex.exe`（`0.167.0-alpha.3.2`，`4f91ae86…`）已不在盤上；實際安裝為 `bin/9e1da79431da526b/codex.exe`（`0.167.0-alpha.4.1`，`83f5c2dd…`）。以工具自身 `--declare` 重寫 overlay，pre-image 備份 `hermes-codex-lane.live.PREIMAGE_20261112.json`（`be2cd0c85a2d6c10…`），新 overlay `6002efa4f07c3e28…`。origin 宣告 `ba357dcc…` 未動；工具回報的 `origin_sha256` 已變為 `1aab074c…`，這個落差照實記在附錄（不由本根解釋）。

### 10.4 Guard 的兩個實測事實
- **SoD 生效**：maker==checker（同為 `deepseek-v4.1-flash`）→ exit 2 `REFUSE`（`SOD` 檢查 `ok=false`）。
- **epoch 欄位錯接**：`_live_epoch()` 讀 `source_of_routes` 文件的 `revision`（=44），再與 registry `epoch`（=41）比較 → 任何呼叫都得到 `ERR_LANE_STALE_EPOCH`。同一文件同時帶 `epoch=41`／`registry_epoch=41`。因此**即使 maker/checker 不同模型、admission 已宣告 ADMITTED，guard 仍會拒絕**（exit 3）。這是 origin 腳本的欄位語義缺陷，本根**只記錄＋提候選修法**，不改 origin。

### 10.5 來源與複本台帳
- ImportMap：433 entries（`1bae7892372ae63a…`），POS-01 全數重雜湊通過（本回合曾因 `fhs_3lm.py` 被改而 FAIL，已還原）。
- 複本台帳重宣告：**41 群／343 copies，V1–V5 全過，verdict PASS**（`G19_REREG_CHECK.json` 565 B `15f91fc693f71032…`）。舊 73／394 為 lineage（`old_copies` 逐群保留）。

---

## 11. Vertical Slice／Walking Skeleton（真實接線、可重跑）

**輸入 → 動作 → 輸出 → 原 Consumer**（每一步都有可執行的命令與 exit code，見附錄 §3）：

1. **輸入**：`Goal + Source + Scope`（本次＝「執行 W0 過渡基線全部項目」＋三個原域入口）。
2. **動作**：Fabric 導航（只讀）→ SBL/HGK 原 Reader → 六條 gate 重跑 → 車道 menu/bind/assert → 一次受界實派 → 寫兩份交付。
3. **輸出**：本正文＋證據附錄＋`W0_R6_W1ENTRY_20261114/out/` 的 JSON 回執。
4. **原 Consumer**：Fabric Policy Consumer／HGK Issuer／SBL PIPD Reader **本次皆未被呼叫**；因此這條 slice 的 claim 停在 `LOCAL_CHECK`，不宣稱 E2E 通過。
5. **恢復**：所有中間物都在 `FHS_NEXT_Workspace/W0_R6_W1ENTRY_20261114/`，重跑六條命令即可重建判定；owner 視窗 `WIN-9a9fd4263977` 有效至 `1794597219`（約 3 小時）。

---

## 12. POS／NEG 實測與受影 HOLD

### 12.1 本回合 POS／NEG（摘要；逐條在附錄 §4）
- `selfcheck`：POS 9／NEG 7／pass 15／fail 1；`neg_all_refused_correctly=true`。
- 唯一非 PASS：`POS-02`（control/ seed 與規格庫原件的位元同一性）→ **具名 HOLD**：宣告路徑 `…\FHS_PIPD-LS-PKG\實作\FHS_NEXT\EXECUTION_CONTROL\…` 已不存在；以檔名在知識庫根＋兩個封存根（約 336,000 檔）比對 **0 命中**，故不是改名可救，是原件已不在盤上。`control/` 兩檔自身 bytes 未變（`51f66aec…`、`66a414f4…`）。
- 新產生的 NEG：guard 同模型 exit 2；guard 陳舊 epoch exit 3（缺陷）；PLAN／VERIFY `ERR_ARM_NOT_IN_ASSIGNMENT` exit 4；EXECUTE `ok=false`（usage 缺）。以上皆為**正確拒收或正確不升級**。

### 12.2 HOLD 帳（只停受影效果）
| HOLD | 範圍 | 解除條件（原域） |
|---|---|---|
| `H-H16` | Protected SoD／Checker 資格 | HGK 原 Trust/Issuer；真 SID/ACL/金鑰隔離＋原 Checker 收據 |
| `H-READER` | 原 Canonical Reader ACK | SBL/PIPD 原 Reader 對 r8／本 vNEXT 的 scoped ACK |
| `H-ENTRY` | 入口鏡像當原 Reader 的提升 | Fabric mirror Owner；NAV 永遠 `effect_permission=NONE` |
| `H-POS02-ORIGIN`（新） | control/ seed 的原件比對 | 原 Owner 提供原件或宣告該比對作廢（不得改分母） |
| `H-GUARD-EPOCH`（新） | 受影 lane dispatch 的 guard 判定 | HGK 原域修 `_live_epoch()` 欄位（revision≠epoch） |
| `H-MANDATE-PLAN-VERIFY`（新） | PLAN／VERIFY 以 deepseek served | 原域改派 assignment（W1 R5），不得用 `--force-rank` 繞 |
| `H-USAGE-EXECUTE`（新） | EXECUTE served 的 usage row | 原 relay/ledger 落帳後重派一次 |

---

## 13. ActualServed／Resume

- **ActualServed 只有一筆可談**：EXECUTE transport 層（模型回聲＋`turn.completed` usage）。因 usage ledger 缺列，origin 判 `ok=false`，本文件**不把它寫成 served**，記 `SERVED_TRANSPORT_ONLY`。
- **Resume**：所有 gate 可重跑；owner 視窗仍有效（0/2 ops）；車道 binding 已存在；Codex pin 已可用。任何重跑從 §10 的六條命令開始，不需重建 W0。

---

## 14. W1 Entry 逐列（不要求 W2–W4 提前完工）

| # | W1 項目 | 本回合判定 | 理由／缺口 |
|---|---|---|---|
| R1 | 取得 `RepoContext`（`shw097-team/FHS` 私有庫） | `NOT_CREATED_BY_DESIGN` + `OWNER_DECISION_REQUIRED` | W0 禁止提前建庫；需 Owner 給 RepoName／ACL／Module Boundaries |
| R2 | 綁定首個 WorkOrder 十欄 | `READY_WITH_HOLD` | 十欄規格在 `docs/FHS_vNEXT_PLP_W1.md` §3；缺真 RepoContext |
| R3 | 手冊能力四分類（57 列） | `READY_WITH_HOLD` | 台帳在；分類需原 Tool/Host Owner 逐列簽 |
| R4 | SBL PIPD 原編譯入口接線 | `READY_WITH_HOLD` | `integrations/pipd` 可讀、13 verbs 實測；真編譯需原 Reader |
| R5 | VERIFY 車道 assignment 納入 mandated checker | `REPORTED_OPEN_CONDITIONAL` | 本回合以 `ERR_ARM_NOT_IN_ASSIGNMENT` 再次證實未改派 |
| R6 | H16 protected path 收斂 | `HOLD`（原域） | 需 HGK 原 Issuer/Owner 回執 |
| R7 | 原 Reader 對 r8 的採納範圍 | `HOLD`（原域） | 現有 ACK 為 `subject=None/scope=None` 的 scoped 版本 |

---

## 15. 具體下一步（依序，且各自有前置）

1. **原域改派 assignment**（R5）：讓 PLAN／VERIFY 的 assigned arm 等於 Owner 指定的 `opencode-go/deepseek-v4.1-flash`，改派後 `--require-arm` 應不再 exit 4。
2. **修 `_live_epoch()` 欄位**（`H-GUARD-EPOCH`）：以 `epoch`／`registry_epoch` 取代 `revision`；修前不得以 guard 綠燈宣稱任何 admission。
3. **補 EXECUTE 的 usage row**（`H-USAGE-EXECUTE`）：relay/ledger 落帳後重派一次，取得 `ok=true` 且 `served_arm_assigned=true`。
4. **Owner 對 control/ seed 原件裁決**（`H-POS02-ORIGIN`）：提供原件或宣告該 POS 作廢。
5. **W1 R1**：Owner 給 `shw097-team/FHS` 的 RepoName／ACL／Module Boundaries 後，才開第一筆 WriteSet。

---

## 16. 回退與 Claim Ceiling

**回退點**
- Codex pin：刪除新 overlay 即回到 `PREIMAGE_20261112`（`be2cd0c85a2d6c10…`）。
- 複本台帳：`COPY_REGISTER_PRE_OD3.json`（2026-11-12）與本回合 `COPY_REGISTER_CURRENT.json`（`f94494e468fe1ce2…`）並存，舊回合數字不改。
- `fhs_3lm.py`：已還原為 map 的 `0c5fc663…`；路徑差異改由 adapter 承擔（adapter 可整檔刪除）。
- 本回合所有輸出都在 `FHS_NEXT_Workspace/W0_R6_W1ENTRY_20261114/`，可整目錄丟棄而不影響 r8／r26／As-Built。

**能主張**：`SOURCE_READ`、`LOCAL_CHECK`、`AUTHOR_DESIGN`、本次實測的 Host Raw（Hermes 0.23.1／venv 3.11.9／registry epoch 41 讀回）、三車道「可選取」、六條 gate 的可重跑結果。

**不能主張**：原生准入、WorkID/Grant、Independent PASS、原域語義核簽、PLP 正式取代舊 Reader、W1 Repo 已建、任何 Release。**本文件結束於 `AUTHOR_DESIGN_ONLY / LOCAL_DELIVERABLES / NO_NATIVE_EFFECT / NO_INDEPENDENT_VERDICT / NO_RELEASE`。**
