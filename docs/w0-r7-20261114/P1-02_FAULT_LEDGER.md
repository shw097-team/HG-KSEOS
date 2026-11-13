# P1-02 故障分帳台帳（HGK suite 83 failed + 16 errors）

- 產出時間：2026-11-14T01:25:01+08:00
- 台帳 JSON：`C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\W0_R7_FULL_20261114\out\P1-02_FAULT_LEDGER.json`（83879 B，sha256 `0dd54e26c331e72a…`）
- 輸入（唯讀，未修改）：`_local/evidence/hgk_suite_r4_lines.txt` sha256 `df451f929ab122c3…`（69708 B）、
  `_local/W0_R1_V5_FAULT_CLASSES.json` sha256 `e8e00e92e373e0df…`（9319 B）
- Claim 上限：LOCAL_CHECK - a re-classification of bytes already on disk on this host. No test was re-run, no origin file was modified, nothing here is an acceptance, an admission or a release.

## 1. 結論

| 指標 | 值 |
|---|---:|
| `total_events` | **99** |
| `failed` | **83** |
| `errors` | **16** |
| `UNCLASSIFIED` | **0** |

逐類別：Real Defect `2`、Historical `5`、Env `15`、Original Owner `55`、
W1 wiring `22`、Unclassified `0` — 合計 `99`。

## 2. 分母對帳（83 + 16 是否等於 JSON 內計數）

| 來源 | failed | errors | total |
|---|---:|---:|---:|
| baseline P1-02 宣告 | 83 | 16 | 99 |
| 本台帳逐一列舉 | 83 | 16 | 99 |
| **差額** | **0** | **0** | **0** |

- 逐筆 CaseID 直接取自 r4 短摘要的 `FAILED` / `ERROR` 行（原文照抄，未改寫、未合併）。
- 該次 runner 自己的結尾行：`83 failed, 644 passed, 22 skipped, 4 xfailed, 16 errors, 28 subtests passed in 111.43s (0:01:51)` — 與 83/16 一致。
- 差額為 0，**沒有湊數**：JSON 內 `denominator.reconciled = true`。

**必須明講的一點（避免「33 案例冒 83」）**：`W0_R1_V5_FAULT_CLASSES.json` 分帳的是 **r1**（171 failed / 17 errors = 188 事件），
其四類合計只有 `153` 筆，**r1 自身就有 35 筆未入帳**；
它不含 r4 的逐案 CaseID。因此本台帳的列舉來源是 r4 日誌，V5 只用於類別定義、owner 對照與樣本文字。
baseline §12 僅具名 33 筆（14 historical / 5 epoch / 13 assertion / 1 native）；本台帳列滿 99 筆，較其多出 66 筆，
其中 50 failed + 16 errors 正是 baseline 標記為「待 Raw 分帳」的部分。

## 3. 類別與計數

| class | failed | errors | total | next-action owner |
|---|---:|---:|---:|---|
| `REAL_DEFECT` | 2 | 0 | 2 | HG-KSEOS owning repo (scoped diff) |
| `HISTORICAL` | 5 | 0 | 5 | origin repo (evidence exists there, not imported by policy) |
| `ENV` | 7 | 8 | 15 | this construction root / host |
| `ORIGINAL_OWNER` | 55 | 0 | 55 | HGK Native Issuer (H2) / HG-KSEOS owner (H1 epoch) |
| `W1_WIRING` | 14 | 8 | 22 | W1 wiring (imports, entry points, addendum script) |
| `UNCLASSIFIED` | 0 | 0 | 0 | - |
| **total** | **83** | **16** | **99** | |

| class | reason key | cases |
|---|---|---:|
| `ORIGINAL_OWNER` | `bundle` | 45 |
| `ORIGINAL_OWNER` | `epoch_drift` | 10 |
| `W1_WIRING` | `missing_script` | 8 |
| `W1_WIRING` | `mod_import` | 8 |
| `ENV` | `frontdoor_bare` | 6 |
| `ENV` | `root_abs` | 5 |
| `HISTORICAL` | `historical_deliv` | 3 |
| `W1_WIRING` | `exit2_family` | 3 |
| `HISTORICAL` | `toolchain_decl` | 2 |
| `W1_WIRING` | `spawn_fnf` | 2 |
| `ENV` | `control_fnf` | 1 |
| `ENV` | `appdata_ver` | 1 |
| `ENV` | `w3_fixtures` | 1 |
| `ENV` | `frontdoor_dep` | 1 |
| `REAL_DEFECT` | `nameerror` | 1 |
| `REAL_DEFECT` | `guide_digest` | 1 |
| `W1_WIRING` | `cli_crash` | 1 |

