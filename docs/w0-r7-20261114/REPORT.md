# FHS_PIPD-LS-PKG_W0_vNEXT 實質正文（r2）

> **版本**：`FHS-PIPD-LS-PKG-W0-vNEXT/2026-11-14-r2`（Asia/Taipei）
> **內部簡稱**：W0 vNEXT 交付視圖 r2
> **前版**：r1（`c4617197f47bb2c2437b9340b4cffda740369bf7c4796f1aba3a6166a8656d7f`，21,791 B）
> **Claim ceiling**：`SOURCE_READ + HOST_RAW + AUTHOR_DESIGN + LOCAL_CHECK + LANE_SERVED + WRAPPER_SCOPED_SOD`
> **不在本件的聲明**：`ORIGINAL_ACK`／`NATIVE_PASS`／`INDEPENDENT_PASS`／`RELEASE`
> **配對證據**：`FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r2_證據型附錄.md`（同目錄）

---

## 0｜本件的法位：交付視圖，不是第三份 W0 SPEC

L2《FHS_vNEXT_PLP_全波次藍圖》§02 明寫「**本輪不另產第三份 W0 文件**」（L2:L2544）。Thin Prompt §4 又要求交出「一份實質正文＋一份證據型附錄」。兩者不衝突，但**必須說清楚本件是哪一種**：

- 本件是 **r8 的交付視圖（delivery view）**：所有規範內容仍以 `spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md`（680,998 B，`42546311c3c62ae4c721403740ac675b748f3f66898157fca94c328af592ecc4`）為唯一 current，本件不建立第二個 W0 Reader、不改它的任何條款。
- 本件只承載三件 r8 沒有的東西：**(a)** 本輪實測 Raw（gate／車道／NEG）；**(b)** 與 L0/L1/L2 的逐項對帳；**(c)** 具名 HOLD 的 FirstFail 與 Resume。
- 因此下游若要引用規範，引 r8 的條號；要引用「本輪實際量到什麼」，引本件與附錄的 Raw 路徑。

---

## 1｜上游藍圖對帳（本輪真的讀了 L1/L2）

前兩回合我只讀 L0，這是漏做。本輪把 L1、L2 做結構級解析並落地索引（`out/L1_L2_HEADING_INDEX.json`、`out/L1_CH_ALIGNMENT.json`）。

| 上游 | 檔名／大小 | SHA-256 | 本輪實際取用 |
|---|---|---|---|
| L0 | `FHS_vNEXT_總藍圖.md`／365,153 B | `33e49ca22872b135534e078661df32d6a2892058c8c0efae859540943731caf0` | 六層聲明、A/B FUO、S1–S5、§06.2A 車道卡、§11.1A SoD、§16 HOLD |
| L1 | `FHS_vNEXT_PLP_藍圖.md`／7,256,694 B／34,272 行／**50 個 H1（CH-00..49）**／1,268 標題 | `bd2ab0b74f21da6b74cac2e1b1ffd2c8dcbde11daa6d22333a3c52d0675af060` | 每 CH 的五段結構（1 需要／2 輸入行為 Consumer／3 可施工規格／4 專屬 POS-NEG／5 原產品條款）作為本件的章節驗收樣板 |
| L2 | `FHS_vNEXT_PLP_全波次藍圖.md`／2,759,509 B／16,815 行／54 H1 | `a6077aa208aa9cbcb2d37572e13be73de14125cd3f5881b3fa6320e34814c39b` | §02 W0 真實狀態、§03 由依賴推導 W0→Wn（**n=4**，W0–W4）、§04 各波正文、§05 22 WP |
| 任務入口 | `FHS_vNEXT_W0_HERMES_FHS_THIN_PROMPT_2026-11-13_r1.md` | `82d3def56bfd1f1df98d9489a42a0f65d22cded8387a4ab801d54e3a89f8021c` | §2 權威順序、§4 兩份 MD 規格、§5 完成判準 |
| 本輪 baseline | `_local/FHS_vNEXT_W0_TRANSITION_BASELINE_AND_W1_ENTRY_20261112.md`／114,616 B | `f1ee542923e3725b8d87040a2ba63f6dc0018a5d7c945a2674d706e13ff62237` | P0-01～P1-06 逐列驗收面 |

