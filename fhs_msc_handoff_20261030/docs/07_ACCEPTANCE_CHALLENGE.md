<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 07 ACCEPTANCE CHALLENGE｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：r2 §8 AC15／96 Oracle 真 Consumer

## 8. Acceptance Challenge 15 異構 Edge 與 96 原 Oracle：每邊各自資料形狀

各 Edge 的 `Input Payload/Required Field→Transform/Typed Output→Original Receiver`、POS/NEG、權限、Resume **不得與另一邊互借**；Portable `challenge-review` 只可製造 Advisory Finding，Checker Verdict 必須由不同 Principal 的原 Protected AO 簽發。96 Oracle 每個 ID 保存本 Case Class 專用判準；若原 Oracle 還是設計候選，不能以外部 Review 構造 Native PASS。[BODY07 R2-07-AC/C39]

### 8.1 AC-E01～E15 原 Handoff

<a id="current-4a23c9cff2bdc7bee39e"></a>
#### AC-E01｜OWNER/TPM → TPM Intake
- **來源**：`BODY-07:25`
- trigger/input：當此邊的上游產物ready，接收GoalIntake；required=goal, source_locators, known_answers。
- transform/output：goal非空且source locator在admitted root → IntentCardProposal；只有TPM Intake可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：LOCAL_DRAFT_WRITE；隔離SPEC目錄授權。
- POS：goal非空且source locator在admitted root。NEG：blank goal / path traversal → INTAKE_INVALID。
- rollback/exit/resume：撤本輪Intent候選，不改source；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L666；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-858e97d2c14971547d67"></a>
#### AC-E02｜SBL TPM → 原PIPD Intake
- **來源**：`BODY-07:34`
- trigger/input：當此邊的上游產物ready，接收ThreeSpecHandoff；required=product_spec, architecture_spec, program_spec, source_manifest_sha。
- transform/output：三SPEC各有ACC/NEG/來源與non-goals → PIPDIntakeRequest；只有原PIPD Intake可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：LOCAL_DRAFT_WRITE；原PIPD候選輸出scope。
- POS：三SPEC各有ACC/NEG/來源與non-goals。NEG：用TPM敘事冒canonical PI → CANONICAL_WRITER_COLLISION。
- rollback/exit/resume：丟候選；回原SPEC補缺；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L667；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-b59869ab82405c749088"></a>
#### AC-E03｜原Source/Profile Writer → 原PIPD DOC02 Writer
- **來源**：`BODY-07:43`
- trigger/input：當此邊的上游產物ready，接收PICompileRequest；required=intent, profile, atoms, goal。
- transform/output：strict shape/source/Oracle相容才編譯 → PI-PKG；只有原PIPD DOC02 Writer可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：LOCAL_DRAFT_WRITE；原Canonical Writer，不含Issuer權。
- POS：strict shape/source/Oracle相容才編譯。NEG：unknown _profile_meta/錯Oracle alias → PI_SCHEMA_OR_ORACLE_HOLD。
- rollback/exit/resume：保留sidecar；只PI promotion HOLD；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L668；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-5babf418542ab68f5c8e"></a>
#### AC-E04｜原PIPD DOC02 → 原PIPD DOC03 Binder
- **來源**：`BODY-07:52`
- trigger/input：當此邊的上游產物ready，接收PDBindRequest；required=pi_ref, repo_context, head, scope。
- transform/output：real root/HEAD/index/untracked fresh且scope contained → PD-PKG；只有原PIPD DOC03 Binder可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：LOCAL_DRAFT_WRITE；真root唯讀/候選output scope。
- POS：real root/HEAD/index/untracked fresh且scope contained。NEG：stale HEAD或 ** WriteSet → PD_BIND_NACK。
- rollback/exit/resume：丟過期PD候選重讀root；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L669；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-9f605c6cd8c641ba2ed7"></a>
#### AC-E05｜原PD Writer → 原DOC05 ECP/DOC07 TQAEP
- **來源**：`BODY-07:61`
- trigger/input：當此邊的上游產物ready，接收ExecutionPlanSplit；required=pd_ref, dev_scope, ops_scope, case_oracles。
- transform/output：DEV/OPS分路且cases逐原子POS/NEG → DEV/OPS ECP + PlannedTQAEP；只有原DOC05 ECP/DOC07 TQAEP可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：LOCAL_DRAFT_WRITE；原Compiler候選權，不授world effect。
- POS：DEV/OPS分路且cases逐原子POS/NEG。NEG：PlannedTQAEP自稱Independent PASS → PLANNED_IS_NOT_ACCEPTED。
- rollback/exit/resume：撤分路候選，不碰既有permit；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L670；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-83665f46d4a6206738e9"></a>
#### AC-E06｜原PIPD ECP/Admission → 原HGK Issuer
- **來源**：`BODY-07:70`
- trigger/input：當此邊的上游產物ready，接收AdmissionRequest；required=ecp_ref, subject, effect_class, scope, policy_epoch, receiver_binding。
- transform/output：LoadedPolicy/epoch/scope/TTL與原Issuer簽核一致 → AdmittedWorkOrder/Permit；只有原HGK Issuer可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：HOST_OP；原Issuer/OPS-DEV有效准入。
- POS：LoadedPolicy/epoch/scope/TTL與原Issuer簽核一致。NEG：ECP文字當Permit或DEV grant作Host → ADMISSION_DENIED。
- rollback/exit/resume：原Issuer撤受影permit；unknown先reconcile；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L671；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-a7402f58c13ba759576c"></a>
#### AC-E07｜原HGK Admission → 原Hermes SharedSpine
- **來源**：`BODY-07:79`
- trigger/input：當此邊的上游產物ready，接收LeaseCAS；required=admitted_work_id, expected_revision, lease_generation, worker_id。
- transform/output：同WorkID只有一個generation有效claim → LeaseClaimACK；只有原Hermes SharedSpine可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：HOST_OP；原Queue Writer/CAS binding。
- POS：同WorkID只有一個generation有效claim。NEG：雙Worker用同舊revision claim → LEASE_FENCING_DENY。
- rollback/exit/resume：只釋放本worker合法lease；不刪queue；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L672；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-bf56829cd4e21da4c589"></a>
#### AC-E08｜原Hermes Worker → 原World Effect Receiver
- **來源**：`BODY-07:88`
- trigger/input：當此邊的上游產物ready，接收EffectInvocation；required=operation_id, permit_ref, nonce, preimage, expected_postcondition。
- transform/output：effect intent先Journal，世界post讀回同operation → WorldRawReadback；只有原World Effect Receiver可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：REPO_OR_NATIVE_BY_ADMITTED_ECP；exact DEV/OPS scope/nonce/TTL。
- POS：effect intent先Journal，世界post讀回同operation。NEG：unknown timeout同nonce重播 → EFFECT_REPLAY_DENY。
- rollback/exit/resume：reconcile→補償ECP/residue；不盲retry；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L673；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-cbdb3641a286c0b3492a"></a>
#### AC-E09｜原World Raw Reader → 原Frozen Readset Reader
- **來源**：`BODY-07:97`
- trigger/input：當此邊的上游產物ready，接收RawFreeze；required=raw_refs, raw_hashes, candidate_sha, source_sha。
- transform/output：Raw bytes/hash與同candidate可重算 → FrozenReadsetManifest；只有原Frozen Readset Reader可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：SOURCE_READ；合法Raw read ACL。
- POS：Raw bytes/hash與同candidate可重算。NEG：跨Host/過期candidate raw → RAW_SUBJECT_MISMATCH。
- rollback/exit/resume：丟快照重讀；不擦原Raw；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L674；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-c720889a6f553104b23e"></a>
#### AC-E10｜Frozen Reader → SBL External Challenge
- **來源**：`BODY-07:106`
- trigger/input：當此邊的上游產物ready，接收ChallengeRead；required=frozen_readset, candidate_sha, evidence_sha, review_scope。
- transform/output：固定SHA唯讀逐claim反證，無原檔mutation → AdvisoryFindings；只有SBL External Challenge可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：SOURCE_READ；A READONLY readset scope。
- POS：固定SHA唯讀逐claim反證，無原檔mutation。NEG：Reviewer修改subject或moving branch → FROZEN_SUBJECT_DRIFT。
- rollback/exit/resume：停止受影review；重新freeze新candidate；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L675；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-82a31cb4226dc78f0388"></a>
#### AC-E11｜SBL Challenge Advisory → 原HGK AO Receiver
- **來源**：`BODY-07:115`
- trigger/input：當此邊的上游產物ready，接收AOInboxSubmit；required=finding_refs, source_sha, candidate_sha, inbox_binding, effect_scope。
- transform/output：僅C有真inbox ACL/ECP與payload hash ACK → AOInboxACK；只有原HGK AO Receiver可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：HOST_OP；A READONLY；B隔離advisory；C CHECKER_INBOX_EFFECT需原OPS。
- POS：僅C有真inbox ACL/ECP與payload hash ACK。NEG：用A/B只讀權直接寫protected inbox → CHECKER_INBOX_PERMISSION_DENY。
- rollback/exit/resume：原Receiver撤受影message或補償；保留原finding；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L676；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-f8a2f08cdbf3cf7d0b3d"></a>
#### AC-E12｜原AO Receiver ACK → 原Protected Checker
- **來源**：`BODY-07:124`
- trigger/input：當此邊的上游產物ready，接收ProtectedCheckerRun；required=checker_request, oracle_refs, actual_raw_refs, maker_principal, checker_binding。
- transform/output：原Checker讀Raw執Oracle；signature可由protected Reader驗 → ProtectedVerdictReceipt；只有原Protected Checker可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：PROTECTED_CHECKER_EFFECT；真不同credential＋原Checker權。
- POS：原Checker讀Raw執Oracle；signature可由protected Reader驗。NEG：LeaseCAS object冒verdict或Maker自簽 → NACK_WRONG_DOMAIN_SCHEMA/SELF_ACCEPTANCE_DENY。
- rollback/exit/resume：保留原Raw，原Checker出invalidated/supersedes receipt；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L677；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-3cbd3f6fef786c550224"></a>
#### AC-E13｜Protected AO Checker → 原HGK Reducer
- **來源**：`BODY-07:133`
- trigger/input：當此邊的上游產物ready，接收VerdictReduce；required=protected_verdict_ref, signature_ref, expected_revision, subject。
- transform/output：有效signature/Oracle/candidate與CAS同revision → ReducedStateACK；只有原HGK Reducer可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：HOST_OP；原Reducer Writer＋Checker驗簽。
- POS：有效signature/Oracle/candidate與CAS同revision。NEG：advisory字串PASS當protected verdict → VERDICT_AUTHORITY_DENY。
- rollback/exit/resume：原Reducer合法逆轉/新事件；原journal保留；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L678；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-c891a64a005eee60d8a8"></a>
#### AC-E14｜原Reducer/Native Commander → 原Maker/Authorized Dev
- **來源**：`BODY-07:142`
- trigger/input：當此邊的上游產物ready，接收RepairConeDispatch；required=first_fail, affected_paths, preimage_sha, budget, ecp_ref。
- transform/output：原Oracle下RED→bounded patch→GREEN與新candidate → NewCandidate+RedGreenRaw；只有原Maker/Authorized Dev可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：REPO_WRITE；L2 DEV ECP/exact cone。
- POS：原Oracle下RED→bounded patch→GREEN與新candidate。NEG：改Oracle/擴WriteSet/覆蓋舊Evidence → REPAIR_SCOPE_DENY。
- rollback/exit/resume：原preimage inverse patch；residue與版本留存；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L679；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

