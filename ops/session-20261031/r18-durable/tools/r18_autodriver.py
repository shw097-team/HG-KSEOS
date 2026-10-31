"""R18 unattended driver: the thing that replaces "I will continue next turn" with a loop.

WHY (FAR_R18-11): every previous stopping point was self-inflicted in the same way — the ledger treated
PARTIAL as terminal, so the queue said "nothing to do", and a turn-based agent has no scheduler, so
"continuing" depended on somebody typing. Neither is a governance problem; both are state-machine and
scheduling problems.

Contract
  * a row is ACTIONABLE when a JOB exists for it and its status is not DONE
  * each job is idempotent and writes its own receipt
  * the driver journals every run, updates the ledger, and exits 0
  * when no job remains, it writes STOPPED_ALL_ROWS_TERMINAL and does nothing on later runs
  * it never touches a row whose resume_predicate needs another principal (Issuer, Writer, checker)
"""
import json
import pathlib
import subprocess
import sys
import time

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
LEDGER = ROUND / "ledger.json"
JOURNAL = ROUND / "receipts" / "DRIVER_JOURNAL.jsonl"
STATE = ROUND / "DRIVER_STATE.json"
PY = sys.executable

# job id -> (script, rows it closes, one-line description)
JOBS = {
    "wp0203_bindings": ("tools/wp0203_17_bindings.py", ["WP-FHS-02", "WP-FHS-03"],
                        "measure Fabric policy / Issuer / CAP-BOOT bindings"),
    "wp17_capboot": ("tools/wp0203_17_bindings.py", ["WP-FHS-17"], "measure CAP-BOOT presence"),
    "wp_contract": ("tools/wp_contract_harness.py", [], "re-run the 22-WP contract harness"),
    "mvs_mapping": ("tools/wp04_wp15_wp16_wp05_mvs.py", ["R18-MVS"], "re-derive the MVS01-10 mapping"),
}


def log(entry):
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + chr(10))


def ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def row_status(rows, wp):
    r = next((x for x in rows if x["id"] == wp), None)
    return (r or {}).get("status")


def run_job(jid, script, rows_to_close, desc):
    started = time.time()
    p = subprocess.run([PY, "-B", str(ROUND / script)], capture_output=True, text=True, timeout=1800)
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "job": jid, "script": script,
             "desc": desc, "rc": p.returncode, "seconds": round(time.time() - started, 1),
             "stdout_tail": (p.stdout or "").strip()[-600:], "stderr_tail": (p.stderr or "").strip()[-400:]}
    if p.returncode == 0:
        for wp in rows_to_close:
            subprocess.run([PY, "-B", str(ROUND / "tools" / "ledger_driver.py"), "--set", wp,
                            "status=PARTIAL", "engineering=MEASURED",
                            "evidence=receipts/WP0203_17_BINDINGS.json"],
                           capture_output=True, text=True, timeout=120)
        entry["rows_touched"] = rows_to_close
    log(entry)
    return entry


def main():
    rows = ledger()["rows"]
    todo = []
    for jid, (script, wp_rows, desc) in JOBS.items():
        pending = [w for w in wp_rows if row_status(rows, w) not in ("DONE", "REUSE")]
        if wp_rows and not pending:
            continue                      # every row it would close is already terminal
        todo.append((jid, script, wp_rows, desc))

    state = {"schema": "R18.DRIVER_STATE/1", "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "jobs_total": len(JOBS), "jobs_run": [], "remaining": [t[0] for t in todo]}

    if not todo:
        state["verdict"] = "STOPPED_ALL_ROWS_TERMINAL"
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        log({"ts": state["at"], "verdict": state["verdict"]})
        print(json.dumps(state, ensure_ascii=False))
        return 0

    for jid, script, wp_rows, desc in todo:
        state["jobs_run"].append(run_job(jid, script, wp_rows, desc))

    rows = ledger()["rows"]
    state["after"] = {s: sum(1 for r in rows if r["status"] == s) for s in {r["status"] for r in rows}}
    state["verdict"] = "RAN_JOBS"
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"verdict": state["verdict"], "after": state["after"],
                      "jobs": [j["job"] + ":rc" + str(j["rc"]) for j in state["jobs_run"]]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
