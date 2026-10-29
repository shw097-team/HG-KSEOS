"""Re-derive config/model-lane-assignment.json's wiring from the lane registry, instead of restating it by hand.

Measured defect (R14, 44 field-path inconsistencies): the assignment file declared PLAN on gpt-6.1-sol but carried
transport_model opencode-go/minimax-m3.1-flash-free - i.e. it would have SENT MiniMax while DECLARING GPT. EXECUTE had
the same swap one step over (declared minimax, transport deepseek; the auto-selected entry was the deepseek arm), and
VERIFY_SECURITY auto-selected the MiniMax arm even though the owner order puts VERIFY/SECURITY on GPT. Because
check_drift() compares against values that were themselves pinned from the drifted file, it reported [] throughout.

This script makes the assignment a projection of the registry, which is the authority for lane -> provider/model.
"""
from __future__ import annotations
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "config/lane-routing-registry.yaml"
ASG = ROOT / "config/model-lane-assignment.json"
ROLES = ("PLAN", "EXECUTE", "VERIFY_SECURITY")


def main(apply: bool) -> int:
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    by_lane = {r["lane"]: r for r in reg["routes"]}
    doc = json.loads(ASG.read_text(encoding="utf-8"))
    changes = []
    for role in ROLES:
        route = by_lane[role]
        arms = route["arms"]
        chain = doc["lane_chains"][role]
        for i, arm in enumerate(arms[: len(chain)]):
            for field, want in (("provider", arm["provider"]), ("model", arm["model"]),
                                ("transport_model", arm.get("transport_model")),
                                ("automatic_selection", bool(arm.get("automatic_selection")))):
                have = chain[i].get(field)
                if have != want:
                    changes.append({"role": role, "index": i, "field": field, "was": have, "now": want})
                    chain[i][field] = want
    # the flat `assignment` list: name the role explicitly instead of leaving it null and relying on order
    flat = []
    for role in ROLES:
        route = by_lane[role]
        flat.append({"role": role, "assigned_provider": route["provider"], "assigned_model": route["model"],
                     "transport_model": route["arms"][0].get("transport_model"),
                     "authority": route.get("selection_authority")})
    if doc.get("assignment") != flat:
        changes.append({"role": "*", "field": "assignment", "was": len(doc.get("assignment", [])), "now": len(flat)})
        doc["assignment"] = flat
    if changes:
        doc["revision"] = int(doc.get("revision", 0)) + 1
        doc["revision_27_reason"] = (
            "Re-derived from config/lane-routing-registry.yaml after measurement found the assignment restating the "
            "wiring incorrectly: PLAN declared gpt-6.1-sol with a MiniMax transport, EXECUTE's auto-selected entry was "
            "the deepseek arm with a MiniMax transport, and VERIFY_SECURITY auto-selected MiniMax. The registry already "
            "matched the owner order, so the assignment is now a projection of it rather than a second copy of it.")
    if apply and changes:
        ASG.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"changes": len(changes), "detail": changes[:12], "applied": bool(apply and changes)},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main("--apply" in sys.argv))
