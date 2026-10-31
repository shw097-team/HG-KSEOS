#!/usr/bin/env python3
"""Owner-side issuance for a sandboxed subject run (WP-FHS-17).

Why this exists: the owner's private key is DPAPI-wrapped and cannot be unwrapped inside the codex sandbox, so a
checker that runs the install chain can never mint its own admission or grant. Two wrong answers were available:
give the checker the key, or let it proceed on a stale admission. This does neither.

The subject states what it needs (`WP17_PREPARE_ONLY=1` writes the exact argv), the owner's issuer signs it here,
outside the sandbox, and the subject consumes the signed object (`WP17_PREISSUED=<dir>`). The checker never holds
signing capability.

Usage:
    python scripts/wp17_owner_preissue.py --subject <path to the WP-FHS-17 copy> [--out <dir>]

It loops: prepare -> sign what was requested -> prepare again -> ... until every requested object exists. It never
runs the chain itself; the officer does that.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess

# Module-level, executed (not described in the docstring): the console gate reads the AST, because a guard that is
# text inside a docstring never runs. winproc keeps every descendant of this process on one hidden console.
try:
    import winproc as _winproc
    _winproc.install()
except Exception:  # non-Windows, or the helper is absent: the per-call CREATE_NO_WINDOW above still applies
    _winproc = None
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update(env_extra or {})
    # Same window rule as everywhere else on this host: a console child of a console-less parent gets a NEW
    # console, and a new console is a visible window. This script runs one-shot from the owner side, but it was
    # the only subject the console gate still flagged, so it gets the flag like the rest of the tree.
    kw = {}
    if os.name == "nt":
        kw["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=600, **kw)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True, help="the WP-FHS-17 tree the officer will run")
    ap.add_argument("--out", default=None, help="where the signed objects land (default <subject>/evidence/preissued)")
    ap.add_argument("--max-rounds", type=int, default=6)
    args = ap.parse_args(argv)

    subject = Path(args.subject).resolve()
    build = subject / "tools" / "build_evidence.py"
    if not build.is_file():
        print(json.dumps({"ok": False, "why": f"no build_evidence.py under {subject}"}))
        return 2
    out_dir = Path(args.out).resolve() if args.out else subject / "evidence" / "preissued"
    out_dir.mkdir(parents=True, exist_ok=True)

    signed: list[dict] = []
    for rnd in range(1, args.max_rounds + 1):
        env = {"WP17_PREPARE_ONLY": "1"}
        if any(out_dir.glob("*.json")):
            env["WP17_PREISSUED"] = str(out_dir)
        res = run([sys.executable, str(build)], subject, env)
        req_path = subject / "evidence" / "preissue-request.json"
        if not req_path.is_file():
            print(json.dumps({"ok": False, "why": "prepare produced no request file",
                              "stdout_tail": res.stdout[-800:], "stderr_tail": res.stderr[-800:]}))
            return 3
        doc = json.loads(req_path.read_text(encoding="utf-8"))
        pending = [r for r in doc.get("requests") or [] if not (out_dir / f"{r['op']}.json").is_file()]
        if not pending:
            print(json.dumps({"ok": True, "rounds": rnd, "signed": signed, "out": str(out_dir),
                              "note": "every requested object exists; the officer can run with WP17_PREISSUED"},
                             ensure_ascii=False))
            return 0
        for req in pending:
            op = req["op"]
            sig = run([str(a) for a in req["argv"]], subject, None)
            produced = Path(req["out"])
            if sig.returncode != 0 or not produced.is_file():
                print(json.dumps({"ok": False, "why": f"issuer refused {op}", "exit": sig.returncode,
                                  "stderr_tail": sig.stderr[-900:], "stdout_tail": sig.stdout[-400:]},
                                 ensure_ascii=False))
                return 4
            import shutil
            shutil.copyfile(produced, out_dir / f"{op}.json")
            signed.append({"op": op, "exit": sig.returncode, "out": str(out_dir / f'{op}.json')})
    print(json.dumps({"ok": False, "why": "did not converge", "signed": signed}, ensure_ascii=False))
    return 5


if __name__ == "__main__":
    raise SystemExit(main())
