"""WP-11, the three Hermes cells: the model half, measured on the canonical entry.

The nine-cell table stood at 6 PASS + 3 `LOADER_PASS_MODEL_HALF_UNMEASURED`: the Hermes host loaded the
probe skill (the loader half) but no Hermes path answered a model turn, so the cell could not be decided.
WP-12's lab (`scripts/wp12_runtime_path_lab.py`) found the entry that works; this script runs the *same*
protocol the Codex and Claude Code cells ran, on that entry:

    install a probe skill carrying (a) a fresh token and (b) the profile archive digest
      -> ask the host for both in a clean cwd          (POS: both must come back)
      -> uninstall the probe skill
      -> ask the identical question again              (NEG: neither may come back)

`digest` is the archive sha256 of the profile under test (`PIPD/dist/prof-<P>/export_manifest.json`),
`badge` is the profile name the packager wrote into that manifest. A cell passes only when the positive
answer carries both facts and the negative answer carries neither — the token cannot leak from anywhere
but the skill file, because the cwd is empty and outside every repository.

Usage:
    python scripts/wp11_hermes_cells.py [--profiles LITE STANDARD ASSURED] [--json-dir DIR]
"""
import winproc  # noqa: E402  (executed module-level guard; the child tree must stay hidden)
winproc.install()

import argparse
import hashlib
import json
import os
import pathlib
import secrets
import shutil
import subprocess
import sys
import time

# The canonical home of THIS profile: the CLI derives the profile name from HERMES_HOME, so pointing it at
# the product root silently runs the `default` profile and loads no hgk-governed skill (measured: the same
# `-z` answered "active profile is `default` and no fhs-wp11-probe skill is loaded into my context").
HERMES_ROOT = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes")
HERMES_HOME = HERMES_ROOT / "profiles" / "hgk-governed"
AGENT = HERMES_ROOT / "hermes-agent"
RUNTIME_PY = AGENT / ".hermes-runtime" / "python" / "cpython-3.11.17-windows-x86_64-none" / "python.exe"
VENV_SP = AGENT / "venv" / "Lib" / "site-packages"
PROFILE = "hgk-governed"
SKILL_ROOT = HERMES_HOME / "skills"
PIPD_DIST = pathlib.Path(r"C:\Projects\Agent_Workspace\PIPD\dist")
PROBE = "fhs-wp11-probe"


def profile_facts(profile):
    manifest = json.loads((PIPD_DIST / f"prof-{profile}" / "export_manifest.json").read_text(encoding="utf-8"))
    return {
        "archive_sha256": manifest["archive"]["sha256"],
        "archive_name": manifest["archive"]["name"],
        "file_count": manifest["file_count"],
        "badge": manifest.get("profile", {}).get("profile"),
        "assurance": manifest.get("profile", {}).get("assurance"),
        "manifest_path": str(PIPD_DIST / f"prof-{profile}" / "export_manifest.json"),
    }


def emit_skill(token, sha, profile):
    body = (
        "---\n"
        f"name: {PROBE}\n"
        "description: WP-11 host cell probe (installed for one measurement, then removed).\n"
        "---\n"
        f"# {PROBE}\n\n"
        f"PROFILE_UNDER_TEST: {profile}\n"
        f"BUNDLE_ARCHIVE_SHA256: {sha}\n"
        "When asked for the WP-11 host cell token and the bundle archive SHA256, answer with exactly these\n"
        "two lines and nothing else:\n"
        f"TRIGGER_TOKEN: {token}\n"
        f"BUNDLE_ARCHIVE_SHA256: {sha}\n"
    )
    d = SKILL_ROOT / PROBE
    d.mkdir(parents=True, exist_ok=True)
    f = d / "SKILL.md"
    f.write_text(body, encoding="utf-8")
    return f


