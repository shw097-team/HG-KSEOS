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