<a id="current-8f9d0bcfa3d7eba4d0c5"></a>
#### AC-E15｜Closed B1 Evidence → 原W18 NormalMode Owner
- **來源**：`BODY-07:151`
- trigger/input：當此邊的上游產物ready，接收NormalModeQualification；required=b1_evidence_refs, fresh_pid, default_profile_sha, ordinary_goal, test_only_removed。
- transform/output：新PID零B1長Prompt且正式profile自動路由/真served → NM01-03/E33-E42 Raw；只有原W18 NormalMode Owner可出ACK(payload_hash,consumer_identity,原schema_version)；NACK含first_fail/affected_scope/resume。
- effect/permission：HOST_OP；原Host OPS/User scope；不是Release。
- POS：新PID零B1長Prompt且正式profile自動路由/真served。NEG：test-only profile或手選lane冒常態 → NORMAL_MODE_NOT_QUALIFIED。
- rollback/exit/resume：原Host restore profile；B1收據保留，不重播effect；缺原schema或Receiver就只此邊ABI_BIND_HOLD；原Owner讀回binding後再准入。
- source：SRC-L-001:L680；SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。

### 8.2 96 個原異構 Oracle 專屬處理
<a id="current-31d3fe0a459635a2b9a7"></a>
#### AC-C39-POS-DETERMINISTIC

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；observed_value改成非expected
- **Source** `BODY-07:165`，原 Oracle `AC-C39-POS-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L445，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/DETERMINISTIC` | `SBL DOC08:L392` 原規則 `L3855 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `feature_invoked and acceptance_predicate_declared && DETERMINISTIC_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/pos/deterministic := __CORRUPT__001` → `MISSING_POS_FUNCTION`；`AC-C39-POS-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-e77dbba046a6d1fbf9ca"></a>
#### AC-C39-POS-STATE_READBACK

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:207`，原 Oracle `AC-C39-POS-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L446，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/STATE_READBACK` | `SBL DOC08:L393` 原規則 `L3856 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `feature_invoked and acceptance_predicate_declared && STATE_READBACK_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/pos/state_readback := __CORRUPT__002` → `MISSING_POS_FUNCTION`；`AC-C39-POS-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-e0d22b42b7745d813e2f"></a>
#### AC-C39-POS-PROPERTY

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；至少一generated case破invariant
- **Source** `BODY-07:266`，原 Oracle `AC-C39-POS-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L447，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/PROPERTY` | `SBL DOC08:L394` 原規則 `L3857 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `feature_invoked and acceptance_predicate_declared && PROPERTY_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/pos/property := __CORRUPT__003` → `MISSING_POS_FUNCTION`；`AC-C39-POS-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-b3ee8f105da2172ad180"></a>
#### AC-C39-POS-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；更換reference或輸出差異
- **Source** `BODY-07:318`，原 Oracle `AC-C39-POS-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L448，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/REFERENCE_OUTPUT` | `SBL DOC08:L395` 原規則 `L3858 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `feature_invoked and acceptance_predicate_declared && REFERENCE_OUTPUT_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/pos/reference_output := __CORRUPT__004` → `MISSING_POS_FUNCTION`；`AC-C39-POS-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-fface0c568ee8a252f63"></a>
#### AC-C39-POS-STATISTICAL

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:372`，原 Oracle `AC-C39-POS-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L449，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/STATISTICAL` | `SBL DOC08:L396` 原規則 `L3859 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `feature_invoked and acceptance_predicate_declared && STATISTICAL_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/pos/statistical := __CORRUPT__005` → `MISSING_POS_FUNCTION`；`AC-C39-POS-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-694cef4f7a19e3d184d6"></a>
#### AC-C39-POS-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:418`，原 Oracle `AC-C39-POS-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L450，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/SEMANTIC_JUDGE` | `SBL DOC08:L397` 原規則 `L3860 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `feature_invoked and acceptance_predicate_declared && SEMANTIC_JUDGE_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/pos/semantic_judge := __CORRUPT__006` → `MISSING_POS_FUNCTION`；`AC-C39-POS-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-0c795ce79e91cf94918b"></a>
#### AC-C39-POS-HUMAN

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；Maker冒Human或決議是另一scope
- **Source** `BODY-07:461`，原 Oracle `AC-C39-POS-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L451，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/HUMAN` | `SBL DOC08:L398` 原規則 `L3861 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `feature_invoked and acceptance_predicate_declared && HUMAN_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/pos/human := __CORRUPT__007` → `MISSING_POS_FUNCTION`；`AC-C39-POS-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-fba3518c30aa248c17f5"></a>
#### AC-C39-POS-COMPOSITE

- **原 NEG 本版有效保留**：去掉必要輸出或接受錯誤輸出；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:503`，原 Oracle `AC-C39-POS-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=POS，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：功能被要求且已宣告acceptance predicate；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L452，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `POS/COMPOSITE` | `SBL DOC08:L399` 原規則 `L3862 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `feature_invoked and acceptance_predicate_declared && COMPOSITE_inputs_bound`；requires feature invoked + acceptance predicate; consumer output and real raw | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/pos/composite := __CORRUPT__008` → `MISSING_POS_FUNCTION`；`AC-C39-POS-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=POS，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執POS專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-adcf14bd76cbbaa89148"></a>
#### AC-C39-NEG-DETERMINISTIC

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；observed_value改成非expected
- **Source** `BODY-07:578`，原 Oracle `AC-C39-NEG-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L453，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/DETERMINISTIC` | `SBL DOC08:L400` 原規則 `L3863 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `invalid_input_contract or forbidden_action_declared && DETERMINISTIC_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/neg/deterministic := __CORRUPT__009` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-9937c87d40bca7f20b4f"></a>
#### AC-C39-NEG-STATE_READBACK

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:682`，原 Oracle `AC-C39-NEG-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L454，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/STATE_READBACK` | `SBL DOC08:L401` 原規則 `L3864 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `invalid_input_contract or forbidden_action_declared && STATE_READBACK_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/neg/state_readback := __CORRUPT__010` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-9c10ba75287e099dc90c"></a>
#### AC-C39-NEG-PROPERTY

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；至少一generated case破invariant
- **Source** `BODY-07:822`，原 Oracle `AC-C39-NEG-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L455，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/PROPERTY` | `SBL DOC08:L402` 原規則 `L3865 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `invalid_input_contract or forbidden_action_declared && PROPERTY_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/neg/property := __CORRUPT__011` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-56e81908b984f8e047cd"></a>
#### AC-C39-NEG-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；更換reference或輸出差異
- **Source** `BODY-07:967`，原 Oracle `AC-C39-NEG-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L456，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/REFERENCE_OUTPUT` | `SBL DOC08:L403` 原規則 `L3866 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `invalid_input_contract or forbidden_action_declared && REFERENCE_OUTPUT_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/neg/reference_output := __CORRUPT__012` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-90381fb9b7348a42766e"></a>
#### AC-C39-NEG-STATISTICAL

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:1081`，原 Oracle `AC-C39-NEG-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L457，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/STATISTICAL` | `SBL DOC08:L404` 原規則 `L3867 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `invalid_input_contract or forbidden_action_declared && STATISTICAL_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/neg/statistical := __CORRUPT__013` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-1f0bf4730201b6be0449"></a>
#### AC-C39-NEG-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:1189`，原 Oracle `AC-C39-NEG-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L458，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/SEMANTIC_JUDGE` | `SBL DOC08:L405` 原規則 `L3868 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `invalid_input_contract or forbidden_action_declared && SEMANTIC_JUDGE_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/neg/semantic_judge := __CORRUPT__014` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-c6f8102269a94f3d47d5"></a>
#### AC-C39-NEG-HUMAN

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；Maker冒Human或決議是另一scope
- **Source** `BODY-07:1294`，原 Oracle `AC-C39-NEG-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L459，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/HUMAN` | `SBL DOC08:L406` 原規則 `L3869 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `invalid_input_contract or forbidden_action_declared && HUMAN_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/neg/human := __CORRUPT__015` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-b9d9bc337c4f11ef3356"></a>
#### AC-C39-NEG-COMPOSITE

- **原 NEG 本版有效保留**：將拒收轉成功或寫入禁止state；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:1398`，原 Oracle `AC-C39-NEG-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=NEG，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- applicability/source：來源禁止行為或非法輸入可構造；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L460，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `NEG/COMPOSITE` | `SBL DOC08:L407` 原規則 `L3870 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `invalid_input_contract or forbidden_action_declared && COMPOSITE_inputs_bound`；requires forbidden action or invalid input; deny with world no diff | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/neg/composite := __CORRUPT__016` → `NEGATIVE_ACCEPTED`；`AC-C39-NEG-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=NEG，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-NEG-DUPLICATE']；無Raw不可假裝已跑Native。
- transform/typed output：先執NEG專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-95db638d4a9f43a80f75"></a>
#### AC-C39-EDGE-DETERMINISTIC

