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

try:  # every child of this process must be consoleless (see scripts/winproc.py)
    import winproc as _winproc  # noqa: E402
    _winproc.install()
except Exception:  # a missing helper must not stop a lane
    pass

import hashlib




import argparse
import json
from subprocess import Popen
import sqlite3
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
MAX_PHASE_ATTEMPTS = 3
# A FAIL is a specification, but not an infinite one: after this many EXECUTE rounds the unit needs a ruling.
MAX_EXECUTE_ROUNDS = 6
# Measured 2026-10-31: an EXECUTE attempt was cut at 900.09s while still writing files, so its receipt could not
# be cited. A writer that needs to finish is not the same budget as a reader.
LANE_TIMEOUTS = {"PLAN": 900, "VERIFY_SECURITY": 900, "EXECUTE": 1800}   # two failures are a flake; the third is a defect and stops the loop
STATE = QUEUE / "driver_state.json"
LOG = QUEUE / "driver.log"


CREATE_NO_WINDOW = 0x08000000


def sp_run(argv, **kw):
    """subprocess.run that cannot put a window on the owner's desktop.

    Explicit flags rather than the winproc monkeypatch: measured 2026-10-31 02:01, a tick still produced eight
    `python.exe` console windows although winproc.install() reported True in the same tree. Whatever the reason
    (an install that silently failed in a detached child), the call site is the one place that can be certain.
    """
    kw["creationflags"] = int(kw.get("creationflags") or 0) | CREATE_NO_WINDOW
    return subprocess.run(argv, **kw)


def sp_popen(argv, **kw):
    kw["creationflags"] = int(kw.get("creationflags") or 0) | CREATE_NO_WINDOW
    return subprocess.Popen(argv, **kw)


