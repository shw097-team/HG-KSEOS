#!/usr/bin/env python3
"""IR-1 — policy must have a transaction.

A lane turn must not run against a routing surface that exists only as uncommitted edits in one
working tree. When it does, three things follow silently, and all three are fatal to reproducing the
round:
  * the receipt describes revision N while `HEAD` is revision N-5;
  * every other clone (and every later session) reads a different policy;
  * whoever needs a different answer edits the same file again, so the drift compounds.

Usage:
    python ir1_policy_gate.py --repo DIR [--json]
Exit: 0 clean (or no policy surface), 2 POLICY_DIRTY, 3 no repo
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

POLICY_PATHS = [
    "config/model-lane-assignment.json",
    "config/lane-routing-registry.yaml",
    "config/hermes-codex-lane.json",
    "config/active-policy.json",
]


def git(cwd: str, *args: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", cwd, *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rc, _ = git(a.repo, "rev-parse", "--show-toplevel")
    if rc != 0:
        out = {"verdict": "NO_REPO", "repo": a.repo}
        print(json.dumps(out) if a.json else "NO_REPO")
        return 3

    rc, head = git(a.repo, "rev-parse", "--short", "HEAD")
    _, present = git(a.repo, "ls-files", "--", *POLICY_PATHS)
    existing = [p for p in POLICY_PATHS if present.strip() and p in present]
    if not existing:
        out = {"verdict": "NO_POLICY_SURFACE", "repo": a.repo, "head": head.strip()}
        print(json.dumps(out, ensure_ascii=False) if a.json else "NO_POLICY_SURFACE")
        return 0

    _, status = git(a.repo, "status", "--porcelain", "--", *existing)
    dirty = [l for l in status.splitlines() if l.strip()]
    if dirty:
        out = {
            "verdict": "POLICY_DIRTY",
            "repo": a.repo,
            "head": head.strip(),
            "policy_files": existing,
            "dirty": dirty,
            "rule": "IR-1: a receipt produced against uncommitted policy is not reproducible",
            "fix": "commit the policy (or revert it) before starting the turn",
        }
        print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else
              "POLICY_DIRTY  " + ", ".join(d[3:] for d in dirty))
        return 2

    out = {"verdict": "POLICY_COMMITTED", "repo": a.repo, "head": head.strip(), "policy_files": existing}
    print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else f"POLICY_COMMITTED @ {head.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