- **原 NEG 本版有效保留**：off-by-one接受越界值；observed_value改成非expected
- **Source** `BODY-07:1555`，原 Oracle `AC-C39-EDGE-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L461，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/DETERMINISTIC` | `SBL DOC08:L408` 原規則 `L3871 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `input_boundary_or_resource_limit_declared && DETERMINISTIC_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/edge/deterministic := __CORRUPT__017` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-db9cdcb3a8acb2085714"></a>
#### AC-C39-EDGE-STATE_READBACK

- **原 NEG 本版有效保留**：off-by-one接受越界值；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:1659`，原 Oracle `AC-C39-EDGE-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L462，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/STATE_READBACK` | `SBL DOC08:L409` 原規則 `L3872 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `input_boundary_or_resource_limit_declared && STATE_READBACK_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/edge/state_readback := __CORRUPT__018` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-1e59f3c2fae91fa7155e"></a>
#### AC-C39-EDGE-PROPERTY

- **原 NEG 本版有效保留**：off-by-one接受越界值；至少一generated case破invariant
- **Source** `BODY-07:1799`，原 Oracle `AC-C39-EDGE-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L463，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/PROPERTY` | `SBL DOC08:L410` 原規則 `L3873 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `input_boundary_or_resource_limit_declared && PROPERTY_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/edge/property := __CORRUPT__019` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-7cb87a2d592128517ccc"></a>
#### AC-C39-EDGE-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：off-by-one接受越界值；更換reference或輸出差異
- **Source** `BODY-07:1944`，原 Oracle `AC-C39-EDGE-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L464，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/REFERENCE_OUTPUT` | `SBL DOC08:L411` 原規則 `L3874 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `input_boundary_or_resource_limit_declared && REFERENCE_OUTPUT_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/edge/reference_output := __CORRUPT__020` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-4d16cdc09abc006fd333"></a>
#### AC-C39-EDGE-STATISTICAL

- **原 NEG 本版有效保留**：off-by-one接受越界值；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:2058`，原 Oracle `AC-C39-EDGE-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L465，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/STATISTICAL` | `SBL DOC08:L412` 原規則 `L3875 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `input_boundary_or_resource_limit_declared && STATISTICAL_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/edge/statistical := __CORRUPT__021` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-5ddbaf1f86a81c5717e5"></a>
#### AC-C39-EDGE-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：off-by-one接受越界值；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:2166`，原 Oracle `AC-C39-EDGE-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L466，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/SEMANTIC_JUDGE` | `SBL DOC08:L413` 原規則 `L3876 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `input_boundary_or_resource_limit_declared && SEMANTIC_JUDGE_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/edge/semantic_judge := __CORRUPT__022` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-dabe7c8261a2f8110c80"></a>
#### AC-C39-EDGE-HUMAN

- **原 NEG 本版有效保留**：off-by-one接受越界值；Maker冒Human或決議是另一scope
- **Source** `BODY-07:2271`，原 Oracle `AC-C39-EDGE-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L467，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/HUMAN` | `SBL DOC08:L414` 原規則 `L3877 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `input_boundary_or_resource_limit_declared && HUMAN_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/edge/human := __CORRUPT__023` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-7cb1c84c1245a4c1ecc1"></a>
#### AC-C39-EDGE-COMPOSITE

