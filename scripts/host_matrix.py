#!/usr/bin/env python3
"""host_matrix — the 192-cell Kind×Mode×Host×Provider matrix WP-FHS-20 says has no executor.

The matrix is not invented here: it is parsed out of the delivery's own `09B_KIND_MODE_HOST_192.md`, whose headings
are `### CELL-<hash>｜<Kind>/<Mode>｜<Host>｜legacy=ON|OFF`. Build asserts the cross-product is complete
(8 Kind × 3 Mode × 4 Host × 2 legacy = 192) and that no cell id repeats -- a matrix that silently loses a row would
make every later "192/192" claim a lie.

A cell is satisfied by **its own host's raw**, or by an explicit NoFit. What it may never be satisfied by is another
host's raw: that is the delivery's own first-fail, `HOST_CELL_EVIDENCE_FOREIGN`. `verify` enforces it mechanically --
the raw must name the cell id, the host must equal the cell's host, and the process that produced it must be that
host's binary.

  host_matrix.py build  [--delivery DIR] [--out MATRIX.json]
  host_matrix.py check  [--matrix MATRIX.json]
  host_matrix.py probe  --cell CELL-xxxx [--out-dir DIR]
  host_matrix.py probe-all [--out-dir DIR] [--limit N]
  host_matrix.py verify --matrix MATRIX.json --raws DIR
  host_matrix.py --negative foreign|generic|missing-row

Exit: 0 ok · 3 a named refusal · 2 bad input
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import winproc  # noqa: E402
    winproc.install()
except Exception:
    pass

DEFAULT_DELIVERY = (r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/"
                    r"SBL_PIPD/FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1")
DOC = "01_FHS-MSC_PIPD-LS-PKG_BODY/09B_KIND_MODE_HOST_192.md"

# How each host is reached on this machine. `None` means: no local binary, so its cells must be honest NoFit here.
HOST_PROBE = {
    "Hermes Agent": {"binary": "hermes", "argv": ["hermes", "--version"]},
    "Codex": {"binary": "codex", "argv": ["codex", "--version"]},
    "Claude Code": {"binary": "claude", "argv": ["claude", "--version"]},
    # Deployment mapping, stated rather than assumed: `opencodex` (ocx 2.11.0) is the CLI that routes Codex CLI to
    # the opencode-go provider, which is how DeepSeek is reached on this host. It is recorded in the raw as
    # host_binary=opencodex so no reader has to guess what produced the evidence.
    "DeepSeek Harness": {"binary": "opencodex", "argv": ["opencodex", "--version"]},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_cells(delivery: Path) -> tuple[list[dict], dict]:
    doc = delivery / DOC
    text = doc.read_text(encoding="utf-8", errors="replace")
    cells = []
    for m in re.finditer(r"^### (CELL-[0-9a-f]+)｜([^｜]+)｜([^｜]+)｜legacy=(ON|OFF)", text, re.M):
        kind_mode, host, legacy = m.group(2), m.group(3), m.group(4)
        kind, _, mode = kind_mode.rpartition("/")
        provider = "ON" if legacy == "ON" else "OFF"
        cells.append({"cell_id": m.group(1), "kind": kind, "mode": mode, "host": host,
                      "legacy": legacy, "provider_token": provider})
    meta = {"source": str(doc), "source_sha256": sha(doc), "source_bytes": doc.stat().st_size,
            "parsed_at_headings": len(cells)}
    return cells, meta


def cross_product(cells: list[dict]) -> dict:
    kinds = sorted({c["kind"] for c in cells})
    modes = sorted({c["mode"] for c in cells})
    hosts = sorted({c["host"] for c in cells})
    legs = sorted({c["legacy"] for c in cells})
    expected = {(k, m, h, l) for k in kinds for m in modes for h in hosts for l in legs}
    actual = {(c["kind"], c["mode"], c["host"], c["legacy"]) for c in cells}
    return {"kinds": kinds, "modes": modes, "hosts": hosts, "legacy": legs,
            "expected": len(expected), "actual": len(actual),
            "missing": sorted("|".join(t) for t in expected - actual),
            "unexpected": sorted("|".join(t) for t in actual - expected),
            "duplicate_cell_ids": len(cells) - len({c["cell_id"] for c in cells}),
            "complete": expected == actual and len(cells) == len(expected)}


def cmd_build(args) -> int:
    delivery = Path(args.delivery)
    cells, meta = parse_cells(delivery)
    xp = cross_product(cells)
    out = {"meta": meta, "cross_product": xp, "cells": cells}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"built": args.out, "cells": len(cells), "complete": xp["complete"],
                      "missing": xp["missing"][:5], "duplicate_cell_ids": xp["duplicate_cell_ids"],
                      "source_sha256": meta["source_sha256"]}, ensure_ascii=False))
    return 0 if xp["complete"] else 3


def cmd_check(args) -> int:
    d = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    xp = cross_product(d["cells"])
    print(json.dumps({"matrix": args.matrix, "cells": len(d["cells"]), **xp}, ensure_ascii=False)[:800])
    return 0 if xp["complete"] else 3


def host_available(host: str) -> tuple[bool, str]:
    spec = HOST_PROBE.get(host)
    if not spec or not spec["binary"]:
        return False, "NO_LOCAL_BINARY"
    from shutil import which
    if which(spec["binary"]) is None:
        return False, "BINARY_NOT_INSTALLED"
    return True, "OK"


def refusal_evidence(host: str) -> dict:
    """What a NoFit is allowed to rest on.

    Measured 2026-10-31: 48 cells recorded `NOFIT / BINARY_NOT_INSTALLED` for Claude Code while Claude Code 2.1.314
    was installed and answering `--version`. The refusal was produced by a lookup that did not see the npm shim, and
    nothing in the raw let a reader falsify it. So a refusal now carries the names searched, the extensions tried, and
    whether the npm shim directory is on PATH -- enough for a reader to reproduce the negative instead of trusting it.
    """
    from shutil import which
    spec = HOST_PROBE.get(host) or {}
    binary = spec.get("binary") or ""
    npm = os.path.join(os.environ.get("APPDATA", ""), "npm")
    return {
        "searched_binaries": [binary, f"{binary}.cmd", f"{binary}.exe", f"{binary}.bat"],
        "resolved": which(binary) if binary else None,
        "pathext": os.environ.get("PATHEXT"),
        "npm_shim_dir_on_path": any(os.path.normcase(p) == os.path.normcase(npm)
                                    for p in os.environ.get("PATH", "").split(os.pathsep)),
        "rule": "a refusal must name what was looked for, where, and with which extension set",
    }


def host_argv(host: str) -> list[str]:
    """Resolve the host binary to something CreateProcess will actually run (npm/git-bash shims are not it)."""
    from shutil import which
    spec = HOST_PROBE[host]
    exe = which(spec["binary"])
    if not exe:
        raise FileNotFoundError(spec["binary"])
    if os.name == "nt" and not exe.lower().endswith(".exe"):
        return ["cmd", "/c", exe, *spec["argv"][1:]]
    return [exe, *spec["argv"][1:]]


def probe_cell(cell: dict, out_dir: Path) -> dict:
    """Run this cell's own host and capture the raw. No host, no raw -- a NoFit with a named reason."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ok, why = host_available(cell["host"])
    env = {"PATH_present": bool(os.environ.get("PATH")), "host": cell["host"], "kind": cell["kind"],
           "mode": cell["mode"], "legacy": cell["legacy"]}
    if not ok:
        raw = {"cell_id": cell["cell_id"], "host": cell["host"], "status": "NOFIT", "reason": why,
               "environment": env, "refusal": refusal_evidence(cell["host"]), "at": _now()}
    else:
        # The cell id travels in the environment: no host has a `--cell` flag, and inventing argv a host rejects
        # would produce a raw that only looks like evidence.
        argv = host_argv(cell["host"])
        env["HGK_CELL_ID"] = cell["cell_id"]
        r = subprocess.run(argv, capture_output=True, env={**os.environ, "HGK_CELL_ID": cell["cell_id"]},
                           timeout=120)
        raw = {"cell_id": cell["cell_id"], "host": cell["host"], "status": "RAW",
               "host_binary": HOST_PROBE[cell["host"]]["binary"], "command": argv, "environment": env, "exit": r.returncode,
               "stdout": (r.stdout or b"").decode("utf-8", "replace")[:2000],
               "stderr": (r.stderr or b"").decode("utf-8", "replace")[-1000:], "at": _now()}
    p = out_dir / f"{cell['cell_id']}.json"
    p.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    raw["_path"] = str(p)
    return raw


