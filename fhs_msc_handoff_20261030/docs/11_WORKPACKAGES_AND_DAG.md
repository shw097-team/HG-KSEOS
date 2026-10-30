<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 11 WORKPACKAGES AND DAG｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：r2 §9 22 WP typed DAG完整施工契約

## 9. 22 WorkPackages：保持原 Typed DAG、各 WP 的 Done／Resume／FirstFail

以下不是新的 22 個 Gate。僅按原 Dependency Closure 選可執行 WP；如欠原 Producer，受影 WP `PARK`，不對全部普通 Goal 加 SourceFreeze／Native Runner 要求。每 WP 保留原前置、Effect、真正交付、NEG、Rollback 和原 Consumer。[BODY11 `R2-11-GRAPH`]

<a id="current-ca2aa6fffcd9f6d184a5"></a>
### WP-FHS-00｜Source/Host Discovery
- **Producer → ABI/Schema → Consumer**：原 SourceReader/RepoProbe → `SourceManifest + RepoContext readback` → 原 TPM/PIPD Source Reader。
- **Input**：原來源根、四庫 HEAD/index/untracked、原檔 bytes；不輸入模型推測版本。
- **Output**：SourceManifest+RepoContext。
- **DAG dependency**：無前置卡；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`SOURCE_READ`；原唯讀 ACL/read scope。
- **WriteSet / LateBind**：唯讀原 admitted root；此工作不寫來源、不需要 Live Permit。
- **POS**：根路徑/HEAD/index/untracked/bytes SHA當期可讀。
- **NEG / FirstFail**：README或junction別名冒真root → `WP-FHS-00.FIRST_FAIL:ROOT_CURRENTNESS_NOT_PROVEN`。
- **Done**：根路徑/HEAD/index/untracked/bytes SHA當期可讀；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-00 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 TPM/PIPD Source Reader。
- **NoFit / Exit**：WP-FHS-00 的 WP-FHS-00.FIRST_FAIL:ROOT_CURRENTNESS_NOT_PROVEN 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：丟棄 WP-FHS-00 唯讀快照後重讀。
- **Resume**：重讀 WP-FHS-00 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-8a0c0dff28abe22a5e07"></a>
### WP-FHS-01｜Authority/Oracle/Profile
- **Producer → ABI/Schema → Consumer**：原 Authority/Profile Owner → `AuthorityBinding/ProfileBinding 原 19-schema Registry` → PIPD compile-pi。
- **Input**：SourceFamily SHA、Domain Owner、原 Oracle、九 context 軸與十二風險分數獨立 sidecar。
- **Output**：AuthorityConflictLedger+Oracle/ProfileBinding。
- **DAG dependency**：WP-FHS-00；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`SOURCE_READ`；原唯讀 ACL/read scope。
- **WriteSet / LateBind**：唯讀原 admitted root；此工作不寫來源、不需要 Live Permit。
- **POS**：原Authority/Oracle/Profile衝突被明列而未偷偷promotion。
- **NEG / FirstFail**：九enum直接當十二軸分數 → `WP-FHS-01.FIRST_FAIL:PROFILE_OR_ORACLE_BIND_HOLD`。
- **Done**：原Authority/Oracle/Profile衝突被明列而未偷偷promotion；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-01 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=PIPD compile-pi。
- **NoFit / Exit**：WP-FHS-01 的 WP-FHS-01.FIRST_FAIL:PROFILE_OR_ORACLE_BIND_HOLD 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：丟棄 WP-FHS-01 唯讀快照後重讀。
- **Resume**：重讀 WP-FHS-01 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-40f74d815d632b8cdceb"></a>
### WP-FHS-02｜Fabric Policy Consumer
- **Producer → ABI/Schema → Consumer**：Fabric Policy Owner → `FABRIC/fabric/consumers/hgk_policy_consumer.py 原 Consumer ABI` → HGK policy consumer。
- **Input**：真 policy epoch/SourceSHA、已批准 policy ref、Host target；先讀原 active/loaded/consumed 分開證據。
- **Output**：PolicyLoadedConsumerACK。
- **DAG dependency**：WP-FHS-01；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 HGK policy consumer 對 WP-FHS-02 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：Source/Stage/Approve/Active/Loaded/Consumer各自hash同scope。
- **NEG / FirstFail**：Stage文件冒Loaded ACK → `WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED`。
- **Done**：Source/Stage/Approve/Active/Loaded/Consumer各自hash同scope；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-02 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=HGK policy consumer。
- **NoFit / Exit**：WP-FHS-02 的 WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 Fabric Policy Owner 按 WP-FHS-02 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-02 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-792dbf8ac23d0fbe5a8a"></a>
### WP-FHS-03｜HGK Registry/Issuer
- **Producer → ABI/Schema → Consumer**：HGK 原 Registry/Resolver/Issuer → `原 HGK WorkOrder/ExecutionBinding/Permit ABI` → 原 HGK Receiver。
- **Input**：原受權 WorkID、Subject、Scope、PolicyEpoch、TTL、nonce；文件 ECP 不充 Permit。
- **Output**：IssuerReceiverBinding。
- **DAG dependency**：WP-FHS-01；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原 HGK Receiver 對 WP-FHS-03 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：原Receiver/Issuer registry同epoch與scope。
- **NEG / FirstFail**：候選ECP冒Permit → `WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID`。
- **Done**：原Receiver/Issuer registry同epoch與scope；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-03 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 HGK Receiver。
- **NoFit / Exit**：WP-FHS-03 的 WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 HGK 原 Registry/Resolver/Issuer 按 WP-FHS-03 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-03 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-fafdb583b5281b6eb182"></a>
### WP-FHS-04｜Hermes Durable Runtime
- **Producer → ABI/Schema → Consumer**：Hermes 原 runtime/journal Owner → `原 WorkID/Queue/Lease/Journal ABI` → 原 bounded Worker。
- **Input**：原 WorkID、queue item、lease generation、checkpoint；不建立新 queue 或 SQLite journal。
- **Output**：WakeLeaseRuntimeBinding。
- **DAG dependency**：WP-FHS-00；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原 bounded Worker 對 WP-FHS-04 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：原Journal/Wake/Lease schema及checkpoint可讀。
- **NEG / FirstFail**：新增第二Queue或舊generation commit → `WP-FHS-04.FIRST_FAIL:RUNTIME_LEASE_BINDING_DENY`。
- **Done**：原Journal/Wake/Lease schema及checkpoint可讀；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-04 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 bounded Worker。
- **NoFit / Exit**：WP-FHS-04 的 WP-FHS-04.FIRST_FAIL:RUNTIME_LEASE_BINDING_DENY 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 Hermes 原 runtime/journal Owner 按 WP-FHS-04 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-04 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-f2c90a133e3bfccb358e"></a>
### WP-FHS-05｜PIPD Native Compiler
- **Producer → ABI/Schema → Consumer**：PIPD 原 Intake/PI/PD/ECP Compiler → `PIPD schemas/registry.json 原 19 families` → HGK construction/OPS adapters。
- **Input**：三 SPEC、IntentCard、SourceFreeze、Profile、PI；PD 僅在真 RepoContext 晚綁。
- **Output**：PI/PD/DEV-OPS候選。
- **DAG dependency**：WP-FHS-01；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`LOCAL_DRAFT_WRITE`；明列隔離 output root 的使用者授權。
- **WriteSet / LateBind**：在本輪隔離 root 內先列 manifest exact relpath/preimage，新檔 preimage=ABSENT；不寫正式 Repo、Host 或 User store。
- **POS**：PI語義/PD scope/DEV-OPS分路與strict input一致。
- **NEG / FirstFail**：sidecar塞strict payload或expected當Raw → `WP-FHS-05.FIRST_FAIL:PIPD_FORMAL_PROMOTION_HOLD`。
- **Done**：PI語義/PD scope/DEV-OPS分路與strict input一致；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-05 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=HGK construction/OPS adapters。
- **NoFit / Exit**：WP-FHS-05 的 WP-FHS-05.FIRST_FAIL:PIPD_FORMAL_PROMOTION_HOLD 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：只撤本輪 WP-FHS-05 隔離候選、恢復 exact preimage；原來源不動。
- **Resume**：重讀 WP-FHS-05 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-9a936346d13548670c4f"></a>
### WP-FHS-06｜Legal First Reversible Slice
- **Producer → ABI/Schema → Consumer**：已受權 Codex bounded Writer → `ConstructionContract + DEV ECP + 原 HGK admission` → 原 Repo Reader/Checker。
- **Input**：exact RepoContext、preimage、WriteSet、測試入口、有效 DEV grant、需要的 capability qualification。
- **Output**：最小可逆Repo diff+Raw。
- **DAG dependency**：WP-FHS-02, WP-FHS-03, WP-FHS-04, WP-FHS-05, WP-FHS-17；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`REPO_WRITE`；DEV ECP + exact WriteSet + 原 HGK admission。
- **WriteSet / LateBind**：合法晚綁：由原 原 Repo Reader/Checker 對 WP-FHS-06 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：needed capability qualified後在exact Repo scope取得可逆diff/Raw。
- **NEG / FirstFail**：WP17尚未具能力就發首effect → `WP-FHS-06.FIRST_FAIL:FIRST_EFFECT_CAPABILITY_MISSING`。
- **Done**：needed capability qualified後在exact Repo scope取得可逆diff/Raw；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-06 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 Repo Reader/Checker。
- **NoFit / Exit**：WP-FHS-06 的 WP-FHS-06.FIRST_FAIL:FIRST_EFFECT_CAPABILITY_MISSING 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 已受權 Codex bounded Writer 按 WP-FHS-06 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-06 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-9922fca1cd4f9de82ae6"></a>
### WP-FHS-07｜Native PLAN Commander A/B/C
- **Producer → ABI/Schema → Consumer**：原 SBL TPM/Commander PLAN Reader → `PlanRevisionProposal + 原 PLAN CAS ABI` → 原 HGK PLAN Reader。
- **Input**：Goal/KnownAnswer、SourceSHA、三 SPEC、原 plan revision；A 只讀、B 隔離候選、C effect 分開。
- **Output**：PlanRevisionProposal+CAS ACK。
- **DAG dependency**：WP-FHS-01, WP-FHS-15；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`LOCAL_DRAFT_WRITE`；明列隔離 output root 的使用者授權。
- **WriteSet / LateBind**：在本輪隔離 root 內先列 manifest exact relpath/preimage，新檔 preimage=ABSENT；不寫正式 Repo、Host 或 User store。
- **POS**：A只讀/B隔離proposal使用原PLAN CAS Reader。
- **NEG / FirstFail**：要求先有同WO permit才能規劃或呼叫legacy SP → `WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION`。
- **Done**：A只讀/B隔離proposal使用原PLAN CAS Reader；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-07 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 HGK PLAN Reader。
- **NoFit / Exit**：WP-FHS-07 的 WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：只撤本輪 WP-FHS-07 隔離候選、恢復 exact preimage；原來源不動。
- **Resume**：重讀 WP-FHS-07 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-b6f8b2586e3982755d83"></a>
### WP-FHS-08｜FHS Execute Worker
- **Producer → ABI/Schema → Consumer**：原 Hermes Dispatcher + bounded Worker → `原 ExecutionBinding/lease fence/EffectRaw ABI` → 原 WorldRaw Collector。
- **Input**：同 WorkID/operation intent/nonce/lease、原 effect receiver；三 lane required/selected/served。
- **Output**：WorkerEffectRaw+JournalCursor。
- **DAG dependency**：WP-FHS-06, WP-FHS-07；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原 WorldRaw Collector 對 WP-FHS-08 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：已admitted WorkID單一lease以Worker真PID完成本operation。
- **NEG / FirstFail**：timeout同nonce盲replay → `WP-FHS-08.FIRST_FAIL:EFFECT_REPLAY_DENY`。
- **Done**：已admitted WorkID單一lease以Worker真PID完成本operation；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-08 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 WorldRaw Collector。
- **NoFit / Exit**：WP-FHS-08 的 WP-FHS-08.FIRST_FAIL:EFFECT_REPLAY_DENY 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Hermes Dispatcher + bounded Worker 按 WP-FHS-08 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-08 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-20f1a0506b20ef1a751d"></a>
### WP-FHS-09｜Challenge/Protected AO
- **Producer → ABI/Schema → Consumer**：原 WorldRaw Producer → `原 TQAEP/Protected Checker Request ABI` → 不同 Principal 的原 Protected Checker。
- **Input**：同 CandidateSHA/Subject/CaseID 的 WorldRaw、原 OracleSHA、Maker 與 Checker 權限分離。
- **Output**：ProtectedCheckerRequest/Receipt（需另一主體）。
- **DAG dependency**：WP-FHS-08, WP-FHS-21；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`SOURCE_READ`；原唯讀 ACL/read scope。
- **WriteSet / LateBind**：唯讀原 admitted root；此工作不寫來源、不需要 Live Permit。
- **POS**：真Raw與原Oracle交不同principal受保護Reader。
- **NEG / FirstFail**：Maker自簽PASS或借sibling verdict → `WP-FHS-09.FIRST_FAIL:SELF_ACCEPTANCE_DENY`。
- **Done**：真Raw與原Oracle交不同principal受保護Reader；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-09 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=不同 Principal 的原 Protected Checker。
- **NoFit / Exit**：WP-FHS-09 的 WP-FHS-09.FIRST_FAIL:SELF_ACCEPTANCE_DENY 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：丟棄 WP-FHS-09 唯讀快照後重讀。
- **Resume**：重讀 WP-FHS-09 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-67820a91ded6db92f652"></a>
### WP-FHS-10｜B1 3 GWO & G-A/G-B
- **Producer → ABI/Schema → Consumer**：Fabric/HGK/SBL 三個原 GWO Owner → `B1 原 PI27→PD31→TQAEP ABI` → 三 GWO 各自原 Receiver。
- **Input**：每個 GWO 各自 SourceSHA、Scope、Raw；G-A/G-B 不用單一 GWO 借證。
- **Output**：三GWO各自Raw+G-A/G-B。
- **DAG dependency**：WP-FHS-09, WP-FHS-20；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 三 GWO 各自原 Receiver 對 WP-FHS-10 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：Fabric/HGK/SBL三GWO各自effect與G-A/G-B證據。
- **NEG / FirstFail**：一個GWO冒其餘兩個 → `WP-FHS-10.FIRST_FAIL:GWO_EVIDENCE_JOIN_INCOMPLETE`。
- **Done**：Fabric/HGK/SBL三GWO各自effect與G-A/G-B證據；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-10 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=三 GWO 各自原 Receiver。
- **NoFit / Exit**：WP-FHS-10 的 WP-FHS-10.FIRST_FAIL:GWO_EVIDENCE_JOIN_INCOMPLETE 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 Fabric/HGK/SBL 三個原 GWO Owner 按 WP-FHS-10 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-10 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-ac915bfd9a557f283fe3"></a>
### WP-FHS-11｜Portable Host Dogfood
- **Producer → ABI/Schema → Consumer**：原 Portable SP packager/Host Loader → `原各 Host install/load/invoke/remove manifest` → 各 Host 原 Skill Reader。
- **Input**：TPM/Commander/Challenge 三 SP 本 Host pin、license、trigger/nontrigger；原八 PIPD skills 分開。
- **Output**：三SP逐Host loaded/invoked raw。
- **DAG dependency**：WP-FHS-05, WP-FHS-16；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 各 Host 原 Skill Reader 對 WP-FHS-11 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：每Portable SP的Host install/load/invoke/nontrigger/remove。
- **NEG / FirstFail**：一SP安裝receipt當三SP9/9 → `WP-FHS-11.FIRST_FAIL:HOST_SP_MATRIX_INCOMPLETE`。
- **Done**：每Portable SP的Host install/load/invoke/nontrigger/remove；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-11 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=各 Host 原 Skill Reader。
- **NoFit / Exit**：WP-FHS-11 的 WP-FHS-11.FIRST_FAIL:HOST_SP_MATRIX_INCOMPLETE 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Portable SP packager/Host Loader 按 WP-FHS-11 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-11 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-6fb690c7ea4579b87f48"></a>
### WP-FHS-12｜W18 Normal Mode
- **Producer → ABI/Schema → Consumer**：原 Hermes normal-entry Owner → `W18 ordinary Goal/E33–E42 原 ABI` → 原 normal Profile/ToolAutoSelect Reader。
- **Input**：fresh PID、普通 Goal、原 live Profile/ToolSelection、checkpoint；不要求 B1 長 Prompt。
- **Output**：新PID普通Goal E33-E42 Raw。
- **DAG dependency**：WP-FHS-10, WP-FHS-11；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原 normal Profile/ToolAutoSelect Reader 對 WP-FHS-12 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：新PID普通Goal正式Profile/ToolAutoSelect/真served且test-only移除。
- **NEG / FirstFail**：B1專用Prompt或test plugin充NormalMode → `WP-FHS-12.FIRST_FAIL:NORMAL_MODE_NOT_QUALIFIED`。
- **Done**：新PID普通Goal正式Profile/ToolAutoSelect/真served且test-only移除；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-12 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 normal Profile/ToolAutoSelect Reader。
- **NoFit / Exit**：WP-FHS-12 的 WP-FHS-12.FIRST_FAIL:NORMAL_MODE_NOT_QUALIFIED 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Hermes normal-entry Owner 按 WP-FHS-12 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-12 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-07844261d409ca68f150"></a>
### WP-FHS-13｜CAP On-Demand + HotSwap
- **Producer → ABI/Schema → Consumer**：原 TechnologyAdmission/Host capability Owner → `原 Need/Occupant/HotSwap admission ABI` → 原有 Consumer 與 Host Loader。
- **Input**：Need+Host+Scope+version、原 OriginalDisposition、舊/新 Occupant 的專屬 parity POS/NEG。
- **Output**：CAP gap/HotSwap parity+readback。
- **DAG dependency**：WP-FHS-16, WP-FHS-17；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原有 Consumer 與 Host Loader 對 WP-FHS-13 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：needed CAP走原route且替代Parity同原功能。
- **NEG / FirstFail**：熱替代Issuer或以選型當invoke → `WP-FHS-13.FIRST_FAIL:CAPABILITY_PARITY_NOT_PROVEN`。
- **Done**：needed CAP走原route且替代Parity同原功能；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-13 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原有 Consumer 與 Host Loader。
- **NoFit / Exit**：WP-FHS-13 的 WP-FHS-13.FIRST_FAIL:CAPABILITY_PARITY_NOT_PROVEN 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 TechnologyAdmission/Host capability Owner 按 WP-FHS-13 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-13 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-cac955aa4f4105285497"></a>
### WP-FHS-14｜Release/Retire Candidate
- **Producer → ABI/Schema → Consumer**：原 Publisher → `原 Release/Retire + GHP-02 ABI` → 原發行 channel Reader。
- **Input**：同 SubjectSHA 的供應鏈證據、Protected Checker、Publisher 權限；本輪無發布權。
- **Output**：ReleaseCandidate+原Publisher receipt。
- **DAG dependency**：WP-FHS-09, WP-FHS-19；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`RELEASE`；原 Publisher/GHP-02 + 受保護 Checker。
- **WriteSet / LateBind**：合法晚綁：由原 原發行 channel Reader 對 WP-FHS-14 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：供應鏈+受保護驗收+原Publisher/GHP-02實際readback。
- **NEG / FirstFail**：CI/作者檔案封裝冒Release → `WP-FHS-14.FIRST_FAIL:RELEASE_NOT_AUTHORIZED`。
- **Done**：供應鏈+受保護驗收+原Publisher/GHP-02實際readback；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-14 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原發行 channel Reader。
- **NoFit / Exit**：WP-FHS-14 的 WP-FHS-14.FIRST_FAIL:RELEASE_NOT_AUTHORIZED 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Publisher 按 WP-FHS-14 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-14 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-cfc168de89f17b4be6ef"></a>
### WP-FHS-15｜TPM Corpus & SPEC 18Stage