類別對照（與舊四桶）：`ORIGINAL_OWNER → ORIGINAL_OWNER_HOLD`、`HISTORICAL → HISTORICAL_FIXTURE_EXCLUDED`、
`ENV / W1_WIRING → PATH_ABI 拆分`、`REAL_DEFECT → REAL_DEFECT`。
舊四桶合計：{"REAL_DEFECT": 2, "HISTORICAL_FIXTURE_EXCLUDED": 5, "PATH_ABI": 37, "ORIGINAL_OWNER_HOLD": 55, "unmapped": 0}。

## 4. 受影波次（affected_wave）

| wave | cases | 定義 |
|---|---:|---|
| W0 | 17 | 可在本施工根內收斂（路徑/版面、host 依賴、P1 scoped defect） |
| W1 | 32 | 需 W1 接線（import/entry）或第一批所需的單一 epoch 正規化 |
| W2 | 45 | 需 owner native 發行（bundle + permit，HOLD H2） |
| ORIGIN | 5 | 需回原 repo（歷史證據、RCA 產物重建） |

## 5. 未分類與證據等級

- `UNCLASSIFIED = 0`：沒有把任何一筆丟進「不知道」桶；每一筆都有實測例外訊息、實測 ERROR 區塊，或在
  `evidence_grade` 明示其為 setup 同源 / 推論。
- 證據等級分佈：{"MEASURED_MESSAGE_1TO1": 80, "INFERRED_EXIT2_FAMILY": 3, "MEASURED_BLOCK": 10, "SAME_SETUP_FIXTURE": 6}

## 6. 方法（可稽核）

