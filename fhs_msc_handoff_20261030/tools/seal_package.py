"""Seal the handoff delivery into two deterministic archives and read them back.

The delivered tree on disk carries no ZIPs and no PACKAGE_READBACK.json even though
SHA256_DELIVERY_MANIFEST.md lists both, so the two declared SHAs cannot be re-verified.
This tool does NOT claim to reproduce them: it produces a NEW, reproducible seal and says so.

Recipe (fixed, so two runs are byte-identical):
  * entries sorted by posix path, one entry per file, NO directory entries
  * timestamp pinned to 1980-01-01T00:00:00 (zip epoch)
  * ZIP_DEFLATED level 9, external_attr 0644
  * BODY     = the seventeen current books under 01_SUBSTANTIVE_BODY/
  * EVIDENCE = 02_EVIDENCE_AUDIT_APPENDICES + 02_FIRST_WORK + 03_HANDOFF_EVIDENCE + root docs

Readback per entry: CRC32, byte length, SHA-256, and UTF-8 decodability for text entries.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

PKG = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\wg\pkg")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else r"C:\wg\seal2")
STAMP = (1980, 1, 1, 0, 0, 0)
ROOT_DOCS = ["INDEX.md", "COVERAGE_REPORT.md", "REPAIR_CLOSURE_REPORT.md", "VERSION_AND_DELIVERY.md",
             "HANDOFF_README.md", "FIRST_WORK_RECEIVER_CONTRACT.md", "CURRENT_READER_SCOPE.json",
             "SHA256_PAYLOAD_MANIFEST.json", "SHA256_DELIVERY_MANIFEST.md"]


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def collect() -> tuple[list[tuple[str, Path]], list[tuple[str, Path]]]:
    body = [("01_SUBSTANTIVE_BODY/" + p.name, p)
            for p in sorted((PKG / "01_SUBSTANTIVE_BODY").glob("*.md"))]
    ev: list[tuple[str, Path]] = []
    for sub in ("02_EVIDENCE_AUDIT_APPENDICES", "02_FIRST_WORK", "03_HANDOFF_EVIDENCE"):
        base = PKG / sub
        if base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file():
                    ev.append((p.relative_to(PKG).as_posix(), p))
    for name in ROOT_DOCS:
        p = PKG / name
        if p.is_file():
            ev.append((name, p))
    return body, ev


def write_zip(path: Path, entries: list[tuple[str, Path]]) -> dict:
    rows = []
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel, p in sorted(entries, key=lambda x: x[0]):
            data = p.read_bytes()
            zi = zipfile.ZipInfo(rel, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
            rows.append({"path": rel, "bytes": len(data), "sha256": sha_bytes(data),
                         "crc32": f"{zipfile.crc32(data) & 0xffffffff:08x}"})
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": sha_bytes(path.read_bytes()),
            "entries": len(rows), "entry_rows": rows}


def readback(zip_path: Path, expect: dict) -> dict:
    problems = []
    with zipfile.ZipFile(zip_path) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        if len(infos) != expect["entries"]:
            problems.append(f"entry_count:{len(infos)}!={expect['entries']}")
        for i in infos:
            data = z.read(i.filename)
            row = next((r for r in expect["entry_rows"] if r["path"] == i.filename), None)
            if row is None:
                problems.append(f"undeclared_entry:{i.filename}")
                continue
            if zipfile.crc32(data) & 0xffffffff != i.CRC or f"{i.CRC:08x}" != row["crc32"]:
                problems.append(f"crc_mismatch:{i.filename}")
            if len(data) != row["bytes"] or sha_bytes(data) != row["sha256"]:
                problems.append(f"bytes_or_sha_mismatch:{i.filename}")
            if i.filename.endswith((".md", ".json", ".txt", ".yaml", ".yml", ".tsv", ".csv")):
                try:
                    data.decode("utf-8")
                except UnicodeDecodeError:
                    problems.append(f"utf8_invalid:{i.filename}")
    return {"file": zip_path.name, "entries_verified": expect["entries"], "problems": problems,
            "verdict": "PASS" if not problems else "FAIL"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    body, ev = collect()
    z1 = write_zip(OUT / "FHS-MSC_BODY_2026-10-30_HANDOFF-PATCH-v1-EXEC.zip", body)
    z2 = write_zip(OUT / "FHS-MSC_EVIDENCE_2026-10-30_HANDOFF-PATCH-v1-EXEC.zip", ev)
    rb = {
        "schema": "FHS-MSC-HANDOFF-PACKAGE-READBACK/1",
        "generated_by": "tools/seal_package.py",
        "scope": "NEW_SEAL_NOT_A_REPRODUCTION_OF_THE_DECLARED_ARCHIVES",
        "why_new_seal": ("the delivered directory carried neither ZIP nor PACKAGE_READBACK.json, so the "
                         "two SHAs in SHA256_DELIVERY_MANIFEST.md could not be re-verified at all; this "
                         "seal is reproducible but is NOT claimed byte-identical to them"),
        "declared": [
            {"file": "FHS-MSC_BODY_2026-10-30_HANDOFF-PATCH-v1.zip",
             "declared_bytes": 4007065,
             "declared_sha256": "5e722cfbf200efc17de246fb5bfe877c5509b5d4d3849d42921ab56b9a86af5b",
             "present_on_disk": False},
            {"file": "FHS-MSC_EVIDENCE_2026-10-30_HANDOFF-PATCH-v1.zip",
             "declared_bytes": 25914281,
             "declared_sha256": "0e7763b8856f38ad32f9714d7415bb19c215903c72576f9b2f433790c2e70a6d",
             "present_on_disk": False},
        ],
        "zips": [{k: v for k, v in z1.items() if k != "entry_rows"},
                 {k: v for k, v in z2.items() if k != "entry_rows"}],
        "readback": [readback(OUT / z1["file"], z1), readback(OUT / z2["file"], z2)],
    }
    rb["verdict"] = "PASS" if all(r["verdict"] == "PASS" for r in rb["readback"]) else "FAIL"
    (OUT / "PACKAGE_READBACK.json").write_text(json.dumps(rb, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8")
    # idempotence: a second seal from the same input must be byte-identical
    z1b = write_zip(OUT / "_idem_body.zip", body)
    z2b = write_zip(OUT / "_idem_evidence.zip", ev)
    rb2 = {"body_identical": z1b["sha256"] == z1["sha256"],
           "evidence_identical": z2b["sha256"] == z2["sha256"]}
    for f in ("_idem_body.zip", "_idem_evidence.zip"):
        (OUT / f).unlink(missing_ok=True)
    rb["idempotence"] = rb2
    (OUT / "PACKAGE_READBACK.json").write_text(json.dumps(rb, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8")
    print(json.dumps({"verdict": rb["verdict"], "idempotence": rb2,
                      "zips": rb["zips"], "readback": rb["readback"]}, ensure_ascii=False, indent=1))
    return 0 if rb["verdict"] == "PASS" and all(rb2.values()) else 3


if __name__ == "__main__":
    raise SystemExit(main())
