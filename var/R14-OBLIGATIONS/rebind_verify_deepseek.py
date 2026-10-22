"""Rebind VERIFY_SECURITY to opencode-go/deepseek-v4.1-flash in ONE movement.

Owner mandate (2026-10-22, third model plan): PLAN = openai-codex/gpt-6.1-sol, EXECUTE = opencode-go/minimax-m3.1-flash-free,
VERIFY/SECURITY = opencode-go/deepseek-v4.1-flash. The registry already matches the first two; only the checker lane differs.

Half a rebind is worse than none: registry, propagated assignment fields, the dispatch pool and the projection bindings all
have to move together, and the drift baseline has to describe the NEW intended state rather than the old residue. This
script applies all of them, runs the lane suites, and reverts everything if any suite fails - so the failure is a
measurement, not a half-applied state.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "config"
BACKUP = ROOT / "var" / "R14-OBLIGATIONS" / "rebind_backup_verify_deepseek"
TARGET_PLAN = ("openai-codex", "gpt-6.1-sol")
TARGET_EXEC = ("opencode-go", "minimax-m3.1-flash-free")
TARGET_VERIFY = ("opencode-go", "deepseek-v4.1-flash")
FILES = ["lane-routing-registry.yaml", "model-lane-assignment.json",
         "lane-route-slots.candidate.json", "hermes-codex-lane.json"]
TESTS = ["tests/test_lane_policy.py", "tests/test_lane_guard.py", "tests/test_lane_scope_isolation.py"]


def backup() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copyfile(CFG / name, BACKUP / name)


def restore() -> None:
    for name in FILES:
        shutil.copyfile(BACKUP / name, CFG / name)


def apply() -> dict:
    changes = []

    # 1) registry: the checker route, and the epoch that everything else is projected from
    registry_path = CFG / "lane-routing-registry.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    old_epoch = registry["epoch"]
    for route in registry["routes"]:
        if route["lane"] == "VERIFY_SECURITY":
            changes.append({"where": "registry.routes[VERIFY_SECURITY]",
                            "from": [route.get("provider"), route.get("model")],
                            "to": list(TARGET_VERIFY)})
            route["provider"], route["model"] = TARGET_VERIFY
            route["canonical_identity"] = TARGET_VERIFY[1]
            route["transport_model"] = f"{TARGET_VERIFY[0]}/{TARGET_VERIFY[1]}"
    registry["epoch"] = old_epoch + 1
    changes.append({"where": "registry.epoch", "from": old_epoch, "to": registry["epoch"]})

    # 2) propagated assignment: the VERIFY group and its chain arms
    assignment_path = CFG / "model-lane-assignment.json"
    assignment = json.loads(assignment_path.read_text(encoding="utf-8"))
    old_rev = assignment.get("revision")
    for group in assignment["assignment"]:
        if group.get("lane_group") == "VERIFY_SECURITY":
            changes.append({"where": "assignment.VERIFY_SECURITY",
                            "from": [group.get("assigned_provider"), group.get("assigned_model")],
                            "to": list(TARGET_VERIFY)})
            group["assigned_provider"], group["assigned_model"] = TARGET_VERIFY
            group["canonical_identity"] = TARGET_VERIFY[1]
            group["supply"] = "OpenCode Go"
            group["auth"] = "env_ref:OPENCODE_GO_API_KEY"
    chain = assignment.get("lane_chains", {}).get("VERIFY_SECURITY", [])
    for arm in chain:
        changes.append({"where": f"assignment.lane_chains.VERIFY_SECURITY[{arm.get('role')}]",
                        "from": [arm.get("provider"), arm.get("model")], "to": list(TARGET_VERIFY)})
        arm["provider"], arm["model"] = TARGET_VERIFY
        arm["transport_model"] = f"{TARGET_VERIFY[0]}/{TARGET_VERIFY[1]}"
    assignment["revision"] = (old_rev or 0) + 1
    assignment["registry_epoch"] = registry["epoch"]
    changes.append({"where": "assignment.registry_epoch", "from": old_epoch, "to": registry["epoch"]})

    # 3) projection bindings: the expected values are the new intended state, not the old residue
    for projection in registry.get("projections", []):
        if projection.get("id") != "model-lane-assignment":
            continue
        for binding in projection.get("bindings", []):
            pointer = binding["pointer"]
            if "VERIFY_SECURITY" in pointer or pointer.startswith("/sod/verify") or pointer.startswith("/assignment/2"):
                value = resolve(assignment, pointer)
                if value != binding.get("expected"):
                    changes.append({"where": f"binding {pointer}", "from": binding.get("expected"), "to": value})
                    binding["expected"] = value
        projection["registry_epoch"] = registry["epoch"]

    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=True), encoding="utf-8")
    assignment_path.write_text(json.dumps(assignment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 4) dispatch pool: the checker slot follows the checker
    pool_path = CFG / "lane-route-slots.candidate.json"
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    for slot in pool.get("slots", []):
        if slot.get("lane") == "VERIFY_SECURITY":
            changes.append({"where": f"pool.{slot.get('id', 'VERIFY_SECURITY')}",
                            "from": [slot.get("provider"), slot.get("model")], "to": list(TARGET_VERIFY)})
            slot["provider"], slot["model"] = TARGET_VERIFY
            slot["transport_model"] = f"{TARGET_VERIFY[0]}/{TARGET_VERIFY[1]}"
    pool["revision"] = (pool.get("revision") or 0) + 1
    pool_path.write_text(json.dumps(pool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"changes": changes}


def resolve(document, pointer: str):
    current = document
    for part in pointer.strip("/").split("/"):
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current[part]
    return current


def main() -> int:
    backup()
    try:
        result = apply()
    except Exception as exc:  # noqa: BLE001
        restore()
        print(json.dumps({"ok": False, "stage": "apply", "error": repr(exc)}, indent=2))
        return 1
    proc = subprocess.run([sys.executable, "-m", "pytest", *TESTS, "-q", "-p", "no:cacheprovider", "--no-header"],
                          cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8")
    ok = proc.returncode == 0
    if not ok:
        restore()
    payload = {"ok": ok, "changes": result["changes"], "pytest_exit": proc.returncode,
               "pytest_tail": (proc.stdout or proc.stderr or "")[-1500:],
               "reverted": not ok}
    out = ROOT / "var" / "R14-OBLIGATIONS" / "rebind_verify_deepseek.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": ok, "changes": len(result["changes"]), "reverted": not ok,
                      "pytest_exit": proc.returncode}, indent=2))
    if not ok:
        print(payload["pytest_tail"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
