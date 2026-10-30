<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 02 PIPD LIFECYCLE AND TPM｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜首工作功能 PI 的真 Compiler 接收

**普通 Goal**：為一個普通工程需求讀取已內建的 SBL14/PIPD10 與已知答案，產出三 SPEC 到受權隔離草稿區，ProviderOff=true，再交原 PIPD。使用者不須重貼 B1 長 Prompt 或重新上傳24 DOC。

**可直接讀取的實例**：`02_FIRST_WORK/RUN/ProductSPEC.json`、`ArchitectureSPEC.json`、`ProgramSPEC.json` 由原 sbl-tpm-sp `plan_spec` 實際產生；`SourceAuthority.json` 由原 PIPD `freeze_authority` 產生，SourceFamily digest/locator 逐檔釘住；`IntentCard.json` 由原 `intake` 讀 `FIRST_WORK_FUNCTIONAL_SOURCE.md` 24條業務功能；`ProfileBinding.json` 與 Compiler 的有效 Profile 使用原九軸安全 veto，沒有將十二風險分數塞成九軸 enum。

**原 Compiler 輸出**：PI=`PI-035c5e6e6333148b`，hash=`035c5e6e6333148b4808492d7c9277dd83cfcd503201e0f508dad14e1d7bafb3`。原 `pipeline.validate_pi` 驗 PI、ProfileBinding、24個 RequirementAtom、24條 TraceLink，回覆 PASS；另對 strict TaskSpecSeed/ExecutionHandoff/WorkOrderCandidate 驗 Schema與 frozen context回覆 PASS。每 Atom 的專屬 Consumer、POS、NEG、原 Source coordinate 在 `FUNCTIONAL_ATOMS_CONSUMERS_POS_NEG.json`，不是只有 ID/FirstFail 的投影。

**晚綁界線**：TaskSpecSeed=`TSS-f9a394ca4633c841` 交原 receiver adapter；`PD_LATE_BIND_RECEIVER_CONTRACT.json` 明列原 `pipeline.bind_pd(pi, repo_context)` 的實際入參、有限 WriteSet、實測 root/HEAD/index/untracked 與 freshness。交接時不序列化假 live PD；已另以實際存在的隔離 document fixture 驗真 PD binder 的 POS、缺 root、stale freshness、`**` 拒收。該 fixture PD 不是施工工作樹，不拿其 PREDEV_READY 當 Native Ready。

**不構成阻斷的舊差異**：全17冊直接 intake 的舊 NACK 不適用這24條已接收的必要閉包。CLI13/14 差異只隔離新增 compile-cc 本身，本首工作使用兩版共有的 intake/profile/compile-pi/bind-pd/validate Reader。PI legacy `DOC-03 DOMAIN_ORACLES` 依原 Schema 原字保留；DOC07為 semantic Owner 的正式 ratification 只在原 Protected Checker/Native promotion消費時受影，不改 strict payload、不阻斷本輪 source/draft/PI規劃。T4/T5 的正式 StateEnum 未被草稿產生改寫。

## 本輪同域受影修復：r2 §2 TPM 18 Stage／PIPD 19/13

## 2. TPM 18 Stage、K0–K3、PIPD 五出口、19 Contract、13 CLI 的施工編排

### 2.1 K0→K3 Cold Host 導入，不要求使用者重上傳24 DOC

`K0 ImmutableCorpusBundle`：14 SBL＋10 PIPD DOC bytes/sha/Owner/License→原 Host Reader，24/24 可校驗；`K1 ClauseIndex`：Heading/Line/TextSHA/ACL 索引；`K2 SupersessionConflictRegistry`：依同 Domain Writer/Scope/Supersedes 判 current，不由較新日期跨域篡位；`K3 OnDemandReader`：同 Subject/Source/Clause/ACL 輸出 SourceBoundExcerpt 給三 SPEC。發現 K0 缺文件、K1 stale、K2 writer conflict、K3 Injection 時各走受影 HOLD、退回前一可信 Readset；未全裝的 Host 不能稱 `HOST_LOADED`。[BODY02 §6.1]

## STATIC-v1 三角色 18 Stage：按插件原 Clause Reader 的實際契約

