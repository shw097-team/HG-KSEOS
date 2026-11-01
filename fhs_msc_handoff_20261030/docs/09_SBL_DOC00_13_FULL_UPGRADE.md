<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 09 SBL DOC00 13 FULL UPGRADE｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：14冊 SBL 原意與逐DOC原條款／Consumer

## 十四冊 SBL 原產品：逐 DOC 直接可用的具名 Reader／功能回歸條款

本節為 FHS 跨域整合設計 Reader，不更名、不覆寫 SBL DOC 的 Canonical Writer。下列原文取自本輪具名物理 DOC；其各自原產品條款以來源文脈與原負例為準，若截取片段與完整 Parent 有差異，必須回完整來源定位並設 `SOURCE_CONTEXT_HOLD`。各 DOC 的新跨域接入均應遵守原 Scope／Consumer，以下 excerpt 為可操作輸入而不是語義全量證明。

### SBL DOC-00｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-00(1).md`；SHA-256 `bd9c1a85ea0cae68fa8cde617e5592fca6123f72b4caf1a9d2894167d9a82e01`；原章節定位保留；Canonical Writer = 原 SBL DOC-00 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-00｜R00.r3.1｜五分鐘產品操作契約與七痛點→實體成果｜來源 L53–L69</summary>

## R00.r3.1｜五分鐘產品操作契約與七痛點→實體成果
人類入口 `goal + source_locator（可為待提供的查詢結果而非已凍結） + requested ProductKind + mode`；TPM 問最多一個**已被來源核對確有必要**的阻擋問題（單問僅為設計 UX 假說，不是已實測閾值），輸出 `GoalCard`、`MethodDecision` 和可讀 `MissingInput`。若只有 goal 而無來源，顯示「需一份文件或合法來源路徑」並可先進行無效應探索，不虛構 PI 或開始施工。七痛點的「成果」是以下可操作功能，非抽象品質宣言。
| Pain | 來源痛點 | SBL 產品行為 | 所借輪子／Owner | Input→可讀 FUO | 首次拒收 NEG | Moments／Journey | 詳規 DOC |
|---|---|---|---|---|---|---|---|
| P01 | 選型困難 | 目標→風險／Host／TaskKind 分流；返回 MethodDecision 的推薦、排除原因與 no-fit | MP-01；TPM-SP／DOC03 | GoalCard → RouteCard{selected,excluded,reason,missing} | 未定位來源卻輸出 install 命令 | M00-M02／GJ01 | DOC01/03/06 |
| P02 | 跨工具交接斷裂 | 以 subject_sha／typed_ref／owner／schema_version 關聯 PI/PD/DELIVER，只把 proposal 翻譯進合法 Writer | P4 route→PI→PD | HandoffEnvelope → typed ACK/NACK | 異主體或 stale head 被 ACK | M03-M06／GJ02 | DOC02/05/09 |
| P03 | 重問與決策遺失 | QuestionLedger 記 qkey／source sha／decision version，同版本不重問；變更需重算依賴 | Matt grill-with-docs；DecisionLedger | AnsweredQuestionSet → DeltaQuestions | same hash 反覆問或 source drift 不重問 | M01-M03／GJ01 | DOC01/03/10 |
| P04 | Writer 碰撞 | Typed OwnerMap 先定唯一 PIPD/HGK/SWOF Writer；OpenSpec/Spec Kit 僅 proposal | OpenSpec；Spec Kit→PIPD | SourceDelta → ReqAtomProposal | 由 SBL 直接宣稱正式 PI-PKG、Native Permit | M03-M07／GJ02 | DOC02/04/05 |
| P05 | 虛假 PASS | 同 subject SHA 的 POS/NEG 及真 RawReceipt；Checker 不同 principal 且有實體收據 | Superpowers；gstack；P4 TQAEP | TestCandidate → TQAEP/IndependentFinding | maker 自簽或 exit=0 且 0 tests | M08-M10／GJ02 | DOC08/09 |
| P06 | 宿主掛載失真 | 每 Host install/register/effective-load/trigger/deny/uninstall/readback | GENIEMAKER；Host Adapter | InstallSession → HostEffectivenessProof | 只有 ZIP/SKILL.md，loader 未列舉 | M14-M15／GJ03 | DOC10/12 |
| P07 | 最後一哩 FUO 缺失 | 新環境手動使用得到結果並能撤銷；Provider-off 走功能受限路徑 | DeliverBOM/Consumer UAT | Build → ConsumerOutcome/UninstallReceipt | 只有 README 或模擬沒清楚標示 | M12-M15／GJ01-03 | DOC12/13 |

**共同 UX 量測協議**：每個 FUO 回報 `persona,clean_start,source_sha,selected_path,first_useful_output,elapsed_ms,questions_reasked,error_count,provider_off,consumer_acceptance`。本文建議將 P03 同來源重問目標設為 0、每 Journey 回合使用者主觀「可用」且可重播；所有時效及操作次數為 **UAT 待量測門檻**，非已達標 KPI。`READ_ONLY_DESIGN` 時僅有可檢閱 Spec，不宣稱 CLI 已可執行。


# C02｜上位藍圖、設計規劃與文件來源的憲制／裁決優先序

</details>

<details>
<summary>DOC-00｜C02.r3.base.1｜五權威域並列，不因較新時間跨 Owner 奪權｜來源 L70–L80</summary>

## C02.r3.base.1｜五權威域並列，不因較新時間跨 Owner 奪權
| Domain | Formal Writer / Owner | 此 DOC-00 可投影 | 禁止的跨域替代 | 首敗 |
|---|---|---|---|---|
| SBL 產品/UX | SBL Product Owner + `SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md` | FUO、三 SP、八 ProductKind、GJ/ModeGate 的設計 reader | 本 DOC 寫第二 Product Truth | `SBL_PRODUCT_AUTHORITY_MISMATCH` |
| PIPD PI/PD | `PIPD-LIFECYCLE-SPEC@1.1.0`＋ PIPD DOC-00～09 各 Writer | 只讀 S0～S8 製程、TypedRef、Claim Ladder | OpenSpec/SpecKit/SBL 原文冒充正式 PI/PD | `AUTHORITY_UNKNOWN` |
| SWOF | SWOF Canonical/ABI/Release/Domain Owner | 7 PrimaryKinds/231 Entity/59 Relation/72 MC source-bound projection | SBL 建立新 SWOF identity/同名覆寫 | `DOMAIN_OWNER_MISMATCH` |
| HGK/Fabric | HG-KSEOS sole Native control plane；Fabric policy / Hermes runtime 分域 | Token、Effect、Readback/rollback 的預期契約 | 由 DOC-00、Skill 文案自行核准效果 | `NATIVE_PERMIT_MISSING` |
| Independent / Human | 真獨立 Checker principal + 人類 Release Owner | 預期判準、Negative Fixture、證據清單 | Maker 自簽獨立 PASS／生成 Human Token | `SOD_VIOLATION` |

**已核對的敏感衝突** `CR-ORACLE-001`：P4 `pipd-pi-compile/skill.md` 寫 `oracle_source=DOC-03 DOMAIN_ORACLES`，而 PIPD `DOC-07` 為 Verification/Oracle/Fixture 正式 writer；二者為不同抽象/來源，並非單憑名稱即可認定必然衝突或等價。直到原 PIPD Owner 提供 `OracleBinding` 指向的 `oracle_id/predicate_hash/version` 且批准映射，不得向 PI 編譯器注入臆造 alias；受影需求 `ORACLE_BINDING_HOLD`，未受影的只讀導覽可繼續。

</details>

- **跨域修補的 FirstFail**：`DOC00_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-01｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-01(1).md`；SHA-256 `43a0a7ed26d2adf9c2803062032019ccb6acce27cebb49af4d37c3cd4b0a3a2f`；原章節定位保留；Canonical Writer = 原 SBL DOC-01 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-01｜產品讀者五分鐘 Quickview（當前設計正文入口）｜來源 L22–L57</summary>

## 產品讀者五分鐘 Quickview（當前設計正文入口）

| 讀者現在要做的事 | 讀取位置 | 可得到的具體結果 | 不可推論 |
|---|---|---|---|
| 用一句目標產生可用產品 | C01、C04、C08、C10/GJ01 | 狀態明確的 ProductIntent 與可安裝 CLI BOM、成功與拒收行為 | 已經實際安裝 |
| 拆分所有使用者義務 | C05.1、C05.2、R09.4B | 50 parent＋149 逐子 POS/NEG、來源上下文與 Owner HOLD | 149 Native Owner 已批准 |
| 選 Kind/Mode/Host/Risk | C06、C10/GJ03 | 24 Cell 與四宿主條件式能力路線 | Host effective load 已完成 |
| 使用現有輪子，防止重造 | R08.1、R08.2、R10 TechnologyAdmission | 六 Donor、25 方法、24 NOBJ、386 來源項與 25 TAD 逐名路由 | 所有工具均可安裝或已驗 License |
| 跨 DOC 交接與可拒收 ABI | R01、R10.10 | 單一 ProductIntent Proposal ABI、九 SPEC 欄位契約與 NACK | DOC-01 具有 Native Compiler 權限 |
| 執行被治理工作或正式獨立驗收 | PIPD 原生流程 DOC-00～09、HGK/Fabric、DOC-08 | 本文提供產品輸入契約與可重播測例 | r3 自行簽發 SourceFreeze/Permit/Checker |

---
artifact_id: SBL_PIPD-LS-PKG_DOC-01
artifact_name: SBL_PIPD-LS-PKG_DOC-01.md
formal_name_zh: 產品需求、PrimaryKind、使用旅程與體驗契約
formal_name_en: Product Requirements, Kinds & Human Journeys
short_name: PRODUCT_JOURNEY
document_type: FULL_SUBSTANTIVE_PRODUCT_DESIGN_BODY
version: 2026-10-18_r3_DOC01_SUBSTANTIVE_SOURCE_INTEGRATED_AUTHOR_SIDE
observation_date: 2026-10-18
language: zh-TW
root_task_kind: DESIGN + SOURCE_BASED_RESEARCH + FULL_CORPUS_RECONCILIATION + AUTHOR_SIDE_VERIFICATION
upper_sbl_authority: SBL_MASTER_v2.0r1
pipd_canonical_standard: PIPD-LIFECYCLE-SPEC@1.1.0
product_owner: SBL_PRODUCT_OWNER_RATIFICATION_PENDING
editorial_role: SBL-R001
source_status: LOCAL_READABLE_WITH_PROFILE_GRP_GAP
formal_source_freeze: HOLD
n14_status: PROVISIONAL_OWNER_RATIFICATION_PENDING
oracle_conflict: CR-ORACLE-001_OPEN
native_effect: NOT_EXECUTED
independent_acceptance: NOT_EXECUTED
release: NOT_EXECUTED
claim_ceiling: AUTHOR_SIDE_SUBSTANTIVE_DESIGN_DELIVERED_WITH_TT_NOT_FORMALLY_QUALIFIED
---

</details>

- **跨域修補的 FirstFail**：`DOC01_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-02｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-02(1).md`；SHA-256 `4ff0cda5ab00ba5f577151e5b004d2167d933e912e302c9e3529b237ccb9e035`；原章節定位保留；Canonical Writer = 原 SBL DOC-02 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-02｜r1 可核回保留之 RoleActivationMatrix／Authority Graph（以 r2 上段為準）｜來源 L88–L89</summary>

## r1 可核回保留之 RoleActivationMatrix／Authority Graph（以 r2 上段為準）

</details>

<details>
<summary>DOC-02｜六步可重現來源掃描與分母／失敗狀態｜來源 L124–L134</summary>

## 六步可重現來源掃描與分母／失敗狀態

**S1 Index** 為每卷核對 `Volume Metadata / Source Count / - [SRC-*]`；**S2 Operative** 把完整檔案逐行解碼、保留前後文且不混用 Index 作正文；**S3 Terms** 掃描中英義務/否定/Owner/State/ABI/Hash；**S4 CrossCheck** 指向上位、PIPD 及 Donor Owner；**S5 Atomize** 先列候選 Parent、AND/OR、每一量詞 Child；**S6 Disposition** 逐條加上 SourceSpan、實質設計落點、Owner、FirstFail、驗收與證據。S1～S3 的機械掃描可以通過；S4～S6 對所有相關 substantive clauses 的判定仍未全量完成，因此不使用 FULL_SCAN_PASS 字樣。

來源分母如下： `D_physical_md=186`；`D_index_fragments` 僅對具有顯式 Source Index 的卷逐卷統計；`D_donor_physical` 與本地實體重疊；`D_web_url` 非本地 bytes；`D_clause_semantic=UNRESOLVED`。不允許空分母自動 PASS、把候選 token 計為 adopted atom，或只因全文含有字串便宣稱覆蓋。

# C03｜全來源凍結、來源索引、全文研究、SourceClause Ledger 與零無聲漏失

任何 index、keyword 或卷級來源皆只是 locator；FullSourceSpanMap 保留實際物理資料 bytes 與 line span。SBL 在此只建設防漏資料層，不得簽 Native SourceFreeze。

</details>

- **跨域修補的 FirstFail**：`DOC02_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-03｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-03(1).md`；SHA-256 `ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476`；原章節定位保留；Canonical Writer = 原 SBL DOC-03 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-03｜C18.2｜SBLAtom → P4 CanonicalAtom 無損 Adapter；不得直接送 Native｜來源 L952–L996</summary>

## C18.2｜SBLAtom → P4 CanonicalAtom 無損 Adapter；不得直接送 Native
P4 `pipd-pi-compile` **輸入 Schema 嚴格禁止額外欄位**：`goal`（非空）、`intent(subject_id,content_hash)`、`profile ∈ {LITE,STANDARD,ASSURED}`、`atoms[]`（minItems=1），每 atom 必須有 `req_id ∈ {REQ-INTENT,REQ-KNOWLEDGE,REQ-VERIFY,REQ-DELIVER,REQ-GOVERN}`、`source_clause`, `owner = PIPD-EC`, `acceptance_cue`, `risk_guard`。把 `U03.1` 或 `SBL03-REQ-*` 直接送 `req_id`，或送 `owner=SBL_PRODUCT_OWNER`，均是 schema 驗收失敗，而非補個其他欄位就通過。
**受控轉換算法設計**：
1. SBL `SBLAtom` 保留 `sbl_atom_id,parent_id,original_owner,source_sha256,source_line,behavior,negative,acceptance,product_kind,mode` 在**另外的 ReadOnlyCrosswalk**；由專屬 `AdapterRegistry` 鎖 `sbl_atom_id ↔ canonical_axis(req_id) ↔ P4 source_clause ↔ Native Atom content_hash`，不把 crosswalk 當 P4 extra key。
2. `req_id` 五類按原意映射：`REQ-INTENT`=目標/功能、`REQ-KNOWLEDGE`=資料/來源、`REQ-VERIFY`=測試/安全、`REQ-DELIVER`=交付/Host、`REQ-GOVERN`=Owner/Gate/Release；一個 SBL child 可投影成數個不同軸 atoms，但一個 P4 input atom 只佔一個五枚舉值，必須保留覆蓋矩陣和 count。
3. `owner=PIPD-EC` 是 Native compiler record 的固定角色，不覆寫 SBL source original_owner；將 SBL original owner 放在 ReadOnlyCrosswalk，並在 `source_clause` 以穩定 admitted locator＋hash 綁可逆源 URI（不偷渡 P4 sidecar）。
4. `decode(encode(atom))` 必等於原 `sbl_atom_id,source_clause,owner,behavior,negative`；碰到相同 source_clause 多個 child 而不能反解 → `ADAPTER_NOT_LOSSLESS/HOLD`。`req_id` 只有五值，不可用其取代 149 unique identities。
5. P4 output `acceptance.mode="bound"` 的 `oracle_source=DOC-03 DOMAIN_ORACLES` 是其 **目前已安裝 schema const**；本設計不謊稱已由 PIPD DOC07 Owner adjudicate。受影 Native compile/acceptance `CR-ORACLE-001` OPEN 時 `PI_PROMOTION_HOLD`，此為資料衝突而非可以繞過 schema 的 fallback。

**可測適配實例**（SBL proposal；不是 Native P4 input）：
```json
{
  "sbl_atom_id": "U03.1",
  "parent_id": "U03",
  "source_sha256": "83ea1bef8d045bf0a100a27599fcb2d51b1e9ed993d6ccc5c7d70708753dd747",
  "source_line": 5506,
  "source_clause": "SBL Master v2.0r1 U03 Web GPT 三 SP 可真正安裝",
  "original_owner": "SBL_ARCHITECT_OWNER",
  "axis": "REQ-DELIVER",
  "behavior": "Host must emit separately scoped install receipts per SP",
  "negative": "one SP missing receipt must not pass"
}
```
**型別正例 fixture**（synthetic valid-shape only, `INTENT-111…`/hash 為刻意測試值，不能聲稱是實際 IntakeCard）：
```json
{
  "goal": "Produce a source-bound SBL Host Skill installation contract",
  "intent": {
    "subject_id": "INTENT-1111111111111111",
    "content_hash": "2222222222222222222222222222222222222222222222222222222222222222"
  },
  "profile": "STANDARD",
  "atoms": [
    {
      "req_id": "REQ-DELIVER",
      "source_clause": "sbl://SBL-MASTER/U03.1@sha256:83ea1bef8d045bf0a100a27599fcb2d51b1e9ed993d6ccc5c7d70708753dd747",
      "owner": "PIPD-EC",
      "acceptance_cue": "distinct host receipt and positive/nontrigger for TPM-SP",
      "risk_guard": "do not claim installed from a file copy"
    }
  ]
}
```
| Mutation | 預期 first-fail | 不容許降級為 |
| --- | --- | --- |

</details>

- **跨域修補的 FirstFail**：`DOC03_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-04｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-04(1).md`；SHA-256 `ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0`；原章節定位保留；Canonical Writer = 原 SBL DOC-04 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-04｜C12.2 修補後六個 Flow Modules（各有輸入、輸出、Owner、Consumer、FirstFail）｜來源 L292–L302</summary>

## C12.2 修補後六個 Flow Modules（各有輸入、輸出、Owner、Consumer、FirstFail）

| Module | 功能 | 具型別輸入 | 具型別輸出 | Writer boundary | Reader | 首失效 |
|---|---|---|---|---|---|---|
| M1 | Intake | GoalCard+persona+ProductKind | IntentDraft+QuestionLedger | SBL M1 design | M2/TPM | NO_SOURCE→INTAKE_HOLD |
| M2 | Authority | SourceLocator+Readset | SourceBindingCandidate+Conflict | PIPD source owner | M3 | SOURCE_DRIFT→FREEZE_HOLD |
| M3 | SPEC | BoundAtoms+canonical PI ref | SpecProjection+AccRefs (read only) | PIPD Compiler | Commander | SECOND_WRITER→DENY |
| M4 | Reuse Resolver | CapabilityNeeds+license policy | SlotAdmissionCandidate+NoFit | DOC-06 Admission Owner | M5 | PIN_MISSING→INSTALL_HOLD |
| M5 | Execution Handoff | Valid PI/PD/ECP refs+scope | NativeHandoffRequest (not Issued ECP) | CAPC/HGK Receiver | M6 | TOKEN_ABSENT→NACK |
| M6 | Evidence Closure | RawReceipt refs+Findings | ClaimProjection+RepairConeRef | PIPD/TQAEP/Native Oracle | C15/Reader | RAW_MISMATCH→REQUALIFY |

</details>

<details>
<summary>DOC-04｜R04｜跨域 Typed ABI、HashLineage、Envelope、ACK/NACK 與安全資料流｜來源 L210–L254</summary>

## R04｜跨域 Typed ABI、HashLineage、Envelope、ACK/NACK 與安全資料流

所有 SBL 跨域物件採 `schema_version + producer + consumer + subject_sha256 + source_ref + issuer + authority_namespace + timestamp + payload_ref + explicit_status + first_fail` Envelope；SBL 可寫草稿 Projection，`NativeReceipt/Permit` 由原 Writer 簽發且不可逆向冒名。`HashLineage` 同時綁 `source_hash / candidate_hash / repo_HEAD / evidence_manifest_hash / native_receipt_subject_hash`，任一不符先 NACK 再終止。

```json
{
  "example_only": true,
  "schema_version": "sbl.reader-envelope.design/1",
  "object_type": "NativeHandoffRequest",
  "producer": "Commander-SP/design-only",
  "consumer": "HGK-native/admission-reader",
  "source_ref": "REQUIRES_REAL_SOURCE_HASH",
  "subject_sha256": null,
  "repo_head": null,
  "work_order_ref": null,
  "ecp_ref": null,
  "permit_ref": null,
  "candidate_scope": ["affected/path-only"],
  "effect_intent": "NONE_UNTIL_NATIVE_APPROVED",
  "claim": "PROPOSAL_ONLY",
  "first_fail": "UNBOUND_NATIVE_CONTEXT"
}
```

**InterfaceRegistry** 的每一 row = `{iface_id, schema_version, producer_owner, consumer_owner, mandatory_fields, canonical_writer, compat_policy, source_sha, rollback_rule, ack_contract}`；若版本不相容需明示 AdapterCompatibility 的 `minor-compatible / major-break / dual-read migration / reject`，不得 silent alias。TypedRef 只指向 Owner 的合法內容定址物件，禁止 SBL 生成冒充 Native 的 `WorkOrderRef/ECPRef/PermitRef/ExecutionReceipt`。

| Object | Draft producer | Canonical issuer/writer | Consumer | ACK / NACK |
|---|---|---|---|---|
| `SourceInventory` / `SourceFreezeCandidate` | SBL Source Reader | PIPD SourceFreeze（另需 Profile） | PIPD PI | `FROZEN` / `PROFILE_GRP_MISSING` |
| `IntentCard` / `PI-PKG` | SBL goal projection only | PIPD EC/PI | PD binder | canonical ref / `PI_SEMANTIC` |
| `PD-PKG` / `RepoContext` | candidate only | PIPD PD | ECP Owner | bounded scope / `REPO_CONTEXT_MISSING` |
| `TaskSpecSeed` / `ThinPromptProjection` | TPM/Commander | SBL design reader | Native CAPC | content bind / `PROMPT_NOT_EFFECT` |
| `NativeHandoffRequest` | Commander | HGK admission reader accepts/rejects | HGK | actual response / `TOKEN_MISSING` |
| `WorkOrderRef` / `ECPRef` / `PermitRef` | never SBL issuer | respective PIPD/CAPC/HGK Native Owner | HGK runner | signed token / deny |
| `ExecutionReceipt` / `EvidenceRef` | never SBL issuer | Native Runner / independent checker | TQAEP/SBL evidence projection | subject-bound raw / `EVIDENCE_GAP` |
| `SWOFReceiverACK` | no SBL issuer | Published SWOF Receiver | Connected SBL | owner ACK / `READY_W3_MISSING` |

**Host EffectiveLoadReceipt**（欄位示例，`ILLUSTRATIVE_NOT_EXECUTED`）必含：`host, host_version, skill_id, manifest_sha, source_pin, issuer_principal, capabilities, install_dir, discover_ok, bind_ok, trigger_input_ref, trigger_raw_result, exit_code, unload_verification, provider_off_parity, observed_at, candidate_hash, signature`；空 trigger 或只有 install log 必回 `HOST_NOT_EFFECTIVE`。Web GPT 不聲稱本地 CLI / Repo install；四 Host 都須獨立正／負測試。

```mermaid
sequenceDiagram
 participant U as User
 participant S as SBL TPM/Commander
 participant P as PIPD Native
 participant H as HGK Native

</details>

- **跨域修補的 FirstFail**：`DOC04_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-05｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-05(1).md`；SHA-256 `3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27`；原章節定位保留；Canonical Writer = 原 SBL DOC-05 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-05｜R00.2 入口、前提、出入口與 FirstFail｜來源 L53–L70</summary>

## R00.2 入口、前提、出入口與 FirstFail

### R00.2.A｜來源入口原子化及保守拒收：原版反證與核心設計保留
**本域反證入口**：用空 source_refs 的輸入測入口。**輸入／判準**：輸入 source_refs=[]，第一失敗 SOURCE_LOCATOR_MISSING，禁止繼續校驗 RepoContext。資料責任維持本節所指定的正式 Owner；此處的 `expected` 是設計 Oracle，不是已執行的 RawReceipt。


**入口型別**：`DOC05DesignRequest{source_refs:[nonempty],candidate_hash:sha256,mode:STANDALONE|PREW3_SHADOW|SWOF_CONNECTED,domain_payload:typed}`；所有正式 Receiver 活動必另有有效 Owner 決策；空來源先 `SOURCE_LOCATOR_MISSING`，假 subject `SUBJECT_HASH_MISMATCH`，SourceFreeze 不成立為 `SOURCE_FREEZE_HOLD`，再看 Repo 與 ECP。

**出入口**：本冊只有 `PDReadProjection`（read_only=true）與 `ECPRequirementEnvelope`（proposal_only=true），以及 NACK／FirstFail／EExp。提案不等於正式 PD/ECP。**POS**：完整欄位與同主體 SHA 產生 `READ_ONLY_DESIGN_PROJECTION`；**NEG**：無 source_refs 直接 NACK，無任何 Native effect；後續憑 raw receipt 才可判定更高階。

### R00.2.B｜歷史 r2 實質協議：來源入口原子化及保守拒收

**原意／機制**：先解析 source_refs[]/candidate_hash/mode/domain_payload，對缺來源直接產 NACK；已缺凍結者仍可形成 blueprint，但不能走 Native binder。**Typed I/O**：`DOC05DesignRequest → TypedPreflightDecision`。**消費路由**：`SBL DOC05 → 原生 PIPD DOC-00／對應 SBL 下游`；製作此文字者不自動是原生 Writer。

**定向 NEG（單欄破壞）**：source_refs 空→SOURCE_LOCATOR_MISSING。**本地失敗邊界**：原生 effect 必保留獨立授權與 world readback，不得從設計 fixture 推斷已執行。

**本節逐原子閉環**：`D05-REQ-R00-2 → SBL-D05-SPEC-R00-2 → ACC-D05-R00-2 → FX-D05-R00-2-POS/NEG → EEXP-D05-R00-2 → DEL-D05-R00-2`。原始 r1 clause=`SBL_PIPD-LS-PKG_DOC-05_%E8%97%8D%E5%9C%96+skeleton_2026-10-18_r1(1).md#L241`，r1 SHA256=`aea120809b40794849449196bba27e01bc795466a64a73c45f5f82da87b40d13`；原生欄位如受影應交 `PIPD_LS_DOC-00` 的有效 Schema/Owner 審核，真實 Native receipt **未取得**。

</details>

<details>
<summary>DOC-05｜R01.3 P4 Skill 安裝可讀狀態、順序與 Owner｜來源 L139–L165</summary>

## R01.3 P4 Skill 安裝可讀狀態、順序與 Owner

