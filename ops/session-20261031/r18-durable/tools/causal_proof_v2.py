"""Causal repair proof, v2 — targeting a real working copy (the v1 run hit the wrong tree).

red -> repair the COPY -> green -> restore the copy's manifest -> red again.
causal is true only if the failure returns after restoring the manifest.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import time

P = "\\\\?\\"
R = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
COPY = R / "causal_tmp"


def x(p):
    s = str(p).replace("/", "\\")
    return s if s.startswith(P) else P + s


def val(root):
    pr = subprocess.run([sys.executable, "-B", str(root / "tools" / "validate.py")], cwd=str(root),
                        capture_output=True, text=True, timeout=1800)
    d = {}
    for line in (pr.stdout or "").splitlines():
        if line.strip().startswith("{"):
            try:
                j = json.loads(line)
                if "passed" in j:
                    d = j
            except Exception:
                pass
    return {"rc": pr.returncode, "passed": d.get("passed"), "failed": d.get("failed")}


shutil.rmtree(x(COPY), ignore_errors=True)
shutil.copytree(x(R / "subject"), x(COPY))
red = val(COPY)
rep = subprocess.run([sys.executable, "-B", str(R / "tools" / "repair_stale_pins.py"), "--target", str(COPY)],
                     capture_output=True, text=True, timeout=900)
green = val(COPY)
shutil.copyfile(x(R / "subject" / "03_TESTS_AND_READBACK" / "source_manifest.json"),
                x(COPY / "03_TESTS_AND_READBACK" / "source_manifest.json"))
red2 = val(COPY)

out = {
    "schema": "R18.WP18_CAUSAL_REPAIR/2",
    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "target": str(COPY),
    "red_before": red, "repair_rc": rep.returncode, "repair_tail": (rep.stdout or "").strip()[-300:],
    "green_after": green, "red_after_unpatch": red2,
    "causal": red.get("failed") == 1 and green.get("failed") == 0 and red2.get("failed") == 1,
    "claim_ceiling": ("data-side repair inside a working copy; the delivered candidate stays byte-frozen. "
                      "SOURCE-BYTES-UNCHANGED depends on external source paths relocated after the freeze, so "
                      "any PASS count is only meaningful together with that path state"),
}
(R / "receipts" / "WP18_CAUSAL_REPAIR.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")
shutil.rmtree(x(COPY), ignore_errors=True)
print(json.dumps({"red": red, "green": green, "red2": red2, "causal": out["causal"]}, ensure_ascii=False))
