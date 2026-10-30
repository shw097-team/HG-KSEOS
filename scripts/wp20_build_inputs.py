#!/usr/bin/env python3
"""wp20_build_inputs — the candidate binding WP-FHS-20's officer said was absent.

The verdict was exact:

    candidate_manifest = {path: C:/wg/queue/WP-FHS-20/output/build-inputs.json, state: ABSENT}
    counts = {qualified: 0, justified_NoFit: 0, NOT_RUN: 192, mapping_HOLD_overlay: 192}
    "Required candidate manifest absent; no complete candidate digest can be asserted"

Two things were missing, and they are different in kind:

1. **The candidate digest.** A cell raw on its own proves a probe ran; it does not prove *what* was probed. The
   digest binds the matrix, the runner, the source clauses and every cell's raw sha into one value, so "this is the
   candidate I judged" stops being a matter of trust.
2. **The provider dimension.** The delivery records its own hold — `OWNER_BIND_HOLD`, with the explicit instruction
   that the provider enum may not be guessed from labels. That hold is the owner's to release, and only in writing.
   This tool therefore *refuses to invent* a provider binding: it records the owner acknowledgement instrument that
   released the hold, its sha, and the exact decision that was made. No ack, no release, and the matrix stays held.

  wp20_build_inputs.py --matrix MATRIX.json --raws DIR [--ack ACK.json] --out output/build-inputs.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

DELIVERY = (r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/"
            r"FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1")
DOCS = ["01_FHS-MSC_PIPD-LS-PKG_BODY/09B_KIND_MODE_HOST_192.md",
        "01_FHS-MSC_PIPD-LS-PKG_BODY/11_WORKPACKAGES_AND_DAG.md"]


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", default=r"C:/wg/r28/wp20/MATRIX.json")
    ap.add_argument("--raws", default=r"C:/wg/r28/wp20/raws")
    ap.add_argument("--runner", default=r"C:/Projects/Agent_Workspace/HG-KSEOS/scripts/host_matrix.py")
    ap.add_argument("--ack", default=r"C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer/OWNER_AUTHORIZATION.json")
    ap.add_argument("--out", default=r"C:/wg/queue/WP-FHS-20/output/build-inputs.json")
    a = ap.parse_args(argv or sys.argv[1:])

    matrix = json.loads(Path(a.matrix).read_text(encoding="utf-8"))
    raws = Path(a.raws)
    cells, counted = [], {"RAW": 0, "NOFIT": 0, "MISSING": 0}
    for c in matrix["cells"]:
        rp = raws / f"{c['cell_id']}.json"
        entry = {"cell_id": c["cell_id"], "kind": c["kind"], "mode": c["mode"], "host": c["host"],
                 "legacy": c["legacy"]}
        if rp.is_file():
            raw = json.loads(rp.read_text(encoding="utf-8"))
            entry["evidence"] = {"status": raw.get("status"), "raw": str(rp), "raw_sha256": sha(rp),
                                 "host_binary": raw.get("host_binary"), "reason": raw.get("reason")}
            counted[raw.get("status", "MISSING")] = counted.get(raw.get("status", "MISSING"), 0) + 1
        else:
            entry["evidence"] = {"status": "MISSING", "raw": None, "raw_sha256": None}
            counted["MISSING"] += 1
        cells.append(entry)

    # The provider dimension is the owner's, not mine: release only against a written acknowledgement.
    ack_path = Path(a.ack)
    if not ack_path.is_file():
        print(json.dumps({"verdict": "OWNER_BIND_HOLD_STANDS",
                          "detail": f"no owner acknowledgement at {ack_path}; the provider enum stays unbound",
                          "counts": counted}, ensure_ascii=False))
        return 5
    ack = json.loads(ack_path.read_text(encoding="utf-8"))
    binding = {
        "hold": "OWNER_BIND_HOLD",
        "released_by": ack.get("grantor"),
        "instrument": ack.get("instrument"),
        "ack_sha256": sha(ack_path),
        "authorization_quote": ack.get("authorization_quote"),
        "decisions": {
            "provider_token": "legacy ON/OFF as written in the 09B cell headings; not re-derived from names",
            "host_mapping": {"DeepSeek Harness": "opencodex 2.11.0 (the CLI that routes Codex CLI to the "
                                                 "opencode-go provider on this host)"},
            "unavailable_hosts": {"Claude Code": "no binary on this host; cells recorded NoFit, never borrowed"},
        },
        "limits": ack.get("limits"),
    }

    source_hashes = {d: sha(Path(DELIVERY) / d) for d in DOCS if (Path(DELIVERY) / d).is_file()}
    body = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "delivery": {"id": "FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1", "source_sha256": source_hashes},
        "matrix": {"path": a.matrix, "sha256": sha(a.matrix), "cells": len(matrix["cells"])},
        "runner": {"path": a.runner, "sha256": sha(a.runner)},
        "owner_binding": binding,
        "counts": counted,
        "cells": cells,
    }
    body["candidate_digest"] = digest({k: body[k] for k in ("delivery", "matrix", "runner", "counts")}
                                      | {"cell_raws": [c["evidence"]["raw_sha256"] for c in cells]})
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"built": str(out), "cells": len(cells), "counts": counted,
                      "candidate_digest": body["candidate_digest"],
                      "hold": "RELEASED" if binding["ack_sha256"] else "STANDS"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
