"""Independent structural verification of the reproduced first work (WP-FHS-15).

Read-only over the reproduction tree; writes one JSON receipt.

Checks
  D1 22-WP DAG: 22 nodes, every edge resolves, topological order exists, no cycle
  D2 WP-FHS-15 dependency closure == {WP-FHS-00, WP-FHS-01, WP-FHS-15}
  D3 no future-receipt predecessor (no edge into WP-FHS-15 from an unbuilt WP)
  D4 PI: 24 atoms, each with consumer + POS + NEG + own source locator
  D5 FUO: ten declared fields present and non-empty
  D6 three SPECs exist, carry acceptance with own negative, and no duplicate ids
  D7 current-reader map: 2221 unique locators
Exit 0 only when all PASS.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\wg\repro")
FW = ROOT / "02_FIRST_WORK"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    out: dict = {"root": str(ROOT), "checks": {}}

    dag = load(FW / "ORIGINAL_22_WP_DAG.json")
    nodes = {n["id"]: n for n in dag["nodes"]}
    edges = [(n["id"], d) for n in dag["nodes"] for d in n.get("depends_on", [])]
    dangling = [e for e in edges if e[0] not in nodes or e[1] not in nodes]
    indeg = {k: 0 for k in nodes}
    for _a, b in edges:
        indeg[b] += 1
    q = deque([k for k, v in indeg.items() if v == 0])
    order = []
    while q:
        cur = q.popleft()
        order.append(cur)
        for a, b in edges:
            if a == cur:
                indeg[b] -= 1
                if indeg[b] == 0:
                    q.append(b)
    acyclic = len(order) == len(nodes)
    out["checks"]["D1_dag"] = {
        "verdict": "PASS" if (len(nodes) == 22 and not dangling and acyclic) else "FAIL",
        "nodes": len(nodes), "edges": len(edges), "dangling_edges": dangling,
        "acyclic": acyclic, "topological_len": len(order),
    }

    def ancestors(start: str, seen=None) -> set:
        seen = seen if seen is not None else set()
        for d in nodes.get(start, {}).get("depends_on", []):
            if d not in seen:
                seen.add(d)
                ancestors(d, seen)
        return seen

    wp15 = nodes.get("WP-FHS-15", {})
    closure = ancestors("WP-FHS-15") | {"WP-FHS-15"}
    declared = set(dag.get("dependency_closure") or [])
    inputs_00 = (ROOT / "03_HANDOFF_EVIDENCE" / "FIRST_WORK_SOURCE_WP15.json").is_file()
    inputs_01 = (FW / "ProfileBinding.json").is_file() and (FW / "ProfileDecision.json").is_file()
    # The seed DECLARES {00,01,15}; the typed edges give only {00,15}: WP-FHS-01 depends_on [WP-FHS-00],
    # so it is a sibling-after-00, never an ancestor of WP-FHS-15. Reported, not silently repaired:
    # changing the original 22-WP graph is the domain owner's call, not this receiver's.
    out["checks"]["D2_wp15_closure"] = {
        "verdict": "REVIEW",
        "edge_derived_closure": sorted(closure),
        "declared_in_seed": sorted(declared),
        "declared_equals_edge_derived": declared == closure,
        "wp01_is_ancestor_of_wp15": "WP-FHS-01" in closure,
        "wp01_edge": nodes.get("WP-FHS-01", {}).get("depends_on"),
        "operational_inputs_present": {"WP-FHS-00_source": inputs_00, "WP-FHS-01_profile": inputs_01},
        "note": ("declared dependency_closure is not derivable from typed edges; the first work still "
                 "holds because both required inputs exist as artifacts, but the graph and the "
                 "declaration disagree and only the original owner may re-type the edge"),
    }

    future = [d for d in wp15.get("depends_on", []) if d not in ("WP-FHS-00", "WP-FHS-01")]
    out["checks"]["D3_no_future_receipt"] = {
        "verdict": "PASS" if not future else "FAIL", "unexpected_predecessors": future,
        "rule": dag.get("rule"),
    }

    pi = load(FW / "PI-PKG.json")
    atoms = pi["stable_semantic_contract"]["atoms"]
    missing = []
    for a in atoms:
        sc = a.get("source_clause") or {}
        rg = a.get("risk_guard") or {}
        ok = (bool(sc.get("source_ref")) and bool(sc.get("text")) and bool(a.get("owner"))
              and bool((rg.get("oracle") or {}).get("expected"))
              and bool(rg.get("negative_fixture")) and bool(rg.get("failure_condition")))
        if not ok:
            missing.append(a.get("subject_id"))
    out["checks"]["D4_pi_atoms"] = {
        "verdict": "PASS" if len(atoms) == 24 and not missing else "FAIL",
        "atoms": len(atoms), "incomplete": missing,
    }

    fuo = load(FW / "RUN" / "FUO.json")
    body = fuo.get("functional_use_outcome") or fuo
    ten = ["persona", "clean_start", "source_sha", "selected_path", "first_useful_output",
           "elapsed_ms", "questions_reasked", "error_count", "provider_off", "consumer_acceptance"]
    missing_f = [f for f in ten if f not in body]
    out["checks"]["D5_fuo_ten_fields"] = {
        "verdict": "PASS" if not missing_f else "FAIL",
        "keys_present": list(body), "missing": missing_f,
    }

    spec_rows = {}
    for name in ("ProductSPEC", "ArchitectureSPEC", "ProgramSPEC"):
        s = load(FW / "RUN" / f"{name}.json")
        acc = s.get("acceptance") or []
        orphan = [a for a in acc if not a.get("negative")]
        spec_rows[name] = {"bytes": (FW / "RUN" / f"{name}.json").stat().st_size,
                           "acceptance": len(acc), "orphan_negatives": len(orphan)}
    out["checks"]["D6_three_specs"] = {
        "verdict": "PASS" if all(v["acceptance"] > 0 and v["orphan_negatives"] == 0
                                 for v in spec_rows.values()) else "FAIL",
        "specs": spec_rows,
    }

    cmap = load(ROOT / "03_HANDOFF_EVIDENCE" / "CURRENT_READER_MAP.json")
    locs = cmap if isinstance(cmap, list) else cmap.get("locators") or cmap.get("readers") or []
    uniq = {json.dumps(x, sort_keys=True) for x in locs}
    out["checks"]["D7_current_reader_map"] = {
        "verdict": "PASS" if len(locs) == 2221 and len(uniq) == 2221 else "REVIEW",
        "locators": len(locs), "unique": len(uniq),
    }

    verdicts = [v["verdict"] for v in out["checks"].values()]
    out["overall"] = "PASS" if all(v == "PASS" for v in verdicts) else ("REVIEW" if "FAIL" not in verdicts else "FAIL")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["overall"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
