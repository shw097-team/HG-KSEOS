"""R19 exact-byte locator repair for the r2-revision2 source manifest.

Defect (measured R19): `03_TESTS_AND_READBACK/source_manifest.json` pins 29 documents
inside `...\\FHS-MSC_PIPD-LS-PKG\\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_DRAFT\\...`, a
directory that was later renamed into `...\\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\\OLD\\`.
`validate.py`'s SOURCE-BYTES-UNCHANGED case therefore reports 29 UNREADABLE -> 2788/1.

Repair rule (no oracle change): a locator may be rewritten ONLY when the candidate file's
full SHA-256 equals the manifest's expected full SHA-256. No name/size/prefix matching.
Outputs: RELOCATION_INDEX.json (evidence) and an optional repaired manifest copy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

MANIFEST_REL = "03_TESTS_AND_READBACK/source_manifest.json"


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(p: str) -> str:
    return p[4:] if p.startswith("\\\\?\\") else p


def sweep(roots: list[pathlib.Path], skip_dirs: set[str]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    seen = 0
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith("__pycache__")]
            for name in filenames:
                p = pathlib.Path(dirpath) / name
                try:
                    if p.stat().st_size > 64 << 20:
                        continue
                    index.setdefault(sha256(p), []).append(str(p))
                    seen += 1
                except OSError:
                    continue
    print(f"[sweep] indexed {seen} files under {len(roots)} roots", file=sys.stderr)
    return index


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--copy", required=True, help="isolated copy of the package")
    ap.add_argument("--candidate-root", action="append", required=True)
    ap.add_argument("--out", required=True, help="RELOCATION_INDEX.json path")
    ap.add_argument("--write-repaired-manifest", default=None)
    a = ap.parse_args()

    copy = pathlib.Path(a.copy).resolve()
    manifest_path = copy / MANIFEST_REL
    rows = json.loads(manifest_path.read_text(encoding="utf-8"))
    index = sweep([pathlib.Path(r).resolve() for r in a.candidate_root], {".git", "__pycache__"})

    at = datetime.now(timezone.utc).isoformat()
    repaired, unresolved, unchanged = [], [], 0
    for r in rows:
        path = norm(r["path"])
        loc = pathlib.Path(path)
        expected = r["sha256"]
        if loc.is_file():
            actual = sha256(loc)
            if actual == expected:
                unchanged += 1
                continue
            unresolved.append({"path": path, "expected_sha256": expected, "actual_sha256": actual,
                               "status": "DRIFT_AT_ORIGINAL_LOCATION", "candidates": []})
            continue
        hits = [c for c in index.get(expected, []) if not c.lower().startswith(str(copy).lower())]
        if len(hits) == 1:
            rec = {"path": path, "expected_sha256": expected, "resolved_path": hits[0],
                   "status": "RELOCATED_BY_EXACT_BYTES", "candidates_considered": 1}
            repaired.append(rec)
        elif len(hits) > 1:
            rec = {"path": path, "expected_sha256": expected, "resolved_path": None,
                   "status": "AMBIGUOUS_MULTIPLE_EXACT_MATCHES", "candidates": hits}
            unresolved.append(rec)
        else:
            unresolved.append({"path": path, "expected_sha256": expected, "resolved_path": None,
                               "status": "NOT_FOUND_BY_EXACT_BYTES", "candidates": []})

    out = {
        "schema": "R19.SOURCE_RELOCATION_INDEX/1",
        "at": at,
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "rows_total": len(rows),
        "verdict_unchanged_in_place": unchanged,
        "verdict_relocated": len(repaired),
        "verdict_unresolved": len(unresolved),
        "rule": "a locator is rewritten only on full 64-hex exact-byte equality; no name/size/prefix matching",
        "relocated": repaired,
        "unresolved": unresolved,
    }
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    if a.write_repaired_manifest:
        mapping = {r["path"]: r["resolved_path"] for r in repaired}
        new_rows = []
        for r in rows:
            r2 = dict(r)
            p = norm(r["path"])
            if p in mapping:
                r2["path"] = "\\\\?\\" + mapping[p]
                r2["locator_repaired_from"] = p
                r2["locator_repair_rule"] = "EXACT_BYTES_SHA256_EQUAL"
            new_rows.append(r2)
        pathlib.Path(a.write_repaired_manifest).write_text(
            json.dumps(new_rows, ensure_ascii=False, indent=1), encoding="utf-8")

    print(json.dumps({k: out[k] for k in ("rows_total", "verdict_unchanged_in_place",
                                          "verdict_relocated", "verdict_unresolved")}, indent=1))
    return 0 if not unresolved else 2


if __name__ == "__main__":
    raise SystemExit(main())