**逐項對齊結果**

| # | 上游要求 | 本輪實作 | 判定 |
|---|---|---|---|
| 1 | L2 §04：W0 主波 WP 集合 = `WP-FHS-00/01/15/16/19/21` | 本件 §3 以此六包列 Done/Trace | **ALIGNED** |
| 2 | L2 §03：n=4（W0–W4），W18 不是第 18 波 | 本件只做 W0 出口，不派 W2 受保護效果 | **ALIGNED** |
| 3 | L2 §02：不另產第三份 W0 文件 | 本件定位為 r8 的交付視圖（§0） | **ALIGNED（以視圖名義）** |
| 4 | L2 §04 W0 POS：普通短 Goal 在合法 read/draft 可交具 Source/Consumer/FUO 的三 SPEC | `spec_identity_check` ok；三 SPEC 同 Goal 四項相異 | **ALIGNED（作者端）** |
| 5 | L2 §04 W0 NEG：不得把 `PASS_WRAPPER_SCOPED` 當全權、不得用缺 OPS 阻 Draft、不得用附錄歷史降 E3 | 本件 §6 保留三個受界 HOLD，未升格 | **ALIGNED** |
| 6 | L1：每 CH 需五段＋POS/NEG＋Consumer | L1 自身 **50/50 五段齊全**（缺 s1–s5／POS／NEG／consumer／resume 皆 0，見附錄 F）；本件章節亦照該樣板 | **ALIGNED（結構）／語義核簽仍 H-L1-OWNER-ACK** |
| 7 | L0 §07 R4-ENG.10/11：薄控制包與薄啟動 Prompt 需「完整可轉錄正文」 | `control/` 兩檔存在且已 pin，但**非 byte-identical import**（見 H-POS02） | **DIVERGENT（已具名 HOLD）** |

**DIVERGENT 的處置**：第 7 項不是本輪可以自行解決的——spec-library 端的 2026-11-11 原件在 `FHS_PIPD-LS-PKG/實作/FHS_NEXT/` 下**不存在**（該目錄本身不存在），336k 檔封存掃描 0 命中。因此 `control/` 兩檔只能是**轉錄件**（依 L0 §07 R4-ENG.10/11 的「完整可轉錄正文」要求）。這一點已寫成 `out/POS02_SCOPE_CHANGE_CANDIDATE.md` 交給 owner 裁決，不自行改 selfcheck 的判準。

---

## 2｜本輪實測（可重跑；數字皆為本次執行結果）

### 2.1 W0 gate

| 檢查 | 指令 | 結果 | Raw |
|---|---|---|---|
| selfcheck | `ops/selfcheck.py` | **15/16 PASS，exit 1**；唯一 FAIL `POS-02`（origin 目錄不存在） | `out/SELFCHECK.txt` |
| SPEC 身分 | `ops/tools/spec_identity_check.py` | **exit 0，ok=true**（三份同 Goal、四項相異） | `out/SPEC_IDENTITY.json` |
| 31 冊語料 | `ops/tools/gate_corpus.py` | **declared 31／matched 31／missing 0** | `out/GATE_CORPUS.json` |
| 副本重宣告 | `ops/tools/reregister_check.py` | **groups 41／members 343／343 read／PASS**（7.3 s） | `out/REREGISTER.json` |
| lane pin | `ops/tools/lane_pin.py --check` | **exit 0** | `out/LANE_PIN.json` |
| lane policy | `HG-KSEOS/scripts/hgk-lane-policy.py validate` | **exit 0，status=CANDIDATE，debt=[]，87 站點** | `out/LANE_POLICY.txt` |