| Stage | 原 Input | 原操作 → Output／Consumer | Guard／FirstFail／退出 |
|---|---|---|---|
| PM:T0 | goalcard, known_answer_refs, source_sha256 | segregate facts from user guesses; detect unanswered JTBD → ProductKnownState@1(goal_sha,missing_questions) / ProductOwner/PIPD Reader | GoalCard+known_answer_refs; source_sha present；KNOWN_ANSWER_REASK；ASK_NEW_ONLY；`T1` |
| PM:T1 | persona, painledger, jtbd, source_sha256 | rank questions by user information gain → QuestionPriority@1(qid,impact,source_ref) / ProductOwner/PIPD Reader | Persona+PainLedger+JTBD; source_sha present；JTBD_UNBOUND；FUO_PATH_BOUND；`T2` |
| PM:T2 | fuo, useroutcome, variants, source_sha256 | define observable CLI/add,list,delete or brownfield user result → ProductSuccess@1(FUO,exit_code,negative_cases) / ProductOwner/PIPD Reader | FUO+UserOutcome+variants; source_sha present；FUO_UNTESTABLE；USER_VALUE_MEASURABLE；`T3` |
| PM:T3 | productsuccess, primarykind, source_sha256 | compile ProductSPEC draft and acceptance cues → ProductSPECDraft@1(journey_id,kind,acceptance_sha) / ProductOwner/PIPD Reader | ProductSuccess+PrimaryKind; source_sha present；KIND_ID_DRIFT；OWNER_REVIEW_REQUESTED；`T4` |
| PM:T4 | productspecdraft, acc_neg, source_sha256 | issue user-facing POS/NEG proposal, not Native verdict → ProductAcceptanceProposal@1(pos,neg,raw_expect) / ProductOwner/PIPD Reader | ProductSPECDraft+ACC_NEG; source_sha present；ACC_NOT_BOUND；PIPD_ACC_REF_AVAILABLE；`T5` |
| PM:T5 | fuo_raw_refs, feedback, source_sha256 | compare observable use vs claimed outcome; create repair request → ProductReviewRequest@1(gap,affected_journeys) / ProductOwner/PIPD Reader | FUO_raw_refs+feedback; source_sha present；FUO_RAW_MISSING；REVIEW_WITH_RAW_OR_HOLD；`T5 final review or affected T3/T4 rework` |
| SE:T0 | repoboundaries, sourceindex, source_sha256 | enumerate source/destination trust seams → SystemReadset@1(owners,sha,scope) / ArchitectureOwner/HostReader | RepoBoundaries+SourceIndex; source_sha present；SYSTEM_SOURCE_GAP；SOURCE_BOUND；`T1` |
| SE:T1 | systemreadset, adrrefs, source_sha256 | assign every seam to exactly one writer → OwnershipSeamMap@1(writer,reader,forbidden_effect) / ArchitectureOwner/HostReader | SystemReadset+ADRRefs; source_sha present；SEAM_OWNER_CONFLICT；ONE_WRITER_PER_SEAM；`T2` |
| SE:T2 | riskinventory, hostcaps, source_sha256 | trade off typed ABI and provider-off reliability → ADRSet@1(option,tradeoff,security_guard) / ArchitectureOwner/HostReader | RiskInventory+HostCaps; source_sha present；ARCHITECTURE_RISK_OPEN；ADR_OWNER_REVIEW；`T3` |
| SE:T3 | adrset, c4, componentcards, source_sha256 | bind schemas and compatibility version → ArchitectureSPEC@1(abi,compat,host_matrix) / ArchitectureOwner/HostReader | ADRSet+C4+ComponentCards; source_sha present；ABI_SCHEMA_MISMATCH；SCHEMA_READER_BOUND；`T4` |
| SE:T4 | architecturespec, boundaryneg, source_sha256 | test scope/token/provider-off/thin adapter semantics → ArchitectureNEGRequest@1(neg,oracle_source) / ArchitectureOwner/HostReader | ArchitectureSPEC+BoundaryNEG; source_sha present；PERMISSION_NEG_MISSING；NEG_PROPOSAL_READY；`T5` |
| SE:T5 | nativerawrefs, integrationrisks, source_sha256 | re-evaluate actual host ABI and raw results → ArchitectureReview@1(findings,repair_cone) / ArchitectureOwner/HostReader | NativeRawRefs+IntegrationRisks; source_sha present；HOST_RAW_MISSING；RAW_OR_HOLD；`T5 final review or affected T3/T4 rework` |
| TPgM:T0 | ownerroster, costtime, source_sha256 | identify budget milestones without claiming approval → ProgramIntent@1(milestone,owner,risk) / ProgramOwner/NativeRouter | OwnerRoster+CostTime; source_sha present；MILESTONE_OWNER_MISSING；OWNER_ROSTER_COMPLETE；`T1` |
| TPgM:T1 | unknowndependencies, resourcecaps, source_sha256 | record sequencing constraints and blocking decisions → SchedulingAssumptions@1(edges,confidence) / ProgramOwner/NativeRouter | UnknownDependencies+ResourceCaps; source_sha present；UNBOUNDED_WORK；DEPENDENCY_DISCLOSED；`T2` |
| TPgM:T2 | ownergates, dependencyedges, source_sha256 | toposort bounded DAG and cycle check → ProgramDAG@1(topo,locks,no_fit) / ProgramOwner/NativeRouter | OwnerGates+DependencyEdges; source_sha present；DAG_CYCLE；ACYCLIC_AND_SCOPED；`T3` |
| TPgM:T3 | programdag, productspec, architecturespec, source_sha256 | package work with traceable scope and approver → ProgramSPEC@1(wp,effort,owner,stop) / ProgramOwner/NativeRouter | ProgramDAG+ProductSPEC+ArchitectureSPEC; source_sha present；WP_SCOPE_UNKNOWN；WORK_PACKAGE_OWNER_REVIEW；`T4` |
| TPgM:T4 | pi_pd_refs, verifierreferral, source_sha256 | route to correct Native ECP/Oracle Owner → HandoffReferral@1(expected_grants,oracle_conflict) / ProgramOwner/NativeRouter | PI_PD_refs+VerifierReferral; source_sha present；CR_ORACLE_001；NATIVE_REF_NOT_SYNTHESIZED；`T5` |
| TPgM:T5 | milestoneraw, issueledger, source_sha256 | review schedule with evidence status; refreeze affected only → ProgramReview@1(blocked_waves,replan_cone) / ProgramOwner/NativeRouter | MilestoneRaw+IssueLedger; source_sha present；STALE_MILESTONE_EVIDENCE；REVIEW_OR_HOLD；`T5 final review or affected T3/T4 rework` |

各列來源為 SBL-04 原 SourceSHA 與原 line，已由 `sbl-tpm-sp/scripts/core.py::read_clause` 驗 SHA 讀回；完整座標逐列保存。這是 Stage draft 接線，不將 T4/T5 提案升為原 StateEnum。T5 必須讀 Raw；缺 Raw 只退受影 T3/T4，不阻斷其他 READY。原版 PM:T2 與 T4 的不同提案名稱已退出當期 Stage Reader。

### 2.3 PIPD 五個出口：每條分離，禁止用 PI/PD/ECP 串詞代替

| 出口 | Producer Input→原真能力→Output／Consumer | 受影 POS／NEG／Rollback |
|---|---|---|
| E1 `SOURCE/PROFILE→PI` | Goal＋SourceFamily ManifestSHA＋Profile nine-axis/Oracle→原 `pipd intake/profile/compile-pi` 和 PIPD DOC02 原 Writer→`PI-PKG/RequirementAtom` | POS strict schema＋SourceSHA 同 Subject；缺 Source、Profile veto、外欄或舊 Oracle alias NACK；不讓 Matt/OpenSpec Writer 簽 PI |
| E2 `PI→PD` | 真 PI＋RepoContext(root,HEAD,index,untracked,ACL)→原 `pipd bind-pd`→有界 PD-PKG＋WriteSet Candidate | POS exact Subject/HEAD/root；stale HEAD/`**`/path escape→只 PD HOLD，保留 PI |
| E3 `PD→DEV` | 原 PD＋preimage、exact files、Tests、Rollback→原 `pipd compile-ecp`/原 DEV Construction Owner→DEV ECP/ConstructionContract | POS 原 DEV Writer＋Original HGK Admission 才可 Repo Write；缺 WriteSet/Permit 禁 Apply；回原 preimage |
| E4 `PD→OPS/Host/User/Remote` | 原 PD＋HostTarget/PolicyEpoch/Effect/Compensation→原 `pipd compile-ecp`/OPS Writer→OPS ECP Proposal | POS 同 Host/Scope/Issuer；不能把 DEV Grant 轉成 Host/Remote Permit；UNKNOWN 經原 Receiver Reconcile |
| E5 `PD→PlannedTQAEP` | PD＋每 Atom 原 Oracle/ACC POS+NEG/CaseID→原 `pipd compile-tqaep`／DOC07→PlannedTQAEP | POS 原 Case/Oracle 可定位；未跑/同 Maker 並非 Checker PASS；回補受影 Case 而非重建全部 |

