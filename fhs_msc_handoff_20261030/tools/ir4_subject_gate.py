#!/usr/bin/env python3
"""IR-4 — a subject must exist in the durable layer.

Any round that claims progress on an artefact must be able to name a commit that contains it.
A directory on disk, a sealed zip nobody published, or a worktree that will be overwritten is not a
subject: it cannot be verified by a second party, cannot be diffed, and cannot be rolled back.

Checks, in order:
  1. is the path inside a git worktree?            (else NO_REPO)
  2. are its files tracked in HEAD?                (else NOT_COMMITTED)
  3. is the working tree clean for those files?     (else DIRTY_SUBJECT — the claim describes bytes
                                                     that exist only locally)

Usage:
    python ir4_subject_gate.py --path DIR [--json] [--advisory]
Exit: 0 COMMITTED, 2 NOT_COMMITTED, 3 NO_REPO, 4 DIRTY_SUBJECT
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(cwd: str, *args: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--advisory", action="store_true")
    a = ap.parse_args()

    target = Path(a.path)
    if not target.exists():
        out = {"verdict": "MISSING", "path": a.path}
        print(json.dumps(out) if a.json else out["verdict"])
        return 0 if a.advisory else 3

    cwd = str(target if target.is_dir() else target.parent)
    rc, top = git(cwd, "rev-parse", "--show-toplevel")
    if rc != 0:
        out = {"verdict": "NO_REPO", "path": a.path,
               "detail": "not inside any git worktree: no lineage, no diff, no rollback",
               "effect": "claims about this subject are ADVISORY_ONLY"}
        print(json.dumps(out, ensure_ascii=False) if a.json else f"NO_REPO  {a.path}")
        return 0 if a.advisory else 3

    root = top.strip()
    rel = str(target.resolve()).replace("\\", "/")
    rc, head = git(root, "rev-parse", "--short", "HEAD")
    rc2, tracked = git(root, "ls-files", "--", str(target))
    n_tracked = len([l for l in tracked.splitlines() if l.strip()])

    rc3, dirty = git(root, "status", "--porcelain", "--", str(target))
    dirty_lines = [l for l in dirty.splitlines() if l.strip()]

    if n_tracked == 0:
        verdict, code = "NOT_COMMITTED", 2
    elif dirty_lines:
        verdict, code = "DIRTY_SUBJECT", 4
    else:
        verdict, code = "COMMITTED", 0

    out = {
        "verdict": verdict,
        "path": a.path,
        "repo": root,
        "head": head.strip(),
        "tracked_files": n_tracked,
        "dirty_entries": len(dirty_lines),
        "rule": "IR-4: a round may only claim progress on a subject that has a commit",
        "effect": "ADVISORY_ONLY" if verdict != "COMMITTED" else "ok",
    }
    print(json.dumps(out, ensure_ascii=False, indent=1) if a.json else f"{verdict} @ {head.strip()}  tracked={n_tracked} dirty={len(dirty_lines)}  {a.path}")
    return 0 if a.advisory else code


if __name__ == "__main__":
    sys.exit(main())