### R01.3.A｜P4 原生技能版本與輸入路由：原版反證與核心設計保留
**本域反證入口**：輸入 P4 Skill 與假來源 Locator。**輸入／判準**：pipd-authority-source 需真 digest；missing SHA 不得輸出 SourceFreezeManifest。資料責任維持本節所指定的正式 Owner；此處的 `expected` 是設計 Oracle，不是已執行的 RawReceipt。


| 路由 Skill（實際 URI suffix） | Typed input→output | 前置／FirstFail | 正式 Owner→Consumer | 本次 |
|---|---|---|---|---|
| `pipd-route-intake` | goal+locators→IntentCard | 非空 goal/locator；`SOURCE_LOCATOR_MISSING` | PIPD-EC→source/PI | skill.md READ |
| `pipd-authority-source` | source families+SHA→SourceFreezeManifest | 非空真 SHA、沒有衝突；`AUTHORITY_CONFLICT` | PIPD→compiler | skill.md READ; formal HOLD |
| `pipd-profile-tailor` | LITE/STANDARD/ASSURED+axis→ProfileBinding | 安全 veto 只升不降；`PROFILE_INVALID` | PIPD→PI | skill.md READ |
| `pipd-pi-compile` | frozen IntentCard+atoms→PI-PKG | 每 atom source_clause/owner/acceptance_cue/risk_guard；`PI_SEMANTIC` | PIPD→PD | skill.md READ |
| `pipd-pd-bind` | PIRef+real RepoContext→PD-PKG | 真 root/head/tracked/scope；`REPO_CONTEXT_MISSING` | PIPD DOC-03→handoff | skill+contract READ, NO INVOKE |
| `pipd-execution-contract` | bound PI/PD→ConstructionContract+ECP | Token/rollback/scope；`ECP_PERMISSION` | PIPD ECP→HGK | skill+contract READ, NO INVOKE |
| `pipd-assurance-tqaep` | PI+ECP+distinct checker receipt→TQAEP | maker!=checker；`TQ_SOD` | PIPD TQAEP→checker | skill+contract READ, NO INVOKE |
| `pipd-package-project` | nonempty bundle→ClaimCeiling/TraceClosure | orphan／claim gate；`EVIDENCE_GAP` | PIPD→Reader/Release | skill+contract READ, NO INVOKE |

所有 URI prefix 均為 `skills://plugins/pipd-ls-sp-public-skills-p4/`；`schemas/input.schema.json` 與 `schemas/output.schema.json` 為相應 Native IO，不將此設計例取代 Schema。P4 `pipd-pi-compile` 的 DOC-03 DOMAIN_ORACLES 與 PIPD DOC-07 官方 Oracle 法位存在 `CR-ORACLE-001`，需字段級雙側比對、Owner 裁定前 `HOLD_AFFECTED_ONLY`。

### R01.3.B｜歷史 r2 實質協議：P4 原生技能版本與輸入路由

**原意／機制**：八個 Skill 必按 input/output.schema.json 同當輪實體內容核對；正式輸出和設計投影分開，缺必填不呼叫 Effect。**Typed I/O**：`SkillRef+SchemaRef → CapabilityRouteDecision`。**消費路由**：`SBL DOC05 → 原生 PIPD DOC-00／對應 SBL 下游`；製作此文字者不自動是原生 Writer。

**定向 NEG（單欄破壞）**：未讀 schema 以模型記憶編碼→NATIVE_SCHEMA_UNVERIFIED。**本地失敗邊界**：原生 effect 必保留獨立授權與 world readback，不得從設計 fixture 推斷已執行。

**本節逐原子閉環**：`D05-REQ-R01-3 → SBL-D05-SPEC-R01-3 → ACC-D05-R01-3 → FX-D05-R01-3-POS/NEG → EEXP-D05-R01-3 → DEL-D05-R01-3`。原始 r1 clause=`SBL_PIPD-LS-PKG_DOC-05_%E8%97%8D%E5%9C%96+skeleton_2026-10-18_r1(1).md#L292`，r1 SHA256=`aea120809b40794849449196bba27e01bc795466a64a73c45f5f82da87b40d13`；原生欄位如受影應交 `PIPD_LS_DOC-00` 的有效 Schema/Owner 審核，真實 Native receipt **未取得**。

</details>

- **跨域修補的 FirstFail**：`DOC05_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-06｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-06(1).md`；SHA-256 `64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b`；原章節定位保留；Canonical Writer = 原 SBL DOC-06 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-06｜C32.3｜24/24 Slot：互異 Trigger／非觸發／准許效果／輸出／撤銷；一槽一個來源原子｜來源 L174–L218</summary>

## C32.3｜24/24 Slot：互異 Trigger／非觸發／准許效果／輸出／撤銷；一槽一個來源原子

| Slot | Donor | 保留原能力 | 原行 | POS Trigger | Nontrigger | target EffectClass | Permit/前態 | Observable Output | provider-off 最低成果 | 明確不等價 | FirstFail | pre→event→post/rollback | POS fixture | NEG fixture | 閉環定位 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SLOT-OS-01 | OpenSpec | OS-01: if unclear→Explore; if conflict→TT | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L273 | Explore when ambiguous | 已知且已回答問題不重新發問 | READ_SOURCE | SOURCE_READ（只允許合法來源/無權則 NACK） | DecisionLedger+QuestionDelta | 來源引用的問題清單 | 不要把未知補成事實 | NACK_SOURCE | 撤銷訪問→CANCELED, no extra read | POS SLOT-OS-01: Explore when ambiguous → DecisionLedger+QuestionDelta raw-bound | NEG SLOT-OS-01: 無權讀取來源/來源 hash 改變 → NACK_SOURCE | SPEC-C32-SLOT-OS-01/ACC-C32-SLOT-OS-01/TEST-C32-SLOT-OS-01/EEXP-C32-SLOT-OS-01/DEL-C32 |
| SLOT-OS-02 | OpenSpec | OS-02: diff current spec to requested behavior | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L274 | CurrentHEAD+desired scope bounded diff | 未提供 RepoContext 或當前基準不是同 HEAD | READ_DIFF | REPO_READ（exact Repo HEAD + allowed paths） | SpecDelta+ChangeProposal | 本地可檢視 diff 和路徑差異 | 不得自動 apply | NACK_SCOPE | HEAD漂移→STALE_DIFF，重新取 HEAD | POS SLOT-OS-02: CurrentHEAD+desired scope bounded diff → SpecDelta+ChangeProposal raw-bound | NEG SLOT-OS-02: Repo HEAD stale / out-of-scope → NACK_SCOPE | SPEC-C32-SLOT-OS-02/ACC-C32-SLOT-OS-02/TEST-C32-SLOT-OS-02/EEXP-C32-SLOT-OS-02/DEL-C32 |
| SLOT-OS-03 | OpenSpec | OS-03: apply only legal write paths then verify | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L275 | Approved Change+WriteSet+Native ECP | 沒有 Write Token／WriteSet 或受保護路徑 | GOVERNED_REPO_WRITE | NATIVE_ECP_REPO_WRITE（token+head+Scope SoD/at-most-once） | ChangeSet+ApplyReadback | 生成 diff+人類 Apply 步驟 | 不是已寫入 Repo | ECP_PERMISSION_DENIED | 許可撤銷→BLOCK; rollback exact preimage | POS SLOT-OS-03: Approved Change+WriteSet+Native ECP → ChangeSet+ApplyReadback raw-bound | NEG SLOT-OS-03: path escape / token absent / nonce replay → ECP_PERMISSION_DENIED | SPEC-C32-SLOT-OS-03/ACC-C32-SLOT-OS-03/TEST-C32-SLOT-OS-03/EEXP-C32-SLOT-OS-03/DEL-C32 |
| SLOT-OS-04 | OpenSpec | OS-04: archive only when truth & trace settled | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L276 | Verified change + trace closed archive | TT 未閉合或 evidence subject SHA 與包不一致 | GOVERNED_ARCHIVE_METADATA | NATIVE_ARCHIVE_OWNER（closure ACK + subject SHA） | ArchiveRecord+Supersession | 產生 archive candidate 記錄 | 不是已封存 | NACK_ARCHIVE | 閉合撤銷→ARCHIVE_BLOCKED; restore prior ref | POS SLOT-OS-04: Verified change + trace closed archive → ArchiveRecord+Supersession raw-bound | NEG SLOT-OS-04: unclosed evidence/stale package → NACK_ARCHIVE | SPEC-C32-SLOT-OS-04/ACC-C32-SLOT-OS-04/TEST-C32-SLOT-OS-04/EEXP-C32-SLOT-OS-04/DEL-C32 |
| SLOT-SK-01 | Spec Kit | SK-01: carry precedence into all downstream artifacts | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L277 | Product kind + Constitution + non-goals | 來源 lower-rank 嘗試覆寫安全/法律條文 | READ_CONSTITUTION | PIPD_DOC01_READ（只可產候選映射） | ConstitutionBinding | 清晰非目標/風險清單 | 不能發布第二 Constitution | NACK_AUTHORITY | 來源章節變更→STALE_BINDING, rebind | POS SLOT-SK-01: Product kind + Constitution + non-goals → ConstitutionBinding raw-bound | NEG SLOT-SK-01: Constitution source missing / precedence mismatch → NACK_AUTHORITY | SPEC-C32-SLOT-SK-01/ACC-C32-SLOT-SK-01/TEST-C32-SLOT-SK-01/EEXP-C32-SLOT-SK-01/DEL-C32 |
| SLOT-SK-02 | Spec Kit | SK-02: clarify only new high-value unknowns | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L278 | Unknown requirement + value of information | QuestionLedger 已有答案或不影響 ACC | READ_CLARIFICATION | PIPD_PI_INTAKE（每 Atom source_clause owner risk acceptance） | RequirementAtom+ACCSeed | 只問尚未明確的高價值問題 | 不是正式 PI compiled | PI_NOT_READY | 答覆變動→invalidate affected atoms | POS SLOT-SK-02: Unknown requirement + value of information → RequirementAtom+ACCSeed raw-bound | NEG SLOT-SK-02: zero atoms / missing acceptance cue → PI_NOT_READY | SPEC-C32-SLOT-SK-02/ACC-C32-SLOT-SK-02/TEST-C32-SLOT-SK-02/EEXP-C32-SLOT-SK-02/DEL-C32 |
| SLOT-SK-03 | Spec Kit | SK-03: topologically sort task nodes after dependencies | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L279 | Bounded task nodes + dependency and owner | Task missing owner or DAG cycle | READ_PLAN_DAG | PIPD_PLAN_READ（acyclic + no orphan） | TaskDAG+TopoOrder | 可排序的任務與前置條件 | 不能自動執行 | NACK_DAG | 依賴變更→invalidate topo plan | POS SLOT-SK-03: Bounded task nodes + dependency and owner → TaskDAG+TopoOrder raw-bound | NEG SLOT-SK-03: cycle/orphan → NACK_DAG | SPEC-C32-SLOT-SK-03/ACC-C32-SLOT-SK-03/TEST-C32-SLOT-SK-03/EEXP-C32-SLOT-SK-03/DEL-C32 |
| SLOT-SK-04 | Spec Kit | SK-04: compose only admitted modules | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L280 | Approved workflow manifests with versions | 任一 unpinned extension 或未准入 module | READ_COMPOSE | HOST_WORKFLOW_DISCOVERY（exact schema/extension pin） | WorkflowComposition | 只輸出本地結構化工作流草稿 | 不能偷裝 extension | NACK_UNPINNED_WORKFLOW | 撤銷 module→disable composition | POS SLOT-SK-04: Approved workflow manifests with versions → WorkflowComposition raw-bound | NEG SLOT-SK-04: extension provenance invalid → NACK_UNPINNED_WORKFLOW | SPEC-C32-SLOT-SK-04/ACC-C32-SLOT-SK-04/TEST-C32-SLOT-SK-04/EEXP-C32-SLOT-SK-04/DEL-C32 |
| SLOT-MP-01 | mattpocock/skills | MP-01: route domain need, not donor brand | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L281 | Goal+intent type+host capability | 品牌偏好無任務匹配 | READ_SKILL_ROUTING | HOST_SKILL_REGISTRY（只依 eligible procedure 選用） | SkillRouteDecision | 本地 SKILL.md 路徑/替代步驟 | 無 host load claim | NACK_SKILL_ROUTE | Skill unload→not_eligible then reroute | POS SLOT-MP-01: Goal+intent type+host capability → SkillRouteDecision raw-bound | NEG SLOT-MP-01: unknown trigger or missing dependencies → NACK_SKILL_ROUTE | SPEC-C32-SLOT-MP-01/ACC-C32-SLOT-MP-01/TEST-C32-SLOT-MP-01/EEXP-C32-SLOT-MP-01/DEL-C32 |
| SLOT-MP-02 | mattpocock/skills | MP-02: maximize information gain / known answers never reask | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L282 | Document context+known answers+uncertainty | 重複問題或依賴檔不存在 | READ_QA | TPM_INTERVIEW（可核引用+去重） | QuestionLedger | 有限條高增益問題列表 | 無匿名外部問卷 | NACK_DUPLICATE_QUESTION | 來源重載→重算 unanswered set | POS SLOT-MP-02: Document context+known answers+uncertainty → QuestionLedger raw-bound | NEG SLOT-MP-02: repeat/low information gain → NACK_DUPLICATE_QUESTION | SPEC-C32-SLOT-MP-02/ACC-C32-SLOT-MP-02/TEST-C32-SLOT-MP-02/EEXP-C32-SLOT-MP-02/DEL-C32 |
| SLOT-MP-03 | mattpocock/skills | MP-03: normalize glossary before ADR | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L283 | Glossary terms+boundary+events | Ontology 無來源支持或概念同名衝突 | READ_DOMAIN_MODEL | TPM_SYSTEMS_ENGINEER（語彙對齊 + 來源冲突） | DomainModel+Glossary+ADR | 領域詞彙定義及建模決策 | 不可寫 HGK ontology | NACK_DOMAIN_CONFLICT | Domain owner 覆寫→conflict and rebase | POS SLOT-MP-03: Glossary terms+boundary+events → DomainModel+Glossary+ADR raw-bound | NEG SLOT-MP-03: invented native ontology → NACK_DOMAIN_CONFLICT | SPEC-C32-SLOT-MP-03/ACC-C32-SLOT-MP-03/TEST-C32-SLOT-MP-03/EEXP-C32-SLOT-MP-03/DEL-C32 |
| SLOT-MP-04 | mattpocock/skills | MP-04: atom→task seed and acceptance ref | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L284 | Approved SpecCandidate+ACC+task owner | 無已批准規格或要求遠端 Issue 無令牌 | READ_TASK_SEED | TPM_TASK_FACTORY（Acceptance and owner bound） | TaskSpecSeed+TicketCandidate | 本地可貼到 issue 的候選票券 | 無 remote Issue publish | NACK_ISSUE_PUBLISH | Task source stale→invalidate ticket drafts | POS SLOT-MP-04: Approved SpecCandidate+ACC+task owner → TaskSpecSeed+TicketCandidate raw-bound | NEG SLOT-MP-04: missing accepted spec/remote issue publish → NACK_ISSUE_PUBLISH | SPEC-C32-SLOT-MP-04/ACC-C32-SLOT-MP-04/TEST-C32-SLOT-MP-04/EEXP-C32-SLOT-MP-04/DEL-C32 |
| SLOT-GS-01 | GSD | GS-01: partition immutable refs and task context | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L285 | SourceHash+Goal+Phase context | 既有 Checkpoint sourceSHA 不符 | CHECKPOINT_PLAN_READ | LOCAL_CHECKPOINT（subject and source frozen） | CheckpointManifest | 本地階段草稿+hash | 不能以對話記憶復原 effect | NACK_CHECKPOINT_STALE | source SHA change→EXPIRED | POS SLOT-GS-01: SourceHash+Goal+Phase context → CheckpointManifest raw-bound | NEG SLOT-GS-01: source drift on resume → NACK_CHECKPOINT_STALE | SPEC-C32-SLOT-GS-01/ACC-C32-SLOT-GS-01/TEST-C32-SLOT-GS-01/EEXP-C32-SLOT-GS-01/DEL-C32 |
| SLOT-GS-02 | GSD | GS-02: gate previous phase before next | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L286 | Milestone DAG + gate prerequisites | 純時間點或人工聲稱完成 | MILESTONE_GATE_READ | TPM_PLAN_GATE（evidence before next stage） | MilestoneGateDecision | 列出尚未滿足的 Gate 與下一步 | 無自動 PASS | NACK_MILESTONE_EVIDENCE | Gate 撤銷→HOLD_PRIOR_MILESTONE | POS SLOT-GS-02: Milestone DAG + gate prerequisites → MilestoneGateDecision raw-bound | NEG SLOT-GS-02: missing gate evidence → NACK_MILESTONE_EVIDENCE | SPEC-C32-SLOT-GS-02/ACC-C32-SLOT-GS-02/TEST-C32-SLOT-GS-02/EEXP-C32-SLOT-GS-02/DEL-C32 |
| SLOT-GS-03 | GSD | GS-03: resume after readback and nonce proof | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L287 | Saved Checkpoint+nonce+effect result | 曾被送出但無 readback 的動作想重播 | GOVERNED_RESUME | NATIVE_EFFECT_GATE（readback before replay; at-most-once） | ResumeDecision+EffectReadback | 可安全續讀和整理未完成事項 | 不能重新執行有副作用工單 | NACK_EFFECT_REPLAY | 效果不明→RECOVERY_REQUIRED | POS SLOT-GS-03: Saved Checkpoint+nonce+effect result → ResumeDecision+EffectReadback raw-bound | NEG SLOT-GS-03: nonce replay / unknown effect → NACK_EFFECT_REPLAY | SPEC-C32-SLOT-GS-03/ACC-C32-SLOT-GS-03/TEST-C32-SLOT-GS-03/EEXP-C32-SLOT-GS-03/DEL-C32 |
| SLOT-GS-04 | GSD | GS-04: bind release input sha to test sha | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L288 | Build SubjectSHA+verification+release rights | 未測試或跨 Candidate SHA | RELEASE_READINESS_ONLY | RELEASE_OWNER_READER（non-Publisher review only） | ReleaseReadinessReport | 可讀 release gap 清單 | 不是 Tag/Publish | NACK_RELEASE_READINESS | evidence revoke→HOLD_RELEASE | POS SLOT-GS-04: Build SubjectSHA+verification+release rights → ReleaseReadinessReport raw-bound | NEG SLOT-GS-04: foreign receipt/missing signer → NACK_RELEASE_READINESS | SPEC-C32-SLOT-GS-04/ACC-C32-SLOT-GS-04/TEST-C32-SLOT-GS-04/EEXP-C32-SLOT-GS-04/DEL-C32 |
| SLOT-GT-01 | gstack | GT-01: role review product value with concrete alternatives | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L289 | ProductKind+JTBD/FUO target | 以模板功能代替真用戶結果 | REVIEW_FINDINGS_READ | SBL_PRODUCT_OWNER（reproduce user use case） | ProductReviewFindings | 指出無法達到 FUO 的使用路徑 | 不授批准 | NACK_PRODUCT_FUO | FUO 變更→re-run product review | POS SLOT-GT-01: ProductKind+JTBD/FUO target → ProductReviewFindings raw-bound | NEG SLOT-GT-01: no target user or FUO → NACK_PRODUCT_FUO | SPEC-C32-SLOT-GT-01/ACC-C32-SLOT-GT-01/TEST-C32-SLOT-GT-01/EEXP-C32-SLOT-GT-01/DEL-C32 |
| SLOT-GT-02 | gstack | GT-02: review usability,NFR,error paths | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L290 | Arch+NFR+UX baseline | 無 repro 憑感想說品質 | REVIEW_FINDINGS_READ | SBL_SE_OWNER（measurable NFR/screen path） | EngineeringUXFindings | 可重播 UX 或性能改善建議 | 不自行修 code | NACK_ENG_REPRO | NFR drift→mark findings stale | POS SLOT-GT-02: Arch+NFR+UX baseline → EngineeringUXFindings raw-bound | NEG SLOT-GT-02: missing measurable NFR → NACK_ENG_REPRO | SPEC-C32-SLOT-GT-02/ACC-C32-SLOT-GT-02/TEST-C32-SLOT-GT-02/EEXP-C32-SLOT-GT-02/DEL-C32 |
| SLOT-GT-03 | gstack | GT-03: independent review/QA on exact source | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L291 | Test plan+candidate hash+independent checker | Reviewer==Maker 或缺 QA testcase | INDEPENDENT_REVIEW_ROUTE | PIPD_TQAEP_CHECKER（Maker!=Checker and receipt） | QAReviewFindings+CheckerRequest | 負例與復現路線/查核請求 | 不是本模型獨立 PASS | MAKER_SELF_ACCEPT | checker disqualified→HOLD_ACCEPTANCE | POS SLOT-GT-03: Test plan+candidate hash+independent checker → QAReviewFindings+CheckerRequest raw-bound | NEG SLOT-GT-03: self-accept/absent raw evidence → MAKER_SELF_ACCEPT | SPEC-C32-SLOT-GT-03/ACC-C32-SLOT-GT-03/TEST-C32-SLOT-GT-03/EEXP-C32-SLOT-GT-03/DEL-C32 |
| SLOT-GT-04 | gstack | GT-04: check ship gate and log retro without modifying Oracle | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L292 | Status checks+user value+release evidence | 試圖直接 tag/publish 或主體未驗 | RELEASE_READINESS_ONLY | PUBLISHER_READER（Publisher must separately approve） | ShipReadinessFindings | 可讀應補發布證據表 | 不能 publish | NACK_SHIP_POLICY | release gate revoke→HOLD_SHIP | POS SLOT-GT-04: Status checks+user value+release evidence → ShipReadinessFindings raw-bound | NEG SLOT-GT-04: missing status/independent gate → NACK_SHIP_POLICY | SPEC-C32-SLOT-GT-04/ACC-C32-SLOT-GT-04/TEST-C32-SLOT-GT-04/EEXP-C32-SLOT-GT-04/DEL-C32 |
| SLOT-SP-01 | Superpowers | SP-01: freeze key ADR before effect | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L293 | Design options+source-risk-ADR | 還無 ADR 卻要求直接寫代碼 | READ_DESIGN | SBL_SE_OWNER（decision before change） | ArchitectureADR+WriteIntentCandidate | 可比較方案和狹義 PatchIntent | 不是 WorkOrder | NACK_ADR | ADR superseded→invalidate write intent | POS SLOT-SP-01: Design options+source-risk-ADR → ArchitectureADR+WriteIntentCandidate raw-bound | NEG SLOT-SP-01: ADR unresolved → NACK_ADR | SPEC-C32-SLOT-SP-01/ACC-C32-SLOT-SP-01/TEST-C32-SLOT-SP-01/EEXP-C32-SLOT-SP-01/DEL-C32 |
| SLOT-SP-02 | Superpowers | SP-02: run Red on old HEAD → modify → Green on new HEAD | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L294 | Failing test OldHEAD+exact code scope | 沒真 Red/Green runner卻說通過 TDD | GOVERNED_TEST_EXECUTE | NATIVE_TEST_EXECUTOR（token + exact HEAD + test permissions） | RedGreenTrace+RunnerRawLog | Red/Green 測試指引與候選預期 | 不是已執行測試 | NACK_RED_PHASE | new head diff/failed green→rollback preimage | POS SLOT-SP-02: Failing test OldHEAD+exact code scope → RedGreenTrace+RunnerRawLog raw-bound | NEG SLOT-SP-02: no real red on old head → NACK_RED_PHASE | SPEC-C32-SLOT-SP-02/ACC-C32-SLOT-SP-02/TEST-C32-SLOT-SP-02/EEXP-C32-SLOT-SP-02/DEL-C32 |
| SLOT-SP-03 | Superpowers | SP-03: identify invariant then smallest affected cone | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L295 | Observed failure+repro+root cause | 未分離相關失敗就 shotgun edits | READ_ROOT_CAUSE | SBL_COMMANDER（scope minimal affected paths） | RootCauseRecord+RepairCone | 診斷與限界修補建議 | 不是實際修復 | NACK_ROOT_CAUSE | repro drift→invalidate repair cone | POS SLOT-SP-03: Observed failure+repro+root cause → RootCauseRecord+RepairCone raw-bound | NEG SLOT-SP-03: root cause unproven → NACK_ROOT_CAUSE | SPEC-C32-SLOT-SP-03/ACC-C32-SLOT-SP-03/TEST-C32-SLOT-SP-03/EEXP-C32-SLOT-SP-03/DEL-C32 |
| SLOT-SP-04 | Superpowers | SP-04: bounded plan/test/independent review | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L296 | Plan+independent evidence+review request | 沒 MakerChecker 分離或沒有真 logs | INDEPENDENT_COMPLETION_ROUTE | SBL_CHALLENGE_READER（distinct checker identity and raw receipt） | CompletionGateCandidate | 完成前核對清單與 stop report | 不算正式 acceptance | NACK_COMPLETION_GATE | checker receipt revoked→HOLD_COMPLETION | POS SLOT-SP-04: Plan+independent evidence+review request → CompletionGateCandidate raw-bound | NEG SLOT-SP-04: checker missing/mismatched evidence → NACK_COMPLETION_GATE | SPEC-C32-SLOT-SP-04/ACC-C32-SLOT-SP-04/TEST-C32-SLOT-SP-04/EEXP-C32-SLOT-SP-04/DEL-C32 |
**24 槽驗收前置**：每槽 `design_auth=DESIGN_ONLY_THIS_TURN`；`runtime_mode` 取 `STANDALONE / PREW3_SHADOW / SWOF_CONNECTED`，Shadow 禁任何非只讀動作。所有帶副作用的 `target_effect` 須另取得 Native Owner 權限、有效 RepoContext、token+SoD、at-most-once、readback 與 exact rollback；ReleaseReadiness 不等於發行，ReviewFinding 不等於獨立驗收。上表逐槽 `event` 即最小狀態失效 fixture，缺 raw receipt 僅是設計案例。

### C32.3.1｜24 槽部署／替代／Host Gate／逐槽撤銷與 Exit（作者端設計選定）

本表與緊鄰的 24/24 原身分、POS/NEG、Before/After、FirstFail 表以 SlotID 構成同一 `SlotLedger`；任一資料缺失，consumer 必拒收而非填預設。優先序 `REUSE > THIN_WRAP > EXTEND > MINIMAL_BUILD`；下列 preferred 皆為 `SELECTED_IN_DESIGN / NOT_INSTALLED`。