`POS-02` 的失敗是**定位失敗，不是內容失敗**：它用 rglob 在 spec-library 找檔名比位元，而 origin 子樹 `FHS_PIPD-LS-PKG/實作/FHS_NEXT/EXECUTION_CONTROL/` 已被知識庫重組移走（現有目錄是 `FHS_NEXT_升級`、`FHS-MSC_PIPD-LS-PKG_BODY`、`PIPD-LS-PKG`、`藍圖`）。`control/` 兩檔的 bytes 仍等於進口清冊宣佈的 `target_sha256`（`51f66aec…`／`66a414f4…`），本輪以新增的 `ops/tools/pos02b_control_pin.py` 驗證：**兩檔 pin 全對、`source_absent=true`、verdict `PASS_PIN_ONLY`**（`out/POS02B.json`，exit 0）。要把 `selfcheck` 改綠需 owner 裁定定位方式，候選見 `out/POS02_LOCATOR_CANDIDATE.md`。

### 2.2 三車道 ActualServed（本次新證據）

relay 以 `OPENCODEX_HOME=%LOCALAPPDATA%/HG-KSEOS/opencodex-hermes` 重啟（這是上一回合 `ERR_LANE_ALL_ROUTES_EXHAUSTED` 的真正根因：我用預設 home 起 relay，dispatcher 讀的是 lane-home 帳本，因此永遠 0 列）。重啟後三車道皆在同一本 `usage.jsonl` 落地：

| Lane | 選取方式 | served arm | `usage_rows_after_offset` | `served_arm_assigned` | 回執 |
|---|---|---|---|---|---|
| EXECUTE | `--force-rank 1` | `opencode-go/deepseek-v4.1-flash` | 1 | **true** | `out/LANE_EXECUTE.json` |
| PLAN | `--force-rank 2` | 同上 | 1 | false（chain 內非 primary） | `out/LANE_PLAN.json` |
| VERIFY_SECURITY | `--force-rank 3` | 同上 | 1 | false（chain 內非 primary） | `out/LANE_VERIFY_SECURITY.json` |

三張回執皆 `ok=true`、`ok code=None`、nonce 由模型逐字回聲。**PLAN ActualServed 因此由「未提供」變成「有 Raw」**（baseline P0-05 的 POS）。

必須同時說清楚的三件事：
1. `--force-rank` 不是繞過：它選的是 assignment chain 內既有的臂（PLAN rank 2、VERIFY rank 3），origin 自己在回執記 `served_arm_assigned=false`，這就是它願意的最大誠實度。
2. 只有 EXECUTE 的 `served_arm_assigned=true`。PLAN／VERIFY 的 assigned primary 不是 deepseek，這是**原域指派事實**，不是我能改的（改它等於改 Issuer）。
3. VERIFY 車道 served ≠ Independent PASS。L0 §06.2A 寫的是「模型只產 FINDING/候選，獨立 Protected Checker 在不同 Credential 裁決」。本輪拿到的是 served 回執，不是 protected verdict。

### 2.3 SoD 的四個 NEG（baseline P0-06）

用既有 `lane_dispatch_guarded.py`（不是新建），同一 lane、同一 binding：

| 案例 | 注入 | 結果 |
|---|---|---|
| maker 缺失 | 省略 `--maker-*` | **REFUSE `ERR_MAKER_MISSING`，exit 3** |
| maker 偽造 | `--maker-engine forged --maker-model forged/none` | **REFUSE `ERR_MAKER_NOT_IN_ASSIGNMENT`，exit 4** |
| maker=checker 無豁免 | 兩側同為 deepseek | **REFUSE `ERR_LANE_SOD_VIOLATION`，exit 2** |
| maker=checker 有業主裁決 | 加 `--sod-exemption "owner ruling 2026-11-12 … SOD006-C4"` | 放行派送、served `deepseek-v4.1-flash`，但模型未回聲 nonce → `ERR_NO_ARM_EMITTED_NONCE`，exit 6 |

結論：**fail-closed 四個案例都真的會拒**（前三案），第四案證明豁免路徑存在但其歸屬仍未成立（nonce 未回聲）。所以 P0-06 的狀態是 `PASS_WRAPPER_SCOPED`，不是 PASS。