#### HANDOFF-v1 首工作有效接收契約

- **真功能與Input**：普通Goal、live KnownAnswer、內建24 DOC bytes/SHA → 原 corpus/QuestionLedger/三SPEC draft Reader；不是只保留ID/FirstFail。
- **Output**：原三SPECDraft、來源readback、FUO十欄；24功能Atom的原PI、TaskSpecSeed與PD晚綁契約已存在，PIPD Reader ACK可讀回。
- **合法起點／DAG**：WP00 source snapshot；WP01 source/profile author decision；WP15只依賴WP00既有讀入。WP05.prepare是原Compiler服務，消費已存在的設計SPEC，不等待WP15未來的Native完成Receipt。原22 WP edges不改，無bootstrap循環。
- **Producer→Schema→Consumer**：原 TPM `plan_spec`→Product/Architecture/ProgramSPECDraft→原PIPD `intake/compile_pi/validate_pi`→原TaskSpecSeed/ExecutionHandoff→HGK原adapter→原Hermes。
- **Effect／Scope／Admission**：SOURCE_READ + LOCAL_DRAFT；只在receiver-authorized root寫五個精確檔。此階段不索Live Permit。若後續需要Repo/Host/User/Remote/Release則各原ECP/Issuer在effect前准入，不能混用。
- **POS／NEG／Done**：24功能源句/24Atom、全部原trace與strict Reader PASS、三SPEC可讀且KnownAnswer零重問；空goal、source drift、foreign root、漏NEG/雙writer、cycle、stale PD/lease、ProviderOff外呼、UNKNOWN盲重送均受影拒收或Reconcile。只說明靜態接收，Native/Checker/Release仍NOT_RUN。
- **Evidence／Rollback／Resume**：`03_HANDOFF_EVIDENCE/MINIMAL_STATIC_TESTS.json`、真Compiler ACK與pure request constructor讀回；撤本WorkID草稿的exact preimage，不改來源；sameSource/key重用，source drift只失效受影錐，真effectUNKNOWN先原reconcile，沿原WorkID續行。
- **餘項分派**：全部7649量詞候選、485技術、282Runner/W18等產品義務留在原WP與適用驗收，未完成不在本輪灌PASS，也不成為此首工作的無關global HOLD。
- **Producer → ABI/Schema → Consumer**：原 TPM Corpus Reader/PM/SE/TPgM → `SBL 三 SPECDraft + source-bound Stage contracts` → 原 PIPD Intake。
- **Input**：SBL14/PIPD10 原 bytes/SHA、普通 Goal、KnownAnswer、18Stage 原來源；不重問已知答案。
- **Output**：三SPEC+18stage trace。
- **DAG dependency**：WP-FHS-00；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`LOCAL_DRAFT_WRITE`；明列隔離 output root 的使用者授權。
- **WriteSet / LateBind**：在本輪隔離 root 內先列 manifest exact relpath/preimage，新檔 preimage=ABSENT；不寫正式 Repo、Host 或 User store。
- **POS**：24 base docs真hash Reader與18 Stage三SPEC具來源。
- **NEG / FirstFail**：要求重新上傳內建DOC或T4/T5自升正式 → `WP-FHS-15.FIRST_FAIL:TPM_SOURCE_STAGE_GUARD`。
- **Done**：24 base docs真hash Reader與18 Stage三SPEC具來源；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-15 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 PIPD Intake。
- **NoFit / Exit**：WP-FHS-15 的 WP-FHS-15.FIRST_FAIL:TPM_SOURCE_STAGE_GUARD 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：只撤本輪 WP-FHS-15 隔離候選、恢復 exact preimage；原來源不動。
- **Resume**：重讀 WP-FHS-15 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-c693c72dcd7f9544c429"></a>
### WP-FHS-16｜Donor/Method Slot Translation
- **Producer → ABI/Schema → Consumer**：原 SBL DOC06 TechnologyAdmission Owner → `原 24 Donor Slot/25 Method Reader projection` → 原 TPM/PIPD/HGK 各受影 Consumer。
- **Input**：逐 Slot/Method 的 Need、原 SourceSHA、Input/Output、OriginalDisposition；方法不冒已安裝 binary。
- **Output**：24slot/25method壓製候選。
- **DAG dependency**：WP-FHS-00；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`LOCAL_DRAFT_WRITE`；明列隔離 output root 的使用者授權。
- **WriteSet / LateBind**：在本輪隔離 root 內先列 manifest exact relpath/preimage，新檔 preimage=ABSENT；不寫正式 Repo、Host 或 User store。
- **POS**：24槽/25方法依原disposition產特定輸出且方法不假installer。
- **NEG / FirstFail**：REFERENCE_ONLY自動安裝 → `WP-FHS-16.FIRST_FAIL:DONOR_METHOD_DISPOSITION_DENY`。
- **Done**：24槽/25方法依原disposition產特定輸出且方法不假installer；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-16 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 TPM/PIPD/HGK 各受影 Consumer。
- **NoFit / Exit**：WP-FHS-16 的 WP-FHS-16.FIRST_FAIL:DONOR_METHOD_DISPOSITION_DENY 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：只撤本輪 WP-FHS-16 隔離候選、恢復 exact preimage；原來源不動。
- **Resume**：重讀 WP-FHS-16 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-b8c0abdfb9dc52ea4f52"></a>
### WP-FHS-17｜CAP-BOOT Native Occupants
- **Producer → ABI/Schema → Consumer**：原 Host Installer + HGK 原 Issuer → `CAP-BOOT 原 Host admission + manifest ABI` → 原 Host capability Registry/Consumer。
- **Input**：已存在 Issuer 的最小合法 installer Scope、需要的 occupant pin/license、有效 OPS grant。
- **Output**：needed能力最小HostOccupant+loaded ACK。
- **DAG dependency**：WP-FHS-00, WP-FHS-02, WP-FHS-03；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 原 Host capability Registry/Consumer 對 WP-FHS-17 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：現有Issuer合法installer先建needed occupant再驗LoadedSHA。
- **NEG / FirstFail**：依WP06才准WP17形成循環 → `WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION`。
- **Done**：現有Issuer合法installer先建needed occupant再驗LoadedSHA；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-17 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 Host capability Registry/Consumer。
- **NoFit / Exit**：WP-FHS-17 的 WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Host Installer + HGK 原 Issuer 按 WP-FHS-17 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-17 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-469370ea8cc5896ad9a6"></a>
### WP-FHS-18｜FAR Bounded Repair & Incident
- **Producer → ABI/Schema → Consumer**：原 FAR/incident Reader + bounded Writer → `原 FirstFail/RepairCone + DEV ECP ABI` → 原 affected rechallenge/Checker。
- **Input**：真 FirstFail/repro、原 Oracle、最小依賴錐、budget、preimage、exact files；不改 Oracle 躲錯。
- **Output**：BoundedRepairDiff+RedGreen+residue。
- **DAG dependency**：WP-FHS-08；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`REPO_WRITE`；DEV ECP + exact WriteSet + 原 HGK admission。
- **WriteSet / LateBind**：合法晚綁：由原 原 affected rechallenge/Checker 對 WP-FHS-18 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：first_fail最小cone在原Oracle Red→Patch→Green且budget有界。
- **NEG / FirstFail**：擴scope/改Oracle或刪舊失敗Raw → `WP-FHS-18.FIRST_FAIL:REPAIR_SCOPE_DENY`。
- **Done**：first_fail最小cone在原Oracle Red→Patch→Green且budget有界；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-18 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 affected rechallenge/Checker。
- **NoFit / Exit**：WP-FHS-18 的 WP-FHS-18.FIRST_FAIL:REPAIR_SCOPE_DENY 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 FAR/incident Reader + bounded Writer 按 WP-FHS-18 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-18 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-8b3d82f9385832b1cd63"></a>
### WP-FHS-19｜CI/Supply Chain & Requal
- **Producer → ABI/Schema → Consumer**：原 CI/supply-chain Reader → `原 license/NOTICE/SBOM/dependency evidence ABI` → 原 release-readiness Reader。
- **Input**：同 CandidateSHA 的 license/NOTICE/SBOM/lock、實際命令/stdout/stderr/exit；不把存在當 PASS。
- **Output**：CI/License/NOTICE/SBOM掃描Raw。
- **DAG dependency**：WP-FHS-00；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`SOURCE_READ`；原唯讀 ACL/read scope。
- **WriteSet / LateBind**：唯讀原 admitted root；此工作不寫來源、不需要 Live Permit。
- **POS**：license/NOTICE/SBOM/dependency/secret輸出與同candidate可回算。
- **NEG / FirstFail**：未執行掃描以名字充通過 → `WP-FHS-19.FIRST_FAIL:SUPPLY_CHAIN_EVIDENCE_MISSING`。
- **Done**：license/NOTICE/SBOM/dependency/secret輸出與同candidate可回算；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-19 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 release-readiness Reader。
- **NoFit / Exit**：WP-FHS-19 的 WP-FHS-19.FIRST_FAIL:SUPPLY_CHAIN_EVIDENCE_MISSING 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：丟棄 WP-FHS-19 唯讀快照後重讀。
- **Resume**：重讀 WP-FHS-19 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-2e8fae00aa4535711041"></a>
### WP-FHS-20｜CLI/Agent/Host Kind Matrix
- **Producer → ABI/Schema → Consumer**：原 Product/Host matrix Owner → `原八 Kind×三 Mode×四 Host×Provider token Cell ABI` → 每個原 Cell 的原 Host Reader。
- **Input**：192 原 CellID/Host/raw ON-OFF、明確 NoFit、該 Cell own Raw；DeepSeek48 原身份不改。
- **Output**：192Cell適用/NoFit/Host Raw。
- **DAG dependency**：WP-FHS-05, WP-FHS-16；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。
- **WriteSet / LateBind**：合法晚綁：由原 每個原 Cell 的原 Host Reader 對 WP-FHS-20 的具名 target root/Host/operation 解析 canonical path/object identity、拒 alias/junction/traversal，列有限 exact WriteSet 與 preimage SHA；空集合或未簽 Scope 不准 effect。原 Owner/Issuer 綁 principal、epoch、TTL、nonce；文件中不預填任意實體路徑。
- **POS**：192組合每Host/Mode/Provider具本cell Raw或明確NoFit。
- **NEG / FirstFail**：Hermes Raw借Claude/DeepSeek → `WP-FHS-20.FIRST_FAIL:HOST_CELL_EVIDENCE_FOREIGN`。
- **Done**：192組合每Host/Mode/Provider具本cell Raw或明確NoFit；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-20 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=每個原 Cell 的原 Host Reader。
- **NoFit / Exit**：WP-FHS-20 的 WP-FHS-20.FIRST_FAIL:HOST_CELL_EVIDENCE_FOREIGN 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：由原 原 Product/Host matrix Owner 按 WP-FHS-20 原 receiver inverse/compensation 恢復 exact preimage；UNKNOWN 先 reconcile，保留原 journal/residue，不 reset 他人變更。
- **Resume**：重讀 WP-FHS-20 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。

