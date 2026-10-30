#!/usr/bin/env python3
"""policy_loaded_consumer_ack — WP-FHS-02's PolicyLoadedConsumerACK, measured instead of asserted.

The delivery's Done for WP-FHS-02 is one sentence: **Source / Stage / Approve / Active / Loaded / Consumer
each hash the same scope**, and the evidence must be read back **by the original consumer**, not by me.

So this tool does three things and nothing else:
  1. hash each of the six layers where that layer actually lives on this host (and say ABSENT if it does not);
  2. ask the real Fabric consumer (`load_router`, `route_event`) for the readback, and record its raw output;
  3. write one ACK that states the scope once and binds every layer to it.

It does not decide PASS. A layer with no object is recorded ABSENT and the ACK says so.

Usage: policy_loaded_consumer_ack.py --out <file.json> [--fabric-root DIR] [--hk-root DIR]
Exit 0 = ACK written. Exit 2 = a layer could not be measured (the ACK still written, with the reason).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

DEFAULT_FABRIC = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\FABRIC")
DEFAULT_HK = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
# The change classes are whatever the loaded router declares. Guessing them (the first version used
# CONFIG_ONLY/CODE_ONLY/...) produced five FAIL_CLOSED "UNKNOWN_CHANGE_CLASS" answers and a readback that
# looked like a policy failure when it was my list that was wrong.
CHANGE_CLASSES: tuple[str, ...] = ()


def sha256(path: pathlib.Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def layer(name: str, plane: str, path: pathlib.Path | None, note: str) -> dict:
    if path is None:
        return {"layer": name, "plane": plane, "state": "ABSENT", "note": note}
    digest = sha256(path)
    return {"layer": name, "plane": plane,
            "state": "PRESENT" if digest else "ABSENT",
            "path": str(path), "sha256": digest, "note": note}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--fabric-root", default=str(DEFAULT_FABRIC))
    ap.add_argument("--hk-root", default=str(DEFAULT_HK))
    args = ap.parse_args()

    fabric = pathlib.Path(args.fabric_root)
    hk = pathlib.Path(args.hk_root)
    layers: list[dict] = []
    problems: list[str] = []

    router = fabric / "rp002" / "RP002_CHANGE_CLASS_ROUTER.yaml"
    layers.append(layer("source", "Fabric", router, "the policy source the consumer reads"))

    # A staged artefact is only a layer if the governance tree actually stages one for this policy.
    staged = fabric / "stage" / "RP002-STAGE-HGK" / "RP002_CHANGE_CLASS_ROUTER.staged.yaml"
    layers.append(layer("stage", "Fabric", staged if staged.exists() else None,
                        "no staged copy exists for this policy on this host"))

    approve = fabric / "rp002" / "FROZEN_ACCEPTANCE_ORACLE.yaml"
    layers.append(layer("approve", "Fabric", approve, "the frozen acceptance oracle that approves the class routes"))

    # Active: Fabric holds no policy-epoch object (measured 2026-10-30: 40 hits for policy_epoch/IN_FORCE,
    # all inside evidence/). The in-force declaration lives in the control plane, so the layer is recorded
    # with its real plane rather than invented on the Fabric side.
    registry = hk / "config" / "lane-routing-registry.yaml"
    active = layer("active", "HG-KSEOS", registry,
                   "Fabric has no policy-epoch object; the in-force epoch declaration is the control plane's")
    if active["state"] == "PRESENT":
        try:
            text = registry.read_text(encoding="utf-8", errors="replace")
            active["contract_epoch"] = next(
                (line.split(":", 1)[1].strip() for line in text.splitlines()
                 if line.strip().startswith("contract_epoch:")), None)
            active["status"] = next(
                (line.split(":", 1)[1].strip() for line in text.splitlines()
                 if line.strip().startswith("status:")), None)
        except OSError as exc:
            problems.append(f"active_unreadable: {exc}")
    layers.append(active)

    # Loaded and Consumer come from the real consumer, run here and now.
    sys.path.insert(0, str(fabric))
    loaded: dict = {"layer": "loaded", "plane": "Fabric consumer", "state": "ABSENT"}
    consumer: dict = {"layer": "consumer", "plane": "Fabric consumer", "state": "ABSENT"}
    try:
        from fabric.consumers import hgk_policy_consumer as hpc  # type: ignore

        router_classes = hpc.load_router()
        loaded = {"layer": "loaded", "plane": "Fabric consumer", "state": "PRESENT",
                  "module": str(pathlib.Path(hpc.__file__).resolve()),
                  "module_sha256": sha256(pathlib.Path(hpc.__file__).resolve()),
                  "policy_file_read": str((hpc.FAB / "rp002" / "RP002_CHANGE_CLASS_ROUTER.yaml").resolve()),
                  "policy_sha256": sha256(hpc.FAB / "rp002" / "RP002_CHANGE_CLASS_ROUTER.yaml"),
                  "classes_loaded": sorted(router_classes),
                  "classes_count": len(router_classes)}
        classes = tuple(sorted(router_classes))
        results = {c: hpc.route_event(c) for c in classes}
        results["__unknown_class__"] = hpc.route_event("NOT_A_CLASS")
        consumer = {"layer": "consumer", "plane": "Fabric consumer", "state": "PRESENT",
                    "route_readback": results,
                    "all_route_ok": all(results[c]["verdict"] == "ROUTE_OK" for c in classes),
                    "unknown_class_fails_closed": results["__unknown_class__"]["verdict"] == "FAIL_CLOSED"}
    except Exception as exc:  # noqa: BLE001 - a broken consumer is a finding, not a crash
        problems.append(f"consumer_error: {type(exc).__name__}: {exc}")
    layers.append(loaded)
    layers.append(consumer)

    scope = {
        "subject": "FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1/WP-FHS-02",
        "source_sha256": layers[0].get("sha256"),
        "candidate_sha256": layers[4].get("module_sha256"),
        "policy_epoch": layers[3].get("contract_epoch"),
        "policy_status": layers[3].get("status"),
    }
    absent = [x["layer"] for x in layers if x["state"] != "PRESENT"]
    ack = {
        "schema": "POLICY-LOADED-CONSUMER-ACK/1",
        "work_package": "WP-FHS-02",
        "scope": scope,
        "layers": layers,
        "layers_present": [x["layer"] for x in layers if x["state"] == "PRESENT"],
        "layers_absent": absent,
        "problems": problems,
        "verdict_inputs": {
            "all_six_present": not absent,
            "consumer_readback_by_the_original_consumer": consumer.get("all_route_ok") is True,
            "unknown_class_fails_closed": consumer.get("unknown_class_fails_closed") is True,
        },
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ack": str(out), "present": ack["layers_present"], "absent": absent,
                      "inputs": ack["verdict_inputs"], "problems": problems}, ensure_ascii=False))
    return 0 if not problems else 2


if __name__ == "__main__":
    raise SystemExit(main())
