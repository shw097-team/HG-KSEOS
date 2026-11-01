"""WP-FHS-06 — legal first reversible slice.

One file, additive, revertible by a single `git revert`. It pins the delivery's own counts so that a
future round cannot quietly shrink the payload and still call it delivered. If a manifest changes, this
test fails until the change is deliberate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DELIVERIES = Path(__file__).resolve().parents[1] / "fhs_msc_handoff_20261030" / "deliveries"

EXPECTED = {
    "manifest.handoff-patch-v1.json": {"files": 911, "bytes": 236_157_841},
    "manifest.skeleton-spine-r2-revision2.json": {"files": 86},
    "manifest.b1-implementation.json": {"files": 141},
}


def _load(name: str) -> dict:
    return json.loads((DELIVERIES / name).read_text(encoding="utf-8"))


def test_manifest_counts_are_the_delivered_counts() -> None:
    for name, expected in EXPECTED.items():
        manifest = _load(name)
        assert manifest["files"], f"{name} declares no files"
        if "files" in expected:
            assert len(manifest["files"]) == expected["files"], (
                f"{name}: shipped {len(manifest['files'])} entries, expected {expected['files']}"
            )
        if "bytes" in expected:
            total = sum(row["bytes"] for row in manifest["files"])
            assert total == expected["bytes"], f"{name}: byte total drifted ({total})"


def test_every_manifest_row_carries_a_digest() -> None:
    for name in EXPECTED:
        for row in _load(name)["files"]:
            assert len(row["sha256"]) == 64 and row["bytes"] >= 0, f"{name}: bad row {row['path']}"


def test_release_record_matches_the_published_assets() -> None:
    record = _load("RELEASE_20261030.json")
    assert record["release"].endswith("fhs-msc-deliveries-20261030")
    assert len(record["assets"]) == 3
    for asset in record["assets"]:
        assert len(asset["sha256"]) == 64
        local = DELIVERIES / asset["name"]
        if local.exists():
            digest = hashlib.sha256(local.read_bytes()).hexdigest()
            assert digest == asset["sha256"], f"{asset['name']}: local archive does not match the record"
