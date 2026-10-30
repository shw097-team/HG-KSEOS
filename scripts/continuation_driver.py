#!/usr/bin/env python3
"""continuation_driver -- keeps the round moving when no turn is running.

The problem this solves, measured: the owner's standing order is "do not stop to report or ask". The assistant's
only output is a message, and a turn ends when it stops calling tools, so no gate, hook or event is ever invoked
at that moment. Nothing in this deployment resumed work afterwards -- `hermes cron list` was empty, the queue of
remaining work lived in session context, and the last time it was reconstructed from memory the WP order came out
contradicting the delivery's own DAG.

So the loop is moved out of the turn and into a clock. Every invocation is idempotent and does at most one of:

  * a dispatch is already alive                     -> do nothing
  * queue drained                                   -> exit 0
  * next WP has no brief                            -> dispatch the PLAN lane to AUTHOR the brief
  * brief exists, no verdict                        -> dispatch VERIFY_SECURITY with a NONCE-ECHO line
  * verdict exists                                  -> run lane_evidence_gate and report what to record

It never records PASS and never writes a verdict. Acceptance stays with the officer and the registry; this only
hands work to the next gate. It dispatches solely through scripts/hgk-lane-dispatch.py, so there is no second
scheduler -- HG-KSEOS still admits, routes and records.

Usage:
  continuation_driver.py --once [--dry-run] [--lanes-dir DIR]
Exit 0 = did nothing or dispatching; 3 = driver could not proceed (queue/db unreadable).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

K = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
PY = sys.executable
CODEX = Path(r"C:/Users/user/AppData/Local/OpenAI/Codex/bin/22cfb1d302613eae/codex.exe")
RELAY = "https://chatgpt.com/backend-api/codex"
QUEUE = Path(r"C:/wg/queue")
STATE = QUEUE / "driver_state.json"
LOG = QUEUE / "driver.log"


def log(event: dict) -> None:
    QUEUE.mkdir(parents=True, exist_ok=True)
    event["at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def dispatch_alive() -> bool:
    """A dispatch in flight owns the lane; starting another would contend for the same arm and the same repo.

    `wmic` does not exist on this host (measured: WinError 2), and a check that silently answers "no" every time
    is worse than none -- it would let the driver start a second dispatch on top of a live one. So: PowerShell
    CIM, and if even that fails the answer is "assume alive" (refuse to start), not "assume free".
    """
    query = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*hgk-lane-dispatch.py*' } | Measure-Object | "
             "Select-Object -ExpandProperty Count")
    try:
        done = subprocess.run(["powershell", "-NoProfile", "-Command", query],
                              capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return True
    text = done.stdout.decode("utf-8", errors="replace") if isinstance(done.stdout, bytes) else done.stdout
    return text.strip() not in ("0", "")


def next_item() -> dict:
    done = subprocess.run([PY, str(K / "scripts" / "work_queue.py"), "next"],
                          capture_output=True, text=True, timeout=120)
    if done.returncode != 0 or not done.stdout.strip():
        raise RuntimeError(f"work_queue next failed rc={done.returncode}: {done.stderr[-300:]}")
    return json.loads(done.stdout.strip().splitlines()[-1])


def launch(lane: str, prompt: str, nonce: str, cwd: Path, json_out: Path, timeout: int = 900) -> int:
    cwd.mkdir(parents=True, exist_ok=True)
    argv = [
        PY, str(K / "scripts" / "hgk-lane-dispatch.py"),
        "--lane", lane,
        "--prompt", prompt,
        "--nonce", nonce,
        "--codex-executable", str(CODEX),
        "--codex-home", r"C:/Users/user/.codex",
        "--allow-human-home-transport",
        "--relay-base", RELAY,
        "--identity-source", "codex-rollout",
        "--cwd", str(cwd),
        "--timeout", str(timeout),
        "--sandbox", "workspace-write",
        "--allow-sandbox-escalation",
        "--guard-subject", str(K / "scripts"),
        "--require-durable-gates",
        "--durable-gates-subject", str(K / "config" / "recurrence-ledger.json"),
        "--json-out", str(json_out),
    ]
    flags = 0
    if os.name == "nt":
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    log({"action": "spawn", "lane": lane, "nonce": nonce, "json_out": str(json_out), "cwd": str(cwd)})
    # A detached launch with its output thrown away is unobservable: the first attempt died instantly and left
    # no trace at all. Every dispatch therefore owns a log next to its receipt.
    log_path = cwd / f"{json_out.stem}.log"
    with log_path.open("wb") as fh:
        proc = subprocess.Popen(argv, cwd=str(K), stdout=fh, stderr=subprocess.STDOUT,
                                creationflags=flags, close_fds=True)
    log({"action": "spawned", "pid": proc.pid, "log": str(log_path)})
    return proc.pid


def plan_prompt(wp: str, title: str, queue_dir: Path, nonce: str) -> str:
    return (
        f"You are the PLAN lane for {wp} ({title}) of the delivery "
        "FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1. "
        "Read the work-package section for this WP in "
        "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/FHS-MSC/"
        "FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1/01_FHS-MSC_PIPD-LS-PKG_BODY/"
        "11_WORKPACKAGES_AND_DAG.md, plus the current registry rows and the evidence already on disk. "
        f"Write an execution+acceptance brief to {queue_dir.as_posix()}/brief.md . "
        "The brief must state what must be BUILT (not merely measured), the exact artefacts the officer will "
        "hash, the negative fixture, and what would falsify a PASS. "
        f"Your FIRST line must be NONCE-ECHO: {nonce}"
    )


def verify_prompt(wp: str, queue_dir: Path, nonce: str) -> str:
    return (
        f"Read {queue_dir.as_posix()}/brief.md and execute it as the Independent Acceptance Officer for {wp}. "
        f"Writes confined to {queue_dir.as_posix()}. "
        f"Your FIRST line must be NONCE-ECHO: {nonce}"
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run one step (the cron body)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv or sys.argv[1:])

    try:
        item = next_item()
    except Exception as exc:  # noqa: BLE001 - a driver that cannot read the queue must say so, not hang
        log({"action": "error", "detail": str(exc)})
        print(json.dumps({"verdict": "DRIVER_BLOCKED", "detail": str(exc)}))
        return 3

    if item.get("wp") is None:
        log({"action": "queue_drained", "remaining_fail": item.get("remaining_fail")})
        print(json.dumps({"verdict": "QUEUE_DRAINED", "remaining_fail": item.get("remaining_fail")}))
        return 0

    wp, phase = item["wp"], item["phase"]
    queue_dir = Path(item["queue_dir"])
    if dispatch_alive():
        print(json.dumps({"verdict": "DISPATCH_IN_FLIGHT", "wp": wp}))
        return 0

    stamp = time.strftime("%Y%m%d%H%M%S")
    nonce = f"NONCE-{wp}-AUTO-{stamp}"
    if phase == "NO_BRIEF":
        prompt, lane = plan_prompt(wp, item["title"], queue_dir, nonce), "PLAN"
    elif phase == "BRIEF_READY":
        prompt, lane = verify_prompt(wp, queue_dir, nonce), "VERIFY_SECURITY"
    else:  # AWAITING_RECORD -- the gate decides, the driver only reports
        gate = subprocess.run(
            [PY, str(K / "scripts" / "lane_evidence_gate.py"), str(queue_dir / "verdict.json"),
             "--lane", "VERIFY_SECURITY", "--json"], capture_output=True, text=True, timeout=120)
        print(json.dumps({"verdict": "AWAITING_RECORD", "wp": wp, "gate": gate.stdout.strip()[:400]}))
        log({"action": "awaiting_record", "wp": wp, "gate": gate.stdout.strip()[:400]})
        return 0

    json_out = queue_dir / f"{wp}-{lane.lower()}-{stamp}.json"
    if args.dry_run:
        print(json.dumps({"verdict": "DRY_RUN", "wp": wp, "lane": lane, "phase": phase,
                          "nonce": nonce, "json_out": str(json_out)}, ensure_ascii=False))
        return 0
    pid = launch(lane, prompt, nonce, queue_dir, json_out)
    print(json.dumps({"verdict": "DISPATCHED", "wp": wp, "lane": lane, "phase": phase, "pid": pid,
                      "json_out": str(json_out), "nonce": nonce}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
