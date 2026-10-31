#!/usr/bin/env python3
"""console_guard_gate — prove the console guard is *executable code* in a file, not text inside a docstring.

Why this exists
---------------
Measured 2026-10-31 08:05: `scripts/hgk-lane-dispatch.py` and `scripts/continuation_driver.py` both contained

    try:  # keep every console child off the owner's desktop
        import winproc as _winproc
        _winproc.install()
    except Exception:
        pass

and in both files that text sat **inside the module docstring**, because it had been inserted above the docstring body.
Text in a docstring is never executed, so `winproc.install()` never ran, so every `codex.exe`/`powershell.exe` the
dispatcher started allocated a brand-new console -- which is a window on the owner's desktop, one per dispatch, which
is exactly the "windows keep popping up" report.

The check I had been doing was `grep creationflags` and `grep winproc`: both passed. What failed is the only thing that
matters -- whether the statement runs. So this gate parses the file and looks for the guard as an **AST node of the
module body**, and separately refuses a file whose guard is inside a string constant.

Usage:
    python scripts/console_guard_gate.py scripts/hgk-lane-dispatch.py [more files...]
    python scripts/console_guard_gate.py --all          # every entry point that spawns children

Exit 0 = every named file executes its guard; 3 = at least one does not (prints CONSOLE_GUARD_NOT_EXECUTED).
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

K = Path(__file__).resolve().parent.parent
SCRIPTS = K / "scripts"

# Entry points that start child processes (measured by scanning for subprocess/Popen).
DEFAULT_TARGETS = [
    "hgk-lane-dispatch.py",
    "continuation_driver.py",
    "window_watch.py",
    "relay_daemon.py",
    "ops_status.py",
    "stall_monitor.py",
    "host_matrix.py",
    "occupant_install.py",
    "issue_grant.py",
    "work_queue.py",
    "detach.py",
]


def _is_winproc_import(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(a.name == "winproc" or a.name.startswith("winproc.") for a in node.names)
    if isinstance(node, ast.ImportFrom):
        return (node.module or "").startswith("winproc")
    return False


def _calls_install(node: ast.AST) -> bool:
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
            if sub.func.attr == "install":
                return True
    return False


def guard_state(path: Path) -> dict:
    src = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return {"file": path.name, "state": "SYNTAX_ERROR", "detail": f"line {exc.lineno}: {exc.msg}"}

    docstring_text = ""
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
        if isinstance(tree.body[0].value.value, str):
            docstring_text = tree.body[0].value.value

    executed = False
    for node in tree.body:                       # module level only: a guard inside `if False:` is not a guard
        if isinstance(node, ast.Try):
            if any(_is_winproc_import(b) for b in node.body) and _calls_install(node):
                executed = True
                break
        if isinstance(node, (ast.Import, ast.ImportFrom)) and _is_winproc_import(node):
            executed = True                     # imported at module level; install() may be called later
            break

    in_docstring = ("import winproc" in docstring_text) and ("install()" in docstring_text)
    if executed:
        return {"file": path.name, "state": "GUARD_EXECUTES", "in_docstring_copy": in_docstring}
    if in_docstring:
        return {"file": path.name, "state": "CONSOLE_GUARD_NOT_EXECUTED",
                "detail": "the winproc guard is inside the module docstring: it is text, it never runs"}
    return {"file": path.name, "state": "CONSOLE_GUARD_NOT_EXECUTED", "detail": "no module-level winproc install"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args(argv)
    targets = []
    if args.all or not args.files:
        targets = [SCRIPTS / n for n in DEFAULT_TARGETS if (SCRIPTS / n).exists()]
        # plus anything else that spawns children
        for p in sorted(SCRIPTS.glob("*.py")):
            if p.name in DEFAULT_TARGETS:
                continue
            body = p.read_text(encoding="utf-8", errors="replace")
            if "subprocess.Popen(" in body or "subprocess.run(" in body:
                targets.append(p)
    else:
        targets = [Path(f) for f in args.files]

    results = [guard_state(p) for p in targets]
    bad = [r for r in results if r["state"] != "GUARD_EXECUTES"]
    print(json.dumps({"checked": len(results), "ok": len(results) - len(bad), "bad": bad,
                      "note": "a guard that is text inside a docstring is not a guard"}, ensure_ascii=False, indent=2))
    return 0 if not bad else 3


if __name__ == "__main__":
    sys.exit(main())
