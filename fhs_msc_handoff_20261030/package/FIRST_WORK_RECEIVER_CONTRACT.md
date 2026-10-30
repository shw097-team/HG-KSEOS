# 首工作原接收面契約｜WP-FHS-15

輸入為普通Goal、KnownAnswer、已釘SHA的24 DOC與該首工作SourceAuthority/Profile；輸出是三SPEC、來源readback與FUO十欄、功能PI、TaskSpecSeed/ExecutionHandoff。已生成全部實例，請直接讀`02_FIRST_WORK`。

| 連接 | 真 Producer／ABI／Consumer | 接收及退出條件 |
|---|---|---|
| Goal→SPEC | 原 TPM corpus/QuestionLedger/plan_spec → 三 SPECDraft → PIPD intake | empty goal/缺 source/來源漂移/缺專屬NEG拒收；已有同key答案零重問；僅失效受影輸出 |
| Source/Profile→PI | 原 freeze_authority/profile_record/compile_pi → 原 19-schema PI-PKG/RequirementAtom/TraceLink → validate_pi | 24功能Atom全成員Reader PASS；sidecar不塞strict record；source或atom/trace漂移NACK |
| PI→TaskSpecSeed | 原 PIPD record factory → TaskSpecSeed/ExecutionHandoff → 原 HGK adapter | 不建立Native identity；候選只有接收用途，WorkOrderCandidate固定candidate_only |
| PI→PD | 原 pipeline.bind_pd → 原 PD-PKG → 原施工接收端 | root/HEAD/index/untracked/ACL/有限WriteSet於Receiver真正施工前再測；缺root/stale/**拒收；不預填live PD |
| TaskSpec→Canonical WO | 原 native_admission pure request constructors → 原 SharedSpine.create_taskspec/create_workorder | 純constructor靜態接收已測；原HGK配置實際IDs與frozen Requirement並受保護准入；本輪不呼叫Canonical mutation |
| WO→Hermes | 原Canonical WorkID關聯原Hermes task_id → 原Queue/claim/get_task/Journal | sameWorkID/operation key續工；舊lease先拒；不是從fixture或candidate取真WorkID |
| effect→Delivery | 原boundedWorker→原WorldReadback/Reconcile→ProtectedChecker→原Delivery/Publisher | DEV/OPS/USER/REMOTE/RELEASE各自原准入；UNKNOWN不重送；作者static PASS不是Independent或Release |

五個精確輸出名為ProductSPEC.json、ArchitectureSPEC.json、ProgramSPEC.json、SourceReadback.json、FUO.json。Receiver在受權isolated root下解析exact paths與preimage，Path逃逸/alias或他人檔案拒收；rollback只恢復本工作草稿。若尚無Canonical原生授權，source/draft仍可在已授本地範圍完成，Canonical提交與Native effect停在各原Receiver門前。這個分流避免Bootstrap反轉而沒有削弱原Issuer。

機器可讀的函式簽章、各Owner/Reader、第一失敗與resume條件見PD晚綁契約及差額表；純request fixture使用STATIC-TEST IDs，不是實際TaskSpec/WorkOrder。
