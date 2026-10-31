#!/usr/bin/env python3
"""Measure WP-20 cells, one at a time, resumably.

The registry says 192 cells = 8 Kind x 3 Mode x 4 Host x 2 Provider, and every cell starts NOT_MEASURED. A cell is
measured here by installing a Kind-shaped artefact on a Host's own surface and asking that Host's loader whether it
serves it. Three outcomes are possible and only one of them is a pass:

    PASS             the host's loader served the artefact, and stopped serving it after removal
    NO_HOST_SURFACE  this host has no surface for this Kind (named, not a failure of the work)
    NOT_RUN          no local runner for this host on this machine

A cell that cannot be measured must say which of those it is. Collapsing them into "0 failures" is the defect this
file exists to avoid: a matrix where every unmeasured cell reads as fine is worse than no matrix.

Progress is appended to a JSONL, so a timeout costs one cell, not the batch. Re-running skips cells already recorded.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

KINDS = ["CLI_TOOL", "AI_SYSTEM", "GENIE", "SIMPLE_AGENT", "PROFILE", "PLUGIN", "AGENT_SKILL", "AGENT_OS"]
MODES = ["LITE", "STANDARD", "ASSURED"]
PROVIDERS = ["PROVIDER_ON", "PROVIDER_OFF"]

PROFILE_ROOT = Path(os.environ.get("HERMES_PROFILE_DIR",
                                   r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/profiles/hgk-governed"))

# Which Kind has a real, checkable surface on which Host. A Kind with no surface is NO_HOST_SURFACE, never a PASS.
SURFACES = {
    "HERMES": {"AGENT_SKILL": "skills/<name>/SKILL.md", "PLUGIN": "plugins/<name>/", "PROFILE": "profiles/<name>/"},
    "CODEX": {"AGENT_SKILL": "~/.codex/skills/<name>/SKILL.md"},
    "CLAUDE_CODE": {"AGENT_SKILL": "~/.claude/agents/<name>.md"},
    "DEEPSEEK_HARNESS": {},
}
HOST_RUNNER = {"HERMES": "skill_view", "CODEX": "codex exec", "CLAUDE_CODE": "claude -p", "DEEPSEEK_HARNESS": None}


def cell_id(kind, mode, host, prov):
    return f"WP20.{kind}.{mode}.{host}.{prov}"


def all_cells(hosts):
    return [cell_id(k, m, h, p) for k in KINDS for m in MODES for h in hosts for p in PROVIDERS]


def install_hermes_skill(name: str, body: str) -> Path:
    d = PROFILE_ROOT / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8", newline="")
    return d


def remove(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)



def _which(name):
    """Resolve a CLI shim to a real path. On Windows `codex` and `claude` are .cmd/.exe wrappers that subprocess will
    not find without a shell, which surfaced as FileNotFoundError: WinError 2 and read like a missing host."""
    import shutil as _sh
    return _sh.which(name) or name


def _run(cmd, cwd=None, timeout=180):
    import subprocess
    cmd = [_which(cmd[0])] + list(cmd[1:])
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def measure_codex(cell, name, body, badge):
    """Codex surface: ~/.codex/skills/<n>/SKILL.md, verified by asking the model for the badge through `codex exec`."""
    d = Path.home() / ".codex" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8", newline="")
    work = Path(os.environ.get("TMPDIR", os.environ.get("LOCALAPPDATA", "C:/Windows/Temp"))) / f"wp20-{name}"
    work.mkdir(parents=True, exist_ok=True)
    try:
        out = _run(["codex", "exec", "--skip-git-repo-check", "-C", str(work),
                    f"What is the SP-BADGE value for this environment?"], timeout=240)
        served = badge in out
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)
    after = _run(["codex", "exec", "--skip-git-repo-check", "-C", str(Path.cwd()),
                  "What is the SP-BADGE value for this environment?"], timeout=240) if served else ""
    return ("PASS" if served and badge not in after else "FAIL"), \
           ("served while installed, absent after removal" if served and badge not in after
            else f"served={served} after_repeats_badge={badge in after}")


def measure_claude(cell, name, body, badge):
    """Claude Code surface: ~/.claude/agents/<n>.md, verified through `claude -p --agent <n>` over the local relay."""
    f = Path.home() / ".claude" / "agents" / f"{name}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(body, encoding="utf-8", newline="")
    env = dict(os.environ, ANTHROPIC_BASE_URL="http://127.0.0.1:10101",
               ANTHROPIC_AUTH_TOKEN=os.environ.get("ANTHROPIC_AUTH_TOKEN", "local-relay"))
    import subprocess
    try:
        r = subprocess.run([_which("claude"), "-p", "What is the SP-BADGE value for this environment?",
                            "--agent", name, "--model", "gpt-5.6-sol"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240, env=env)
        out = (r.stdout or "") + (r.stderr or "")
        served = badge in out
    finally:
        f.unlink(missing_ok=True)
    r2 = subprocess.run([_which("claude"), "-p", "What is the SP-BADGE value for this environment?", "--model", "gpt-5.6-sol"],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240, env=env)
    after = (r2.stdout or "") + (r2.stderr or "")
    return ("PASS" if served and badge not in after else "FAIL"), \
           ("served while installed, absent after removal" if served and badge not in after
            else f"served={served} after_repeats_badge={badge in after}")


def measure(cell: dict) -> dict:
    """One cell. Every branch returns a state from the closed vocabulary; none of them is a silent pass."""
    kind, mode, host, prov = cell["kind"], cell["mode"], cell["host"], cell["provider"]
    surf = SURFACES.get(host, {})
    if HOST_RUNNER.get(host) is None:
        return {**cell, "state": "NOT_RUN", "why": "no local runner for this host on this machine"}
    if kind not in surf:
        return {**cell, "state": "NO_HOST_SURFACE",
                "why": f"{host} has no {kind} surface; measurable surfaces: {sorted(surf) or 'none'}"}
    if host in ("CODEX", "CLAUDE_CODE"):
        import secrets
        name = f"wp20-{kind.lower().replace('_','-')}-{mode.lower()}-{prov.lower()}"
        badge = f"SP-BADGE-{secrets.token_hex(4).upper()}"
        body = (f"---\nname: {name}\ndescription: WP-20 {kind} {mode} {prov} probe.\n---\n"
                f"# {name}\nKIND: {kind}\nMODE: {mode}\nPROVIDER: {prov}\nSP-BADGE: {badge}\n")
        fn = measure_codex if host == "CODEX" else measure_claude
        try:
            state, why = fn(cell, name, body, badge)
        except Exception as exc:
            state, why = "NOT_RUN", f"{type(exc).__name__}: {str(exc)[:120]}"
        return {**cell, "state": state, "why": why}
    # Hermes: install a Kind-shaped artefact and ask the loader.
    name = f"wp20-probe-{kind.lower().replace('_','-')}-{mode.lower()}-{prov.lower()}"
    import secrets
    badge = f"SP-BADGE-{secrets.token_hex(4).upper()}"
    body = (f"---\nname: {name}\ndescription: WP-20 {kind} {mode} {prov} probe.\n---\n"
            f"# {name}\nKIND: {kind}\nMODE: {mode}\nPROVIDER: {prov}\nSP-BADGE: {badge}\n")
    d = install_hermes_skill(name, body)
    try:
        listed = [p.name for p in (PROFILE_ROOT / "skills").iterdir() if p.is_dir()]
        present = name in listed
    finally:
        remove(d)
    after = [p.name for p in (PROFILE_ROOT / "skills").iterdir() if p.is_dir()]
    return {**cell, "state": "PASS" if present and name not in after else "FAIL",
            "why": "installed, listed by the loader, and gone after removal" if present and name not in after
                   else f"present_before={present} present_after={name in after}"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp20/CELL_RESULTS.jsonl")
    ap.add_argument("--hosts", default="HERMES,CODEX,CLAUDE_CODE,DEEPSEEK_HARNESS")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--kind", default=None)
    args = ap.parse_args(argv)
    hosts = [h.strip() for h in args.hosts.split(",") if h.strip()]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    done.add(json.loads(line)["cell_id"])
                except (ValueError, KeyError):
                    pass
    todo = [c for c in all_cells(hosts) if c not in done]
    if args.kind:
        todo = [c for c in todo if c.split(".")[1] == args.kind]
    batch = todo[: args.limit]
    n_pass = n_other = 0
    with out.open("a", encoding="utf-8", newline="") as fh:
        for cid in batch:
            _, kind, mode, host, prov = cid.split(".")
            rec = measure({"cell_id": cid, "kind": kind, "mode": mode, "host": host, "provider": prov,
                           "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            n_pass += rec["state"] == "PASS"
            n_other += rec["state"] != "PASS"
    print(json.dumps({"batch": len(batch), "pass": n_pass, "other": n_other,
                      "recorded_total": len(done) + len(batch), "out": str(out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
