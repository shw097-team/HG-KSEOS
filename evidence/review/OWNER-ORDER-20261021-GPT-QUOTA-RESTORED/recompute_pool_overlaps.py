#!/usr/bin/env python
"""Recompute the pool's `identity_overlaps_recorded_not_enforced` from the pool itself.

WHY: the field is a RECORD of which model identities occupy more than one lane.
After the owner order of 2026-10-21 (GPT quota restored) the record still named
the OLD arrangement (deepseek at rank 1 on EXECUTE/VERIFY, gpt-6.1-sol at PLAN
rank 3), which is no longer true. A stale overlap record is worse than none: it
tells a reviewer that a collision is absent when it is present, and vice versa.

The list is DERIVED, not hand-written: for every (provider, model) that appears
in more than one lane, the record names the lanes and the ranks. A hand-written
list drifts the moment the pool is re-bound; a derived one cannot.

Also records the ONE collision that is in force under the current owner order:
PLAN and VERIFY_SECURITY share gpt-6.1-sol BY OWNER ORDER (SOD006-C4,
OPEN_OWNER_ORDERED) -- process separation only, model independence not claimed.

Read-only derivation + a guarded write: the file's pre-image digest is checked
immediately before the write.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
POOL = HGK / "config" / "lane-route-slots.candidate.json"

OWNER_ORDERED_SHARED = {
    ("openai-codex", "gpt-6.1-sol"): (
        "BY OWNER ORDER (2026-10-21, GPT quota restored): the PLAN lane and the "
        "Independent Acceptance Officer / VERIFY / SECURITY checker lane are BOTH "
        "openai-codex/gpt-6.1-sol. The collision is REAL and is declared "
        "SOD006-C4 (OPEN_OWNER_ORDERED); independence for this pair is PROCESS, LANE "
        "and EVIDENCE-PATH separation only, and model independence is NOT claimed. "
        "The EXECUTE writer is on a DIFFERENT model (opencode-go/deepseek-v4.1-flash), "
        "so the maker/checker separation holds on the model axis."
    ),
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    raw = POOL.read_bytes()
    pre = sha256_bytes(raw)
    print("pool pre-image sha256:", pre)

    pool = json.loads(raw.decode("utf-8"))
    occ = defaultdict(list)
    for lane in pool["lanes"]:
        for e in lane["ordered_pool"]:
            occ[(e.get("provider"), e.get("model"))].append((lane.get("lane"), e.get("rank")))

    lines = []
    for (prov, model), places in sorted(occ.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        lane_names = sorted({l for l, _ in places})
        if len(lane_names) < 2:
            continue
        detail = ", ".join(f"{l} rank {r}" for l, r in sorted(places, key=lambda x: (x[0], x[1])))
        line = f"{prov}/{model} appears at {detail} - the same identity can occupy all three lanes"
        lines.append(line)
        note = OWNER_ORDERED_SHARED.get((prov, model))
        if note:
            lines.append(f"{prov}/{model}: {note}")
            print("  shared-BY-OWNER-ORDER:", prov, model)
    pool["identity_overlaps_recorded_not_enforced"] = lines
    print(f"\nderived {len(lines)} overlap record lines:")
    for l in lines:
        print("  -", l[:150])

    out = json.dumps(pool, indent=2, ensure_ascii=False) + "\n"
    if sha256_bytes(POOL.read_bytes()) != pre:
        print("REFUSE: the pool moved since the freeze. Aborting.")
        return 2
    POOL.write_text(out, encoding="utf-8", newline="\n")
    print(f"\npool post-image sha256: {sha256_bytes(POOL.read_bytes())}")

    import sys
    sys.path.insert(0, str(HGK / "src"))
    from hg_kseos import lane_policy as lp
    findings = lp.check_drift()
    print(f"drift gate: {len(findings)} findings, fatal={lp.drift_is_fatal(findings)}")
    for f in findings[:10]:
        print("  ", f.get("severity"), f.get("code"), f.get("path"), f.get("pointer"))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
