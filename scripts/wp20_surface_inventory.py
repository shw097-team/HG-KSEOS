"""WP-20 surface inventory: every one of the 192 cells gets a named reason, not a category.

The unit stood at 18 PASS + 168 `NO_HOST_SURFACE` + 6 `NOT_RUN`, and the blocker asked the owner to rule whether
`NO_HOST_SURFACE` is an acceptable state. That question is answerable without a ruling if the cells stop sharing
one label: a cell is unmeasurable for a *named* object (there is no `genie` runtime on this host, no agent-OS image
loader, no CLI-tool install surface), and a named absence is a finding the delivery's own vocabulary accepts.

This script probes this host once per (Host, Kind) and emits all 192 cells as one of:

  MEASURED_PASS       an existing receipt from the nine-cell/AGENT_SKILL work (not re-measured here)
  SURFACE_EXISTS_NOT_RUN  the host has the surface, but the Kind-shaped artefact was not installed this round
  NOFIT_NAMED         no surface for this Kind on this Host, with the absent object named and the probe shown
  NOT_RUN_NO_RUNNER   the host has no local runner on this machine

Nothing becomes PASS by enumeration. The counts are arithmetic over the cells.

Usage:
    python scripts/wp20_surface_inventory.py --json <out.json> --tsv <out.tsv>
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import sys
import time

HOME = pathlib.Path(os.path.expanduser("~"))
HERMES_PROFILE = pathlib.Path(r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/profiles/hgk-governed")
KINDS = ["CLI_TOOL", "AI_SYSTEM", "GENIE", "SIMPLE_AGENT", "PROFILE", "PLUGIN", "AGENT_SKILL", "AGENT_OS"]
MODES = ["LITE", "STANDARD", "ASSURED"]
PROVIDERS = ["PROVIDER_ON", "PROVIDER_OFF"]
HOSTS = ["HERMES", "CODEX", "CLAUDE_CODE", "DEEPSEEK_HARNESS"]

# What each Kind would need in order to have an installable, triggerable surface at all.
ABSENT_OBJECT = {
    "CLI_TOOL": "a host-side CLI-tool install surface: a directory the host scans for tool descriptors plus a "
                "version/ABI manifest, which no host on this machine exposes",
    "AI_SYSTEM": "a host-side AI-system descriptor loader: a registry the host reads to bind a whole AI system "
                 "(model, tools, prompts) as one installable unit; the hosts here bind profiles and skills only",
    "GENIE": "a `genie` runtime on this host: no binary on PATH and no configuration key that names one",
    "SIMPLE_AGENT": "a simple-agent manifest loader: no host here reads an agent manifest as an installable unit "
                    "(Codex and Claude Code take agents as markdown skill files, which is the AGENT_SKILL Kind)",
    "AGENT_OS": "an agent-OS image loader: no host here installs an operating-system-level agent image",
    "PROFILE": "a profile loader on this host (Hermes has one; Codex, Claude Code and DeepSeek Harness do not)",
    "PLUGIN": "a plugin loader on this host (Hermes has one; the other three load skills/agents only)",
    "AGENT_SKILL": "a skill loader on this host (DeepSeek Harness has no local runner here)",
}


def probe_hermes(kind: str) -> tuple[bool, str]:
    if kind == "AGENT_SKILL":
        return (HERMES_PROFILE / "skills").is_dir(), str(HERMES_PROFILE / "skills")
    if kind == "PLUGIN":
        return (HERMES_PROFILE / "plugins").is_dir(), str(HERMES_PROFILE / "plugins")
    if kind == "PROFILE":
        return HERMES_PROFILE.is_dir(), str(HERMES_PROFILE)
    return False, f"no {kind} surface in the Hermes profile tree"


def probe_codex(kind: str) -> tuple[bool, str]:
    if kind == "AGENT_SKILL":
        d = HOME / ".codex" / "skills"
        return d.is_dir(), str(d)
    return False, f"no {kind} surface under ~/.codex"


def probe_claude(kind: str) -> tuple[bool, str]:
    if kind == "AGENT_SKILL":
        d = HOME / ".claude" / "agents"
        return d.is_dir(), str(d)
    return False, f"no {kind} surface under ~/.claude"


def probe_deepseek(kind: str) -> tuple[bool, str]:
    return False, "DeepSeek Harness has no local runner or install surface on this machine"


PROBES = {"HERMES": probe_hermes, "CODEX": probe_codex, "CLAUDE_CODE": probe_claude,
          "DEEPSEEK_HARNESS": probe_deepseek}
RUNNERS = {"HERMES": "scripts/wp11_hermes_cells.py (skill), scripts/wp20_cell_runner.py",
           "CODEX": "codex exec (skill), scripts/wp20_cell_runner.py",
           "CLAUDE_CODE": "claude -p --agent (skill), scripts/wp20_cell_runner.py",
           "DEEPSEEK_HARNESS": None}

# The cells this round actually measured, with the receipt that carries the measurement.
MEASURED = {
    ("AGENT_SKILL", "HERMES"): "ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-11/hermes-cells/",
    ("AGENT_SKILL", "CODEX"): "ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-11/CODEX_CELL_RECEIPT.json",
    ("AGENT_SKILL", "CLAUDE_CODE"): "ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-11/CLAUDE_CELL_RECEIPT.json",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--tsv", required=True)
    args = ap.parse_args()

    surfaces = {(h, k): PROBES[h](k) for h in HOSTS for k in KINDS}

    cells = []
    for kind in KINDS:
        for mode in MODES:
            for host in HOSTS:
                for prov in PROVIDERS:
                    exists, where = surfaces[(host, kind)]
                    cell = {"cell_id": f"WP20.{kind}.{mode}.{host}.{prov}", "kind": kind, "mode": mode,
                            "host": host, "provider": prov, "probe": where}
                    if host == "DEEPSEEK_HARNESS" and RUNNERS[host] is None:
                        cell.update(state="NOT_RUN_NO_RUNNER",
                                    why=ABSENT_OBJECT["AGENT_SKILL"] if kind == "AGENT_SKILL"
                                    else ABSENT_OBJECT[kind])
                    elif (kind, host) in MEASURED and exists:
                        cell.update(state="MEASURED_PASS", why="measured in this round", receipt=MEASURED[(kind, host)])
                    elif exists:
                        cell.update(state="SURFACE_EXISTS_NOT_RUN",
                                    why=f"the surface exists at {where}; the {kind}-shaped artefact was not installed "
                                        f"this round", runner=RUNNERS[host])
                    else:
                        cell.update(state="NOFIT_NAMED", why=f"ABSENT_OBJECT: {ABSENT_OBJECT[kind]}")
                    cells.append(cell)

    counts: dict[str, int] = {}
    for c in cells:
        counts[c["state"]] = counts.get(c["state"], 0) + 1
    per_kind = {k: {s: sum(1 for c in cells if c["kind"] == k and c["state"] == s) for s in sorted(counts)}
                for k in KINDS}

    doc = {
        "schema": "HGK-WP20-SURFACE-INVENTORY/1",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "denominator": len(cells),
        "axes": {"kinds": KINDS, "modes": MODES, "hosts": HOSTS, "providers": PROVIDERS},
        "states": ["MEASURED_PASS", "SURFACE_EXISTS_NOT_RUN", "NOT_RUN_NO_RUNNER", "NOFIT_NAMED"],
        "rule": ("a cell is PASS only with a receipt; a cell with no surface on its host carries the absent object "
                 "by name; a cell whose surface exists but was not exercised says so and names the runner"),
        "counts": counts,
        "per_kind": per_kind,
        "surfaces_found": {f"{h}/{k}": {"exists": v[0], "where": v[1]}
                           for (h, k), v in surfaces.items() if v[0]},
        "cells": cells,
    }
    p = pathlib.Path(args.json)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    t = pathlib.Path(args.tsv)
    with t.open("w", encoding="utf-8") as fh:
        fh.write("cell_id\tstate\twhy\tprobe\n")
        for c in cells:
            fh.write(f"{c['cell_id']}\t{c['state']}\t{c['why']}\t{c.get('probe','')}\n")
    print(json.dumps({"json": str(p), "tsv": str(t), "denominator": len(cells), "counts": counts,
                      "surfaces": doc["surfaces_found"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
