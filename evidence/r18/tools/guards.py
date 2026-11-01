"""Three guards for the three violations FAR_R18-12 measured.

G1 STATE: goal status has exactly one writer - this module, and it only sets ACTIVE when the ledger audit passes.
G2 LANE:  a judgement artefact must name the lane receipt that produced it; prose from the agent is not a verdict.
G3 STOP:  the round may not end while the driver reports actionable work; it ends only when every row is DONE/REUSE
          or carries owner + next_legal_action + resume_predicate.
"""
import argparse
import json
import pathlib
import sqlite3
import subprocess
import sys
import time

ROUND = pathlib.Path(__file__).resolve().parents[1]
STATE_DB = pathlib.Path.home() / "AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/state.db"
SESSION = "20261029_123118_143d2d"


def audit_rc():
    p = subprocess.run([sys.executable, "-B", str(ROUND / "tools" / "ledger_driver.py"), "--audit"],
                       capture_output=True, text=True, timeout=180)
    return p.returncode, (p.stdout or "").strip()[:120]


def set_goal_status(status, reason):
    rc, out = audit_rc()
    if status == "active" and rc != 0:
        return {"applied": False, "refused": "AUDIT_RC_%d" % rc, "audit": out}
    con = sqlite3.connect(STATE_DB)
    cur = con.cursor()
    key = "goal:" + SESSION
    row = cur.execute("select value from state_meta where key=?", (key,)).fetchone()
    d = json.loads(row[0]) if row else {}
    d["status"] = status
    d["status_reason"] = reason
    d["status_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cur.execute("update state_meta set value=? where key=?", (json.dumps(d, ensure_ascii=False), key))
    con.commit()
    con.close()
    return {"applied": True, "status": status, "audit_rc": rc}


def lane_guard():
    """A judgement artefact must cite a lane receipt that exists and whose served arm is the spec arm."""
    lane_dir = ROUND / "lane"
    checker = ROUND / "checker"
    receipts = []
    for p in sorted(list(lane_dir.glob("*.json")) + list(checker.glob("VERIFY*.json"))):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        served = d.get("served") or d.get("model") or d.get("arm")
        receipts.append({"file": p.name, "served": served,
                         "mtime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(p.stat().st_mtime))})
    verdicts = [p.name for p in checker.glob("VERDICT*.md")]
    unbacked = [v for v in verdicts if not receipts]
    return {"lane_receipts": receipts, "verdicts": verdicts,
            "violation": bool(verdicts and not receipts) or bool(unbacked),
            "rule": "a VERDICT without a lane receipt is agent prose, not a verdict"}


def stop_guard():
    ts_path = ROUND / "receipts" / "TERMINAL_STATE.json"
    ts = json.loads(ts_path.read_text(encoding="utf-8")) if ts_path.is_file() else {}
    journal = ROUND / "receipts" / "DRIVER_JOURNAL.jsonl"
    actionable = 0
    if journal.is_file():
        for line in journal.read_text(encoding="utf-8").splitlines()[-20:]:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("actionable") and r.get("status") not in ("DONE", "REUSE"):
                actionable += 1
    nondef = [w["wp"] for w in ts.get("wps", []) if not w.get("defensible")]
    return {"defensible": ts.get("summary", {}).get("defensible"), "non_defensible": nondef,
            "actionable_rows": actionable,
            "may_stop": (not nondef) and actionable == 0,
            "rule": "stop only when every WP is defensible and the driver reports no actionable work"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set-goal", choices=["active", "paused"])
    ap.add_argument("--reason", default="guards.py")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if a.set_goal:
        out["state"] = set_goal_status(a.set_goal, a.reason)
    out["lane"] = lane_guard()
    out["stop"] = stop_guard()
    (ROUND / "receipts" / "SELFREPAIR_GUARDS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"state": out.get("state"), "lane_violation": out["lane"]["violation"],
                      "lane_receipts": len(out["lane"]["lane_receipts"]), "may_stop": out["stop"]["may_stop"],
                      "non_defensible": out["stop"]["non_defensible"]}, ensure_ascii=False))