**遠端 main 此版 CLI 精確 13 命令**：`init, intake, profile, compile-pi, bind-pd, compile-ecp, compile-tqaep, validate, doctor, project, export, diff, repair`。`Agent_Workspace/PIPD` 本地 HEAD `995c7ad0c69a05a0c5cf6528155a62020ce31f87` 的實作另外具有 `compile-cc`，實測 COMMANDS=14；遠端 main `f6335a94157c61da75d92121d14c43feb413e981` 為13。兩者分版本保存，不把本地14當遠端已生效契約，也不把它隱藏成不存在。正式 Verb Parser 以 `PIPD-LS-SP/src/pipd_ls_sp/cli.py::COMMANDS` 為 Code Fact；`pipeline.intake()` 等已存在 Python 函式的參數仍要按該版呼叫，不由本文擅改函式簽章。[BODY02 `R2-02-CLI`；PIPD 原 CLI Source]

**原 19 Schema**：`ArtifactIdentity`, `AuthorityBinding`, `RequirementAtom`, `ProfileBinding`, `TechnologyAdmission`, `PI-PKG`, `PD-PKG`, `TraceLink`, `TaskSpecSeed`, `ConstructionContract`, `WorkOrderCandidate`, `ECP`, `TQAEP`, `ExecutionHandoff`, `EvidenceExpectation`, `ClaimCeiling`, `SurfaceProjectionManifest`, `GENIEProjectionRef`, `ExecutionBindingRef`。原 `$id` 以 `schemas/registry.json` 讀值，名稱並非憑本文件新產生的 Schema；`GENIEProjectionRef/ExecutionBindingRef` 的 seam-only 仍依原 Registry 限制。19 中每個只有 Syntax PASS 不等於 Domain Semantic PASS。[PIPD Registry／BODY02 `R2-02-CONTRACTS`]

**PIPD 原八個正式 Skill（四庫 `skills/` 目錄逐名核對）**：各別執行 `PACKAGED/INSTALLED/LOADED/INVOKED/QUALIFIED` 的原 Host Reader 驗證；這些名稱不授予原 Publisher/Permit 權。

| 原 PIPD Skill | Need／輸入→能力→候選輸出／原 Consumer | 原負例與降級 |
|---|---|---|
| `pipd-route-intake` | Goal/Source→合法 Intake、Need/SourceRef→原 PIPD `intake` | 缺 Source/Foreign Scope→`INTAKE_HOLD` |
| `pipd-authority-source` | SourceFamily／SHA→Authority Binding Reader→原 `freeze_authority`／PIPD Writer | 跨 Writer／失效 SHA→`AUTHORITY_HOLD` |
| `pipd-profile-tailor` | Product/Host/Context→Profile candidate／Veto→原 `profile` | 非受支援 Surface／Safety veto→`PROFILE_HOLD` |
| `pipd-pi-compile` | RequirementAtom／Source→`compile-pi`→PI-PKG | Unknown Oracle/Schema drift→`PI_HOLD` |
| `pipd-pd-bind` | PI＋Repo HEAD/index/ACL→`bind-pd`→PD-PKG | Stale HEAD／Root Escape→`PD_HOLD` |
| `pipd-execution-contract` | PD/EffectScope→原 `compile-ecp`→DEV/OPS ECP | 無 Exact WriteSet/Permit→`ADMISSION_HOLD` |
| `pipd-assurance-tqaep` | PD/Oracle→`compile-tqaep`→PlannedTQAEP | 沒有 Protected Checker 不得 `INDEPENDENT_PASS` |
| `pipd-package-project` | 原合法工件→`project/export/validate`→受限發行候選 | 打包不等於 SourceFreeze/Release |

**狀態**：八項未有當期真 Host 8/8 Effective Load/Trigger/Nontrigger 完整 Receipt，保持 `HOST_PENDING`；`.hermes/skills/openspec-*` 是另一套 OpenSpec 方法 Skill，**不得與八個正式 Skill 混同**。具體 Skill 命令、輸入須核其同 SHA `SKILL.md`。[PIPD Repository `skills/`；PIPD DOC02/06/07]