### 2.4 退役臂的四個 NEG（baseline P0-07 / H11-H14）

| 退役臂 | 結果 |
|---|---|
| `opencode-go/mimo-v2.6-pro` | `ERR_LANE_REQUIRED_ARM_ABSENT`，attempts=0 |
| `glm-5.3` | 同上 |
| `z-ai/glm-5.3-flash` | 同上 |
| `minimax-m3.1-flash-free` | 同上 |

四臂在派送層被擋且**零次嘗試**（attempts=0 表示連 spawn 都沒有）。殘留缺口：**直呼 relay 的 10101 仍可達退役模型**（上一回合實測 200）；那是 relay 邊界，屬原域，記 `H-RETIREMENT-BOUNDARY`。

### 2.5 Guard 的 epoch 分歧（baseline P0-04）

`hgk-lane-guard.py --lane VERIFY_SECURITY --expected-epoch 41` 的原始回執（`out/GUARD_EPOCH41.json`）：

```
status=REFUSE  decision=REFUSE  exit_code=2
epoch=41  live_epoch=44
admission_status=UNPROVEN  claim_ceiling=CANDIDATE_ONLY
```

根因在 `_live_epoch()`（`HG-KSEOS/scripts/hgk-lane-guard.py:92-110`）：它讀 `source_of_routes` 指向的 assignment，然後回傳 `doc["revision"]`。assignment 的 `revision` 是**它自己的版次 44**，其 epoch 欄位是 `registry_epoch: 41`（`config.live/model-lane-assignment.json:665`）。registry 則是 `contract_epoch: 41`（`lane-routing-registry.yaml:4`）。

因此 `live_epoch=44` 是**讀錯欄位**，不是真的漂移。這正是 baseline P0-04 說的「Assignment、Registry、Pool、Guard 讀同一來源」沒有做到。修法只能是原域的 6 行 patch（候選見附錄 G），本輪不自行改 origin。

### 2.6 子代理並行產出的四份台帳（皆 read-only，未改原樹）

| 台帳 | 關鍵數字 | 檔案 |
|---|---|---|
| Host 讀回（P0-02／P1-03） | relay `healthz` 200／`opencodex 2.11.0`；codex 僅一個 bin 目錄 `9e1da79431da526b`；venv311 路徑有效；`lane_pin --check` exit 0；`blocked=[]`（無欄位取不到） | `out/HOST_READBACK.json`（21,542 B） |
| 分母對帳（P0-03） | 31/31；ImportMap **433 entries／423 distinct paths／3,713,290 B**，其中 **74,127 B 重複計入、定位到 10 個具名 entry**；G19 當期 **41 groups／343 members PASS**；**73/394 已被取代、不可與 41/343 同時宣稱有效**；431 已定位 | `out/P0-03_COUNT_LEDGER.json`（37,473 B） |
| 故障分帳（P1-02） | **99 events = 83 failed ＋ 16 errors**（分母吻合，無湊數）；`REAL_DEFECT 2／HISTORICAL 5／ENV 15／ORIGINAL_OWNER 55／W1_WIRING 22／UNCLASSIFIED 0`；受影波次 `W0 17／W1 32／W2 45／ORIGIN 5` | `out/P1-02_FAULT_LEDGER.json`（83,879 B）＋`.md` |
| L1 結構（§1 補證） | **50 章、五段齊全 50/50**；缺 s1/s2/s3/s4/s5、缺 POS、缺 NEG、缺 consumer、缺 resume **皆為 0** | `out/L1_CH_ALIGNMENT.json`（32,787 B） |

`P1-02` 的 55 筆 `ORIGINAL_OWNER` 是本輪最重要的訊息：多數紅燈不是壞掉，而是**原域尚未裁決**。這正好對應 baseline P1-02 要求的「至少列出 W0/W1 受影未分類部分」——現在未分類是 0，且 W0 受影 17 筆已逐筆有名。

