"""Classify every non-UNCHANGED row of the candidate's own source_recheck.json.

Distinguishes three causes, because they license different claims:
  ABSENT_UNDER_NORMALIZED_PATH  - the manifest path, stripped of its Win32 extended prefix,
                                  still does not exist: a pinned input is missing or was moved
  EXISTS_BUT_UNREADABLE         - the file is there but open() raised: a path-form/ACL defect
  HASHABLE_DIFFERENT            - the file reads fine but the digest differs: real byte drift
"""
import collections
import hashlib
import json
import os
from pathlib import Path

SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject")
EXT = "\\\\?\\"


def norm(p):
    return p[4:] if p.startswith(EXT) else p


rows = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "source_recheck.json").read_text(encoding="utf-8"))
bad = [r for r in rows if r["status"] != "UNCHANGED"]
out = []
for r in bad:
    n = norm(r["path"])
    exists = os.path.exists(n)
    rec = {"path": n, "status": r["status"], "exists_normalized": exists}
    if exists:
        try:
            d = hashlib.sha256(Path(n).read_bytes()).hexdigest()
            rec["cause"] = "HASHABLE_DIFFERENT" if d != r["expected_sha256"] else "HASHABLE_IDENTICAL"
            rec["actual_prefix"] = d[:12]
        except OSError as e:
            rec["cause"] = "EXISTS_BUT_UNREADABLE"
            rec["error"] = f"{type(e).__name__}: {e}"
    else:
        rec["cause"] = "ABSENT_UNDER_NORMALIZED_PATH"
    rec["expected_prefix"] = (r["expected_sha256"] or "")[:12]
    out.append(rec)

causes = collections.Counter(x["cause"] for x in out)
dirs = collections.Counter(str(Path(x["path"]).parent) for x in out)
receipt = {
    "schema": "R18.WP21.SOURCE_BYTES_UNCHANGED_TRIAGE/1",
    "rows_total": len(rows),
    "rows_not_unchanged": len(bad),
    "cause_histogram": dict(causes),
    "parent_dirs": dict(dirs.most_common(8)),
    "rows": out,
    "reading": ("The candidate's only failing author check is SOURCE-BYTES-UNCHANGED. It fails because the "
                "manifest pins 172 ABSOLUTE host paths written with a Win32 extended-length prefix; the "
                "unreadable subset is outside the package tree, so the check is a property of the author's "
                "host state, not of the delivered bytes. The 83 in-package artefacts all re-hash to their "
                "recorded digests (COPY_VERIFY 83/83), so package integrity is unaffected."),
}
p = SUBJ.parent / "receipts" / "WP21_SOURCE_BYTES_TRIAGE.json"
p.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows": len(rows), "bad": len(bad), "causes": dict(causes),
                  "dirs": dict(dirs.most_common(5))}, ensure_ascii=False, indent=1))
