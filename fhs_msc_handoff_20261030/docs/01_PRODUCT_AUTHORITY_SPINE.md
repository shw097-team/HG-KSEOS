<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 01 PRODUCT AUTHORITY SPINE｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：r2 §1 Goal/Kind/Mode/Host、三 SP

## 1. 使用者產品入口：七痛點、八 Kind、三 Mode、四 Host、三 SP 與 First Useful Outcome

### 1.1 Goal 最短合法路由（不是新的服務）

**輸入**：`Goal`、有效 `Source Locator` 或合法缺源、`ProductKind`、`Mode`、`HostTarget`、`ProviderState`、`DesiredEffect`、`KnownAnswerRef`、`DesiredOutcome`；所有欄位按 SBL 原資料契約 Reader 消費，不能新加必填 Canonical 欄位。[SBL DOC00 `R00.r3.1/R02/R04`；BODY00/09/09B]

**順序與真結果**：

1. SBL 原 Source Reader 讀 Subject/SourceSHA 與有效 ACL；無有效來源可進 no-effect explore 與 Needs，不得造 PI 或施工。
2. SBL 原 GoalCard／QuestionLedger 消化同 Source/Scope/Epoch 的 Known Answers；同問題不重問，只對 Source/DecisionVersion 變更部分開 NeedDelta。
3. 原 MethodDecision 先定一次**主要 Plan Owner**及可按 Stage 調用的受限方法鏈（不是全 Donor 串行）；列出選用理由、不選理由和終止／NoFit 路線。
4. 原 Capability Reader 依 Kind/Mode/Host/Provider ON/OFF 查 Default30 原承諾、具名 Occupant 與其 `PIN→INSTALL→LOAD→TRIGGER→QUALIFY` 狀態；已合格且同 Scope 直接復用，缺載入只停需要該輪子的子功能。
5. 依 Kind 先做合法的 First Useful Outcome：三 SPEC Draft、可運行 CLI、可觸發 Skill、Plugin Host Artifact、受界 Agent、合格 Profile 或 GENIE.md 等；原 ModeGate 決定是否可進 Effect。
6. 要變更受治理世界才轉入 PIPD 五出口、Fabric Policy、HGK WorkOrder/Permit/SharedSpine、Hermes Maker、World、Checker；無效果請求不因完整 Native Gate 未跑被卡死。
7. 同 Subject 已有合法 WorkOrder，核 Epoch／Source／Scope／Cursor 後原位 Resume，不再次問 Goal、不生成第二 Task、不重放已施加的 Operation。

**負例**：`SOURCE_MISSING`→只無效果探索；`KNOWN_ANSWER_REASK`→讀有效答案；`KIND_HOST_NOFIT`→指明缺少的 Host Capability，不假稱合格；`PROVIDER_OFF`→零未批准 Provider 呼叫；`EFFECT_SCOPE_DENIED`→保留候選、拒絕寫入；`UNKNOWN_EFFECT`→Reconcile，禁止盲重試。[BODY00/03/09B/10]

### 1.2 八 ProductKind：真產物與合法降級