- **原 NEG 本版有效保留**：off-by-one接受越界值；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:2375`，原 Oracle `AC-C39-EDGE-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=EDGE，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- applicability/source：來源boundary/empty/limit適用；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L468，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `EDGE/COMPOSITE` | `SBL DOC08:L415` 原規則 `L3878 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `input_boundary_or_resource_limit_declared && COMPOSITE_inputs_bound`；requires input bound or resource limit; one-past boundary rejection | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/edge/composite := __CORRUPT__024` → `EDGE_BOUND_VIOLATION`；`AC-C39-EDGE-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=EDGE，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-EDGE-EMPTY-TITLE']；無Raw不可假裝已跑Native。
- transform/typed output：先執EDGE專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-decf235940f901bdf23e"></a>
#### AC-C39-SEC-DETERMINISTIC

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；observed_value改成非expected
- **Source** `BODY-07:2532`，原 Oracle `AC-C39-SEC-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L469，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/DETERMINISTIC` | `SBL DOC08:L416` 原規則 `L3879 REQUIRED for EFFECT machine-checkable predicate in each GJ` | `trust_boundary or secrets or untrusted_source or permission_effect && DETERMINISTIC_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/sec/deterministic := __CORRUPT__025` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-0b91b66a4fe05cc17a16"></a>
#### AC-C39-SEC-STATE_READBACK

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:2608`，原 Oracle `AC-C39-SEC-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L470，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/STATE_READBACK` | `SBL DOC08:L417` 原規則 `L3880 REQUIRED if EFFECT changes state; SHADOW readonly snapshot allowed only` | `trust_boundary or secrets or untrusted_source or permission_effect && STATE_READBACK_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/sec/state_readback := __CORRUPT__026` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-d622d3e38f778242c8f7"></a>
#### AC-C39-SEC-PROPERTY

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；至少一generated case破invariant
- **Source** `BODY-07:2692`，原 Oracle `AC-C39-SEC-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L471，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/PROPERTY` | `SBL DOC08:L418` 原規則 `L3881 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `trust_boundary or secrets or untrusted_source or permission_effect && PROPERTY_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/sec/property := __CORRUPT__027` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-aaabeba7783541cee7a9"></a>
#### AC-C39-SEC-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；更換reference或輸出差異
- **Source** `BODY-07:2795`，原 Oracle `AC-C39-SEC-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L472，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/REFERENCE_OUTPUT` | `SBL DOC08:L419` 原規則 `L3882 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `trust_boundary or secrets or untrusted_source or permission_effect && REFERENCE_OUTPUT_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/sec/reference_output := __CORRUPT__028` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-54a9517d940c4199a2ea"></a>
#### AC-C39-SEC-STATISTICAL

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:2881`，原 Oracle `AC-C39-SEC-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L473，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/STATISTICAL` | `SBL DOC08:L420` 原規則 `L3883 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `trust_boundary or secrets or untrusted_source or permission_effect && STATISTICAL_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/sec/statistical := __CORRUPT__029` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-ab083e7aeac284a4c499"></a>
#### AC-C39-SEC-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:2961`，原 Oracle `AC-C39-SEC-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L474，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/SEMANTIC_JUDGE` | `SBL DOC08:L421` 原規則 `L3884 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `trust_boundary or secrets or untrusted_source or permission_effect && SEMANTIC_JUDGE_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/sec/semantic_judge := __CORRUPT__030` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-26370560955913a56cd3"></a>
#### AC-C39-SEC-HUMAN

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；Maker冒Human或決議是另一scope
- **Source** `BODY-07:3038`，原 Oracle `AC-C39-SEC-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L475，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/HUMAN` | `SBL DOC08:L422` 原規則 `L3885 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `trust_boundary or secrets or untrusted_source or permission_effect && HUMAN_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/sec/human := __CORRUPT__031` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-0a82236281721630b5ff"></a>
#### AC-C39-SEC-COMPOSITE

- **原 NEG 本版有效保留**：越域payload或自簽verdict被接受；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:3114`，原 Oracle `AC-C39-SEC-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=SEC，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：trust boundary/credential/source受影；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L476，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `SEC/COMPOSITE` | `SBL DOC08:L423` 原規則 `L3886 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `trust_boundary or secrets or untrusted_source or permission_effect && COMPOSITE_inputs_bound`；requires trust/secrets/untrusted source/permission effect; rights stay bounded | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/sec/composite := __CORRUPT__032` → `SECURITY_BOUNDARY_BREACH`；`AC-C39-SEC-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=SEC，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執SEC專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-d40911e3027a8ba4a872"></a>
#### AC-C39-PERF-DETERMINISTIC

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；observed_value改成非expected
- **Source** `BODY-07:3215`，原 Oracle `AC-C39-PERF-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L477，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/DETERMINISTIC` | `SBL DOC08:L424` 原規則 `L3887 REQUIRED for PERF machine-checkable predicate in each GJ` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && DETERMINISTIC_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/perf/deterministic := __CORRUPT__033` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-7a7b0f66b91cd44b6bee"></a>
#### AC-C39-PERF-STATE_READBACK

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:3279`，原 Oracle `AC-C39-PERF-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L478，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/STATE_READBACK` | `SBL DOC08:L425` 原規則 `L3888 REQUIRED if PERF changes state; SHADOW readonly snapshot allowed only` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && STATE_READBACK_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/perf/state_readback := __CORRUPT__034` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-b7c9a704b28529aaf2a0"></a>
#### AC-C39-PERF-PROPERTY

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；至少一generated case破invariant
- **Source** `BODY-07:3384`，原 Oracle `AC-C39-PERF-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L479，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/PROPERTY` | `SBL DOC08:L426` 原規則 `L3889 CONDITIONAL: PERF typed property/reference/composite defined with source and fixtures` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && PROPERTY_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/perf/property := __CORRUPT__035` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-a0bbdae7bc3ba0852c6a"></a>
#### AC-C39-PERF-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；更換reference或輸出差異
- **Source** `BODY-07:3469`，原 Oracle `AC-C39-PERF-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L480，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/REFERENCE_OUTPUT` | `SBL DOC08:L427` 原規則 `L3890 CONDITIONAL: PERF typed property/reference/composite defined with source and fixtures` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && REFERENCE_OUTPUT_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/perf/reference_output := __CORRUPT__036` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-f13ecc62c252e80da6e2"></a>
#### AC-C39-PERF-STATISTICAL

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:3541`，原 Oracle `AC-C39-PERF-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L481，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/STATISTICAL` | `SBL DOC08:L428` 原規則 `L3891 CONDITIONAL: PERF benchmark with calibrated dataset+confidence; no stand-alone release g` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && STATISTICAL_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/perf/statistical := __CORRUPT__037` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-5ce76fdd93507ca84edc"></a>
#### AC-C39-PERF-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:3609`，原 Oracle `AC-C39-PERF-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L482，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/SEMANTIC_JUDGE` | `SBL DOC08:L429` 原規則 `L3892 CONDITIONAL: PERF benchmark with calibrated dataset+confidence; no stand-alone release g` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && SEMANTIC_JUDGE_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/perf/semantic_judge := __CORRUPT__038` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-5b8abad4946ecaba3652"></a>
#### AC-C39-PERF-HUMAN

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；Maker冒Human或決議是另一scope
- **Source** `BODY-07:3674`，原 Oracle `AC-C39-PERF-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L483，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/HUMAN` | `SBL DOC08:L430` 原規則 `L3893 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && HUMAN_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/perf/human := __CORRUPT__039` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-4f2d4fc7c92eac7cc176"></a>
#### AC-C39-PERF-COMPOSITE

- **原 NEG 本版有效保留**：改校準或把漏測樣本去除；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:3738`，原 Oracle `AC-C39-PERF-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PERF，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- applicability/source：有來源校準dataset/metric/budget；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L484，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PERF/COMPOSITE` | `SBL DOC08:L431` 原規則 `L3894 CONDITIONAL: PERF typed property/reference/composite defined with source and fixtures` | `nfr_sli_slo_id and benchmark_dataset_pin and metric_threshold && COMPOSITE_inputs_bound`；requires actual SLI/SLO + pinned benchmark; do not proxy latency | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/perf/composite := __CORRUPT__040` → `PERF_SLO_EXCEEDED`；`AC-C39-PERF-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PERF，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-PERF-LIST-00', 'CLI-PERF-LIST-01', 'CLI-PERF-LIST-02', 'CLI-PERF-LIST-03', 'CLI-PERF-LIST-04', 'CLI-PERF-LIST-05', 'CLI-PERF-LIST-06', 'CLI-PERF-LIST-07', 'CLI-PERF-LIST-08', 'CLI-PERF-LIST-09', 'CLI-PERF-LIST-10', 'CLI-PERF-LIST-11']；無Raw不可假裝已跑Native。
- transform/typed output：先執PERF專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-99e26111e03f13906621"></a>
#### AC-C39-PARITY-DETERMINISTIC

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；observed_value改成非expected
- **Source** `BODY-07:3849`，原 Oracle `AC-C39-PARITY-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L485，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/DETERMINISTIC` | `SBL DOC08:L432` 原規則 `L3895 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `provider_off_required and provider_off_profile_id and fallback_contract && DETERMINISTIC_inputs_bound`；requires provider-off profile + fallback; no network egress | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/parity/deterministic := __CORRUPT__041` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-fbc51fa913fa35c84c1e"></a>
#### AC-C39-PARITY-STATE_READBACK

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:3929`，原 Oracle `AC-C39-PARITY-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L486，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/STATE_READBACK` | `SBL DOC08:L433` 原規則 `L3896 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `provider_off_required and provider_off_profile_id and fallback_contract && STATE_READBACK_inputs_bound`；requires provider-off profile + fallback; no network egress | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/parity/state_readback := __CORRUPT__042` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-e031c5591c9d49a8e666"></a>
#### AC-C39-PARITY-PROPERTY

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；至少一generated case破invariant
- **Source** `BODY-07:4036`，原 Oracle `AC-C39-PARITY-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L487，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/PROPERTY` | `SBL DOC08:L434` 原規則 `L3897 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `provider_off_required and provider_off_profile_id and fallback_contract && PROPERTY_inputs_bound`；requires provider-off profile + fallback; no network egress | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/parity/property := __CORRUPT__043` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-4e0f02e3e85f9ecbea7b"></a>
#### AC-C39-PARITY-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；更換reference或輸出差異
- **Source** `BODY-07:4149`，原 Oracle `AC-C39-PARITY-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L488，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/REFERENCE_OUTPUT` | `SBL DOC08:L435` 原規則 `L3898 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `provider_off_required and provider_off_profile_id and fallback_contract && REFERENCE_OUTPUT_inputs_bound`；requires provider-off profile + fallback; no network egress | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/parity/reference_output := __CORRUPT__044` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-840adc2a016bb6b307cd"></a>
#### AC-C39-PARITY-STATISTICAL

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:4239`，原 Oracle `AC-C39-PARITY-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L489，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/STATISTICAL` | `SBL DOC08:L436` 原規則 `L3899 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `provider_off_required and provider_off_profile_id and fallback_contract && STATISTICAL_inputs_bound`；requires provider-off profile + fallback; no network egress | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/parity/statistical := __CORRUPT__045` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-4af1fa94a4b62c7a6c0a"></a>
#### AC-C39-PARITY-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:4323`，原 Oracle `AC-C39-PARITY-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L490，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/SEMANTIC_JUDGE` | `SBL DOC08:L437` 原規則 `L3900 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `provider_off_required and provider_off_profile_id and fallback_contract && SEMANTIC_JUDGE_inputs_bound`；requires provider-off profile + fallback; no network egress | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/parity/semantic_judge := __CORRUPT__046` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-8a0e15e6ce18ae7686d8"></a>
#### AC-C39-PARITY-HUMAN

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；Maker冒Human或決議是另一scope
- **Source** `BODY-07:4404`，原 Oracle `AC-C39-PARITY-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L491，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/HUMAN` | `SBL DOC08:L438` 原規則 `L3901 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `provider_off_required and provider_off_profile_id and fallback_contract && HUMAN_inputs_bound`；requires provider-off profile + fallback; no network egress | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/parity/human := __CORRUPT__047` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-080760ed5a3c18ed496b"></a>
#### AC-C39-PARITY-COMPOSITE

