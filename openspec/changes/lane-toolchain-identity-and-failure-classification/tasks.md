## 1. T1 — Toolchain resolver

- [x] T1.1 Define the declared lane-toolchain identity as one source: declared binary path + expected version + expected sha256
  — evidence: tests/w3_solution/test_lane_toolchain_resolver.py ; tests/w3_solution/test_lane_toolchain_resolver.py::test_matching_identity_resolves_and_prints_path_sha_version
- [x] T1.2 Implement `scripts/hgk-lane-toolchain.py` to resolve the binary from the declared identity and print path + sha256 + `--version`
  — evidence: tests/w3_solution/test_lane_toolchain_resolver.py ; tests/w3_solution/test_lane_toolchain_resolver.py::test_matching_identity_resolves_and_prints_path_sha_version ; tests/w3_solution/test_lane_toolchain_resolver.py::test_cli_check_bin_prints_only_the_path
- [x] T1.3 Fail closed: a resolved build whose version differs from the declared one exits non-zero with a typed error naming the offending build (path + version)
  — evidence: tests/w3_solution/test_lane_toolchain_resolver.py ; tests/w3_solution/test_lane_toolchain_resolver.py::test_version_mismatch_fails_closed_and_names_offending_build ; tests/w3_solution/test_lane_toolchain_resolver.py::test_digest_mismatch_fails_closed_and_names_offending_build ; tests/w3_solution/test_lane_toolchain_resolver.py::test_missing_declaration_and_binary_fail_closed
- [ ] T1.4 No ad-hoc discovery: the resolver and its callers use no `find` / `command -v`

## 2. T2 — Bounded pre-lane identity preflight + typed classification

- [ ] T2.1 Implement the preflight as a one-line echo with a `<=120s` budget, run BEFORE any long lane
- [x] T2.2 Classify a models-cache schema error (`failed to load models cache: missing field ...`) as `LANE_TOOLCHAIN_MISMATCH`
  — evidence: tests/w3_solution/test_lane_preflight_classification.py ; tests/w3_solution/test_lane_preflight_classification.py::test_models_cache_schema_error_is_harness_fault
- [x] T2.3 Classify `Model metadata for <model> not found` as `LANE_TOOLCHAIN_MISMATCH`
  — evidence: tests/w3_solution/test_lane_preflight_classification.py ; tests/w3_solution/test_lane_preflight_classification.py::test_model_metadata_not_found_is_harness_fault
- [x] T2.4 Classify an unknown subcommand/flag and the unsupported stdin form (`error: unexpected argument '-' found`) as `LANE_TOOLCHAIN_MISMATCH`
  — evidence: tests/w3_solution/test_lane_preflight_classification.py ; tests/w3_solution/test_lane_preflight_classification.py::test_unexpected_argument_stdin_form_is_harness_fault ; tests/w3_solution/test_lane_preflight_classification.py::test_unknown_subcommand_and_unknown_flag_are_harness_faults
- [x] T2.5 Classify a genuine provider refusal on the declared model (build otherwise matching) as `LANE_MODEL_REFUSED`
  — evidence: tests/w3_solution/test_lane_preflight_classification.py ; tests/w3_solution/test_lane_preflight_classification.py::test_genuine_provider_refusal_maps_to_model_refused
- [x] T2.6 Record the preflight raw output and the resulting error class
  — evidence: tests/w3_solution/test_receipt_schema.py ; tests/w3_solution/test_receipt_schema.py::test_preflight_receipt_carries_all_additive_fields

## 3. T3 — Wire into the lane launcher

- [x] T3.1 The lane launcher resolves its binary via `scripts/hgk-lane-toolchain.py` before spawning any turn
  — evidence: tests/w3_solution/test_substitution_gate.py ; tests/w3_solution/test_substitution_gate.py::test_resolver_failure_refuses_before_any_deviation_or_lane
- [x] T3.2 The preflight runs before the long lane and its typed result gates the turn
  — evidence: tests/w3_solution/test_substitution_gate.py ; tests/w3_solution/test_substitution_gate.py::test_mismatch_refuses_to_substitute_and_writes_no_deviation