- CaseIDs taken verbatim from the r4 short-summary FAILED/ERROR lines (99 node ids, no paraphrase).
- The r4 log's FAILURES section is stripped of per-test header frames, so each failure's exception line was paired positionally with the summary: 83 E-lines for 83 FAILED lines, one E per failure, both in report order. Two independent anchors confirm the pairing (index 58 carries its '- hg_k...' suffix on the summary line itself; index 66's message 'expected a typed repo-head refusal, got InvariantViolation(ERR_NATIVE_BUNDLE_REQUIRED)' is the same string V5 records as its ORIGINAL_OWNER_HOLD sample).
- Classes are the six required buckets; class_in_v5 records how each maps onto the older four-bucket taxonomy (W1_WIRING splits out of PATH_ABI).
- Where the log is thin the row says so in evidence_grade (SAME_SETUP_FIXTURE for the 6 message-less frontdoor setups, INFERRED_EXIT2_FAMILY for the 3 exit-code-only mandate cases), instead of being quietly re-bucketed.

## 7. 限制

- No test was re-run in this round; every verdict is a reading of the recorded r4 bytes.
- Positional pairing is an inference about log structure, evidenced by the two anchors above; it would be voided if the log had dropped or merged an error line. The 1:1 count and the anchors are the guard against that.
- The 45 ERR_NATIVE_BUNDLE_REQUIRED cases are classified by the refusal they raise, not by what the test intended to assert; if an owner bundle were supplied the underlying assertions are untested and could still fail.
- Reasons cite paths as they appear in the r4 log; existence checks were made against the tree as it stands today, so an ABSENT-then / PRESENT-now path is reported as path drift, not as a defect.

## 8. 附錄：99 筆逐案

| # | case_id | status | class | wave | reason key |
|---:|---|---|---|---|---|
| 1 | `tests/test_controls_observability_repo.py::ControlValidationTests::test_all_materialized_controls_have_effective_contracts` | FAILED | `ENV` | W0 | `control_fnf` |
| 2 | `tests/test_cs_a_gate_repair.py::D2ProjectScopedRequirementTests::test_existing_req_001_collision_avoided` | FAILED | `ENV` | W0 | `root_abs` |
| 3 | `tests/test_cs_a_gate_repair.py::D2ProjectScopedRequirementTests::test_requirement_id_is_project_scoped` | FAILED | `ENV` | W0 | `root_abs` |
| 4 | `tests/test_cs_a_gate_repair.py::D4PendingWorkCannotDeliverTests::test_delivered_allowed_when_workorders_terminal` | FAILED | `ENV` | W0 | `root_abs` |
| 5 | `tests/test_cs_a_gate_repair.py::D4PendingWorkCannotDeliverTests::test_delivered_rejected_when_workorders_open` | FAILED | `ENV` | W0 | `root_abs` |
| 6 | `tests/test_cs_a_gate_repair.py::D5OrdinaryUserFlowTests::test_start_to_admit_no_spine_workaround` | FAILED | `REAL_DEFECT` | W0 | `nameerror` |
| 7 | `tests/test_cs_a_gate_repair.py::D6DenominatorTests::test_denominator_cli` | FAILED | `W1_WIRING` | W1 | `cli_crash` |
| 8 | `tests/test_cs_a_gate_repair.py::D6DenominatorTests::test_denominator_materializes_full_project` | FAILED | `ENV` | W0 | `root_abs` |
| 9 | `tests/test_delivery_manifest_counts.py::test_manifest_counts_are_the_delivered_counts` | FAILED | `HISTORICAL` | ORIGIN | `historical_deliv` |
| 10 | `tests/test_delivery_manifest_counts.py::test_every_manifest_row_carries_a_digest` | FAILED | `HISTORICAL` | ORIGIN | `historical_deliv` |
| 11 | `tests/test_delivery_manifest_counts.py::test_release_record_matches_the_published_assets` | FAILED | `HISTORICAL` | ORIGIN | `historical_deliv` |
| 12 | `tests/test_e2e_vertical_slice.py::VerticalSliceTests::test_requirement_to_evidence_to_rollback_slice` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 13 | `tests/test_far_lane_fix_20261015.py::TestP0PinAssert::test_current_pin_verifies` | FAILED | `HISTORICAL` | ORIGIN | `toolchain_decl` |
| 14 | `tests/test_far_lane_fix_20261015.py::TestP0PinAssert::test_digest_mismatch_is_typed_not_a_spawn` | FAILED | `HISTORICAL` | ORIGIN | `toolchain_decl` |
| 15 | `tests/test_far_lane_fix_20261015.py::TestP1MandateConsumer::test_inactive_lane_refuses` | FAILED | `W1_WIRING` | W1 | `exit2_family` |
| 16 | `tests/test_far_lane_fix_20261015.py::TestP1MandateConsumer::test_missing_file_refuses` | FAILED | `W1_WIRING` | W1 | `exit2_family` |
| 17 | `tests/test_far_lane_fix_20261015.py::TestP1MandateConsumer::test_owner_order_mandate_resolves` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 18 | `tests/test_far_lane_fix_20261015.py::TestP1MandateConsumer::test_verify_security_mandate_resolves` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 19 | `tests/test_far_lane_fix_20261015.py::TestP1MandateConsumer::test_wrong_model_in_pool_refuses` | FAILED | `W1_WIRING` | W1 | `exit2_family` |
| 20 | `tests/test_g0_wave3_controls.py::G0ContinuationTests::test_denominator_exposes_open_scope_signal` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 21 | `tests/test_g0_wave3_controls.py::G0ContinuationTests::test_required_scope_without_workorders_fails_closed` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 22 | `tests/test_g0_wave3_controls.py::G0DynamicDenominatorTests::test_expand_denominator_absorbs_new_requirement` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 23 | `tests/test_g0_wave3_controls.py::G0CompletionSweepTests::test_sweep_classifies_auto_local` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 24 | `tests/test_g0_wave3_controls.py::G0CompletionSweepTests::test_sweep_detects_unadmitted_required_scope` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 25 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_dotdot_escape_to_protected_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 26 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_execute_code_relative_from_parent_cwd_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 27 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_execute_code_under_protected_cwd_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 28 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_relative_path_under_protected_cwd_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 29 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_terminal_mentioning_protected_root_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 30 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_terminal_relative_from_parent_cwd_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 31 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_terminal_relative_write_under_protected_cwd_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 32 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_maker_write_inside_protected_denied` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 33 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_neg_malformed_stdin_nonzero_and_not_bare_allow` | FAILED | `W1_WIRING` | W1 | `spawn_fnf` |
| 34 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_absent_session_id_free_text_is_answered_not_an_outage` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 35 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_absent_session_id_is_answered_not_an_outage` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 36 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_checker_write_allowed` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 37 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_non_governed_session_write_allowed` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 38 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_null_session_id_is_answered_not_an_outage` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 39 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_ordinary_read_allowed` | FAILED | `W1_WIRING` | W1 | `spawn_fnf` |
| 40 | `tests/test_governed_runtime_controller.py::GovernedRuntimeController::test_pos_write_outside_protected_allowed` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 41 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_neg_effort_mismatch_is_refused` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 42 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_neg_mandate_effort_absent_from_pool_is_refused` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 43 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_neg_served_effort_mismatch_is_refused` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 44 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_neg_served_effort_without_a_mandate_effort_is_unverifiable` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 45 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_pos_lane_without_a_declared_effort_stays_a_pass_through` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 46 | `tests/test_lane_effort_enforcement.py::LaneEffortEnforcement::test_pos_matching_effort_passes` | FAILED | `W1_WIRING` | W1 | `missing_script` |
| 47 | `tests/test_lane_guard.py::TestLaneGuard::test_admit_with_receipt_evidence` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 48 | `tests/test_lane_guard.py::TestLaneGuard::test_declared_owner_ordered_pair_admits_with_conflict_id` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 49 | `tests/test_lane_guard.py::TestLaneGuard::test_distinct_pair_admits_without_declared_conflict` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 50 | `tests/test_lane_guard.py::TestLaneGuard::test_v3_bare_admitted_string_is_not_admissible` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 51 | `tests/test_lane_guard.py::TestLaneGuard::test_v4_omitted_provider_is_not_a_wildcard` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 52 | `tests/test_lane_guard.py::TestLaneGuard::test_v4_provider_mismatch_is_refused` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 53 | `tests/test_lane_policy.py::TestLanePolicyConformance::test_drift_injection_subcases` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 54 | `tests/test_lane_policy.py::TestLanePolicyConformance::test_registry_and_projection_shape` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 55 | `tests/test_lane_scope_isolation.py::LaneScopeIsolationTests::test_epoch_matches_between_assignment_and_registry` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 56 | `tests/test_lane_scope_isolation.py::LaneScopeIsolationTests::test_new_divergence_fails_and_known_residue_is_registered` | FAILED | `ORIGINAL_OWNER` | W1 | `epoch_drift` |
| 57 | `tests/test_matrix_d_full.py::M06::test_argv_require_arm_conflicting_with_mandate_refused_no_spawn` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 58 | `tests/test_matrix_d_full.py::M07::test_omitted_require_arm_cannot_escape_mandate` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 59 | `tests/test_matrix_d_full.py::M07::test_wrong_force_rank_refused - hg_k...` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 60 | `tests/test_matrix_d_full.py::M08::test_foreign_surface_usage_receipt_cannot_complete` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 61 | `tests/test_matrix_d_full.py::M08::test_mandated_surface_usage_receipt_completes_control` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 62 | `tests/test_matrix_m02_resume.py::M02ResumeRetention::test_resume_keeps_the_same_binding_and_forces_the_same_arm` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 63 | `tests/test_matrix_m02_resume.py::M02ResumeRefusesAnAlteredBinding::test_altered_arm_refuses_with_arm_mismatch` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 64 | `tests/test_matrix_m02_resume.py::M02ResumeRefusesAnAlteredBinding::test_altered_round_refuses_with_round_mismatch` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 65 | `tests/test_matrix_m02_resume.py::M02ResumeRefusesAnAlteredBinding::test_altered_session_no_longer_resolves_the_old_binding` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 66 | `tests/test_r13_repo_head_cwd.py::test_admission_uses_target_head_not_process_cwd` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 67 | `tests/test_r13_repo_head_cwd.py::test_admission_fails_closed_when_target_is_not_a_repo` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 68 | `tests/test_r13_repo_head_cwd.py::test_target_inside_another_repo_inherits_that_repo_head` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 69 | `tests/test_role_binding_enforcement.py::SpineConsumer::test_legacy_non_governed_row_unchanged` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 70 | `tests/test_role_binding_enforcement.py::SpineConsumer::test_negative_bound_wo_refuses_empty_evidence` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 71 | `tests/test_role_binding_enforcement.py::SpineConsumer::test_negative_bound_wo_refuses_replayed_foreign_receipt` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 72 | `tests/test_role_binding_enforcement.py::SpineConsumer::test_negative_self_checker_and_no_delivery` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 73 | `tests/test_role_binding_enforcement.py::SpineConsumer::test_positive_bound_wo_verified_with_exact_evidence` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 74 | `tests/test_role_binding_enforcement.py::DispatcherPreSpawn::test_prespawn_expired_binding_refused` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 75 | `tests/test_role_binding_enforcement.py::DispatcherPreSpawn::test_prespawn_require_arm_mismatch_refused_no_spawn` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 76 | `tests/test_role_binding_enforcement.py::DispatcherPreSpawn::test_prespawn_require_arm_omission_derives_mandatory_arm` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 77 | `tests/test_role_binding_enforcement.py::SessionBindingLookup::test_negative_blank_session_is_a_typed_refusal` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 78 | `tests/test_role_binding_enforcement.py::SessionBindingLookup::test_negative_different_session_workorder_is_not_returned_for_s` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 79 | `tests/test_role_binding_enforcement.py::SessionBindingLookup::test_negative_two_live_workorders_same_session_refuse_no_pick` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 80 | `tests/test_role_binding_enforcement.py::SessionBindingLookup::test_negative_unknown_session_returns_none_no_exception` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 81 | `tests/test_role_binding_enforcement.py::SessionBindingLookup::test_positive_single_live_match_returns_wo_and_binding_with_matching_digest` | FAILED | `ORIGINAL_OWNER` | W2 | `bundle` |
| 82 | `tests/test_task014_named_method_closure.py::CanonicalRuntimeTests::test_config_resolves_scheme_b_appdata_runtime` | FAILED | `ENV` | W0 | `appdata_ver` |
| 83 | `tests/test_task015_coherence_closure.py::GuideAndDeterminismTests::test_final_md_guide_projection_matches_actual_guide` | FAILED | `REAL_DEFECT` | W0 | `guide_digest` |
| 84 | `tests/test_acceptance_gate.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 85 | `tests/test_acceptance_resolution.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 86 | `tests/test_acceptance_runner.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 87 | `tests/test_agents_providers.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 88 | `tests/test_assurance.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 89 | `tests/test_autonomy_evolution.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 90 | `tests/test_bootstrap.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 91 | `tests/test_c2_case_run.py` | ERROR | `W1_WIRING` | W1 | `mod_import` |
| 92 | `tests/w3_solution - AssertionError: FIXTURES is not an existing directo...` | ERROR | `ENV` | W0 | `w3_fixtures` |
| 93 | `tests/test_frontdoor_active_policy.py::test_missing_designation_refuses_to_start` | ERROR | `ENV` | W0 | `frontdoor_dep` |
| 94 | `tests/test_frontdoor_active_policy.py::test_missing_designation_can_be_allowed_by_an_explicit_flag` | ERROR | `ENV` | W0 | `frontdoor_bare` |
| 95 | `tests/test_frontdoor_active_policy.py::test_designation_naming_another_policy_is_refused` | ERROR | `ENV` | W0 | `frontdoor_bare` |
| 96 | `tests/test_frontdoor_active_policy.py::test_designation_bound_to_exact_bytes` | ERROR | `ENV` | W0 | `frontdoor_bare` |
| 97 | `tests/test_frontdoor_active_policy.py::test_stale_designation_refuses_to_start` | ERROR | `ENV` | W0 | `frontdoor_bare` |
| 98 | `tests/test_frontdoor_active_policy.py::test_policy_edited_after_designation_is_refused` | ERROR | `ENV` | W0 | `frontdoor_bare` |
| 99 | `tests/test_frontdoor_active_policy.py::test_malformed_designation_is_typed_not_ignored` | ERROR | `ENV` | W0 | `frontdoor_bare` |