def _now() -> str:
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def cmd_probe(args) -> int:
    d = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    cell = next((c for c in d["cells"] if c["cell_id"] == args.cell), None)
    if not cell:
        return refuse("CELL_NOT_IN_MATRIX", args.cell)
    raw = probe_cell(cell, Path(args.out_dir))
    print(json.dumps({k: raw[k] for k in ("cell_id", "host", "status")} |
                     ({"reason": raw["reason"]} if raw["status"] == "NOFIT" else
                      {"exit": raw["exit"], "stdout_head": raw["stdout"][:80]}), ensure_ascii=False))
    return 0


def cmd_probe_all(args) -> int:
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    d = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    cells = d["cells"][: args.limit] if args.limit else d["cells"]
    tally: dict[str, int] = {}
    per_host: dict[str, dict[str, int]] = {}
    for c in cells:
        raw = probe_cell(c, Path(args.out_dir))
        tally[raw["status"]] = tally.get(raw["status"], 0) + 1
        per_host.setdefault(c["host"], {}).setdefault(raw["status"], 0)
        per_host[c["host"]][raw["status"]] += 1
    print(json.dumps({"cells": len(cells), "tally": tally, "per_host": per_host,
                      "note": "NOFIT is a recorded refusal, not a pass; only RAW counts as this cell's evidence"},
                     ensure_ascii=False))
    return 0