- [x] T3.3 Only `LANE_MODEL_REFUSED` opens a declared model deviation; `LANE_TOOLCHAIN_MISMATCH` refuses to substitute and names the offending build
  — evidence: tests/w3_solution/test_substitution_gate.py ; tests/w3_solution/test_substitution_gate.py::test_mismatch_refuses_to_substitute_and_writes_no_deviation ; tests/w3_solution/test_substitution_gate.py::test_model_refused_may_open_a_declared_deviation_with_receipt_fields
- [ ] T3.4 No lane script performs binary discovery with `find` / `command -v`

## 4. T4 — Tests

- [x] T4.1 Resolver: a matching declared identity resolves; a mismatched version fails closed
  — evidence: tests/w3_solution/test_lane_toolchain_resolver.py ; tests/w3_solution/test_lane_toolchain_resolver.py::test_matching_identity_resolves_and_prints_path_sha_version ; tests/w3_solution/test_lane_toolchain_resolver.py::test_version_mismatch_fails_closed_and_names_offending_build
- [x] T4.2 Classifier positive/negative/boundary for each signature in T2.2-T2.5 on recorded raw samples
  — evidence: tests/w3_solution/test_lane_preflight_classification.py ; tests/w3_solution/test_lane_preflight_classification.py::test_combined_real_failing_log_is_harness_fault_no_substitution ; tests/w3_solution/test_lane_preflight_classification.py::test_empty_output_is_inconclusive ; tests/w3_solution/test_lane_preflight_classification.py::test_provider_error_without_account_language_is_not_a_deviation
- [x] T4.3 Substitution refused under `LANE_TOOLCHAIN_MISMATCH`; permitted under `LANE_MODEL_REFUSED`
  — evidence: tests/w3_solution/test_substitution_gate.py ; tests/w3_solution/test_substitution_gate.py::test_mismatch_refuses_to_substitute_and_writes_no_deviation ; tests/w3_solution/test_substitution_gate.py::test_model_refused_may_open_a_declared_deviation_with_receipt_fields
- [ ] T4.4 Determinism: no test depends on the network, a real model, the relay, or the developer's real Codex home
- [x] T4.5 The named suite for this surface passes as a whole
  — evidence: tests/w3_solution (39 passed) ; `cd HG && python -m pytest tests/w3_solution -q` -> 39 passed in 46.67s ; `cd HG/tests/w3_solution && python -m pytest -q` -> 39 passed in 44.94s ; see evidence/APPLIED_W3_RECEIPT_V3.json

## 5. T5 — Receipt schema

- [x] T5.1 Add `codex_cli`, `codex_cli_version`, `declared_model`, `served_model`, `error_class`, `preflight_raw` to the receipt
  — evidence: tests/w3_solution/test_receipt_schema.py ; tests/w3_solution/test_receipt_schema.py::test_preflight_receipt_carries_all_additive_fields
- [x] T5.2 Populate the fields on every preflight run; `served_model` is `null` when no turn was served
  — evidence: tests/w3_solution/test_receipt_schema.py ; tests/w3_solution/test_receipt_schema.py::test_preflight_receipt_carries_all_additive_fields ; tests/w3_solution/test_receipt_schema.py::test_served_model_is_null_when_no_turn_is_served
- [x] T5.3 Additive only: an existing consumer matching the old fallback code keeps working
  — evidence: tests/w3_solution/test_receipt_schema.py ; tests/w3_solution/test_receipt_schema.py::test_old_fallback_consumer_keeps_working_on_the_new_receipt

## 6. T6 — Docs + governance rule

- [ ] T6.1 Document the declared lane-toolchain identity and how to read the resolver output (path + sha256 + `--version`)
- [ ] T6.2 Document the typed code table (`LANE_TOOLCHAIN_MISMATCH` vs `LANE_MODEL_REFUSED`) and the substitution gate
- [ ] T6.3 Document the verdict-binds-bytes rule (a post-verdict rebuild / digest refresh / published-asset replacement invalidates the verdict) as policy; its enforcement is out of scope here

## 7. Verification and closure

- [ ] 7.1 Candidate-only constants hold: no promotion, no archive, no main-spec write, no `config/` or route edit, everything additive
- [ ] 7.2 No task in this change is marked done: the round is a candidate, not an acceptance
