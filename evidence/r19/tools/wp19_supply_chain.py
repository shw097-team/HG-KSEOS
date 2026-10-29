"""WP-FHS-19 supply chain readback for the DELIVERED r2-revision2 package.

Scope: the artefact an external team would receive (44 files + the outer ZIP), not the round's
working copy. Everything is recomputed twice; the receipt is only evidence if both passes agree.

Produces: per-file sha256 inventory (SBOM basis), declared third-party imports of the shipped
tools, LICENSE/NOTICE disposition, secret-pattern scan with a planted canary positive control,
and a byte total. Absence of a file is recorded as a named finding, never as a pass.
"""
from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

PKG = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2")
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\receipts")

SECRET_PATTERNS = {
    "github_pat": re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    "ghp": re.compile(rb"ghp_[A-Za-z0-9]{20,}"),
    "aws_akid": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "openai_sk": re.compile(rb"sk-[A-Za-z0-9]{32,}"),
    "slack": re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}"),
}
STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def scan() -> dict:
    entries, total, hits = {}, 0, []
    for p in sorted(PKG.rglob("*")):
        if not p.is_file():
            continue
        b = p.read_bytes()
        rel = p.relative_to(PKG).as_posix()
        entries[rel] = {"sha256": sha(b), "bytes": len(b)}
        total += len(b)
        for name, rx in SECRET_PATTERNS.items():
            if rx.search(b):
                hits.append({"path": rel, "pattern": name})
    return {"entries": entries, "bytes": total, "secret_hits": hits}


def imports_of_tools() -> dict:
    mods = set()
    for p in sorted((PKG / "tools").glob("*.py")):
        tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods.add(node.module.split(".")[0])
    local = {p.stem for p in (PKG / "tools").glob("*.py")} | {"tools"}
    third = sorted(m for m in mods if m not in STDLIB and m not in local)
    return {"all_imports": sorted(mods), "third_party": third,
            "stdlib_only_except": third}


def main() -> int:
    a = scan()
    b = scan()
    stable = a["entries"] == b["entries"] and a["bytes"] == b["bytes"]

    canary_fired = None
    probe = PKG / "03_TESTS_AND_READBACK" / "_canary_probe.tmp"
    try:
        probe.write_bytes(b"token=ghp_" + b"A" * 24 + b"\n")
        canary_fired = any(h["path"].endswith("_canary_probe.tmp") for h in scan()["secret_hits"])
    finally:
        probe.unlink(missing_ok=True)

    names = {k.lower() for k in a["entries"]}
    lic = [k for k in names if k.startswith("license") or k.startswith("licence")]
    notice = [k for k in names if k.startswith("notice")]

    receipt = {
        "schema": "R19.WP19_SUPPLY_CHAIN/2",
        "at": datetime.now(timezone.utc).isoformat(),
        "scope": "delivered r2-revision2 package (the artefact an external team receives)",
        "package_root": str(PKG),
        "files": len(a["entries"]),
        "bytes_scanned": a["bytes"],
        "stable_across_two_scans": stable,
        "sbom_entries": a["entries"],
        "dependencies": imports_of_tools(),
        "license": {"present": lic, "disposition": "PRESENT" if lic else "ABSENT_NAMED_FINDING"},
        "notice": {"present": notice, "disposition": "PRESENT" if notice else "ABSENT_NAMED_FINDING"},
        "secret_scan": {"hits": a["secret_hits"], "patterns": sorted(SECRET_PATTERNS),
                        "planted_canary_fired": canary_fired,
                        "self_test": "PASS" if canary_fired else "FAIL_SCANNER_DID_NOT_FIRE"},
        "findings": ([] if lic else ["F-LIC-01: the doc package carries no LICENSE file; licence terms live with the repos that ship code (PIPD LICENSE) — recorded, not silently passed"]) +
                    ([] if notice else ["F-NOTICE-01: no NOTICE file in the doc package; same disposition as F-LIC-01"]),
        "recomputable": "entries are plain sha256 over bytes; two independent passes must agree",
        "claim_ceiling": "hash inventory + declared imports + secret pattern scan of this package only. "
                         "It is not a licence audit, not a CVE/dependency-resolution result, and not an SBOM standard format.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "WP19_SUPPLY_CHAIN_R19.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("files", "bytes_scanned", "stable_across_two_scans")}, indent=1))
    print(json.dumps({"third_party": receipt["dependencies"]["third_party"],
                      "license": receipt["license"]["disposition"],
                      "notice": receipt["notice"]["disposition"],
                      "secrets": len(receipt["secret_scan"]["hits"]),
                      "canary": receipt["secret_scan"]["planted_canary_fired"]}, ensure_ascii=False, indent=1))
    return 0 if stable and canary_fired else 1


if __name__ == "__main__":
    raise SystemExit(main())
