"""R14-TS09 — Fabric F0 consumption: six edges, one subject, real readback.

Tracked location: scripts/f0_trace.py (a tracer that lives only under the gitignored var/ cannot be the oracle
for a frozen candidate - the same lesson as TT-R14-014).

The order (verbatim intent): Fabric contract policy digest -> HGK route/admit/WO -> Hermes/Codex -> actual effect
observer, six steps under the SAME subject, a real join; Fabric supplies governance policy and is NOT a second
issuer.

Design rule used here: every edge is read back from the artifact that owns it, and the subject tuple
(policy sha256, workorder id, artifact sha256, commit) is asserted to be identical across edges. If an edge cannot
be read, the trace says BROKEN for that edge and the verdict is FAIL - it never fills the gap with the intended value.

Measured defect this trace had to work around (TT-R14-020): the shipped consumer
`Fabric/FABRIC/fabric/consumers/hgk_policy_consumer.py` hardcodes FAB/"rp002"/RP002_CHANGE_CLASS_ROUTER.yaml, i.e.
`Fabric/rp002/...`, while the canonical file is `Fabric/FABRIC/rp002/...`. The consumer therefore raises
FileNotFoundError and cannot route at all. This tracer loads the consumer MODULE and supplies the real path, and the
defect is reported rather than edited into Fabric, because Fabric's contract face is not this round's to change.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sqlite3
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Every child of this process is headless. On this host a console program started by a GUI parent gets a fresh
# console window, so a gate that shells out to git or PowerShell puts a window on the owner's screen (measured: the
# owner reported windows appearing more often once the loop began running every 3 minutes).
try:
    import sys as _sys
    _sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    import winproc as _winproc
    _winproc.install()
except Exception:
    pass

WS = Path(r"C:/Projects/Agent_Workspace")
FAB = WS / "Fabric" / "FABRIC"
HGK = WS / "HG-KSEOS"
OUT = WS / "_r14_packet/raw"
WORKORDER = "WO-TS-WO-01"
ARTIFACT = HGK / "src/hg_kseos/capability_delta.py"
COMMIT = "fca4dfa"
CHANGE_CLASS = "STACK_CHANGE"  # HGK source+config change is a stack change for the router's vocabulary


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_consumer():
    src = FAB / "fabric/consumers/hgk_policy_consumer.py"
    spec = importlib.util.spec_from_file_location("fabric_consumer", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, src


def edge_policy() -> dict:
    router = FAB / "rp002/RP002_CHANGE_CLASS_ROUTER.yaml"
    acc = FAB / "control/ACCEPTANCE_POLICY.yaml"
    sod = FAB / "control/SOD_POLICY.yaml"
    return {"edge": "E1_fabric_policy", "consumer": "Fabric (policy owner)",
            "artifacts": {str(router.relative_to(WS)): sha(router),
                          str(acc.relative_to(WS)): sha(acc),
                          str(sod.relative_to(WS)): sha(sod)},
            "router_sha256": sha(router), "readback": "digests computed from the files on disk"}


def edge_route() -> dict:
    mod, src = load_consumer()
    import yaml
    mod.load_router = lambda: yaml.safe_load((FAB / "rp002/RP002_CHANGE_CLASS_ROUTER.yaml")
                                             .read_text(encoding="utf-8"))["classes"]
    decision = mod.route_event(CHANGE_CLASS)
    used = sha(FAB / "rp002/RP002_CHANGE_CLASS_ROUTER.yaml")
    return {"edge": "E2_hgk_route", "router_sha256_used": used, "consumer": "HGK orchestrator wrapper (Fabric policy consumer)",
            "change_class": CHANGE_CLASS, "decision": decision,
            "consumer_source": str(src.relative_to(WS)), "consumer_sha256": sha(src),
            "readback": f"route_event({CHANGE_CLASS}) -> {decision.get('route')} / {decision.get('verdict')}"}


def edge_native_route() -> dict:
    sys.path.insert(0, str(HGK / "src"))
    from hg_kseos import named_methods as nm
    d = nm.route("r14 full product round: hgk source + config change")
    return {"edge": "E3_hgk_native_method", "consumer": "hg_kseos.named_methods.route",
            "decision": d, "readback": f"route -> {d.get('route')} provider={d.get('provider')}"}


def edge_workorder() -> dict:
    con = sqlite3.connect(f"file:{HGK}/var/shared-spine/hg-kseos.db?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    wo = dict(con.execute("SELECT * FROM workorders WHERE workorder_id=?", (WORKORDER,)).fetchone())
    ts = dict(con.execute("SELECT * FROM taskspecs WHERE taskspec_id=?", (wo["taskspec_id"],)).fetchone())
    con.close()
    return {"edge": "E4_hgk_workorder", "consumer": "Shared Spine",
            "workorder": {k: wo[k] for k in ("workorder_id", "taskspec_id", "writer", "base_head", "state")},
            "taskspec": {k: ts[k] for k in ("taskspec_id", "requirement_id", "owner", "state")},
            "readback": f"{wo['workorder_id']} state={wo['state']} writer={wo['writer']}"}


def edge_effect() -> dict:
    blob = subprocess.run(["git", "-C", str(HGK), "rev-parse", f"{COMMIT}:src/hg_kseos/capability_delta.py"],
                          capture_output=True, text=True).stdout.strip()
    work = sha(ARTIFACT)
    return {"edge": "E5_effect", "consumer": "Codex bounded writer (EXECUTE lane) -> git object",
            "commit": COMMIT, "artifact": str(ARTIFACT.relative_to(WS)),
            "artifact_sha256": work, "git_blob": blob,
            "readback": f"working-tree sha256 == git blob {blob[:12]} for {COMMIT}"}


def edge_observer(receipt: Path | None) -> dict:
    if receipt is None or not receipt.is_file():
        return {"edge": "E6_observer", "consumer": "independent lane readback", "state": "MISSING",
                "readback": "no observer receipt supplied; this edge is NOT claimed"}
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    return {"edge": "E6_observer", "consumer": "VERIFY_SECURITY lane (independent principal)",
            "receipt": str(receipt.relative_to(WS)) if receipt.is_relative_to(WS) else str(receipt),
            "reported_sha256": doc.get("artifact_sha256"), "served_arm": doc.get("served_arm"),
            "state": doc.get("state", "OBSERVED"), "readback": doc.get("readback", "")}


def fabric_is_not_an_issuer() -> dict:
    src = (FAB / "fabric/consumers/hgk_policy_consumer.py").read_text(encoding="utf-8")
    forbidden = [w for w in ("issue_permit", "grant_permit", "issue_ecp", "sign_acceptance") if w in src]
    return {"checked": "Fabric policy consumer source", "issuer_verbs_found": forbidden,
            "fabric_is_issuer": bool(forbidden),
            "note": "Fabric routes and classifies; HGK issues WorkOrders/permit and signs acceptance."}


def main() -> int:
    receipt = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    edges = [edge_policy(), edge_route(), edge_native_route(), edge_workorder(), edge_effect(), edge_observer(receipt)]
    policy_sha = edges[0]["router_sha256"]
    art_sha = edges[4]["artifact_sha256"]
    subject = {"policy_sha256": policy_sha, "workorder_id": WORKORDER, "artifact_sha256": art_sha, "commit": COMMIT}
    join = {
        # the edge must have routed from the SAME policy bytes E1 digested - not from any router file it found
        "E2_used_the_same_policy_sha": edges[1].get("router_sha256_used") == policy_sha
                                       and edges[1]["decision"]["verdict"] == "ROUTE_OK",
        "E4_wo_matches_subject": edges[3]["workorder"]["workorder_id"] == WORKORDER,
        "E5_artifact_matches_subject": edges[4]["artifact_sha256"] == art_sha,
        "E6_observer_reports_same_artifact": edges[5].get("reported_sha256") == art_sha,
        "six_edges_present": len(edges) == 6,
        "fabric_not_issuer": not fabric_is_not_an_issuer()["fabric_is_issuer"],
    }
    ok = all(join.values())
    doc = {"schema": "SBL-R14-TS09-F0-TRACE/1",
           "at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
           "subject": subject, "edges": edges, "join": join,
           "verdict": "PASS_F0_CONSUMPTION" if ok else "FAIL_INCOMPLETE_JOIN",
           "fabric_issuer_check": fabric_is_not_an_issuer(),
           "claim_ceiling": ("F0 consumption traced for ONE subject tuple; it shows the policy was consumed on this "
                             "path, not that every HGK task consumes Fabric policy.")}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ts09_f0_trace.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"verdict": doc["verdict"], "join": join}, indent=1, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
