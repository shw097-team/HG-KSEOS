"""Stage the reviewable deliverable tree for shw097-team/HG-KSEOS.

Deterministic copy only: this script never authors prose. Narrative documents are written by the
EXECUTE lane inside the exact WriteSet declared in its brief.

Source of truth:
  C:\\wg\\repro    reproduced first work (35/35 after the import-order repair)
  C:\\wg\\pkg      delivered package tree (renamed to the canonical 01_SUBSTANTIVE_BODY)
  round dir       receipts + tools + logs produced by this execution
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\FHS-HANDOFF-EXEC-20261030")
REPRO = Path(r"C:\wg\repro")
PKG = Path(r"C:\wg\pkg")
REPO = Path(r"C:\wg\repo")
OUT = REPO / "fhs_msc_handoff_20261030"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def put(src: Path, dst_rel: str) -> dict:
    dst = OUT / dst_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": dst_rel, "bytes": dst.stat().st_size, "sha256": sha(dst)}


def main() -> int:
    # REPAIR (round finding F-09): the first version rmtree'd OUT, which destroyed the narrative
    # documents authored after staging. Staging now owns only the four copied subtrees plus the
    # inventory; narrative files are never deleted by a re-stage.
    OUT.mkdir(parents=True, exist_ok=True)
    for sub in ("receipts", "tools", "logs", "first_work", "docs", "package"):
        if (OUT / sub).exists():
            shutil.rmtree(OUT / sub)

    staged: list[dict] = []

    # 1. receipts and tools actually produced by this execution
    for src in sorted((ROUND / "receipts").glob("*.json")):
        staged.append(put(src, f"receipts/{src.name}"))
    for src in sorted((ROUND / "tools").glob("*.py")):
        staged.append(put(src, f"tools/{src.name}"))
    for name in ("first_work.out", "check_first_work.out", "check_first_work_patched.out",
                 "PIPD_5_AFFECTED_TESTS_RAW.txt", "lane_probe.out", "lane_verify.out",
                 "lane_writer.out", "hgk-lane-dispatch.py.before-R-EXEC-02"):
        src = ROUND / "logs" / name
        if src.is_file():
            staged.append(put(src, f"logs/{name}"))

    # 2. reproduced first-work artifacts (the deliverable of WP-FHS-15)
    for rel in ("RUN/ProductSPEC.json", "RUN/ArchitectureSPEC.json", "RUN/ProgramSPEC.json",
                "RUN/FUO.json", "RUN/SourceReadback.json", "PI-PKG.json", "TaskSpecSeed.json",
                "ORIGINAL_22_WP_DAG.json", "ExecutionHandoff.json", "IntentCard.json",
                "KnownAnswerReadback.json", "ProfileBinding.json", "FUNCTIONAL_SOURCE_TRACE.json",
                "PlannedTQAEP.json", "PD_LATE_BIND_RECEIVER_CONTRACT.json"):
        src = REPRO / "02_FIRST_WORK" / rel
        if src.is_file():
            staged.append(put(src, f"first_work/{rel.replace('/', '_')}"))
    for name in ("MINIMAL_STATIC_TESTS.json", "PIPD_FUNCTIONAL_PI_READER_ACK.json"):
        src = REPRO / "03_HANDOFF_EVIDENCE" / name
        if src.is_file():
            staged.append(put(src, f"first_work/{name}"))

    # 3. the seventeen current books (the design reader the first work compiles against)
    for src in sorted((PKG / "01_SUBSTANTIVE_BODY").glob("*.md")):
        staged.append(put(src, f"docs/{src.name}"))

    # 4. the package's own sealed manifests, kept byte-exact for independent re-verification
    for name in ("SHA256_PAYLOAD_MANIFEST.json", "SHA256_DELIVERY_MANIFEST.md",
                 "VERSION_AND_DELIVERY.md", "HANDOFF_README.md", "FIRST_WORK_RECEIVER_CONTRACT.md",
                 "CURRENT_READER_SCOPE.json"):
        staged.append(put(PKG / name, f"package/{name}"))
    # the delivered artefacts two findings rest on: the 5/5 raw snapshot (F-03) and the pair whose
    # timing is identical to 16 digits (F-14)
    for rel, dst in (("03_HANDOFF_EVIDENCE/EXISTING_AFFECTED_TESTS_RAW.txt", "package/EXISTING_AFFECTED_TESTS_RAW.txt"),
                     ("03_HANDOFF_EVIDENCE/MINIMAL_STATIC_TESTS.json", "package/MINIMAL_STATIC_TESTS.json"),
                     ("03_HANDOFF_EVIDENCE/MINIMAL_STATIC_TESTS_INITIAL.json", "package/MINIMAL_STATIC_TESTS_INITIAL.json")):
        src = PKG / rel
        if src.is_file():
            staged.append(put(src, dst))

    manifest = {
        "schema": "FHS-MSC-HANDOFF-EXEC-DELIVERY/1",
        "round": "FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030",
        "generated_from": {"repro": str(REPRO), "package": str(PKG)},
        "files": len(staged),
        "total_bytes": sum(r["bytes"] for r in staged),
        "entries": staged,
    }
    (OUT / "STAGED_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(OUT), "files": manifest["files"],
                      "total_bytes": manifest["total_bytes"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