| SlotID | ProductKind / Moment / U-anchor | Selected internal baseline | Preferred provider exact workflow | Alternate provider / non-equivalence | Mode / EffectClass | BeforeState → output schema / Consumer | Token, Scope / FirstFail | Host/Install→Verify/Uninstall | POS→NEG evidence | Provider-off / semantic loss | Revoke→Rollback/ExitCost |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SLOT-OS-01 | CLI_TOOL/M00/U01 | local QuestionLedger+DecisionLedger | OpenSpec opsx:explore | manual source-cited interview | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_SOURCE | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:question_delta.json} → SBL TPM | read-capability + source ACL / NACK_SOURCE | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-OS-01: Explore when ambiguous → DecisionLedger+QuestionDelta raw-bound；NEG SLOT-OS-01: 無權讀取來源/來源 hash 改變 → NACK_SOURCE；收據預期 stdout/stderr+hash，未執行 | 來源引用的問題清單 / 不要把未知補成事實 | 撤銷訪問→CANCELED, no extra read；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-OS-02 | CLI_TOOL/M01/U03 | local exact-HEAD SpecDelta | OpenSpec opsx:propose | git diff --no-ext-diff + human review | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_DIFF | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:spec_delta.json} → SBL Spec Reader | read-capability + source ACL / NACK_SCOPE | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-OS-02: CurrentHEAD+desired scope bounded diff → SpecDelta+ChangeProposal raw-bound；NEG SLOT-OS-02: Repo HEAD stale / out-of-scope → NACK_SCOPE；收據預期 stdout/stderr+hash，未執行 | 本地可檢視 diff 和路徑差異 / 不得自動 apply | HEAD漂移→STALE_DIFF，重新取 HEAD；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-OS-03 | CLI_TOOL/M02/U05 | non-applied PatchProposal | OpenSpec apply under governed worker | human-reviewed patch outside SBL | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / GOVERNED_REPO_WRITE | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:change_receipt.json} → HGK Worker | ONE ECP + non-replay nonce + permit + exact scope / ECP_PERMISSION_DENIED | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-OS-03: Approved Change+WriteSet+Native ECP → ChangeSet+ApplyReadback raw-bound；NEG SLOT-OS-03: path escape / token absent / nonce replay → ECP_PERMISSION_DENIED；收據預期 stdout/stderr+hash，未執行 | 生成 diff+人類 Apply 步驟 / 不是已寫入 Repo | 許可撤銷→BLOCK; rollback exact preimage；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-OS-04 | CLI_TOOL/M03/U07 | local archive candidate | OpenSpec archive workflow | preserved supersession map | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / GOVERNED_ARCHIVE_METADATA | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:archive_receipt.json} → PIPD Trace Reader | ONE ECP + non-replay nonce + permit + exact scope / NACK_ARCHIVE | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-OS-04: Verified change + trace closed archive → ArchiveRecord+Supersession raw-bound；NEG SLOT-OS-04: unclosed evidence/stale package → NACK_ARCHIVE；收據預期 stdout/stderr+hash，未執行 | 產生 archive candidate 記錄 / 不是已封存 | 閉合撤銷→ARCHIVE_BLOCKED; restore prior ref；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-SK-01 | CLI_TOOL/M04/U09 | frozen ConstitutionProjection | Spec Kit /speckit.constitution | manual immutable constitution citation | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_CONSTITUTION | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:constitution_projection.json} → PIPD DOC01 | read-capability + source ACL / NACK_AUTHORITY | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-SK-01: Product kind + Constitution + non-goals → ConstitutionBinding raw-bound；NEG SLOT-SK-01: Constitution source missing / precedence mismatch → NACK_AUTHORITY；收據預期 stdout/stderr+hash，未執行 | 清晰非目標/風險清單 / 不能發布第二 Constitution | 來源章節變更→STALE_BINDING, rebind；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-SK-02 | CLI_TOOL/M05/U11 | source-bound ClarificationLedger | Spec Kit /speckit.clarify | in-house guided questions | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_CLARIFICATION | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:clarification.json} → SBL TPM | read-capability + source ACL / PI_NOT_READY | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-SK-02: Unknown requirement + value of information → RequirementAtom+ACCSeed raw-bound；NEG SLOT-SK-02: zero atoms / missing acceptance cue → PI_NOT_READY；收據預期 stdout/stderr+hash，未執行 | 只問尚未明確的高價值問題 / 不是正式 PI compiled | 答覆變動→invalidate affected atoms；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-SK-03 | CLI_TOOL/M06/U13 | typed SPEC+TaskDAG candidate | Spec Kit /speckit.specify + /speckit.plan + /speckit.tasks | local DAG validator | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_PLAN | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:task_dag.json} → PIPD PI Intake | read-capability + source ACL / NACK_DAG | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-SK-03: Bounded task nodes + dependency and owner → TaskDAG+TopoOrder raw-bound；NEG SLOT-SK-03: cycle/orphan → NACK_DAG；收據預期 stdout/stderr+hash，未執行 | 可排序的任務與前置條件 / 不能自動執行 | 依賴變更→invalidate topo plan；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-SK-04 | CLI_TOOL/M07/U15 | Change/Task readiness verifier | Spec Kit validation/extension flows | schema+graph offline checks | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_VERIFY | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:task_validation.json} → PIPD Trace | read-capability + source ACL / NACK_UNPINNED_WORKFLOW | CLI/Windows/Host: exact executable version, command help and controlled dry-run | POS SLOT-SK-04: Approved workflow manifests with versions → WorkflowComposition raw-bound；NEG SLOT-SK-04: extension provenance invalid → NACK_UNPINNED_WORKFLOW；收據預期 stdout/stderr+hash，未執行 | 只輸出本地結構化工作流草稿 / 不能偷裝 extension | 撤銷 module→disable composition；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |
| SLOT-MP-01 | AGENT_SKILL/M08/U17 | portable Skill manifest validator | Matt skills taxonomy+grilling | standalone SKILL.md parser | PREW3_SHADOW: READ_ONLY; STANDALONE: scoped native permit; SWOF_CONNECTED: SWOF ACK+HGK ECP / READ_SKILL | SOURCE_CITED / {slot_id,subject_sha256,source_ref,mode,provider_status,body:skill_manifest.json} → SBL DOC10 | read-capability + source ACL / NACK_SKILL_ROUTE | Codex/Claude/Hermes/HGK: compare installed manifest and session discovery, POS+NEG+uninstall | POS SLOT-MP-01: Goal+intent type+host capability → SkillRouteDecision raw-bound；NEG SLOT-MP-01: unknown trigger or missing dependencies → NACK_SKILL_ROUTE；收據預期 stdout/stderr+hash，未執行 | 本地 SKILL.md 路徑/替代步驟 / 無 host load claim | Skill unload→not_eligible then reroute；unload=remove only this adapter; rollback=restore exact preimage or previous signed manifest; exit cost=adapter+Host UAT+ABI diff |

</details>

<details>
<summary>DOC-06｜C33.2｜386/386 逐筆原身份保全＋差異化功能 Consumer／正負驗收／退出｜來源 L294–L338</summary>

## C33.2｜386/386 逐筆原身份保全＋差異化功能 Consumer／正負驗收／退出


### C33.2.NOBJ24｜24 條（原件原判＋新增非模板設計）

| 原 ID | 原名稱 | 原 SBL 狀態 | Master Locator | 驗證等級 | 保留原 action | 原 Grant/Deny（未定位仍TT） | 原 Home/Owner | 原 Tests/Exit | 功能域 | Slot | 具名 Consumer | 目標預設 / baseline | 專屬 POS / 預期輸出 | 專屬 NEG / 可見錯誤 | FirstFail | Owner 授權 / Exit | R1→R2 決策 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NOBJ-001 | HLPE Native PLAN/BOOTSTRAP/FACTORY | PORTABLE_REIMPLEMENTATION | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L323 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L274 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Portable HLPE Phases | SLOT-SK-03 | SBL TPM / HLPE | PROPOSED_PORTABLE_METHOD · local PhasePlan | PLAN/BOOTSTRAP/FACTORY 的分階段狀態與來源一致 | 把上游 legacy phase 當 SBL PI Compiler→PARALLEL_COMPILER | PARALLEL_COMPILER | PIPD/HLPE Owner；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-002 | Matt grill-with-docs | REFERENCE_METHOD_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L324 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L275 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Docs-assisted Interview | SLOT-MP-02 | TPM interview | METHOD_REFERENCE_ALLOWED_EXECUTOR_DENIED · read SKILL.md dependent files | source-anchored questions with known-answer exclusion | unknown referenced SKILL path→NACK_DEPENDENCY | METHOD_EXECUTION_UNAUTHORIZED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-003 | OpenSpec | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L325 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L276 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Brownfield Spec Workflow | SLOT-OS-02 | SBL SpecDelta Consumer | DESIGN_FIT_PENDING_LICENSE_HOST · local ChangeDraft | proposal/current-vs-intended spec delta with repo SHA | stale source revision→NACK_SCOPE | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-004 | Spec Kit | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L326 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L277 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Greenfield Spec Workflow | SLOT-SK-02 | SBL SPEC / TPM | DESIGN_FIT_PENDING_LICENSE_HOST · local SPEC+TaskDAG | constitution/spec/plan/tasks source-bound projection | unversioned extension or Constitution overwrite→NACK_AUTHORITY | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-005 | Superpowers test-driven-development | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L327 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L278 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | TDD / Debug Discipline | SLOT-SP-02 | Commander / HGK | DESIGN_FIT_PENDING_LICENSE_HOST · test plan + repair cone | RedGreenTrace and bounded RootCause record | no executed RED on old HEAD→NACK_RED_PHASE | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-006 | Superpowers systematic-debugging | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L328 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L279 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Systematic Debugging | SLOT-SP-03 | Commander-SP / RootCause Reader | TRANSLATE_REUSE_DEBUG_NOT_TDD · source-bound diagnostic plan | reproducible RootCauseRecord+RepairCone sourced to failure and scope | unknown root cause followed by broad edits→NACK_ROOT_CAUSE | NACK_ROOT_CAUSE | Native source Owner + SBL-R019；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-007 | Superpowers verification-before-completion | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L329 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L280 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Verification Before Completion | SLOT-SP-04 | Challenge-SP / Completion Gate Reader | TRANSLATE_REUSE_COMPLETION_NOT_TDD · completion checklist | CompletionGateRequest bound to checked plan, tests and distinct reviewer | maker self-verification as independent PASS→MAKER_SELF_ACCEPT | MAKER_SELF_ACCEPT | Independent checker Owner + SBL-R019；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-008 | GStack | REFERENCE_METHOD_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L330 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L281 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Specialist Review | SLOT-GT-01 | SBL Review & Challenge | METHOD_REFERENCE_ALLOWED_EXECUTOR_DENIED · local reviewer checklist | product/engineering/QA/release issue list with reproduction | self-issued independent PASS→MAKER_SELF_ACCEPT | METHOD_EXECUTION_UNAUTHORIZED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-009 | GSD / planning-with-files | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L331 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L282 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Long-running Checkpoint | SLOT-GS-01 | SBL Milestone/Resume | DESIGN_FIT_PENDING_LICENSE_HOST · hash-bound PhasePlan | phase artifact hash and resume/replay permit decision | archived source treated as current installer→ARCHIVED_SOURCE_DENIED | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-010 | AGENTS.md | PORTABLE_REIMPLEMENTATION | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L332 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L283 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Agent Repo Guide | SLOT-MP-01 | Codex host loader | DESIGN_FIT_PENDING_LICENSE_HOST · read-only repo policy summary | scoped repository instruction readback | AGENTS tries to confer tool permission→INSTRUCTION_PRIVILEGE | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-011 | SKILL.md | PORTABLE_REIMPLEMENTATION | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L333 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L284 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Skill Procedure | SLOT-MP-01 | Host Skill Registry | DESIGN_FIT_PENDING_LICENSE_HOST · plain SKILL.md reading | frontmatter/dependency/procedure/trigger manifest | injection or missing dependency→SKILL_LOAD_NACK | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-012 | DESIGN.md | REFERENCE_METHOD_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L334 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L285 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Design View | SLOT-SP-01 | TPM design reader | METHOD_REFERENCE_ALLOWED_EXECUTOR_DENIED · read-only ADR | design decisions and alternative/cost review | DESIGN.md claims approval token→NACK_AUTHORITY | METHOD_EXECUTION_UNAUTHORIZED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-013 | Prompt projection | PORTABLE_REIMPLEMENTATION | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L335 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L286 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Model / Agent / Skill | SLOT-MP-01 | SBL Host/Procedure Reader | DESIGN_FIT_PENDING_LICENSE_HOST · read-only procedure | Prompt projection：受控提示/技能路由的版本、作用域與可觀測產物 | Prompt projection 越權到 Host token/Policy Writer→HOST_AUTH_DENIED | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-014 | OpenAI skill-creator | FALLBACK_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L336 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L287 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Model / Agent / Skill | SLOT-MP-01 | SBL Host/Procedure Reader | FALLBACK_NONDEFAULT_ONLY · read-only procedure | OpenAI skill-creator：受控提示/技能路由的版本、作用域與可觀測產物 | OpenAI skill-creator 越權到 Host token/Policy Writer→HOST_AUTH_DENIED | FALLBACK_PRIMARY_AVAILABLE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-015 | OpenAI plugin-creator | FALLBACK_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L337 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L288 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Model / Agent / Skill | SLOT-MP-01 | SBL Host/Procedure Reader | FALLBACK_NONDEFAULT_ONLY · read-only procedure | OpenAI plugin-creator：受控提示/技能路由的版本、作用域與可觀測產物 | OpenAI plugin-creator 越權到 Host token/Policy Writer→HOST_AUTH_DENIED | FALLBACK_PRIMARY_AVAILABLE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-016 | Agent Skills specification | REFERENCE_METHOD_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L338 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L289 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Skill Format Specification | SLOT-MP-01 | SBL Host Adapter | METHOD_REFERENCE_ALLOWED_EXECUTOR_DENIED · local SKILL.md parser | format validation and consistent trigger envelope | format valid but host unloaded→HOST_NOT_LOADED | METHOD_EXECUTION_UNAUTHORIZED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-017 | Agent Plugins 1.0 Working Draft | QUARANTINED | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L339 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L290 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | NO_ACTIVATION; OWNER_CR_REQUIRED; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Quarantined Draft | SLOT-MP-01 | Host experiment only | REJECTED_OR_QUARANTINED_REFERENCE_ONLY · 原狀態禁止實例化；reference documentation only | schema comparison, quarantined extension record | plugin draft promoted to installed→QUARANTINED_DEFAULT_DENIED | ORIGINAL_SOURCE_DENY | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-018 | JSON Schema 2020-12 | TRANSLATE_AND_REUSE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L340 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L291 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Contract Validation | SLOT-SK-02 | PIPD/Schema Reader | DESIGN_FIT_PENDING_LICENSE_HOST · local jsonschema validation | 2020-12 validation errors per path | undeclared sidecar key or unknown schema→NACK_SCHEMA | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-019 | pytest | ADOPT | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L341 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L292 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Unit Testing | SLOT-SP-02 | Native Test Runner | DESIGN_FIT_PENDING_LICENSE_HOST · test design cases | real case counts/exit/error logs attached to tested SHA | zero collected tests→TEST_DENOMINATOR_ZERO | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-020 | GitHub Actions | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L342 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L293 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | CI Workflow | SLOT-GS-04 | CI Evidence Producer | DESIGN_FIT_PENDING_LICENSE_HOST · local test instructions | workflow run id/check name/source SHA and logs | fork PR secret elevation→CI_TRUST_BOUNDARY | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-021 | CycloneDX | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L343 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L294 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | SBOM Format | SLOT-GS-04 | Supply Chain Normalizer | DESIGN_FIT_PENDING_LICENSE_HOST · local BOM JSON schema | CycloneDX document, format version and component hashes | wrong schema/subject→SBOM_SCHEMA_FAIL | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-022 | Gitleaks | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L344 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L295 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Secret Scanning | SLOT-GT-03 | Security CI | DESIGN_FIT_PENDING_LICENSE_HOST · no secrets baseline check | findings with detector/secret fingerprint/location | secret hit suppressed without owner exception→SECRET_POLICY_DENIED | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-023 | markdownlint | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L345 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L296 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Markdown Lint | SLOT-SK-01 | Docs CI | DESIGN_FIT_PENDING_LICENSE_HOST · local markdown review | MD diagnostic rule and line | invalid frontmatter ignored→MD_LINT_FAIL | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| NOBJ-024 | Ruff + type checker | WRAP_WITH_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L346 @sha256:83ea1bef8d045bf0…; upstream `R2 §7` L297 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Code Lint | SLOT-SP-02 | Native CI | DESIGN_FIT_PENDING_LICENSE_HOST · static code review | lint diagnostics with file/line/rule | skipped lint result masquerades success→QUALITY_GATE_FAIL | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
**NOBJ24 關閉要求**：逐原 ID 的 `SPEC-C33-NOBJ24-<id> → ACC → TEST(POS/NEG) → EEXP(expected raw, same candidate SHA) → DEL(DecisionRecord)`。本輪全部為 `DESIGNED_NOT_EXECUTED`。原 Native grant/deny 未取回的欄明示 TT；不宣稱該欄為原生直接證實。

### C33.2.OSS19｜19 條（原件原判＋新增非模板設計）

| 原 ID | 原名稱 | 原 SBL 狀態 | Master Locator | 驗證等級 | 保留原 action | 原 Grant/Deny（未定位仍TT） | 原 Home/Owner | 原 Tests/Exit | 功能域 | Slot | 具名 Consumer | 目標預設 / baseline | 專屬 POS / 預期輸出 | 專屬 NEG / 可見錯誤 | FirstFail | Owner 授權 / Exit | R1→R2 決策 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 341 | OpenTelemetry GenAI | ADOPT | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L358 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L309 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Trace Semantic Surface | SLOT-GS-01 | Ops Observability Reader | DESIGN_FIT_PENDING_LICENSE_HOST · local structured trace JSON | trace/span IDs and semantic attribute map | evidence SHA derived from trace proxy→PROXY_EVIDENCE_DENIED | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 342 | Spec Kit 1.1 patterns | BORROW_ADAPTER | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L359 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L310 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Greenfield Spec Workflow | SLOT-SK-02 | SBL SPEC / TPM | SOURCE_STATE_PRESERVED_PENDING_OWNER · local SPEC+TaskDAG | constitution/spec/plan/tasks source-bound projection | unversioned extension or Constitution overwrite→NACK_AUTHORITY | OWNER_DECISION_REQUIRED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 343 | LangGraph checkpoint tests | TEST_DONOR_ONLY | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L360 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L311 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Execution Context / Phase | SLOT-GS-01 | SBL Scoped Context Reader | METHOD_REFERENCE_ALLOWED_EXECUTOR_DENIED · local PhasePlan | LangGraph checkpoint tests：階段狀態、當前源 digest 與可回復點的型別化讀回 | LangGraph checkpoint tests 未取證仍顯示 resumed → CHECKPOINT_NO_EVIDENCE | METHOD_EXECUTION_UNAUTHORIZED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 344 | Groundability method | ADOPT_REVIEW_METHOD | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L361 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L312 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Support / Method Assessment | SLOT-SP-01 | SBL Reuse Scout | DESIGN_FIT_PENDING_LICENSE_HOST · source-bound ADR | Groundability method：輸入/輸出和原狀態核對的受控方法或工具適配紀錄 | Groundability method 無 FeatureDiff 直接成為 Default→ADMISSION_MISSING | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 345 | Global Coherence | ADOPT_STATE_COMMIT_PRINCIPLE | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L362 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L313 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Support / Method Assessment | SLOT-SP-01 | SBL Reuse Scout | DESIGN_FIT_PENDING_LICENSE_HOST · source-bound ADR | Global Coherence：輸入/輸出和原狀態核對的受控方法或工具適配紀錄 | Global Coherence 無 FeatureDiff 直接成為 Default→ADMISSION_MISSING | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 346 | Finding-the-Right-Fit | ADOPT_QUALIFICATION_METHOD | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L363 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L314 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Support / Method Assessment | SLOT-SP-01 | SBL Reuse Scout | DESIGN_FIT_PENDING_LICENSE_HOST · source-bound ADR | Finding-the-Right-Fit：輸入/輸出和原狀態核對的受控方法或工具適配紀錄 | Finding-the-Right-Fit 無 FeatureDiff 直接成為 Default→ADMISSION_MISSING | LICENSE_OR_HOST_GATE | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 347 | HF 6,204 trajectories | SECONDARY_CORPUS | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L364 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L315 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Support / Method Assessment | SLOT-SP-01 | SBL Reuse Scout | SOURCE_STATE_PRESERVED_PENDING_OWNER · source-bound ADR | HF 6,204 trajectories：輸入/輸出和原狀態核對的受控方法或工具適配紀錄 | HF 6,204 trajectories 無 FeatureDiff 直接成為 Default→ADMISSION_MISSING | OWNER_DECISION_REQUIRED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |
| 348 | Promptfoo | OPTIONAL_ATTACK_DONOR | SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L365 @sha256:83ea1bef8d045bf0…; upstream `R2 §8` L316 | SBL_MASTER_LINE / NATIVE_DIRECT_TT | CONDITIONAL_OR_DEFERRED; NO_AUTO_INSTALL; positive: source+qualified scope; negative: forged role/downgrade→FAIL | UNLOCATED+TT-NATIVE-GRANT ; UNLOCATED+TT-NATIVE-DENY | UNLOCATED+TT-NATIVE-FINAL_HOME / UNLOCATED+TT-NATIVE-OWNER | UNLOCATED+TT-NATIVE-TEST ; UNLOCATED+TT-NATIVE-EXIT | Prompt Attack Tests | SLOT-GT-03 | Security Evaluator | SOURCE_STATE_PRESERVED_PENDING_OWNER · manual red-team cases | prompt injection fixture result with prompt hash | no negatives yet PASS→NEGATIVE_FIXTURE_MISSING | OWNER_DECISION_REQUIRED | NATIVE_OWNER+SBL-R019+SBL-R052；退出：撤銷提供者投影、保留原始來源，核對必要原授權/會話/回滾 | SOURCE_PROVENANCE_RETAINED; SUBSTANTIVE_ROUTE_REFINED |

</details>

- **跨域修補的 FirstFail**：`DOC06_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-07｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-07(1).md`；SHA-256 `a366d3783c82089c5593ffabb0704d8507632cce45622684f7a0186f2ae310f8`；原章節定位保留；Canonical Writer = 原 SBL DOC-07 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-07｜C11.2｜PREW3_SHADOW：Frozen W2 Readset、NoEffect 與相容性｜來源 L162–L179</summary>

## C11.2｜PREW3_SHADOW：Frozen W2 Readset、NoEffect 與相容性
**Shadow 不可具有任何治理效果的白名單例外**：`PREW3_SHADOW` 只允許讀 `W2_FROZEN_READSET` 與離線計算相容性、差異、風險、阻擋理由；其結果不可觸發 commit、merge、PR approval、CI promote、issue close、Token mint、World Effect、W3 ready 或 Release。關閉寫入工具只是第一道保護；必須同時以 executor capability allowlist、容器/Host 外層 ACL、可驗證 effect journal 零新增及 readback 殘留掃描證明未生效。

**故障處理**：若 W2 readset `subject_sha` 與當前參考不符，產生 `W2_READSET_STALE`，仍允許離線產出 mismatch report，但該 report 不能合併至 W3；若 write API 被嘗試，拒收碼為 `DENY_SHADOW_EFFECT`，並產出 `NoEffectProofDesign` 包含所有應檢介質而非單一「未成功」訊息。禁止使用 `dry_run=true` 標籤代替 effect sink 層的實際封鎖。


`PREW3_SHADOW` 的唯一資料入口是經 `readset_id+source_sha+snapshot_time+W2_owner` 校驗的 frozen W2 reference；任何 WorkOrder 寫入、Native mutation、repair、merge、publish、W3 token 請求都不出本模式。允許產 `CompatibilityAssessment`、`ExpectedNoEffect`、`ChangeCandidate`；不允許可執行 ECP 或 ReadyW3 token。若讀取範圍漂移，標 `W2_READSET_STALE`；若工具要求 write，標 `DENY_SHADOW_EFFECT` 並 quarantine；拒收後對 repo diff、remote side-effect journal、artifact publication queue 執行授權範圍內的 read-only residue scan。

**可證明的 NoEffect 必須同時滿足**：start/end repository/tree digest、native effect journal delta=0、release/publish queue delta=0、external action request=0、scope/subject 相同、receipt freshness、真 checker；缺任何觀測只能 `NO_EFFECT_UNPROVEN`，不可用「沒有看到 log」推導無世界效果。


### C11.2a｜W2 Frozen Readset 及 39 Gate 的 Shadow 隔離流程
Shadow Runner 以 isolated **read-only filesystem**、不可變 W2 snapshot mount、`deny network writes` / token-mint / remote-side-effect tools、no-effect ECP placeholder（僅描述、不發實效）運行；出站網路即使只發生未知 telemetry 亦歸 `UNOBSERVED_EFFECT_RISK`。W2 SourceOwner 交付 `{w2_readset_id,manifest_sha,signer_ref,snapshot_time,state,source_hash,expiry}`，目前任何缺件都 `W2_READSET_UNBOUND`。在啟動前及結束後比對 image/fs/git HEAD、Host open handles、CI job/remote queue、Native journal、publication registry，對無權觀測的遠端則 `INCONCLUSIVE_NO_EFFECT` 而不是 `PASS_ZERO_EFFECT`。W2 讀集 stale、長任務掛住、MCP 從讀變寫、checkpoint restore 帶 token 都先 DENY；G07/G08/G11/G12 逐格 F。合法 POS 僅為 W2 frozen read→CompatibilityAssessment，不含效果。

### C11.2b｜四 Host Shadow 原生效果封鎖器

W2 Owner 需提供同 Subject 的 FrozenReadset、RAG/外聯 allowlist、journal/outbox/remote sink list。Hermes 封 HGK effect dispatch、Codex 封 shell/repo write hooks、Claude Code 封 bash/edit/permission-grant 與 plugin hooks、DeepSeek 若無可驗原生沙箱即 `UNSUPPORTED_NATIVE_ABI`；Web 僅 DOC_MOUNT。POS 為 W2 只讀 CompatibilityAssessment；NEG 為伪 `dry_run telemetry POST`, CI queue, issue create；必有 proxy+queue+filesystem+CI 同窗 readback，缺任一→`INCONCLUSIVE_NO_EFFECT`，不填 PASS。

</details>

<details>
<summary>DOC-07｜C27.3｜CredentialTokenScopeContract 與 Capability Broker｜來源 L525–L540</summary>

## C27.3｜CredentialTokenScopeContract 與 Capability Broker
**Token 最小模型**：`issuer`、`subject/principal`、`audience`、`resource`、`action`、`scope`、`effect_class`、`candidate_hash`、`ecp_id`、`nonce`、`issued_at/expiry`、`revocation_epoch`、`approval_receipt_ref` 彼此綁定；敏感值僅在 Native Broker/Secret Store 中處理，對模型只交不含 secret 的引用。`delegation_chain` 每跳需縮小 scope、縮短 TTL，不可增加權力；破壞簽章、錯誤 audience、跨 Subject 重放、過期或 revoke 一律拒收。

若 token 因 race 在 effect 完成後被撤銷，應保留事件及世界讀回、啟動 Owner-controlled containment，而非刪除紀錄假裝沒有執行。缺乏真 issuer 的設計例只呈現 JSON schema，**不得**產生可被誤用的 JWT、bearer 值或通過簽章的展示碼。


