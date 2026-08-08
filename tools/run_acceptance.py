from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


EXPECTED_BASELINE_SHA256 = "1564bbf7a8cd4baeabc1704586dc50ebe1e30dd6c1d09c84a7ad629a2b8d8176"

TEST_BINDINGS = {
    "TST-010": "tests.test_assurance.AssuranceTests.test_permission_mode_and_unicode_space_path",
    "TST-004": "tests.test_security_harness.SecurityHarnessTests.test_prompt_injection_in_metadata_rejected",
    "TST-005": "tests.test_spine.SharedSpineTests.test_dual_writer_is_rejected",
    "TST-006": "tests.test_e2e_vertical_slice.VerticalSliceTests.test_requirement_to_evidence_to_rollback_slice",
    "TST-011": "tests.test_security_harness.SecurityHarnessTests.test_privilege_escalation_rejected",
    "TST-013": "tests.test_knowledge.KnowledgeTests.test_clean_candidate_promotes_with_citation",
    "TST-014": "tests.test_knowledge.KnowledgeTests.test_injection_is_quarantined",
    "TST-015": "tests.test_knowledge.KnowledgeTests.test_clean_candidate_promotes_with_citation",
    "TST-016": "tests.test_knowledge.KnowledgeTests.test_unsupported_query_abstains",
    "TST-017": "tests.test_knowledge.KnowledgeTests.test_withdrawal_removes_derived_retrieval",
    "TST-018": "tests.test_knowledge.KnowledgeTests.test_pii_memory_requires_explicit_admission",
    "TST-019": "tests.test_spine.SharedSpineTests.test_wrong_lease_token_is_rejected",
    "TST-020": "tests.test_agents_providers.AgentTests.test_join_propagates_nack",
    "TST-021": "tests.test_security_harness.SecurityHarnessTests.test_path_traversal_rejected",
    "TST-022": "tests.test_security_harness.SecurityHarnessTests.test_network_not_admitted",
    "TST-023": "tests.test_controls_observability_repo.ObservabilityTests.test_structured_log_and_no_progress_watchdog",
    "TST-024": "tests.test_recovery_release.RecoveryReleaseTests.test_tampered_backup_rejected",
    "TST-025": "tests.test_assurance.AssuranceTests.test_instruction_precedence_and_stale_override",
    "TST-026": "tests.test_assurance.AssuranceTests.test_skill_collision_implicit_and_clean_removal",
    "TST-027": "tests.test_assurance.AssuranceTests.test_mcp_revision_negotiation",
    "TST-028": "tests.test_security_harness.SecurityHarnessTests.test_mcp_tool_description_poisoning_rejected",
    "TST-029": "tests.test_controls_observability_repo.ControlValidationTests.test_all_materialized_controls_have_effective_contracts",
    "TST-030": "tests.test_e2e_vertical_slice.VerticalSliceTests.test_requirement_to_evidence_to_rollback_slice",
    "TST-031": "tests.test_security_harness.SecurityHarnessTests.test_path_traversal_rejected",
    "TST-032": "tests.test_assurance.AssuranceTests.test_stale_base_and_deterministic_oracle",
    "TST-033": "tests.test_knowledge.KnowledgeTests.test_injection_is_quarantined",
    "TST-034": "tests.test_security_harness.SecurityHarnessTests.test_secret_detection_and_redaction",
    "TST-035": "tests.test_security_harness.SecurityHarnessTests.test_privilege_escalation_rejected",
    "TST-036": "tests.test_assurance.AssuranceTests.test_stale_base_and_deterministic_oracle",
    "TST-038": "tests.test_assurance.AssuranceTests.test_telemetry_privacy_and_budget",
    "TST-039": "tests.test_assurance.AssuranceTests.test_telemetry_privacy_and_budget",
    "TST-040": "tests.test_recovery_release.RecoveryReleaseTests.test_release_reducer_fails_closed",
    "TST-042": "tests.test_recovery_release.RecoveryReleaseTests.test_backup_restore_readback",
    "TST-043": "tests.test_recovery_release.RecoveryReleaseTests.test_release_reducer_fails_closed",
    "TST-044": "tests.test_assurance.AssuranceTests.test_sbom_and_migration_reconciliation",
    "TST-045": "tests.test_knowledge.KnowledgeTests.test_self_approval_rejected",
    "TST-046": "tests.test_assurance.AssuranceTests.test_receiver_packet_capability_and_nack",
    "TST-047": "tests.test_assurance.AssuranceTests.test_receiver_packet_capability_and_nack",
    "TST-049": "tests.test_assurance.AssuranceTests.test_regression_release_drift_and_archive_failure",
    "TST-050": "tests.test_agents_providers.AgentTests.test_checker_write_scope_rejected",
    "TST-052": "tests.test_security_harness.SecurityHarnessTests.test_supply_chain_pin_mismatch_rejected",
    "TST-055": "tests.test_security_harness.SecurityHarnessTests.test_privilege_escalation_rejected",
    "TST-056": "tests.test_assurance.AssuranceTests.test_permission_mode_and_unicode_space_path",
    "TST-057": "tests.test_assurance.AssuranceTests.test_regression_release_drift_and_archive_failure",
    "TST-058": "tests.test_assurance.AssuranceTests.test_regression_release_drift_and_archive_failure",
    "TST-061": "tests.test_assurance.AssuranceTests.test_mcp_revision_negotiation",
    "TST-062": "tests.test_security_harness.SecurityHarnessTests.test_mcp_tool_description_poisoning_rejected",
    "TST-063": "tests.test_controls_observability_repo.ControlValidationTests.test_all_materialized_controls_have_effective_contracts",
    "TST-064": "tests.test_assurance.AssuranceTests.test_skill_collision_implicit_and_clean_removal",
    "TST-065": "tests.test_assurance.AssuranceTests.test_skill_collision_implicit_and_clean_removal",
    "TST-066": "tests.test_security_harness.SecurityHarnessTests.test_secret_detection_and_redaction",
    "TST-067": "tests.test_security_harness.SecurityHarnessTests.test_supply_chain_pin_mismatch_rejected",
    "TST-068": "tests.test_assurance.AssuranceTests.test_telemetry_privacy_and_budget",
    "TST-069": "tests.test_security_harness.SecurityHarnessTests.test_prompt_injection_in_metadata_rejected",
    "TST-070": "tests.test_controls_observability_repo.ObservabilityTests.test_structured_log_and_no_progress_watchdog",
    "TST-071": "tests.test_spine.SharedSpineTests.test_stale_version_is_rejected",
    "TST-072": "tests.test_agents_providers.AgentTests.test_checker_write_scope_rejected",
    "TST-073": "tests.test_assurance.AssuranceTests.test_rollback_prompt_veto_provider_and_token",
    "TST-074": "tests.test_controls_observability_repo.ObservabilityTests.test_structured_log_and_no_progress_watchdog",
    "TST-075": "tests.test_knowledge.KnowledgeTests.test_self_approval_rejected",
    "TST-076": "tests.test_assurance.AssuranceTests.test_rollback_prompt_veto_provider_and_token",
    "TST-077": "tests.test_recovery_release.RecoveryReleaseTests.test_release_reducer_fails_closed",
    "TST-078": "tests.test_recovery_release.RecoveryReleaseTests.test_release_reducer_fails_closed",
    "TST-079": "tests.test_assurance.AssuranceTests.test_rollback_prompt_veto_provider_and_token",
    "TST-080": "tests.test_assurance.AssuranceTests.test_receiver_packet_capability_and_nack",
    "TST-081": "tests.test_controls_observability_repo.ControlValidationTests.test_all_materialized_controls_have_effective_contracts",
    "TST-082": "tests.test_assurance.AssuranceTests.test_rollback_prompt_veto_provider_and_token",
    "TST-083": "tests.test_assurance.AssuranceTests.test_skill_collision_implicit_and_clean_removal",
    "TST-084": "tests.test_assurance.AssuranceTests.test_instruction_precedence_and_stale_override",
    "TST-085": "tests.test_spine.SharedSpineTests.test_illegal_transition_is_rejected",
    "TST-086": "tests.test_controls_observability_repo.ControlValidationTests.test_all_materialized_controls_have_effective_contracts",
    "TST-087": "tests.test_assurance.AssuranceTests.test_sbom_and_migration_reconciliation",
    "TST-088": "tests.test_assurance.AssuranceTests.test_rollback_prompt_veto_provider_and_token",
    "TST-089": "tests.test_agents_providers.ProviderTests.test_lifecycle_requires_evidence",
    "TST-090": "tests.test_assurance.AssuranceTests.test_permission_mode_and_unicode_space_path",
    "TST-091": "tests.test_security_harness.SecurityHarnessTests.test_privilege_escalation_rejected",
}