- **原 NEG 本版有效保留**：只測一Host借其他HostPASS；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:4484`，原 Oracle `AC-C39-PARITY-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=PARITY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- applicability/source：替代Provider/Host/mode需原Parity；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L492，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `PARITY/COMPOSITE` | `SBL DOC08:L439` 原規則 `L3902 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `provider_off_required and provider_off_profile_id and fallback_contract && COMPOSITE_inputs_bound`；requires provider-off profile + fallback; no network egress | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/parity/composite := __CORRUPT__048` → `PARITY_PROVIDER_OFF_FAIL`；`AC-C39-PARITY-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=PARITY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID', 'CLI-PARITY-SECOND-ENTRYPOINT']；無Raw不可假裝已跑Native。
- transform/typed output：先執PARITY專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-f323a1afbb5b200bf93f"></a>
#### AC-C39-RECOVERY-DETERMINISTIC

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；observed_value改成非expected
- **Source** `BODY-07:4607`，原 Oracle `AC-C39-RECOVERY-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L493，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/DETERMINISTIC` | `SBL DOC08:L440` 原規則 `L3903 REQUIRED for EFFECT machine-checkable predicate in each GJ` | `effect_or_failure_recovery_required and rollback_ref && DETERMINISTIC_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/recovery/deterministic := __CORRUPT__049` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-dfed44642e092a059ad1"></a>
#### AC-C39-RECOVERY-STATE_READBACK

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:4651`，原 Oracle `AC-C39-RECOVERY-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L494，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/STATE_READBACK` | `SBL DOC08:L441` 原規則 `L3904 REQUIRED if EFFECT changes state; SHADOW readonly snapshot allowed only` | `effect_or_failure_recovery_required and rollback_ref && STATE_READBACK_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/recovery/state_readback := __CORRUPT__050` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-e2584442802529542d4a"></a>
#### AC-C39-RECOVERY-PROPERTY

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；至少一generated case破invariant
- **Source** `BODY-07:4720`，原 Oracle `AC-C39-RECOVERY-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L495，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/PROPERTY` | `SBL DOC08:L442` 原規則 `L3905 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `effect_or_failure_recovery_required and rollback_ref && PROPERTY_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/recovery/property := __CORRUPT__051` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-eac54e01f11bf09a7c9f"></a>
#### AC-C39-RECOVERY-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；更換reference或輸出差異
- **Source** `BODY-07:4775`，原 Oracle `AC-C39-RECOVERY-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L496，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/REFERENCE_OUTPUT` | `SBL DOC08:L443` 原規則 `L3906 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `effect_or_failure_recovery_required and rollback_ref && REFERENCE_OUTPUT_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/recovery/reference_output := __CORRUPT__052` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-1e0fa08e4b0c73739c5d"></a>
#### AC-C39-RECOVERY-STATISTICAL

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:4829`，原 Oracle `AC-C39-RECOVERY-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L497，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/STATISTICAL` | `SBL DOC08:L444` 原規則 `L3907 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `effect_or_failure_recovery_required and rollback_ref && STATISTICAL_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/recovery/statistical := __CORRUPT__053` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-957b1632d697d5cf5f8a"></a>
#### AC-C39-RECOVERY-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:4877`，原 Oracle `AC-C39-RECOVERY-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L498，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/SEMANTIC_JUDGE` | `SBL DOC08:L445` 原規則 `L3908 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `effect_or_failure_recovery_required and rollback_ref && SEMANTIC_JUDGE_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/recovery/semantic_judge := __CORRUPT__054` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-702f8f564f98ec9bb367"></a>
#### AC-C39-RECOVERY-HUMAN

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；Maker冒Human或決議是另一scope
- **Source** `BODY-07:4922`，原 Oracle `AC-C39-RECOVERY-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L499，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/HUMAN` | `SBL DOC08:L446` 原規則 `L3909 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `effect_or_failure_recovery_required and rollback_ref && HUMAN_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/recovery/human := __CORRUPT__055` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-935fb7987cb9ba49df5b"></a>
#### AC-C39-RECOVERY-COMPOSITE

- **原 NEG 本版有效保留**：同nonce盲重播或skip未完成工作；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:4966`，原 Oracle `AC-C39-RECOVERY-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=RECOVERY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：存在restart/timeout/checkpoint情境；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L500，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `RECOVERY/COMPOSITE` | `SBL DOC08:L447` 原規則 `L3910 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `effect_or_failure_recovery_required and rollback_ref && COMPOSITE_inputs_bound`；requires failure recovery + rollback ref; pre/post and no residue | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/recovery/composite := __CORRUPT__056` → `RECOVERY_STATE_MISMATCH`；`AC-C39-RECOVERY-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=RECOVERY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執RECOVERY專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-6eaccaf0163f7a9eb3e6"></a>
#### AC-C39-UPGRADE-DETERMINISTIC

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；observed_value改成非expected
- **Source** `BODY-07:5051`，原 Oracle `AC-C39-UPGRADE-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L501，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/DETERMINISTIC` | `SBL DOC08:L448` 原規則 `L3911 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `upgrade_path_declared and from_version and to_version && DETERMINISTIC_inputs_bound`；requires from/to migration invariant + schema versions | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/upgrade/deterministic := __CORRUPT__057` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-2f8783185fd3e4a897c9"></a>
#### AC-C39-UPGRADE-STATE_READBACK

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:5095`，原 Oracle `AC-C39-UPGRADE-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L502，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/STATE_READBACK` | `SBL DOC08:L449` 原規則 `L3912 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `upgrade_path_declared and from_version and to_version && STATE_READBACK_inputs_bound`；requires from/to migration invariant + schema versions | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/upgrade/state_readback := __CORRUPT__058` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-70265ea44541f07f8112"></a>
#### AC-C39-UPGRADE-PROPERTY

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；至少一generated case破invariant
- **Source** `BODY-07:5141`，原 Oracle `AC-C39-UPGRADE-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L503，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/PROPERTY` | `SBL DOC08:L450` 原規則 `L3913 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `upgrade_path_declared and from_version and to_version && PROPERTY_inputs_bound`；requires from/to migration invariant + schema versions | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/upgrade/property := __CORRUPT__059` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-79c5b1cb2af4059656a4"></a>
#### AC-C39-UPGRADE-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；更換reference或輸出差異
- **Source** `BODY-07:5196`，原 Oracle `AC-C39-UPGRADE-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L504，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/REFERENCE_OUTPUT` | `SBL DOC08:L451` 原規則 `L3914 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `upgrade_path_declared and from_version and to_version && REFERENCE_OUTPUT_inputs_bound`；requires from/to migration invariant + schema versions | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/upgrade/reference_output := __CORRUPT__060` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-912399007e87efe2da6b"></a>
#### AC-C39-UPGRADE-STATISTICAL

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:5242`，原 Oracle `AC-C39-UPGRADE-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L505，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/STATISTICAL` | `SBL DOC08:L452` 原規則 `L3915 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `upgrade_path_declared and from_version and to_version && STATISTICAL_inputs_bound`；requires from/to migration invariant + schema versions | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/upgrade/statistical := __CORRUPT__061` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-5db20040797d99769c0c"></a>
#### AC-C39-UPGRADE-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:5290`，原 Oracle `AC-C39-UPGRADE-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L506，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/SEMANTIC_JUDGE` | `SBL DOC08:L453` 原規則 `L3916 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `upgrade_path_declared and from_version and to_version && SEMANTIC_JUDGE_inputs_bound`；requires from/to migration invariant + schema versions | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/upgrade/semantic_judge := __CORRUPT__062` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-0c82840faf3dfd84bc32"></a>
#### AC-C39-UPGRADE-HUMAN

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；Maker冒Human或決議是另一scope
- **Source** `BODY-07:5335`，原 Oracle `AC-C39-UPGRADE-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L507，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/HUMAN` | `SBL DOC08:L454` 原規則 `L3917 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `upgrade_path_declared and from_version and to_version && HUMAN_inputs_bound`；requires from/to migration invariant + schema versions | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/upgrade/human := __CORRUPT__063` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-bc54271ca765538e1663"></a>
#### AC-C39-UPGRADE-COMPOSITE

- **原 NEG 本版有效保留**：靜默丟欄或拿舊receipt當新版；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:5379`，原 Oracle `AC-C39-UPGRADE-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UPGRADE，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- applicability/source：同asset有來源定義版本migration；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L508，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UPGRADE/COMPOSITE` | `SBL DOC08:L455` 原規則 `L3918 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `upgrade_path_declared and from_version and to_version && COMPOSITE_inputs_bound`；requires from/to migration invariant + schema versions | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/upgrade/composite := __CORRUPT__064` → `UPGRADE_VERSION_MISMATCH`；`AC-C39-UPGRADE-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UPGRADE，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=[]；無Raw不可假裝已跑Native。
- transform/typed output：先執UPGRADE專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-5fe49e7d2a479bdce44e"></a>
#### AC-C39-ROLLBACK-DETERMINISTIC

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；observed_value改成非expected
- **Source** `BODY-07:5444`，原 Oracle `AC-C39-ROLLBACK-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L509，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/DETERMINISTIC` | `SBL DOC08:L456` 原規則 `L3919 REQUIRED for EFFECT machine-checkable predicate in each GJ` | `mutating_effect and rollback_ref and preimage_digest && DETERMINISTIC_inputs_bound`；requires mutating effect + preimage; exact state restore | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/rollback/deterministic := __CORRUPT__065` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-a91c0c4e0beaa4a8f5f0"></a>
#### AC-C39-ROLLBACK-STATE_READBACK

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:5490`，原 Oracle `AC-C39-ROLLBACK-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L510，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/STATE_READBACK` | `SBL DOC08:L457` 原規則 `L3920 REQUIRED if EFFECT changes state; SHADOW readonly snapshot allowed only` | `mutating_effect and rollback_ref and preimage_digest && STATE_READBACK_inputs_bound`；requires mutating effect + preimage; exact state restore | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/rollback/state_readback := __CORRUPT__066` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-fbd142d9c008b4fe6230"></a>
#### AC-C39-ROLLBACK-PROPERTY

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；至少一generated case破invariant
- **Source** `BODY-07:5542`，原 Oracle `AC-C39-ROLLBACK-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L511，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/PROPERTY` | `SBL DOC08:L458` 原規則 `L3921 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `mutating_effect and rollback_ref and preimage_digest && PROPERTY_inputs_bound`；requires mutating effect + preimage; exact state restore | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/rollback/property := __CORRUPT__067` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-aeec520365e9137643eb"></a>
#### AC-C39-ROLLBACK-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；更換reference或輸出差異
- **Source** `BODY-07:5598`，原 Oracle `AC-C39-ROLLBACK-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L512，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/REFERENCE_OUTPUT` | `SBL DOC08:L459` 原規則 `L3922 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `mutating_effect and rollback_ref and preimage_digest && REFERENCE_OUTPUT_inputs_bound`；requires mutating effect + preimage; exact state restore | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/rollback/reference_output := __CORRUPT__068` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-50f3c09b0651acfb9e52"></a>
#### AC-C39-ROLLBACK-STATISTICAL

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:5652`，原 Oracle `AC-C39-ROLLBACK-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L513，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/STATISTICAL` | `SBL DOC08:L460` 原規則 `L3923 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `mutating_effect and rollback_ref and preimage_digest && STATISTICAL_inputs_bound`；requires mutating effect + preimage; exact state restore | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/rollback/statistical := __CORRUPT__069` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-e7736ff17fd35cdf9a10"></a>
#### AC-C39-ROLLBACK-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:5702`，原 Oracle `AC-C39-ROLLBACK-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L514，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/SEMANTIC_JUDGE` | `SBL DOC08:L461` 原規則 `L3924 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `mutating_effect and rollback_ref and preimage_digest && SEMANTIC_JUDGE_inputs_bound`；requires mutating effect + preimage; exact state restore | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/rollback/semantic_judge := __CORRUPT__070` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-c71d87be497798c5f495"></a>
#### AC-C39-ROLLBACK-HUMAN

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；Maker冒Human或決議是另一scope
- **Source** `BODY-07:5749`，原 Oracle `AC-C39-ROLLBACK-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L515，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/HUMAN` | `SBL DOC08:L462` 原規則 `L3925 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `mutating_effect and rollback_ref and preimage_digest && HUMAN_inputs_bound`；requires mutating effect + preimage; exact state restore | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/rollback/human := __CORRUPT__071` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-686fa4de548fb691a1ed"></a>
#### AC-C39-ROLLBACK-COMPOSITE