`P0-03` 的 74,127 B 重複計算是舊帳的算式缺陷（同一路徑被兩個 entry 計入），不是檔案損壞；本輪以 distinct path 重算，並在台帳裡指名那 10 個 entry。

---

## 3｜W0 六個 Primary WP（L2 §04 的集合）

| WP | 本輪可見的 Trace | Done | 缺口（實測） |
|---|---|---|---|
| `WP-FHS-00` Source/Host Discovery | `provenance/SOURCE_IMPORT_MAP.json`（433 entries／423 distinct paths／3,713,290 B）＋31/31 語料 gate | **有** | 無 |
| `WP-FHS-01` Authority/Oracle/Profile | `_local/W0_SPEC/SPEC-C_PROGRAM_W0.md §3`（U0–U4 五行散文） | **無** | **AuthorityConflictLedger＋Oracle/ProfileBinding 無檔**（typed ledger 缺） |
| `WP-FHS-15` TPM Corpus & SPEC 18Stage | 三份異質 SPEC＋`spec_identity` exit 0 | **有** | 18 Stage 只做 T3 |
| `WP-FHS-16` Donor/Method Slot Translation | L0 §07.6A 485 槽敘述；OpenSpec 1.8.0 實測、gstack 缺席 | **無** | **24 donor／25 method 壓製候選＋485/485 四欄處置表無檔** |
| `WP-FHS-19` CI/Supply Chain & Requal | PR #25／#68 | **無** | **CI／License／NOTICE／SBOM 同 CandidateSHA 的掃描 Raw 無檔**（repo 未配置 required checks） |
| `WP-FHS-21` Challenge 96/H4/SEAM Coverage | 本件 §2.3／§2.4 的 8 個 NEG | **無** | **96 Case 的 per-case POS/NEG/FirstFail CasePlan 無檔**（只有 seam 鏈圖） |

即 **2/6 有 Done 證據、4/6 只有 Trace 沒有 Done**。這是 P0-09 的真實狀態，不是「已結案」。

---

## 4｜W1 入口（可交接的條件）

W1 的入口不是「文件寫完」，而是這四條同時成立（L2 §04 W1）：

1. **同 Source/Subject 的三 SPEC 可被原 SBL PIPD 重解析** → 目前只有 `spec_identity_check`（作者端身分），原 Compiler 未載入（`H-READER`）。
2. **RepoContext 真值**：Git root／HEAD／index／dirty／untracked／ACL／exact WriteSet → 本輪未開任何 W1 WriteSet。
3. **最小 Host 能力綁定**：`WP-FHS-17` 依 `00/02/03`，不得反加 `WP06→WP17` 循環。
4. **Owner 對首個 WriteSet 的有界授權** → 這就是 owner envelope 這次開窗的用途之一。

本輪不建立新 Repo、不改三庫 main、不派 W2 受保護效果。

---

## 5｜被排除項與非目標（同 r1，未放寬）

- 不重建 W0、不建第二個 SourceFreeze、不產生第二個 PIPD Writer。
- 不以文件完成、CI 綠、PR merge、模型 served 冒充 Original ACK／Native／Independent／Release。
- 不對 485 槽做全安裝；不把 `REFERENCE_ONLY` 安裝成 Tenant；不把 `METHOD_ONLY` 假裝成 binary。
- 不在 `Fabric/ SBL/ HG-KSEOS/` 內改檔；所有原域修補只提 Candidate/PR。

---

## 6｜HOLD 台帳（具名、含 FirstFail 與 Resume）