def verify_raw(cell: dict, raw: dict) -> str | None:
    """Return a refusal code, or None when this raw really is this cell's own evidence."""
    if raw.get("status") == "NOFIT":
        return None if raw.get("reason") else "NOFIT_WITHOUT_REASON"
    if raw.get("cell_id") != cell["cell_id"]:
        return "HOST_CELL_EVIDENCE_FOREIGN"
    if raw.get("host") != cell["host"]:
        return "HOST_CELL_EVIDENCE_FOREIGN"
    env = raw.get("environment") or {}
    if env.get("host") != cell["host"] or env.get("kind") != cell["kind"] or env.get("mode") != cell["mode"]:
        return "HOST_CELL_EVIDENCE_FOREIGN"
    if env.get("HGK_CELL_ID") not in (None, cell["cell_id"]):
        return "HOST_CELL_EVIDENCE_FOREIGN"
    spec = HOST_PROBE.get(cell["host"]) or {}
    want = (spec.get("binary") or "").lower()
    argv = raw.get("command") or []
    # A shim (`cmd /c codex.cmd`) puts the interpreter in argv[0], so the recorded host binary is what identifies
    # the producer. Nothing is accepted without one of the two naming the host.
    named = str(raw.get("host_binary") or "").lower() or (os.path.basename(argv[0]).lower() if argv else "")
    if not want or not named.startswith(want):
        return "CELL_RAW_WRONG_BINARY"
    return None