def _detach_child(argv: list, log_path: Path, env: dict | None = None) -> dict:
    """Spawn outside the job tree. Every child of this driver must use it, or the turn takes the tree down with it.

    Measured 2026-10-31 07:42: a parallel tick reported three dispatched pids and, eleven seconds later, no lane was
    alive -- the tick had spawned its children with subprocess.Popen, so they died with the cell that started the tick.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import detach as _detach
    return _detach.launch(argv, out=log_path, cwd=str(K))


def log(event: dict) -> None:
    QUEUE.mkdir(parents=True, exist_ok=True)
    event["at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def dispatch_alive(wp: str | None = None) -> bool:
    """A dispatch in flight owns the lane; starting another would contend for the same arm and the same repo.

    `wmic` does not exist on this host (measured: WinError 2), and a check that silently answers "no" every time
    is worse than none -- it would let the driver start a second dispatch on top of a live one. So: PowerShell
    CIM, and if even that fails the answer is "assume alive" (refuse to start), not "assume free".
    """
    # Quoting note: passing `-Filter \"Name='python.exe'\"` through subprocess mangles the inner quotes, and the
    # resulting PowerShell error text was itself mistaken for output -- the driver then reported
    # DISPATCH_IN_FLIGHT forever while nothing was running. Filtering in Where-Object needs no inner quoting
    # at all, and a parseable integer is required before anything is believed.
    # Per-unit, not global: two independent units may be in flight at once (that is the point of a parallel
    # supervisor), but never two dispatches of the SAME unit -- those contend for one arm and one repo.
    unit = f"-{wp}-" if wp else ""
    query = ("$p = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and "
             "$_.CommandLine -like '*hgk-lane-dispatch.py*' -and "
             f"$_.CommandLine -like '*{unit}*' }}; ($p | Measure-Object).Count")
    try:
        done = sp_run(["powershell", "-NoProfile", "-Command", query], capture_output=True, timeout=60)
        out = done.stdout.decode("utf-8", errors="replace") if isinstance(done.stdout, bytes) else str(done.stdout)
        digits = "".join(ch for ch in out.strip().splitlines()[-1:] and out.strip().splitlines()[-1] if ch.isdigit())
        if not digits:
            return True          # unreadable answer -> refuse to start a second dispatch
        return int(digits) > 0
    except (OSError, subprocess.SubprocessError):
        return True


def dead_attempts(queue_dir: Path) -> list[dict]:
    """Receipts still saying PRE_ATTEMPT: the process started and never recorded finishing."""
    out = []
    for p in queue_dir.glob("*-*.json"):
        if "attempts" in p.name:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(d, dict) and d.get("phase") == "PRE_ATTEMPT":
            out.append({"receipt": str(p), "nonce": d.get("nonce"), "started_at": d.get("started_at")})
    return out


def next_item(only_wp: str | None = None) -> dict:
    done = sp_run([PY, str(K / "scripts" / "work_queue.py"), "next"] + ([ "--wp", only_wp] if only_wp else []),
                          capture_output=True, text=True, timeout=120)
    if done.returncode != 0 or not done.stdout.strip():
        raise RuntimeError(f"work_queue next failed rc={done.returncode}: {done.stderr[-300:]}")
    return json.loads(done.stdout.strip().splitlines()[-1])


def guard_snapshot(nonce: str) -> tuple[Path, str]:
    """Freeze the guarded subject for the duration of one dispatch.

    Measured six times tonight: a VERIFY/PLAN run is voided with ERR_CHECKER_MUTATED_SUBJECT because the maker
    edited `scripts/` while the review was reading it. `review_lock` blocks commits, not file writes, so a maker
    who is actively developing will void every review he runs. The guarded subject must therefore be a snapshot:
    the review reads a fixed tree, the working tree stays editable, and the snapshot digest is recorded.
    """
    import hashlib, shutil
    src = K / "scripts"
    dst = Path(r"C:/wg/guard-snapshots") / nonce / "scripts"
    if dst.parent.exists():
        shutil.rmtree(dst.parent, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"), dirs_exist_ok=True)
    digest = hashlib.sha256()
    for f in sorted(dst.rglob("*.py")):
        digest.update(f.name.encode())
        digest.update(f.read_bytes())
    log({"action": "guard_snapshot", "nonce": nonce, "path": str(dst), "sha256": digest.hexdigest()})
    return dst, digest.hexdigest()


def launch(lane: str, prompt: str, nonce: str, cwd: Path, json_out: Path, timeout: int = 900) -> int:
    cwd.mkdir(parents=True, exist_ok=True)
    guard_subject, guard_sha = guard_snapshot(nonce)
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
        "--guard-subject", str(guard_subject),
        "--require-durable-gates",
        "--durable-gates-subject", str(K / "config" / "recurrence-ledger.json"),
        "--json-out", str(json_out),
    ]
    flags = 0
    if os.name == "nt":
        # The owner sees one console window per dispatch otherwise, and asked for no windows at all. A detached
        # child with CREATE_NO_WINDOW has no console, so the loop is invisible in the task bar and still logged.
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
    log({"action": "spawn", "lane": lane, "nonce": nonce, "json_out": str(json_out), "cwd": str(cwd)})
    # A detached launch with its output thrown away is unobservable: the first attempt died instantly and left
    # no trace at all. Every dispatch therefore owns a log next to its receipt.
    # Third occurrence of the same shape, 2026-10-30: a PLAN dispatch ran (it wrote a 14,962-byte brief), then
    # vanished leaving neither a receipt nor a traceback. A run that cannot be seen ended is indistinguishable from
    # a run that never started. So the intent is written BEFORE the child exists; if nothing ever overwrites it, the
    # file itself says "attempt started at T, pid N, never completed".
    json_out.write_text(json.dumps({
        "phase": "PRE_ATTEMPT", "lane": lane, "nonce": nonce, "pid": None,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ok": None, "receipt_complete": False,
        "note": "written by continuation_driver before spawn; the dispatcher overwrites this on completion",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log_path = cwd / f"{json_out.stem}.log"
    # Measured 2026-10-31 02:18 -> 07:39: three dispatches wrote their PRE_ATTEMPT and then vanished with the turn,
    # because CREATE_BREAKAWAY_FROM_JOB does not break away from a nested job object. Ask the service host for the
    # process instead: Win32_Process.Create has no parent job to be killed with.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import detach as _detach
        res = _detach.launch(argv, out=log_path, cwd=str(K))
    except Exception as exc:  # noqa: BLE001 - a launcher that cannot launch must not look like a launch
        res = {"ok": False, "pid": 0, "error": f"{type(exc).__name__}: {exc}"}
    if not res.get("ok"):
        log({"action": "spawn_failed", "error": res.get("error")})
        raise RuntimeError(f"DETACH_FAILED: {res.get('error')}")
    log({"action": "spawned", "pid": res["pid"], "log": str(log_path), "method": "Win32_Process.Create"})
    return int(res["pid"])


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


def latest_verdict(queue_dir: Path) -> tuple[Path | None, dict | None]:
    """The operative officer verdict for this unit, if any. Only `verdict.json` counts: a SUPERSEDED or VOIDED copy
    is history, and treating history as current is how a card gets re-judged against an old ruling."""
    # Newest by mtime, not by name: sittings are named after the nonce, and reading the first name in sorted order
    # returned the oldest ruling -- so a unit that had just been judged VOID was routed on a FAIL from an hour before.
    cands = sorted(queue_dir.rglob("verdict.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    for cand in cands:
        try:
            return cand, json.loads(cand.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            continue
    return None, None


def execute_prompt(wp: str, queue_dir: Path, nonce: str, verdict: dict) -> str:
    """One work package, one bounded writer, and the officer's own words as the specification.

    This is the phase that was missing. PLAN wrote a brief and VERIFY judged it, so a FAIL had nowhere to go: the
    loop could produce objections but never the work that answers them, which is why every round needed a new
    assistant turn and looked like "stopping". The officer already states what must exist; EXECUTE reads that and
    nothing else.
    """
    gaps = (verdict.get("must_contain") or verdict.get("decisive_reasons")
            or verdict.get("mandatory_failures") or verdict.get("reason") or [])
    if isinstance(gaps, str):
        gaps = [gaps]
    if verdict.get("maker_return"):
        gaps = list(gaps) + [f"officer's instruction: {verdict['maker_return']}"]
    body = "\n".join(f"  - {g}" for g in list(gaps)[:12]) or "  - (officer stated no itemised gaps; read its verdict)"
    return (
        f"NONCE-ECHO: {nonce}\n\n"
        f"You are the EXECUTE lane (bounded writer) answering the Independent Acceptance Officer's FAIL on {wp}.\n"
        f"Your FIRST line must be exactly: NONCE-ECHO: {nonce}\n\n"
        f"Read the officer's verdict at {verdict.get('_path') or queue_dir / 'officer' / 'verdict.json'} "
        f"and the brief at {queue_dir}/brief.md.\n"
        f"The officer named these gaps:\n{body}\n\n"
        f"Write the artefacts that close exactly those gaps, inside this work package only. Rules:\n"
        f"  1. One work package. Do not touch other WP directories.\n"
        f"  2. Every artefact you claim must be producible by a command that a checker can re-run; put the command in\n"
        f"     the file's header. No hand-written results.\n"
        f"  3. Do not change the acceptance standard, the oracle, or any prior verdict. If a gap cannot be closed,\n"
        f"     say so plainly in EVIDENCE_GAP.md with what is missing -- that is a finding, not a failure to hide.\n"
        f"  4. Write only under {queue_dir}. Report the files you created at the end, one per line.\n"
        f"  5. Files from an earlier attempt may already exist in this directory; read them and finish them rather than\n"
        f"     starting over. Say in the report what you kept and what you replaced.\n"
        f"  6. Write `EXECUTE_REPORT.md` whose FIRST line is exactly `NONCE-ECHO: {nonce}`, then the files you\n"
        f"     created and the command that reproduces each. The line must be in the file, not only in your reply."
    )


def subject_digest(queue_dir: Path) -> str:
    """A digest of what the unit is *being asked to do*: its brief and its own input artefacts.

    Receipts, verdicts and logs are excluded on purpose -- they change on every dispatch, so including them would
    make every subject look new.
    """
    h = hashlib.sha256()
    cands = [queue_dir / "brief.md"]
    out = queue_dir / "output"
    if out.exists():
        for f in out.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(queue_dir).as_posix()
            if rel.startswith("output/officer/") or "/sittings/" in rel:
                continue          # the officer's own history is not part of the ask
            if f.suffix.lower() not in (".md", ".json", ".py", ".yaml", ".yml", ".txt"):
                continue
            if f.stat().st_size > 4_000_000:
                continue
            cands.append(f)
    for f in sorted(set(cands)):
        if f.exists():
            h.update(f.name.encode("utf-8"))
            h.update(f.read_bytes())
    return h.hexdigest()


def note_subject(queue_dir: Path) -> None:
    """Reset the retry budget when the ask itself changed, and say so in the log.

    A cap exists to stop a loop on the *same* problem. Measured 2026-10-31 07:43: WP-FHS-11, -17 and -20 were all
    parked at their caps while the actual cause of the earlier failures had already been fixed (48 false NoFits
    withdrawn, the 192 raws produced, the officer's VOID answered). Counting rounds across a changed subject turns a
    repaired unit into a permanently blocked one, which reads as a stall and is one.
    """
    st = queue_dir / "BUDGET.json"
    cur = subject_digest(queue_dir)
    old = None
    if st.exists():
        try:
            old = json.loads(st.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            old = None
    if old is None or old.get("subject") != cur:
        rounds = len([p for p in queue_dir.glob("*-execute-*.json")])
        st.write_text(json.dumps({"subject": cur, "rounds_at_reset": rounds,
                                  "reset_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                  "why": "the brief or the unit's own inputs changed since the last budget"},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
        log({"action": "budget_reset", "wp": queue_dir.name, "subject": cur[:16], "rounds_at_reset": rounds})


def execute_rounds(queue_dir: Path) -> int:
    """Rounds spent on the current ask. A budget reset (subject changed) starts the count over, on the record."""
    total = len(list(queue_dir.glob("*-execute-*.json")))
    st = queue_dir / "BUDGET.json"
    if st.exists():
        try:
            base = int(json.loads(st.read_text(encoding="utf-8", errors="replace")).get("rounds_at_reset") or 0)
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            base = 0
        return max(0, total - base)
    return total


def record_officer_verdict(wp: str, queue_dir: Path) -> dict:
    """Transcribe the officer's own verdict into the registry — mechanically, with provenance.

    This is the piece that makes the loop unattended. The driver never *decides* anything: it reads a verdict the
    independent officer already wrote, and writes a registry row that names the officer as `verdict_author` and itself
    as `row_mover`. That separation is the whole reason an unattended loop can be trusted: a PASS here is still the
    officer's word, not the driver's.
    """
    found = None
    for cand in sorted(queue_dir.rglob("verdict*.json")):
        if cand.name != "verdict.json":
            continue       # SUPERSEDED / VOIDED / INCONCLUSIVE copies are history, not the operative verdict
        found = cand
    if found is None:
        return {"recorded": None, "why": "no operative verdict.json"}
    d = json.loads(found.read_text(encoding="utf-8", errors="replace"))
    verdict = str(d.get("verdict") or "").upper()
    if verdict not in ("PASS", "FAIL"):
        return {"recorded": None, "why": f"officer verdict {verdict!r} is not PASS/FAIL"}
    con = sqlite3.connect(str(HGK_DB))
    rows = con.execute("SELECT acceptance_id FROM acceptances WHERE acceptance_id LIKE ?",
                       (f"ACC-{wp}-%",)).fetchall()
    nxt = len(rows) + 1
    aid = f"ACC-{wp}-R{nxt}"
    con.execute(
        "INSERT INTO acceptances (acceptance_id,requirement_id,oracle,threshold,negative_fixture,verdict,"
        "evidence_ref,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (aid, wp, str(d.get("oracle_sha256") or "officer oracle"), "officer verdict",
         "see officer verdict", verdict, str(found), time.strftime("%Y-%m-%dT%H:%M:%S")))
    con.commit()
    con.close()
    log({"action": "recorded", "wp": wp, "acceptance_id": aid, "verdict": verdict,
         "verdict_author": "Independent Acceptance Officer", "row_mover": "continuation_driver",
         "evidence_ref": str(found)})
    return {"recorded": aid, "verdict": verdict, "evidence_ref": str(found)}


def refresh_status() -> None:
    """Keep the projection inside its own validity window: a status nobody refreshed reads as stale, and stale is
    how the owner learns to distrust it. Refreshing here means every tick -- dispatched or not -- renews as_of."""
    try:
        sp_run([sys.executable, str(Path(__file__).with_name("ops_status.py"))],
                       capture_output=True, timeout=120)
    except Exception:
        pass


def parallel_tick(n: int, dry_run: bool) -> int:
    """Fan out one tick into up to N detached single-unit runs.

    Measured 2026-10-31: a long-lived supervisor process kept creating a new class of defect every time it was
    touched -- three copies of itself, a pid file written by two owners, and a unit wedged "in flight" for 28 minutes
    by a receipt from a process that had died. The units are independent; the only thing needed is that several start
    together. So there is no daemon: this tick starts N detached children and exits, and the next tick tops up.
    """
    import sqlite3
    con = sqlite3.connect(str(K / "var" / "shared-spine" / "hg-kseos.db"))
    wps = [r[0] for r in con.execute("select wp_id from work_queue order by wp_id")]
    con.close()

    started = []
    for wp in wps:
        if len(started) >= n:
            break
        if dispatch_alive(wp):
            continue                     # this unit already owns a lane; never two dispatches of one unit
        item = next_item(wp)             # the DAG projection decides whether it is ready, not this loop
        if item.get("wp") != wp:
            continue
        if dry_run:
            started.append({"wp": wp, "phase": item.get("phase"), "dry_run": True})
            continue
        flags = 0x08000000 | 0x01000000   # CREATE_NO_WINDOW | DETACHED | BREAKAWAY_FROM_JOB
        logf = QUEUE / f"{wp}.tick.log"
        _res = _detach_child([PY, str(Path(__file__).resolve()), "--once", "--auto-record", "--wp", wp], logf)
        proc = type("P", (), {"pid": _res.get("pid") or 0})()
        started.append({"wp": wp, "phase": item.get("phase"), "pid": proc.pid})
        log({"action": "parallel_dispatch", "wp": wp, "phase": item.get("phase"), "pid": proc.pid})
        time.sleep(1.0)
    refresh_status()
    print(json.dumps({"verdict": "PARALLEL_TICK", "dispatched": started}, ensure_ascii=False))
    return 0


def chain_next(reason: str) -> None:
    """Start the next tick from the unit that just finished, hidden, instead of from a clock.

    Measured 2026-10-31 01:59:50: the only console window this host produced during the whole loop was the cron job's
    own `python.exe` at the moment the scheduler fired it -- the window exists before any of our code can hide
    anything, and it appears inside a new Windows Terminal window on screen. A clock that has to be launched by
    something outside the loop costs a window every tick. So the tick is chained from inside the loop instead: the
    process that just finished a unit starts the next one, and it was itself created with CREATE_NO_WINDOW.
    """
    depth = int(os.environ.get("HGK_CHAIN_DEPTH", "0"))
    if depth >= 12:
        return
    try:
        probe = sp_run([PY, str(K / "scripts" / "work_queue.py"), "next"], capture_output=True, text=True,
                               timeout=120)
        item = json.loads(probe.stdout.strip().splitlines()[-1]) if probe.returncode == 0 and probe.stdout.strip() else {}
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return
    if not item.get("wp"):
        log({"action": "chain_stop", "reason": "nothing ready", "trigger": reason})
        return
    flags = 0x08000000 | 0x01000000
    env = dict(os.environ, HGK_CHAIN_DEPTH=str(depth + 1))
    _detach_child([PY, str(Path(__file__).resolve()), "--parallel", "3", "--auto-record"],
                  QUEUE / "chain.log", env=env)
    log({"action": "chain_next", "trigger": reason, "depth": depth + 1, "next": item.get("wp")})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run one step (the cron body)")
    ap.add_argument("--wp", default=None, help="work this one unit only")
    ap.add_argument("--parallel", type=int, default=1,
                    help="dispatch up to N independent units in this tick, each detached (no daemon, no pid file)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--auto-record", action="store_true",
                    help="transcribe the officer's PASS/FAIL into the registry (verdict_author stays the officer)")
    args = ap.parse_args(argv or sys.argv[1:])

    if args.parallel > 1 and not args.wp:
        return parallel_tick(args.parallel, args.dry_run)

    try:
        item = next_item(args.wp) if args.wp else next_item()
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
    note_subject(queue_dir)
    if dispatch_alive(wp):
        refresh_status()
        print(json.dumps({"verdict": "DISPATCH_IN_FLIGHT", "wp": wp}))
        return 0

    stamp = time.strftime("%Y%m%d%H%M%S")
    nonce = f"NONCE-{wp}-AUTO-{stamp}"

    # The phase the queue reports is about artefacts (brief / verdict present). What the loop needs is one step
    # further: a FAIL is not the end of a unit, it is the specification for the next EXECUTE dispatch.
    vpath, verdict = latest_verdict(queue_dir)
    vword = str(verdict.get("verdict", "")).upper() if verdict else ""
    if vword == "VOID":
        # A void sitting is not a verdict on the work: the officer could not judge the candidate at all. It must still
        # move the unit, or the loop parks on a state no one records. Two voids and the unit stops with a named reason.
        voids = len(list(queue_dir.rglob("verdict.json"))) + len(list(queue_dir.rglob("verdict.VOID*.json")))
        if voids >= 3 or execute_rounds(queue_dir) >= MAX_EXECUTE_ROUNDS:
            log({"action": "halted_void", "wp": wp, "void_sittings": voids})
            refresh_status()
            print(json.dumps({"verdict": "HALTED_SITTING_VOID", "wp": wp, "void_sittings": voids,
                              "officer_named": verdict.get("mandatory_failures"),
                              "maker_return": verdict.get("maker_return"),
                              "detail": "the officer could not judge this candidate and the allowed rounds are spent; "
                                        "another dispatch would be a loop, not work"}, ensure_ascii=False))
            return 0
        phase = "EXECUTE_READY"
    if phase == "AWAITING_RECORD" and vpath is not None and vword in ("FAIL", "VOID"):
        ex = execute_rounds(queue_dir)
        # An EXECUTE receipt only answers a verdict if it is CITABLE. Measured: attempt 1 wrote real files and then
        # timed out at 900.09s with nonce_present=false; counting that mtime as an answer would send VERIFY to judge
        # work nothing can cite, which is how a timed-out write becomes an unearned FAIL.
        def citable(path):
            if path.stat().st_mtime <= vpath.stat().st_mtime:
                return False
            try:
                d = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            except json.JSONDecodeError:
                return False
            if d.get("receipt_complete") is False and not d.get("attempts"):
                return False
            for a in d.get("attempts") or []:
                if a.get("nonce_present") and str(a.get("exit")) in ("0", "OK", "SUCCESS"):
                    return True
            return False

        newer_execute = any(citable(p) for p in queue_dir.glob("*-execute-*.json"))
        if newer_execute:
            phase = "REVERIFY"          # EXECUTE already answered this verdict: let VERIFY judge the answer
        elif ex >= MAX_EXECUTE_ROUNDS:
            log({"action": "halted_execute", "wp": wp, "rounds": ex})
            refresh_status()
            print(json.dumps({"verdict": "HALTED_EXECUTE", "wp": wp, "rounds": ex,
                              "detail": "the officer has failed this unit after the allowed number of EXECUTE rounds; "
                                        "another round would be a loop, not work"}, ensure_ascii=False))
            return 0
        else:
            phase = "EXECUTE_READY"

    if phase == "NO_BRIEF":
        prompt, lane = plan_prompt(wp, item["title"], queue_dir, nonce), "PLAN"
    elif phase == "EXECUTE_READY":
        v = dict(verdict or {})
        v["_path"] = str(vpath) if vpath else None
        prompt, lane = execute_prompt(wp, queue_dir, nonce, v), "EXECUTE"
    elif phase in ("BRIEF_READY", "REVERIFY"):
        prompt, lane = verify_prompt(wp, queue_dir, nonce), "VERIFY_SECURITY"
    else:  # AWAITING_RECORD -- the gate decides, the driver only reports
        # The gate judges a DISPATCH RECEIPT, not the officer's verdict: they are different objects, and asking
        # the gate to read a verdict produced RECEIPT_MISSING -- a check that could never pass.
        receipts = sorted(queue_dir.glob("*-*.json"), key=lambda p: p.stat().st_mtime)
        receipts = [r for r in receipts if "attempts" not in r.name]
        target = receipts[-1] if receipts else queue_dir / "verdict.json"
        gate = sp_run(
            [PY, str(K / "scripts" / "lane_evidence_gate.py"), str(target),
             "--lane", "VERIFY_SECURITY", "--json"], capture_output=True, text=True, timeout=120)
        # A gate that says NO_ATTEMPT while there is no verdict means the dispatch never produced a usable receipt,
        # not that the unit is finished. Returning AWAITING_RECORD there parked the queue forever -- measured twice.
        gate_verdict = ""
        try:
            gate_verdict = str(json.loads(gate.stdout).get("verdict") or "")
        except json.JSONDecodeError:
            pass
        if vpath is None and gate_verdict in ("NO_ATTEMPT", "RECEIPT_MISSING", "RECEIPT_NOT_FOUND"):
            log({"action": "no_attempt_retry", "wp": wp, "gate": gate_verdict})
            phase, lane = "BRIEF_READY", "VERIFY_SECURITY"
            prompt = verify_prompt(wp, queue_dir, nonce)
        else:
            rec = record_officer_verdict(wp, queue_dir) if args.auto_record else {"recorded": None}
            refresh_status()
            print(json.dumps({"verdict": "AWAITING_RECORD", "wp": wp, "gate": gate.stdout.strip()[:400],
                              "recorded": rec}, ensure_ascii=False))
            log({"action": "awaiting_record", "wp": wp, "gate": gate.stdout.strip()[:400]})
            return 0

    closed = sp_run([PY, str(K / "scripts" / "closed_paths_gate.py"), "check", str(queue_dir)],
                            capture_output=True, text=True, timeout=60)
    if closed.returncode == 3:
        log({"action": "refused_closed_path", "wp": wp, "detail": closed.stdout.strip()[:300]})
        print(closed.stdout.strip())
        return 3

    died = dead_attempts(queue_dir)
    if died:
        log({"action": "phase_died", "wp": wp, "count": len(died), "attempts": died[-3:]})
    # Count attempts of THIS phase, not receipts of the unit. PLAN once + VERIFY once + EXECUTE once is three phases
    # working correctly, not one step failing three times -- conflating them halted a unit that was making progress.
    receipts = [p for p in queue_dir.glob("*.json") if "attempts" not in p.name]
    if vpath is not None:
        # A receipt older than the officer's last word has already been answered -- even a VOID sitting answers it,
        # because the candidate it judged is no longer the one being dispatched. Counting those made a unit that was
        # moving look like a unit that was looping.
        receipts = [r for r in receipts if r.stat().st_mtime > vpath.stat().st_mtime]
    same_phase = [r for r in receipts if f"-{lane.lower()}-" in r.name.lower() or f"-{lane.lower().replace('_','-')}-" in r.name.lower()]

    def _completed(r: Path) -> bool:
        """A dead PRE_ATTEMPT is a process that never started, not a round that was tried.

        Measured 2026-10-31: WP-FHS-17 hit HALTED_REPEAT with "receipts: 3" while every one of those three was a
        PRE_ATTEMPT written before a spawn that then died with the turn. Counting them as attempts converted an
        infrastructure fault into an agent-behaviour verdict and parked the unit for five hours.
        """
        try:
            d = json.loads(r.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            return False
        if d.get("phase") == "PRE_ATTEMPT" and not d.get("attempts"):
            return False
        return bool(d.get("attempts") or d.get("receipt_complete"))

    same_phase = [r for r in same_phase if _completed(r)]
    if len(same_phase) >= MAX_PHASE_ATTEMPTS:
        log({"action": "halted_repeat", "wp": wp, "lane": lane, "receipts": len(same_phase)})
        print(json.dumps({"verdict": "HALTED_REPEAT", "wp": wp, "lane": lane, "receipts": len(same_phase),
                          "detail": "this unit has already been dispatched more than the allowed times without a "
                                    "recorded verdict; it needs a human ruling, not another attempt"}, ensure_ascii=False))
        return 0

    json_out = queue_dir / f"{wp}-{lane.lower()}-{stamp}.json"
    if args.dry_run:
        print(json.dumps({"verdict": "DRY_RUN", "wp": wp, "lane": lane, "phase": phase,
                          "nonce": nonce, "json_out": str(json_out)}, ensure_ascii=False))
        return 0
    pid = launch(lane, prompt, nonce, queue_dir, json_out)
    refresh_status()
    print(json.dumps({"verdict": "DISPATCHED", "wp": wp, "lane": lane, "phase": phase, "pid": pid,
                      "previous_dead_attempts": len(died),
                      "json_out": str(json_out), "nonce": nonce}, ensure_ascii=False))
    # This unit's turn is over (launch() is synchronous: it returns when the lane finishes). The next tick starts from
    # here, hidden, rather than from a clock that puts a console on screen before any of our code runs.
    chain_next(f"{wp}:{lane}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
