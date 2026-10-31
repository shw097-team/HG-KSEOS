#!/usr/bin/env python3
"""Generate the WP-FHS-20 cell registry from the delivery's own enumerations.

MEASURED 2026-10-31: the blocker on WP-FHS-20 was `KIND_ENUM_UNREAD` -- nobody had extracted the eight Kinds, so no
cell could be named. They are in the delivery, as `ProductKind=<NAME>`:

    CLI_TOOL  AI_SYSTEM  GENIE  SIMPLE_AGENT  PROFILE  PLUGIN  AGENT_SKILL  AGENT_OS      (8)

The axes are 8 Kind x 3 Mode (LITE / STANDARD / ASSURED) x 4 Host x 2 Provider = 192.

The host set is NOT settled and this generator refuses to pretend it is. The delivery carries two enumerations:

    01_PRODUCT_AUTHORITY_SPINE:  "四 Host：Hermes Agent、Codex、Claude Code、ChatGPT；前 3 的 CLI/Skill/Plugin
                                 能力各以真 Loader/Process/Security..."
    BODY-09B (as read in the R2 test order): the four hosts are Hermes, Codex, Claude Code, DeepSeek Harness,
                                 with an explicit instruction not to rewrite the denominator on the ChatGPT basis.

Arithmetic note: 8 x 3 x 2 = 48, and the delivery also says "四 Host 衝突的完整受影遷移候選（48/48）" -- so 48 is
exactly one host's slice. Whether that slice is ChatGPT or DeepSeek Harness changes which 48 cells are the conflicted
ones, but not the total. This file therefore emits all 192 with the host set recorded as a parameter and a
`host_set_conflict` block, so no cell silently inherits a guess.

Every cell is emitted with state NOT_MEASURED. A cell is never PASS because it was enumerated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

KINDS = ["CLI_TOOL", "AI_SYSTEM", "GENIE", "SIMPLE_AGENT", "PROFILE", "PLUGIN", "AGENT_SKILL", "AGENT_OS"]
MODES = ["LITE", "STANDARD", "ASSURED"]
PROVIDERS = ["PROVIDER_ON", "PROVIDER_OFF"]

# RESOLVED 2026-11-01 from the delivery itself, not by ruling: 09B's R2 section carries 48 `PROPOSAL-CHATGPT-*` entries
# whose source identity is `CELL-<sha>` / `DeepSeek Harness` and whose text says, in each one, "本 ID 尚非 Original 192
# Cell" with exit condition "CR-HOST-192 下 MIGRATION_HOLD". Measured: 48 proposals, 48 MIGRATION_HOLD, 48 source
# identities all DeepSeek Harness.
#
# So the Original 192 are Hermes / Codex / Claude Code / DeepSeek Harness, and ChatGPT is not a fourth host of the
# Original matrix at all -- it is a set of HELD MIGRATION PROPOSALS against 48 of the DeepSeek cells. The "four host
# conflict" was a proposal read as a substitution. D-A's 144 was wrong for that reason: those 48 cells are admitted
# (they are DeepSeek Harness); it is the ChatGPT proposal for them that is held.
HOST_SETS = {
    "ORIGINAL_192": ["HERMES", "CODEX", "CLAUDE_CODE", "DEEPSEEK_HARNESS"],
    "09A_SPINE_READING": ["HERMES", "CODEX", "CLAUDE_CODE", "CHATGPT"],
}
HELD_PROPOSALS = {"kind": "PROPOSAL-CHATGPT", "count": 48, "state": "MIGRATION_HOLD",
                  "source_host": "DEEPSEEK_HARNESS", "overwrites_original_cell_id": False}


def build(host_set: str) -> dict:
    hosts = HOST_SETS[host_set]
    cells = []
    for kind in KINDS:
        for mode in MODES:
            for host in hosts:
                for prov in PROVIDERS:
                    cells.append({
                        "cell_id": f"WP20.{kind}.{mode}.{host}.{prov}",
                        "kind": kind, "mode": mode, "host": host, "provider": prov,
                        "state": "NOT_MEASURED",
                        "evidence_ref": None,
                        "note": ("host is not admitted by the delivery for local runner/CLI/repo install; cannot be "
                                 "measured natively until the host set is ruled on"
                                 if host == "CHATGPT" else ""),
                    })
    return {
        "schema": "SBL-WP20-CELL-REGISTRY/1",
        "wp": "WP-FHS-20",
        "generated_from": "ProductKind=* in /c/wg/pkg (8 distinct values), MODES from profiles.py, hosts from the delivery",
        "axes": {"kind": KINDS, "mode": MODES, "host": hosts, "provider": PROVIDERS},
        "host_set": host_set,
        "counts": {"total": len(cells),
                   "by_kind": {k: sum(1 for c in cells if c["kind"] == k) for k in KINDS},
                   "measured": 0, "not_measured": len(cells)},
        "host_set_resolution": {
            "settled_by": "the delivery's own text, not by a ruling",
            "original_hosts": HOST_SETS["ORIGINAL_192"],
            "held_proposals": HELD_PROPOSALS,
            "why": "each of the 48 PROPOSAL-CHATGPT entries names its source identity as DeepSeek Harness, states it is "
                   "not yet an Original 192 Cell, and exits under MIGRATION_HOLD without overwriting the original CellID",
            "d_a_status": "WITHDRAWN -- it cut the denominator to 144 by treating admitted DeepSeek cells as excluded",
        },
        "cells": cells,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host-set", choices=sorted(HOST_SETS), default="ORIGINAL_192")
    ap.add_argument("--out", default=r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp20/CELL_REGISTRY.json")
    args = ap.parse_args(argv)
    reg = build(args.host_set)
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps({"out": str(p), "host_set": reg["host_set"], "counts": reg["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