### 2.4 19 Canonical Schema 專用 Reader／Required／NEG（全部具名）
原 Domain `schemas/registry.json` 才是 `$id` 真值；本欄原文的 SourcePath、SchemaShape、Invariant/NEG 作原位 Adapter 接線要求，外部 Skill 不得發 Schema。
#### ArtifactIdentity
- **出處**：`BODY-02:61`；原 Canonical Contract `ArtifactIdentity`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ArtifactIdentity.schema.json；SHA `67d26f18d26307410bf0be5369949eb525d477e053ee3a7091e54b97f6d4ad4c`；`$id=urn:pipd:s0:ArtifactIdentity:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: all planes.
- required：subject_id, version, content_hash, schema_version, supersedes, invalidates。
- 專屬 Reader invariant：相同 canonical body 得相同 content_hash；supersedes/invalidates 指到舊版本且不能自指。
- Domain NEG：alter body but retain content_hash → `HASH_MISMATCH`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### AuthorityBinding
- **出處**：`BODY-02:101`；原 Canonical Contract `AuthorityBinding`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\AuthorityBinding.schema.json；SHA `66f1b3ce91d7f12ad6a6350a6628afd6c600e3e7ff62408b714c6fa0f1898ded`；`$id=urn:pipd:s0:AuthorityBinding:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: all compilers/adapters.
- required：source_id, authority_rank, locator, supersession, conflict_state, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：來源存在且 file SHA 符合；CURRENT 無 unresolved conflict 才可供 Compiler。
- Domain NEG：conflict_state=CONFLICT but promotion requested → `AUTHORITY_CONFLICT`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ClaimCeiling
- **出處**：`BODY-02:150`；原 Canonical Contract `ClaimCeiling`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ClaimCeiling.schema.json；SHA `dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85`；`$id=urn:pipd:s0:ClaimCeiling:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: all planes.
- required：allowed_claims, forbidden_escalation, close_conditions, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：allowed_claims需真證據階梯；forbidden_escalation與close_conditions有效。
- Domain NEG：AUTHOR_STATIC promoted to RELEASED → `CLAIM_ESCALATION`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ConstructionContract
- **出處**：`BODY-02:193`；原 Canonical Contract `ConstructionContract`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ConstructionContract.schema.json；SHA `1c56f15abd6e30d06f914f021b0b813f441689f9d47989ef48c7d7325557f0f2`；`$id=urn:pipd:s0:ConstructionContract:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: HGK adapter.
- required：subject, writable_scope, expected_changes, tests, rollback, evidence_expectations, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：writable_scope exact contained paths，expected_changes/tests/rollback 對同 preimage。
- Domain NEG：scope=** or path escapes root → `CC_SCOPE`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ECP
- **出處**：`BODY-02:245`；原 Canonical Contract `ECP`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ECP.schema.json；SHA `c58a8f3ed42808ba20f0102bb6fc7074d4fa321ea779879aa5ceefc6864d1de8`；`$id=urn:pipd:s0:ECP:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD/ECP semantics. Consumer: HGK/TQAEP.
- required：effect_intent, permission, retries, idempotency, readback, rollback, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：effect_intent/permission/retries/idempotency/readback/rollback按同scope；UNKNOWN不得重播。
- Domain NEG：DEV permission used for HOST_OP → `WRONG_EFFECT_GRANT`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### EvidenceExpectation
- **出處**：`BODY-02:297`；原 Canonical Contract `EvidenceExpectation`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\EvidenceExpectation.schema.json；SHA `02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f`；`$id=urn:pipd:s0:EvidenceExpectation:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD/TQAEP. Consumer: HGK/CI/provider.
- required：expected_evidence_type, producer, postcondition, freshness, claim_effect, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：expected_evidence_type/producer/postcondition/freshness/claim_effect只描述期待。
- Domain NEG：expected raw path promoted to observed receipt → `EXPECTED_IS_NOT_RAW`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ExecutionBindingRef
- **出處**：`BODY-02:346`；原 Canonical Contract `ExecutionBindingRef`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ExecutionBindingRef.schema.json；SHA `7c98cebfee30d9719cb8fd2d565c44120ce8d1be5b231071c19528cae1e95f50`；`$id=urn:pipd:s0:ExecutionBindingRef:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: HGK adapter. Consumer: HGK. Schema seam only until S5. Receiver binding id/version/hash/lease/state; ACK only after HGK admission.
- required：receiver_binding_id, receiver_binding_version, receiver_binding_hash, lease, state, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：receiver_binding_id/version/hash+lease/state同原HGK Reader；seam不取代Issuer。
- Domain NEG：foreign lease generation used to execute → `LEASE_FENCING_DENY`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ExecutionHandoff
- **出處**：`BODY-02:395`；原 Canonical Contract `ExecutionHandoff`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ExecutionHandoff.schema.json；SHA `7fa36d3e7fe6e7416111b975381a42f3f5ad46cc81d97b610f317548815bd77b`；`$id=urn:pipd:s0:ExecutionHandoff:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: HGK/other receiver.
- required：receiver, abi_version, payload_refs, ack_nack_state, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：receiver/abi_version/payload_refs真ACK payload hash與Consumer scope。
- Domain NEG：NACK or wrong receiver treated as ACK → `HANDOFF_NACK`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### GENIEProjectionRef
- **出處**：`BODY-02:441`；原 Canonical Contract `GENIEProjectionRef`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\GENIEProjectionRef.schema.json；SHA `22c88a0f9ec4ea4747967546f9a5ea7f19f0285be60ac42567fae2ca0b1c36ed`；`$id=urn:pipd:s0:GENIEProjectionRef:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: GENIE adapter. Consumer: GENIE compiler. Schema seam only until S6. Target references to ProductGraph, Profile, Bundle and GENIEArtifact; no truth writeback.
- required：target_refs, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：僅讀GENIE target_refs，保留SCHEMA_SEAM_ONLY；不成第二Writer。
- Domain NEG：projection creates native GENIE authority → `GENIE_WRITER_COLLISION`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### PD-PKG
- **出處**：`BODY-02:488`；原 Canonical Contract `PD-PKG`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\PD-PKG.schema.json；SHA `37291e8790e03839308a7c36125f9576d14da725a27480c9759ef5362d255541`；`$id=urn:pipd:s0:PD-PKG:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: execution handoff.
- required：RepoContext, currentness, late_bound_construction_binding, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：RepoContext 是當期真 root/HEAD/index/untracked，currentness 與晚綁 scope一致。
- Domain NEG：HEAD drift with old RepoContext → `PD_BIND_STALE`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### PI-PKG
- **出處**：`BODY-02:531`；原 Canonical Contract `PI-PKG`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\PI-PKG.schema.json；SHA `2a204aceba8d2764310a729c7c105301296e11d57d6c91f17bb8372214f793fe`；`$id=urn:pipd:s0:PI-PKG:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: PD binder.
- required：stable_semantic_contract, trace, acceptance, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：stable_semantic_contract 包含全部原原子 trace；Oracle canonical Writer相容。
- Domain NEG：sidecar appended as top-level _profile_meta → `PI_SCHEMA`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### ProfileBinding
- **出處**：`BODY-02:574`；原 Canonical Contract `ProfileBinding`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\ProfileBinding.schema.json；SHA `b559fb70bb6ceb9d491c989cb5ec031f44d15bcad5b40e75d6649aa059a93556`；`$id=urn:pipd:s0:ProfileBinding:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: Skills/JIT/HGK.
- required：profile, axes, vetoes, artifact_depth, assurance, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：九軸 strict enum、去重與 safety veto 只升級；十二軸另存 lossless bridge。
- Domain NEG：unknown axis or downgrade ASSURED → `PROFILE_VETO`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### RequirementAtom
- **出處**：`BODY-02:623`；原 Canonical Contract `RequirementAtom`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\RequirementAtom.schema.json；SHA `021f6a30cf178190281176138686447e492640cf97b125f9c21a0aa2fa31c684`；`$id=urn:pipd:s0:RequirementAtom:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: PI compiler/TQAEP.
- required：req_id, source_clause, owner, acceptance_cue, risk_guard, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：source_clause 實讀、owner 可識別、acceptance_cue 可反證、risk_guard 不空；保留否定作用域。
- Domain NEG：positive wording replaces source prohibition → `ATOM_POLARITY_LOSS`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### SurfaceProjectionManifest
- **出處**：`BODY-02:672`；原 Canonical Contract `SurfaceProjectionManifest`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\SurfaceProjectionManifest.schema.json；SHA `87f8057e8dac68f304ed4e9c2dd118a26c69428015769ab09d39398d34dcb57d`；`$id=urn:pipd:s0:SurfaceProjectionManifest:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: surface compiler.
- required：surface, source_hashes, generated_files, parity_loss, stale_rule, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：surface/source_hashes/generated_files/parity_loss/stale_rule可重算；loss不默丟。
- Domain NEG：stale source hash still projected as current → `PROJECTION_STALE`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### TaskSpecSeed
- **出處**：`BODY-02:721`；原 Canonical Contract `TaskSpecSeed`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\TaskSpecSeed.schema.json；SHA `c6e086aef0e4f21179cba52c5187c33a3873b18732c669c4d03bcad057e9b6cc`；`$id=urn:pipd:s0:TaskSpecSeed:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: receiver adapter.
- required：goal, inputs, outputs, constraints, dependencies, tests, rollback, evidence, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：goal→inputs→outputs→tests→rollback/evidence 可閉合且 dependencies 有具名輸出。
- Domain NEG：output has no consumer or test → `TASKSEED_INCOMPLETE`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### TechnologyAdmission
- **出處**：`BODY-02:779`；原 Canonical Contract `TechnologyAdmission`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\TechnologyAdmission.schema.json；SHA `40703552af4fb14c7aa87dd68ead6eac1cf7d272541fda273cf22b8fb109c4d6`；`$id=urn:pipd:s0:TechnologyAdmission:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: tool/provider adapters. Tightened from the untyped `{}` shape found in review: every field now carries a type and the source's 24-column design record (PKG-00 §9.2) is representable without additionalProperties loss.
- required：capability_need, candidate, disposition, pin_license_currentness, fallback_exit, subject_id, version, content_hash, schema_version, technology_id, external_name, capability_slot, license, immutable_pin。
- 專屬 Reader invariant：原 disposition 與17-state不默變；license+immutable_pin 真讀回，REJECT 不進 install。
- Domain NEG：REJECT candidate sent to installer → `TECH_ADMISSION_DENY`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### TQAEP
- **出處**：`BODY-02:843`；原 Canonical Contract `TQAEP`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\TQAEP.schema.json；SHA `d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd`；`$id=urn:pipd:s0:TQAEP:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD/TQAEP semantics. Consumer: Independent checker/release.
- required：tests, oracles, fixtures, acceptance, requalification, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：tests/oracles/fixtures/acceptance/requalification 逐atom對應；受保護receipt另讀。
- Domain NEG：PlannedTQAEP or Maker expected interpreted as actual verdict → `SELF_ACCEPTANCE_DENY`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### TraceLink
- **出處**：`BODY-02:892`；原 Canonical Contract `TraceLink`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\TraceLink.schema.json；SHA `ff6ef713b95a1a2812bd31d2b10cdcc064671c986d29d0e69318dc5a9f54e5e4`；`$id=urn:pipd:s0:TraceLink:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD/TQAEP. Consumer: validators/checkers.
- required：from_type, from_id, from_hash, to_type, to_id, to_hash, rationale, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：from_id/from_hash 與 to_id/to_hash 可在 bundle雙向解析；方向不交換。
- Domain NEG：to_hash names another candidate → `TRACE_HASH_MISMATCH`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

