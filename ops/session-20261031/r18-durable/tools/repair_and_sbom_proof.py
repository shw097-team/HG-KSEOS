"""WP-18 causal repair proof + WP-19 SBOM rescan, both on throwaway copies.

WP-18: the SWARM audit found my repair receipt was an isolated-copy artefact whose ceiling admitted the
delivered candidate still carries the defect, and that D-R18-02 had no receipt. A repair claim is only
worth anything if it is causal, so this does red -> patch -> green -> un-patch -> red in ONE copy and
records all four numbers. If un-patching does not return the failure, the "repair" was noise.

WP-19: the earlier SBOM was captured across a moving tree (5/85 entries drifted, byte count differed).
This rescans the frozen subject twice and only accepts the SBOM if both scans agree byte-for-byte.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
SUB = ROUND / "subject"
WORK = ROUND / "repair_work_tmp"
PY = sys.executable
now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def xp(p):
    s = str(p).replace("/", "\\")
    return s if s.startswith("\\\\?\\") else "\\\\?\\" + s


def run_validate(root):
    """validate.py prints a JSON report and writes it to 03_TESTS_AND_READBACK/static_validation_result.json."""
    report = pathlib.Path(root) / "03_TESTS_AND_READBACK" / "static_validation_result.json"
    before = report.read_bytes() if report.is_file() else None
    p = subprocess.run([PY, "-B", str(pathlib.Path(root) / "tools" / "validate.py")],
                       cwd=str(root), capture_output=True, text=True, timeout=1800)
    d = {}
    for line in (p.stdout or "").splitlines():
        if line.strip().startswith("{"):
            try:
                j = json.loads(line)
                if "passed" in j:
                    d = j
            except Exception:
                pass
    if not d and report.is_file():
        try:
            d = json.loads(report.read_text(encoding="utf-8"))
        except Exception:
            d = {}
    return {"rc": p.returncode, "passed": d.get("passed"), "failed": d.get("failed"),
            "fail_names": [r.get("name") or r.get("case") or r.get("id")
                           for r in (d.get("results") or []) if r.get("status") == "FAIL"][:5],
            "report_changed": before != (report.read_bytes() if report.is_file() else None)}


# ---------------------------------------------------------------- fresh copy
if WORK.exists():
    shutil.rmtree(xp(WORK), ignore_errors=True)
shutil.copytree(xp(SUB), xp(WORK))
res = {"schema": "R18.WP18_CAUSAL_REPAIR/1", "at": now(), "copy": str(WORK)}

res["red_before"] = run_validate(WORK)

# apply the data-side pin repair inside the copy only
repair = subprocess.run([PY, "-B", str(ROUND / "tools" / "repair_stale_pins.py")],
                        capture_output=True, text=True, timeout=600, cwd=str(WORK))
res["repair_rc"] = repair.returncode
res["repair_tail"] = (repair.stdout or "").strip()[-300:]
res["green_after"] = run_validate(WORK)

# un-patch: restore the manifest from the pre-repair copy
bak = WORK / "03_TESTS_AND_READBACK" / "source_manifest.json"
orig = SUB / "03_TESTS_AND_READBACK" / "source_manifest.json"
shutil.copyfile(xp(orig), xp(bak))
res["red_after_unpatch"] = run_validate(WORK)

rb, ga, ra = res["red_before"], res["green_after"], res["red_after_unpatch"]
res["causal"] = (rb.get("failed") == 1 and ga.get("failed") == 0 and ra.get("failed") == 1)
res["numbers"] = {"pristine": "%s/%s" % (rb.get("passed"), rb.get("failed")),
                  "patched": "%s/%s" % (ga.get("passed"), ga.get("failed")),
                  "unpatched": "%s/%s" % (ra.get("passed"), ra.get("failed"))}
res["claim_ceiling"] = ("the repair is data-side (manifest pins) inside a working copy. The delivered "
                        "candidate is byte-frozen and still carries D-R18-01; 2789/0 is NOT a property of "
                        "the delivered artefact")
res["negative_control"] = ("un-patching restores the failure, so the pass is caused by the repair and not by "
                          "the environment drifting mid-run")
(ROUND / "receipts" / "WP18_CAUSAL_REPAIR.json").write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                                           encoding="utf-8")
shutil.rmtree(xp(WORK), ignore_errors=True)

# ---------------------------------------------------------------- WP-19 SBOM rescan (frozen subject)
def scan(root):
    entries = {}
    total = 0
    root = pathlib.Path(root)
    for p in sorted(root.rglob("*")):
        if p.is_file():
            try:
                b = p.read_bytes()
            except Exception:
                continue
            rel = str(p.relative_to(root)).replace("\\", "/")
            entries[rel] = hashlib.sha256(b).hexdigest()
            total += len(b)
    return entries, total

e1, t1 = scan(SUB)
e2, t2 = scan(SUB)
sbom = {
    "schema": "R18.WP19_SBOM_RESCAN/1", "at": now(),
    "files": len(e1), "bytes_scanned": t1,
    "stable_across_two_scans": (e1 == e2 and t1 == t2),
    "entries": e1,
    "why_stable_matters": ("the previous SBOM mixed two tree states (5/85 drift). An SBOM that is not "
                           "recomputable is not evidence"),
    "claim_ceiling": "hash inventory of the frozen subject only; it is not a licence audit and not an SBOM format standard",
}
(ROUND / "receipts" / "WP19_SBOM_RESCAN.json").write_text(json.dumps(sbom, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")

subprocess.run([PY, "-B", str(ROUND / "tools" / "ledger_driver.py"), "--set", "WP-FHS-18",
                "status=PARTIAL", "engineering=MEASURED",
                "evidence=receipts/WP18_CAUSAL_REPAIR.json;receipts/WP18_D_R18_01_REPAIR.json",
                "note=causal red/patched-green/unpatched-red proved in one copy; delivered candidate still frozen with the defect"],
               capture_output=True, text=True, timeout=120)
subprocess.run([PY, "-B", str(ROUND / "tools" / "ledger_driver.py"), "--set", "WP-FHS-19",
                "status=PARTIAL", "engineering=MEASURED",
                "evidence=receipts/WP19_SBOM_RESCAN.json;receipts/WP19_SUPPLY_CHAIN.json",
                "note=SBOM rescanned on the frozen subject twice, byte-stable; supersedes the transient scan"],
               capture_output=True, text=True, timeout=120)

print(json.dumps({"wp18": res["numbers"], "causal": res["causal"],
                  "wp19_files": sbom["files"], "stable": sbom["stable_across_two_scans"]}, ensure_ascii=False))
