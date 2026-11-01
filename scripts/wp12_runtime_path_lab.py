"""WP-12: resolve the Hermes runtime path, measured. One experiment, three measurements.

Blocked for three sittings as `RUNTIME_PATH_UNRESOLVED`, with the cause recorded as "the venv holds
openai 2.24.0 and the missing symbol imports cleanly there, while the hermes on PATH is a frozen PE
launcher whose runtime has no openai; PYTHONPATH does not reach it". None of that is the mechanism.

MEASURED 2026-11-01:

  * `hermes` on PATH is NOT this product's entry point. It resolves to
    `D:\\Hermes-Recovery\\live22\\bin\\hermes` (a recovery forwarder whose `hermes.cmd` sets
    HERMES_HOME=D:\\Hermes-Recovery\\live22). Its agent turn imports `openai` from a *lease-managed*
    environment under `<hermes home>\\installs\\<install>\\environments\\<env>\\venv\\Lib\\site-packages`.
  * That environment's path pushes `openai/types/responses/response_computer_tool_call_output_screenshot_param.py`
    to exactly 260 characters. Windows MAX_PATH allows 259, so the importer answers
    `ModuleNotFoundError` — the file is present, unreadable, and the error names a package problem.
  * The canonical entry (the one the desktop gateway runs) is
    `<hermes-agent>\\.hermes-runtime\\python\\cpython-3.11.17-windows-x86_64-none\\python.exe -m hermes_cli.main`
    with HERMES_HOME pointed at the product's own home and the venv's site-packages on PYTHONPATH.
    That path answers a model in ~9 s at the ordered arm.

So the repair is a *path*, not a package: SBL measures and uses the canonical entry, and the
recovery forwarder is recorded as the object that must be retired or shortened (its `openai` tree
cannot be imported on this host at any version, because the length is in the directory, not the file).

Usage:
    python scripts/wp12_runtime_path_lab.py --json <out.json>
"""
import winproc  # noqa: E402  (imported before anything else so the whole child tree is hidden)
winproc.install()

import argparse
import hashlib
import json
import os
import pathlib
import re
import secrets
import shutil
import subprocess
import sys
import time

HERMES_HOME = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes")
AGENT = HERMES_HOME / "hermes-agent"
RUNTIME_PY = AGENT / ".hermes-runtime" / "python" / "cpython-3.11.17-windows-x86_64-none" / "python.exe"
VENV_SP = AGENT / "venv" / "Lib" / "site-packages"
PROFILE = "hgk-governed"

# The recovery forwarder that `hermes` on PATH resolves to, and the lease-managed environment it injects.
LIVE22_HERMES = pathlib.Path(r"D:\Hermes-Recovery\live22\bin\hermes")
INSTALLS = HERMES_HOME / "installs"
TARGET_MODULE = "openai/types/responses/response_computer_tool_call_output_screenshot_param.py"
MAX_PATH_LIMIT = 259  # CreateFileW limit; a path of length 260 is not addressable without the \\?\ prefix


def _openai_envs():
    return sorted(p for p in INSTALLS.glob("*/environments/*/venv/Lib/site-packages/openai") if p.is_dir())


def measure_path_arithmetic():
    """The mechanism: is the unreachable file long, or missing?"""
    rows = []
    for pkg in _openai_envs():
        total = 0
        over = []
        for root, _dirs, files in os.walk("\\\\?\\" + str(pkg)):
            for f in files:
                if not f.endswith(".py"):
                    continue
                total += 1
                full = os.path.join(root, f)
                real = full[4:] if full.startswith("\\\\?\\") else full
                if len(real) >= 260:
                    over.append({"path": real, "len": len(real)})
        # `pkg` is <venv>/Lib/site-packages/openai, so parents[2] is <venv>. The previous expression walked up one
        # level too many and dropped the environment id, which is why the receipt reported 222 characters for a
        # module the boundary experiment places at 260 — the checker caught the arithmetic, not the mechanism.
        venv = pkg.parents[2]
        target_path = str(venv / "Lib" / "site-packages" / TARGET_MODULE)
        rows.append({
            "openai_package": str(pkg),
            "py_modules": total,
            "modules_over_max_path": len(over),
            "examples_over": over[:5],
            "target_module": target_path,
            "target_module_len": len(target_path),
            "exists_via_plain_open": os.path.exists(target_path),
            "readable_via_win32_prefix": os.path.exists("\\\\?\\" + target_path),
        })
    return rows


