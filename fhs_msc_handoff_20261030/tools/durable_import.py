#!/usr/bin/env python3
"""Durable-import manifest builder.

Turns a directory that exists only on disk into something a stranger can verify: one row per file
(path / bytes / SHA-256), a rollup digest, and an explicit list of what was excluded and why.

It does NOT copy the payload. Copying 236 MB (or 900 MB) of evidence into git history is the wrong
trade; the durable form is: manifest in git + sealed archive as an immutable release asset, bound by
digest. This tool produces the first half and the receipt that binds the second.

Usage:
    python durable_import.py --root DIR --id ID --out OUTDIR
                              [--exclude-glob PATTERN ...] [--derived-glob PATTERN ...]
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# The \\?\ extended-length prefix, assembled from code points so no layer of quoting can mangle it.
# Without it, os.walk silently stops at the first path over MAX_PATH: a 911-file delivery then
# measures as 95 files, and every digest built from it is wrong in a way that still looks green.
PFX = chr(92) * 2 + "?" + chr(92)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--exclude-glob", action="append", default=[])
    ap.add_argument("--derived-glob", action="append", default=[],
                    help="reproducible derived artefacts: recorded, not hashed into the payload rollup")
    a = ap.parse_args()

    root = Path(a.root)
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    base = (PFX + str(root.resolve())) if os.name == "nt" else str(root)
    walk_errors: list[dict] = []

    def _err(e):
        walk_errors.append({"path": str(getattr(e, "filename", "?")), "error": type(e).__name__})

    rows, derived, skipped = [], [], []
    total = 0
    for dirpath, _dirnames, filenames in os.walk(base, onerror=_err):
        for fn in sorted(filenames):
            apath = Path(dirpath) / fn
            try:
                if not apath.is_file():
                    continue
                rel = apath.relative_to(base).as_posix()
                size = apath.stat().st_size
            except OSError:
                walk_errors.append({"path": str(apath), "error": "OSError"})
                continue
            if any(fnmatch.fnmatch(rel, g) for g in a.exclude_glob):
                skipped.append({"path": rel, "reason": "excluded by rule"})
                continue
            if any(fnmatch.fnmatch(rel, g) for g in a.derived_glob):
                derived.append({"path": rel, "bytes": size, "reason": "reproducible derived artefact"})
                continue
            rows.append({"path": rel, "bytes": size, "sha256": sha256_file(apath)})
            total += size

    rollup = hashlib.sha256()
    for r in rows:
        rollup.update(f"{r['path']}\0{r['bytes']}\0{r['sha256']}\n".encode())

    manifest = {
        "schema": "DURABLE-IMPORT-MANIFEST/1",
        "id": a.id,
        "source_root": str(root.resolve()),
        "built_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "files": rows,
        "files_count": len(rows),
        "payload_bytes": total,
        "payload_rollup_sha256": rollup.hexdigest(),
        "derived_not_hashed": derived,
        "skipped": skipped,
        "walk_errors": walk_errors,
        "durability": {
            "state": "MANIFEST_ONLY",
            "what_is_needed": [
                "commit this manifest",
                "seal the payload into one deterministic archive and publish it as an immutable release asset",
                "record the archive digest in the receipt",
                "register the id in the control-plane registry",
            ],
            "why": "a directory on disk is not durable: no lineage, no digest other than this one, "
                   "no way for a second party to verify it after the machine changes",
        },
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / f"manifest.{a.id}.json"
    dest.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({
        "id": a.id, "files": len(rows), "bytes": total, "rollup": rollup.hexdigest(),
        "derived": len(derived), "skipped": len(skipped), "walk_errors": len(walk_errors),
        "manifest": str(dest.resolve()),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
