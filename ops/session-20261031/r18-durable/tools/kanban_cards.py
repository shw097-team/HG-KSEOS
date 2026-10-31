"""Create the R18 Kanban board cards: one per WP-FHS node + round-level cards."""
import json
import os
import subprocess
import sys
from pathlib import Path

HERMES_HOME = os.environ["HERMES_HOME"]
CLI = [sys.executable, "-m", "hermes_cli.main", "kanban", "--board", "fhs-msc-skeleton-spine-r18"]
CWD = Path(HERMES_HOME) / "hermes-agent"
SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject")

dag = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "wp_graph.json").read_text(encoding="utf-8"))

TITLES = []
for n in sorted(dag["nodes"], key=lambda x: x["id"]):
    TITLES.append((
        "%s %s" % (n["id"], n["name"]),
        "tier=%s effect=%s phase=%s\noutput: %s\ndeps: %s\nPOS: %s\nNEG: %s\nfirst_fail: %s\n"
        "permission_basis: %s" % (
            n["tier"], n["effect_class"], n["phase"], n["output"],
            ",".join(n["depends_on"]) or "-", n["positive"], n["negative"],
            n["first_fail"], n["permission_basis"]),
    ))
TITLES += [
    ("R18 ADMISSION (spine project + 22 frozen requirements + gate refusal proof)",
     "receipts/ADMISSION_R18.json"),
    ("R18 MVS01-10 receipt mapping", "receipts/MVS_R18.json"),
    ("R18 INDEPENDENT ACCEPTANCE (different principal checker lane)", "checker/"),
    ("R18 DELIVERY (candidate branch + commit + push + PR per repo)", "no main / no force / no merge"),
    ("R18 HANDOFF (STATUS/HANDOFF + RESUME_HERE + machine state)", "handoff/"),
]

out = []
for title, body in TITLES:
    r = subprocess.run(CLI + ["create", title, "--body", body], cwd=str(CWD),
                       capture_output=True, text=True)
    out.append({"title": title, "rc": r.returncode,
                "stdout": (r.stdout or "").strip()[-200:], "stderr": (r.stderr or "").strip()[-200:]})
    print(title[:70], "rc=%d" % r.returncode, (r.stdout or "").strip()[:80])

Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\receipts\KANBAN_CREATE.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("cards attempted:", len(out), "failed:", sum(1 for x in out if x["rc"] != 0))