#### WorkOrderCandidate
- **出處**：`BODY-02:947`；原 Canonical Contract `WorkOrderCandidate`。
- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\WorkOrderCandidate.schema.json；SHA `03a8692f183f106ec7e4739b925c980ba07d68551627ca6af315fa9f9e2caf54`；`$id=urn:pipd:s0:WorkOrderCandidate:1`；schema dialect 2020-12；additionalProperties=false。
- Producer/Consumer：Owner: PIPD. Consumer: HGK admission. Candidate only; never runtime authority.
- required：candidate_only, subject_id, version, content_hash, schema_version。
- 專屬 Reader invariant：candidate_only=true；只送原HGK admission，不能直接 enqueue。
- Domain NEG：candidate_only=false → `CANDIDATE_NOT_AUTHORITY`；與 missing-required/unknown-key 的 schema拒收分開。
- roundtrip：原 Reader重序列化 payload，再讀回相同identity/trace；schema syntactic fixture通過不證明content_hash/Principal/License有效。
- **拒收**：本 Schema 專用 Reader 的 required/invariant/NEG 不符則僅停受影 Canonical Consumer；`jsonschema` syntax PASS 不能冒語義/Native PASS。

### 2.5 13 CLI 原 Verb 專屬操作及可重播失敗（全部具名）
每個 Verb 的合法 Flag/Parser 以原 PIPD `cli.py` 的 `COMMANDS`、同版本 `--help`/Tests 為準；此處載入原 BODY-02 的作用、輸入/輸出和負例，不產第14個命令。
#### pipd init
- **出處**：`BODY-02:989`；原 `pipd` Verb `pipd init`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`init --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd intake
- **出處**：`BODY-02:1014`；原 `pipd` Verb `pipd intake`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`intake --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd profile
- **出處**：`BODY-02:1044`；原 `pipd` Verb `pipd profile`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`profile --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd compile-pi
- **出處**：`BODY-02:1071`；原 `pipd` Verb `pipd compile-pi`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`compile-pi --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd bind-pd
- **出處**：`BODY-02:1101`；原 `pipd` Verb `pipd bind-pd`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`bind-pd --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd compile-ecp
- **出處**：`BODY-02:1129`；原 `pipd` Verb `pipd compile-ecp`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`compile-ecp --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd compile-tqaep
- **出處**：`BODY-02:1157`；原 `pipd` Verb `pipd compile-tqaep`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`compile-tqaep --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd validate
- **出處**：`BODY-02:1190`；原 `pipd` Verb `pipd validate`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`validate --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd doctor
- **出處**：`BODY-02:1217`；原 `pipd` Verb `pipd doctor`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`doctor --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd project
- **出處**：`BODY-02:1242`；原 `pipd` Verb `pipd project`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`project --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd export
- **出處**：`BODY-02:1273`；原 `pipd` Verb `pipd export`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`export --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd diff
- **出處**：`BODY-02:1304`；原 `pipd` Verb `pipd diff`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`diff --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。

#### pipd repair
- **出處**：`BODY-02:1332`；原 `pipd` Verb `pipd repair`。
- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：
- nonzero：`repair --definitely-invalid-flag` exit=2，typed stdout：
- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。
- **結果**：由原 CLI+Schema Reader 產同 Subject/Source/Scope 輸出；CLI Help/Dryrun 不等於 Native E2E。


## 本輪同域受影修復：plugin Stage 原合約與五出口

## 依 sbl-tpm-sp 實讀 SkillContract 的八階候選包（不冒正式 Canonical）

