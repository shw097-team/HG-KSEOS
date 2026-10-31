"""Bounded repair D-R18-01 (stale source pins) in the ISOLATED copy only.

Defect: 03_TESTS_AND_READBACK/source_manifest.json pins 29 absolute host paths into
..._SKELETON_SPINE_DRAFT. That tree no longer exists (superseded by revision2), and 20 of the
remapped revision2 files legitimately differ from the pinned draft bytes because revision2 IS the
repair. So the author's own SOURCE-BYTES-UNCHANGED check asserts "the repair never happened" and can
never pass on the delivered package. Measured red: 2788 PASS / 1 FAIL.

Repair (data, not logic - validate.py is left byte-identical to the author's):
  * 20 pins whose file exists at the same relative path in revision2 -> re-pin to the delivered bytes,
    old digest kept in the receipt as pin_refresh evidence
  * 9 pins with no equivalent in the delivered package -> dropped from the invariant set with a named
    reason (they describe a superseded tree; they are not delivered inputs)
The 83 in-package artefacts are still independently covered by artifact_checksums.sha256 (83/83).
"""
import hashlib
import json
import shutil
from pathlib import Path

SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject")
PRE = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\preimage")
PKG_PARENT = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG")
DRAFT = PKG_PARENT / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_DRAFT"
REV2 = PKG_PARENT / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE" / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2"
EXT = "\\\\?\\"
import argparse as _ap
_ap_ = _ap.ArgumentParser(add_help=True)
_ap_.add_argument("--target", default=str(SUBJ),
                  help="directory whose source_manifest.json is repaired; the frozen subject is refused")
_ap_.add_argument("--i-know-this-writes", action="store_true")
_A = _ap_.parse_args()
_TARGET = Path(_A.target).resolve()
_FROZEN = SUBJ.resolve()
if _TARGET == _FROZEN:
    raise SystemExit("REFUSED_FROZEN_SUBJECT: this tool repairs a WORKING COPY only. Point --target at a copy, "
                     "never at var/R18-FHS-SKELETON-SPINE-20261029/subject (the frozen subject).")
if not _TARGET.is_dir():
    raise SystemExit("ERR_TARGET_MISSING: %s" % _TARGET)
MANIFEST = _TARGET / "03_TESTS_AND_READBACK" / "source_manifest.json"

PRE.mkdir(parents=True, exist_ok=True)
shutil.copy2(MANIFEST, PRE / "source_manifest.json.bak")

rows = json.loads(MANIFEST.read_text(encoding="utf-8"))
out, refreshed, dropped = [], [], []
for r in rows:
    p = r["path"]
    n = p[4:] if p.startswith(EXT) else p
    path = Path(n)
    try:
        rel = path.relative_to(DRAFT)
        is_draft = True
    except ValueError:
        rel = None
        is_draft = path.parent == PKG_PARENT
    if not is_draft:
        out.append(r)
        continue
    cand = (REV2 / rel) if rel is not None else None
    if cand is not None and cand.is_file():
        new_sha = hashlib.sha256(cand.read_bytes()).hexdigest()
        rec = dict(r)
        rec["path"] = str(cand)
        rec["sha256"] = new_sha
        rec["bytes"] = cand.stat().st_size
        out.append(rec)
        refreshed.append({"name": r.get("name"), "rel": str(rel), "old_sha256": r["sha256"],
                          "new_sha256": new_sha, "changed": new_sha != r["sha256"]})
    else:
        dropped.append({"name": r.get("name"), "pinned_path": n,
                        "reason": "NO_EQUIVALENT_IN_DELIVERED_REVISION2; the pin describes the superseded "
                                  "_SKELETON_SPINE_DRAFT tree and is not a delivered input"})

MANIFEST.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
receipt = {
    "schema": "R18.WP18.DEFECT_D-R18-01_REPAIR/1",
    "defect": "D-R18-01 source_manifest pins the superseded _SKELETON_SPINE_DRAFT tree",
    "pre_repair_measurement": {"passed": 2788, "failed": 1, "failing_case": "SOURCE-BYTES-UNCHANGED"},
    "manifest_rows_before": len(rows),
    "manifest_rows_after": len(out),
    "pins_refreshed": len(refreshed),
    "pins_refreshed_with_changed_bytes": sum(1 for x in refreshed if x["changed"]),
    "pins_dropped_named_reason": len(dropped),
    "refreshed": refreshed,
    "dropped": dropped,
    "validator_untouched": True,
    "preimage": str(PRE / "source_manifest.json.bak"),
    "claim_ceiling": "isolated-copy repair; the delivered candidate remains byte-frozen and still carries the "
                     "defect - the fix is offered to the author, not silently applied to the sealed package",
}
(SUBJ.parent / "receipts" / "WP18_D_R18_01_REPAIR.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: receipt[k] for k in ("manifest_rows_before", "manifest_rows_after", "pins_refreshed",
                                          "pins_refreshed_with_changed_bytes", "pins_dropped_named_reason")},
                 ensure_ascii=False))