| 原 Kind | Input→具體建造或讀取→第一成果 | 真 Consumer、POS/NEG | Host 未合格時 |
|---|---|---|---|
| `CLI_TOOL` | Goal/CLI spec→原 Builder 打包 entrypoint/help、JSON/nonzero、uninstall→可執行 CLI + readback | 原 SBL CLI Product／當期 Host Process；NEG 無 entrypoint、錯 exit code | `KIND_HOST_NOFIT`；可給 CLI SPEC／原命令候選，不能自報 Installed |
| `AGENT_SKILL` | Source+Skill Need→`SKILL.md`、references、Host Adapter、trigger/nontrigger→Portable Skill | 原 Host Skill Loader；NEG copy-only、未觸發、無卸載 | 保留草稿，`HOST_LOAD_HOLD` |
| `SIMPLE_AGENT` | Goal+tool allowlist/timeout/loop budget→有界 Agent→會停止的 Action + Raw | Hermes/具名原 Host Worker；NEG 無上限自動迴圈／越權工具 | 降唯讀 Plan 或 `NOFIT` |
| `PLUGIN` | Manifest/publisher/license/permissions→合法插件包→install/load/trigger/remove | 原 Host Plugin Owner；NEG 只有 Plugin 宣言無 Host 載入 | 候選 manifest，不自稱 Plugin Ready |
| `PROFILE` | Need/Policy/Host→typed Provider/Model Profile→實際 served/readback | 原 HGK Profile/Provider Owner；NEG role card 當真正 Principal | `PROFILE_BIND_HOLD` |
| `AGENT_OS` | Agent OS 全生命週期要求→原相關領域能力審查→真正可執行系統或有界設計 | 原 SBL Product Owner；NEG 以 Hermes Docs 假稱已建完整 OS | 未合格時輸出只讀分析與 `NOFIT`，不捏造 OS |
| `AI_SYSTEM` | 綜合需求→三 SPEC＋PIPD＋多 Host/受影 E2E → 真系統交付候選 | 原 TPM／Domain Builder；NEG 只做單一 Prompt 即稱 System PASS | 分階段、明確阻斷能力，保留最小合法成果 |
| `GENIE/GENIE.md` | Source、Personalized Need、Host Capsule→GENIE.md/version/knowledge refs→有效載入或僅 Draft | 原 GENIEMAKER/Host Writer；NEG GENIE 文本等同 Host Installed | 合格 Host 前只輸出 Source-bound GENIE Draft |

**三 Mode**：`STANDALONE` 可就合法本地非 Native 成果依原使用者授權完成，不必被無關 HGK Gate 卡死；`PREW3_SHADOW` 僅 frozen SOURCE_READ，不能 Build Wheel、改 W3 packet 或寫世界；`SWOF_CONNECTED` 的真 Effect 必須原 HGK Admission/Receiver，不能僅靠 SBL HMAC ACK 解鎖任意 Effect。[SBL `sbl_core/modes.py`；BODY09B]

**四 Host**：Hermes Agent、Codex、Claude Code、ChatGPT；前 3 的 CLI/Skill/Plugin 能力各以真 Loader/Process/Security 驗證；ChatGPT Web/API-only 與有 Plugin/Connector 的不同 Surface 不可假定具有 OS process runner。每 Host 要 Install→Register→Effective Load→Trigger/Nontrigger→Uninstall/Retire，缺哪級只限制受影 Claim；Hermes-first 不刪其他 Host 的原產品承諾。[BODY09B `R2-09B-CELL`]

### 1.3 三 SP：Portable 與 Native 雙形態，不混 Writer／Checker

| SP／形態 | 觸發與操作→結果 | 原消費者、限制與失敗 |
|---|---|---|
| **TPM-SP Portable** | Goal/Source/K0–K3 Readset→Product/Architecture/Program 三 SPEC 候選、QuestionDelta、18 Stage 的 Proposal | PIPD Intake／原 TPM Writer；不可把 Skill 記錄當正式 PI/PD。缺 Reader 只停受影 SPEC。 |
| **Native FHS-TPM** | 已准入的 PLAN WorkOrder→原 PLAN Role/Revision CAS→同 WorkID 的真 PlanRevision | 原 HGK PLAN Consumer；沒有真 Registry/Permit 不自稱 Native Stage Done。 |
| **Commander-Skill Portable** | 使用者選擇 A/B/C Guide、合法 Work Plan Scope→Program Action Proposal/NeedInfo | 原 PLAN Producer 或原 PIPD；不建立新的 Executor Queue，不重問已有 Decision。 |
| **Native FHS-Commander** | 有權原 PLAN／Guide Request→原 Writer CAS Replan/Scope/Epoch→同 WorkID 可恢復 Cursor | 原 HGK/TPM；沒有原 Enum/Adapter 則 `COMMANDER_ABI_HOLD`，不得製作新 issuer。 |
| **Acceptance Challenge-SP Portable** | Frozen Readset/CaseSpec→有界異構 Review／Attack Finding→Advisory Inbox | 原 AO/Challenge Consumer；外部模型不同不等於獨立 principal。 |
| **Native FHS-Acceptance Challenge** | 原有保護的 Raw/Oracle/Checker Principal→15 異構 AC Edge、適用 96 Oracle 的 Verdict→原 Reducer | Maker 不能改 Oracle／簽 Verdict；不以 Portable Skill Finding 作獨立 PASS。 |

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


## 本輪同域受影修復：三 SPEC 本輪可交付實作

