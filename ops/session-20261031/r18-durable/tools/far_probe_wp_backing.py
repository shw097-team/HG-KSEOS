"""FAR probe 1: are the 22 WP oracles really unbacked?

The bounded EXECUTE lane reported UNBACKED POS 22 / UNBACKED NEG 22. That claim decides whether the
candidate's skeleton+spine has any verification grounding at all, so it must not rest on one script's
reading. This probe looks for backing in every place the package actually keeps case identities:
challenge96, cells192, children149, b1_edges31, runner_bindings, acceptance_edges15, and the wp_graph
node fields themselves.
"""
import json
import re
from pathlib import Path

SUBJ = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\subject\03_TESTS_AND_READBACK")
ROUND = SUBJ.parent.parent


def load(n, default=None):
    try:
        return json.loads((SUBJ / n).read_text(encoding="utf-8"))
    except Exception:
        return default


graph = load("wp_graph.json", {})
oracles = load("challenge96.json", [])
cells = load("cells192.json", [])
children = load("children149.json", [])
edges31 = load("b1_edges31.json", [])
binds = load("runner_bindings.json", [])
acc_edges = load("acceptance_edges15.json", [])


def ids_of(obj, keys=("case_id", "id", "cell_id", "child_id", "atom_id", "node_id")):
    out = set()
    if isinstance(obj, list):
        for r in obj:
            if isinstance(r, dict):
                for k in keys:
                    if r.get(k):
                        out.add(str(r[k]))
    elif isinstance(obj, dict):
        for k in keys:
            if obj.get(k):
                out.add(str(obj[k]))
    return out


pool = {
    "challenge96": ids_of(oracles),
    "cells192": ids_of(cells),
    "children149": ids_of(children),
    "b1_edges31": ids_of(edges31),
    "runner_bindings": ids_of(binds),
}
all_ids = set().union(*pool.values())

nodes = graph.get("nodes") or []
print("wp_graph nodes:", len(nodes), "| pooled case ids:", len(all_ids))
sample_node = nodes[0] if nodes else {}
print("node fields:", list(sample_node)[:14])

# gather every id-like string that appears anywhere in a node's own fields
def node_refs(n):
    blob = json.dumps(n, ensure_ascii=False)
    return set(re.findall(r"[A-Z]{1,4}-[A-Z0-9]{1,6}-?\d{1,4}", blob))


rows = []
for n in nodes:
    refs = node_refs(n)
    backed = refs & all_ids
    rows.append({"wp": n.get("id") or n.get("wp_id"), "refs_in_node": len(refs),
                 "refs_backed": len(backed), "backed_sample": sorted(backed)[:3]})

backed_wps = [r for r in rows if r["refs_backed"]]
print("WPs with >=1 backed reference:", len(backed_wps), "of", len(rows))
for r in backed_wps[:6]:
    print("  ", r["wp"], "refs", r["refs_in_node"], "backed", r["refs_backed"], r["backed_sample"])

# also: does any node carry an explicit oracle/case field at all?
oracle_fields = {}
for n in nodes:
    for k, v in n.items():
        if any(t in k.lower() for t in ("oracle", "case", "test", "verify", "accept")):
            oracle_fields.setdefault(k, 0)
            oracle_fields[k] += 1
print("oracle-ish node fields:", oracle_fields)

# how many distinct case ids does the graph mention outside the nodes (edges)?
edges = graph.get("edges") or []
edge_refs = set()
for e in edges:
    edge_refs |= set(re.findall(r"[A-Z]{1,4}-[A-Z0-9]{1,6}-?\d{1,4}", json.dumps(e, ensure_ascii=False)))
print("edge refs:", len(edge_refs), "| backed by pool:", len(edge_refs & all_ids))
print("edge type histogram:", {t: sum(1 for e in edges if e.get("type") == t) for t in
                                {e.get("type") for e in edges}})

out = {"wp_count": len(rows), "pooled_ids": {k: len(v) for k, v in pool.items()},
       "wps_with_backed_ref": len(backed_wps), "oracle_like_fields": oracle_fields,
       "edge_refs": len(edge_refs), "edge_refs_backed": len(edge_refs & all_ids),
       "rows": rows}
(ROUND / "receipts" / "FAR_PROBE_WP_ORACLE_BACKING.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