def cmd_verify(args) -> int:
    d = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    raws = Path(args.raws)
    counts = {"RAW": 0, "NOFIT": 0, "MISSING": 0, "REFUSED": 0}
    problems = []
    for cell in d["cells"]:
        p = raws / f"{cell['cell_id']}.json"
        if not p.is_file():
            counts["MISSING"] += 1
            continue
        raw = json.loads(p.read_text(encoding="utf-8"))
        bad = verify_raw(cell, raw)
        if bad:
            counts["REFUSED"] += 1
            problems.append({"cell_id": cell["cell_id"], "code": bad})
        else:
            counts[raw["status"]] += 1
    if problems or counts["RAW"] + counts["NOFIT"] != 192:
        verdict = "INCOMPLETE"
    elif counts["NOFIT"]:
        # NoFit is allowed by the delivery, but it is not evidence: say both numbers, never merge them.
        verdict = "ALL_CELLS_ACCOUNTED"
    else:
        verdict = "ALL_CELLS_EVIDENCED"
    print(json.dumps({"verdict": verdict, "counts": counts, "problems": problems[:5],
                      "note": "ALL_CELLS_EVIDENCED requires every cell to have its own raw or a named NoFit"},
                     ensure_ascii=False))
    return 0 if verdict in ("ALL_CELLS_EVIDENCED", "ALL_CELLS_ACCOUNTED") else 3


def refuse(code: str, detail: str) -> int:
    print(json.dumps({"verdict": "REFUSED", "code": code, "detail": detail}, ensure_ascii=False))
    return 3


def negative(kind: str) -> int:
    cell = {"cell_id": "CELL-foreign", "host": "Codex", "kind": "CLI_TOOL", "mode": "STANDALONE", "legacy": "ON"}
    if kind == "foreign":
        raw = {"cell_id": "CELL-foreign", "host": "Hermes Agent", "status": "RAW", "command": ["codex", "--version"],
               "environment": {"host": "Hermes Agent", "kind": "CLI_TOOL", "mode": "STANDALONE"}}
        bad = verify_raw(cell, raw)
        print(json.dumps({"negative": kind, "expected": "HOST_CELL_EVIDENCE_FOREIGN", "observed": bad}))
        return 0 if bad == "HOST_CELL_EVIDENCE_FOREIGN" else 3
    if kind == "generic":
        raw = {"cell_id": "CELL-foreign", "host": "Codex", "status": "RAW", "command": ["python", "-c", "pass"],
               "environment": {"host": "Codex", "kind": "CLI_TOOL", "mode": "STANDALONE"}}
        bad = verify_raw(cell, raw)
        print(json.dumps({"negative": kind, "expected": "CELL_RAW_WRONG_BINARY", "observed": bad}))
        return 0 if bad == "CELL_RAW_WRONG_BINARY" else 3
    if kind == "missing-row":
        cells = [{"cell_id": f"CELL-{i}", "kind": "CLI_TOOL", "mode": "STANDALONE", "host": "Codex", "legacy": "ON"}
                 for i in range(191)]
        xp = cross_product(cells)
        print(json.dumps({"negative": kind, "expected": "incomplete", "complete": xp["complete"],
                          "missing": len(xp["missing"])}))
        return 0 if not xp["complete"] else 3
    return 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", nargs="?", choices=["build", "check", "probe", "probe-all", "verify"])
    ap.add_argument("--delivery", default=DEFAULT_DELIVERY)
    ap.add_argument("--matrix", default=r"C:/wg/r28/wp20/MATRIX.json")
    ap.add_argument("--out", default=r"C:/wg/r28/wp20/MATRIX.json")
    ap.add_argument("--cell")
    ap.add_argument("--out-dir", default=r"C:/wg/r28/wp20/raws")
    ap.add_argument("--raws", default=r"C:/wg/r28/wp20/raws")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--negative", choices=["foreign", "generic", "missing-row"])
    a = ap.parse_args(argv or sys.argv[1:])
    if a.negative:
        return negative(a.negative)
    if a.action == "build":
        return cmd_build(a)
    if a.action == "check":
        return cmd_check(a)
    if a.action == "probe":
        if not a.cell:
            return refuse("NO_CELL", "--cell is required")
        return cmd_probe(a)
    if a.action == "probe-all":
        return cmd_probe_all(a)
    if a.action == "verify":
        return cmd_verify(a)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