1. `pipd-route-intake`：Input 只接受非空 Goal + 至少一個不跳出 admitted root 的 source locator，輸出 content-addressed IntentCard。POS：可定位來源且按域產必要 atom；NEG：blank goal、空來源、`../` 立即 `INTAKE_INVALID/AUTHORITY_UNKNOWN`。
2. `pipd-authority-source`：每 family 的 SHA-256、file locator、Rank、supersession、conflict 必全部有據；本輪只造作者端 `SourceManifest`，未得原 Owner 正式 SourceFreeze，不能將物理 digest 擅升為正式 freeze。NEG：缺 SHA／跨 root／互斥來源 `AUTHORITY_UNKNOWN`。
3. `pipd-profile-tailor`：`LITE/STANDARD/ASSURED` 共九正交軸，safety veto 只升不降；provider-off parity 必須時由 LITE 升 STANDARD，超出 axis ceiling 依原合約升級；Profile T4/T5 `CR-DOC04-STATE-MAP` 仍 HOLD。
4. `pipd-pi-compile`：嚴格 Input 只有 intent/profile/atoms/goal；每 atom 必須有原 source_clause、owner、acceptance_cue、risk_guard；嚴禁 `_profile_meta` sidecar 偷塞 strict record。因未讀到真當期 Compiler Run，本輪提供 PI Proposal 和 atom TraceLink，不稱正式 `PI-PKG`。
5. `pipd-pd-bind`：必須本輪有真 RepoContext(root/head/tracked_files/currentness/writable_scope)，不接受 README 路徑當 repo root；沒有 Windows current HEAD/index/untracked 的時候 `REPO_CONTEXT_MISSING`，保留尚可用 SPEC/PI 設計。
6. `pipd-execution-contract`：DEV ConstructionContract/DEV ECP 與 OPS/USER/REMOTE/RELEASE 各自 permission/effect 不能混；exact WriteSet、preimage、expected changes/tests、at-most-once、readback residue、rollback pointer。原許可缺件只做 ECP design proposal，不 mint token。
7. `pipd-assurance-tqaep`：本輪為 `SBL.PlannedTQAEP@1`，每原 atom/case 有 POS/NEG、Oracle/fixture、raw expectation；真 `TQAEP` 的 `checker_execution_receipt` 必須是不同 principal、真正受保護 Reader 提供，禁止 SELF_ATTESTED。
8. `pipd-package-project`：完成文檔 hash、trace closure 和 EvidenceExpectation；本次最多 `AUTHOR_SIDE_STATIC_VALIDATED`，沒有 `LOCAL_QUALIFIED` 所需的原批准+Checker；正式 Claim Ladder 未越權。

**五個 PIPD 產物交付位置**：PI design 以 BODY-02 和 10B 的 original atom/trace；PD design 以 BODY-03/10B 的 repo late-binding contract；DEV ECP 以 BODY-03/10B 的 RepoWrite；OPS ECP 以 BODY-04/06/10B 的 Host effect；TQAEP design 以 BODY-07/10A 的 POS/NEG/Oracle/Fixture。五出口皆 `PROPOSED_WITH_EVIDENCE_GAP` 而非偽造的原 Runtime Record。


---



## R2 PI：正式 Reader 對齊候選／當前保守停點

**三 SPEC 真實受影內容**：ProductSPEC 的 persona=單人 Owner、JTBD=普通 Goal 自動導向產品、FUO=八 Kind 中各有 Host 可測首成果或 NoFit、ACC=原產品 Oracle、NEG=README-only；ArchitectureSPEC 固定唯一 SBL Product Owner、PIPD Writer、Fabric Policy、HGK Issuer、Hermes Executor、Independent Checker，拒絕第二控制平面；ProgramSPEC 從原 22 WP typed DAG 做最小適用子圖、Resume=同 subject/source/scope/epoch。

- `IntentCard@1` 正式入參 **僅** `goal,sources[].rel,constraints,non_goals`，不可進 `_profile_meta`；原 Source locator 取上傳指令，`source_sha256=835934a4397c9840de0d4c529f1800414f1c679ba797d61c67529060e1c5a8c7`。負例：空 Goal/缺 Source/traversal 優先 `INTAKE_INVALID/AUTHORITY_UNKNOWN`。
- `ProfileBinding` 以 `ASSURED` 的本次安全 veto 設計提案；九軸與 T4/T5 原 Owner StateMap 仍 `CR-DOC04-STATE-MAP`，不能自行把 Profile 名稱當原 Ratified State。
- `PI-PKG` 入參 `intent(subject_id,content_hash),profile=ASSURED,goal,atoms[]`，本輪實例逐 atom 帶 `req_id,source_clause,owner,acceptance_cue,risk_guard`；當期 `PI-PKG` 只有 historical schema shape validation，**未由 PIPD 原 CLI Writer compile**；無 `Writer ACK` 不提升正式 PI。
- `SourceFreezeManifest` 要正式 SourceFamilies／AuthorityBinding；本輪 SourceManifest SHA 及 offline `IntentCard` 不是正式 SourceFreeze。原 Reader 缺 epoch/OwnerDecision 就受影 `SOURCEFREEZE_HOLD`，不阻擋 L0 Draft。
- Schema 對齊素材在證據 ZIP `_machine/R2_OFFLINE_PIPD_CANDIDATES/` 中，逐條 positive/negative 在本章文字已固化；只做本地草稿，不以範例 JSON 當正式五出口。



## 本版未受影條文（完整沿用、當期生效）

## R2-02-HANDOFF：五個正式出口與候選隔離

SOURCE/PROFILE→PI：`pipd-route-intake` 只收 nonblank goal+contained sources；authority-source每family有file digest+locators，衝突拒freeze；profile-tailor九軸safety veto不得降級；pi-compile strict shape只有intent/profile/atoms/goal。POS原五REQ namespace可重播identity；NEG `_profile_meta` → schema NACK；project atom lossless sidecar不混入strict payload。

PI→PD：原pd-bind消費PI、真RepoContext與currentness。先read real root/HEAD/index/untracked/reparse/ACL，再late-bind exact writable scope；NEG stale HEAD或foreign subject→PD_BIND_NACK。沒有當期root evidence不得用README或歷史sha代用。

PD→DEV Construction/ECP：同subject的writable_scope/expected_changes/tests/rollback/evidence；exact preimage+原Issuer admission才可Repo effect。PD→OPS ECP：Host/User/Remote/Release分receiver/grant/nonce/TTL/epoch，不能套用DEV grant。POS分別對原Writer schema ACK；NEG ECP string當Permit→ADMISSION_DENIED。文稿僅候選，無真Compiler/Host ACK不得冒正式包。

TQAEP計畫→Checker：`SBL.PlannedTQAEP@1`保留per-atom POS/NEG/oracle/fixture，不提供live receipt。正式TQAEP/受保護check需不同credential及本輪Raw reader；Maker輸入receipt字串不能自簽。POS 真Reader查same candidate/Oracle/identity；NEG foreign receipt或same Maker→SELF_ACCEPTANCE_DENY。

DOC07 canonical Oracle↔legacy DOC03與十二風險軸→九context enum有語義落差；原Owner需提供alias/migration/loss ledger、roundtrip POS/NEG與Writer ACK。缺此只PI語義promotion及依賴ECP HOLD；不阻已合法admitted工作。

## R2-02-STAGE：K0–K3 與原18-stage投影

插件 corpus 24檔完整性重算PASS；K0原bytes/K1 clause index/K2相容提案/K3 bounded reader。歷史fixture不是live收據。T4/T5受CR-DOC04-STATE-MAP影響仍為formal HOLD，Draft SPEC可繼續。