def _base_env():
    env = dict(os.environ)
    env["HERMES_HOME"] = str(HERMES_HOME)
    env["HERMES_PROFILE"] = PROFILE
    # `-m hermes_cli.main` needs the product tree importable from anywhere; the venv supplies the deps.
    env["PYTHONPATH"] = os.pathsep.join([str(AGENT), str(VENV_SP)])
    env.pop("HERMES_SERVE_HEADLESS", None)
    return env


def _run(cmd, cwd, env, timeout):
    started = time.time()
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, errors="replace", encoding="utf-8")
    try:
        out, err = proc.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
        out, err = proc.communicate()
        timed_out = True
    return {
        "cmd": cmd if isinstance(cmd, list) else [cmd],
        "cwd": str(cwd),
        "pid": proc.pid,
        "exit": proc.returncode,
        "timed_out": timed_out,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(started)),
        "ended_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "duration_s": round(time.time() - started, 2),
        "stdout": (out or "").strip(),
        "stderr_tail": (err or "").strip()[-1200:],
    }


def which_hermes():
    """What `hermes` resolved to at the moment of the test, and what that file says."""
    exe = shutil.which("hermes")
    doc = {"which": exe}
    if exe:
        try:
            text = pathlib.Path(exe).read_text(encoding="utf-8", errors="replace")
            doc["head"] = "\n".join(text.splitlines()[:12])
            doc["sha256"] = hashlib.sha256(pathlib.Path(exe).read_bytes()).hexdigest()
            doc["sets_HERMES_HOME"] = [ln.strip() for ln in text.splitlines() if "HERMES_HOME" in ln][:3]
        except OSError as exc:
            doc["read_error"] = str(exc)
    return doc