身份認證 Authn 先於 Authz：`issuer,principal,audience,subject_sha,task_id,effect_class,capability_id,allowed_path/namespace,tenant_id,mode,issued_at,expires_at,nonce,idempotency_ref,revocation_epoch,approval_ref,signature_ref` 缺一項適用關鍵欄就拒收。Token 短期、受 audience/task/effect/scope/TTL 綁定；禁止 cross-tenant reuse、CI secret 靜態環境複用、憑證寫入 prompt 或 stdout。每一次 effect 都由正確 Native issuer/validator 驗簽、校時、讀撤銷、查最小權限。SBL `PermitRequestDesign` 是 request shape，絕無授權欄位 `granted=true`。


### C27.3a｜Token 生命週期、雙查與撤銷競態
`REQUESTED → ISSUED → VALID → (CONSUMED|EXPIRED|REVOKED)` 是**設計上的狀態投影**，簽發狀態仍由原生 Identity/Policy Owner 控制。兩次驗證：第一次在 EffectRequest admission，第二次在**真正 side effect 當下**的 native sink（防 TOCTOU）核對 `issuer public key/key_id/key_rotation_epoch,signature,principal,tenant,audience,subject_sha,scope/effect,nonce,expiry,revocation_epoch,delegation_chain,clock_skew_budget`。Idempotency key 不因 token refresh 改變；時鐘偏差超過 Owner policy→`TOKEN_CLOCK_SKEW`，撤銷 cache stale→`REVOCATION_STALE`，跨租戶/錯 audience→`CROSS_TENANT_DENIED`，已 consume nonce 重播→`TOKEN_REPLAY_DENIED`；任一等候 Owner 時不執行 effect。Token 不進 Prompt/stdout/artifact/SBOM，任何 leak→C44.4 incident。Read-only Shell tool 必拒未要求的 credential escalation。

### C27.3b｜Token Broker 真 issuer 與競態雙檢（不把模型上下文當錢包）

`TokenRef` 僅 opaque handle，密鑰原文不可進 AGENT context/trace/log；驗簽時必查 issuer、audience、tenant、delegate_chain、nonce、TTL、requested effect、subject digest、revocation_epoch 的即時原生狀態。POS 模擬收發兩次皆為有效 scope 時只產 request；NEG 在排程後、effect sink 前撤銷 Token → Native NACK (`TOKEN_REVOKED`)；即使 queued side effect 已落外部帳戶，撤銷後要開 Incident、不得假報 transaction rollback。SBL 不能簽發 JWT/Permit 或選擇 issuer 代替 Native。

</details>

- **跨域修補的 FirstFail**：`DOC07_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-08｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-08(1).md`；SHA-256 `c7029c1ff07abe3135d33d3abf858a5fecedd911b494cd69c16eb1ddb8158288`；原章節定位保留；Canonical Writer = 原 SBL DOC-08 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-08｜C22.3｜EligibilityResolver 可執行決策，非「default ALLOW」｜來源 L194–L223</summary>

## C22.3｜EligibilityResolver 可執行決策，非「default ALLOW」

依需求枚舉全部 1,152 個核心組合，只是靜態決策空間；每個 output 的 `status`, `first_fail`, `source_ref`, `owner`, `recheck_on` 不得為空；對未支持 v0.1 Kind 明確 `UNSUPPORTED_V0_1`；未裝載 Host 一律設計合法但 `DEFERRED_UNVERIFIED`；原生 Oracle 未釘定一律 `OWNER_HOLD`；二者不可寫成 PASS。

```python
from itertools import product
KINDS = ['CLI_TOOL', 'AGENT_SKILL', 'SIMPLE_AGENT', 'PLUGIN', 'PROFILE', 'AGENT_OS', 'AI_SYSTEM', 'GENIE/GENIE.md']
MODES = ['STANDALONE', 'PREW3_SHADOW', 'SWOF_CONNECTED']
RISK = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
HOSTS = ['HERMES', 'CODEX', 'CLAUDE', 'DEEPSEEK']
PROFILES = ['LITE', 'STANDARD', 'ASSURED']
def resolve(q):
    if q["product_kind"] not in KINDS: return "HARD_DENY", "UNKNOWN_KIND"
    if q["core_host"] not in HOSTS: return "HARD_DENY", "UNKNOWN_CORE_HOST"
    if q["mode"] == "PREW3_SHADOW" and q["state_effect_requested"]:
        return "HARD_DENY", "DENY_NO_NATIVE_EFFECT"
    if q["mode"] == "SWOF_CONNECTED" and (q["receiver"] != "SWOF_W3" or not q["native_receiver_ready"]):
        return "SWOF_RESERVED_COMPATIBILITY_ONLY", "SWOF_NATIVE_OWNER_HOLD"
    if q["product_kind"] not in {"CLI_TOOL", "AGENT_SKILL", "SIMPLE_AGENT"}:
        return "UNSUPPORTED_V0_1", "PRODUCT_KIND_V01_UNSUPPORTED"
    if q["risk"] in {"HIGH", "CRITICAL"} and q["profile"] != "ASSURED":
        return "OWNER_HOLD", "PROFILE_SAFETY_ESCALATION_REQUIRED"
    if not q["owner_oracle_bound"]:
        return "OWNER_HOLD", "CR_ORACLE_UNRESOLVED"
    if not q["qualified_host_loaded"]:
        return "DEFERRED_UNVERIFIED", "HOST_NOT_EFFECTIVE"
    return "DESIGN_ELIGIBLE", "RUNTIME_QUALIFICATION_REQUIRED"
assert len(list(product(KINDS, MODES, RISK, HOSTS, PROFILES))) == 1152
```

</details>

<details>
<summary>DOC-08｜C22.4｜三條 Golden Journeys：可觀察 Before→After、Host/Installer Discovery 與破壞性 NEG｜來源 L224–L235</summary>

## C22.4｜三條 Golden Journeys：可觀察 Before→After、Host/Installer Discovery 與破壞性 NEG

| Journey/Kind/Scope | 合法前置與正向消費流程 | 可觀察 After／Raw Evidence | 真正 NEG／FirstFail | 復原與 Provider-off |
| --- | --- | --- | --- | --- |
| GJ01 CLI_TOOL/STANDALONE | Owner 已 pin 套件 digest+license+合法 manifest 的 install recipe；讀 manifest 內 add/list argv，不猜測旗標；clean install→新增 record→list→重啟查同 ID→uninstall | 真可執行 binary hash、exit code、stdout JSON schema、state DB before/after 與重啟一致、uninstall 檔案刪除白名單／用戶資料 retention | 只顯示 --help 無 add→FUNCTIONAL_CONSUMER_MISSING；重啟資料消失→PERSISTENCE_FAIL；uninstall 遺留可執行檔→RESIDUE_FAIL | 影響範圍撤銷、先保留用戶資料且經同意再刪；provider-off 命令仍可離線執行本地 add/list |
| GJ02 CLI_TOOL 或 PLUGIN adapter；affected-only | 真 root/head/tracked_files/currentness 與 scoped PD；SpecDelta/TaskDAG→dry-run diff→經 token 的合法單次 ECP effect→測試→Rollback | 原 Repo preimage/changed-file集合/HEAD，actual diff ⊆ writable_scope；idempotency nonce；復原後 World state 與 residue 再讀 | 使用 LIBRARY 作 ProductKind→UNKNOWN_KIND；修改非 scope→REPAIR_SCOPE；無 token 施工→ECP_PERMISSION；SHA 漂移→SOURCE_STALE | 反向 patch 只作用 affected cone、驗 before/after hash；Shadow 僅產 diff preview＋NoEffect Receipt |
| GJ03 AGENT_SKILL；Host Effective Load | pin Skill digest/license/security→Host 原生 install/load→trigger 正輸入→non-trigger 誤輸入→provider-off→deactivate/uninstall | Host 原生 loaded/trigger log、nontrigger zero dispatch、removed manifests+cache scan、provider-off trace 無網路 | SKILL.md 存在但 Host 未 loaded→HOST_NOT_EFFECTIVE；跨 skill trigger→ROUTING_OVERLAP；cache 仍 dispatch→STALE_PROVIDER_CACHE | 停用導流、Host 重新載入驗快取歸零；禁止自動從其他 provider 偷取受權範圍 |

**GJ01 最小設計施工 WorkPackage**：指定 `ProductKind=CLI_TOOL, CoreHost=CODEX, mode=STANDALONE, OS=Linux-x86_64` 作首版 Target，不宣稱已安裝；Builder 必先從合法 manifest 的 `entrypoints.add`, `entrypoints.list`, `install.recipe`, `uninstall.recipe`, `argv_schema`, `data_retention_policy` 發現真命令。Discovery 若缺欄位，`COMMAND_MANIFEST_MISSING` 阻擋施工；不可自造 `sbl add` 等實際 CLI 指令。本稿規定有效測試行為，不是假裝產品已存在。

**GJ02** 設計代表路徑 `OpenSpec OS-02 → SpecDelta → PIPD Source/Atom/PI/PD → ONE ECP → HGK bounded effect → Native WorldReceipt → C39 MUT/RECOVERY`；Pinned upstream 不能取代 PIPD 施工 Owner。**GJ03** 的 Host 快取、Skill 路由及 provider-off 需在每個原生宿主分別出具原始收據。

</details>

- **跨域修補的 FirstFail**：`DOC08_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-09｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-09(1).md`；SHA-256 `6450f7c15915ec8b304f4e5fd4093ea707434db8bae9d2bb6e66c30ab6eed2e1`；原章節定位保留；Canonical Writer = 原 SBL DOC-09 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-09｜R09-01.6｜九步 SOP 實質操作閉包與複合需求分解｜來源 L84–L90</summary>

## R09-01.6｜九步 SOP 實質操作閉包與複合需求分解

本輪逐檔 index 195/195→定位 SBL r3/audit、官方 PIPD DOC00–09、SBL Master/十卷、當版 DOC06 `C32/C33/C34`→全文 search 18 個核心詞→逐 ID 對照 C23/C24/C25、24/25/386/39/38/96/16/3/18→把含「各有／分別／對應」轉成 child、cell、positive/negative/consumer 的**獨立行**→從原章位回填 typed 行為→記錄 source-gap、Owner-gap。

分母閉合狀態：`13/13` Child、`24/24` CAP、`25/25` Method、`386/386` Named Items（來源 DOC06 current fields 一一對接）、`96/96` Mode×Kind×Host、`39/39` Gate、`38/38` Surface、`16/16` Moment、`18/18` Audit fixture，這些是**具名結構與設計讀取覆蓋**；不是 195 檔已全部歸納成真正完整 RequirementsAtom 語義全集。特別是三份上位獨立來源、N14、CR-ORACLE-001 和 Host/Native 本體未 closure，必 `FORMAL_QUALIFICATION_HOLD`。每個 open token 含 `{source,owner,consequence,next_evidence,firstfail}`；任何 UNKNOWN 不得記 N/A。

</details>

- **跨域修補的 FirstFail**：`DOC09_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-10｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-10(1).md`；SHA-256 `a64aa21c977334dd74d660a86377ee10c4d329aa5fde0dae25ff81a3e69e8d8f`；原章節定位保留；Canonical Writer = 原 SBL DOC-10 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-10｜1.5｜GatePrecedenceRegistry v1（全冊唯一生效的 FirstFail 演算法）｜來源 L95–L132</summary>

## 1.5｜GatePrecedenceRegistry v1（全冊唯一生效的 FirstFail 演算法）

同一輸入只允許此表 G00→G90 的**首個確定性拒收結果**。任何章節寫的「七閘」「八節點」「先 Host 再 Source」均為歷史說明，於 r4 以本表取代。第一個 `HOLD` 不得被後面 success 覆蓋；緊急撤銷與已知不可逆違法風險是旁路 `STOP_NOW` 安全 interlock，**立即阻止效果**，但診斷 first_fail 保留按 G00→G90 唯一排序、另記 `hard_stop_reason`。沒有 Native 簽發不能評成 Native PASS。

| Gate | 控制名 | 唯一主管 | 首拒碼 | 過閘前置／Reader 動作 |
|---|---|---|---|---|
| `G00` | `REQUEST_SCHEMA` | SBL DOC10 intake | `REQUEST_SHAPE_INVALID` | nonempty goal+locator+schema_version; effect class known |
| `G10` | `SOURCE_RIGHTS_CURRENTNESS` | PIPD authority-source + Source Owner | `SOURCE_FREEZE_HOLD` | real source digest / ACL / source rights / latest supersession; design only can proceed while formal freeze HOLD |
| `G20` | `PRODUCT_KIND` | SBL DOC01 Kind Owner | `PRODUCT_KIND_ELIGIBILITY_ERROR` | 8 exact kind; unsupported/deferred cannot execute |
| `G30` | `MODE_HARD_VETO` | SBL DOC07 + W2 Native Owner | `SHADOW_WORLD_EFFECT_DENIED` | SHADOW effect=READ_ONLY; W2 source signed+fresh |
| `G40` | `SP_ROLE_SOD` | SBL DOC04 + PIPD Checker | `SOD_NOT_INDEPENDENT` | TPM/Commander/Challenge mutual effect ceilings; principal not profile |
| `G50` | `PERMISSION_EFFECT` | Native Permit/HGK/PIPD | `NO_TOKEN_DENIED` | ECP+actor+token+effect+nonce+human veto; read-only does not require write token |
| `G60` | `HOST_VERSION_NATIVE_ABI` | Host Native Owner | `HOST_ABI_UNVERIFIED` | identity+version+OS+loader+session+ACL |
| `G70` | `DONOR_ADMISSION` | SBL DOC06 Owner | `TECH_ADMISSION_UNBOUND` | OriginalDisposition immutable; exact pin+license/NOTICE/SBOM |
| `G80` | `DOMAIN_SUBGRAPH` | GENIEMAKER/G-KNOW Native Owners | `DOMAIN_RECEIPT_UNBOUND` | C31 compiler chain or C38 grounded/currentness/Journal |
| `G90` | `CONSUMER_ACK` | DOC11/DOC12 Native Consumer | `CONSUMER_ACK_UNVERIFIED` | typed receipt same subject/schema; authority verified |

`GateDecision@r4` 必有 `{request_sha,subject_sha,gate_registry_version:"1",evaluation_order:[G00..G90],evaluations[],first_fail_gate,first_fail_code,hard_stop_reason?,design_state:DESIGN_PROPOSAL|HOLD|DENY,actual_native_state:NOT_EXECUTED|RECEIPT_VERIFIED,owner_route,blocked_effects,next_action}`。未有原生 RawReceipt，`actual_native_state=NOT_EXECUTED`；所有 D10-09 CellRuleProof 依 `gate_registry_version=1` 引用，不能自帶不同優先序。

```python
GATE_ORDER = ["G00","G10","G20","G30","G40","G50","G60","G70","G80","G90"]
def decide_gate(request, gate_results, emergency_stop=False):
    # gate_results 只能由各合法 Owner 或明示 DESIGN-only validator 提供，禁止模型補簽
    first = next(((g,gate_results[g]["first_fail"]) for g in GATE_ORDER
                  if gate_results[g]["decision"] in ("DENY","HOLD")),None)
    return {"first_fail_gate":first[0] if first else None,
            "first_fail_code":first[1] if first else None,
            "hard_stop":emergency_stop,
            "effect_dispatch_allowed":False}  # 本文件的設計端永不派發效果
```

**多錯破壞性回歸**：`{source_freeze_missing:true,token_missing:true,host_unverified:true}` 固定首拒 `G10/SOURCE_FREEZE_HOLD`；`{source_ok:true,mode:PREW3_SHADOW,effect:REPO_WRITE,token_missing:true}` 固定 `G30/SHADOW_WORLD_EFFECT_DENIED`；`{source_ok:true,mode:STANDALONE,effect:REPO_WRITE,checker_same_as_maker:true,token_missing:true}` 首拒 `G40/SOD_NOT_INDEPENDENT`；`{source_ok:true,mode:STANDALONE,effect:READ_ONLY,host_unverified:true,donor_pin_missing:true}` 首拒 `G60/HOST_ABI_UNVERIFIED`。以上為**預期 fixture，不是實測 Owner Decision**。


# D10-02｜SourceInventory、ReadCoverage、TermIndex、SourceGap

> **r2 正確適用性說明**：以下「173 檔」及 keyword hits 均為 r1 原版當時的 snapshot，供來源追溯，不是 r2 最新封存分母；本 r4 應以當輪新驗證清冊、AUDIT 本身以及現存實體重新計算。原有搜尋命中不能證成條文適用或原子需求充分性。

</details>

<details>
<summary>DOC-10｜1.1 三 Mode、三工作面與效果的明確判定序｜來源 L57–L68</summary>

## 1.1 三 Mode、三工作面與效果的明確判定序

1. `SourceAuthorityGate`：來源是否有合法文件定位、受驗 hash、有效 Canonical Writer 與原始 `disposition`；缺件可 `DESIGN_READ_ONLY`，不得作 `SOURCE_FROZEN`。
2. `ProductKindGate`：DOC-01 原生 Owner 是否明確授權產品類型；`NOT_V0_1_MVP` 不是 `TRUE_NA`。
3. `ModeGate`：`STANDALONE` 不得冒稱 SWOF；`PREW3_SHADOW` W2 readset 完全匹配且所有工具零效果；`SWOF_CONNECTED` 必須 DOC-11/Native Receiver 同 subject 的合法 H0–H4 gate。
4. `PermissionGate`：DOC-07/Native Owner 檢驗 Token、Issuer、Scope、Expiry、operation；Agent/Skill 文本不能補 Token。
5. `HostGate`：Host 身份、真 native loader、固定版本與 OS、capability probe、tool schema、fresh session、受影 readback；`HostVersion=UNKNOWN` 只能 `UNVERIFIED`。
6. `AdmissionGate`：DOC-06 原始 24+25+386 `AdmissionDecision/SlotRef` 不存在或 QUARANTINED，則只能設計候選、回退或明示 NoFit。
7. `ConsumerGate`：GENIEMAKER Compiler / DOC-11 SWOF Native / DOC-12 Delivery 真簽發 ACK；其中一閘失敗即 `NACK/HOLD`，停止效果、不跳階。

每閘輸出 `{gate, decision:PASS|DENY|HOLD|NOT_APPLICABLE_WITH_OWNER, first_fail:error|null, owner, evidence_expected, next_user_action}`；只有 **在 Owner 決定永久不適用** 才能用最後一值。禁止用 “版本未釘住” 推導 ProductKind 不適用。

</details>

- **跨域修補的 FirstFail**：`DOC10_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-11｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-11(1).md`；SHA-256 `12f8705d780b76f264457c194a6ff359da8d74b5d6d8c83fa245b74d2a37508e`；原章節定位保留；Canonical Writer = 原 SBL DOC-11 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-11｜動態專家路由（邏輯職能，非多人簽署）｜來源 L42–L61</summary>

## 動態專家路由（邏輯職能，非多人簽署）

| 觸發 | 現行 role_id | 專精／設計輸入輸出 | 禁止簽署 |
|---|---|---|---|
| 產品意圖／模式定位 | G01 | SBL Master→Product Truth、Mode Scope | SWOF READY_W3 |
| One Core／三 SP 與 Native 邊界 | G04 | architecture/ABI boundary→C29 C30 | HGK Permit |
| Authority／SourceFreeze | G05 | SourceInventory→AuthorityBinding proposal | 代替正式 PIPD Freeze |
| Normative conform | G08 | DOC-00～09→ConflictLedger | Independent PASS |
| Intent/atoms | P01 | goal+locator→typed requirement atoms | PI Native compile |
| PI／PD late binding | P03／P04 | Canonical PI/PD readthrough→handoff | 假 RepoContext |
| Agent Host／Native Adapter | A01／A02／A12 | typed host/receiver boundary, SWOF projection | Native field 認證 |
| 文件與 provenance | K04 | SourceClause→Trace→DELIVER | 當作語義全量驗收 |
| OSS 方法／選型 | D01／D02／D03／D04 | thin adapters、TechAdmission | 自動安裝任何輪子 |
| Assurance | V01／V02／V03 | POS/NEG/EDGE/SEC、Checker plan | 同一 Maker 自簽 |
| 回饋與受控發行 | R01／R05／R06 | Consumer ACK、W2/W3、FUO | Production Promotion |

**LegacyRoleAliasResolution：** r2 Skeleton 使用 `SBL-R062`（integration coordinator）、`SBL-R063`（risk gate）、`SBL-R064`（gate challenge）。這三者不是現行總表的有效 58-role ID；其責任分別投影到 `G04/K04`、`G08/V02`、`V01/V03` 邏輯職能。**不**宣告獨立 Principal 已指派，也不賦予真 Maker/Checker SoD。來源：Skeleton 行 19–29。

</details>

<details>
<summary>DOC-11｜r2 產品/技術設計修補總則｜來源 L16–L19</summary>

## r2 產品/技術設計修補總則

`r1 列舉存在` **不等於** `r2 功能可施工`。每個直接採用輪子必揭示其 type、設計選型、source-digest、消費端可用輸出、負例、退出、真正由哪個 Owner 允許效果；不符合僅阻 activation，不把產品意圖降成無限期選型待定。計畫與 Native Effect 分離；`ZERO_DESIGN_REDISCOVERY` 只涵蓋本設計已作出的產品及接口裁決，`NATIVE_BINDING_REQUIRED` 必由合法 Owner 供真 schema。

</details>

- **跨域修補的 FirstFail**：`DOC11_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-12｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-12(1).md`；SHA-256 `d1e470d82ca14319582cb8947aa52007927aa38e726249b1430804cfe8c8ca56`；原章節定位保留；Canonical Writer = 原 SBL DOC-12 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-12｜D12-01.PATCH｜七痛點、十六 User Moments、三 Golden Journeys 的 Consumer-first 設計實體｜來源 L39–L83</summary>

## D12-01.PATCH｜七痛點、十六 User Moments、三 Golden Journeys 的 Consumer-first 設計實體

`FUO` 必須由**本地消費者**在當前同 Subject、新會話／乾淨環境中觀測得到，不能以 Writer 自述、`--help`、README、ZIP 存在、`SKILL.md` 可讀或「workflow green」充數。`Design-selected`、`Host-installed`、`Host-effective`、`task-outcome`、`user-accepted`、`provider-off`、`uninstalled` 是相互獨立的狀態，不可互相推導。下面每項以本 DOC12 接收或傳遞的責任呈現，不篡奪 DOC01/03/05/08/11 的源 Owner。

| 痛點 ID | DOC12 具體消費功能 | Input→Output / Oracle | 第一負例與退場 |
|---|---|---|---|
| P01 | 依目標與風險回放 Method/Host/Kind 候選及 no-fit 理由 | IntentRef→DeliveryRoute(accepted/refused,reason,owner)；不需用戶猜品牌 | 未 pin 的外部工具直接被選為 READY→TOOL_PIN_MISSING；回 STANDALONE read-only |
| P02 | `SPEC → PI → PD → ONE ECP → Build → DELIVER` 的同 subject handoff | 每條 edge 有 from/to/subject_sha/owner/receipt/ref，沒有 orphan | 不同 SHA、遺失 NFR/Scope→HANDOFF_SUBJECT_MISMATCH；NACK |
| P03 | 讀 DecisionLedger/Checkpoint 做低摩擦 resume | decision_id+source_hash+checkpoint →保留已回答資料；新未知只開 TT | 重問或用舊 checkpoint 重放effect→RESUME_REPLAY_DENIED |
| P04 | 依 AuthorityBinding 路由 Native Owner，禁止第二 Writer | owner_graph+field_scope→one writer lease or HOLD | Candidate 文稿鑄造 PIPD/SWOF 正式文號→AUTHORITY_COLLISION |
| P05 | POS/NEG/EDGE/SEC 與真 checker 分離 | RawResult 同 SHA + distinct principal → acceptance candidate，未具憑證阻擋 | exit0/LLM 評語冒充 independent pass→INDEPENDENT_RECEIPT_MISSING |
| P06 | 四 Host×SP 逐格 Native session/install/trigger/nontrigger/uninstall | cell_id+pin/host_version→InstallSessionClosure；DeepSeek 3 格 NOT_ADMITTED | 1 格成功冒稱 12 格/Zip 假生效→HOST_CELL_FALSE_COVERAGE |
| P07 | Time-to-FUO＋clean install＋實際 user outcome | GJ01/02/03各 `consumer_action, observed_state, cleanup, receipt` | README/help/空 JSON/假 agent success→FUO_NOT_OBSERVED |

### D12-01.PATCH.1｜GJ01：CLI_TOOL Standalone 乾淨環境交付

**入口**：M00/M01 定位使用者想做的待辦；M02/M03 frozen Intent、`REQ-CLI-ADD/LIST`, `ACC-PERSIST`；M04/M05 產生受 scope 限定的模組依賴 DAG；M06 經 PIPD PI/PD 或 Local standalone lawful route 綁定來源／scope。**建置**：只取 M1（Spec）M3（test）M5（packager）M6（delivery）必需節點；artifact path、hash、license、version 與 rollback 在單一 `DeliverBOM`。**安裝**：在本機乾淨 tmp prefix install，不改 HOME；`sbl-todo add --title '<unique>'` 回 transaction id，`sbl-todo list --json` 必含該 id/title/status 且 exit=0；關閉重開後再 list 與 non-empty JSON；錯參數不得做任何 mutation。**卸載**：按 BOM reverse dependency，退出後 process/path/schema/residue clean；同 SHA 的 InstallSession 有真 native receipt 方可請求 qualified，否則 `HOLD`。**NEG**：只有 `--help`、README、檔案 exists、stdout 示意、無持久 readback→`FUO_TASK_NOT_FOUND`。**Provider off**：本地 CLI 仍需能運行；關閉遠端後功能不得依賴遠端 Agent。

### D12-01.PATCH.2｜GJ02：Brownfield 受影響改動與可逆交付

**入口**：M00–M06 以真 `RepoContext{root,HEAD,tracked_files,writable_scope,lock}` 及原 Spec Delta 同步；無 HEAD 或其 drift 即 `PD_BIND_HOLD`。選 OpenSpec `OS-02` delta + Spec Kit `SK-03` task DAG + Superpowers `SP-02/SP-03` Red→Green 小修。**Effect boundary**：ONE ECP、token、at-most-once、rollback pointer；執行端只能對批准 diff 內做更動，Maker 不得讓自己當 checker。**結果**：現行 SHA/HEAD、diff allowlist、原子測試的真 Red before / Green after、受影響測試及 Repo 最終 readback；D12-04 BOM 只收可逆變更與 rollback refs。**NEG**：stale HEAD、out-of-scope path、零測試、未核准 PR 修改使測試 exit0→`REPAIR_SCOPE`/`RAW_TEST_MISSING`。**Provider-off**：可唯讀檢視與候選計畫，不能讓缺 provider 才過關的 mutation 偷渡。**退出**：git restore 只在確切簽可回復 path/ref 及 Repository Owner approve 後允許；本 DOC12 不執行。

