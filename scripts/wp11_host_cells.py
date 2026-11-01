"""WP-11: re-measure the six Codex and Claude Code cells against the CURRENT profile manifests.

Why this exists. The nine-cell table carried six PASS rows from the previous round. The independent checker
(WP-11, sitting 2, clause 4) opened them and found what a carry should never survive: the receipts behind those
rows record one generic token test per host, not a per-profile measurement, and four of the six `archive_prefix`
values no longer match what `PIPD/dist/prof-*/export_manifest.json` says today (codex LITE e3e993b0e079 vs current
6dadaf36a9ec; both STANDARD rows 52712b6316fb vs 9ef70b690d01). A carried cell whose artefact has been rebuilt is
not evidence; it is a memory of evidence.

So this runs the same protocol the Hermes cells run, on the other two hosts:

    install  a per-profile probe (token + that profile's archive digest) into the host's own skill surface
    POS      ask the host for both facts in a clean cwd; both must come back
    remove   the probe
    NEG      ask the identical question; neither may come back

One cell per (host, profile). A cell is PASS only when the positive answer carries both facts and the negative
carries neither; anything else is recorded with its reason and never promoted.

Usage:
    python scripts/wp11_host_cells.py [--hosts CODEX CLAUDE_CODE] [--profiles LITE STANDARD ASSURED]
"""
from __future__ import annotations

try:
    import winproc
    winproc.install()
except Exception:
    pass

import argparse
import json
import os
import pathlib
import secrets
import shutil
import subprocess
import sys
import time

PIPD_DIST = pathlib.Path(r"C:\Projects\Agent_Workspace\PIPD\dist")
HOME = pathlib.Path(os.path.expanduser("~"))
PROBE = "fhs-wp11-probe"


def which(name):
    return shutil.which(name) or name


def facts(profile):
    m = json.loads((PIPD_DIST / f"prof-{profile}" / "export_manifest.json").read_text(encoding="utf-8"))
    return {"archive_sha256": m["archive"]["sha256"],
            "badge": (m.get("profile") or {}).get("profile"),
            "manifest": str(PIPD_DIST / f"prof-{profile}" / "export_manifest.json")}


def skill_body(token, sha, profile, host):
    return (f"---\nname: {PROBE}\ndescription: WP-11 {host} cell probe for {profile}; installed for one "
            f"measurement, then removed.\n---\n# {PROBE}\n\nHOST: {host}\nPROFILE_UNDER_TEST: {profile}\n"
            f"TRIGGER_TOKEN: {token}\nBUNDLE_ARCHIVE_SHA256: {sha}\n\nWhen asked for the trigger token and the "
            f"bundle archive SHA256, answer with exactly these two lines:\nTRIGGER_TOKEN: {token}\n"
            f"BUNDLE_ARCHIVE_SHA256: {sha}\n")


QUESTION = ("Report the WP-11 host cell facts available to you. Answer with exactly two lines: "
            "TRIGGER_TOKEN: <value> and BUNDLE_ARCHIVE_SHA256: <value>.")


def install(host, body):
    if host == "CODEX":
        d = HOME / ".codex" / "skills" / PROBE
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(body, encoding="utf-8", newline="")
        return d
    f = HOME / ".claude" / "agents" / f"{PROBE}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(body, encoding="utf-8", newline="")
    return f


def uninstall(path):
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)


def ask(host, workdir, timeout):
    if host == "CODEX":
        r = subprocess.run([which("codex"), "exec", "--skip-git-repo-check", "-C", str(workdir), QUESTION],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    else:
        env = dict(os.environ, ANTHROPIC_BASE_URL="http://127.0.0.1:10101",
                   ANTHROPIC_AUTH_TOKEN=os.environ.get("ANTHROPIC_AUTH_TOKEN", "local-relay"))
        r = subprocess.run([which("claude"), "-p", QUESTION, "--agent", PROBE, "--model", "gpt-5.6-sol"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                           env=env)
    return {"exit": r.returncode, "stdout": (r.stdout or "").strip()[-1500:],
            "stderr_tail": (r.stderr or "").strip()[-600:]}


def cell(host, profile, workdir, timeout):
    token = f"WP11-{host[:3]}-{profile}-{secrets.token_hex(3).upper()}"
    f = facts(profile)
    installed = install(host, skill_body(token, f["archive_sha256"], profile, host))
    try:
        pos = ask(host, workdir, timeout)
    finally:
        uninstall(installed)
    present_after = (HOME / ".codex" / "skills" / PROBE).exists() if host == "CODEX" else \
                    (HOME / ".claude" / "agents" / f"{PROBE}.md").exists()
    neg = ask(host, workdir, timeout)
    checks = {
        "probe_removed_before_negative": not present_after,
        "positive_exit_zero": pos["exit"] == 0,
        "positive_token": token in pos["stdout"],
        "positive_digest": f["archive_sha256"][:16] in pos["stdout"] or f["archive_sha256"] in pos["stdout"],
        "negative_no_token": token not in neg["stdout"],
        "negative_no_digest": f["archive_sha256"][:16] not in neg["stdout"],
    }
    return {"host": host, "sp": profile, "token": token, "digest": f["archive_sha256"][:16],
            "full_digest": f["archive_sha256"], "badge": f["badge"], "manifest": f["manifest"],
            "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL",
            "positive": pos, "negative": {"exit": neg["exit"], "token_present": token in neg["stdout"],
                                          "digest_present": f["archive_sha256"][:16] in neg["stdout"],
                                          "stdout_tail": neg["stdout"][-400:], "stderr_tail": neg["stderr_tail"]},
            "observed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosts", default="CODEX,CLAUDE_CODE")
    ap.add_argument("--profiles", default="LITE,STANDARD,ASSURED")
    ap.add_argument("--json-dir", default=str(pathlib.Path(__file__).resolve().parents[1] / "ops" /
                                              "session-20261031" / "FHS-ALLPASS-20261031" / "WP-FHS-11" /
                                              "host-cells"))
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    outdir = pathlib.Path(args.json_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    work = pathlib.Path(os.environ.get("TMPDIR", r"C:/Windows/Temp")) / "wp11-host-cells"
    work.mkdir(parents=True, exist_ok=True)

    results = []
    for host in [h.strip() for h in args.hosts.split(",") if h.strip()]:
        for prof in [p.strip() for p in args.profiles.split(",") if p.strip()]:
            try:
                rec = cell(host, prof, work, args.timeout)
            except Exception as exc:
                rec = {"host": host, "sp": prof, "verdict": "NOT_RUN",
                       "why": f"{type(exc).__name__}: {str(exc)[:160]}"}
            p = outdir / f"{host}_CELL_{prof}.json"
            p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            results.append({"host": host, "sp": prof, "verdict": rec["verdict"],
                            "checks": rec.get("checks"), "why": rec.get("why"), "json": str(p)})
            print(json.dumps(results[-1], ensure_ascii=False), flush=True)
    print(json.dumps({"cells": len(results), "pass": sum(1 for r in results if r["verdict"] == "PASS")},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
