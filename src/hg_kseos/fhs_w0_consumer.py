# -*- coding: utf-8 -*-
"""HGK-side consumer for the FHS W0 implementation result (read-only candidate gate).

This module consumes the artefacts an FHS W0 round deposits in SBL and Fabric. It is a
*consumer*: it never compiles a PIPD artefact, never mints an HGK permit, never writes
canonical state, and never upgrades a candidate to admitted/released. Its only job is to
answer one bounded question -- "is this W0 result internally complete enough for an HGK
reader to review, and does it falsely claim a native effect?" -- and to answer it with a
typed verdict that a caller cannot mistake for acceptance.

Design rules encoded here:
  * A result carrying any native claim (permit, admitted, release, protected checker,
    native E2E) is REFUSED, not downgraded: a candidate that overclaims is not safe to read.
  * A missing work package is REFUSED with the package named; absence is not "partial pass".
  * A trace closure whose scope is not AUTHOR_STATIC is REFUSED.
  * Everything accepted is stamped CANDIDATE_ONLY with an explicit non-claim list.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_WP = (
    "WP-FHS-00",
    "WP-FHS-01",
    "WP-FHS-15",
    "WP-FHS-16",
    "WP-FHS-19",
    "WP-FHS-21",
)
NATIVE_CLAIM_KEYS = (
    "hgk_permit",
    "hgk_admitted",
    "pipd_canonical",
    "released",
    "protected_checker",
    "native_e2e",
)

MISSING_ARTIFACT = "MISSING_ARTIFACT"
RESULT_UNPARSABLE = "RESULT_UNPARSABLE"
WP_NOT_IMPLEMENTED = "WP_NOT_IMPLEMENTED"
WP_STATUS_UNKNOWN = "WP_STATUS_UNKNOWN"
NATIVE_CLAIM_REFUSED = "NATIVE_CLAIM_REFUSED"
TRACE_SCOPE_INVALID = "TRACE_SCOPE_INVALID"
SPEC_UNBOUND = "SPEC_UNBOUND"


@dataclass
class Verdict:
    verdict: str
    first_fail: str | None
    findings: list[str] = field(default_factory=list)
    accepted_wps: list[str] = field(default_factory=list)
    claim_ceiling: str = "CANDIDATE_ONLY"
    non_claims: list[str] = field(default_factory=lambda: [
        "NOT_AN_HGK_PERMIT",
        "NOT_PROTECTED_CHECKER_ACCEPTANCE",
        "NOT_PIPD_CANONICAL",
        "NOT_RELEASED",
    ])

    def as_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict,
            "first_fail": self.first_fail,
            "findings": self.findings,
            "accepted_wps": self.accepted_wps,
            "claim_ceiling": self.claim_ceiling,
            "non_claims": self.non_claims,
        }


def _walk_true_keys(obj: Any, keys: set[str]) -> list[str]:
    hits: list[str] = []
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            for k, v in cur.items():
                if k.lower() in keys and v is True:
                    hits.append(k.lower())
                stack.append(v)
        elif isinstance(cur, list):
            stack.extend(cur)
    return sorted(set(hits))


def evaluate(path: str | Path) -> Verdict:
    p = Path(path)
    if not p.exists():
        return Verdict("REFUSED", MISSING_ARTIFACT, [str(p)])
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return Verdict("REFUSED", RESULT_UNPARSABLE, [str(exc)[:200]])

    overclaim = _walk_true_keys(data, set(NATIVE_CLAIM_KEYS))
    if overclaim:
        return Verdict("REFUSED", NATIVE_CLAIM_REFUSED, overclaim)

    wps = data.get("work_packages") or {}
    if not isinstance(wps, dict):
        return Verdict("REFUSED", WP_STATUS_UNKNOWN, ["work_packages is not an object"])

    missing = [w for w in REQUIRED_WP if w not in wps]
    if missing:
        return Verdict("REFUSED", WP_NOT_IMPLEMENTED, missing)

    allowed = {"DONE", "PARTIAL", "HOLD"}
    bad = [w for w in REQUIRED_WP if str(wps[w].get("status")) not in allowed]
    if bad:
        return Verdict("REFUSED", WP_STATUS_UNKNOWN, bad)

    trace = data.get("trace") or {}
    if trace.get("scope") != "AUTHOR_STATIC":
        return Verdict("REFUSED", TRACE_SCOPE_INVALID, [str(trace.get("scope"))])

    specs = data.get("specs") or {}
    unbound = [k for k in ("product", "architecture", "program")
               if not (specs.get(k) or {}).get("sha256")]
    if unbound:
        return Verdict("REFUSED", SPEC_UNBOUND, unbound)

    return Verdict("CANDIDATE_READY_FOR_HGK_REVIEW", None, [], list(REQUIRED_WP))


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys
    ap = argparse.ArgumentParser(description="read-only HGK consumer gate for an FHS W0 result")
    ap.add_argument("result_json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    v = evaluate(a.result_json)
    print(json.dumps(v.as_dict(), ensure_ascii=False, indent=2))
    return 0 if v.verdict.startswith("CANDIDATE_READY") else 3


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