### D12-01.PATCH.3｜GJ03：Agent Skill/Minimal Agent 真任務與安全拒收

**入口**：M00–M06 決定 Host=Hermes/Codex/Claude Code 及 private Web surface（必各自 ABI），實體 Host 須真 version+loader path+skill hash+Host effective probe；DeepSeek native skill 在缺原生 loader 時三格 `NOT_ADMITTED`。**結果**：針對明確意圖觸發後，允許的 read-only 容器內產出 user-requested machine-readable `output_ref`/`task_id`/`evidence_ref`；同時非觸發時不載入，越權寫入確實被拒且無 side effect；重新開 session、重測 provider-off 及 uninstall residue。**NEG**：只有 `SKILL.md`/manifest 存在、agent 說 done、自己給自己 checker receipt、模型 API 被當原生 skill runtime→`HOST_EFFECTIVE_LOAD_MISSING` 或 `SELF_ACCEPTANCE_DENIED`。**安全**：任一對 Host/Repo/GUI 的 effect 需由真 HGK/Local native principal 授權，不由聊天 prompt 自動觸發。

### D12-01.PATCH.4｜16 Moments 在 DOC12 的精確消費介面

| Moment | 上游原語義 | DOC12 Consumer Input→Output | Positive / Negative / 轉交 Owner |
|---|---|---|---|
| M00 Understand | 需求方的原始語句／附件 | `M00` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `SourceInventory→IntentRecord`；DOC12 只消費，不取代上游 writer | POS=需求被精確引用；空來源拒收; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Source Freeze |
| M01 Explore | 尚不確定可行性目標 | `M01` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `Explore/DecisionLedger`；DOC12 只消費，不取代上游 writer | POS=有效可行性分歧；無來源不問假問題; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，TPM |
| M02 Define | 產品願景/JTBD | `M02` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `ProductBrief/FUO/MVP/NonGoal`；DOC12 只消費，不取代上游 writer | POS=Owner 確定可量測成果；禁止抽象「做一個系統」當 FUO; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，PM |
| M03 Specify | 凍結需求/Oracle cues | `M03` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `PI atoms/Acceptance/Verification`；DOC12 只消費，不取代上游 writer | POS=至少一條驗收與非零分母；Provider-off 只輸出候選; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，PIPD |
| M04 Architect | NFR/RepoContext | `M04` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `Domain/ADR/Threat/Interface`；DOC12 只消費，不取代上游 writer | POS=方案權衡具來源；缺 Native Context 不冒充已綁 PD; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，SE |
| M05 Plan | Task Spec/Dependency | `M05` 來源條文/決策 → `SOURCE_READER` 中綁定 exact subject、scope、version 的 `有向無環 DAG/Owner/Milestone`；DOC12 只消費，不取代上游 writer | POS=有合法 Task；拒孤兒與環; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，TPM |
| M06 Prepare | Repo HEAD/WritableScope/ECP | `M06` 來源條文/決策 → `RECEIVER_GATE` 中綁定 exact subject、scope、version 的 `PD Construction Binding+TQAEP`；DOC12 只消費，不取代上游 writer | POS=準備合法施工；無真 RepoContext BLOCK; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，PIPD |
| M07 Build | 核准 WorkOrder/Permit | `M07` 來源條文/決策 → `DELIVER_SESSION` 中綁定 exact subject、scope、version 的 `受控 Worker ChangeSet`；DOC12 只消費，不取代上游 writer | POS=真產物；禁止無許可 Repo 修改; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，HGK/Local Owner |
| M08 Test | 現行候選及 Test Oracle | `M08` 來源條文/決策 → `DELIVER_SESSION` 中綁定 exact subject、scope、version 的 `Raw Logs/Exit/Trace`；DOC12 只消費，不取代上游 writer | POS=可重播 Test；拒假 Exit0/零測試; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Runner |
| M09 Review | 正確 Candidate SHA+diff | `M09` 來源條文/決策 → `RECEIVER_GATE` 中綁定 exact subject、scope、version 的 `Reviewer Findings`；DOC12 只消費，不取代上游 writer | POS=品質意見精確定位；自簽不能算獨立; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Checker |
| M10 Verify | 同版本/Scope 之實體證據 | `M10` 來源條文/決策 → `RECEIVER_GATE` 中綁定 exact subject、scope、version 的 `Local AO/Acceptance Receipt`；DOC12 只消費，不取代上游 writer | POS=實際功能符合；foreign evidence 拒收; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，AO |
| M11 Repair | FirstFail/RepairScope | `M11` 來源條文/決策 → `RECEIVER_GATE` 中綁定 exact subject、scope、version 的 `RepairCone/Scoped Rerun`；DOC12 只消費，不取代上游 writer | POS=最小改動重測；STOP shotgun repair; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Commander |
| M12 Ship | ReleaseAuthority/Pin/Rights | `M12` 來源條文/決策 → `DELIVER_SESSION` 中綁定 exact subject、scope、version 的 `GitHub Tag/Assets/Provenance`；DOC12 只消費，不取代上游 writer | POS=新環境實裝使用；無批准不發; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Release |
| M13 Maintain | 已發行版本+事故/使用紀錄 | `M13` 來源條文/決策 → `RECEIVER_GATE` 中綁定 exact subject、scope、version 的 `Repair/Migration/Regression`；DOC12 只消費，不取代上游 writer | POS=確實可復原；不可偷換 Oracle; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ01/02/03，Ops |
| M14 Host Portability | 4 Host × 各 SP/Full Stack | `M14` 來源條文/決策 → `DELIVER_SESSION` 中綁定 exact subject、scope、version 的 `NativeInstall/EffLoad/Uninstall`；DOC12 只消費，不取代上游 writer | POS=每宿主真作用；無效裝載拒 PASS; NEG=無原子來源/未核准 effect/跨 SHA 冒充成果；Owner=GJ03/Host UAT |

</details>

<details>
<summary>DOC-12｜D12-01.3｜`PrimaryProductKind` 與 `DeliveryArtifactKind` 正交，Owner 先算 Applicability｜來源 L107–L123</summary>

## D12-01.3｜`PrimaryProductKind` 與 `DeliveryArtifactKind` 正交，Owner 先算 Applicability

`PrimaryProductKind` 必須先由產品權威合法 enum 得到，絕不從 ZIP 或 workflow 反向推導。`DeliveryArtifactKind` 僅表傳輸載體，如 `CLI_BINARY`、`AGENT_SKILL_BUNDLE`、`HOST_ADAPTER`、`WEB_PRIVATE_SP`、`SPEC_PACKAGE`、`CONSTRUCTION_PACKET`、`EVIDENCE_PACKAGE`、`WORKFLOW_RUNBOOK`，不得混列為正式產品類。其餘維度獨立：`Host=HERMES|CODEX|CLAUDE_CODE|DEEPSEEK_DECLARED|null`、`Mode=STANDALONE|PREW3_SHADOW|SWOF_CONNECTED`、`OS/Arch`、`ProfileBinding`、`SWOF Native Permit`。Web GPT/Claude Web 不是上述 Native Host 的等價 Host，也不能由 agent prompt 證明 native tool-effect。

`Applicable(product,artifact,host,os,arch,mode) = PrimaryEnumValid ∧ ScopeSupported ∧ DOC01_Eligibility ∧ DOC11_ModeAdmission ∧ HostABI_Qualified ∧ ProfileVetoSatisfied ∧ PermissionsValid ∧ ExactSubjectBound`。`UNKNOWN` 不轉 `false N/A`，而輸出 `UNRESOLVED_HOST_CAPABILITY`／`OWNER_DECISION_REQUIRED`。`UNSUPPORTED` 和 `SWOF_RESERVED` 即使有 ZIP 亦永遠不能變 SBL Native Release。合法 N/A 必留 reason、Native Owner、source ref 與負例 oracle。

| 正交資料類型 | 實質例子 | Gate 標準拒收 |
|---|---|---|
| `ProductDeliveryBinding` | `CLI_TOOL + CLI_BINARY + STANDALONE + linux-amd64` | 產品 enum、載體、模態各自強型別驗證 |
| `HostSurfaceBinding` | `AGENT_SKILL + AGENT_SKILL_BUNDLE + CODEX + STANDALONE` | 需 Codex 原生目錄/載入 readback；Web 不算等價 |
| `WebProfileDistribution` | `AGENT_SKILL + WEB_PRIVATE_SP + WEB_GPT_TPM` | 可作規格投影，不代 native Host UAT |
| `NativeOwnerRestricted` | `GENIE/GENIE.md + SWOF_CONNECTED` | SWOF 正式 Native readset/ACK/permit 不可缺 |

**DENY fixtures**：`HOST_ADAPTER` 當 PrimaryProductKind → `INVALID_PRIMARY_PRODUCT_KIND`；`SIMPLE_AGENT` 不在產品矩陣卻標全已測 → `APPLICABILITY_MISSING_KIND`；未知 mode 默准 → `MODE_ADMISSION_MISSING`。

# D12-02｜Source Identity、Authority、P4 生效與跨 DOC 依賴

</details>