| Stage | input→operation→output | Owner→Consumer | guard/first_fail/source |
|---|---|---|---|
| PM:T0 | ['goalcard', 'known_answer_refs', 'source_sha256'] → segregate facts from user guesses; detect unanswered JTBD → ProductKnownState@1(goal_sha,missing_questions) | ProductOwner → ProductOwner/PIPD Reader | GoalCard+known_answer_refs; source_sha present / KNOWN_ANSWER_REASK / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 510} |
| PM:T1 | ['persona', 'painledger', 'jtbd', 'source_sha256'] → rank questions by user information gain → QuestionPriority@1(qid,impact,source_ref) | ProductOwner → ProductOwner/PIPD Reader | Persona+PainLedger+JTBD; source_sha present / JTBD_UNBOUND / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 511} |
| PM:T2 | ['fuo', 'useroutcome', 'variants', 'source_sha256'] → define observable CLI/add,list,delete or brownfield user result → ProductSuccess@1(FUO,exit_code,negative_cases) | ProductOwner → ProductOwner/PIPD Reader | FUO+UserOutcome+variants; source_sha present / FUO_UNTESTABLE / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 512} |
| PM:T3 | ['productsuccess', 'primarykind', 'source_sha256'] → compile ProductSPEC draft and acceptance cues → ProductSPECDraft@1(journey_id,kind,acceptance_sha) | ProductOwner → ProductOwner/PIPD Reader | ProductSuccess+PrimaryKind; source_sha present / KIND_ID_DRIFT / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 513} |
| PM:T4 | ['productspecdraft', 'acc_neg', 'source_sha256'] → issue user-facing POS/NEG proposal, not Native verdict → ProductAcceptanceProposal@1(pos,neg,raw_expect) | ProductOwner → ProductOwner/PIPD Reader | ProductSPECDraft+ACC_NEG; source_sha present / ACC_NOT_BOUND / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 514} |
| PM:T5 | ['fuo_raw_refs', 'feedback', 'source_sha256'] → compare observable use vs claimed outcome; create repair request → ProductReviewRequest@1(gap,affected_journeys) | ProductOwner → ProductOwner/PIPD Reader | FUO_raw_refs+feedback; source_sha present / FUO_RAW_MISSING / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 515} |
| SE:T0 | ['repoboundaries', 'sourceindex', 'source_sha256'] → enumerate source/destination trust seams → SystemReadset@1(owners,sha,scope) | ArchitectureOwner → ArchitectureOwner/HostReader | RepoBoundaries+SourceIndex; source_sha present / SYSTEM_SOURCE_GAP / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 516} |
| SE:T1 | ['systemreadset', 'adrrefs', 'source_sha256'] → assign every seam to exactly one writer → OwnershipSeamMap@1(writer,reader,forbidden_effect) | ArchitectureOwner → ArchitectureOwner/HostReader | SystemReadset+ADRRefs; source_sha present / SEAM_OWNER_CONFLICT / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 517} |
| SE:T2 | ['riskinventory', 'hostcaps', 'source_sha256'] → trade off typed ABI and provider-off reliability → ADRSet@1(option,tradeoff,security_guard) | ArchitectureOwner → ArchitectureOwner/HostReader | RiskInventory+HostCaps; source_sha present / ARCHITECTURE_RISK_OPEN / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 518} |
| SE:T3 | ['adrset', 'c4', 'componentcards', 'source_sha256'] → bind schemas and compatibility version → ArchitectureSPEC@1(abi,compat,host_matrix) | ArchitectureOwner → ArchitectureOwner/HostReader | ADRSet+C4+ComponentCards; source_sha present / ABI_SCHEMA_MISMATCH / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 519} |
| SE:T4 | ['architecturespec', 'boundaryneg', 'source_sha256'] → test scope/token/provider-off/thin adapter semantics → ArchitectureNEGRequest@1(neg,oracle_source) | ArchitectureOwner → ArchitectureOwner/HostReader | ArchitectureSPEC+BoundaryNEG; source_sha present / PERMISSION_NEG_MISSING / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 520} |
| SE:T5 | ['nativerawrefs', 'integrationrisks', 'source_sha256'] → re-evaluate actual host ABI and raw results → ArchitectureReview@1(findings,repair_cone) | ArchitectureOwner → ArchitectureOwner/HostReader | NativeRawRefs+IntegrationRisks; source_sha present / HOST_RAW_MISSING / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 521} |
| TPgM:T0 | ['ownerroster', 'costtime', 'source_sha256'] → identify budget milestones without claiming approval → ProgramIntent@1(milestone,owner,risk) | ProgramOwner → ProgramOwner/NativeRouter | OwnerRoster+CostTime; source_sha present / MILESTONE_OWNER_MISSING / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 522} |
| TPgM:T1 | ['unknowndependencies', 'resourcecaps', 'source_sha256'] → record sequencing constraints and blocking decisions → SchedulingAssumptions@1(edges,confidence) | ProgramOwner → ProgramOwner/NativeRouter | UnknownDependencies+ResourceCaps; source_sha present / UNBOUNDED_WORK / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 523} |
| TPgM:T2 | ['ownergates', 'dependencyedges', 'source_sha256'] → toposort bounded DAG and cycle check → ProgramDAG@1(topo,locks,no_fit) | ProgramOwner → ProgramOwner/NativeRouter | OwnerGates+DependencyEdges; source_sha present / DAG_CYCLE / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 524} |
| TPgM:T3 | ['programdag', 'productspec', 'architecturespec', 'source_sha256'] → package work with traceable scope and approver → ProgramSPEC@1(wp,effort,owner,stop) | ProgramOwner → ProgramOwner/NativeRouter | ProgramDAG+ProductSPEC+ArchitectureSPEC; source_sha present / WP_SCOPE_UNKNOWN / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 525} |
| TPgM:T4 | ['pi_pd_refs', 'verifierreferral', 'source_sha256'] → route to correct Native ECP/Oracle Owner → HandoffReferral@1(expected_grants,oracle_conflict) | ProgramOwner → ProgramOwner/NativeRouter | PI_PD_refs+VerifierReferral; source_sha present / CR_ORACLE_001 / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 526} |
| TPgM:T5 | ['milestoneraw', 'issueledger', 'source_sha256'] → review schedule with evidence status; refreeze affected only → ProgramReview@1(blocked_waves,replan_cone) | ProgramOwner → ProgramOwner/NativeRouter | MilestoneRaw+IssueLedger; source_sha present / STALE_MILESTONE_EVIDENCE / {'source_id': 'SBL-04', 'sha256': 'ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0', 'line': 527} |

## R2-02-CLI：13 原 verb 的 parser 真讀回與額外 verb 衝突

