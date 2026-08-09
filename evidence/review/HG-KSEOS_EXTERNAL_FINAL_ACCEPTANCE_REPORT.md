# HG-KSEOS External Final Acceptance Report

- **Status**: EXTERNAL_FINAL_ACCEPTANCE_PENDING
- **Production**: NOT_CLAIMED
- **Checked at**: 2026-08-09T07:47:41.366149+00:00

## Candidate identity

| Field | Value |
|---|---|
| Final HEAD | `908501df14b25e11e3191237cd508e79ff73c4aa` |
| Package | `var/releases/HG-KSEOS_LOCAL_CANDIDATE.zip` |
| Package SHA-256 | `8b30df8fccad0716a523012398ddf7705a472b38219ab98bebf9c3a20682c59b` |
| Package bytes | 26613945 |
| Payload files | 361 |
| TST-092 | INDEPENDENT_CASE_PASS (same HEAD + same package) |

## Test denominator reconciliation (§23)

| Component | Count |
|---|---|
| core_product_tests | 16 |
| user_experience_reducer_tests | 1 |
| workbench_integration_tests | 1 |
| tool_adapter_tests | 0 (adapters covered in workbench/e2e) |
| other_discovered_tests | 0 |
| **total_discovered_tests** | 18 (sum(parts)==total: True) |

Lineage: 101 (pre-UECX) → 110 (101+9 UX reducer) → 119 (110+9 fail-closed F5 tests). Current = discovered files, not hardcoded.

## Denominators

- Obsidian official feature accounting: 32/32, unknown=0 (REQUIRED_AND_PASS=19)
- Obsidian HGK functions: 30/30, unknown=0
- LLM Wiki native: 16/16, unknown=0
- LLM Wiki 40-capability crosswalk: 31 RUNTIME_PASS + 5 SUPPORTED_NOT_REQUIRED + 3 HGK-adjacent + 1 credential-gated, fail=0

## Workbench

- WB E2E: 21/21 PASS
- No-brain canary: PASS
- Workbench full acceptance: 12/12 PASS
- UECX: scan PASS; crosswalk errors all zero; raw_missing=0, independent_missing=0
- UserExperienceReducer v1 exit: 0

## Hard checks

- FAIL tree_clean
- PASS final_head_matches
- PASS final_package_matches
- PASS tst092_independent_pass
- PASS blocking_tt_zero
- PASS uecx_scan_complete
- PASS uecx_crosswalk_zero
- PASS uecx_raw_zero
- PASS uecx_independent_zero
- PASS obsidian_identity_resolved
- PASS obsidian_official_denominator
- PASS obsidian_hgk_functions
- PASS llmwiki_identity_resolved
- PASS llmwiki_native_denominator
- PASS llmwiki_40cap_zero_fail
- PASS workbench_e2e_pass
- PASS no_brain_canary_pass
- PASS ux_reducer_exit_zero
- PASS canonical_authority_violation_zero
- PASS secret_leak_zero
- PASS unadmitted_provider_zero
- PASS unapproved_plugin_zero
- PASS denominator_sum_matches

## Tools

- **Obsidian**: 1.13.4 [catalyst (Early access)], official CLI binary `Obsidian.com` present (enablement = user Settings toggle), community plugins DENY_BY_DEFAULT (zero installed), rollback = 1.12.7 public.
- **LLM Wiki**: atomicstrata/llm-wiki-compiler package `llm-wiki-compiler` v1.1.0 (MIT), npm pin, isolated prefix. RETAINED per §11 (working tool, all hard tests pass; task-seed candidates nvk/jackwener/Pratiyush/nashsu evaluated in drift research — not installed identity, no material misfit).

## Decision

**EXTERNAL_FINAL_ACCEPTANCE_PENDING** — production NOT_CLAIMED.
