"""WP-FHS-15 / 16 per-ID disposition readback.

WP-16's positive predicate is "24 slots / 25 methods produce their disposition-specific output and no
method pretends to be an installer". That is checkable per ID from the rows the package already carries
(asset_sets.json Donor24/Method25, b1_edges31.json for the 31 PD slots) — what was missing in R18 was
per-ID presence, not another summary count.

Also re-verifies the ORIGINAL plugin invocation receipt: the plugin manifest sha recorded there must
still match the plugin on disk, otherwise the receipt describes a different plugin build.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime, timezone

DATA = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\copy_a\03_TESTS_AND_READBACK")
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\receipts")
PLUGIN = pathlib.Path(r"C:\Projects\Agent_Workspace\SBL\sbl-tpm-sp-0.2.0rc1")

FIELDS = ("id", "name", "original_disposition", "product_decision", "install_state", "load_state",
          "invoke_state", "acceptance_state", "source", "trigger", "rollback")


def rows_for(key: str) -> list[dict]:
    sets = json.loads((DATA / "asset_sets.json").read_text(encoding="utf-8"))
    out = []
    for r in sets[key]:
        out.append({k: r.get(k) for k in FIELDS if k in r} | {"set": key})
    return out


def slots() -> list[dict]:
    edges = json.loads((DATA / "b1_edges31.json").read_text(encoding="utf-8"))
    return [{"set": "Slot31", "id": e["slot_id"], "pd_slot_id": e["pd_slot_id"], "atom_id": e["atom_id"],
             "domain": e["domain"], "required_effect": e["required_effect"], "ecp_route": e["ecp_route"],
             "original_disposition": e["ecp_route"],
             "install_state": "NO_INSTALL_REQUIRED", "load_state": "NO_LOAD_REQUIRED",
             "invoke_state": "ROUTED_BY_PIPD_NOT_HOST_INVOKED",
             "acceptance_state": e.get("native_status") or "NATIVE_NOT_RUN",
             "source": f"b1_edges31.json#source_v1_line:{e['source_v1_line']}",
             "trigger": e.get("acc"), "rollback": e.get("neg")} for e in edges]


def state_counts(rows: list[dict]) -> dict:
    out: dict[str, dict[str, int]] = {}
    for r in rows:
        s = r.setdefault("set", "?")
        for f in ("install_state", "load_state", "invoke_state", "acceptance_state"):
            v = str(r.get(f))
            out.setdefault(f, {})
            out[f][v] = out[f].get(v, 0) + 1
    return out


def plugin_verify() -> dict:
    inv = json.loads((DATA / "plugin_invocation.json").read_text(encoding="utf-8"))
    manifest = PLUGIN / "plugin.json"
    on_disk = hashlib.sha256(manifest.read_bytes()).hexdigest() if manifest.is_file() else None
    ops = [r.get("operation") for r in inv.get("results", [])]
    return {"plugin_path": str(PLUGIN), "recorded_manifest_sha256": inv.get("plugin_manifest_sha"),
            "on_disk_manifest_sha256": on_disk, "match": on_disk == inv.get("plugin_manifest_sha"),
            "operations": ops, "operation_count": len(ops),
            "host_signed_receipt": inv.get("host_signed_receipt"),
            "script_status": inv.get("script_status"), "skill_status": inv.get("skill_status")}


def main() -> int:
    methods = rows_for("Method25")
    donors = rows_for("Donor24")
    sl = slots()
    allrows = methods + donors + sl

    # a row may not claim a state that a doc-only disposition cannot produce
    illegal = [r for r in allrows if str(r.get("install_state", "")).upper() in {"INSTALLED", "LOADED"}
               and "REFERENCE_ONLY" in str(r.get("original_disposition", "")).upper()]

    receipt = {
        "schema": "R19.WP15_16_ID_LEDGER/1",
        "at": datetime.now(timezone.utc).isoformat(),
        "per_id": {"method25": len(methods), "donor24": len(donors), "slot31": len(sl), "total": len(allrows)},
        "state_counts": state_counts(allrows),
        "illegal_doc_only_install_claims": len(illegal),
        "plugin_invocation": plugin_verify(),
        "rows": allrows,
        "positive_predicate": "each ID carries its own disposition row (install/load/invoke/acceptance state + source locator); no doc-only row claims INSTALLED/LOADED",
        "negative_predicate": "a REFERENCE_ONLY row claiming INSTALLED/LOADED would be counted in illegal_doc_only_install_claims and fail this receipt",
        "claim_ceiling": ("disposition ledger derived from the package's own rows plus a live re-hash of the original "
                          "plugin manifest. It is NOT a host install/load/invoke of 25 methods, and NOT native acceptance."),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "WP15_16_ID_LEDGER.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"per_id": receipt["per_id"], "illegal": len(illegal),
                      "plugin_match": receipt["plugin_invocation"]["match"],
                      "plugin_ops": receipt["plugin_invocation"]["operation_count"]}, ensure_ascii=False, indent=1))
    print(json.dumps(receipt["state_counts"], ensure_ascii=False, indent=1)[:1200])
    return 0 if illegal == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