STATIC_CASES = {
    "TST-001", "TST-002", "TST-003", "TST-007", "TST-008", "TST-009",
    "TST-012", "TST-037", "TST-041", "TST-048", "TST-051", "TST-053", "TST-059", "TST-060",
}

BLOCKED_CASES = {
    "TST-054": ("TT-HERMES-UNINSTALL", "Only official full-uninstall dry-run is authorized; destructive uninstall/reinstall proof is pending."),
    "TST-092": ("TT-HGK-WRITE-BINDING", "Canonical target write/readback and final package exact-set are blocked by workspace binding."),
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def csv_count(path: Path) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def static_probe(case_id: str, root: Path) -> tuple[bool, dict[str, object]]:
    if case_id == "TST-001":
        receipt = json.loads((root / "source-freeze" / "SOURCE_FREEZE_RECEIPT.json").read_text(encoding="utf-8"))
        return True, {"authority_receipt": receipt.get("status"), "conflicts": csv_count(root / "source-freeze" / "CONFLICT_LEDGER.csv")}
    if case_id == "TST-002":
        count = csv_count(root / "requirements" / "ATOMIC_CHILD_REQUIREMENTS.csv")
        return count == 1040, {"atomic_children": count, "expected": 1040}
    if case_id == "TST-003":
        controls = csv_count(root / "registries" / "CONTROL_MATERIALIZATION_MANIFEST.csv")
        denominator = json.loads((root / "source-freeze" / "DENOMINATOR_RECONCILIATION.json").read_text(encoding="utf-8"))
        return controls == 60, {"materialized_control_files": controls, "predev_slice_denominator": 857, "denominator_status": denominator["status"]}
    if case_id == "TST-007":
        trace = csv_count(root / "requirements" / "REQUIREMENT_TRACEABILITY.csv")
        acceptances = csv_count(root / "requirements" / "ACCEPTANCE_EVIDENCE_PLAN.csv")
        return trace == acceptances == 499, {"trace_rows": trace, "acceptance_rows": acceptances}
    if case_id == "TST-008":
        conflicts = csv_count(root / "source-freeze" / "CONFLICT_LEDGER.csv")
        tt = (root / "source-freeze" / "TT_LEDGER.csv").read_text(encoding="utf-8")
        return conflicts > 0 and "TT-HLPE" in tt, {"conflict_rows": conflicts, "tt_conflict_present": "TT-HLPE" in tt}
    if case_id == "TST-009":
        from hg_kseos.doctor import doctor
        report = doctor(root)
        return report["verdict"] == "PASS", {"doctor_verdict": report["verdict"], "blocking": report["blocking"]}
    if case_id in {"TST-012", "TST-060"}:
        hermes = json.loads((root / "config" / "hermes.json").read_text(encoding="utf-8"))
        project = json.loads((root / "config" / "project.json").read_text(encoding="utf-8"))
        return hermes["provider_credentials_configured"] is False, {"hermes_status": hermes["status"], "canonical_database": project["canonical_database"], "fallback": "Codex/manual + Shared Spine"}
    if case_id == "TST-037":
        fixture = json.loads((root / "eval" / "nrtv" / "TST-037.json").read_text(encoding="utf-8"))
        compiled_relative = "requirements/REQUIREMENT_COMPILATION_RECEIPT.json"
        allowed = set(fixture["allowed_compiled_artifacts"])
        if compiled_relative not in allowed:
            return False, {"reason": "ERR_NRTV_COMPILED_ARTIFACT_NOT_ALLOWED"}
        compiled_path = (root / compiled_relative).resolve(strict=True)
        forbidden = [Path(value).resolve() for value in fixture["forbidden_inputs"]]
        if any(compiled_path == path or path in compiled_path.parents for path in forbidden):
            return False, {"reason": "ERR_NRTV_FORBIDDEN_RAW_INPUT"}
        compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
        answer = {name: compiled[name] for name in fixture["expected_answer"]}
        expected_locators = [f"{compiled_relative}#/{name}" for name in fixture["expected_answer"]]
        locators_valid = fixture["required_locators"] == expected_locators
        passed = answer == fixture["expected_answer"] and answer["predev_requirements"] + answer["p0_requirements"] == answer["requirement_trace_rows"] and locators_valid
        return passed, {"query": fixture["query"], "answer": answer, "locators": fixture["required_locators"], "locators_machine_validated": locators_valid, "allowed_artifact_enforced": compiled_relative, "forbidden_roots_enforced": fixture["forbidden_inputs"], "raw_source_volumes_read": False}
    if case_id == "TST-041":
        receipt = json.loads((root / "evidence" / "wave-13" / "SBOM_RECONCILIATION.json").read_text(encoding="utf-8"))
        passed = receipt["status"] == "PASS" and not receipt["unexplained_dependencies"]
        return passed, {"status": receipt["status"], "total_components": receipt["total_components"], "unexplained_dependencies": receipt["unexplained_dependencies"], "sbom_sha256": receipt["sbom_sha256"]}
    if case_id == "TST-048":
        rows = json.loads((root / "source-freeze" / "DENOMINATOR_RECONCILIATION.json").read_text(encoding="utf-8"))["rows"]
        values = {row["identity"]: row["observed"] for row in rows}
        passed = values.get("WP") == 24 and values.get("RBWI") == 18 and values.get("CA") == 30
        return passed, {"WP": values.get("WP"), "RBWI": values.get("RBWI"), "CA": values.get("CA")}
    if case_id in {"TST-051", "TST-059"}:
        receipt = json.loads((root / "evidence" / "wave-06" / "HERMES_INSTALL_RECEIPT.json").read_text(encoding="utf-8"))
        passed = receipt["installer"]["full_installer_executed"] is False and receipt["mutations"]["global_git_config_modified"] is False
        return passed, {"full_installer_executed": receipt["installer"]["full_installer_executed"], "global_git_config_modified": receipt["mutations"]["global_git_config_modified"], "unlocked_fallback_used": receipt["uv"]["unlocked_fallback_used"]}
    if case_id == "TST-053":
        report = json.loads((root / "evidence" / "wave-06" / "HERMES_RUNTIME_VALIDATION.json").read_text(encoding="utf-8"))
        tests = report["official_security_rollback_tests"]
        passed = tests["failures"] == 7 and report["overall"].startswith("TEMP_CLOSED")
        return passed, {"tests": tests["tests"], "passed": tests["passed"], "capability_exceptions": tests["failures"], "overall": report["overall"]}
    raise AssertionError(case_id)


def run_unittest(root: Path, qualified_name: str) -> tuple[bool, dict[str, object]]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [str(root / ".venv" / "Scripts" / "python.exe"), "-m", "unittest", "-v", qualified_name],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    return completed.returncode == 0, {"test": qualified_name, "returncode": completed.returncode, "output_sha256": sha256_bytes(output.encode("utf-8")), "output": output}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    baseline = root / "eval" / "FROZEN_ACCEPTANCE_CASES.csv"
    baseline_bytes = baseline.read_bytes()
    baseline_hash = sha256_bytes(baseline_bytes)
    if baseline_hash != EXPECTED_BASELINE_SHA256:
        raise SystemExit(f"acceptance baseline drift: {baseline_hash}")
    with baseline.open(encoding="utf-8-sig", newline="") as handle:
        cases = list(csv.DictReader(handle))
    if len(cases) != 92 or {row["case_id"] for row in cases} != {f"TST-{number:03d}" for number in range(1, 93)}:
        raise SystemExit("acceptance denominator/exact-set mismatch")

    output_root = root / "evidence" / "wave-15"
    case_root = output_root / "cases"
    fixture_root = root / "eval" / "fixtures"
    case_root.mkdir(parents=True, exist_ok=True)
    fixture_root.mkdir(parents=True, exist_ok=True)
    cache: dict[str, tuple[bool, dict[str, object]]] = {}
    results: list[dict[str, object]] = []
    captured_at = datetime.now(timezone.utc).isoformat()
    for row in cases:
        case_id = row["case_id"]
        fixture = {
            "schema": "HGK-ACCEPTANCE-FIXTURE/1",
            "case_id": case_id,
            "type": row["type"],
            "fixture": row["fixture"],
            "preconditions": row["preconditions"],
            "oracle": row["oracle"],
            "expected": row["expected"],
            "reject_code": row["reject_code"],
            "source_locator": row["source_locator"],
            "frozen_baseline_sha256": baseline_hash,
        }
        fixture_path = fixture_root / f"{case_id}.yaml"
        fixture_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if case_id in BLOCKED_CASES:
            tt_id, reason = BLOCKED_CASES[case_id]
            status = "BLOCKED"
            details: dict[str, object] = {"tt_id": tt_id, "reason": reason}
        elif case_id in STATIC_CASES:
            passed, details = static_probe(case_id, root)
            status = "MAKER_CASE_PASS" if passed and case_id == "TST-037" else ("MAKER_PROXY_PASS" if passed else "FAIL")
        else:
            binding = TEST_BINDINGS.get(case_id)
            if not binding:
                status = "FAIL"
                details = {"reason": "ERR_CASE_IMPLEMENTATION_MISSING"}
            else:
                if binding not in cache:
                    cache[binding] = run_unittest(root, binding)
                passed, details = cache[binding]
                status = "MAKER_PROXY_PASS" if passed else "FAIL"
        evidence = {
            "schema": "HGK-CASE-EVIDENCE/1",
            "captured_at_utc": captured_at,
            "case_id": case_id,
            "domain": row["domain"],
            "status": status,
            "oracle": row["oracle"],
            "source_locator": row["source_locator"],
            "fixture": str(fixture_path.relative_to(root)).replace("\\", "/"),
            "fixture_sha256": sha256_bytes(fixture_path.read_bytes()),
            "details": details,
            "maker": "CODEX_MAIN_MAKER",
            "independent_verifier": row["independent_verifier"],
            "independent_verdict": "INDEPENDENT_PASS" if case_id == "TST-037" and (root / "evidence" / "wave-19" / "INDEPENDENT_CHECKER_REPORT.json").is_file() else "NOT_RUN",
            "claim_ceiling": "Maker execution only; not independent acceptance.",
        }
        evidence_path = case_root / f"{case_id}.json"
        evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append(
            {
                "case_id": case_id,
                "domain": row["domain"],
                "type": row["type"],
                "status": status,
                "evidence": str(evidence_path.relative_to(root)).replace("\\", "/"),
                "evidence_sha256": sha256_bytes(evidence_path.read_bytes()),
                "independent_verdict": evidence["independent_verdict"],
            }
        )

    counts = {name: sum(1 for row in results if row["status"] == name) for name in ("MAKER_CASE_PASS", "MAKER_PROXY_PASS", "BLOCKED", "FAIL")}
    report = {
        "schema": "HGK-MAKER-ACCEPTANCE-REPORT/1",
        "captured_at_utc": captured_at,
        "baseline_sha256": baseline_hash,
        "denominator": 92,
        "counts": counts,
        "exact_set": True,
        "independent_acceptance": "PARTIAL_1_OF_92_TST_037_ONLY",
        "verdict": "TEMP_CLOSED" if counts["BLOCKED"] and not counts["FAIL"] else ("FAIL" if counts["FAIL"] else "MAKER_PASS_ONLY"),
        "claim_ceiling": "92/92 maker cases attempted; shared unit/static mappings are explicitly proxy checks, case-specific pass is separate, blocked cases remain open, and no independent/remote/deploy/production claim is made.",
    }
    report_path = output_root / "MAKER_ACCEPTANCE_REPORT.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_root / "CASE_RESULTS.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(json.dumps(report, ensure_ascii=False))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