<a id="current-0b6e1234bbb3bb59bb79"></a>
### WP-FHS-21｜Challenge 96/H4/SEAM Coverage
- **Producer → ABI/Schema → Consumer**：原 Acceptance/Oracle Owner → `原 AC15/Oracle96/H4/SEAM Reader ABI` → 原 Protected AO Request Reader。
- **Input**：每 Case 原 Oracle 類型、calibration、POS/NEG fixtures、Raw schema；計畫不冒實跑。
- **Output**：96Cell/H4/SEAM原Oracle計畫。
- **DAG dependency**：WP-FHS-01；依賴原服務，不創第二 Scheduler。
- **EffectClass / Admission**：`SOURCE_READ`；原唯讀 ACL/read scope。
- **WriteSet / LateBind**：唯讀原 admitted root；此工作不寫來源、不需要 Live Permit。
- **POS**：96cell及H4/SEAM按原predicate/校準逐格Reader可判。
- **NEG / FirstFail**：同一generic fixture聲稱全部已實測 → `WP-FHS-21.FIRST_FAIL:ORACLE_CELL_NOT_PROVEN`。
- **Done**：96cell及H4/SEAM按原predicate/校準逐格Reader可判；同 Subject/SourceSHA/operation 證據由原 Consumer 讀回；沒有 Raw 記 NOT_RUN。
- **EvidenceExpectation**：同 WP-FHS-21 original operation 的 command/environment/exit/stdout/stderr 或原 Host WorldRaw；freshness=same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch；Reader=原 Protected AO Request Reader。
- **NoFit / Exit**：WP-FHS-21 的 WP-FHS-21.FIRST_FAIL:ORACLE_CELL_NOT_PROVEN 只停本卡 effect 與依賴錐；既有 READ_ONLY/LOCAL_DRAFT READY 繼續。
- **Rollback**：丟棄 WP-FHS-21 唯讀快照後重讀。
- **Resume**：重讀 WP-FHS-21 的 SourceSHA/HEAD/index/checkpoint 與依賴 ACK；已完成且同 key 不重播；UNKNOWN effect 只進原 Reconcile，變更只 invalidate 本卡受影下游。