- **跨域修補的 FirstFail**：`DOC12_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。

### SBL DOC-13｜原產品功能與本次 FHS 消費接口
- 唯讀原件：`SBL_PIPD-LS-PKG_DOC-13(1).md`；SHA-256 `7cc0c8b17311130c875910b2548b93c28bd4e1c8ee04d300f85fc33d4c09beb1`；原章節定位保留；Canonical Writer = 原 SBL DOC-13 Owner。
- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。
- POS：各原片段的領域成功 predicate 與原功能輸出均須由同 Scope Reader 讀回；NEG：任何禁用功能、跨 Host、憑檔名宣稱安裝、跨域冒 Canonical 與偽造 Checker 收據均拒收；缺者只受影 HOLD。
- Exit：無效果者丟棄候選或重讀；真效果由原 ECP/Owner 的 preimage、compensation、residue 與 requalification 處置，不消除 SBL Full Product 義務。
**原條款的上下文節選（非額外 Normative）**：
<details>
<summary>DOC-13｜C46.11｜對 C45/C47 的完整退出與 requalification 消費回路｜來源 L572–L576</summary>

## C46.11｜對 C45/C47 的完整退出與 requalification 消費回路

每 `DriftEvent{kind:PIN|ADVISORY|LICENSE|ABI|HOST|PROVIDER|MODEL|SCHEMA|POLICY|MODEGATE|REPO_HEAD,oldhash,newhash,source_item_id,slot_id?,source_version,detected_at,source_refs}` 依 R90.16 Projection 查回 source original status；`affected_GJ` 至少檢測三 journey 適用性，`affected_loop` 給三 ontology 語義差異，`TestRequalClosure` 需出 positive/negative/edge/sec；未定位原 ID 拒收 `TECH_ID_UNBOUND`，未定位原 License/Pin 拒收 `TECH_ADMISSION_DENY`。Owner route：DOC-06 准入來源→DOC-05 Repo/Binding→DOC-08 Checker→DOC-09 Ledger→DOC-10 Host→DOC-11 SWOF→DOC-12 Migration/DELIVER。任何 downstream ACK 只能證明消費合約相容，不能背書正式獨立 PASS。

</details>

- **跨域修補的 FirstFail**：`DOC13_SOURCE_SCOPE_OR_NATIVE_BIND_HOLD`；恢復條件：原 DOC Owner/Reader 的同版 Input/Output/NEG、Host Caps 與必要 PIPD/HGK Readback 齊備；不因設計成功宣稱 Host Installed。


## 本輪同域受影修復：r2 §1.4 15 TDR與原Kind經驗

### 1.4 SBL 15 個原 TDR Wheel 的逐項產品路由

| TDR | 原 Wheel／能力 | Need→原有/可採能力→Output／原 Consumer | Effect／NoFit／回退 |
|---|---|---|---|
| TDR-01 | PIPD-LS-SP/P4 | Source/Goal→19 Schema/13 CLI/8 Skill→PI/PD/ECP/TQAEP | 原 Writer；無 Schema 合法 ABI→PIPD_HOLD |
| TDR-02 | Fabric/HG-KSEOS | 受治理 Effect→Policy/Issuer/Spine→Permit/WorkOrder/World | 不可換 Issuer；未 Consumed→POLICY_HOLD |
| TDR-03 | GPTs_GENIEMAKER | GENIE/Host Need→GENIE.md、原 Source/Scope refs、Host load→Genie Result | Loader 未合格保留 Draft，不能假稱已部署 |
| TDR-04 | OpenSpec | Brownfield Change→Explore/Delta/CLI validate→Source-bound Spec Candidate | 原 PIPD/Repo Consumer，Warning→CHANGE_HOLD |
| TDR-05 | Spec Kit | Greenfield Plan→Constitution/Specify/Plan/Tasks→PIPD Proposal | 全域 Hermes Skill 衝突→隔離，原欄位不變 |
| TDR-06 | gstack | Product/UX/QA Need→OfficeHours/QA/Review→Finding/Retro | `/ship` 不能 Release，未合格維持方法候選 |
| TDR-07 | Superpowers | Coding/Failure Need→TDD/Debug/Review→RedGreen/Smallest Repair | 原 Worker/Checker，禁自簽 PASS |
| TDR-08 | Matt Skills | 需求/已知答案→Grill/Domain/Glossary/Ticket→ReqAtomProposal | QuestionLedger 去重，缺合法來源只 Need |
| TDR-09 | AGENTS.md | Repo Host Need→讀指令來源、信任層級、SourceSHA→Project Guidance | Prompt-injection 不可提升 Permit |
| TDR-10 | challenge-review Skill | Frozen Case/Raw→異構批判→Advisory Finding | 轉原 Challenge AC 邊，不是 Protected AO |
| TDR-11 | construction-acceptance-prompt-compiler Skill | 原 WorkOrder/ECP/Oracle→有界 Worker Prompt/CaseSpec Candidate | 無 Permit 不可執行真效果 |
| TDR-12 | SDLC_PRW_HLPE | Source/PRW/Checkpoint→原 WorkPlan/Resume Hint | 不產第二 Journal；過期 Memory NACK |
| TDR-13 | SRU_OROCHI | Incident/FirstFail→KnownFix/Smallest Repair/Compensation Proposal | 先核 Freshness；UNKNOWN Effect 不盲重試 |
| TDR-14 | AI_AGENT_SPEC | Agent Role/Tool Permission→Skill/RoleContract+Host Bound Result | 限原 Host 真 Load/ACL，不臆造 Principal |
| TDR-15 | GSD/planning-with-files | Context/Phase/Resume Need→可讀 Phase/Checkpoint 方法→原 Program Plan Input | 不啟動另一排程狀態機 |

### 1.5 SBL 七痛點的端到端可驗效果

P01：MethodDecision 不把 Tool Choice 推回使用者；P02：同 Subject、Typed ACK/NACK、五出口資料不丟；P03：已回答不再問、Source 改版才局部問；P04：外部工具只給 Candidate、不覆寫 Canonical；P05：世界 Raw＋專屬 NEG＋Protected Checker 防虛假 PASS；P06：Package/Install/Load/Trigger/Uninstall 逐級有效；P07：正常 Goal 有 First Useful Outcome、可重播且可回退。測量直接用原 `elapsed_ms/questions_reasked/error_count/provider_off/consumer_acceptance`，不建 KPI 平台。[SBL DOC00 R00；BODY09/12]


---



## R2 14冊逐條功能修補原生接收路由

- DOC-00：45條帶量詞原句逐條掃描，拆為 262 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-00_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `3dc07137d4921f42cd7950e1d077295307a2d2db3585a627189cfbb41164989e` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-01：81條帶量詞原句逐條掃描，拆為 594 個具名子項 + 149 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-01_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `58df0c623b979c87fb18aa8f12fe27d4b4695204c1a0a20c0f564bc5bf551d4a` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-02：119條帶量詞原句逐條掃描，拆為 763 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-02_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `ebdf1440acda7571d15a5b68572c404e54ef96295ecff1b8abc11c728af121b9` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-03：210條帶量詞原句逐條掃描，拆為 2393 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-03_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `3313459d948d9eed45e11bda9c18db2dbe7a042ae154ff3d0d68692716878ac6` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-04：51條帶量詞原句逐條掃描，拆為 252 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-04_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `562b734e387cb6fdaf3023d72987dec40047c7e67947f5d733db776619574ce0` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-05：97條帶量詞原句逐條掃描，拆為 587 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-05_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `7037e4c8bf17ccd7f901f5922e40cf48493aa2afbe8a83a931ad73fa6704d79b` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-06：13條帶量詞原句逐條掃描，拆為 89 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-06_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `d98ca519ed1418ece75206ae770893b55d016aae89f60e40d94b761520046c3a` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-07：76條帶量詞原句逐條掃描，拆為 424 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-07_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `30f3a0d3ee3c5d033b7f5bf26ec69ff9e17722b66620751a6dca814513463c31` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-08：25條帶量詞原句逐條掃描，拆為 131 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-08_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `92cac11da74866fba99daae22a5c72f1e8eae1b0c651bc359aa08ebeae380abd` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-09：52條帶量詞原句逐條掃描，拆為 340 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-09_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `ef5e514980b2a4a1354e8b662bfc0aa7038d151d3259860ceb250383bc267229` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-10：51條帶量詞原句逐條掃描，拆為 324 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-10_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `e87ece230f6c9e3eab31e07993a1a51b6f2da993e4065a6e6e0cc2ad0eadefe9` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-11：125條帶量詞原句逐條掃描，拆為 516 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-11_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `3b6b0927c058eba1d5a7242b24c08e93c508cffefa65c2ca4724daa13269a045` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-12：62條帶量詞原句逐條掃描，拆為 507 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-12_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `5d21deae2c9dafa292fa0e9e6ee5e3c416c3c2112628ec2c2109b2daf9563f25` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。
- DOC-13：54條帶量詞原句逐條掃描，拆為 467 個具名子項 + 0 個 ContextualChild；直接讀本封包 `SBL_DOC00_13_INTEGRATED_READER_UPGRADES/SBL_PIPD-LS-PKG_DOC-13_FHS_INTEGRATED_UPGRADE.md` 的有效 DeltaSpec。原正文 SHA `90de1ed79820d8e7eb30014f8e40ff518d555433868a1d25d47f4debb0993ac1` 另存唯讀回歸歸檔；這是**新跨域接收候選**不等於原 SBL 產品 Owner 批准。


## R2 Contextual Child 149 專項有效 Consumer/Oracle（逐原 ID）

每個原 Child 的 Parent 原句、實際短句、POS、NEG、第一失敗都是本版讀取器的單獨作用域；不得以總表 149/149 替代個別執行。

<a id="current-cebffe169fab9e8d2923"></a>
### CHILD-U01.1｜U01：專用合約
- 原 Parent：SBL 是獨立品牌，名稱不與 SWOF GENIE Lifecycle 混同
- 子要求：SBL 是獨立品牌；來源 `SRC-L-041`、原 clause SHA `343e9f22d0cebbbdefa6390bfb2df3d341d93f4749706f9dd252510027c4d6ee`；原 Owner `SBL_PRODUCT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`產品顯示品牌為SBL`。
- **NEG / FirstFail**：將結果變為 `顯示為SWOF`，原 Reader 必回 `DOMAIN_U01_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U01.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d5dee8bc50111601b5bc"></a>
### CHILD-U01.2｜U01：專用合約
- 原 Parent：SBL 是獨立品牌，名稱不與 SWOF GENIE Lifecycle 混同
- 子要求：名稱不；來源 `SRC-L-041`、原 clause SHA `d88ac6c4d15a967496e6f9571d4a08ad2c38ef48b2654b48d785602dfcca98e9`；原 Owner `SBL_PRODUCT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`名稱解析SBL與SWOF為不同identity`。
- **NEG / FirstFail**：將結果變為 `SBL名稱alias指向SWOF`，原 Reader 必回 `DOMAIN_U01_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U01.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-780ea4d8e5910e9a9822"></a>
### CHILD-U01.3｜U01：專用合約
- 原 Parent：SBL 是獨立品牌，名稱不與 SWOF GENIE Lifecycle 混同
- 子要求：SWOF GENIE Lifecycle 混同 (L5504)；來源 `SRC-L-041`、原 clause SHA `992339747baaddee4af384b99d1e9a0c3471953ba13722c50eaee9d979f7a9cc`；原 Owner `SBL_PRODUCT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`GENIE Lifecycle權威不由SBL接管`。
- **NEG / FirstFail**：將結果變為 `SBL成GENIE canonical writer`，原 Reader 必回 `DOMAIN_U01_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U01.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-69335fa113bcf66a05b9"></a>
### CHILD-U02.1｜U02：專用合約
- 原 Parent：SBL 有 TPM-SP、Commander-SP、External Challenge-SP 三個獨立 SP
- 子要求：SBL 有 TPM-SP；來源 `SRC-L-041`、原 clause SHA `cb6e9a03a45aeefc1f211331096c77cd21955f25d2206cdca58d9854c4efc28a`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`TPM有獨立入口與邊界`。
- **NEG / FirstFail**：將結果變為 `TPM併入Commander credential`，原 Reader 必回 `DOMAIN_U02_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U02.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-46dec6042f42ab2c3dc2"></a>
### CHILD-U02.2｜U02：專用合約
- 原 Parent：SBL 有 TPM-SP、Commander-SP、External Challenge-SP 三個獨立 SP
- 子要求：Commander-SP；來源 `SRC-L-041`、原 clause SHA `a56ec318d7c59d3e03c07e772c69a83c2392c8c1fc1081165cda766f1456d6a3`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Commander獨立只讀會話`。
- **NEG / FirstFail**：將結果變為 `Commander寫Target Repo`，原 Reader 必回 `DOMAIN_U02_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U02.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-19c9b74eedd38499a885"></a>
### CHILD-U02.3｜U02：專用合約
- 原 Parent：SBL 有 TPM-SP、Commander-SP、External Challenge-SP 三個獨立 SP
- 子要求：External Challenge-SP 三個獨立 SP (L5505)；來源 `SRC-L-041`、原 clause SHA `d859f849371efb4c1185d008274f89b49726a8529aa78076136a6e7cb92d7af4`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Challenge獨立frozen readset會話`。
- **NEG / FirstFail**：將結果變為 `Maker同會話自審`，原 Reader 必回 `DOMAIN_U02_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U02.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-dba02c9feb0228835cfb"></a>
### CHILD-U03.1｜U03：專用合約
- 原 Parent：Web GPT 三 SP 各自可真正安裝、掛載、調用
- 子要求：Web GPT 三 SP 各自可真正安裝；來源 `SRC-L-041`、原 clause SHA `146c8d84091554efe7002bbaa95aa2736f9a148a1d768013c504b8254ced1a17`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`TPM/Commander/Challenge各有本Host安裝Raw`。
- **NEG / FirstFail**：將結果變為 `只安裝TPM`，原 Reader 必回 `DOMAIN_U03_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U03.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-788666b87286445add68"></a>
### CHILD-U03.2｜U03：專用合約
- 原 Parent：Web GPT 三 SP 各自可真正安裝、掛載、調用
- 子要求：掛載；來源 `SRC-L-041`、原 clause SHA `070d16eee37f9d51b3c9fcd8274e7df052a43adf1d78ce6e2c0bfbe6adf9ea3e`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`三SP各有fresh-session loaded SHA`。
- **NEG / FirstFail**：將結果變為 `磁碟存在當loaded`，原 Reader 必回 `DOMAIN_U03_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U03.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-54d5a5447c067c4f016a"></a>
### CHILD-U03.3｜U03：專用合約
- 原 Parent：Web GPT 三 SP 各自可真正安裝、掛載、調用
- 子要求：調用 (L5506)；來源 `SRC-L-041`、原 clause SHA `b9ec027bed5c274ea6cb25dd13248303ce519bbcaa93b9811c58aa511a7ff56d`；原 Owner `SBL_ARCHITECT_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`三SP各有trigger/nontrigger/卸載後不觸發Raw`。
- **NEG / FirstFail**：將結果變為 `借一SP invocation給其餘`，原 Reader 必回 `DOMAIN_U03_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U03.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-5a483be5a7dcab48aa5a"></a>
### CHILD-U04.1｜U04：專用合約
- 原 Parent：TPM-SP 保留 PIPD-LS-SP 原標準和 Repo，並可讓原用戶單獨使用
- 子要求：TPM-SP 保留 PIPD-LS-SP 原標準和 Repo；來源 `SRC-L-041`、原 clause SHA `d6796a0267ab49bc51a5f65745b13739fb7ca1b3b41f663891851f55784281b4`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PIPD原Repo/標準與Writer持續可讀`。
- **NEG / FirstFail**：將結果變為 `重建第二PIPD Compiler`，原 Reader 必回 `DOMAIN_U04_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U04.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-12ef70eb3f05beb61a34"></a>
### CHILD-U04.2｜U04：專用合約
- 原 Parent：TPM-SP 保留 PIPD-LS-SP 原標準和 Repo，並可讓原用戶單獨使用
- 子要求：並可讓原用戶單獨使用 (L5507)；來源 `SRC-L-041`、原 clause SHA `d0617aee313e6d211894c98c204cd65cf5b96316a2d086ad6043790148b7aa78`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`原PIPD用戶不用SBL wrapper仍能獨立使用`。
- **NEG / FirstFail**：將結果變為 `強制先裝SBL Stack`，原 Reader 必回 `DOMAIN_U04_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U04.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a3e99db6404600246ab0"></a>
### CHILD-U05.1｜U05：專用合約
- 原 Parent：TPM-SP Product Manager 釐清 JTBD、FUO、MVP／Non-goals
- 子要求：TPM-SP Product Manager 釐清 JTBD；來源 `SRC-L-041`、原 clause SHA `99f482d67436b43443e3c7c4fdbaf0f3dbe218abf87772503b0a8f3a803151a4`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`JTBD連結persona/pain與可見工作結果`。
- **NEG / FirstFail**：將結果變為 `把工具清單當JTBD`，原 Reader 必回 `DOMAIN_U05_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U05.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-0e631a24eba25efaec40"></a>
### CHILD-U05.2｜U05：專用合約
- 原 Parent：TPM-SP Product Manager 釐清 JTBD、FUO、MVP／Non-goals
- 子要求：FUO；來源 `SRC-L-041`、原 clause SHA `c55bdfcc914b277d0488d0f655e0abca35001d0bc96d6a3ddc0f93b0e5000121`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`FUO為使用者可取用成果且有ACC`。
- **NEG / FirstFail**：將結果變為 `只有文件計數`，原 Reader 必回 `DOMAIN_U05_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U05.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-036bd1c6b039636c7e1c"></a>
### CHILD-U05.3｜U05：專用合約
- 原 Parent：TPM-SP Product Manager 釐清 JTBD、FUO、MVP／Non-goals
- 子要求：MVP；來源 `SRC-L-041`、原 clause SHA `adeab142bcf413ca9d832a392f36bea34cd847fbc05a4420db35baf665bedf72`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`MVP邊界列必要功能與驗收`。
- **NEG / FirstFail**：將結果變為 `把Full Product全項灌入首切片`，原 Reader 必回 `DOMAIN_U05_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U05.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-263e90aba80205d44cac"></a>
### CHILD-U05.4｜U05：專用合約
- 原 Parent：TPM-SP Product Manager 釐清 JTBD、FUO、MVP／Non-goals
- 子要求：Non-goals (L5508)；來源 `SRC-L-041`、原 clause SHA `89ee66dec40061f87ed3c4751b6bc44ee1d817c9692c65351809d7158d3a0af6`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`non-goals可拒超範圍請求`。
- **NEG / FirstFail**：將結果變為 `non-goal被默當必做`，原 Reader 必回 `DOMAIN_U05_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U05.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-c869c1f69a371ac88bb1"></a>
### CHILD-U06.1｜U06：專用合約
- 原 Parent：TPM-SP Systems Engineer 建模 Domain、NFR、Architecture、ADR
- 子要求：TPM-SP Systems Engineer 建模 Domain；來源 `SRC-L-041`、原 clause SHA `467ae1ea0c9e53f3e20eb8fa6b17cd94ac9e6f2d6040a3cd987930bf667ad107`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Domain模型有實體/關係/所有權`。
- **NEG / FirstFail**：將結果變為 `多Owner同寫同物件`，原 Reader 必回 `DOMAIN_U06_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U06.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b283ecf606950a0c216e"></a>
### CHILD-U06.2｜U06：專用合約
- 原 Parent：TPM-SP Systems Engineer 建模 Domain、NFR、Architecture、ADR
- 子要求：NFR；來源 `SRC-L-041`、原 clause SHA `bdee988e7cf1542196b10385812c996a61e9e1c9ee101b28e0910ea0e0aa7098`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`NFR有來源條款與測量方式`。
- **NEG / FirstFail**：將結果變為 `未校準數值冒SLA`，原 Reader 必回 `DOMAIN_U06_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U06.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-25ed6f2ca54074afe8e0"></a>
### CHILD-U06.3｜U06：專用合約
- 原 Parent：TPM-SP Systems Engineer 建模 Domain、NFR、Architecture、ADR
- 子要求：Architecture；來源 `SRC-L-041`、原 clause SHA `ac9d4a2687372403521be2cc541ec908ddfc2d80dfe48b94337b182709207faf`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Architecture seam有producer/consumer/effect`。
- **NEG / FirstFail**：將結果變為 `只有架構圖無reader`，原 Reader 必回 `DOMAIN_U06_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U06.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-25b69e6b3245d98933b7"></a>
### CHILD-U06.4｜U06：專用合約
- 原 Parent：TPM-SP Systems Engineer 建模 Domain、NFR、Architecture、ADR
- 子要求：ADR (L5509)；來源 `SRC-L-041`、原 clause SHA `deacac687b71f2a12021cc06020fa340466ed2245639bc2581ec2f21a4e2dae6`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`ADR保留選項/理由/被拒替代`。
- **NEG / FirstFail**：將結果變為 `先選型後補造決議`，原 Reader 必回 `DOMAIN_U06_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U06.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-588e7180453fd4588b6b"></a>
### CHILD-U07.1｜U07：專用合約
- 原 Parent：TPM-SP Technical Program Manager 建任務 DAG、里程碑、風險、交接
- 子要求：TPM-SP Technical Program Manager 建任務 DAG；來源 `SRC-L-041`、原 clause SHA `45c0626686c532dc8f997c3a5d60e4f6de8fa681038639e9e9e882004bc101a6`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`DAG拓樸可排序且無環`。
- **NEG / FirstFail**：將結果變為 `注入06到17反向依賴`，原 Reader 必回 `DOMAIN_U07_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U07.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-024d5939637372aca36b"></a>
### CHILD-U07.2｜U07：專用合約
- 原 Parent：TPM-SP Technical Program Manager 建任務 DAG、里程碑、風險、交接
- 子要求：里程碑；來源 `SRC-L-041`、原 clause SHA `6751a1c7223ad7235f1723a2d2fa8d94b8e32792f206b740aa866f77d1b83f37`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`里程碑有可見輸出與依賴`。
- **NEG / FirstFail**：將結果變為 `只列日期無交付物`，原 Reader 必回 `DOMAIN_U07_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U07.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-fdeaa3c87738ed532b5b"></a>
### CHILD-U07.3｜U07：專用合約
- 原 Parent：TPM-SP Technical Program Manager 建任務 DAG、里程碑、風險、交接
- 子要求：風險；來源 `SRC-L-041`、原 clause SHA `5d353b88a4e9d80ce1a1389a4a3232cfe07f40ef0c4e474fca57d46bae67c20b`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`風險含trigger/owner/回復`。
- **NEG / FirstFail**：將結果變為 `高風險無責任Owner`，原 Reader 必回 `DOMAIN_U07_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U07.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9a45b354735a052582bd"></a>
### CHILD-U07.4｜U07：專用合約
- 原 Parent：TPM-SP Technical Program Manager 建任務 DAG、里程碑、風險、交接
- 子要求：交接 (L5510)；來源 `SRC-L-041`、原 clause SHA `e6cc3bf5de036680a7a4e01dc638e79740732c02eb4720c6586cf68941932c8a`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`handoff有exact subject/hash/next action`。
- **NEG / FirstFail**：將結果變為 `只交長Prompt無來源`，原 Reader 必回 `DOMAIN_U07_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U07.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-26a77c3976fad38db24b"></a>
### CHILD-U08.1｜U08：專用合約
- 原 Parent：TPM-SP Quick/Guided/Critical 依難度動態問答
- 子要求：TPM-SP Quick；來源 `SRC-L-041`、原 clause SHA `17ada52c07a3837f97181331fe4d3c96c143bc663ed3bfd38036205fcc64336b`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Quick重用已知答覆直接形成候選`。
- **NEG / FirstFail**：將結果變為 `重問已知Goal`，原 Reader 必回 `DOMAIN_U08_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U08.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-f2ed7410a09093f39ec3"></a>
### CHILD-U08.2｜U08：專用合約
- 原 Parent：TPM-SP Quick/Guided/Critical 依難度動態問答
- 子要求：Guided；來源 `SRC-L-041`、原 clause SHA `1f655539398d6971748b8c0fa38e9a86e4e8c02b5d2fb576c614ba71c262a081`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Guided只問會改FUO的缺項`。
- **NEG / FirstFail**：將結果變為 `要求重上傳內建DOC`，原 Reader 必回 `DOMAIN_U08_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U08.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-213546cf2a87dbb8c87b"></a>
### CHILD-U08.3｜U08：專用合約
- 原 Parent：TPM-SP Quick/Guided/Critical 依難度動態問答
- 子要求：Critical 依難度動態問答 (L5511)；來源 `SRC-L-041`、原 clause SHA `f8aa2e2ef766ba7efb7d5e70097cc44a16d4e0d5621ba2f688fc3a4db7a9e5d5`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Critical對未知效果與Owner衝突升級`。
- **NEG / FirstFail**：將結果變為 `把高風險降到Quick`，原 Reader 必回 `DOMAIN_U08_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U08.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a4594215e730c20a626a"></a>
### CHILD-U09.1｜U09：專用合約
- 原 Parent：TPM 使用 BMAD 引導和主動 Help／教練式探索
- 子要求：TPM 使用 BMAD 引導和主動 Help；來源 `SRC-L-041`、原 clause SHA `11cc6bfc4d7bee6b8d59afe5c40e5562fa45387e491d00af72056324a1745752`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Help根據目前缺口給具體下一步`。
- **NEG / FirstFail**：將結果變為 `固定每輪重貼全部治理`，原 Reader 必回 `DOMAIN_U09_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U09.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9c8611a4acadcf5a6e6c"></a>
### CHILD-U09.2｜U09：專用合約
- 原 Parent：TPM 使用 BMAD 引導和主動 Help／教練式探索
- 子要求：教練式探索 (L5512)；來源 `SRC-L-041`、原 clause SHA `9ca0abf882d9b395ef40d73af4e52a5b449b7881f37d3e5fcadb3fb80d7adc77`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`教練式探索把假設與事實分開`。
- **NEG / FirstFail**：將結果變為 `用猜測填Owner決議`，原 Reader 必回 `DOMAIN_U09_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U09.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-7fa19dc7e888f1a78838"></a>
### CHILD-U10.1｜U10：專用合約
- 原 Parent：TPM 使用 Matt Grilling/Domain Modeling/Spec/Tickets 分工
- 子要求：TPM 使用 Matt Grilling；來源 `SRC-L-041`、原 clause SHA `e007c72b7e526a824632ee0b037efc504b51e966253bd980e6bb84d59a89ace1`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Matt方法以已知資料跳過重問`。
- **NEG / FirstFail**：將結果變為 `把方法字串當已調用`，原 Reader 必回 `DOMAIN_U10_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U10.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-21ad3a8edd55dc00d6ba"></a>
### CHILD-U10.2｜U10：專用合約
- 原 Parent：TPM 使用 Matt Grilling/Domain Modeling/Spec/Tickets 分工
- 子要求：Domain Modeling；來源 `SRC-L-041`、原 clause SHA `6d22648a8231c0129edbb4c18679bb277c6d4bfd453853f27adc52b1fcc1f837`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Domain Modeling產領域界線`。
- **NEG / FirstFail**：將結果變為 `混合Product與Runtime Writer`，原 Reader 必回 `DOMAIN_U10_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U10.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-8e77a2fba1a3726d63dd"></a>
### CHILD-U10.3｜U10：專用合約
- 原 Parent：TPM 使用 Matt Grilling/Domain Modeling/Spec/Tickets 分工
- 子要求：Spec；來源 `SRC-L-041`、原 clause SHA `cfbd39d8c3b9801b526ea8ca25526cf4c604cbd938b27d1db8a061878d1fb5cf`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Spec有ACC/NEG與來源`。
- **NEG / FirstFail**：將結果變為 `只有需求標題`，原 Reader 必回 `DOMAIN_U10_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U10.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-58151e41c8221c2053e3"></a>
### CHILD-U10.4｜U10：專用合約
- 原 Parent：TPM 使用 Matt Grilling/Domain Modeling/Spec/Tickets 分工
- 子要求：Tickets 分工 (L5513)；來源 `SRC-L-041`、原 clause SHA `9d708b59ba782225a5cd59292341810389b9c537295ff127e99f36fbc9dc936e`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Ticket連結DAG/Owner/DoD`。
- **NEG / FirstFail**：將結果變為 `無Consumer任務進READY`，原 Reader 必回 `DOMAIN_U10_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U10.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b80f12b3b4aeacc35b02"></a>
### CHILD-U11.1｜U11：專用合約
- 原 Parent：TPM 保留來源／Assumptions／Decision Ledger
- 子要求：TPM 保留來源；來源 `SRC-L-041`、原 clause SHA `3be544db4512584b65248a5909947b5f8b1220a22af8678200d3e4bc12032184`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`每規範claim回到原source SHA/line`。
- **NEG / FirstFail**：將結果變為 `無來源宣稱canonical`，原 Reader 必回 `DOMAIN_U11_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U11.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-27e9a1b3d105c9b4746e"></a>
### CHILD-U11.2｜U11：專用合約
- 原 Parent：TPM 保留來源／Assumptions／Decision Ledger
- 子要求：Assumptions；來源 `SRC-L-041`、原 clause SHA `6936a2a2f77f741a87c654661740f5ac0908a1a7d10e915e93b04260779765df`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Assumption有待驗狀態與owner`。
- **NEG / FirstFail**：將結果變為 `假設冒原Owner已決`，原 Reader 必回 `DOMAIN_U11_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U11.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-f1dfabf141275d25dfd0"></a>
### CHILD-U11.3｜U11：專用合約
- 原 Parent：TPM 保留來源／Assumptions／Decision Ledger
- 子要求：Decision Ledger (L5514)；來源 `SRC-L-041`、原 clause SHA `7fdad79d32cb2b495f613a756b037237c0f9b09f906e488b1002a5d38959e3b8`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Decision保留原處置與變更理由`。
- **NEG / FirstFail**：將結果變為 `REJECT被默改SELECTED`，原 Reader 必回 `DOMAIN_U11_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U11.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-204264d22d5d598b63f9"></a>
### CHILD-U12.1｜U12：專用合約
- 原 Parent：TPM 實際編譯相容 PIPD PI 規格包
- 子要求：TPM 實際編譯相容 PIPD PI 規格包 (L5515)；來源 `SRC-L-041`、原 clause SHA `822ff39f3938cccf52c7157ccf7e052bde7598de7c03daa1594de564296f7b82`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`原PI Writer以strict input編譯並ACK相同語義與trace`。
- **NEG / FirstFail**：將結果變為 `TPM候選自稱canonical PI`，原 Reader 必回 `DOMAIN_U12_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U12.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-e52543c8192d85c666cc"></a>
### CHILD-U13.1｜U13：專用合約
- 原 Parent：TPM 實際編譯 PD 環境／施工準備包
- 子要求：TPM 實際編譯 PD 環境；來源 `SRC-L-041`、原 clause SHA `d5540dc32471d48a8170af2319211be925607b22a368e39e4e8440b8076a95d4`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PD Binder從真root/HEAD讀回RepoContext`。
- **NEG / FirstFail**：將結果變為 `呼叫者自填HEAD當事實`，原 Reader 必回 `DOMAIN_U13_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U13.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-980f093b494b39361359"></a>
### CHILD-U13.2｜U13：專用合約
- 原 Parent：TPM 實際編譯 PD 環境／施工準備包
- 子要求：施工準備包 (L5516)；來源 `SRC-L-041`、原 clause SHA `2ad87ef5a5baa104a60992997f187fa805099d1dbdf82e76f7d04bc3cd001dda`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`施工準備含scope/preimage/tests/rollback`。
- **NEG / FirstFail**：將結果變為 `PD候選當permission`，原 Reader 必回 `DOMAIN_U13_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U13.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d891625168e549bb1b7e"></a>
### CHILD-U14.1｜U14：專用合約
- 原 Parent：TPM 具名對應 OPS ECP、DEV ECP 分別
- 子要求：TPM 具名；來源 `SRC-L-041`、原 clause SHA `becd6b34cbea0dfeaec6a32aace5aa04734474a6b292d4734b0d2397c437f55d`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`每effect具名指向一個適用ECP`。
- **NEG / FirstFail**：將結果變為 `泛稱ONE ECP而混兩權限`，原 Reader 必回 `DOMAIN_U14_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U14.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b52354695e14a7077523"></a>
### CHILD-U14.2｜U14：專用合約
- 原 Parent：TPM 具名對應 OPS ECP、DEV ECP 分別
- 子要求：OPS ECP；來源 `SRC-L-041`、原 clause SHA `f9af56f999a1a03ce4f915659e8a517327423435788e79e5acd5c17e2c33a7f3`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Host/User/Remote用各OPS scope與原Issuer`。
- **NEG / FirstFail**：將結果變為 `DEV grant拿去Host install`，原 Reader 必回 `DOMAIN_U14_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U14.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-86fc5983ad9a9490e309"></a>
### CHILD-U14.3｜U14：專用合約
- 原 Parent：TPM 具名對應 OPS ECP、DEV ECP 分別
- 子要求：DEV ECP；來源 `SRC-L-041`、原 clause SHA `24cc590cfcafa4ae4ed26c69f6183fe791539cb40f5d851bb0c78627f0c2b09f`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Repo patch只在DEV exact WriteSet`。
- **NEG / FirstFail**：將結果變為 `用OPS grant寫任意Repo`，原 Reader 必回 `DOMAIN_U14_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U14.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-33ae14b43325a895bb44"></a>
### CHILD-U14.4｜U14：專用合約
- 原 Parent：TPM 具名對應 OPS ECP、DEV ECP 分別
- 子要求：(L5517)；來源 `SRC-L-041`、原 clause SHA `b21dc46eb1eed066a8cc941b75a4aa43cfdb76bfbc1ef5d2da79e19fd6d6f65d`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`OPS與DEV分開且同subject無失真`。
- **NEG / FirstFail**：將結果變為 `省略ECP分流負例`，原 Reader 必回 `DOMAIN_U14_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U14.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9329035f697a3d7c4d4d"></a>
### CHILD-U15.1｜U15：專用合約
- 原 Parent：TPM 具名 TQAEP 測試／驗收／Evidence 包
- 子要求：TPM 具名 TQAEP 測試；來源 `SRC-L-041`、原 clause SHA `9a57a7492209d00209c951ac46c16602916b55359636ca65593a17010afb34c4`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`TQAEP每原子有POS/NEG/Oracle`。
- **NEG / FirstFail**：將結果變為 `以全包一次PASS代逐原子`，原 Reader 必回 `DOMAIN_U15_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U15.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-953c05ca5a042a5a0b36"></a>
### CHILD-U15.2｜U15：專用合約
- 原 Parent：TPM 具名 TQAEP 測試／驗收／Evidence 包
- 子要求：驗收；來源 `SRC-L-041`、原 clause SHA `96bf0c49311d184ca077b661fb8ba9e9fd7a576ece99b7aaf068f5a40df5722d`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`真Checker不同credential執行`。
- **NEG / FirstFail**：將結果變為 `Maker自簽PASS`，原 Reader 必回 `DOMAIN_U15_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U15.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-f96400528ebbb7a11ae0"></a>
### CHILD-U15.3｜U15：專用合約
- 原 Parent：TPM 具名 TQAEP 測試／驗收／Evidence 包
- 子要求：Evidence 包 (L5518)；來源 `SRC-L-041`、原 clause SHA `78775e062c2d567de181450109c7bedc4a3ff7f770345b60036ddf821c4b8726`；原 Owner `TPM_PRODUCT_PIPD_OWNER / DOC-01`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Evidence expectation與actual raw分離`。
- **NEG / FirstFail**：將結果變為 `BIND_FROM_NATIVE文字當Raw`，原 Reader 必回 `DOMAIN_U15_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U15.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-40df973384dd4cc74f88"></a>
### CHILD-U16.1｜U16：專用合約
- 原 Parent：Commander 是獨立會話、不能改 Target Repo
- 子要求：Commander 是獨立會話；來源 `SRC-L-041`、原 clause SHA `91267a3855ae693a83343d92ad712d639323f88845aaf3f4e87ff4c6cefba4e0`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Commander session與Maker執行會話分開`。
- **NEG / FirstFail**：將結果變為 `同會話冒獨立Commander`，原 Reader 必回 `DOMAIN_U16_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U16.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-fca3edc75692e176dd0c"></a>
### CHILD-U16.2｜U16：專用合約
- 原 Parent：Commander 是獨立會話、不能改 Target Repo
- 子要求：不能改 Target Repo (L5519)；來源 `SRC-L-041`、原 clause SHA `3af03c219f0b8e29ac8d01483fa4d937e8512b01972201dae20488467c91f5b0`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Commander讀Target Repo無mutation`。
- **NEG / FirstFail**：將結果變為 `Guide直接apply repo patch`，原 Reader 必回 `DOMAIN_U16_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U16.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a763dcc71bfd2acda1c5"></a>
### CHILD-U17.1｜U17：專用合約
- 原 Parent：Commander 完整理解凍結 PI/PD／ECP／TQAEP
- 子要求：Commander 完整理解凍結 PI；來源 `SRC-L-041`、原 clause SHA `72687e1b9572104b626cce2c4e7e02b4fdc1e77408f24d31730e243d4c6462eb`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`凍結PI的全原子與hash被Reader核對`。
- **NEG / FirstFail**：將結果變為 `只讀PI摘要`，原 Reader 必回 `DOMAIN_U17_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U17.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-201adb0b1e443c62b3a3"></a>
### CHILD-U17.2｜U17：專用合約
- 原 Parent：Commander 完整理解凍結 PI/PD／ECP／TQAEP
- 子要求：PD；來源 `SRC-L-041`、原 clause SHA `d4a2a068ed875a92670084bc952c397aed19271004f2d443087eeaa664f0fa4c`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PD currentness與scope實讀`。
- **NEG / FirstFail**：將結果變為 `借舊RepoContext`，原 Reader 必回 `DOMAIN_U17_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U17.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-95b28bbd6066c7952fba"></a>
### CHILD-U17.3｜U17：專用合約
- 原 Parent：Commander 完整理解凍結 PI/PD／ECP／TQAEP
- 子要求：ECP；來源 `SRC-L-041`、原 clause SHA `0e4c37a935e1e2bcdaa18dc26885bf4b656ca92cbe292a3b882fb8483b209b98`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`DEV/OPS ECP按effect分路理解`。
- **NEG / FirstFail**：將結果變為 `把ECP等同Permit`，原 Reader 必回 `DOMAIN_U17_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U17.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-ecb478f318f38eb26312"></a>
### CHILD-U17.4｜U17：專用合約
- 原 Parent：Commander 完整理解凍結 PI/PD／ECP／TQAEP
- 子要求：TQAEP (L5520)；來源 `SRC-L-041`、原 clause SHA `4f589f535d0e11f8e1b7b44a3b4580442375960c356956282a1258c8b5107404`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`TQAEP Oracle/Raw/Checker界線保留`。
- **NEG / FirstFail**：將結果變為 `expected fixture當actual verdict`，原 Reader 必回 `DOMAIN_U17_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U17.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9db39721e929812f8946"></a>
### CHILD-U18.1｜U18：專用合約
- 原 Parent：Commander 使用既有 C0–C9 Compiler，非第二 Compiler
- 子要求：Commander 使用既有 C0–C9 Compiler；來源 `SRC-L-041`、原 clause SHA `0213ac9014d35341cd518522c2a541d87a77d8594b740e24871e78e269dff1d2`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`原C0-C9 Compiler路線可識別`。
- **NEG / FirstFail**：將結果變為 `Guide自行代編formal包`，原 Reader 必回 `DOMAIN_U18_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U18.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-ed65a4d40797f531e970"></a>
### CHILD-U18.2｜U18：專用合約
- 原 Parent：Commander 使用既有 C0–C9 Compiler，非第二 Compiler
- 子要求：非第二 Compiler (L5521)；來源 `SRC-L-041`、原 clause SHA `c357da06d4df2310ef2fddf25ecbdf53f05217ee4c1372d0780f48832099841c`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`單一Canonical PIPD Writer不變`。
- **NEG / FirstFail**：將結果變為 `另建並行Compiler`，原 Reader 必回 `DOMAIN_U18_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U18.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-83f6aae59c42859e0a03"></a>
### CHILD-U19.1｜U19：專用合約
- 原 Parent：Commander 產生可貼入本地 Hermes 的「薄 Prompt」
- 子要求：Commander 產生可貼入本地 Hermes 的「薄 Prompt」 (L5522)；來源 `SRC-L-041`、原 clause SHA `90ecefac93b4464b10222d0688de999d7fdcd94923a1f94477f1ef4f215e993a`；原 Owner `CAPC_COMMANDER_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`薄Prompt只帶subject/source/ref與下一合法步驟`。
- **NEG / FirstFail**：將結果變為 `長Prompt混入自造許可`，原 Reader 必回 `DOMAIN_U19_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U19.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-25a589737f9ca0a71643"></a>
### CHILD-U20.1｜U20：專用合約
- 原 Parent：HGK 複查 PD03 RepoContext／PD04 WorkOrder／ONE ECP／ExecutionBinding
- 子要求：HGK 複查 PD03 RepoContext；來源 `SRC-L-041`、原 clause SHA `0a4c4b96db590df090efe36605ae60172017f8b9fc59f7dac7bd1e176d9bfee2`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PD03 root/HEAD/index/untracked重新核對`。
- **NEG / FirstFail**：將結果變為 `只信歷史README`，原 Reader 必回 `DOMAIN_U20_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U20.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-2d3243c945c8ad530ca6"></a>
### CHILD-U20.2｜U20：專用合約
- 原 Parent：HGK 複查 PD03 RepoContext／PD04 WorkOrder／ONE ECP／ExecutionBinding
- 子要求：PD04 WorkOrder；來源 `SRC-L-041`、原 clause SHA `8551573776c8a464754f7dd20bf7a9115ac3d5e4aa148888e94d52adb126dde1`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PD04 WO在真Receiver得到ACK`。
- **NEG / FirstFail**：將結果變為 `candidate直接enqueue`，原 Reader 必回 `DOMAIN_U20_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U20.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-7131626e40d0444cc609"></a>
### CHILD-U20.3｜U20：專用合約
- 原 Parent：HGK 複查 PD03 RepoContext／PD04 WorkOrder／ONE ECP／ExecutionBinding
- 子要求：ONE ECP；來源 `SRC-L-041`、原 clause SHA `6890b7c82190c1411acc3b8f630dbef8d7b6976dd911d84fbd742b1eceb21762`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`每次效果選唯一適用ECP`。
- **NEG / FirstFail**：將結果變為 `同effect混DEV和OPS`，原 Reader 必回 `DOMAIN_U20_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U20.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-eb214ad952e5fc0ea184"></a>
### CHILD-U20.4｜U20：專用合約
- 原 Parent：HGK 複查 PD03 RepoContext／PD04 WorkOrder／ONE ECP／ExecutionBinding
- 子要求：ExecutionBinding (L5523)；來源 `SRC-L-041`、原 clause SHA `49107bf4dda28acf759a04db973fea4e6f696fd93d492acbb1e6d62d7c03f365`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`ExecutionBinding同lease/nonce/epoch/scope`。
- **NEG / FirstFail**：將結果變為 `借別WorkID binding`，原 Reader 必回 `DOMAIN_U20_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U20.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-afa5c8e2a22d00e0102f"></a>
### CHILD-U21.1｜U21：專用合約
- 原 Parent：HGK TPM Profile 接收 PIPD並複用既有 Document/Intake 工程能力
- 子要求：HGK TPM Profile 接收 PIPD並複用既有 Document；來源 `SRC-L-041`、原 clause SHA `955a9abb4f53959798ef41e4f23e7562d8dff692319f99d5d9d02fbb190efe99`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`HGK TPM使用既有Document能力讀PIPD`。
- **NEG / FirstFail**：將結果變為 `新增第二文件canonical store`，原 Reader 必回 `DOMAIN_U21_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U21.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-fc9bf637fdace7a4cfc3"></a>
### CHILD-U21.2｜U21：專用合約
- 原 Parent：HGK TPM Profile 接收 PIPD並複用既有 Document/Intake 工程能力
- 子要求：Intake 工程能力 (L5524)；來源 `SRC-L-041`、原 clause SHA `a9fb2a6856670bb2d37c1a49f398417b903421c230ce78cfed3b9a1a890fd9de`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`既有Intake保持source/authority guard`。
- **NEG / FirstFail**：將結果變為 `跳Intake直接effect`，原 Reader 必回 `DOMAIN_U21_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U21.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-c3cad83934448cbb03a9"></a>
### CHILD-U22.1｜U22：專用合約
- 原 Parent：HGK Commander Profile 接收 Prompt/Handoff並控制任務路由
- 子要求：HGK Commander Profile 接收 Prompt；來源 `SRC-L-041`、原 clause SHA `33a91e0e3b0a7ded3d33de8cd385eb45c61742597cac481ec559454f37afa62c`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`HGK Commander讀薄Prompt引用並驗hash`。
- **NEG / FirstFail**：將結果變為 `把Prompt字串當signed WO`，原 Reader 必回 `DOMAIN_U22_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U22.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-2f661c19644e74d93705"></a>
### CHILD-U22.2｜U22：專用合約
- 原 Parent：HGK Commander Profile 接收 Prompt/Handoff並控制任務路由
- 子要求：Handoff並控制任務路由 (L5525)；來源 `SRC-L-041`、原 clause SHA `13e26b215d782c58583a4c4ed232342a6cd4e9f1ac6b7d48075c8441db4413ef`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Handoff走原route/PLAN CAS`。
- **NEG / FirstFail**：將結果變為 `Guide建立第二queue`，原 Reader 必回 `DOMAIN_U22_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U22.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-0de3c195c6ae973c90e8"></a>
### CHILD-U23.1｜U23：專用合約
- 原 Parent：HGK Challenge/AO Profile 接收 Finding＋本地 Local Verification
- 子要求：HGK Challenge；來源 `SRC-L-041`、原 clause SHA `911e88549274e4d7fd4edd33e2933401dfab4cf8e707f66080ef13e934260fe8`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Challenge只產source-bound advisory Finding`。
- **NEG / FirstFail**：將結果變為 `Challenge自頒Permit`，原 Reader 必回 `DOMAIN_U23_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U23.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-3ccf4e531bfb5fb73cb4"></a>
### CHILD-U23.2｜U23：專用合約
- 原 Parent：HGK Challenge/AO Profile 接收 Finding＋本地 Local Verification
- 子要求：AO Profile 接收 Finding＋本地 Local Verification (L5526)；來源 `SRC-L-041`、原 clause SHA `5ebe9addfd7b980f0c707120c491edf11aa314321a0f0ceed3ed22d89da721f7`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`AO原Receiver讀Finding並由本地真Checker驗`。
- **NEG / FirstFail**：將結果變為 `advisory直接升protected PASS`，原 Reader 必回 `DOMAIN_U23_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U23.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d14751f1d30a08131c90"></a>
### CHILD-U24.1｜U24：專用合約
- 原 Parent：HGK 呼叫 Fabric 所治理的既有 FAR/FDA，非另建
- 子要求：HGK 呼叫 Fabric 所治理的既有 FAR；來源 `SRC-L-041`、原 clause SHA `781b6e6a02dab2c37d8b5f077931fd3723af148c3ad067b7d2c835664db217fc`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`FAR走Fabric原治理route與budget`。
- **NEG / FirstFail**：將結果變為 `啟動未准入第二研究控制器`，原 Reader 必回 `DOMAIN_U24_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U24.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-bd1d033a34b1250c27c6"></a>
### CHILD-U24.2｜U24：專用合約
- 原 Parent：HGK 呼叫 Fabric 所治理的既有 FAR/FDA，非另建
- 子要求：FDA；來源 `SRC-L-041`、原 clause SHA `4e1b724753d40db8a007a8693d23172b9c005cc464cd3402a90fc3bc08946708`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`FDA走原Effect Admission`。
- **NEG / FirstFail**：將結果變為 `GUI動作繞過OPS scope`，原 Reader 必回 `DOMAIN_U24_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U24.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-4b8b441e36456b6b62c7"></a>
### CHILD-U24.3｜U24：專用合約
- 原 Parent：HGK 呼叫 Fabric 所治理的既有 FAR/FDA，非另建
- 子要求：非另建 (L5527)；來源 `SRC-L-041`、原 clause SHA `a27aea308927e0129f39930e852dbfad7927d69d7e86046f9b0f7f6a8bb585a6`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`既有FAR/FDA Owner不被adapter取代`。
- **NEG / FirstFail**：將結果變為 `供應商SDK冒Issuer`，原 Reader 必回 `DOMAIN_U24_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U24.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b1317a00935814f61151"></a>
### CHILD-U25.1｜U25：專用合約
- 原 Parent：HGK 合法受限施工、Build、Test、Repair、Checkpoint
- 子要求：HGK 合法受限施工；來源 `SRC-L-041`、原 clause SHA `d5c6f195fdbccd696fade95cf12d490998d81d74d5713589b88bf00f54301f1f`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`施工只在受權scope且原Issuer有效`。
- **NEG / FirstFail**：將結果變為 `跨root mutation`，原 Reader 必回 `DOMAIN_U25_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U25.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a1afc7441407c000584e"></a>
### CHILD-U25.2｜U25：專用合約
- 原 Parent：HGK 合法受限施工、Build、Test、Repair、Checkpoint
- 子要求：Build；來源 `SRC-L-041`、原 clause SHA `a6f504a78e0674bce72e69772a88a10b0e2cecc2eef9d3703c625ed1c8328747`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Build保存input/output/exit並在隔離scope`。
- **NEG / FirstFail**：將結果變為 `PREW3只讀域寫wheel`，原 Reader 必回 `DOMAIN_U25_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U25.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-4ce430d7841caccfccc2"></a>
### CHILD-U25.3｜U25：專用合約
- 原 Parent：HGK 合法受限施工、Build、Test、Repair、Checkpoint
- 子要求：Test；來源 `SRC-L-041`、原 clause SHA `7b981864921ac064f9b25095ef2bcefb4be3621db727a9052c091eb7c9297f57`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Test逐case保存actual Raw`。
- **NEG / FirstFail**：將結果變為 `只列test ID當執行`，原 Reader 必回 `DOMAIN_U25_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U25.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-080c160e6ce2636852c5"></a>
### CHILD-U25.4｜U25：專用合約
- 原 Parent：HGK 合法受限施工、Build、Test、Repair、Checkpoint
- 子要求：Repair；來源 `SRC-L-041`、原 clause SHA `1e3735e047a52d2ca4af41cf00f2aaaa704b691f0cf9ec29c40a39b0888ea8a6`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Repair遵first_fail最小錐與原Oracle`。
- **NEG / FirstFail**：將結果變為 `改Oracle門檻求綠`，原 Reader 必回 `DOMAIN_U25_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U25.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b03812f91d626bf3bbb4"></a>
### CHILD-U25.5｜U25：專用合約
- 原 Parent：HGK 合法受限施工、Build、Test、Repair、Checkpoint
- 子要求：Checkpoint (L5528)；來源 `SRC-L-041`、原 clause SHA `afcf7dbc82f85bfdee697b5c8a40ea2c34b3f6b4b3959265b1ffa1fee43791f8`；原 Owner `HGK_FABRIC_OWNER / DOC-04`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Checkpoint包含operation/cursor/residue可resume`。
- **NEG / FirstFail**：將結果變為 `unknown effect刪journal重試`，原 Reader 必回 `DOMAIN_U25_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U25.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-7a269b3012d932789e6d"></a>
### CHILD-U26.1｜U26：專用合約
- 原 Parent：施工到 GitHub 的 Source Candidate exact SHA
- 子要求：施工到 GitHub 的 Source Candidate exact SHA (L5529)；來源 `SRC-L-041`、原 clause SHA `105df367a0f291cfc113de9ea8469fc69e73739ee20d49f8e9aab76b3c33167e`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`遠端Source Candidate exact commit SHA真讀回`。
- **NEG / FirstFail**：將結果變為 `本地工作樹hash冒遠端commit`，原 Reader 必回 `DOMAIN_U26_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U26.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-270a36e001a872f62421"></a>
### CHILD-U27.1｜U27：專用合約
- 原 Parent：Evidence Commit exact SHA 必須與 Source SHA 分開
- 子要求：Evidence Commit exact SHA 必須；來源 `SRC-L-041`、原 clause SHA `76daa90d33d4c50c336c69a8db4153855d1737c3b9648207223d147d41adabb3`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Evidence Commit單獨immutable commit SHA`。
- **NEG / FirstFail**：將結果變為 `把log路徑當commit SHA`，原 Reader 必回 `DOMAIN_U27_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U27.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-3c4ffcd0774325f54292"></a>
### CHILD-U27.2｜U27：專用合約
- 原 Parent：Evidence Commit exact SHA 必須與 Source SHA 分開
- 子要求：Source SHA 分開 (L5530)；來源 `SRC-L-041`、原 clause SHA `f41edcdd5f3d611789f68fb1ce9a161067a0de19fbe3ca67c1b945ede538be6c`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Source/Evidence SHA不同物件角色且trace相連`。
- **NEG / FirstFail**：將結果變為 `將兩SHA互換`，原 Reader 必回 `DOMAIN_U27_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U27.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d2d06a051c7556610e3c"></a>
### CHILD-U28.1｜U28：專用合約
- 原 Parent：External Challenge 是另一新對話與唯讀 Frozen Readset
- 子要求：External Challenge 是另一新對話；來源 `SRC-L-041`、原 clause SHA `3fbc6987f1befa2f63c041840324b589f927f1d2bcf0d0e7677593ec551e9375`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Challenge新會話對固定candidate/evidence hash`。
- **NEG / FirstFail**：將結果變為 `moving branch被當frozen`，原 Reader 必回 `DOMAIN_U28_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U28.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-1635db4c027c835b7224"></a>
### CHILD-U28.2｜U28：專用合約
- 原 Parent：External Challenge 是另一新對話與唯讀 Frozen Readset
- 子要求：唯讀 Frozen Readset (L5531)；來源 `SRC-L-041`、原 clause SHA `8d3832e36621cb72c179f9fccc22edf440f03ba3d34ed98e145a6377af8e68aa`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Frozen Readset只讀且hash重算不變`。
- **NEG / FirstFail**：將結果變為 `Reviewer修改subject後出PASS`，原 Reader 必回 `DOMAIN_U28_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U28.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-debabc369b5d95dbb7d2"></a>
### CHILD-U29.1｜U29：專用合約
- 原 Parent：External Challenge 逐條對照 PI/PD requirements/oracles/evidence
- 子要求：External Challenge 逐條對照 PI；來源 `SRC-L-041`、原 clause SHA `b382c48212a77f7a5bcd159eb21b023daa9ac082176e1cb0a03214ff0154ca9d`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`逐PI atom與原source對照`。
- **NEG / FirstFail**：將結果變為 `只對總表數量`，原 Reader 必回 `DOMAIN_U29_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U29.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d31d22bc8ad069ca7f8c"></a>
### CHILD-U29.2｜U29：專用合約
- 原 Parent：External Challenge 逐條對照 PI/PD requirements/oracles/evidence
- 子要求：PD requirements；來源 `SRC-L-041`、原 clause SHA `d760af64a69777be55d66331f4ca8348aabbb57a920ef266e631bda094d14a84`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`逐PD scope/currentness對照`。
- **NEG / FirstFail**：將結果變為 `過期HEAD照收`，原 Reader 必回 `DOMAIN_U29_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U29.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-460d4ea48dfcce9c471f"></a>
### CHILD-U29.3｜U29：專用合約
- 原 Parent：External Challenge 逐條對照 PI/PD requirements/oracles/evidence
- 子要求：oracles；來源 `SRC-L-041`、原 clause SHA `7b18473d4d79047ec3172cdcccf5d730c94688271ca40b66363f74797a0a0ee5`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`每Oracle版本與predicate校驗`。
- **NEG / FirstFail**：將結果變為 `以相似Oracle互借`，原 Reader 必回 `DOMAIN_U29_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U29.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9d7a69389c9ec33e5c62"></a>
### CHILD-U29.4｜U29：專用合約
- 原 Parent：External Challenge 逐條對照 PI/PD requirements/oracles/evidence
- 子要求：evidence (L5532)；來源 `SRC-L-041`、原 clause SHA `8c67f54037b7e657967de0e3a454153f394a2de08422f5b59c5f1fc8db1b5b78`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`每raw同candidate可重算且獨立身份`。
- **NEG / FirstFail**：將結果變為 `foreign host raw替代`，原 Reader 必回 `DOMAIN_U29_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U29.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d83fc4ee768ab398d6b6"></a>
### CHILD-U30.1｜U30：專用合約
- 原 Parent：Challenge 產出正式相容的 Review Finding／報告
- 子要求：Challenge 產出正式相容的 Review Finding；來源 `SRC-L-041`、原 clause SHA `319cd3eed4074d3d9ecf34dd4425b88c147c1cac01497a6b25d15d2bb9a19f83`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Finding含command/exit/raw SHA/重現`。
- **NEG / FirstFail**：將結果變為 `未重現猜測當confirmed defect`，原 Reader 必回 `DOMAIN_U30_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U30.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9fc79ea7e971fe95edd5"></a>
### CHILD-U30.2｜U30：專用合約
- 原 Parent：Challenge 產出正式相容的 Review Finding／報告
- 子要求：報告 (L5533)；來源 `SRC-L-041`、原 clause SHA `09cef62504c7ffbebaf73d866951939e666337095bc9ee231a6a4ddbfea3d1cf`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`報告列scope/not_covered/claim ceiling`。
- **NEG / FirstFail**：將結果變為 `自封Production PASS`，原 Reader 必回 `DOMAIN_U30_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U30.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-65545d82faed9c45bbde"></a>
### CHILD-U31.1｜U31：專用合約
- 原 Parent：Commander 接 Evidence + Findings，計算最小修補錐
- 子要求：Commander 接 Evidence；來源 `SRC-L-041`、原 clause SHA `95cfb0114725f8eff98e22e314f2ac35e01c19f2da614f34134ef3fb9955ec83`；原 Owner `CAPC_COMMANDER_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Evidence讀raw/hash/owner`。
- **NEG / FirstFail**：將結果變為 `讀摘要代理raw`，原 Reader 必回 `DOMAIN_U31_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U31.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-50385abd37e77828c958"></a>
### CHILD-U31.2｜U31：專用合約
- 原 Parent：Commander 接 Evidence + Findings，計算最小修補錐
- 子要求：Findings；來源 `SRC-L-041`、原 clause SHA `67d591bb168bea5edac1d61f600c46305a653304762a8febc02311f64af63783`；原 Owner `CAPC_COMMANDER_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Finding帶first_fail和受影consumer`。
- **NEG / FirstFail**：將結果變為 `無定位就全包重寫`，原 Reader 必回 `DOMAIN_U31_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U31.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-8623c1437c18ef5a29a4"></a>
### CHILD-U31.3｜U31：專用合約
- 原 Parent：Commander 接 Evidence + Findings，計算最小修補錐
- 子要求：計算最小修補錐 (L5534)；來源 `SRC-L-041`、原 clause SHA `e3a1908ef5aa96a56ccdeef8949a9de92b30d3011409a68552d93df2fad2ed5a`；原 Owner `CAPC_COMMANDER_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`最小RepairCone只包含受影依賴`。
- **NEG / FirstFail**：將結果變為 `未受影READY也PARK`，原 Reader 必回 `DOMAIN_U31_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U31.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d5d6c13ea3e1304b2042"></a>
### CHILD-U32.1｜U32：專用合約
- 原 Parent：修補生成新 Candidate／Evidence，不覆蓋前版
- 子要求：修補生成新 Candidate；來源 `SRC-L-041`、原 clause SHA `da18c197a438bf41979844bafba7614855ee20af8018ae7bf98d4893965a5ae9`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`新Candidate明示supersedes且新SHA`。
- **NEG / FirstFail**：將結果變為 `直接覆蓋舊candidate`，原 Reader 必回 `DOMAIN_U32_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U32.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-8e613c0613eaf4b66cac"></a>
### CHILD-U32.2｜U32：專用合約
- 原 Parent：修補生成新 Candidate／Evidence，不覆蓋前版
- 子要求：Evidence；來源 `SRC-L-041`、原 clause SHA `5ed8b188963f372694ffcb8abffa782ab2861eb854aab07b71020452b9eb50eb`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`新Evidence指向新candidate與原test`。
- **NEG / FirstFail**：將結果變為 `借前輪Raw`，原 Reader 必回 `DOMAIN_U32_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U32.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-4bc44c57f12185decb4c"></a>
### CHILD-U32.3｜U32：專用合約
- 原 Parent：修補生成新 Candidate／Evidence，不覆蓋前版
- 子要求：不覆蓋前版 (L5535)；來源 `SRC-L-041`、原 clause SHA `79dee2d855f65de23f8fdc804425e8f4d3d879d85f11dba096c5498c67766797`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`舊版候選與證據保持immutable`。
- **NEG / FirstFail**：將結果變為 `清理舊失敗Raw`，原 Reader 必回 `DOMAIN_U32_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U32.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-96b6a5c2f17284b4f9a3"></a>
### CHILD-U33.1｜U33：專用合約
- 原 Parent：外部 Challenge 按高必要性／低 CP 值建議停止
- 子要求：外部 Challenge 按高必要性；來源 `SRC-L-041`、原 clause SHA `9ffb393e01c76ad9b45861411fa2247019cfe028b2fcaf08663eaeaadb8dee77`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`高必要性缺陷仍有明確修補需求`。
- **NEG / FirstFail**：將結果變為 `忽略P0因成本高`，原 Reader 必回 `DOMAIN_U33_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U33.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-3bbd5593f1afaa7adcb7"></a>
### CHILD-U33.2｜U33：專用合約
- 原 Parent：外部 Challenge 按高必要性／低 CP 值建議停止
- 子要求：低 CP 值建議停止 (L5536)；來源 `SRC-L-041`、原 clause SHA `3ffc568ae25f892442c46d8e57683cb1b2fbfebecdd6f68c2453a0e384796880`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`低CP延伸由原Owner決定停損`。
- **NEG / FirstFail**：將結果變為 `Reviewer自行擴大無界研究`，原 Reader 必回 `DOMAIN_U33_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U33.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-44c7c3eeadfd2fbf49a3"></a>
### CHILD-U34.1｜U34：專用合約
- 原 Parent：正式 Owner/Human 決定結案，不由 Challenge 自許可
- 子要求：正式 Owner；來源 `SRC-L-041`、原 clause SHA `c5272a4da78b6151d4fe1b9bf5b36168bcfd40fedb1a7561003c5debc61fdc31`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`正式Owner讀證據後裁定該scope`。
- **NEG / FirstFail**：將結果變為 `Maker替Owner批准`，原 Reader 必回 `DOMAIN_U34_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U34.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-c5348a7aa9d427c160c2"></a>
### CHILD-U34.2｜U34：專用合約
- 原 Parent：正式 Owner/Human 決定結案，不由 Challenge 自許可
- 子要求：Human 決定結案；來源 `SRC-L-041`、原 clause SHA `8d691691a40a99bc5432bacaedcbc160664f0eeb03c1e3ffdbe071544c5cf515`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Human有可review的具體結果再決定`。
- **NEG / FirstFail**：將結果變為 `只給Plan要Human簽`，原 Reader 必回 `DOMAIN_U34_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U34.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-85e3466b3444807105a3"></a>
### CHILD-U34.3｜U34：專用合約
- 原 Parent：正式 Owner/Human 決定結案，不由 Challenge 自許可
- 子要求：不由 Challenge 自許可 (L5537)；來源 `SRC-L-041`、原 clause SHA `687a494adc00e712ac8b724742ef170a33434a08aa7fb0a7eab0a226b523e32c`；原 Owner `EXTERNAL_ASSURANCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Challenge建議不能自行許可`。
- **NEG / FirstFail**：將結果變為 `advisory轉signed verdict`，原 Reader 必回 `DOMAIN_U34_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U34.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-8cc3eec431cc3f236750"></a>
### CHILD-U35.1｜U35：專用合約
- 原 Parent：內部 Loop A Fast Repair、Loop B Local Closure、Loop C External Challenge
- 子要求：內部 Loop A Fast Repair；來源 `SRC-L-041`、原 clause SHA `976506eb16774496e7b6676e37ae41dbdd62ba8b50ed6d42fb7e55aa01206e57`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Loop A bounded快修保存RedGreen`。
- **NEG / FirstFail**：將結果變為 `未repro直接廣改`，原 Reader 必回 `DOMAIN_U35_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U35.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-1e4fff674f41288a144e"></a>
### CHILD-U35.2｜U35：專用合約
- 原 Parent：內部 Loop A Fast Repair、Loop B Local Closure、Loop C External Challenge
- 子要求：Loop B Local Closure；來源 `SRC-L-041`、原 clause SHA `70b364a4692bcad7b9e18138551f08c3e99f9e32b6f2fac96d6e68f69cec8d6d`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Loop B原本地Checker獨立閉合`。
- **NEG / FirstFail**：將結果變為 `同Maker自證`，原 Reader 必回 `DOMAIN_U35_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U35.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-90d4fa5ef736220dbb6f"></a>
### CHILD-U35.3｜U35：專用合約
- 原 Parent：內部 Loop A Fast Repair、Loop B Local Closure、Loop C External Challenge
- 子要求：Loop C External Challenge (L5538)；來源 `SRC-L-041`、原 clause SHA `e7b63ca7f6014cbaba21252eb4aa3a711101e4246327a9a86657ffb68c2b07f3`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Loop C新會話frozen挑戰`。
- **NEG / FirstFail**：將結果變為 `沿用Maker session冒獨立`，原 Reader 必回 `DOMAIN_U35_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U35.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-6d6febb608cab2f9afd0"></a>
### CHILD-U36.1｜U36：專用合約
- 原 Parent：有界 self-research/review/repair/retest/iteration/evolution
- 子要求：有界 self-research；來源 `SRC-L-041`、原 clause SHA `8267b56cb6000618b78121b0daefeec931f732982ed7c6bcea3702b0ac103662`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`research有need/source/time/attempt budget`。
- **NEG / FirstFail**：將結果變為 `無界爬資料`，原 Reader 必回 `DOMAIN_U36_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U36.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-592e7c0e90f41d273f20"></a>
### CHILD-U36.2｜U36：專用合約
- 原 Parent：有界 self-research/review/repair/retest/iteration/evolution
- 子要求：review；來源 `SRC-L-041`、原 clause SHA `ded844c84cc8b878b127497c22e47406ee563696fcf66365be254ef62fed9b08`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`review讀固定SHA並留finding`。
- **NEG / FirstFail**：將結果變為 `review中改subject`，原 Reader 必回 `DOMAIN_U36_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U36.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a4c7f0c5a8e027f0df8a"></a>
### CHILD-U36.3｜U36：專用合約
- 原 Parent：有界 self-research/review/repair/retest/iteration/evolution
- 子要求：repair；來源 `SRC-L-041`、原 clause SHA `ccda3f1990f59aa9657d9c0e23dff3c38e60958ed317303fa33817641972a909`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`repair有exact write scope與preimage`。
- **NEG / FirstFail**：將結果變為 `擴scope避失敗`，原 Reader 必回 `DOMAIN_U36_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U36.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-7b86c70b02be2465089d"></a>
### CHILD-U36.4｜U36：專用合約
- 原 Parent：有界 self-research/review/repair/retest/iteration/evolution
- 子要求：retest；來源 `SRC-L-041`、原 clause SHA `54beb922b67e49bb1615d77be4b2a01dd2e885f75896219340da00db44914de6`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`retest用原Oracle與同candidate`。
- **NEG / FirstFail**：將結果變為 `改threshold`，原 Reader 必回 `DOMAIN_U36_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U36.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-6be409953151a9779f5f"></a>
### CHILD-U36.5｜U36：專用合約
- 原 Parent：有界 self-research/review/repair/retest/iteration/evolution
- 子要求：iteration；來源 `SRC-L-041`、原 clause SHA `48fdd30775252dd69e6c7a0f5bfa5079e3f58599ac7ef46e52c23f6382beada9`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`iteration保留每輪版本與budget止損；evolution候選另准入`。
- **NEG / FirstFail**：將結果變為 `循環自提升法位`，原 Reader 必回 `DOMAIN_U36_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U36.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-6451b059e2d89415b988"></a>
### CHILD-U37.1｜U37：專用合約
- 原 Parent：Dogfood 發現的失敗轉回退回歸／研究與候選，而非自改 Oracle
- 子要求：Dogfood 發現的失敗轉回退回歸；來源 `SRC-L-041`、原 clause SHA `239790948be3d7e4a39f10c583f0ed4330b10757e8cc242a2a4154d9f9830765`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`dogfood失敗加入原回歸集`。
- **NEG / FirstFail**：將結果變為 `刪舊NEG`，原 Reader 必回 `DOMAIN_U37_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U37.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-fe842c101f0da2cd59d9"></a>
### CHILD-U37.2｜U37：專用合約
- 原 Parent：Dogfood 發現的失敗轉回退回歸／研究與候選，而非自改 Oracle
- 子要求：研究；來源 `SRC-L-041`、原 clause SHA `e58e3391dd944b7633c32c8dadb90e2bcb25587c4e4df6199f9efc023ff02e78`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`研究只追first_fail受影源`。
- **NEG / FirstFail**：將結果變為 `無界補工具`，原 Reader 必回 `DOMAIN_U37_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U37.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-9e88f60c62a9f98cef56"></a>
### CHILD-U37.3｜U37：專用合約
- 原 Parent：Dogfood 發現的失敗轉回退回歸／研究與候選，而非自改 Oracle
- 子要求：候選；來源 `SRC-L-041`、原 clause SHA `dd1275de581a2f73d782d069592f9218c74439d4021e72cd53baa1cb3e1159fe`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`新演化candidate保留Owner決議`。
- **NEG / FirstFail**：將結果變為 `直接替換Active`，原 Reader 必回 `DOMAIN_U37_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U37.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-e7ac3698315a4ed5c8b9"></a>
### CHILD-U37.4｜U37：專用合約
- 原 Parent：Dogfood 發現的失敗轉回退回歸／研究與候選，而非自改 Oracle
- 子要求：而非自改 Oracle (L5540)；來源 `SRC-L-041`、原 clause SHA `7ddafb78ee2b32b5c198ad5b5a351e6b529980acab5b794a442d2ee4b8367c87`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Oracle不由Maker自行更改`。
- **NEG / FirstFail**：將結果變為 `降低threshold讓測例過`，原 Reader 必回 `DOMAIN_U37_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U37.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-5c23a431cd8850f2f008"></a>
### CHILD-U38.1｜U38：專用合約
- 原 Parent：Self Dogfood 對 SBL 自己的真實 Repo code/test/rollback
- 子要求：Self Dogfood 對 SBL 自己的真實 Repo code；來源 `SRC-L-041`、原 clause SHA `1da8bd3f7ed6ff74be053ed24da703d2924266f4bcd76be84c879085ddc39508`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Self dogfood真SBL repo code/current HEAD`。
- **NEG / FirstFail**：將結果變為 `fixture repo冒真SBL`，原 Reader 必回 `DOMAIN_U38_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U38.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-84e6d3c30a72dd8f182f"></a>
### CHILD-U38.2｜U38：專用合約
- 原 Parent：Self Dogfood 對 SBL 自己的真實 Repo code/test/rollback
- 子要求：test；來源 `SRC-L-041`、原 clause SHA `2c97e3616a55e2c88bc4af43b2e20b4422677660a969ccc2a0cb5b174cc0277f`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`真test runner exit/raw同candidate`。
- **NEG / FirstFail**：將結果變為 `README PASS冒run`，原 Reader 必回 `DOMAIN_U38_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U38.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-45483261d7568e31d297"></a>
### CHILD-U38.3｜U38：專用合約
- 原 Parent：Self Dogfood 對 SBL 自己的真實 Repo code/test/rollback
- 子要求：rollback (L5541)；來源 `SRC-L-041`、原 clause SHA `7407b0c414d4e804682f71c10b90da1f18df2fc4ef711bbce012d01de5330921`；原 Owner `EVOLUTION_EVIDENCE_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`rollback回復preimage且無越域residue`。
- **NEG / FirstFail**：將結果變為 `reset他人未追蹤變更`，原 Reader 必回 `DOMAIN_U38_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U38.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-76ddef3fa79ab781a3df"></a>
### CHILD-U39.1｜U39：專用合約
- 原 Parent：Cross Dogfood 對 SWOF 的相容工作，正式 Wave/Owner 准入
- 子要求：Cross Dogfood 對 SWOF 的相容工作；來源 `SRC-L-041`、原 clause SHA `61e16a8283f3ff76b6fa789d1ea3ccdb695ec36d597f2d3d52ce81a11893cd14`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Cross dogfood走SWOF原相容contract`。
- **NEG / FirstFail**：將結果變為 `SBL自行宣稱W3 ready`，原 Reader 必回 `DOMAIN_U39_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U39.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-99c64fafbb7b4765abbc"></a>
### CHILD-U39.2｜U39：專用合約
- 原 Parent：Cross Dogfood 對 SWOF 的相容工作，正式 Wave/Owner 准入
- 子要求：正式 Wave；來源 `SRC-L-041`、原 clause SHA `870968632645f5aa885ae65e27fc2da69b1a2c852f5e6fab4c9d338fdcce9c50`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`SWOF Wave實際Gate成立`。
- **NEG / FirstFail**：將結果變為 `W2 shadow當W3`，原 Reader 必回 `DOMAIN_U39_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U39.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-cbba0b62570c9fdf1da4"></a>
### CHILD-U39.3｜U39：專用合約
- 原 Parent：Cross Dogfood 對 SWOF 的相容工作，正式 Wave/Owner 准入
- 子要求：Owner 准入 (L5542)；來源 `SRC-L-041`、原 clause SHA `8d1a76e705099e71c5cf9eba7bccd6e051ca11c329899c885e993acb9cd7a611`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`原Owner admission指向同scope`。
- **NEG / FirstFail**：將結果變為 `借別Wave grant`，原 Reader 必回 `DOMAIN_U39_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U39.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-38824f123ad6de527e3b"></a>
### CHILD-U40.1｜U40：專用合約
- 原 Parent：SBL 與 PRE-W3 僅過渡 Shadow，不阻塞正式 PRE-W3
- 子要求：SBL；來源 `SRC-L-041`、原 clause SHA `6786b7946c5477bda29fcf5a94c461cf56b7847f02f9de3c96b0e81ae6f5285f`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`SBL保持獨立產品與SWOF過渡適配`。
- **NEG / FirstFail**：將結果變為 `SBL接管SWOF lifecycle`，原 Reader 必回 `DOMAIN_U40_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U40.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-55084f47fe98eecc9b16"></a>
### CHILD-U40.2｜U40：專用合約
- 原 Parent：SBL 與 PRE-W3 僅過渡 Shadow，不阻塞正式 PRE-W3
- 子要求：PRE-W3 僅過渡 Shadow；來源 `SRC-L-041`、原 clause SHA `7c4cfec6a175ad4ea0d0b75713dfc174f5364bd97877e68dbeb09bb0fca0f41b`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`PRE-W3只讀frozen readset且world diff0`。
- **NEG / FirstFail**：將結果變為 `Shadow發W3 packet`，原 Reader 必回 `DOMAIN_U40_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U40.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-e1d14a0c395d63b160db"></a>
### CHILD-U40.3｜U40：專用合約
- 原 Parent：SBL 與 PRE-W3 僅過渡 Shadow，不阻塞正式 PRE-W3
- 子要求：不阻塞正式 PRE-W3 (L5543)；來源 `SRC-L-041`、原 clause SHA `4eeef8770324a2c16df35bf9c6101d024c1dd7576ce348aad1f5c56f1122ca15`；原 Owner `HGK_FABRIC_OWNER / DOC-11`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`受影Shadow HOLD不阻正式PRE-W3其他READY`。
- **NEG / FirstFail**：將結果變為 `Global waterfall`，原 Reader 必回 `DOMAIN_U40_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U40.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-1b7793481a0f35dcb9fc"></a>
### CHILD-U41.1｜U41：專用合約
- 原 Parent：W3／W4／W5 的角色回流 SWOF 正式 OS Team／Profile／能力
- 子要求：W3；來源 `SRC-L-041`、原 clause SHA `5be7da97d282c365fe421424754b01ed08345246fceb85a13297b302ca4f277a`；原 Owner `HGK_FABRIC_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`W3路由回正式SWOF Owner/Gate`。
- **NEG / FirstFail**：將結果變為 `SBL proposal直接W3`，原 Reader 必回 `DOMAIN_U41_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U41.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-88d415a523a6eecba349"></a>
### CHILD-U41.2｜U41：專用合約
- 原 Parent：W3／W4／W5 的角色回流 SWOF 正式 OS Team／Profile／能力
- 子要求：W4；來源 `SRC-L-041`、原 clause SHA `e26a9ec7c0d47e5d1520f1c3cba120a04232afcb719d248899cd9074eb9be31a`；原 Owner `HGK_FABRIC_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`W4角色回正式OS Team`。
- **NEG / FirstFail**：將結果變為 `便攜SP自封W4 principal`，原 Reader 必回 `DOMAIN_U41_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U41.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-81bf7667615e65eaaa64"></a>
### CHILD-U41.3｜U41：專用合約
- 原 Parent：W3／W4／W5 的角色回流 SWOF 正式 OS Team／Profile／能力
- 子要求：W5 的角色回流 SWOF 正式 OS Team；來源 `SRC-L-041`、原 clause SHA `46779bd58995fe003136df77b756959fef46e386eecd90a369f2bedeb644e9e4`；原 Owner `HGK_FABRIC_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`W5能力延續正式Team的phase gate`。
- **NEG / FirstFail**：將結果變為 `用W3資格替W5`，原 Reader 必回 `DOMAIN_U41_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U41.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-92ebfa046e2705faf741"></a>
### CHILD-U41.4｜U41：專用合約
- 原 Parent：W3／W4／W5 的角色回流 SWOF 正式 OS Team／Profile／能力
- 子要求：Profile；來源 `SRC-L-041`、原 clause SHA `f288b642f62ee91c67a608f03dc4824661773c857d5954ec5049532459649048`；原 Owner `HGK_FABRIC_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`正式Profile version/loaded SHA真讀回`。
- **NEG / FirstFail**：將結果變為 `fixture profile充正式`，原 Reader 必回 `DOMAIN_U41_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U41.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-ac062bead3eb302c1e3e"></a>
### CHILD-U41.5｜U41：專用合約
- 原 Parent：W3／W4／W5 的角色回流 SWOF 正式 OS Team／Profile／能力
- 子要求：能力 (L5544)；來源 `SRC-L-041`、原 clause SHA `6b0a9cd59413c8e97af44e2a8cf6bb5d47ffb9cd3c724edb8424ba2f1f845cfb`；原 Owner `HGK_FABRIC_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`能力必經原Registry具體consumer ACK`。
- **NEG / FirstFail**：將結果變為 `name-only當能力已啟用`，原 Reader 必回 `DOMAIN_U41_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U41.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-2fe9f57027ed5ccf5867"></a>
### CHILD-U42.1｜U42：專用合約
- 原 Parent：SBL 能出 Skill/Plugin/Agent／Profile/Agent OS/AI System
- 子要求：SBL 能出 Skill；來源 `SRC-L-041`、原 clause SHA `d48e19106b964da01c345b8a55b1eb495bfaec534c8ba62fa565e9a237090299`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Skill有manifest/load/trigger/nontrigger/unload`。
- **NEG / FirstFail**：將結果變為 `copy-only`，原 Reader 必回 `DOMAIN_U42_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U42.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-cbf176b90f2fddd5137d"></a>
### CHILD-U42.2｜U42：專用合約
- 原 Parent：SBL 能出 Skill/Plugin/Agent／Profile/Agent OS/AI System
- 子要求：Plugin；來源 `SRC-L-041`、原 clause SHA `9b9310733c28a1a521a8a889b21a7d713c852f957f9b9dbb3686e167b4a00991`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Plugin有Host權限與version readback`。
- **NEG / FirstFail**：將結果變為 `不支援Host卻假PASS`，原 Reader 必回 `DOMAIN_U42_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U42.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-93897a58a2a02293ab15"></a>
### CHILD-U42.3｜U42：專用合約
- 原 Parent：SBL 能出 Skill/Plugin/Agent／Profile/Agent OS/AI System
- 子要求：Agent；來源 `SRC-L-041`、原 clause SHA `27a6b1ff9cf70f1ba14e5d153328ae3a4a448c10484c15f22b1511b46171991c`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Agent有tool allowlist/budget/stop`。
- **NEG / FirstFail**：將結果變為 `無界自治loop`，原 Reader 必回 `DOMAIN_U42_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U42.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-402a68f2635315acf2aa"></a>
### CHILD-U42.4｜U42：專用合約
- 原 Parent：SBL 能出 Skill/Plugin/Agent／Profile/Agent OS/AI System
- 子要求：Profile；來源 `SRC-L-041`、原 clause SHA `d51e0180018cd836e143fe3f951f3b5b152168e1a3e72d725035b7e855cac15d`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Profile有applicability/loaded SHA`。
- **NEG / FirstFail**：將結果變為 `selected當loaded`，原 Reader 必回 `DOMAIN_U42_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U42.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-0694c73c4aa592e3dd6a"></a>
### CHILD-U42.5｜U42：專用合約
- 原 Parent：SBL 能出 Skill/Plugin/Agent／Profile/Agent OS/AI System
- 子要求：Agent OS；來源 `SRC-L-041`、原 clause SHA `b7948feb0e2083bc1ddc3797eb85bd8b2cfb99745c0f13516bf21e4385b9093f`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Agent OS與AI System各有正式lifecycle/部署接受；不能以規劃冒實作`。
- **NEG / FirstFail**：將結果變為 `以Agent demo冒完整AI System`，原 Reader 必回 `DOMAIN_U42_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U42.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-211bd30261afa0c87606"></a>
### CHILD-U43.1｜U43：專用合約
- 原 Parent：支援 GENIE/GENIE.md 的正式 SWOF 關係不可混同
- 子要求：支援 GENIE；來源 `SRC-L-041`、原 clause SHA `5e6d1dbc0598b1ef1c1395afd46bfb06374e7085f28b44646b68a1d821a1f01e`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`GENIE原canonical owner不被SBL取代`。
- **NEG / FirstFail**：將結果變為 `SBL自建GENIE generator authority`，原 Reader 必回 `DOMAIN_U43_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U43.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-c5cef9f308264db843c6"></a>
### CHILD-U43.2｜U43：專用合約
- 原 Parent：支援 GENIE/GENIE.md 的正式 SWOF 關係不可混同
- 子要求：GENIE.md 的正式 SWOF 關係不可混同 (L5546)；來源 `SRC-L-041`、原 clause SHA `b84b7a1ac9b6b7e8586328dd1ff866beb883ed56da1afadc01da37dc92680394`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`GENIE.md版本read refs與SWOF正式關係可驗`。
- **NEG / FirstFail**：將結果變為 `任意GENIE.md冒原生部署`，原 Reader 必回 `DOMAIN_U43_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U43.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-ebf47ef3a9c6cb39fb28"></a>
### CHILD-U44.1｜U44：專用合約
- 原 Parent：提供可操作的新手 E2E 第一有用成果（FUO）
- 子要求：提供可操作的新手 E2E 第一有用成果（FUO） (L5547)；來源 `SRC-L-041`、原 clause SHA `81b4b08d865657d5194e4ba7007327cee6a42de21c87e10743c38d74d09ab76a`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`新手普通Goal得到可操作FUO與退出；無需B1長Prompt`。
- **NEG / FirstFail**：將結果變為 `只交表格與計數`，原 Reader 必回 `DOMAIN_U44_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U44.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-5d4f024a1ec19dbd8d1a"></a>
### CHILD-U45.1｜U45：專用合約
- 原 Parent：實作「不是重造輪子」的 24 NOBJ 名稱/狀態/准入
- 子要求：實作「不是重造輪子」的 24 NOBJ 名稱；來源 `SRC-L-041`、原 clause SHA `174c1bc78fd08892fa40e1898814cc513767cda41effa40f6788649cdb3f2d28`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`24 NOBJ原名/身份逐筆對讀`。
- **NEG / FirstFail**：將結果變為 `湊24不同工具`，原 Reader 必回 `DOMAIN_U45_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U45.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a7dd9331b5e3b2b92681"></a>
### CHILD-U45.2｜U45：專用合約
- 原 Parent：實作「不是重造輪子」的 24 NOBJ 名稱/狀態/准入
- 子要求：狀態；來源 `SRC-L-041`、原 clause SHA `766371a894463f17b7fefab9d1f71497b9bfc2fb8af46d2beb61481ecf7891cb`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`原REJECT/DEFER/REFERENCE狀態不被改寫`。
- **NEG / FirstFail**：將結果變為 `全改ADOPT`，原 Reader 必回 `DOMAIN_U45_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U45.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-e15a25ec0d5c3d4742dc"></a>
### CHILD-U45.3｜U45：專用合約
- 原 Parent：實作「不是重造輪子」的 24 NOBJ 名稱/狀態/准入
- 子要求：准入 (L5548)；來源 `SRC-L-041`、原 clause SHA `24e51df312681ab78d80d34d3b490f85bdb23da4fa458179768ecfe5c92b249f`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`license/pin/need/原Owner准入後才採用`。
- **NEG / FirstFail**：將結果變為 `未准入自動install`，原 Reader 必回 `DOMAIN_U45_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U45.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d62801a3dcab253bc771"></a>
### CHILD-U46.1｜U46：專用合約
- 原 Parent：保留 /1 vs /2 版本與兩個 Validator 的不相容
- 子要求：保留；來源 `SRC-L-041`、原 clause SHA `73cd770733496d4eda2d48a05fbc5a72e8fc54f035839ac75a597517469be2d9`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`兩版本來源與validator各保留`。
- **NEG / FirstFail**：將結果變為 `合併成單一/最新字串`，原 Reader 必回 `DOMAIN_U46_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U46.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-833ca4850b0a9db23daa"></a>
### CHILD-U46.2｜U46：專用合約
- 原 Parent：保留 /1 vs /2 版本與兩個 Validator 的不相容
- 子要求：1 vs；來源 `SRC-L-041`、原 clause SHA `ff22be5a5bc859dba78affc41b8c9113469b24c4e58b83af7bb9345178dac01c`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`v1送v1 validator需符合v1 shape`。
- **NEG / FirstFail**：將結果變為 `拿v2 receipt認證v1`，原 Reader 必回 `DOMAIN_U46_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U46.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d7773c57f9fbb79e671e"></a>
### CHILD-U46.3｜U46：專用合約
- 原 Parent：保留 /1 vs /2 版本與兩個 Validator 的不相容
- 子要求：2 版本；來源 `SRC-L-041`、原 clause SHA `9a015408055a9e8097f5b7ff7924eeebf92a6586bf6b2396c35158f9259b6e43`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`v2送v2 validator需符合v2 shape`。
- **NEG / FirstFail**：將結果變為 `靜默丟v2欄位`，原 Reader 必回 `DOMAIN_U46_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U46.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-490e1fa8eb0d9958f3f2"></a>
### CHILD-U46.4｜U46：專用合約
- 原 Parent：保留 /1 vs /2 版本與兩個 Validator 的不相容
- 子要求：兩個 Validator 的不相容 (L5549)；來源 `SRC-L-041`、原 clause SHA `a230b8d7dfc2e27fe4a93e0a66b2bdcf8430477697b9e45f630240823b4c2342`；原 Owner `TOOL_REGISTRY_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`不相容時出版本NACK與受影migration`。
- **NEG / FirstFail**：將結果變為 `無損失表直接跨版`，原 Reader 必回 `DOMAIN_U46_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U46.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-ac8876b281da6d203870"></a>
### CHILD-U47.1｜U47：專用合約
- 原 Parent：Open-source License/NOTICE/SBOM/Secret/Dependency 所有正式 Gate
- 子要求：Open-source License；來源 `SRC-L-041`、原 clause SHA `2e6195e74f044dc56706807b9f99aaff560e141cf83051cb3aec8f8b5cfaa70b`；原 Owner `SBL_RELEASE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`License義務與採納source pin一致`。
- **NEG / FirstFail**：將結果變為 `未知license照裝`，原 Reader 必回 `DOMAIN_U47_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U47.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-4a8a99ff7626ddbb1de3"></a>
### CHILD-U47.2｜U47：專用合約
- 原 Parent：Open-source License/NOTICE/SBOM/Secret/Dependency 所有正式 Gate
- 子要求：NOTICE；來源 `SRC-L-041`、原 clause SHA `9cf6b3af0869da8ba63327c3b3e310d3eae2b111bcd9ea99d8e57c93215ce905`；原 Owner `SBL_RELEASE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`NOTICE包含來源歸屬與必要聲明`。
- **NEG / FirstFail**：將結果變為 `剝除原歸屬`，原 Reader 必回 `DOMAIN_U47_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U47.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-b6f698a6b7a5a112b25f"></a>
### CHILD-U47.3｜U47：專用合約
- 原 Parent：Open-source License/NOTICE/SBOM/Secret/Dependency 所有正式 Gate
- 子要求：SBOM；來源 `SRC-L-041`、原 clause SHA `76a5196b0aa1f4b90227bd13380171c835960df6be3fa63f3ddeb0c1b6c9a0fe`；原 Owner `SBL_RELEASE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`SBOM component/pin/subject可回算`。
- **NEG / FirstFail**：將結果變為 `名單冒SBOM`，原 Reader 必回 `DOMAIN_U47_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U47.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-040388cec0eb7dabafd1"></a>
### CHILD-U47.4｜U47：專用合約
- 原 Parent：Open-source License/NOTICE/SBOM/Secret/Dependency 所有正式 Gate
- 子要求：Secret；來源 `SRC-L-041`、原 clause SHA `755a2b942b1f26ad35a48f06f5c8273325eabe99cd7f6059bdf6effad7942731`；原 Owner `SBL_RELEASE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Secret scan命中必擋受影發行且不印secret`。
- **NEG / FirstFail**：將結果變為 `忽略secret hit`，原 Reader 必回 `DOMAIN_U47_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U47.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-4515ed61ae45659fb116"></a>
### CHILD-U47.5｜U47：專用合約
- 原 Parent：Open-source License/NOTICE/SBOM/Secret/Dependency 所有正式 Gate
- 子要求：Dependency 所有正式 Gate (L5550)；來源 `SRC-L-041`、原 clause SHA `5c7a7192fcc2a78ee97431e19b899578d1ea35898e92786575a725719d95be31`；原 Owner `SBL_RELEASE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Dependency供應鏈/漏洞Gate按原Policy與證據`。
- **NEG / FirstFail**：將結果變為 `CI綠就當Release`，原 Reader 必回 `DOMAIN_U47_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U47.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-29a177fa68a99474cb74"></a>
### CHILD-U48.1｜U48：專用合約
- 原 Parent：產品三模式的 Required Gate/Forbidden Gate 逐項編譯
- 子要求：產品三模式的 Required Gate；來源 `SRC-L-041`、原 clause SHA `b5b646fe978afe4ecb100a9d79b4fe9196d2acc5b50434efbb8778e19b40b818`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`三Mode每項Required Gate按need逐項編譯`。
- **NEG / FirstFail**：將結果變為 `Standalone強制全SWOF Gate`，原 Reader 必回 `DOMAIN_U48_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U48.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-3a65eb5f540b552355f5"></a>
### CHILD-U48.2｜U48：專用合約
- 原 Parent：產品三模式的 Required Gate/Forbidden Gate 逐項編譯
- 子要求：Forbidden Gate 逐項編譯 (L5551)；來源 `SRC-L-041`、原 clause SHA `c676e1ec119d404b279b5bce1b934253112624874c657f077c2860f432a55970`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Forbidden Gate在該Mode被實際拒絕`。
- **NEG / FirstFail**：將結果變為 `Shadow允world effect`，原 Reader 必回 `DOMAIN_U48_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U48.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-a7c2edbdcfa8a69300fb"></a>
### CHILD-U49.1｜U49：專用合約
- 原 Parent：反過度工程 Overengineering Index 與停損
- 子要求：反過度工程 Overengineering Index；來源 `SRC-L-041`、原 clause SHA `2297814fa15119c8855fc3cfab6036fb1ee91b2f8d532d6004ab94ed596c43b6`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`Overengineering Index依來源指標與需求差額計算`。
- **NEG / FirstFail**：將結果變為 `自造閾值當Owner標準`，原 Reader 必回 `DOMAIN_U49_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U49.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-891be2cbf43021b4cfb0"></a>
### CHILD-U49.2｜U49：專用合約
- 原 Parent：反過度工程 Overengineering Index 與停損
- 子要求：停損 (L5552)；來源 `SRC-L-041`、原 clause SHA `41347fe1411b11b0ce942cf9a643a1845d43b08ec8d8af5afdde4a1e21b5ee3e`；原 Owner `SBL_PRODUCT_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`達停損條件保留未關閉需求與合法resume`。
- **NEG / FirstFail**：將結果變為 `停損宣告所有需求PASS`，原 Reader 必回 `DOMAIN_U49_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U49.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-1acf5eab1ab097e9c262"></a>
### CHILD-U50.1｜U50：專用合約
- 原 Parent：提供 workflow / script / config、機器 JSON/TSV
- 子要求：提供 workflow；來源 `SRC-L-041`、原 clause SHA `6e3f393c06c3dc29b556c31d82e94c8c8af318ed6a708d2ed13b09df352eb118`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`workflow步驟可按受權scope執行並有退出`。
- **NEG / FirstFail**：將結果變為 `純敘事無步驟`，原 Reader 必回 `DOMAIN_U50_1_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U50.1` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-cc3c60ba4a4607e1023b"></a>
### CHILD-U50.2｜U50：專用合約
- 原 Parent：提供 workflow / script / config、機器 JSON/TSV
- 子要求：script；來源 `SRC-L-041`、原 clause SHA `8de87fa9f663a2a113df24293e05ced6b323de7a16747d0ddeeecbdb6eb873ca`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`script具input/exit與無效輸入拒收`。
- **NEG / FirstFail**：將結果變為 `腳本有名無實體`，原 Reader 必回 `DOMAIN_U50_2_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U50.2` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-f69314ffb8ba3677d128"></a>
### CHILD-U50.3｜U50：專用合約
- 原 Parent：提供 workflow / script / config、機器 JSON/TSV
- 子要求：config；來源 `SRC-L-041`、原 clause SHA `4ac7402906395259e0045ef86614f69f3c9a677e25dcc93a0c4c9bfb048fcbc8`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`config可驗schema/version且有rollback`。
- **NEG / FirstFail**：將結果變為 `改Active未有OPS ECP`，原 Reader 必回 `DOMAIN_U50_3_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U50.3` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-79484b57cbc5efd79c86"></a>
### CHILD-U50.4｜U50：專用合約
- 原 Parent：提供 workflow / script / config、機器 JSON/TSV
- 子要求：機器 JSON；來源 `SRC-L-041`、原 clause SHA `0a1146154e8ba7d82b2853ccdde48fad3b046e5315a8674879a72d491eb4359f`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`JSON可parse且維持所有原ID/否定scope`。
- **NEG / FirstFail**：將結果變為 `只匯出成功列`，原 Reader 必回 `DOMAIN_U50_4_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U50.4` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。

