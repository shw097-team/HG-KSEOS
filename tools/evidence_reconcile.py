#!/usr/bin/env python3
"""A7: assert that the numbers a document claims are the numbers its receipts measured.

Why this exists: during R20 the prose drifted from the receipts twice (a stale archive digest, a package
count that appeared in two places). Prose is not evidence; a document that disagrees with its own receipts
is a defect even when both are "true" in isolation. This tool reads the receipts and REFUSES when the
document's numbers differ -- it never rewrites the document.

Usage:
    python tools/evidence_reconcile.py \
        --receipts var/R20-FHS-20261029/receipts \
        --doc evidence/R20-FHS-20261029/EVIDENCE_INDEX.md

Exit: 0 = every checked number matches, 3 = mismatch (each printed), 4 = a receipt could not be read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--doc", required=True)
    ap.add_argument("--archive", default=None,
                    help="optional archive path; when given, its sha256/bytes/entries are measured directly")
    a = ap.parse_args(argv)

    rdir, doc = Path(a.receipts), Path(a.doc)
    if not doc.is_file():
        print(f"doc missing: {doc}", file=sys.stderr)
        return 4
    raw = doc.read_text(encoding="utf-8", errors="replace")
    # Compare VALUES, not typography: a number written 13,578,117 and one written 13578117 are the same
    # measurement, and failing on the comma would train the reader to ignore this tool.
    text = re.sub(r"[,_]", "", raw)
    text_plain = raw

    checks: list[tuple[str, object, bool]] = []

    def add(label: str, value: object, present=None) -> None:
        needle = str(value)
        ok = (needle in text) or (needle in text_plain)
        checks.append((label, needle, ok if present is None else bool(present)))

    try:
        rep = load(rdir / "P1D_R20B_CHECKSUM_REPAIR.json")
        add("archive sha256", rep["new_zip_sha256"])
        add("archive bytes", rep["new_zip_bytes"])
        add("checksum rows verified", rep["rows_verified"])
        add("archive entries", rep["entries"])
        idem = load(rdir / "P1C_IDEMPOTENCE.json")
        add("validator passed", idem["passed"])
        add("validator failed", idem["failed"])
        add("case count", idem["case_count"])
        tab = load(rdir / "P2A_AUTHOR_TABLES.json")
        add("hold rows", tab["hold_rows"])
        add("stage rows", tab["stage_rows"])
        add("oracle cells", tab["oracle_cells"])
        den = load(rdir / "DENOMINATOR.json")
        add("subject file count", den["file_count"])
        add("subject bytes", den["total_bytes"])
        add("max abs path len", den["max_abs_path_len"])
    except Exception as exc:  # noqa: BLE001 - unreadable receipt is its own failure
        print(f"receipt unreadable: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4

    if a.archive:
        arc = Path(a.archive)
        if not arc.is_file():
            print(f"archive missing: {arc}", file=sys.stderr)
            return 4
        import zipfile
        with zipfile.ZipFile(arc) as zf:
            entries = [i for i in zf.infolist()]
        checks.append(("measured archive sha256 == receipt",
                       rep["new_zip_sha256"], sha256_file(arc) == rep["new_zip_sha256"]))
        checks.append(("measured archive bytes == receipt",
                       str(rep["new_zip_bytes"]), arc.stat().st_size == rep["new_zip_bytes"]))
        checks.append(("measured entry count == receipt",
                       str(rep["entries"]), len(entries) == rep["entries"]))
        checks.append(("directory entries", "0", sum(1 for i in entries if i.is_dir()) == 0))

    bad = [c for c in checks if not c[2]]
    for label, needle, ok in checks:
        print(f"{'OK  ' if ok else 'MISS'} {label}: {needle}")
    print(f"\nchecked={len(checks)} mismatches={len(bad)}")
    return 0 if not bad else 3


if __name__ == "__main__":
    raise SystemExit(main())
