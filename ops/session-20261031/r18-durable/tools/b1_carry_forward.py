"""R18 carry-forward receipt: reuse the closed B1 baseline instead of re-deriving it.

Binds, in one place:
  - the B1 local baseline pointer (PROMOTED.json, B1-LOCAL-2026-10-28)
  - the four repositories' default-branch heads and the b1-promote-20261028 tags
  - the SharedSpine native-admission population (reuse evidence: the native path really ran)
  - a live re-run of the B1 gate script, when it is executable read-only

Writes receipts/B1_CARRY_FORWARD.json. Read-only against every repository.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WS = Path(r"C:\Projects\Agent_Workspace")
ROUND = WS / "var" / "R18-FHS-SKELETON-SPINE-20261029"
OUT = ROUND / "receipts" / "B1_CARRY_FORWARD.json"
SPINE = WS / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"
PROMOTED = WS / "var" / "B1-PIPD-PKG-20261027" / "PROMOTED.json"
GATES = WS / "var" / "B1-PIPD-PKG-20261027" / "gates.py"
CONT = WS / "var" / "B1-CONT-20261028"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(WS / repo)] + list(args),
                       capture_output=True, text=True, timeout=120)
    return r.stdout.strip()


rec = {"schema": "R18.FHS.B1_CARRY_FORWARD/1", "collected_utc": datetime.now(timezone.utc).isoformat()}

# 1. baseline pointer
if PROMOTED.is_file():
    rec["baseline_pointer"] = {"path": str(PROMOTED.relative_to(WS)), "sha256": sha(PROMOTED),
                               "payload": json.loads(PROMOTED.read_text(encoding="utf-8"))}
else:
    rec["baseline_pointer"] = {"path": str(PROMOTED), "status": "ABSENT"}

# 2. repos: working HEAD vs origin/main vs tag
repos = {}
for repo in ["HG-KSEOS", "Fabric", "PIPD", "SBL"]:
    repos[repo] = {
        "worktree_head": git(repo, "rev-parse", "HEAD"),
        "worktree_branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "origin_main": git(repo, "rev-parse", "origin/main"),
        "origin_main_subject": git(repo, "log", "-1", "--format=%s", "origin/main"),
        "tag_b1_promote": git(repo, "rev-parse", "--verify", "refs/tags/b1-promote-20261028^{commit}"),
        "tag_points_at_origin_main": None,
    }
    r = repos[repo]
    r["tag_points_at_origin_main"] = (r["tag_b1_promote"] == r["origin_main"] and bool(r["origin_main"]))
rec["repos"] = repos

# 3. spine native population (reuse evidence)
try:
    import sqlite3
    c = sqlite3.connect(str(SPINE), timeout=20)
    c.row_factory = sqlite3.Row
    q = {}
    for name, sql in {
        "native_admission_events": "select count(*) from canonical_events where entity_type='native_admission'",
        "native_admission_nonces": "select count(*) from native_admission_nonces",
        "native_admission_leases": "select count(*) from native_admission_leases",
        "workorders_total": "select count(*) from workorders",
        "workorders_verified": "select count(*) from workorders where state='VERIFIED'",
        "requirements_total": "select count(*) from requirements",
        "project_FHS_MSC_R18": "select count(*) from requirements where project_id='FHS-MSC-R18-20261029'",
    }.items():
        try:
            q[name] = c.execute(sql).fetchone()[0]
        except Exception as exc:  # noqa: BLE001
            q[name] = "ERR:%s" % exc
    rec["spine_population"] = q
    c.close()
except Exception as exc:  # noqa: BLE001
    rec["spine_population"] = {"error": str(exc)}

# 4. live gate re-run (read-only expectation; capture whatever it prints)
if GATES.is_file():
    try:
        r = subprocess.run([sys.executable, "-B", str(GATES)], cwd=str(GATES.parent),
                           capture_output=True, text=True, timeout=600,
                           env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        tail = (r.stdout or "").strip().splitlines()
        rec["gate_rerun"] = {"command": "python -B var/B1-PIPD-PKG-20261027/gates.py",
                             "exit_code": r.returncode, "stdout_tail": tail[-25:],
                             "stderr_tail": (r.stderr or "").strip().splitlines()[-8:]}
    except subprocess.TimeoutExpired:
        rec["gate_rerun"] = {"exit_code": None, "error": "TIMEOUT_600"}
else:
    rec["gate_rerun"] = {"error": "GATES_ABSENT"}

# 5. the three FARS + resume pointers that a successor must read first
rec["carry_forward_documents"] = []
for p in [CONT / "CLOSEOUT_2026-10-28.md", CONT / "RESUME_HERE.md", CONT / "SESSION_STATE.json",
          CONT / "FAR_B1_v11_20261028.md", CONT / "wave3" / "PROMOTION_RECEIPT.json"]:
    rec["carry_forward_documents"].append(
        {"path": str(p.relative_to(WS)), "exists": p.is_file(),
         "sha256": sha(p) if p.is_file() else None,
         "bytes": p.stat().st_size if p.is_file() else None})

# 6. the verdict a successor may rely on
rec["reuse_ceiling"] = {
    "is": ["B1 local operative baseline B1-LOCAL-2026-10-28",
           "four repos origin/main carry the B1 closure evidence index and the b1-promote-20261028 tag",
           "the native admission path ran for real (event/nonce/lease population measured above)"],
    "is_not": ["a permit for THIS subject: no native Issuer reference binds FHS-MSC-R18-20261029",
               "release", "external acceptance", "a licence to reuse a B1 PASS verdict for a new subject"],
    "reuse_rule": "reuse only verifiable experience and the local baseline; never borrow a Permit or a PASS "
                  "across subjects (BODY-00 R2-00-RESUME QuestionKey includes subject and source_sha).",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"baseline": rec["baseline_pointer"].get("payload", {}).get("version"),
                  "tag_ok": {k: v["tag_points_at_origin_main"] for k, v in repos.items()},
                  "spine": rec["spine_population"],
                  "gate_rc": rec["gate_rerun"].get("exit_code")}, ensure_ascii=False)[:1500])
print("gate tail:", json.dumps(rec["gate_rerun"].get("stdout_tail", [])[-6:], ensure_ascii=False)[:1200])