## 三 SPEC 與一次來源綁定實作投影（TPM-SP／PM／SE／TPgM）

### Product SPEC｜單人 Owner 交付 FUO

- **Persona/JTBD**：同一 OWNER 以普通語言提供 Goal「整理已授權來源，產生可檢核的變更規格並可合法施工」；先得到 source-bound 需求、限制、可見的可交付物，不需預知 PIPD/Model/Lane 或貼 B1 長 Prompt。
- **FUO-01**：原 SourceManifest 中每個適用需求至少具 `原身份→原作用→Owner/Consumer→POS/NEG`，對應可打開的 Product/Architecture/Program SPEC；失敗不能用生成檔案數替代使用者效益。
- **FUO-02**：當有受權真 RepoContext 時能指出 precise patch candidate、DEV/OPS 效果分界、最小 Need closure、rollback；無 RepoContext 時交付可用設計而非假 PD 綁定。
- **FUO-03**：透過真 Host 完成安裝/載入/觸發及功能驗收，否則產品承諾原封保留，Implementation=HOST_PENDING，不把 Mandatory 註銷。
- **Non-goals**：移轉 SBL/PIPD/Fabric/HGK Canonical Writer；在 ChatGPT 沙盒替 Windows 真 Host 發 permit；自簽 Protected Checker；自動 push/release；對 485 工具全裝。
- **ACC/POS**：Owner 新 Goal 不提供 B1 長 Prompt 也得到具來源、版本、分權且有效的 L0 設計；適用原 Child/949/192/Case Oracle 不丟失。
- **NEG**：把別 Host receipt 當現役、由 maker 自填許可、把產品 Mandatory 降成 Optional、缺件 global HOLD，任一出現都拒收。

### Architecture SPEC｜單一 Writer 與有版本的 ABI

| Seam | Producer → Consumer | Input | 受保護輸出 | FirstFail |
|---|---|---|---|---|
| Source / TPM | OWNER → TPM-SP | Goal、known_answers、source locators | 三 SPEC、IntentCard Proposal | INTAKE_INVALID |
| PIPD Canonical | PIPD 原 Writer → PD/ECP Reader | Frozen Intent、Authority、Profile、PI | 原 PI/PD/DEV/OPS/TQAEP | CR-DOC04-STATE-MAP |
| Fabric Policy | Fabric 原 Owner → HGK 既有 Consumer | approved Policy + epoch/SHA | active→loaded→consumed chain | POLICY_NOT_LOADED |
| HGK Admission | 原 Issuer → 原 Hermes Worker | ECP、exact Subject/Scope、nonce/TTL | WorkOrder/ExecutionBinding/Permit | ADMISSION_DENIED |
| Hermes Execute | Hermes 原 Queue/Journal → World Reader | WorkID、lease generation、operation_id | Raw pre/post、cursor、residue | LEASE_FENCING_DENY |
| Challenge / Checker | Challenge reviewer → Protected Checker | Oracle、same-candidate Raw | 獨立 Principal 的驗收結果 | TQ_SOD / CHECKER_NOT_BOUND |
| Publisher | 原 Release Writer → 合法收件者 | independent PASS + Owner approval | versioned release receipt | RELEASE_HOLD |

**ADR-01**：共享核心不等於共享 Principal；不新增 Issuer、Queue、Policy、Checker、Release Authority。**ADR-02**：`SOURCE_READ`/`LOCAL_DRAFT_WRITE` 和 L2/L3 真效果分流；零效果不要求不存在的 operation nonce。**ADR-03**：無實際 Registry Reader、Host Process Raw 或 Schema 時提案保持 `PROPOSED/NOT_BOUND`，不得猜 enum。**ADR-04**：既有同 scope WorkID/cursor 先 resume；unknown effect 先 reconcile 而非重播。**ADR-05**：PREW3_SHADOW 只讀 frozen readset；產品建置在獨立 LOCAL_BUILD subject 中運行，不拿 Shadow 上升權限。

### Program SPEC｜Typed DAG、最小自舉與有界續工