當期 `C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/cli.py` SHA `6db0f828f0a445fcf3593b158c534d02a0a89f1e263746cabda8c043dd462cc9` 的 source module 已實跑 help/invalid parser；這是 SOURCE_MODULE_INVOKED，不是 installed binary Loaded Receipt。實作列14個verb，額外 compile-cc；原13保持獨立分母，額外verb為 `ABI_HOLD_CLI_13_14`，由PIPD CLI Owner決定版本相容/alias，不在本輪偷偷刪原需求或增第14條規範。

### pipd init

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd init [-h]

options:
  -h, --help  show this help message and exit
```

- nonzero：`init --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd intake

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd intake [-h] --goal GOAL [--source SOURCE]
                   [--constraint CONSTRAINT] [--non-goal NON_GOAL]

options:
  -h, --help            show this help message and exit
  --goal GOAL
  --source SOURCE
  --constraint CONSTRAINT
  --non-goal NON_GOAL
```

- nonzero：`intake --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd profile

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd profile [-h] [--profile PROFILE] [--axis AXIS]

options:
  -h, --help         show this help message and exit
  --profile PROFILE
  --axis AXIS
```

- nonzero：`profile --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd compile-pi

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd compile-pi [-h] --intent INTENT [--profile PROFILE] [--explain]
                       [--replay]

options:
  -h, --help         show this help message and exit
  --intent INTENT
  --profile PROFILE
  --explain
  --replay
```

- nonzero：`compile-pi --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd bind-pd

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd bind-pd [-h] --pi PI [--repo-root REPO_ROOT] [--head HEAD]

options:
  -h, --help            show this help message and exit
  --pi PI
  --repo-root REPO_ROOT
  --head HEAD
```

- nonzero：`bind-pd --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd compile-ecp

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd compile-ecp [-h] --pd PD --pi PI [--explain]

options:
  -h, --help  show this help message and exit
  --pd PD
  --pi PI
  --explain
```

- nonzero：`compile-ecp --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd compile-tqaep

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd compile-tqaep [-h] --pi PI --ecp ECP [--maker MAKER]
                          [--checker CHECKER]
                          [--checker-receipt CHECKER_RECEIPT] [--explain]

options:
  -h, --help            show this help message and exit
  --pi PI
  --ecp ECP
  --maker MAKER
  --checker CHECKER
  --checker-receipt CHECKER_RECEIPT
  --explain
```

- nonzero：`compile-tqaep --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd validate

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd validate [-h] --bundle BUNDLE [--explain]

options:
  -h, --help       show this help message and exit
  --bundle BUNDLE
  --explain
```

- nonzero：`validate --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd doctor

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd doctor [-h]

options:
  -h, --help  show this help message and exit
```

- nonzero：`doctor --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd project

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd project [-h] [--out OUT] [--root SUB_ROOT] [--dry-run]
                    [--allow-root ALLOW_ROOT] [--allow-replace]

options:
  -h, --help            show this help message and exit
  --out OUT
  --root SUB_ROOT
  --dry-run
  --allow-root ALLOW_ROOT
  --allow-replace
```

- nonzero：`project --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd export

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd export [-h] [--out OUT] [--dry-run] [--root SUB_ROOT]
                   [--allow-root ALLOW_ROOT] [--allow-replace]

options:
  -h, --help            show this help message and exit
  --out OUT
  --dry-run
  --root SUB_ROOT
  --allow-root ALLOW_ROOT
  --allow-replace
```

- nonzero：`export --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd diff

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：SOURCE_READ；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd diff [-h] --a A --b B [--explain]

options:
  -h, --help  show this help message and exit
  --a A
  --b B
  --explain
```

- nonzero：`diff --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

### pipd repair

- binaryOrigin：source module via Python311 `-B -m pipd_ls_sp.cli`；cwd 本任務 work；installed binary origin NOT_OBSERVED。
- effectScope：LOCAL_DRAFT_WRITE_CANDIDATE_ONLY; repair actual repo scope requires L2；此輪只 `--help` 和 invalid flag，不執行該verb效果。
- helpSchema（exit=0）：

```text
usage: pipd repair [-h] --subject SUBJECT [--authorized-root AUTHORIZED_ROOT]
                   [--scope SCOPE] [--maker MAKER] [--dry-run]

options:
  -h, --help            show this help message and exit
  --subject SUBJECT
  --authorized-root AUTHORIZED_ROOT
  --scope SCOPE
  --maker MAKER
  --dry-run
```

- nonzero：`repair --definitely-invalid-flag` exit=2，typed stdout：

```text
{
 "code": "USAGE_INVALID",
 "message": "invalid command line; see --help for the 13 commands",
 "verdict": "FAIL"
}
```

- 真實作用的POS/NEG與permission保留原下列契約；parser help成功不能聲稱compile/doctor功能已被本輪執行。

## STATIC-v1 真 Compiler、版本差異與不能提高的 Claim

已使用原 `sbl-tpm-sp` corpus Reader、三 SPEC draft adapters 與 receipt-free PlannedTQAEP Reader；24 個內建基礎 DOC 的 bytes/SHA 通過。插件 StageContracts 沒有 SETUP role 條目，故不虛構 SETUP Stage ACK；Host 狀態維持 HOST_PENDING。

`C:/Projects/Agent_Workspace/PIPD` 和 `C:/Projects/pipd-ls-sp` 的 pipeline/requirements/validate 實作 SHA 不同。已各以隔離副本執行原 Compiler：17 冊完整正文 input 在 intake 以 `ambiguous compound: explicit subjects and predicates required` NACK；另列的 22 WP 之 44 條身份／拒收有限投影可編譯 PI、隔離 fixture PD、ConstructionContract、DEV ECP，均保存原 Validator ACK。這 44 條不是全產品 PI，不能代替 2,221 原身份或完整語義子項。PD 的 root 僅是本輪測試副本，不是正式四庫或 live RepoContext。

原 `compile-ecp` 所編此 fixture 是 Repo/DEV effect，不能改名 OPS grant。既有未簽 OPS ECP 保留候選與原 Owner/Host/Effect binding 差額；未看到原 OPS Compiler/Receiver 的 ACK 不宣稱已綁。無 checker receipt 的 Canonical TQAEP 呼叫正確 NACK；規劃改用插件原 `SBL.PlannedTQAEP@1`，其 fixtures 明記 PLANNED_NOT_RUN，不填假收據。

版本化測試：另一個本地 PIPD 版本的 108 項既有靜態測試通過；Agent_Workspace 版本實際可用的 71 項測試有 1 項失敗：`test_oracle_compat.OracleCompat.test_cli_exact_set_preserved` 預期13、實際14。原測試與失敗均保留，不改 Oracle 或正式 Repo 令其變綠。受影 `compile-cc` 與 CLI Exact-set 契約差異由原 PIPD Owner 決定；其他已合法的來源／設計工作不等待此決定。
