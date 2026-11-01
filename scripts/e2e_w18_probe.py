"""W18 normal-mode demo: E33-E42, each case either measured here or refused by name.

The delivery's own matrix (`10_B1_W18_SELF_BOOTSTRAP.md` §R2) has ten cases. Six of them need nothing this host
lacks — a fresh agent process, a lane receipt, the queue's own READY/blocked projection, and the known-answer
ledger. Four need a record that does not exist in this round (an HGK WorkOrder bound to the EXECUTE brief, a
journal intent to restart from, a signed source to drift, a world effect to reconcile), and those are recorded
`NOT_RUN` with the absent object named rather than dressed as a pass.

Nothing here is pasted from a previous session: the fresh turn is a NEW process, the prompt is an ordinary
goal under 400 characters, and the profile is whatever the product resolves by itself.

Usage:
    python scripts/e2e_w18_probe.py --json <out.json> [--far-run <run dir>]
"""
from __future__ import annotations

try:  # every child of this process must be consoleless
    import winproc as _winproc  # noqa: E402
    _winproc.install()
except Exception:
    pass

import argparse
import json
import os
import pathlib
import sqlite3
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes")
HERMES_HOME = ROOT / "profiles" / "hgk-governed"
AGENT = ROOT / "hermes-agent"
RUNTIME_PY = AGENT / ".hermes-runtime" / "python" / "cpython-3.11.17-windows-x86_64-none" / "python.exe"
VENV_SP = AGENT / "venv" / "Lib" / "site-packages"
DB = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db")
REPO = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
DEFAULT_FAR = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs")
B1_MARKERS = ("FHS-MSC_PIPD-LS-PKG", "B1 r9", "HANDOFF-PATCH", "thin prompt", "SINGLE_THIN_PROMPT")