- **原 NEG 本版有效保留**：只刪log卻稱回復世界；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:5795`，原 Oracle `AC-C39-ROLLBACK-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=ROLLBACK，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：本effect可回復或需補償；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L516，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `ROLLBACK/COMPOSITE` | `SBL DOC08:L463` 原規則 `L3926 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `mutating_effect and rollback_ref and preimage_digest && COMPOSITE_inputs_bound`；requires mutating effect + preimage; exact state restore | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/rollback/composite := __CORRUPT__072` → `ROLLBACK_PREIMAGE_MISSING`；`AC-C39-ROLLBACK-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=ROLLBACK，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執ROLLBACK專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-ea400d11fcc57c645db8"></a>
#### AC-C39-UNINSTALL-DETERMINISTIC

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；observed_value改成非expected
- **Source** `BODY-07:5862`，原 Oracle `AC-C39-UNINSTALL-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L517，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/DETERMINISTIC` | `SBL DOC08:L464` 原規則 `L3927 REQUIRED for EFFECT machine-checkable predicate in each GJ` | `installation_workpackage and retention_policy && DETERMINISTIC_inputs_bound`；requires installed workpackage + retention; no stale hooks | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/uninstall/deterministic := __CORRUPT__073` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-6bcc72d35f91841b6f82"></a>
#### AC-C39-UNINSTALL-STATE_READBACK

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:5904`，原 Oracle `AC-C39-UNINSTALL-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L518，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/STATE_READBACK` | `SBL DOC08:L465` 原規則 `L3928 REQUIRED if EFFECT changes state; SHADOW readonly snapshot allowed only` | `installation_workpackage and retention_policy && STATE_READBACK_inputs_bound`；requires installed workpackage + retention; no stale hooks | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/uninstall/state_readback := __CORRUPT__074` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-866e1bcb2e18b9d0766a"></a>
#### AC-C39-UNINSTALL-PROPERTY

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；至少一generated case破invariant
- **Source** `BODY-07:5961`，原 Oracle `AC-C39-UNINSTALL-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L519，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/PROPERTY` | `SBL DOC08:L466` 原規則 `L3929 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `installation_workpackage and retention_policy && PROPERTY_inputs_bound`；requires installed workpackage + retention; no stale hooks | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/uninstall/property := __CORRUPT__075` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-caa15fa0a673fdbde38d"></a>
#### AC-C39-UNINSTALL-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；更換reference或輸出差異
- **Source** `BODY-07:6013`，原 Oracle `AC-C39-UNINSTALL-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L520，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/REFERENCE_OUTPUT` | `SBL DOC08:L467` 原規則 `L3930 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `installation_workpackage and retention_policy && REFERENCE_OUTPUT_inputs_bound`；requires installed workpackage + retention; no stale hooks | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/uninstall/reference_output := __CORRUPT__076` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-af324a6e978428524b8f"></a>
#### AC-C39-UNINSTALL-STATISTICAL

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:6065`，原 Oracle `AC-C39-UNINSTALL-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L521，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/STATISTICAL` | `SBL DOC08:L468` 原規則 `L3931 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `installation_workpackage and retention_policy && STATISTICAL_inputs_bound`；requires installed workpackage + retention; no stale hooks | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/uninstall/statistical := __CORRUPT__077` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-416c98398211b12c735c"></a>
#### AC-C39-UNINSTALL-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:6111`，原 Oracle `AC-C39-UNINSTALL-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L522，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/SEMANTIC_JUDGE` | `SBL DOC08:L469` 原規則 `L3932 CONDITIONAL: EFFECT benchmark with calibrated dataset+confidence; no stand-alone release` | `installation_workpackage and retention_policy && SEMANTIC_JUDGE_inputs_bound`；requires installed workpackage + retention; no stale hooks | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/uninstall/semantic_judge := __CORRUPT__078` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-0cd58fa3c8b9482b6189"></a>
#### AC-C39-UNINSTALL-HUMAN

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；Maker冒Human或決議是另一scope
- **Source** `BODY-07:6154`，原 Oracle `AC-C39-UNINSTALL-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L523，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/HUMAN` | `SBL DOC08:L470` 原規則 `L3933 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `installation_workpackage and retention_policy && HUMAN_inputs_bound`；requires installed workpackage + retention; no stale hooks | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/uninstall/human := __CORRUPT__079` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-d1e9c790d989fe9e953c"></a>
#### AC-C39-UNINSTALL-COMPOSITE

- **原 NEG 本版有效保留**：copy刪除但Host仍loaded；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:6196`，原 Oracle `AC-C39-UNINSTALL-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=UNINSTALL，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- applicability/source：該asset有Host安裝/loaded effect；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L524，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `UNINSTALL/COMPOSITE` | `SBL DOC08:L471` 原規則 `L3934 CONDITIONAL: EFFECT typed property/reference/composite defined with source and fixtures` | `installation_workpackage and retention_policy && COMPOSITE_inputs_bound`；requires installed workpackage + retention; no stale hooks | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/uninstall/composite := __CORRUPT__080` → `UNINSTALL_RESIDUE`；`AC-C39-UNINSTALL-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=UNINSTALL，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-UNINSTALL-OWNED-REMOVE', 'CLI-UNINSTALL-FOREIGN-DENY']；無Raw不可假裝已跑Native。
- transform/typed output：先執UNINSTALL專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-d76cf7b11b96431b1610"></a>
#### AC-C39-MUT-DETERMINISTIC

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；observed_value改成非expected
- **Source** `BODY-07:6269`，原 Oracle `AC-C39-MUT-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L525，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/DETERMINISTIC` | `SBL DOC08:L472` 原規則 `L3935 REQUIRED for MUT machine-checkable predicate in each GJ` | `testable_predicate and mutation_operator and fixed_seed && DETERMINISTIC_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/mut/deterministic := __CORRUPT__081` → `MUTANT_SURVIVED`；`AC-C39-MUT-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-c420dd263e7dbb1cd54f"></a>
#### AC-C39-MUT-STATE_READBACK

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:6307`，原 Oracle `AC-C39-MUT-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L526，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/STATE_READBACK` | `SBL DOC08:L473` 原規則 `L3936 REQUIRED if MUT changes state; SHADOW readonly snapshot allowed only` | `testable_predicate and mutation_operator and fixed_seed && STATE_READBACK_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/mut/state_readback := __CORRUPT__082` → `MUTANT_SURVIVED`；`AC-C39-MUT-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-f8b12fa2072c290745b0"></a>
#### AC-C39-MUT-PROPERTY

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；至少一generated case破invariant
- **Source** `BODY-07:6381`，原 Oracle `AC-C39-MUT-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L527，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/PROPERTY` | `SBL DOC08:L474` 原規則 `L3937 CONDITIONAL: MUT typed property/reference/composite defined with source and fixtures` | `testable_predicate and mutation_operator and fixed_seed && PROPERTY_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/mut/property := __CORRUPT__083` → `MUTANT_SURVIVED`；`AC-C39-MUT-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-40a11cc7361387756a93"></a>
#### AC-C39-MUT-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；更換reference或輸出差異
- **Source** `BODY-07:6427`，原 Oracle `AC-C39-MUT-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L528，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/REFERENCE_OUTPUT` | `SBL DOC08:L475` 原規則 `L3938 CONDITIONAL: MUT typed property/reference/composite defined with source and fixtures` | `testable_predicate and mutation_operator and fixed_seed && REFERENCE_OUTPUT_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/mut/reference_output := __CORRUPT__084` → `MUTANT_SURVIVED`；`AC-C39-MUT-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-bef52d0545909c350768"></a>
#### AC-C39-MUT-STATISTICAL

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:6473`，原 Oracle `AC-C39-MUT-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L529，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/STATISTICAL` | `SBL DOC08:L476` 原規則 `L3939 CONDITIONAL: MUT benchmark with calibrated dataset+confidence; no stand-alone release gr` | `testable_predicate and mutation_operator and fixed_seed && STATISTICAL_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/mut/statistical := __CORRUPT__085` → `MUTANT_SURVIVED`；`AC-C39-MUT-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-11577e53c5aee67d807a"></a>
#### AC-C39-MUT-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:6515`，原 Oracle `AC-C39-MUT-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L530，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/SEMANTIC_JUDGE` | `SBL DOC08:L477` 原規則 `L3940 CONDITIONAL: MUT benchmark with calibrated dataset+confidence; no stand-alone release gr` | `testable_predicate and mutation_operator and fixed_seed && SEMANTIC_JUDGE_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/mut/semantic_judge := __CORRUPT__086` → `MUTANT_SURVIVED`；`AC-C39-MUT-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-bf717c14648ce552d8dc"></a>
#### AC-C39-MUT-HUMAN

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；Maker冒Human或決議是另一scope
- **Source** `BODY-07:6554`，原 Oracle `AC-C39-MUT-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L531，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/HUMAN` | `SBL DOC08:L478` 原規則 `L3941 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `testable_predicate and mutation_operator and fixed_seed && HUMAN_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/mut/human := __CORRUPT__087` → `MUTANT_SURVIVED`；`AC-C39-MUT-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-45627b451a3ce5a58e97"></a>
#### AC-C39-MUT-COMPOSITE