| HOLD | 只影響 | FirstFail（實測） | 解除條件（Resume） | 誰能解 |
|---|---|---|---|---|
| `H-READER` | 原 Canonical PI/PD/ECP/TQAEP 的正式接受 | `spec_identity` 只證作者端身分；原 Compiler 未載入 | 原 SBL PIPD Reader 對同 Subject/Source 回 ACK；可用 owner 信封的 `original_reader_ack` 簽 | 業主／SBL PIPD 原 Reader |
| `H-H16` | Protected SoD 的「真獨立」聲明 | 三 NEG 會拒，但豁免路徑的 nonce 未成立 | 不同受保護憑證的 Checker 對同 Case/Raw 出 verdict | HGK Trust／Protected Checker |
| `H-ENTRY` | Fabric NAV 當授權 | `effect_permission=NONE` | 原 Fabric Policy Consumer 的 ActiveEpoch＋LoadedDigest＋ACK | Fabric Policy Owner |
| `H-POS02` | `selfcheck` 16/16 | origin 子樹被知識庫重組移走 → `POS-02` 定位失敗；但 `POS-02b` 證明兩檔 pin 全對（`PASS_PIN_ONLY`，`source_absent=true`） | owner 對 `POS02_LOCATOR_CANDIDATE.md` 裁定「以 `control_seed.target_sha256` 為 pin、source 缺席不判 FAIL」後改判準 | **業主（已備簽）** |
| `H-GUARD-EPOCH` | Guard 的 epoch 一致性 | `live_epoch=44` vs registry 41（欄位錯接） | 原域 merge 附錄 G 的 patch 後重跑 guard | HG-KSEOS 原 Owner |
| `H-RETIREMENT-BOUNDARY` | 「退役臂在所有路徑都不可達」 | 派送層 4/4 拒，但 relay 直呼仍 200 | 原域封閉 relay 直呼邊界（身分或 ACL） | HG-KSEOS／relay Owner |
| `H-G16B` | Full-scan Closure | 無 `hgk-main` 完整 checkout，`scan_complete` 無法為 true | 原 HGK pinned ref 完整 checkout 後重跑 | HGK 原 Owner |
| `H-L1-OWNER-ACK` | 「L1 已可取代 31 冊」 | L1 50 章結構已存在，但 Owner 語義核簽未取得 | 原 Owner 逐 CH 核簽（U4） | 業主／原 Owner |
| `H-CASES-09` | 96 Oracle／282 B1 的獨立驗收 | 未綁原 Runner | 原 Case Registry 綁 runner/oracle/Raw | 原 Case Owner |
| `H-W18-10` | Normal Mode 資格 | 未以 fresh PID 跑 E33–E42 | 新 PID 普通 Goal 的 served Raw | Hermes Host |

**這一輪真的解掉的**：`H-USAGE-EXECUTE`（relay home 修正後 usage 落地）、`H-MANDATE-PLAN-VERIFY`（force-rank 至 chain 內同一臂後 PLAN/VERIFY 均 served）。這兩個是我上一輪的**操作錯誤**，不是原域限制，已用 Raw 更正。

---

## 7｜下一步（有界、可驗）

1. **W1 首個 WriteSet 授權**：等 owner 給 exact WriteSet 後，才做 `WP-FHS-06` 的前置檢查；在此之前不碰任何 Repo 寫入。
2. **原域 patch**：把附錄 G 的 `_live_epoch` patch 以 branch＋PR 送 HG-KSEOS（candidate only，不合併）。
3. **L1 逐 CH 缺口**：依 `out/L1_CH_ALIGNMENT.json` 的缺件章號，補 L1 自身（不是本件）的 POS/NEG 段。
4. **G16b**：取得完整 `hgk-main` 後重跑，`scan_complete` 必須為 true 才能談 Full Closure。

---

## 8｜回退

- 本件與附錄皆為新檔，不動 r8／r26／AsBuilt 原件；刪除即回退。
- `control/` 兩檔若依 owner 裁決改判準，只改 `ops/selfcheck.py` 的 `pos_control_seed` 語義並保留 `POS-02b` 轉錄 pin 檢查，不改兩檔內容。
- 車道回執與 NEG 回執全部落在 `W0_R7_FULL_20261114/out/`，可獨立重跑（附錄 H 的命令）。

---

*本件由 `fhs_next` profile 於 2026-11-14 產生。所有 PASS 皆可回指附錄中的命令與 Raw 路徑。*
