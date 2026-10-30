#!/usr/bin/env python3
"""Single preflight entry point for the durability gates.

A lane turn should not start when either of these is true:
  * the policy it will obey is uncommitted          (IR-1)
  * the subject it will claim progress on is not in git (IR-4)

Both conditions are silent by nature: the run succeeds, produces receipts, and the receipts describe
a world nobody else can check out. That is how five rounds ended in NOT_RUN without anyone noticing.

Usage:
    python ir_gate.py --repo DIR --subject DIR [--json]
Exit: 0 ok · 2 policy dirty or subject uncommitted · 3 subject not in a repo
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, *args: str) -> tuple[int, dict]:
    p = subprocess.run([sys.executable, str(HERE / script), *args, "--json"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return p.returncode, json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return p.returncode, {"raw": (p.stdout or "")[-400:], "err": (p.stderr or "")[-400:]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="control-plane repo whose policy will be obeyed")
    ap.add_argument("--subject", required=True, help="artefact this turn claims progress on")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rc1, pol = run("ir1_policy_gate.py", "--repo", a.repo)
    rc2, sub = run("ir4_subject_gate.py", "--path", a.subject)

    ok = rc1 == 0 and rc2 == 0
    out = {
        "schema": "IR-GATE-PREFLIGHT/1",
        "verdict": "GO" if ok else "NO_GO",
        "policy": pol,
        "subject": sub,
        "meaning": ("both gates passed" if ok else
                    "a turn started here would produce receipts that cannot be reproduced "
                    "by a second party; fix the failing gate first"),
    }
    print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else out["verdict"])
    return 0 if ok else (2 if rc1 == 2 or rc2 == 2 else 3)


if __name__ == "__main__":
    sys.exit(main())
