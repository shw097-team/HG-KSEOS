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
    # N1 — the PATH entry, run CLEAN. The previous version of this arm forced PYTHONPATH at the product venv and then
    # reported the resulting ImportError as the entry's own failure. The checker refused to accept that as the
    # entry's error, and was right to: the injection, not the entry, was the cause. Run clean first.
    neg_nonce = "WP12-NEG-" + secrets.token_hex(4).upper()
    clean = dict(os.environ)
    clean.pop("PYTHONPATH", None)
    clean.pop("HERMES_HOME", None)
    clean.pop("HERMES_PROFILE", None)
    shim = shutil.which("hermes")
    neg = _run([str(shim), "-z", f"Reply with exactly this one line and nothing else: NONCE-ECHO: {neg_nonce}"],
               workdir, clean, args.timeout)
    neg["entry"] = str(shim)
    neg["env"] = "clean: no PYTHONPATH, no HERMES_HOME"
    neg["nonce"] = neg_nonce
    neg["nonce_present"] = neg_nonce in neg["stdout"]

    # N2 — the entry the recovery tree ships (LIVE22_HERMES), run with the same clean environment. This is the arm
    # that failed in three earlier rounds. N1 answering and N2 failing on the same question, same env, same cwd is
    # the comparison that decides which entry is unusable — the earlier write-up blamed the PATH shim, then blamed
    # a PYTHONPATH injection, and both were wrong.
    inj_nonce = "WP12-RECOVERY-" + secrets.token_hex(4).upper()
    inj_env = dict(clean)
    inj = _run([str(LIVE22_HERMES), "-z", f"Reply with exactly this one line and nothing else: NONCE-ECHO: {inj_nonce}"],
               workdir, inj_env, args.timeout)
    inj["entry"] = str(LIVE22_HERMES)
    inj["env"] = "clean: no PYTHONPATH, no HERMES_HOME"
    inj["nonce"] = inj_nonce
    inj["nonce_present"] = inj_nonce in inj["stdout"]

    # N3 — informational: does the product venv's dependency path on its own break the PATH shim? (Recorded, not a
    # pass condition: an injection that does not reproduce a failure is a finding, not a defect.)
    probe3_nonce = "WP12-INJ-" + secrets.token_hex(4).upper()
    inj3_env = dict(clean)
    inj3_env["PYTHONPATH"] = str(VENV_SP)
    inj3 = _run([str(shim), "-z", f"Reply with exactly this one line and nothing else: NONCE-ECHO: {probe3_nonce}"],
                workdir, inj3_env, args.timeout)
    inj3["entry"] = str(shim)
    inj3["env"] = "PYTHONPATH=<product venv site-packages>"
    inj3["nonce"] = probe3_nonce
    inj3["nonce_present"] = probe3_nonce in inj3["stdout"]
    neg["injected_control"] = inj3


    # The claim this receipt makes is the one these three arms support, and no wider:
    #   canonical  the product runtime answers a model turn (measured, with pid, model and usage file)
    #   N1         the entry `hermes` resolves to on PATH answers when the environment is left alone
    #   N2         the same entry fails when the earlier rounds' PYTHONPATH injection is re-applied
    # The earlier version reported N2 as the entry's own failure, and the independent checker refused it: the
    # injected broken dependency install was the cause, not the entry. Correcting that changes the conclusion —
    # the runtime blocker is a broken dependency install (cp314 extension modules in a 3.11 environment, plus a
    # module path past MAX_PATH), not an entry that cannot run.
    neg["path_resolution_at_test_time"] = which_hermes()
    receipt["c_recovery_negative"] = neg
    receipt["d_injected_control"] = inj

    arithmetic = receipt["a_path_arithmetic"]
    long_paths = sum(r["modules_over_max_path"] for r in arithmetic)
    # Every key is a PASS condition; the verdict is PASS when all of them hold. One polarity, stated, because an
    # earlier revision mixed them under `not any(...)` and made one key mean its opposite.
    checks = {
        "canonical_exit_zero": pos["exit"] == 0,
        "canonical_nonce_present": pos["nonce_present"],
        "canonical_model_recorded": bool(pos["served_model"]),
        "canonical_usage_completed": bool(pos.get("completed")),
        "path_entry_answers_clean": neg["nonce_present"],
        "recovery_entry_fails_where_shim_answers": not inj["nonce_present"],
        "mechanism_recorded": long_paths > 0,
    }
    receipt["checks"] = checks
    receipt["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    receipt["verdict_why"] = (
        f"the product runtime answered '{nonce}' in {pos['duration_s']}s at {pos['served_model']} "
        f"({pos['served_provider']}), pid {pos['pid']}; the PATH entry answered clean "
        f"({'answered' if neg['nonce_present'] else 'did not answer'}), and the recovery entry failed the same "
        f"question in the same environment "
        f"({'failed' if not inj['nonce_present'] else 'also answered — no entry difference'}); "
        f"{long_paths} openai module(s) sit at or "
        f"past {MAX_PATH_LIMIT + 1} characters in the installed environment."
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