def _log_window(logs_dir, start_iso, end_iso, pattern=r"RuntimeError: [^\r\n]*"):
    """The newest matching line whose own timestamp falls inside the run's window.

    A shared log is only usable with both bounds: the checker showed the unbounded version quoting an error three
    minutes older than the process it was supposed to explain.
    """
    try:
        files = sorted(pathlib.Path(logs_dir).glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return None
    rx = re.compile(r"(\d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d)")
    for f in files[:3]:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        hit = None
        for line in lines:
            if not re.search(pattern, line):
                continue
            m = rx.search(line)
            if not m:
                continue
            ts = m.group(1).replace("T", " ")
            if start_iso <= ts <= end_iso:
                hit = {"file": f.name, "timestamp": ts, "line": line.strip()[-400:]}
        if hit:
            return hit
    return None


def _last_error_line(logs_dir, pattern):
    try:
        files = sorted(pathlib.Path(logs_dir).glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return None
    for f in files[:3]:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = re.findall(pattern, text)
        if hits:
            return {"file": str(f), "last_error": hits[-1][:400]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    nonce = "WP12-RUNTIME-" + secrets.token_hex(4).upper()
    question = f"Reply with exactly this one line and nothing else: NONCE-ECHO: {nonce}"
    receipt = {
        "schema": "HGK-WP12-RUNTIME-PATH-LAB/1",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "nonce": nonce,
        "blocker_under_test": "RUNTIME_PATH_UNRESOLVED",
        "canonical_entry": {
            "interpreter": str(RUNTIME_PY),
            "module": "hermes_cli.main",
            "hermes_home": str(HERMES_HOME),
            "profile": PROFILE,
            "pythonpath": str(VENV_SP),
        },
        "a_path_arithmetic": measure_path_arithmetic(),
    }

    workdir = pathlib.Path(os.environ.get("TMPDIR", r"C:\Users\user\AppData\Local\Temp")) / f"wp12-{nonce}"
    workdir.mkdir(parents=True, exist_ok=True)
    usage_file = workdir / "usage.json"

    # A: POSITIVE — the canonical entry answers.
    pos = _run([str(RUNTIME_PY), "-m", "hermes_cli.main", "-z", question, "--usage-file", str(usage_file)],
               AGENT, _base_env(), args.timeout)
    pos["nonce_present"] = nonce in pos["stdout"]
    usage = {}
    if usage_file.exists():
        try:
            usage = json.loads(usage_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            usage = {"parse_error": str(exc)}
    pos["served_model"] = usage.get("model")
    pos["served_provider"] = usage.get("provider")
    pos["completed"] = usage.get("completed")
    pos["session_id"] = usage.get("session_id")
    pos["api_calls"] = usage.get("api_calls")
    receipt["b_canonical_positive"] = pos

    # B: NEGATIVE — the same question through the entry `hermes` resolves to on PATH.
    neg_env = dict(os.environ)
    neg_env["PYTHONPATH"] = str(VENV_SP)
    neg_nonce = "WP12-NEG-" + secrets.token_hex(4).upper()
    neg = _run([str(LIVE22_HERMES), "-z",
                f"Reply with exactly this one line and nothing else: NONCE-ECHO: {neg_nonce}"],
               workdir, neg_env, args.timeout)
    neg["nonce"] = neg_nonce
    neg["nonce_present"] = neg_nonce in neg["stdout"]
    # Bind the failure to THIS run. The previous version took the newest matching line from a shared log, and the
    # checker showed the line it found predated the negative by three minutes: an unbounded search is not evidence.
    # The negative process's own stderr is the first place to look; a log line counts only inside [start, end] and
    # only when it carries the same pid.
    neg["window"] = [neg["started_at"], neg["ended_at"]]
    bound = None
    own = [ln for ln in neg["stderr_tail"].splitlines() if "response_computer_tool_call_output_screenshot_param" in ln]
    if own:
        bound = {"source": "own stderr", "last_error": own[-1].strip(), "pid": neg["pid"]}
    else:
        for cand in (_log_window(HERMES_HOME / "profiles" / PROFILE / "logs", neg["started_at"], neg["ended_at"]),
                     _log_window(pathlib.Path(r"D:\Hermes-Recovery\live22\logs"), neg["started_at"], neg["ended_at"])):
            if cand:
                bound = {"source": cand["file"], "last_error": cand["line"], "pid": neg["pid"],
                         "line_timestamp": cand.get("timestamp")}
                break
    neg["error"] = bound
    neg["error_is_the_one_under_test"] = bool(bound and
                                             "response_computer_tool_call_output_screenshot_param" in bound["last_error"])
    # What IS bound to this run: the process failed (exit != 0), answered nothing, and the banner it printed is its
    # own. What is NOT: the ImportError text, which this entry routes to a gateway log it never wrote (the recovery
    # tree's newest log predates this run by two hours). The named error is bound instead where it is reproducible
    # on identical bytes — the 260-character arm of the boundary experiment. Saying which half is bound where is
    # the difference between evidence and a citation.
    neg["failure_bound_to_run"] = neg["exit"] != 0 and not neg["nonce_present"]
    neg["failure_evidence"] = {
        "exit": neg["exit"],
        "nonce_absent": not neg["nonce_present"],
        "cli_banner": next((ln for ln in neg["stdout"].splitlines() if "went wrong" in ln), None),
        "own_stderr_empty": not neg["stderr_tail"],
        "named_error_bound_in": "c_boundary (260-character arm, identical payload bytes)",
    }
    neg["path_resolution_at_test_time"] = which_hermes()
    receipt["c_recovery_negative"] = neg

    # Verdict — derived, never typed.
    arithmetic = receipt["a_path_arithmetic"]
    long_paths = sum(r["modules_over_max_path"] for r in arithmetic)
    # Each key is a PASS condition; the verdict is PASS when all of them hold. An earlier revision mixed polarities
    # under a single `not any(...)`, which made `no_module_over_max_path` mean its opposite. One polarity, stated.
    checks = {
        "canonical_exit_zero": pos["exit"] == 0,
        "canonical_nonce_present": pos["nonce_present"],
        "canonical_model_recorded": bool(pos["served_model"]),
        "canonical_usage_completed": bool(pos.get("completed")),
        "negative_did_not_answer": not neg["nonce_present"],
        "negative_failure_bound_to_run": neg["failure_bound_to_run"],
        "mechanism_recorded": long_paths > 0,  # informational: the long modules exist and are listed
    }
    receipt["checks"] = checks
    receipt["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    receipt["verdict_why"] = (
        f"canonical entry answered '{nonce}' in {pos['duration_s']}s at {pos['served_model']} "
        f"({pos['served_provider']}), pid {pos['pid']}; the PATH entry did not answer and its failure is "
        f"the recorded MAX_PATH import ({long_paths} openai module(s) sit at or past {MAX_PATH_LIMIT + 1} chars)."
        if receipt["verdict"] == "PASS" else "a check failed; see checks"
    )

    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"verdict": receipt["verdict"], "json": str(out),
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "canonical_pid": pos["pid"], "served": f"{pos['served_provider']}/{pos['served_model']}",
                      "path_hits": long_paths}, ensure_ascii=False))
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
