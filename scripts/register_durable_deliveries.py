#!/usr/bin/env python3
"""Put the three implementation deliveries into the control plane, where they can be counted.

A manifest in a PR branch is still only a claim: nothing outside the branch can tell whether the
delivery exists, and nothing goes red when it does not. This registers each delivery as a requirement
with an acceptance row, bound to the digest of its manifest (and of its sealed archive where one
exists), through the canonical typed API -- no direct SQL.

Verdicts are deliberately not uniform:

  b1-implementation            PASS  manifest + deterministic archive, 141/141 entries byte-identical
  skeleton-spine-r2-revision2  FAIL  manifest only; no sealed archive published yet
  handoff-patch-v1             FAIL  manifest only; 911 files / 236 MB are not yet published as an asset

Registering the two FAILs is the point. The denominator should show what is not done.

Usage:
    PYTHONPATH=src python scripts/register_durable_deliveries.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hg_kseos.errors import HGKError, InvariantViolation  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402

DB = ROOT / "var" / "shared-spine" / "hg-kseos.db"
DELIV = Path(os.environ.get("HGK_DELIVERIES_DIR", "C:/wg/repo/fhs_msc_handoff_20261030/deliveries"))

ROWS = [
    {
        "requirement_id": "REQ-DURABILITY-B1-20261030",
        "acceptance_id": "ACC-DURABILITY-B1-20261030",
        "wording": "B1 Bootstrap Repair implementation is recoverable from the durable layer: manifest with per-file sha256 plus a deterministic archive whose entry set equals the manifest.",
        "oracle": "deliveries/manifest.b1-implementation.json + B1_implementation.zip",
        "threshold": "141 files, rollup 6287198b818c9a01b639ef65b2191f1fb2f2bbb3349292d00229cde228b3f96c, archive sha256 2d388b91f64ab04fb39fe7b0d212ec7190b090c37ffb30138e89531637ec7ca3, entry_set_equals_manifest true",
        "negative_fixture": "tests/test_durable_gates.py::test_manifest_refuses_incomplete_walk",
        "verdict": "PASS",
        "evidence": [("manifest.b1-implementation.json", "manifest"), ("B1_implementation.zip", "archive")],
    },
    {
        "requirement_id": "REQ-DURABILITY-SKELETON-20261030",
        "acceptance_id": "ACC-DURABILITY-SKELETON-20261030",
        "wording": "SKELETON_SPINE r2-revision2 implementation is recoverable from the durable layer.",
        "oracle": "deliveries/manifest.skeleton-spine-r2-revision2.json",
        "threshold": "86 files, rollup 8f498aeb5cc283202afa4a2a9bdc208b9b96eddc5b8711464b1dabe5a85fecfe, sealed archive published with a matching digest",
        "negative_fixture": "tests/test_durable_gates.py::test_subject_without_repo_is_refused",
        "verdict": "FAIL",
        "fail_reason": "manifest exists but no sealed archive has been published; the payload is still only on one disk",
        "evidence": [("manifest.skeleton-spine-r2-revision2.json", "manifest")],
    },
    {
        "requirement_id": "REQ-DURABILITY-HANDOFF-20261030",
        "acceptance_id": "ACC-DURABILITY-HANDOFF-20261030",
        "wording": "FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1 delivery is recoverable from the durable layer.",
        "oracle": "deliveries/manifest.handoff-patch-v1.json",
        "threshold": "911 files, 236157841 bytes, rollup 6ca537df72ab14d39dffb8c65e2b0061dd209778a262998799a195a9a39877f3, sealed archive published with a matching digest",
        "negative_fixture": "tests/test_durable_gates.py::test_dirty_policy_is_refused",
        "verdict": "FAIL",
        "fail_reason": "manifest exists but the 911-file payload is not published; 236 MB stays a single-disk artefact",
        "evidence": [("manifest.handoff-patch-v1.json", "manifest")],
    },
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    spine = SharedSpine(DB)
    spine.create_project()
    results = []
    for row in ROWS:
        ev_refs = []
        for name, kind in row["evidence"]:
            f = DELIV / name
            if not f.exists():
                results.append({"requirement": row["requirement_id"], "state": "MISSING_EVIDENCE", "file": name})
                break
            ev_id = f"EV-{kind.upper()}-{row['acceptance_id']}"
            if not a.dry_run:
                try:
                    spine.register_evidence(ev_id, kind, str(f), sha(f), producer="FAR-DURABILITY-20261030")
                except (HGKError, InvariantViolation) as e:
                    if "UNIQUE" not in str(e) and "exists" not in str(e).lower():
                        raise
            ev_refs.append(ev_id)
        else:
            if a.dry_run:
                results.append({"requirement": row["requirement_id"], "state": "DRY_RUN", "verdict": row["verdict"]})
                continue
            spine.register_requirement(
                row["requirement_id"], str(DELIV), row["wording"], row["acceptance_id"],
                row["oracle"], row["threshold"], row["negative_fixture"])
            token = f"TOK-{row['acceptance_id']}"
            spine.acquire_lease(row["acceptance_id"], "hgk-agent", token, ttl_seconds=120)
            res = spine.resolve_acceptance(
                row["acceptance_id"], verdict=row["verdict"], evidence_ref=ev_refs[0],
                actor="hgk-agent", token=token, expected_version=0,
                idempotency_key=f"IDEM-{row['acceptance_id']}", requirement_id=row["requirement_id"],
                payload={"reason": row.get("fail_reason"), "evidence_refs": ev_refs,
                         "round": "FAR-DURABILITY-20261030"})
            results.append({"requirement": row["requirement_id"], "state": "RESOLVED",
                            "verdict": res.get("verdict"), "evidence": ev_refs})

    print(json.dumps({"schema": "DURABLE-DELIVERY-REGISTRATION/1", "rows": results}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
