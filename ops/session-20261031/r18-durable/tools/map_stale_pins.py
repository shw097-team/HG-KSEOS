"""Can the 29 stale source pins be resolved inside the delivered revision2 package?

The candidate's source_manifest.json pins absolute paths into ..._SKELETON_SPINE_DRAFT (a superseded
sibling tree). This script maps each pinned path onto the same relative location inside the delivered
revision2 package and reports whether the bytes there match the pin.
"""
import collections
import hashlib
import json
import os
from pathlib import Path

PKG_PARENT = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG")
DRAFT = PKG_PARENT / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_DRAFT"
REV2 = PKG_PARENT / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE" / "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2"
SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject")
EXT = "\\\\?\\"

print("DRAFT exists:", DRAFT.exists())
print("REV2  exists:", REV2.exists())

rows = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "source_recheck.json").read_text(encoding="utf-8"))
bad = [r for r in rows if r["status"] != "UNCHANGED"]


def norm(p):
    return p[4:] if p.startswith(EXT) else p


res = []
for r in bad:
    n = norm(r["path"])
    p = Path(n)
    try:
        rel = p.relative_to(DRAFT)
        mapped_to = "DRAFT->REV2"
    except ValueError:
        try:
            rel = p.relative_to(PKG_PARENT)
            mapped_to = "PKGPARENT->REV2"
        except ValueError:
            rel = None
            mapped_to = "UNMAPPED"
    rec = {"pin": n, "mapping": mapped_to, "rel": str(rel) if rel else None}
    if rel is not None:
        cand = REV2 / rel
        rec["rev2_path_exists"] = cand.is_file()
        if cand.is_file():
            d = hashlib.sha256(cand.read_bytes()).hexdigest()
            rec["rev2_sha_prefix"] = d[:12]
            rec["matches_pin"] = d == r["expected_sha256"]
        # also: does the subject copy hold the same relative path?
        sc = SUBJ / rel
        rec["subject_copy_exists"] = sc.is_file()
    res.append(rec)

hist = collections.Counter((x["mapping"], x.get("rev2_path_exists"), x.get("matches_pin")) for x in res)
receipt = {
    "schema": "R18.WP21.STALE_SOURCE_PIN_MAPPING/1",
    "draft_tree_exists": DRAFT.exists(),
    "revision2_tree_exists": REV2.exists(),
    "pins_unreadable": len(bad),
    "histogram": {str(k): v for k, v in hist.items()},
    "rows": res,
}
(SUBJ.parent / "receipts" / "WP21_STALE_SOURCE_PIN_MAPPING.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(receipt["histogram"], ensure_ascii=False, indent=1))
print("unmapped:", sum(1 for x in res if x["mapping"] == "UNMAPPED"))
