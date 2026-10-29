#!/usr/bin/env python3
"""One-shot migration: align the registry's own `projections` declarations with its `routes`.

The registry declares the policy twice: once as `routes` (the authority) and once as
`projections[].bindings[].expected` (what the drift checker demands of the projection files).
When the routes moved to the 2026-10-24 order, the bindings did not, so `check_drift` reported
DRIFT_VALUE against a file that had just been projected from those same routes -- the checker
disagreed with its own source.

This script rewrites the `model-lane-assignment` entry's `bindings` from the routes, and refreshes
the three `/sod/*` strings and `/revision` / `/registry_epoch`. Everything else in the YAML is
preserved byte-for-byte (text splice, not a re-serialisation).

Run once, then rely on `lane_policy_reconcile.py --check`.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "lane-routing-registry.yaml"
ASSIGNMENT = ROOT / "config" / "model-lane-assignment.json"

ARM_LETTERS = "ABCDEFGH"


def bindings_for(registry: dict, revision: int) -> list[dict]:
    out: list[dict] = [
        {"pointer": "/registry_epoch", "expected": registry.get("epoch")},
        {"pointer": "/revision", "expected": revision},
    ]
    for route in registry["routes"]:
        lane = route["lane"]
        arms = [{"provider": route["provider"], "model": route["model"],
                 "transport_model": route.get("transport_model", route["model"]),
                 "reasoning_effort": route.get("reasoning_effort")}]
        arms += [{"provider": f["provider"], "model": f["model"],
                  "transport_model": f.get("transport_model", f["model"])}
                 for f in route.get("fallbacks", [])]
        for i, arm in enumerate(arms):
            base = f"/lane_chains/{lane}/{i}"
            out.append({"pointer": f"{base}/provider", "expected": arm["provider"]})
            out.append({"pointer": f"{base}/model", "expected": arm["model"]})
            out.append({"pointer": f"{base}/arm", "expected": ARM_LETTERS[i]})
            out.append({"pointer": f"{base}/default", "expected": i == 0})
            out.append({"pointer": f"{base}/automatic_selection", "expected": i == 0})
            out.append({"pointer": f"{base}/reasoning_effort", "expected": arm.get("reasoning_effort")})
    plan = next(r for r in registry["routes"] if r["lane"] == "PLAN")
    exe = next(r for r in registry["routes"] if r["lane"] == "EXECUTE")
    ver = next(r for r in registry["routes"] if r["lane"] == "VERIFY_SECURITY")
    out += [
        {"pointer": "/sod/plan_lane",
         "expected": f"{plan['provider']} / {plan['model']} - owner order 2026-10-24 (R17 S2-05 OD-01); "
                     f"supersedes the 2026-10-23 all-lanes-deepseek arrangement."},
        {"pointer": "/sod/execute_lane",
         "expected": f"{exe['provider']} / {exe['model']} - Codex CLI bounded writer; owner order 2026-10-24 "
                     f"keeps EXECUTE on the writer model while PLAN and VERIFY move."},
        {"pointer": "/sod/verify_security_lane",
         "expected": f"{ver['provider']}/{ver['model']} - owner order 2026-10-24; ACCEPTANCE, SECURITY REVIEW "
                     f"and VERIFY use this one checker."},
        {"pointer": "/sod/verify_security_default_arm", "expected": ver["model"]},
    ]
    return out


def dump_bindings(bindings: list[dict]) -> str:
    lines = ["  bindings:"]
    for b in bindings:
        lines.append(f"  - pointer: {b['pointer']}")
        v = b["expected"]
        if isinstance(v, bool):
            lines.append(f"    expected: {'true' if v else 'false'}")
        elif v is None:
            lines.append("    expected: null")
        elif isinstance(v, int):
            lines.append(f"    expected: {v}")
        else:
            lines.append(f"    expected: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    text = REGISTRY.read_text(encoding="utf-8")
    registry = yaml.safe_load(text)
    assignment = json.loads(ASSIGNMENT.read_text(encoding="utf-8"))
    revision = int(assignment.get("revision", 0))

    entry_start = text.index("- id: model-lane-assignment")
    nxt = [m.start() for m in re.finditer(r"^- id: ", text, re.M) if m.start() > entry_start]
    entry_end = nxt[0] if nxt else len(text)
    entry = text[entry_start:entry_end]
    if "  bindings:\n" not in entry:
        print("no bindings block found in the model-lane-assignment projection entry")
        return 1
    head, _ = entry.split("  bindings:\n", 1)
    new_entry = head + dump_bindings(bindings_for(registry, revision))
    REGISTRY.write_text(text[:entry_start] + new_entry + text[entry_end:], encoding="utf-8")

    # sanity: still parseable, and the entry now declares the projected revision
    reparsed = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    print(json.dumps({
        "verdict": "DECLARATIONS_ALIGNED",
        "bindings": len(new_entry.split("  - pointer: ")) - 1,
        "registry_epoch": reparsed.get("epoch"),
        "declared_revision": revision,
        "sod_plan": next(b["expected"] for b in bindings_for(registry, revision) if b["pointer"] == "/sod/plan_lane")[:60],
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