- **原 NEG 本版有效保留**：oracle忽略被mutate欄位；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:6592`，原 Oracle `AC-C39-MUT-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=MUT，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- applicability/source：本domain可構造破壞性mutation；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L532，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `MUT/COMPOSITE` | `SBL DOC08:L479` 原規則 `L3942 CONDITIONAL: MUT typed property/reference/composite defined with source and fixtures` | `testable_predicate and mutation_operator and fixed_seed && COMPOSITE_inputs_bound`；requires testable predicate + operator + fixed seed; mutant killed | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/mut/composite := __CORRUPT__088` → `MUTANT_SURVIVED`；`AC-C39-MUT-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=MUT，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-LIST-FRESH-PID']；無Raw不可假裝已跑Native。
- transform/typed output：先執MUT專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-8e06a56e8bf4f18070c3"></a>
#### AC-C39-JOURNEY-DETERMINISTIC

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；observed_value改成非expected
- **Source** `BODY-07:6683`，原 Oracle `AC-C39-JOURNEY-DETERMINISTIC`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；DETERMINISTIC的required inputs全綁且原source適用；原SRC-L-001:L533，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/DETERMINISTIC` | `SBL DOC08:L480` 原規則 `L3943 REQUIRED for RUNTIME machine-checkable predicate in each GJ` | `consumer_entrypoint and user_outcome_defined and supported_kind && DETERMINISTIC_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `expected_value` → `observed_value`；`exact_eq / observed must equal source-bound expected` | `/outcome/journey/deterministic := __CORRUPT__089` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-DETERMINISTIC` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=DETERMINISTIC；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執DETERMINISTIC的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-84487fad5cc8414ab23a"></a>
#### AC-C39-JOURNEY-STATE_READBACK

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；actual_post_state不同或foreign world Reader
- **Source** `BODY-07:6749`，原 Oracle `AC-C39-JOURNEY-STATE_READBACK`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；STATE_READBACK的required inputs全綁且原source適用；原SRC-L-001:L534，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/STATE_READBACK` | `SBL DOC08:L481` 原規則 `L3944 REQUIRED if RUNTIME changes state; SHADOW readonly snapshot allowed only` | `consumer_entrypoint and user_outcome_defined and supported_kind && STATE_READBACK_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `pre_digest+expected_post_digest` → `native_world_pre+native_world_post`；`state_transition / pre+post digest from real world` | `/outcome/journey/state_readback := __CORRUPT__090` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-STATE_READBACK` | `REQUIRED_UNLESS_REAL_NATIVE_OWNER_WAIVES; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=STATE_READBACK；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執STATE_READBACK的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-70f78409d23c3fb733bb"></a>
#### AC-C39-JOURNEY-PROPERTY

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；至少一generated case破invariant
- **Source** `BODY-07:6829`，原 Oracle `AC-C39-JOURNEY-PROPERTY`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；PROPERTY的required inputs全綁且原source適用；原SRC-L-001:L535，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/PROPERTY` | `SBL DOC08:L482` 原規則 `L3945 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `consumer_entrypoint and user_outcome_defined and supported_kind && PROPERTY_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `invariant+seed` → `generated_cases+minimal_counterexample`；`all_invariant / seeded generated cases + shrunk counterexample` | `/outcome/journey/property := __CORRUPT__091` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-PROPERTY` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=PROPERTY；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執PROPERTY的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-941b052a8fa49baedf40"></a>
#### AC-C39-JOURNEY-REFERENCE_OUTPUT

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；更換reference或輸出差異
- **Source** `BODY-07:6917`，原 Oracle `AC-C39-JOURNEY-REFERENCE_OUTPUT`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；REFERENCE_OUTPUT的required inputs全綁且原source適用；原SRC-L-001:L536，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/REFERENCE_OUTPUT` | `SBL DOC08:L483` 原規則 `L3946 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `consumer_entrypoint and user_outcome_defined and supported_kind && REFERENCE_OUTPUT_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `reference_sha+canonical_output` → `observed_output`；`pinned_reference_eq / reference SHA pinned` | `/outcome/journey/reference_output := __CORRUPT__092` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-REFERENCE_OUTPUT` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=REFERENCE_OUTPUT；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執REFERENCE_OUTPUT的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-04cffe7de0cc6ed59bad"></a>
#### AC-C39-JOURNEY-STATISTICAL

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；刪dataset/改confidence/樣本不達界
- **Source** `BODY-07:6993`，原 Oracle `AC-C39-JOURNEY-STATISTICAL`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；STATISTICAL的required inputs全綁且原source適用；原SRC-L-001:L537，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/STATISTICAL` | `SBL DOC08:L484` 原規則 `L3947 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `consumer_entrypoint and user_outcome_defined and supported_kind && STATISTICAL_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `dataset_sha+calibration_sha+confidence+threshold` → `sample_metrics`；`bound_confidence / dataset+calibration+threshold` | `/outcome/journey/statistical := __CORRUPT__093` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-STATISTICAL` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=STATISTICAL；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執STATISTICAL的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-c1e78dc0b83c201c0912"></a>
#### AC-C39-JOURNEY-SEMANTIC_JUDGE

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；judge未校準/不同rubric卻聲稱一致
- **Source** `BODY-07:7063`，原 Oracle `AC-C39-JOURNEY-SEMANTIC_JUDGE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；SEMANTIC_JUDGE的required inputs全綁且原source適用；原SRC-L-001:L538，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/SEMANTIC_JUDGE` | `SBL DOC08:L485` 原規則 `L3948 CONDITIONAL: RUNTIME benchmark with calibrated dataset+confidence; no stand-alone releas` | `consumer_entrypoint and user_outcome_defined and supported_kind && SEMANTIC_JUDGE_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `rubric_sha+judge_model_pin+human_calibration` → `scores+disagreements`；`calibrated_rubric / model+human calibration+disagreement` | `/outcome/journey/semantic_judge := __CORRUPT__094` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-SEMANTIC_JUDGE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=SEMANTIC_JUDGE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執SEMANTIC_JUDGE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-476cb278d019ee4923a3"></a>
#### AC-C39-JOURNEY-HUMAN

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；Maker冒Human或決議是另一scope
- **Source** `BODY-07:7130`，原 Oracle `AC-C39-JOURNEY-HUMAN`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；HUMAN的required inputs全綁且原source適用；原SRC-L-001:L539，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/HUMAN` | `SBL DOC08:L486` 原規則 `L3949 CONDITIONAL: human rights/risk veto + signed rubric; never sole oracle for deterministic` | `consumer_entrypoint and user_outcome_defined and supported_kind && HUMAN_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `rubric+principal+consent_or_basis` → `signed_human_decision`；`rights_veto / real authorized principal, consent and signed decision` | `/outcome/journey/human := __CORRUPT__095` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-HUMAN` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=HUMAN；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執HUMAN的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：

<a id="current-80056106d0d568d25b6c"></a>
#### AC-C39-JOURNEY-COMPOSITE

- **原 NEG 本版有效保留**：只有零件測試沒有使用者成果；刪hard component或soft分數蓋hard fail
- **Source** `BODY-07:7196`，原 Oracle `AC-C39-JOURNEY-COMPOSITE`；只能由該原 protected checker 讀其適用 Raw/Oracle，不由作者推論 PASS。
- trigger/input：本TestClass domain=JOURNEY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- applicability/source：原使用者Goal/FUO跨邊鏈已定義；COMPOSITE的required inputs全綁且原source適用；原SRC-L-001:L540，SHA `0af1fd914a2bbb1f3221c4959facc6d0bbb4b43d4a6d385ed57f9cde8f8eab99`。
- 原條款：| `JOURNEY/COMPOSITE` | `SBL DOC08:L487` 原規則 `L3950 CONDITIONAL: RUNTIME typed property/reference/composite defined with source and fixtures` | `consumer_entrypoint and user_outcome_defined and supported_kind && COMPOSITE_inputs_bound`；requires consumer entrypoint/outcome and product-kind; real end-user result | `components+ordering+failure_policy` → `component_raw_receipts`；`all_hard_and / ordered hard component receipts` | `/outcome/journey/composite := __CORRUPT__096` → `FUNCTIONAL_CONSUMER_MISSING`；`AC-C39-JOURNEY-COMPOSITE` | `CONDITIONAL_ON_SOURCE_INPUT; live `REQUIRED/CONDITIONAL/N_A_REASONED/HOLD` after Owner predicate & DOC07 native ALL`；原 Oracle Owner=PIPD DOC07，SBL Reader/Checker；`NOT_EXECUTED` |
- trigger/input：本TestClass domain=JOURNEY，Oracle=COMPOSITE；同Subject/scope/source。實際私有CLI Raw refs=['CLI-POS-EMPTY-LIST', 'CLI-POS-ADD', 'CLI-POS-LIST-FRESH-PID', 'CLI-ROLLBACK-REMOVE', 'CLI-JOURNEY-FINAL-EMPTY']；無Raw不可假裝已跑Native。
- transform/typed output：先執JOURNEY專屬domain_predicate，再執COMPOSITE的機制，回AUTHOR.LocalOracleOutcome(case_id,verdict,first_fail,claim_ceiling)。
- POS domain與oracle輸入：


---




## 本版未受影條文（完整沿用、當期生效）

## R2-07-AC：15 條異構Edge與三種Challenge效果

A READONLY只讀Frozen Readset；B ADVISORY_LOCAL_WRITE只寫隔離建議；C CHECKER_INBOX_EFFECT寫原受保護inbox必走原OPS/ACL。Protected Checker與Challenge是不同principal，Maker無權簽Independent PASS。每邊先核特定payload type，再核required、source/candidate/receiver與domain；不能使用同一SourceRef/RawRef袋子代替全部ABI。

以下type_tag是作者端Reader投影辨識符，並非新Native `$id`。PIPD原型別用BODY-02的真Registry `$id`；Queue/Wake/Checker等需原Host Reader回schema/version/hash，不存在時ABI_BIND_HOLD。設計測試只能驗拒收形狀及scope；正式ACK必由列出的原Receiver產生。
## R2-07-H4-SEAM：12 H4與11 SEAM保持原Oracle

| 原Gate/Source | 原業務契約 | 原POS/NEG/退出 |
|---|---|---|
| H4-01 Fresh Context / SRC-01:L202 | 原 checker_principal, loaded_history_ids, write_cap → fresh-context-proof；Consumer/Owner Checker Registry；換真獨立 context／re-run；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS checker≠maker、無重疊私有歷史、無受審檔寫權；NEG 看過 Maker private notes 或可寫候選 → CHECKER_CONTEXT_TAINTED；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-02 Frozen Binding / SRC-01:L203 | 原 subject sha, source manifest, raw refs → exact-hash-binding；Consumer/Owner Source Owner；重凍結後重測；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 每個 SourceLocator 可讀且 sha 與 frozen 一致；NEG source[3] 漂移 → FROZEN_BINDING_MISMATCH；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-03 A∪B∪C / SRC-01:L204 | 原 stable A/B/C IDs, waiver → attack union ledger；Consumer/Owner Challenge Owner；補原攻擊而非改分母；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS A={x,y}, B={y,z}, C={w} 得唯一 4 件且都有 disposition；NEG count=3 或藏未測 → ATTACK_DENOMINATOR_UNDERCOUNT；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-04 Anti-Correlation / SRC-01:L205 | 原 high-risk flags, challenge origin/principal → independence matrix；Consumer/Owner Protected Checker；獨立再生案例；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 高風險有至少一條非 Maker 派生的攻擊與新 context；NEG tests 全取同一 Maker Memo → CORRELATED_BLIND_SPOT；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-05 11 Seams / SRC-01:L206 | 原 seam_case_ids[11]，tamper fields → SeamTestLedger；Consumer/Owner Security/Native Owners；逐 Seam 真測；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 11 個不同故障面各一正一負且對應不同 FirstFail；NEG 11 個僅改標題、未實測 → SEAM_UNTESTED；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-06 Next-Wave / SRC-01:L207 | 原 current+next-wave consumer, policy → under-enforcement check；Consumer/Owner Policy Owner；保持拒收；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 當前沒消費但 next-wave 仍必拒過期權；NEG no current reader 竟豁免 → NEXT_WAVE_UNDERENFORCED；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-07 Regression Retention / SRC-01:L208 | 原 previous F IDs, new SHA, change cone → regression matrix；Consumer/Owner Regression Owner；舊判決保留；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 過往 F17 仍在新 SHA 重測集，除非受權變更；NEG 靜默刪 prior rejection → REGRESSION_SILENT_DROP；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-08 Two-Pass Blind / SRC-01:L209 | 原 PassA seal time/SHA, PassB open time → order proof；Consumer/Owner Checker Owner；新 Session 重新盲審；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS A immutable frozen 後才開 B，能重算 timestamp；NEG B 先開或封印被改 → BLIND_REVIEW_INVALID；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-09 Dual Axis / SRC-01:L210 | 原 candidate truth, reviewer process qualified → two-axis result；Consumer/Owner AO；分軸判斷不可平均；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS candidate=FAIL、process=PASS 時全案仍 HOLD；NEG reviewer 合格便宣稱 candidate PASS → DUAL_AXIS_COLLAPSE；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-10 Native Receipt / SRC-01:L211 | 原 issuer/subject/raw digest/sig → trusted binding；Consumer/Owner HGK Native Owner；驗真 key/ACL；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS sig+scope+raw 同 Subject 有效；NEG S2 收據重播給 S1 → NATIVE_RECEIPT_SUBJECT_MISMATCH；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-11 RepairCone / SRC-01:L212 | 原 first failing invariant, DAG, legal writeset → minimal repair cone；Consumer/Owner Maker/Repair Owner；用受限 L2 ECP；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 只修依賴受影最小集合，重測對應案；NEG 擴寫無關 Source/Oracle → REPAIR_SCOPE_OVERREACH；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| H4-12 PRE-W3 / SRC-01:L213 | 原 first W3 packet, SWOF Gate, dispatch raw → non-dispatch proof；Consumer/Owner SWOF Owner；正式 Gate 前只 shadow；本版只產 H4CaseProposal，Reader=Protected AO/適用 Reviewer。 | POS 沒正式 Gate 時 NOT_DISPATCHED 可驗；NEG 無 Gate 卻寫 W3 → PREW3_GATE_BYPASS；FirstFail 受影 H4 停止，原 Checker Owner 證明退出／重測，不影響無關案。 |
| SEAM-01 Activation / SRC-01:L221 | host_loader.trigger_route 必註冊；受影 Domain Reader=Host Operator。 | 合法 Skill 真觸發；不存在 route 卻稱 Active → HOST_NOT_EFFECTIVE；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-02 Pre-gate bypass / SRC-01:L222 | gate.receipt_ref 在 dispatch 前驗；受影 Domain Reader=HGK Issuer/Receiver。 | 有權 Gate 先於 effect；dispatch_at<admit_at → PRE_GATE_BYPASS；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-03 Input downgrade / SRC-01:L223 | schema_version/security attributes 不降；受影 Domain Reader=Schema/PIPD Owner。 | 不變欄被保留；v1 threat fields 被刪成 v0 → SCHEMA_DOWNGRADE_DENIED；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-04 Internal Oracle / SRC-01:L224 | oracle.principal_id != maker；受影 Domain Reader=Oracle/Checker Owners。 | 有權 Checker 真分離；Maker 上白名單 → TQ_SOD；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-05 Canonical Owner / SRC-01:L225 | pi.writer_namespace 唯 PIPD；受影 Domain Reader=PIPD Owner。 | 正式 PI Writer 正確；SBL 假 PI → SECOND_CANONICAL_WRITER；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-06 Fallback compatibility / SRC-01:L226 | provider-off 必保持 Required FUO；受影 Domain Reader=Product/Host Owner。 | fallback 有同等 FUO；缺 delete 仍稱 parity → PROVIDER_OFF_FUO_LOSS；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-07 Alternate route / SRC-01:L227 | 每條 route 保持 issuer authority；受影 Domain Reader=HGK/SWOF Owners。 | 本地與連線 Route 不換權威；secondary local grant → WRONG_AUTHORITY_GRANT；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-08 Post-gate effect / SRC-01:L228 | Dispatch 實時 nonce/expiry valid；受影 Domain Reader=HGK Receiver。 | 當下可驗效期；plan 後過期仍動手 → POST_GATE_PERMISSION_EXPIRED；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-09 Replay/stale / SRC-01:L229 | nonce/op_id at-most-once；受影 Domain Reader=Hermes/Issuer。 | Unknown 先 readback；timeout blind retry → EFFECT_REPLAY_DENIED；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-10 TOCTOU / SRC-01:L230 | repo_context.head_sha 鎖 preimage；受影 Domain Reader=L2 Repo Owner。 | 写前 HEAD 同凍結版；中途漂移 → TOCTOU_REPO_HEAD；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |
| SEAM-11 Exact evidence / SRC-01:L231 | raw_receipt.subject_sha 同候選；受影 Domain Reader=Evidence/Checker Owner。 | candidate/raw/manifest exact match；舊 SHA Raw 冒用 → RAW_SUBJECT_MISMATCH；FirstFail 停受影 Receiver；原 Owner 更正/驗原 Raw 後才可重入。 |

## R2-07-ACTUAL-ACCEPTANCE：原Spine Reader的證據邊界

原`C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\spine.py:460` SHA `f99a402123f39b8ceaad9372aeec0555628ba643950a5c99a4c917fd9e6d6dcd` 的`resolve_acceptance`有requirement_id、registered evidence ref、lease actor/token、expected_version、idempotency_key與NOT_RUN→PASS/FAIL單次transaction限制。這不是Maker許可；原Checker權責仍在原Host。

該原函式docstring明示：evidence_refs沒有subject/requirement欄，目前只能證明evidence_ref已註冊，不能證明evidence確屬本subject。本候選對foreign-evidence的拒收要求不能冒稱原Native現已實現；必由原HGK Evidence/Checker Owner綁subject-bound registry或原兼容Reader，並以foreign evidence NEG驗實後才給Native PASS。本輪作者guard只驗拒收設計，不修改schema.sql或原DB，不新增Checker。

NEG：註冊但來自另一subject的evidence_ref不得僅因exists就接受。受影scope為AC-E09/12/13及欲借該Raw結案的B1 Case；其他來源/設計Reader繼續。Next legal action：原Owner對同candidate/requirement的evidence binding做兼容遷移與原Checker回歸，保留舊journal和history。