def run_once(question, workdir, timeout, usage_file):
    env = dict(os.environ)
    env["HERMES_HOME"] = str(HERMES_HOME)
    env["PYTHONPATH"] = os.pathsep.join([str(AGENT), str(VENV_SP)])
    env.pop("HERMES_SERVE_HEADLESS", None)
    started = time.time()
    proc = subprocess.Popen([str(RUNTIME_PY), "-m", "hermes_cli.main", "-z", question,
                             "--usage-file", str(usage_file)],
                            cwd=str(workdir), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, errors="replace", encoding="utf-8")
    try:
        out, err = proc.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
        out, err = proc.communicate()
        timed_out = True
    usage = {}
    if usage_file.exists():
        try:
            usage = json.loads(usage_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            usage = {}
    return {
        "pid": proc.pid,
        "exit": proc.returncode,
        "timed_out": timed_out,
        "duration_s": round(time.time() - started, 2),
        "stdout": (out or "").strip(),
        "stderr_tail": (err or "").strip()[-800:],
        "served_model": usage.get("model"),
        "served_provider": usage.get("provider"),
        "completed": usage.get("completed"),
        "api_calls": usage.get("api_calls"),
        "session_id": usage.get("session_id"),
        "usage_file": str(usage_file),
    }


def cell(profile, timeout, out_dir):
    facts = profile_facts(profile)
    token = f"WP11-HERMES-{profile}-" + secrets.token_hex(4).upper()
    question = ("Load your `fhs-wp11-probe` skill with the host's own skill loader (skill_view), then answer "
                "with the two lines it contains. Do not use the terminal or read files directly.")
    workdir = pathlib.Path(os.environ.get("TMPDIR", r"C:\Users\user\AppData\Local\Temp")) / f"wp11-{token}"
    workdir.mkdir(parents=True, exist_ok=True)
    cwd_entries = sorted(p.name for p in workdir.iterdir())

    skill_file = emit_skill(token, facts["archive_sha256"], profile)
    try:
        pos = run_once(question, workdir, timeout, workdir / "usage_pos.json")
        token_in_pos = token in pos["stdout"]
        digest_in_pos = facts["archive_sha256"] in pos["stdout"]
        badge_in_pos = profile in pos["stdout"]
    finally:
        shutil.rmtree(SKILL_ROOT / PROBE, ignore_errors=True)
        skill_removed = not (SKILL_ROOT / PROBE).exists()

    neg = run_once(question, workdir, timeout, workdir / "usage_neg.json")
    token_in_neg = token in neg["stdout"]
    digest_in_neg = facts["archive_sha256"] in neg["stdout"]

    checks = {
        "positive_exit": pos["exit"] == 0,
        "positive_token": token_in_pos,
        "positive_digest": digest_in_pos,
        "positive_badge": badge_in_pos,
        "skill_removed_before_negative": skill_removed,
        "negative_no_token": not token_in_neg,
        "negative_no_digest": not digest_in_neg,
        "served_model_recorded": bool(pos["served_model"]),
    }
    verdict = "PASS" if all(checks.values()) else "FAIL"
    receipt = {
        "schema": "SBL-HOST-EFFECTIVE-LOAD-RECEIPT/1",
        "cell_id": f"WP-FHS-11.HERMES.{profile}",
        "wp": "WP-FHS-11",
        "host": "hermes",
        "host_entry": {
            "interpreter": str(RUNTIME_PY),
            "module": "hermes_cli.main",
            "hermes_home": str(HERMES_HOME),
            "profile": PROFILE,
        },
        "skill_id": PROBE,
        "install_dir": str(skill_file),
        "manifest_sha": hashlib.sha256(pathlib.Path(facts["manifest_path"]).read_bytes()).hexdigest(),
        "archive_sha256": facts["archive_sha256"],
        "archive_name": facts["archive_name"],
        "file_count": facts["file_count"],
        "profile_badge": facts["badge"],
        "assurance": facts["assurance"],
        "trigger_input_ref": question,
        "trigger_raw_result": pos["stdout"][:600],
        "exit_code": pos["exit"],
        "stderr_tail": pos["stderr_tail"],
        "digest": digest_in_pos,
        "badge": badge_in_pos,
        "negative": {
            "raw": neg["stdout"][:300],
            "token_present_after_uninstall": token_in_neg,
            "digest_present_after_uninstall": digest_in_neg,
            "clean_cwd_design": "token and digest exist only in the probe skill file; cwd is empty and outside every repo",
            "cwd_entries_at_start": cwd_entries,
        },
        "served": {"model": pos["served_model"], "provider": pos["served_provider"],
                   "session_id": pos["session_id"], "pid": pos["pid"], "duration_s": pos["duration_s"],
                   # The checker's clause 3 asked for these two by name: run_once already read them, and the
                   # receipt dropped them, which made "the usage file says completed" an unverifiable claim.
                   "completed": pos["completed"], "api_calls": pos["api_calls"],
                   "usage_file": str(pos.get("usage_file", ""))},
        "loader_half": "PASS (the existing nine-cell record; this receipt measures the model half)",
        "checks": checks,
        "observed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "verdict": verdict,
        "verdict_why": ("the canonical Hermes entry answered both facts from the installed skill and "
                        "answered neither after the skill was removed") if verdict == "PASS" else
                       ("checks failed: " + ", ".join(k for k, v in checks.items() if not v)),
    }
    out = pathlib.Path(out_dir) / f"HERMES_CELL_{profile}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    return receipt, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", nargs="+", default=["LITE", "STANDARD", "ASSURED"])
    ap.add_argument("--json-dir", default=r"C:\Projects\Agent_Workspace\HG-KSEOS\ops\session-20261031\FHS-ALLPASS-20261031\WP-FHS-11\hermes-cells")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    results = []
    for p in args.profiles:
        r, path = cell(p, args.timeout, args.json_dir)
        results.append({"profile": p, "verdict": r["verdict"], "json": str(path),
                        "served": f"{r['served']['provider']}/{r['served']['model']}",
                        "duration_s": r["served"]["duration_s"],
                        "checks": r["checks"]})
        print(json.dumps(results[-1], ensure_ascii=False))
    ok = all(x["verdict"] == "PASS" for x in results)
    print(json.dumps({"cells": len(results), "pass": sum(1 for x in results if x["verdict"] == "PASS"),
                      "verdict": "PASS" if ok else "FAIL"}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
