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
        # The flat row names the arm the lane ACTUALLY auto-selects, not arms[0]: the registry's arm
        # order is a fallback ladder, so arms[0] is routinely a non-selected arm (measured 2026-10-29:
        # PLAN/VERIFY declare openai-codex/gpt-6.1-sol with automatic_selection on arms[1], yet this
        # projection wrote arms[0]'s opencode-go transport into the `assigned_model` gpt-6.1-sol row -
        # an identity/transport mismatch that every re-run of this script silently re-created).
        auto = next((a for a in route["arms"] if a.get("automatic_selection")), route["arms"][0])
        # R2: the oracle (projections[].bindings) also expects supply_selector / additional_routes /
        # reasoning_effort on these rows. Emit them from the registry's own arms so the projection
        # surface is never narrower than the expected surface again (measured 2026-10-29: 17 pointers
        # had no emitting code at all, which is what made check_drift fail closed).
        arms = route.get("arms", [])
        supply = {"arms": [{k: a.get(k) for k in ("provider", "model", "transport_model", "role",
                                                 "default", "automatic_selection")} for a in arms],
                  "unspecified_default": {"provider": auto.get("provider")}}
        extra = [{"provider": a.get("provider"), "model": a.get("model"),
                  "transport": ("codex-native-oauth" if a.get("provider") == "openai-codex" else a.get("transport")),
                  "automatic_selection": a.get("automatic_selection", False),
                  "default": a.get("default", False)}
                 for a in arms if a.get("provider") != route.get("provider")]
        row = {"role": role, "assigned_provider": route["provider"], "assigned_model": route["model"],
               "transport_model": auto.get("transport_model"), "authority": route.get("selection_authority"),
               "supply_selector": supply, "additional_routes": extra}
        if route.get("reasoning_effort"):
            row["reasoning_effort"] = route["reasoning_effort"]
        flat.append(row)
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
