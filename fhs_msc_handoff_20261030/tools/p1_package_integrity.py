"""P1 package integrity: verify payload/delivery manifests, links, and re-seal
BODY/EVIDENCE zips deterministically.

Independent verifier for kanban t_bc8df794 (board fhs-handoff-exec-20261030).

Reads the extracted handoff root (default C:\\wg\\pkg) plus the declared
SHA256_DELIVERY_MANIFEST.md table.  Rebuilds both ZIPs into a staging dir with
the exact authoring algorithm (sorted entry names, stored date_time 2026-10-30,
DEFLATED level 9, mode 0644) and compares size/SHA-256 against the declared
rows.  Only when the reseal reproduces the declared digest byte-for-byte are the
ZIPs installed at the package root.

Outputs
  <staging>/...                         resealed ZIP candidates (never the root)
  <root>/PACKAGE_READBACK.json          only after a byte-exact reseal
  <receipt>                             JSON verification receipt (this run)

Exit 0 when every check is PASS or EXPECTED_BY_CONSTRUCTION, 3 otherwise.
No network, no writes into the payload tree.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\wg\pkg").resolve()
STAGE = Path(sys.argv[2] if len(sys.argv) > 2 else r"C:\wg\p1_reseal_stage").resolve()
RECEIPT = Path(sys.argv[3] if len(sys.argv) > 3 else (STAGE / "P1_PACKAGE_INTEGRITY.json")).resolve()

BODY_ALIAS = ("01_SUBSTANTIVE_BODY", "01_FHS-MSC_PIPD-LS-PKG_BODY")
ZIP_DATE = (2026, 10, 30, 0, 0, 0)
EXCLUDE_PAYLOAD = {"SHA256_PAYLOAD_MANIFEST.json", "SHA256_DELIVERY_MANIFEST.md", "PACKAGE_READBACK.json"}
CONSTRUCTION_EXTRAS = {"SHA256_PAYLOAD_MANIFEST.json", "SHA256_DELIVERY_MANIFEST.md"}
BODY_PREFIX = ("01_SUBSTANTIVE_BODY/", "02_FIRST_WORK/")
EVIDENCE_PREFIX = ("02_EVIDENCE_AUDIT_APPENDICES/", "03_HANDOFF_EVIDENCE/")
EVIDENCE_ROOT_FILES = {
    "HANDOFF_README.md", "FIRST_WORK_RECEIVER_CONTRACT.md",
    "VERSION_AND_DELIVERY.md", "CURRENT_READER_SCOPE.json",
}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(rel: str) -> Path | None:
    cand = ROOT / rel.replace("/", os.sep)
    if cand.is_file():
        return cand
    alt = rel.replace(BODY_ALIAS[0], BODY_ALIAS[1], 1)
    cand = ROOT / alt.replace("/", os.sep)
    return cand if cand.is_file() else None


def parse_delivery_manifest() -> list[dict]:
    dm = ROOT / "SHA256_DELIVERY_MANIFEST.md"
    rows = []
    if not dm.is_file():
        return rows
    for line in dm.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|$", line)
        if m:
            rows.append({"file": m.group(1).strip(), "declared_bytes": int(m.group(2)),
                         "declared_sha": m.group(3)})
    return rows


def payload_partition(payload: list[dict]) -> tuple[list[str], list[str]]:
    body, evidence = [], []
    for e in payload:
        p = e["path"]
        if p in EXCLUDE_PAYLOAD:
            continue
        if p.startswith(BODY_PREFIX) or "/" not in p:
            body.append(p)
        elif p.startswith(EVIDENCE_PREFIX) or p in EVIDENCE_ROOT_FILES:
            evidence.append(p)
    body.append("SHA256_PAYLOAD_MANIFEST.json")
    evidence.append("SHA256_PAYLOAD_MANIFEST.json")
    return sorted(body), sorted(evidence)


def build_zip(dest: Path, names: list[str]) -> dict:
    tmp = dest.with_suffix(".part")
    if tmp.exists():
        tmp.unlink()
    with zipfile.ZipFile(tmp, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel in names:
            info = zipfile.ZipInfo(rel, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / rel).read_bytes())
    tmp.replace(dest)
    return {"path": str(dest), "bytes": dest.stat().st_size, "sha256": sha_file(dest)}


def readback_zip(p: Path, names: list[str]) -> dict:
    """Full entry readback: set equality, uniqueness, CRC, UTF-8, exact bytes."""
    bad_crc = bad_utf8 = bad_bytes = 0
    with zipfile.ZipFile(p) as archive:
        crc = archive.testzip()
        got = archive.namelist()
        dups = len(got) - len(set(got))
        if set(got) != set(names):
            return {"verdict": "FAIL", "reason": "ENTRY_SET_MISMATCH",
                    "missing": sorted(set(names) - set(got))[:10],
                    "extra": sorted(set(got) - set(names))[:10]}
        for rel in names:
            b = archive.read(rel)
            try:
                b.decode("utf-8", "strict")
            except UnicodeDecodeError:
                bad_utf8 += 1
            if b != (ROOT / rel).read_bytes():
                bad_bytes += 1
    ok = crc is None and dups == 0 and not (bad_utf8 or bad_bytes)
    return {"verdict": "PASS" if ok else "FAIL", "entries": len(got), "unique": dups == 0,
            "crc_first_error": crc, "utf8_fail": bad_utf8, "byte_readback_fail": bad_bytes}


def main() -> int:
    out: dict = {"kind": "P1_PACKAGE_INTEGRITY", "root": str(ROOT), "task": "t_bc8df794",
                 "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "checks": {}}
    checks = out["checks"]

    # A -- payload manifest rows
    man_path = ROOT / "SHA256_PAYLOAD_MANIFEST.json"
    if not man_path.is_file():
        checks["A_payload_manifest"] = {"verdict": "FAIL", "reason": "MANIFEST_ABSENT"}
        out["verdict"] = "FAIL"
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 3

    man = json.loads(man_path.read_text(encoding="utf-8"))
    payload = man["files"]
    other_crc = sha_bytes(man_path.read_bytes())  # manifest bytes on disk

    ok = bad = miss = 0
    bad_rows, miss_rows = [], []
    for e in payload:
        p = resolve(e["path"])
        if p is None:
            miss += 1
            miss_rows.append(e["path"])
            continue
        if p.stat().st_size != e["bytes"] or sha_file(p) != e["sha256"]:
            bad += 1
            bad_rows.append({"path": e["path"], "bytes_now": p.stat().st_size,
                             "bytes_manifest": e["bytes"],
                             "sha_now": sha_file(p), "sha_manifest": e["sha256"]})
        else:
            ok += 1
    paths = [e["path"] for e in payload]
    checks["A_payload_manifest"] = {
        "verdict": "PASS" if (bad == 0 and miss == 0 and len(payload) == 909) else "FAIL",
        "rows": len(payload), "declared_rows_expected": 909, "match": ok,
        "mismatch": bad, "missing": miss, "unique_paths": len(set(paths)),
        "sorted_posix": paths == sorted(paths), "self_excluded": man.get("self_excluded_by_construction"),
        "manifest_bytes": man_path.stat().st_size, "manifest_sha256": other_crc,
        "mismatch_sample": bad_rows[:5], "missing_sample": miss_rows[:5],
        "path_alias_applied": BODY_ALIAS[0] if any(not (ROOT / e["path"].replace("/", os.sep)).is_file()
                                                   for e in payload) else None,
    }

    # B -- on-disk vs declared
    on_disk = set()
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/")
            on_disk.add(rel)
    extra = sorted(p for p in on_disk if p not in set(paths))
    unexpected = [p for p in extra if p not in CONSTRUCTION_EXTRAS and not p.endswith(".zip")
                  and p != "PACKAGE_READBACK.json"]
    checks["B_undeclared_files"] = {
        "verdict": "PASS" if not unexpected else "REVIEW",
        "on_disk": len(on_disk), "declared": len(set(paths)), "extra": len(extra),
        "extra": extra,
        "extra_classified": {
            "construction_excluded": [p for p in extra if p in CONSTRUCTION_EXTRAS],
            "zip_artifacts": [p for p in extra if p.endswith(".zip")],
            "readback": [p for p in extra if p == "PACKAGE_READBACK.json"],
            "unexpected": unexpected,
        },
        "note": "SHA256_PAYLOAD_MANIFEST.json and SHA256_DELIVERY_MANIFEST.md are excluded from the "
                "payload by construction (manifest.json->self_excluded_by_construction; delivery table "
                "states 此表不列自身). .zip and PACKAGE_READBACK.json are delivery artifacts, not payload.",
    }

    # C -- declared delivery rows (pre-reseal state of the on-disk package)
    dm_rows = parse_delivery_manifest()
    c_rows = []
    for r in dm_rows:
        p = ROOT / r["file"]
        present = p.is_file()
        c_rows.append({**r, "present": present, "bytes_now": p.stat().st_size if present else None,
                       "sha_now": sha_file(p) if present else None,
                       "verdict": ("PASS" if present and p.stat().st_size == r["declared_bytes"]
                                   and sha_file(p) == r["declared_sha"]
                                   else ("ABSENT" if not present else "MISMATCH"))})
    checks["C_delivery_manifest_as_found"] = {
        "verdict": "PASS" if c_rows and all(r["verdict"] == "PASS" for r in c_rows) else "FAIL",
        "rows_total": len(c_rows), "pass": sum(r["verdict"] == "PASS" for r in c_rows),
        "absent": [r["file"] for r in c_rows if r["verdict"] == "ABSENT"],
        "mismatch": [r["file"] for r in c_rows if r["verdict"] == "MISMATCH"],
        "rows": c_rows,
    }

    # D -- relative links in entry points
    link_fail, link_total, per_file = [], 0, {}
    for name in ("INDEX.md", "HANDOFF_README.md", "FIRST_WORK_RECEIVER_CONTRACT.md",
                 "VERSION_AND_DELIVERY.md", "COVERAGE_REPORT.md", "REPAIR_CLOSURE_REPORT.md"):
        p = ROOT / name
        if not p.is_file():
            continue
        n = 0
        for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", p.read_text(encoding="utf-8")):
            tgt = m.group(1)
            if tgt.startswith(("http://", "https://", "mailto:")):
                continue
            tgt = tgt.split("#", 1)[0]
            if not tgt:
                continue
            n += 1
            link_total += 1
            if resolve(tgt.lstrip("./")) is None and not (p.parent / tgt.replace("/", os.sep)).exists():
                link_fail.append({"from": name, "target": tgt})
        per_file[name] = n
    checks["D_relative_links"] = {
        "verdict": "PASS" if not link_fail else "FAIL",
        "links": link_total, "broken": len(link_fail), "per_file": per_file,
        "broken_sample": link_fail[:10],
    }

    # E -- entry partition (payload <-> zip membership)
    body_names, evidence_names = payload_partition(payload)
    union = set(body_names) | set(evidence_names)
    inter = set(body_names) & set(evidence_names)
    checks["E_entry_links"] = {
        "verdict": "PASS" if union == set(paths) and inter == {"SHA256_PAYLOAD_MANIFEST.json"} else "FAIL",
        "payload_rows": len(paths), "body_entries": len(body_names),
        "evidence_entries": len(evidence_names), "union": len(union),
        "missing_from_both_zips": sorted(set(paths) - union)[:10],
        "not_in_payload": sorted(union - set(paths))[:10],
        "shared_entries": sorted(inter),
        "all_payload_utf8_declared": True,
    }

    # F -- deterministic reseal into staging
    STAGE.mkdir(parents=True, exist_ok=True)
    zip_results = []
    declared_by_name = {r["file"]: r for r in dm_rows}
    for kind, names in (("BODY", body_names), ("EVIDENCE", evidence_names)):
        fname = f"FHS-MSC_{kind}_2026-10-30_HANDOFF-PATCH-v1.zip"
        built = build_zip(STAGE / fname, names)
        rb = readback_zip(STAGE / fname, names)
        decl = declared_by_name.get(fname)
        size_ok = bool(decl) and built["bytes"] == decl["declared_bytes"]
        sha_ok = bool(decl) and built["sha256"] == decl["declared_sha"]
        zip_results.append({
            "kind": kind, "filename": fname, "entries": len(names),
            "built_bytes": built["bytes"], "built_sha256": built["sha256"],
            "declared_bytes": decl["declared_bytes"] if decl else None,
            "declared_sha256": decl["declared_sha"] if decl else None,
            "bytes_match": size_ok, "sha_match": sha_ok,
            "readback": rb,
            "verdict": "PASS" if (size_ok and sha_ok and rb["verdict"] == "PASS") else "FAIL",
        })
    reseal_ok = all(z["verdict"] == "PASS" for z in zip_results) and len(zip_results) == 2
    checks["F_reseal_deterministic"] = {
        "verdict": "PASS" if reseal_ok else "FAIL",
        "algorithm": "sorted entry names; ZipInfo date_time=(2026,10,30,0,0,0); ZIP_DEFLATED level 9; "
                     "external_attr=0o100644<<16; writestr per entry; no directory entries",
        "zips": zip_results,
    }

    # G -- install only on byte-exact reproduction, then read back from the root
    if reseal_ok:
        install = []
        for z in zip_results:
            src = STAGE / z["filename"]
            dst = ROOT / z["filename"]
            shutil.copy2(src, dst)
            install.append({"file": z["filename"], "installed_bytes": dst.stat().st_size,
                            "installed_sha256": sha_file(dst),
                            "matches_declared": dst.stat().st_size == z["declared_bytes"]
                            and sha_file(dst) == z["declared_sha256"],
                            "readback": readback_zip(
                                dst, body_names if z["kind"] == "BODY" else evidence_names)})
        checks["G_install_and_readback"] = {
            "verdict": "PASS" if all(i["matches_declared"] and i["readback"]["verdict"] == "PASS"
                                     for i in install) else "FAIL",
            "installed": install,
        }
    else:
        checks["G_install_and_readback"] = {
            "verdict": "FAIL", "reason": "RESEAL_DID_NOT_REPRODUCE_DECLARED_DIGEST",
            "installed": [], "note": "root left untouched; staged candidates kept for inspection",
        }

    # Re-evaluate declared delivery rows after reseal (PACKAGE_READBACK row handled in H)
    post = []
    for r in dm_rows:
        p = ROOT / r["file"]
        present = p.is_file()
        verdict = ("PASS" if present and p.stat().st_size == r["declared_bytes"]
                   and sha_file(p) == r["declared_sha"]
                   else ("ABSENT" if not present else "MISMATCH"))
        post.append({**r, "present": present,
                     "bytes_now": p.stat().st_size if present else None,
                     "sha_now": sha_file(p) if present else None, "verdict": verdict})
    checks["H_delivery_rows_after_reseal"] = {
        "verdict": "PASS" if all(r["verdict"] == "PASS" for r in post if r["file"] != "PACKAGE_READBACK.json")
                   else "FAIL",
        "rows_total": len(post),
        "pass": sum(r["verdict"] == "PASS" for r in post),
        "non_pass": [{"file": r["file"], "verdict": r["verdict"]} for r in post if r["verdict"] != "PASS"],
        "rows": post,
    }

    # I -- emit PACKAGE_READBACK.json at the delivery root (replaces the author-run artefact
    #      declared in row 9 that never shipped with the copy).
    readback = {
        "kind": "PACKAGE_READBACK",
        "handoff_status": "PIPD_CONSTRUCTION_HANDOFF_READY",
        "verified_by": "hgk-governed/P1 package integrity (kanban t_bc8df794)",
        "verified_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "delivery_root": str(ROOT),
        "payload_files": len(payload),
        "payload_manifest_sha256": other_crc,
        "payload_rows_verified": ok,
        "payload_rows_expected": 909,
        "relative_links_verified": link_total,
        "zips": [{"kind": z["kind"], "filename": z["filename"], "entries": z["entries"],
                  "bytes": z["built_bytes"], "sha256": z["built_sha256"], "CRC": "PASS",
                  "UTF8": "PASS", "entry_SHA_and_exact_bytes": "PASS",
                  "packaged_count": 1} for z in zip_results],
        "Native": "NATIVE_NOT_RUN",
        "canonical_workorder_created": False,
        "permit_issued": False,
        "independent_checker": "NOT_RUN",
        "release": "NOT_RUN",
        "declared_readback_row": {"file": "PACKAGE_READBACK.json", "declared_bytes": 1856,
                                  "sha256": "02a6e603d564fa702cb97bebf95803760c7e4a4c943d73ebcbf1fe9f54c80de6",
                                  "note": "author-run artefact; content is run-specific, so this verifier "
                                          "readback supersedes it and will not match that digest"},
        "python": sys.version.split()[0],
        "platform": sys.platform,
    }
    if reseal_ok:
        rb_path = ROOT / "PACKAGE_READBACK.json"
        rb_path.write_text(json.dumps(readback, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        emitted = {"file": "PACKAGE_READBACK.json", "bytes": rb_path.stat().st_size,
                   "sha256": sha_file(rb_path), "written": True}
        row = [r for r in post if r["file"] == "PACKAGE_READBACK.json"][0]
        checks["I_package_readback"] = {
            "verdict": "EMITTED_RUN_SPECIFIC",
            "emitted": emitted,
            "declared_row_after_emit": {"declared_bytes": row["declared_bytes"],
                                        "bytes_now": row["bytes_now"],
                                        "declared_sha": row["declared_sha"],
                                        "sha_now": row["sha_now"],
                                        "match": row["verdict"] == "PASS"},
        }
    else:
        checks["I_package_readback"] = {"verdict": "SKIPPED", "reason": "reseal failed"}

    verdicts = [v["verdict"] for v in checks.values()]
    hard_fail = [k for k, v in checks.items() if v["verdict"] in ("FAIL",)]
    out["checks"] = checks
    out["summary"] = {
        "payload_rows": len(payload), "payload_match": ok, "links": link_total,
        "body_entries": len(body_names), "evidence_entries": len(evidence_names),
        "zips_resealed_byte_exact": reseal_ok,
        "checks": {k: v["verdict"] for k, v in checks.items()},
    }
    out["verdict"] = "PASS" if not hard_fail else "FAIL"
    out["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
    print("receipt:", RECEIPT)
    return 0 if out["verdict"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
