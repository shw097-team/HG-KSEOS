"""R18 governed admission: project + 22 WP requirements + typed refusal probe.

Registers the FHS-MSC revision2 round in the canonical Shared Spine, freezes one
requirement per WP-FHS-00..21 from the package's own typed DAG, and then ATTEMPTS a
native taskspec admission to prove the Issuer gate actually fires (a gate that cannot
be shown to refuse is not a gate).
"""
import json
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
sys.path.insert(0, str(ROOT / "src"))

from hg_kseos.spine import SharedSpine  # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest  # noqa: E402

DB = ROOT / "var" / "shared-spine" / "hg-kseos.db"
PKG_REL = ("知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/FHS-MSC/"
           "FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE/"
           "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2")
SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject")
OUT = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\receipts\ADMISSION_R18.json")
PID = "FHS-MSC-R18-20261029"

dag = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "wp_graph.json").read_text(encoding="utf-8"))
nodes = {n["id"]: n for n in dag["nodes"]}

receipt = {"schema": "R18.FHS.ADMISSION/1", "project_id": PID, "steps": []}

spine = SharedSpine(DB)
ctl = ProjectLifecycleController(spine)

goal = ("FHS-MSC Skeleton+Spine revision2: execute the existing WP-FHS-00..21 typed DAG "
        "(wiring, necessary implementation, FAR research, tests, bounded repair, regression, "
        "independent acceptance, delivery) for source "
        "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2")
request = ProjectRequest(
    goal=goal,
    source_paths=[str(Path(r"C:\Projects\Agent_Workspace") / PKG_REL)],
    constraints=[
        "source bytes are read-only; all work happens in var/R18-FHS-SKELETON-SPINE-20261029",
        "L2/L3/L4 effects require a native Issuer PERMIT bound to this exact request",
        "no self-acceptance: maker and checker are different principals",
        "candidate-only; no main merge, no tag, no release",
    ],
    non_goals=["Full Product 949", "TECH 386 installation", "MVS10 remote delivery",
               "B1 re-derivation"],
    target_root=r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029",
)

try:
    start = ctl.start(request, project_id=PID)
    receipt["steps"].append({"step": "lifecycle.start", "ok": True, "result": start})
except Exception as exc:  # noqa: BLE001
    receipt["steps"].append({"step": "lifecycle.start", "ok": False,
                             "error": f"{type(exc).__name__}: {exc}"})

# --- requirements, one per WP node, wording/oracle/negative taken from the DAG itself
registered, frozen, errors = [], [], []
for wp in sorted(nodes):
    node = nodes[wp]
    req_id = "R18-%s" % wp
    acc_id = "ACC-%s" % wp
    try:
        spine.register_requirement(
            requirement_id=req_id,
            source_locator="%s::03_TESTS_AND_READBACK/wp_graph.json#%s" % (PKG_REL, wp),
            wording="%s [%s/%s] output=%s" % (node["name"], node["tier"],
                                              node["effect_class"], node["output"]),
            acceptance_id=acc_id,
            oracle=node["positive"],
            threshold="%s first_fail=%s" % (node["phase"], node["first_fail"]),
            negative_fixture=node["negative"],
            priority="P0",
            project_id=PID,
        )
        registered.append(req_id)
    except Exception as exc:  # noqa: BLE001
        errors.append({"wp": wp, "step": "register_requirement",
                       "error": f"{type(exc).__name__}: {exc}"})
        continue
    token = "R18-%s-freeze" % wp
    try:
        spine.acquire_lease(req_id, "hermes-r18-orchestrator", token, ttl_seconds=600)
        spine.transition_requirement(
            req_id, "FROZEN", actor="hermes-r18-orchestrator", token=token,
            expected_version=0,
            evidence_ref="var/R18-FHS-SKELETON-SPINE-20261029/receipts/WP00_SOURCE_CURRENTNESS.json",
            idempotency_key="R18-FREEZE-%s" % wp,
        )
        frozen.append(req_id)
        spine.release_lease(req_id, "hermes-r18-orchestrator", token)
    except Exception as exc:  # noqa: BLE001
        errors.append({"wp": wp, "step": "freeze", "error": f"{type(exc).__name__}: {exc}"})

receipt["requirements"] = {"registered": len(registered), "frozen": len(frozen),
                           "ids": registered, "errors": errors}

# --- negative control: the native taskspec admission must REFUSE without an Issuer bundle
probe = {}
try:
    spine.create_taskspec(
        taskspec_id="TS-R18-WP00-PROBE",
        requirement_id="R18-WP-FHS-00",
        objective="probe: native admission without Issuer references must fail closed",
        owner="hermes-r18-orchestrator",
        writable_root=Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029"),
        permissions={"tier": "L1", "effect_class": "SOURCE_READ"},
        tests=["probe"],
        evidence_plan="probe",
    )
    probe = {"refused": False, "note": "ADMISSION SUCCEEDED WITHOUT A BUNDLE -- gate is NOT firing"}
except Exception as exc:  # noqa: BLE001
    probe = {"refused": True, "error_type": type(exc).__name__, "error": str(exc),
             "trace_head": traceback.format_exc().splitlines()[-3:]}
receipt["native_admission_probe"] = probe

try:
    receipt["status"] = ctl.status(PID)
except Exception as exc:  # noqa: BLE001
    receipt["status"] = {"error": f"{type(exc).__name__}: {exc}"}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print(json.dumps({"start": receipt["steps"][0].get("ok"),
                  "registered": len(registered), "frozen": len(frozen),
                  "errors": errors[:4], "probe": probe}, ensure_ascii=False, default=str)[:1800])
print("STATUS", json.dumps(receipt["status"], ensure_ascii=False, default=str)[:600])