<a id="current-d45f6cb3c21b8cacdb67"></a>
### CHILD-U50.5｜U50：專用合約
- 原 Parent：提供 workflow / script / config、機器 JSON/TSV
- 子要求：TSV (L5553)；來源 `SRC-L-041`、原 clause SHA `601a4540eb020bc6cb5a610a0fc8454b90ccea761acae2e82c1668b0571417ce`；原 Owner `ARCHITECT_ASSURANCE_OWNER / DOC-12`。
- 具名 Producer→Receiver：原 `SBL DOC-01 Product Reader` 將此 Child 原子投入 `ProductOutcome`，依本 Child 的效果型別及 Mode/Host 生成一個具 `child_id, original_parent, sourceSHA, observed_result` 的有界候選；不把其它 Child 的結果當本 Child 的 Raw。
- **POS**：`TSV欄位escape/行數/ID與JSON roundtrip一致`。
- **NEG / FirstFail**：將結果變為 `分隔符破壞列`，原 Reader 必回 `DOMAIN_U50_5_VIOLATION`，不得將原 Parent 否定倒轉。
- NoFit/Exit：本 Host/Domain Source/Loader 缺件時標記 `U50.5` 受影 HOLD；保留 SBL FullProduct 義務，失敗只撤這筆候選，真正 Native Case 未跑前不得 PASS。


