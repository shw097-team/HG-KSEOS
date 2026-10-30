#!/usr/bin/env python3
"""closed_paths_gate — refuse to write where the project has decided implementations do not live.

Measured context: B1 (141 files) and SKELETON_SPINE (291 files) were written into a documentation tree that is not a
git repository. Their promoted copies live in the delivery repo (b1_closure_20261028/, deliveries/
SKELETON_SPINE_r2_revision2.zip). The originals stayed writable, so the next agent -- me, twice tonight -- kept
putting repairs back into the copy that no one reads and that no test can see.

Two layers, in this order:
  1. this gate, which refuses a dispatch whose working directory or guarded subject sits under a closed path;
  2. a deny-write ACL on the closed directories, which holds even when a tool ignores the gate.

Usage:
  python scripts/closed_paths_gate.py check <path>     # exit 0 open, 3 CLOSED_PATH
  python scripts/closed_paths_gate.py list
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

K = Path(__file__).resolve().parent.parent
CFG = K / "config" / "closed_paths.yaml"


def load() -> list[dict]:
    try:
        data = json.loads(CFG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return [c for c in data.get("closed_paths", []) if c.get("status", "").startswith("CLOSED")]


def check(path: str) -> tuple[bool, dict | None]:
    target = os.path.normcase(os.path.abspath(path))
    for entry in load():
        root = os.path.normcase(os.path.abspath(entry["path"]))
        if target == root or target.startswith(root + os.sep):
            return False, entry
    return True, None


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] == "list":
        for e in load():
            print(f"{e['status']}\t{e['path']}\tpromoted_to={e.get('promoted_to','')}")
        return 0
    if argv[0] == "check":
        target = argv[1] if len(argv) > 1 else os.getcwd()
        ok, entry = check(target)
        if ok:
            print(json.dumps({"verdict": "OPEN", "path": target}, ensure_ascii=False))
            return 0
        print(json.dumps({"verdict": "CLOSED_PATH", "path": target, "closed_path": entry["path"],
                          "promoted_to": entry.get("promoted_to"), "rule": "promote, do not patch in place"},
                         ensure_ascii=False))
        return 3
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
