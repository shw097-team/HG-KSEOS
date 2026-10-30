"""Verify the FHS-MSC HANDOFF-PATCH-v1 delivery on disk.

Read-only: never writes into the package. Emits a JSON receipt on stdout.

Checks
  A payload-manifest rows (path/bytes/sha256) against the extracted tree
  B files present on disk but absent from the manifest (undeclared payload)
  C delivery-manifest rows (the .md table) against reality, incl. ZIPs
  D relative links inside the entry-point markdown files
  E claim-ceiling keywords that the package itself asserts

Exit code 0 only when every check is PASS; 3 otherwise.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\wg\pkg")
ALT = ("01_SUBSTANTIVE_BODY", "01_FHS-MSC_PIPD-LS-PKG_BODY")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(rel: str) -> Path | None:
    cand = ROOT / rel.replace("/", os.sep)
    if cand.is_file():
        return cand
    alt = rel.replace(ALT[0], ALT[1])
    cand = ROOT / alt.replace("/", os.sep)
    if cand.is_file():
        return cand
    return None


def main() -> int:
    out: dict = {"root": str(ROOT), "checks": {}}

    man = json.loads((ROOT / "SHA256_PAYLOAD_MANIFEST.json").read_text(encoding="utf-8"))
    rows = man["files"]
    ok = bad = miss = 0
    bad_rows, miss_rows = [], []
    for e in rows:
        p = resolve(e["path"])
        if p is None:
            miss += 1
            miss_rows.append(e["path"])
            continue
        if p.stat().st_size != e["bytes"] or sha256(p) != e["sha256"]:
            bad += 1
            bad_rows.append({"path": e["path"], "bytes_now": p.stat().st_size,
                             "bytes_manifest": e["bytes"], "sha_now": sha256(p)[:16],
                             "sha_manifest": e["sha256"][:16]})
        else:
            ok += 1
    out["checks"]["A_payload_manifest"] = {
        "verdict": "PASS" if (bad == 0 and miss == 0) else "FAIL",
        "rows": len(rows), "match": ok, "mismatch": bad, "missing": miss,
        "mismatch_sample": bad_rows[:10], "missing_sample": miss_rows[:10],
        "path_alias_applied": ALT[1],
    }

    declared = {e["path"] for e in rows}
    on_disk = set()
    for dirpath, _dirs, files in os.walk(ROOT):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/")
            on_disk.add(rel)
    extra = sorted(p for p in on_disk if p not in declared)
    out["checks"]["B_undeclared_files"] = {
        "verdict": "PASS" if not extra else "REVIEW",
        "on_disk": len(on_disk), "declared": len(declared), "extra": len(extra),
        "extra_sample": extra[:20],
    }

    # C delivery manifest table
    dm = ROOT / "SHA256_DELIVERY_MANIFEST.md"
    c_rows = []
    if dm.is_file():
        for line in dm.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|$", line)
            if m:
                name, nbytes, want = m.group(1), int(m.group(2)), m.group(3)
                p = ROOT / name
                have = sha256(p) if p.is_file() else None
                c_rows.append({
                    "file": name, "declared_bytes": nbytes, "declared_sha": want,
                    "present": p.is_file(),
                    "bytes_now": p.stat().st_size if p.is_file() else None,
                    "sha_now": have,
                    "verdict": "PASS" if (have == want and p.is_file() and p.stat().st_size == nbytes) else
                               ("ABSENT" if not p.is_file() else "MISMATCH"),
                })
    out["checks"]["C_delivery_manifest"] = {
        "verdict": "PASS" if c_rows and all(r["verdict"] == "PASS" for r in c_rows) else "FAIL",
        "rows": c_rows,
    }

    # D relative links in entry points
    link_fail = []
    link_total = 0
    for name in ("INDEX.md", "HANDOFF_README.md", "FIRST_WORK_RECEIVER_CONTRACT.md"):
        p = ROOT / name
        if not p.is_file():
            continue
        for m in re.finditer(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)", p.read_text(encoding="utf-8")):
            tgt = m.group(1).strip()
            if tgt.startswith(("http://", "https://", "mailto:")):
                continue
            link_total += 1
            if resolve(tgt) is None:
                link_fail.append({"from": name, "target": tgt})
    out["checks"]["D_relative_links"] = {
        "verdict": "PASS" if not link_fail else "FAIL",
        "links": link_total, "broken": len(link_fail), "broken_sample": link_fail[:10],
    }

    # E claim ceiling keywords
    claims = {}
    for name in ("VERSION_AND_DELIVERY.md", "HANDOFF_README.md", "CURRENT_READER_SCOPE.json"):
        p = ROOT / name
        t = p.read_text(encoding="utf-8") if p.is_file() else ""
        claims[name] = {
            "NATIVE_NOT_RUN": t.count("NATIVE_NOT_RUN") + t.count("NATIVE_NOT_RUN\"") + t.count('"NONE"'),
            "RELEASE_NOT_RUN": t.count("NOT_RUN"),
            "PIPD_CONSTRUCTION_HANDOFF_READY": t.count("PIPD_CONSTRUCTION_HANDOFF_READY"),
        }
    out["checks"]["E_claim_keywords"] = {"verdict": "PASS", "by_file": claims}

    out["overall"] = "PASS" if all(v["verdict"] == "PASS" for v in out["checks"].values()) else "FAIL"
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["overall"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