## 本版未受影條文（完整沿用、當期生效）

## R2-09-U03：三SP×三動作九子測（原ID不改）

每條先查本Host支援的真installer/loader/trigger。移除後不得觸發；非相關目標不得誤觸發；未支援Web Host只報HOST_HOLD，不偷換Codex成功。
| subtest_id | POS | NEG/first_fail | expected raw |
|---|---|---|---|
| U03.1@TPM | TPM 本身在此Host install 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的install Raw給TPM / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'install_observation'] |
| U03.1@Commander | Commander 本身在此Host install 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的install Raw給Commander / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'install_observation'] |
| U03.1@Challenge | Challenge 本身在此Host install 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的install Raw給Challenge / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'install_observation'] |
| U03.2@TPM | TPM 本身在此Host load 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的load Raw給TPM / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'load_observation'] |
| U03.2@Commander | Commander 本身在此Host load 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的load Raw給Commander / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'load_observation'] |
| U03.2@Challenge | Challenge 本身在此Host load 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的load Raw給Challenge / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'load_observation'] |
| U03.3@TPM | TPM 本身在此Host invoke 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的invoke Raw給TPM / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'invoke_observation'] |
| U03.3@Commander | Commander 本身在此Host invoke 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的invoke Raw給Commander / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'invoke_observation'] |
| U03.3@Challenge | Challenge 本身在此Host invoke 可讀回；invoke含trigger/nontrigger/卸載後不觸發 | 借TPM或其它SP的invoke Raw給Challenge / SP_ACTION_EVIDENCE_MISMATCH | ['host_identity', 'sp_manifest_sha', 'fresh_session_id', 'invoke_observation'] |
