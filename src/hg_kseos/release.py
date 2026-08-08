from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .spine import SharedSpine
from .util import canonical_json, new_id, sha256_text, utc_now


@dataclass(frozen=True)
class EvidenceEnvelope:
    requirements_total: int
    requirements_passed: int
    blocking_tests_passed: bool
    security_critical: int
    rollback_passed: bool
    restore_passed: bool
    independent_passed: bool
    provider_lifecycle_closed: bool
    user_guide_complete: bool
    raw_evidence_complete: bool
    open_blocking_tt: int
    checker: str
    artifacts: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EvidenceEnvelope":
        required = {field.name for field in cls.__dataclass_fields__.values()}
        missing = required - value.keys()
        if missing:
            raise ValueError(f"ERR_EVIDENCE_ENVELOPE_MISSING:{sorted(missing)}")
        value = dict(value)
        value["artifacts"] = tuple(value["artifacts"])
        return cls(**{key: value[key] for key in required})


class ReleaseReducer:
    VERSION = "1"

    def __init__(self, spine: SharedSpine) -> None:
        self.spine = spine

    def reduce(self, envelope: EvidenceEnvelope) -> dict[str, Any]:
        reasons: list[str] = []
        if envelope.requirements_total <= 0 or envelope.requirements_passed != envelope.requirements_total:
            reasons.append("REQUIREMENT_COVERAGE_INCOMPLETE")
        if not envelope.blocking_tests_passed:
            reasons.append("BLOCKING_TEST_FAILURE")
        if envelope.security_critical:
            reasons.append("SECURITY_CRITICAL_NONZERO")
        if not envelope.rollback_passed or not envelope.restore_passed:
            reasons.append("RECOVERY_NOT_PROVEN")
        if not envelope.independent_passed or not envelope.checker:
            reasons.append("INDEPENDENT_ACCEPTANCE_MISSING")
        if not envelope.provider_lifecycle_closed:
            reasons.append("PROVIDER_LIFECYCLE_OPEN")
        if not envelope.user_guide_complete:
            reasons.append("USER_GUIDE_INCOMPLETE")
        if not envelope.raw_evidence_complete or not envelope.artifacts:
            reasons.append("RAW_EVIDENCE_INCOMPLETE")
        if envelope.open_blocking_tt:
            reasons.append("RELEASE_BLOCKING_TT_OPEN")
        verdict = "HG-KSEOS_LOCAL_DELIVERY_PASS" if not reasons else "FAIL_CLOSED"
        envelope_json = canonical_json(envelope.__dict__)
        decision = {
            "decision_id": new_id("REL"),
            "candidate_digest": sha256_text(envelope_json),
            "reducer_version": self.VERSION,
            "verdict": verdict,
            "reasons": reasons,
            "checker": envelope.checker,
            "created_at": utc_now(),
        }
        with self.spine.transaction() as connection:
            connection.execute(
                """INSERT INTO release_decisions
                   (decision_id,candidate_digest,reducer_version,verdict,reasons_json,
                    independent_checker,evidence_envelope,created_at)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (
                    decision["decision_id"],
                    decision["candidate_digest"],
                    self.VERSION,
                    verdict,
                    json.dumps(reasons),
                    envelope.checker,
                    envelope_json,
                    decision["created_at"],
                ),
            )
        return decision


# Terminal statuses acceptable for a coverage domain (指令-4 §11 / §13).
TERMINAL_STATUSES = {
    "RUNTIME_PASS",
    "DEFERRED_SOURCE_BACKED",
    "NOT_APPLICABLE_SOURCE_BACKED",
    "PROHIBITED_SOURCE_BACKED",
}
FORBIDDEN_DOMAIN_STATUSES = {
    "UNKNOWN",
    "MISSING",
    "DESIGN_ONLY_WHEN_RUNTIME_REQUIRED",
    "STATIC_ONLY_WHEN_RUNTIME_REQUIRED",
    "OPEN_BLOCKING_TT",
}


@dataclass(frozen=True)
class CoverageEnvelope:
    """Coverage-complete final gate input (指令-4 §13 schema)."""

    coverage_domains_total: int
    coverage_domains_terminal: int
    canonical_requirements_total: int
    requirements_reconciled: bool
    orphan_requirements: int
    unowned_mandatory_assets: int
    tst_total: int
    tst_independent_pass: int
    semantic_depth_calibrated: bool
    runtime_required_static_only_count: int
    domains: dict[str, str]
    knowledge_security_negative: str
    domain_blocking_gaps: int
    hermes_provider: str
    hermes_model: str
    codex_cli_primary_executor: bool
    opencodex_transport: bool
    openai_model_fallback: bool
    protected_identities_78_disposition_complete: bool
    mandatory_default_active_providers_certified: bool
    tst_054: str
    tst_092: str
    product_tests_all_pass: bool
    hlpe_tests_all_pass: bool
    security_blockers: int
    blocking_tt: int
    backup_restore_pass: bool
    rollback_pass: bool
    sbom_current: bool
    user_guide_exists: bool
    user_guide_runtime_consistent: bool
    user_guide_sha256_verified: bool
    package_exact_readback: bool
    final_head_independently_checked: bool
    final_evidence_md_exists: bool
    final_evidence_md_readback_verified: bool
    checker: str
    artifacts: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "CoverageEnvelope":
        required = {field.name for field in cls.__dataclass_fields__.values()}
        missing = required - value.keys()
        if missing:
            raise ValueError(f"ERR_COVERAGE_ENVELOPE_MISSING:{sorted(missing)}")
        value = dict(value)
        value["artifacts"] = tuple(value["artifacts"])
        value["domains"] = dict(value["domains"])
        return cls(**{key: value[key] for key in required})


class CoverageReducer:
    """Coverage-complete deterministic final gate (reducer v2, 指令-4 §13/§17).

    Any domain with UNKNOWN / MISSING / DESIGN_ONLY_WHEN_RUNTIME_REQUIRED /
    STATIC_ONLY_WHEN_RUNTIME_REQUIRED / OPEN_BLOCKING_TT status, or any
    required runtime flag false, forces exit 1 (FAIL_CLOSED).
    """

    VERSION = "2"

    def __init__(self, spine: SharedSpine) -> None:
        self.spine = spine

    def reduce(self, envelope: CoverageEnvelope) -> dict[str, Any]:
        reasons: list[str] = []

        # authority / denominator
        if envelope.coverage_domains_total < 1 or envelope.coverage_domains_terminal != envelope.coverage_domains_total:
            reasons.append("DOMAIN_COVERAGE_INCOMPLETE")
        if not envelope.requirements_reconciled or envelope.orphan_requirements or envelope.unowned_mandatory_assets:
            reasons.append("REQUIREMENT_RECONCILIATION_INCOMPLETE")
        # acceptance depth
        if envelope.tst_total < 1 or envelope.tst_independent_pass != envelope.tst_total:
            reasons.append("ACCEPTANCE_NOT_INDEPENDENT_FULL")
        if not envelope.semantic_depth_calibrated or envelope.runtime_required_static_only_count:
            reasons.append("SEMANTIC_DEPTH_NOT_CALIBRATED")
        # domains: every status terminal source-backed
        for domain, status in envelope.domains.items():
            if status in FORBIDDEN_DOMAIN_STATUSES:
                reasons.append(f"DOMAIN_STATUS_FORBIDDEN:{domain}:{status}")
            elif status not in TERMINAL_STATUSES:
                reasons.append(f"DOMAIN_STATUS_NONTERMINAL:{domain}:{status}")
        if envelope.domain_blocking_gaps:
            reasons.append("DOMAIN_BLOCKING_GAPS_NONZERO")
        # runtime/provider routing (fail closed: no OpenAI fallback)
        if envelope.hermes_provider != "opencode-go" or envelope.hermes_model != "deepseek-v4-flash":
            reasons.append("HERMES_ROUTE_MISMATCH")
        if not envelope.codex_cli_primary_executor or not envelope.opencodex_transport:
            reasons.append("CODEX_ROUTE_INCOMPLETE")
        if envelope.openai_model_fallback:
            reasons.append("OPENAI_MODEL_FALLBACK_ENABLED")
        if not envelope.protected_identities_78_disposition_complete:
            reasons.append("PROTECTED_IDENTITIES_INCOMPLETE")
        if not envelope.mandatory_default_active_providers_certified:
            reasons.append("PROVIDER_CERTIFICATION_INCOMPLETE")
        # tests / security / tt
        if not envelope.product_tests_all_pass or not envelope.hlpe_tests_all_pass:
            reasons.append("TEST_SUITE_NOT_ALL_PASS")
        if envelope.security_blockers:
            reasons.append("SECURITY_BLOCKERS_NONZERO")
        if envelope.blocking_tt:
            reasons.append("BLOCKING_TT_OPEN")
        if envelope.knowledge_security_negative != "PASS":
            reasons.append("KNOWLEDGE_SECURITY_NEGATIVE_NOT_PASS")
        # recovery / package / evidence
        if not envelope.backup_restore_pass or not envelope.rollback_pass:
            reasons.append("RECOVERY_NOT_PROVEN")
        if not envelope.sbom_current:
            reasons.append("SBOM_NOT_CURRENT")
        if not envelope.user_guide_exists or not envelope.user_guide_runtime_consistent or not envelope.user_guide_sha256_verified:
            reasons.append("USER_GUIDE_NOT_VERIFIED")
        if not envelope.package_exact_readback or not envelope.final_head_independently_checked:
            reasons.append("PACKAGE_OR_HEAD_NOT_CHECKED")
        if not envelope.final_evidence_md_exists or not envelope.final_evidence_md_readback_verified:
            reasons.append("FINAL_EVIDENCE_MD_NOT_VERIFIED")
        if envelope.tst_054 != "INDEPENDENT_CASE_PASS" or envelope.tst_092 != "INDEPENDENT_CASE_PASS":
            reasons.append("TST_054_092_NOT_INDEPENDENT_PASS")

        verdict = "HG-KSEOS_LOCAL_DELIVERY_PASS" if not reasons else "FAIL_CLOSED"
        envelope_json = canonical_json(envelope.__dict__)
        decision = {
            "decision_id": new_id("REL"),
            "candidate_digest": sha256_text(envelope_json),
            "reducer_version": self.VERSION,
            "verdict": verdict,
            "reasons": reasons,
            "checker": envelope.checker,
            "created_at": utc_now(),
        }
        with self.spine.transaction() as connection:
            connection.execute(
                """INSERT INTO release_decisions
                   (decision_id,candidate_digest,reducer_version,verdict,reasons_json,
                    independent_checker,evidence_envelope,created_at)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (
                    decision["decision_id"],
                    decision["candidate_digest"],
                    self.VERSION,
                    verdict,
                    json.dumps(reasons),
                    envelope.checker,
                    envelope_json,
                    decision["created_at"],
                ),
            )
        return decision