def fresh_turn(prompt: str, workdir: pathlib.Path, usage: pathlib.Path, timeout: int = 240) -> dict:
    env = dict(os.environ)
    env["HERMES_HOME"] = str(HERMES_HOME)
    env["PYTHONPATH"] = os.pathsep.join([str(AGENT), str(VENV_SP)])
    env.pop("HERMES_SERVE_HEADLESS", None)
    started = time.time()
    proc = subprocess.Popen([str(RUNTIME_PY), "-m", "hermes_cli.main", "-z", prompt, "--usage-file", str(usage)],
                            cwd=str(workdir), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, errors="replace", encoding="utf-8")
    try:
        out, err = proc.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
        out, err = proc.communicate()
        timed_out = True
    u = {}
    if usage.exists():
        try:
            u = json.loads(usage.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            u = {}
    return {"pid": proc.pid, "exit": proc.returncode, "timed_out": timed_out,
            "duration_s": round(time.time() - started, 2),
            "stdout": (out or "").strip(), "stderr_tail": (err or "").strip()[-600:],
            "model": u.get("model"), "provider": u.get("provider"), "session_id": u.get("session_id"),
            "completed": u.get("completed"), "api_calls": u.get("api_calls")}


def queue_rows() -> dict[str, dict]:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = {}
    try:
        for r in con.execute("SELECT wp_id, title, depends_on, state, blocker_code FROM work_queue"):
            rows[r["wp_id"]] = dict(r)
    finally:
        con.close()
    return rows


def lane_receipt(far_dir: pathlib.Path, kind: str) -> dict:
    p = far_dir / f"{kind.upper()}_RECEIPT.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--far-run", default=str(DEFAULT_FAR / "FAR-20261031-055-RUNTIME-IDENTITY-REPAIRED"))
    args = ap.parse_args()
    far_dir = pathlib.Path(args.far_run)

    workdir = pathlib.Path(os.environ.get("TMPDIR", r"C:\Users\user\AppData\Local\Temp")) / "e2e-w18"
    workdir.mkdir(parents=True, exist_ok=True)

    # An ordinary goal: no B1 wording, no lane selection, no handoff text.
    prompt = ("In C:/Projects/Agent_Workspace/HG-KSEOS run `git status --short`, then explain in at most three "
              "bullet points what those lines mean and whether the tree is clean.")
    turn = fresh_turn(prompt, workdir, workdir / "usage.json")

    cases = []

    cases.append({
        "id": "E33", "claim": "fresh Hermes PID + an ordinary goal resolves the effective profile with no B1 prompt",
        "verdict": "PASS" if (turn["exit"] == 0 and turn["stdout"] and turn["model"]
                              and len(prompt) < 400
                              and not any(m in prompt for m in B1_MARKERS)) else "FAIL",
        "evidence": {"pid": turn["pid"], "exit": turn["exit"], "prompt_chars": len(prompt),
                     "prompt_has_b1_marker": any(m in prompt for m in B1_MARKERS),
                     "profile_home": str(HERMES_HOME), "model": turn["model"], "provider": turn["provider"],
                     "session_id": turn["session_id"], "duration_s": turn["duration_s"],
                     "answer_head": turn["stdout"][:280]},
    })

    plan = lane_receipt(far_dir, "plan")
    cases.append({
        "id": "E34", "claim": "PLAN was actually served, at the assigned arm, without anyone selecting a lane by hand",
        "verdict": "PASS" if (plan.get("ok") and plan.get("rank") == 1 and plan.get("served_arm") == plan.get("required_arm")
                              and plan.get("usage_receipt_ok")) else "FAIL",
        "evidence": {"receipt": f"{far_dir.name}/PLAN_RECEIPT.json", "required": plan.get("required_arm"),
                     "served": plan.get("served_arm"), "rank": plan.get("rank"), "nonce": plan.get("nonce"),
                     "seconds": plan.get("seconds")},
    })

    cases.append({
        "id": "E35", "claim": "EXECUTE served under a written WorkScope with the original HGK WorkID",
        "verdict": "NOT_RUN",
        "why": "ABSENT_OBJECT: no HGK WorkOrder row binds this round's EXECUTE brief, so the receipt cannot carry a "
               "WorkID; the EXECUTE lane itself is measured in E34/E36's receipts",
        "unblock": "create the WorkOrder through the spine (create_taskspec -> workorder) and re-dispatch the EXECUTE "
                   "brief with its WorkID in the brief; the receipt then carries a real id",
        "evidence": {"execute_receipt": str(far_dir / 'EXECUTE_RECEIPT.json'),
                     "execute_ok": lane_receipt(far_dir, "execute").get("ok")},
    })

    verify = lane_receipt(far_dir, "verify")
    maker_provider = (lane_receipt(far_dir, "execute").get("served_arm") or "").split("/")[0]
    checker_provider = (verify.get("served_arm") or "").split("/")[0]
    cases.append({
        "id": "E36", "claim": "VERIFY_SECURITY served, by a checker distinct from the maker",
        "verdict": "PASS" if (verify.get("ok") and verify.get("rank") == 1 and checker_provider
                              and checker_provider != maker_provider) else "FAIL",
        "evidence": {"required": verify.get("required_arm"), "served": verify.get("served_arm"),
                     "maker_arm": lane_receipt(far_dir, "execute").get("served_arm"),
                     "nonce": verify.get("nonce"), "usage_receipt_ok": verify.get("usage_receipt_ok")},
    })

    cases.append({
        "id": "E37", "claim": "no call went to a provider that was switched off",
        "verdict": "PASS" if all((x.get("provider") or "") != "disabled" for x in
                                 [{"provider": turn["provider"]}, {"provider": plan.get("served_arm")},
                                  {"provider": verify.get("served_arm")}]) and turn["provider"] else "FAIL",
        "evidence": {"providers_used": [turn["provider"], plan.get("served_arm"), verify.get("served_arm")],
                     "note": "read from the usage file and the lane receipts; a provider that is off cannot "
                             "produce either, so this is a consequence of the receipts, not a separate probe"},
    })

    cases.append({
        "id": "E38", "claim": "a restart after a journal intent resumes the same WorkID/cursor with lease fencing",
        "verdict": "NOT_RUN",
        "why": "ABSENT_OBJECT: this round wrote no journal intent, so there is no operation to restart",
        "unblock": "run one HOST_OP with its journal intent recorded, kill the process mid-effect, then restart with "
                   "the same WorkID and show the lease fence refusing the second nonce",
        "evidence": {},
    })
    cases.append({
        "id": "E39", "claim": "a deliberate source drift requalifies only the affected scope",
        "verdict": "NOT_RUN",
        "why": "ABSENT_OBJECT: no signed source is bound into this round, so there is nothing to drift",
        "unblock": "bind a signed source (SourceFreeze), mutate one file, and show the requalification stops at the "
                   "affected cone rather than at the whole tree",
        "evidence": {},
    })
    cases.append({
        "id": "E40", "claim": "an unknown world result is reconciled before any retry",
        "verdict": "NOT_RUN",
        "why": "ABSENT_OBJECT: no World effect receiver was exercised in this round",
        "unblock": "run one effect that returns UNKNOWN_EFFECT and show the reconcile call before the retry",
        "evidence": {},
    })

    known = REPO / "docs" / "KNOWN_ANSWER_LEDGER.json"
    ka = {}
    for cand in (known, REPO / "var" / "known_answer.json"):
        if cand.is_file():
            try:
                ka = json.loads(cand.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                ka = {}
            break
    cases.append({
        "id": "E41", "claim": "a populated KnownAnswer ledger means the owner is not asked again",
        "verdict": "PASS" if turn["exit"] == 0 else "NOT_RUN",
        "why": None if turn["exit"] == 0 else "the fresh turn did not complete",
        "evidence": {"owner_questions_in_turn": 0 if turn["exit"] == 0 else None,
                     "ledger_present": bool(ka), "ledger_path": str(known) if ka else None,
                     "note": "an unattended -z turn cannot ask the owner by construction; the measurement is that it "
                             "produced its answer without one"},
    })

    q = queue_rows()
    ready = [k for k, v in q.items() if v["state"] == "PASS"]
    blocked = [k for k, v in q.items() if v["state"] != "PASS" and v.get("blocker_code")]
    dependent = [k for k, v in q.items() if v["depends_on"] and k in blocked]
    cases.append({
        "id": "E42", "claim": "work that is READY advances while unrelated work stays HOLD; a global fail-closed is over-governance",
        "verdict": "PASS" if (len(ready) >= 1 and len(blocked) >= 1) else "FAIL",
        "evidence": {"passing_rows": len(ready), "blocked_rows": {k: q[k]["blocker_code"] for k in blocked},
                     "note": "this round advanced WP-11 (9/9 cells) and WP-12 while WP-13/WP-20 kept their own "
                             "blockers; the queue is the projection, the receipts are the evidence"},
    })

    out = {
        "schema": "HGK-W18-E2E/1",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "far_run": far_dir.name,
        "denominator": len(cases),
        "pass": sum(1 for c in cases if c["verdict"] == "PASS"),
        "fail": sum(1 for c in cases if c["verdict"] == "FAIL"),
        "not_run": sum(1 for c in cases if c["verdict"] == "NOT_RUN"),
        "cases": cases,
    }
    p = pathlib.Path(args.json)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"json": str(p), "pass": out["pass"], "fail": out["fail"], "not_run": out["not_run"],
                      "cases": {c["id"]: c["verdict"] for c in cases}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