- **起跑線**：WP-FHS-00 → WP-FHS-01 → WP-FHS-02 先 source/authority/Host 唯讀；依 Need 選 ready WP，無 effect 時可停於可交付 design FUO。
- **首效果**：只在 Active/Consumed Policy、HGK Issuer、CAP-BOOT 當期 qualified 後開始；WP17 技術啟用不能反依賴 WP06 的首個效果，須以原 Host installer 自舉。
- **B1→W18**：保留 PI27、PD31、TQAEP 282 cases，依 Worker crash/resume/unknown-operation、new PID everyday Goal 給出單獨 Runner Binding 與 H18 原本 test ID；Maker/Checker 分權。
- **Stop**：只停止第一失敗依賴的 WorkPackage 受影錐，維持其他 READY；一個已回答且同 Subject/Scope 的 Owner QuestionLedger 答覆不得重新詢問。
- **Resume**：重新讀 SHA/current HEAD/PolicyEpoch/receiver schema/operation World Raw，只重試尚未有已知效果且獲原 Issuer 新授權的卡；不同 Subject 不借用 nonce。


---




## 本版未受影條文（完整沿用、當期生效）

## R2-01-SPEC：三份 SPEC 的不同消費結果

Product SPEC：單人 OWNER 輸入 goal/source/known_answers，PM 將 Persona/Pain/JTBD 轉為可見 FUO、MVP、non_goals、ACC/NEG。FUO 必是使用者能取用的成果，例如普通「整理來源後產待審變更規格」得到 source-bound SpecDelta；不得以檔案數當 FUO。Consumer 是 PIPD Intake/原產品 Owner；POS 原需求每一否定作用域有來源；NEG 把「不得混同 SWOF」改成「等同 SWOF」必拒 `PRODUCT_POLARITY_LOSS`。

Architecture SPEC：SE 讀 Product SPEC、既有 RepoContext 和權威表，劃 Domain/ABI/NFR/ADR。每個 seam 記單一 writer、reader、輸入/輸出版本、trust boundary、effect class 和 first_fail。Consumer 為原架構 Owner/PIPD Binder；POS 同一 effect 只有原 Issuer；NEG 用 adapter 增設 Issuer、Queue、Policy 或 Checker → `AUTHORITY_COLLISION`。

Program SPEC：TPgM 消費上述兩份 SPEC，以每 WP exact output/typed dependency、風險、Done、rollback、resume 組合法 DAG。Consumer 為原 Native PLAN；POS SOURCE_READ 能獨立完成，不待 effect permit；NEG WP17 待 WP06、而 WP06 又待 WP17 → `DAG_CYCLE`。22 WP 唯一實體在 [BODY-11](11_WORKPACKAGES_AND_DAG.md)。

## R2-01-AUTHORITY：三 SP、六模組與 Owner

TPM 對 Goal Intake/Specification/Program proposal 負責；Guide 支援 Routing/Planning proposal；Governed Execution Interface 只轉交原 PIPD/Fabric/HGK；Evidence/Verification 支援 frozen-readset Challenge；Bounded Evolution 將 first_fail 送原 Maker repair。這是職能視角，不能當不同 OS principal。

Master 決定跨域意圖，Domain v2 決定該域設計，SBL DOC00–13 保留原產品義務，PIPD DOC00–09 保留 formal Writer。Fabric Policy、HGK Issuer、SharedSpine、Checker、Publisher 的真 registry/ACL 不受文稿改寫。三 SP 各自 install/load/invoke 九子測在 [BODY-09](09_SBL_DOC00_13_FULL_UPGRADE.md)。舊 SBL Commander-SP 僅作歷史來源；現役路線只能使用非 legacy Producer 或正確 `C PARK`。

## R2-01-EXAMPLE：普通 Goal 到候選與退出

輸入「為此既有產品加入離線來源查詢」：PM 指定離線可查 source locator 是 FUO；SE 指定 SOURCE_READ、provider_off=true、不新建 Authority DB；TPgM 產唯讀 source probe 和隔離 spec 卡。輸出三 SPEC + trace + unresolved bindings，交原 PIPD Intake。若沒有原 Writer ACK，狀態為 SPEC_CANDIDATE；使用者仍可讀 SPEC，只有 PI promotion HOLD。NEG：未找到 CLI 就聲稱 PI_COMPILED 或擅 install 三十套工具 → `CLAIM_ESCALATION/UNNEEDED_EFFECT`。退出僅撤本輪隔離候選，保留來源及既有 admitted work。
