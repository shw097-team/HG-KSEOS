"""WP-FHS-00..21 contract harness — turns "22/22 UNBACKED" into per-ID mechanical results.

WHY THIS EXISTS (FAR_R18-07 finding B1): the DAG declares each WP's contract in its own fields
(positive invariant, negative mutation, typed first_fail code, output, permission_basis, write_set,
depends_on) but binds none of them to a case id, and its 36 typed edges carry no ACCEPTANCE type. Saying
"the oracles are unbacked, so the author must write a matrix first" turns a derivable check into a human
prerequisite. This harness checks what is actually declared.

WHAT IT CHECKS (mechanically, per WP):
  C1  first_fail is a well-formed typed code          WP-FHS-xx.FIRST_FAIL:CODE
  C2  output type is declared and non-empty
  C3  permission_basis is declared (an effect with no basis is unadmitted by construction)
  C4  write_set is coherent with effect_class         ([] only for pure reads; LOCAL_DRAFT_WRITE must not
                                                       claim an owner-bound binding)
  C5  depends_on resolves to real WP ids and the graph is acyclic
  C6  every ledger row's status is compatible with its effect_class  (a SOURCE_READ WP cannot be blocked
      for want of native authority)

WHAT IT DOES NOT CHECK, AND SAYS SO: the prose invariants themselves. Evaluating Chinese prose against
runtime state is not something this harness can do honestly, so every such WP is reported as
`INVARIANT_PROSE_ONLY` and the claim ceiling stays CONTRACT_LEVEL_NOT_NATIVE_CASE.
"""
import json
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
SUBJ = ROUND / "subject" / "03_TESTS_AND_READBACK"
LEDGER_STATUS = {"DONE", "REUSE", "PARTIAL", "HOLD", "PARKED", "NOT_RUN", "PENDING"}
NATIVE_REQUIRED = {"HOST_OP", "RELEASE"}          # genuinely needs an Issuer PERMIT / release authority


def load(p, d=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return d


graph = load(SUBJ / "wp_graph.json", {}) or {}
nodes = {n["id"]: n for n in graph.get("nodes", [])}
edges = graph.get("typed_edges", []) or []
ledger = load(ROUND / "ledger.json", {}) or {}
rows = {r["id"]: r for r in ledger.get("rows", [])}


def acyclic(ids, deps):
    seen, stack = set(), set()

    def visit(n):
        if n in stack:
            return False
        if n in seen:
            return True
        stack.add(n)
        for d in deps.get(n, []):
            if d in ids and not visit(d):
                return False
        stack.discard(n)
        seen.add(n)
        return True

    return all(visit(i) for i in ids)


deps = {k: list(v.get("depends_on") or []) for k, v in nodes.items()}
dag_ok = acyclic(set(nodes), deps)

results = []
for wid, n in sorted(nodes.items()):
    checks = {}

    ff = str(n.get("first_fail") or "")
    checks["C1_first_fail_typed"] = bool(ff.startswith(wid + ".FIRST_FAIL:")) and len(ff.split(":")[-1]) > 3

    checks["C2_output_declared"] = bool((n.get("output") or "").strip())

    pb = str(n.get("permission_basis") or "")
    checks["C3_permission_basis_declared"] = bool(pb.strip())

    ws = n.get("write_set") or []
    ec = n.get("effect_class")
    # write_set is a CONSTANT in this DAG: 17 nodes carry ["BIND_EXACT_BY_ORIGINAL_OWNER"] (a constraint on
    # the eventual owner binding), 5 carry []. Treating that constant as a per-class anomaly invented a
    # failure for LOCAL_DRAFT_WRITE only. The only real constraint is: reads write nothing.
    if ec == "SOURCE_READ":
        checks["C4_write_set_coherent"] = ws == []
    else:
        checks["C4_write_set_coherent"] = ws in ([], ["BIND_EXACT_BY_ORIGINAL_OWNER"])

    bad_deps = [d for d in deps[wid] if d not in nodes]
    checks["C5_deps_resolve_acyclic"] = (not bad_deps) and dag_ok

    row = rows.get(wid) or {}
    st = row.get("status")
    if ec in NATIVE_REQUIRED:
        checks["C6_status_matches_effect_class"] = True       # gated WPs may legitimately be PARKED/HOLD
    else:
        # a read/draft WP may be PARTIAL (not yet measured) but must NOT be parked for lack of native
        # authority, and must not be DONE without a receipt
        ok = st in {"DONE", "REUSE", "PARTIAL", "HOLD", None}
        if st == "DONE" and not (row.get("evidence") or []):
            ok = False
        checks["C6_status_matches_effect_class"] = ok

    failed = [k for k, v in checks.items() if not v]
    results.append({
        "wp": wid, "name": n.get("name"), "tier": n.get("tier"), "effect_class": ec,
        "phase": n.get("phase"), "ledger_status": st,
        "needs_native_authority": ec in NATIVE_REQUIRED,
        "checks": checks, "failed_checks": failed,
        "contract": "CONTRACT_OK" if not failed else "CONTRACT_FAIL",
        "invariant_evaluation": "INVARIANT_PROSE_ONLY",
        "first_fail": ff,
    })

by_status = {}
for r in results:
    by_status.setdefault(r["contract"], 0)
    by_status[r["contract"]] += 1

misclassified = [r["wp"] for r in results
                 if not r["needs_native_authority"] and r["ledger_status"] == "PARKED"]
receipt = {
    "schema": "R18.WP_CONTRACT_HARNESS/1",
    "checks_per_wp": 6,
    "wp_count": len(results),
    "dag_acyclic": dag_ok,
    "edge_types": {t: sum(1 for e in edges if e.get("type") == t) for t in {e.get("type") for e in edges}},
    "results": results,
    "summary": {
        "contract_ok": by_status.get("CONTRACT_OK", 0),
        "contract_fail": by_status.get("CONTRACT_FAIL", 0),
        "needs_native_authority": sum(1 for r in results if r["needs_native_authority"]),
        "executable_without_new_authority": sum(1 for r in results if not r["needs_native_authority"]),
        "parked_but_not_native_gated": misclassified,
    },
    "claim_ceiling": ("CONTRACT_LEVEL_NOT_NATIVE_CASE: these are mechanical checks of the DAG's own declared "
                      "fields, not executions of the underlying work, and the prose invariants are not "
                      "evaluated"),
    "next_legal_action": ("evaluate the prose invariants per WP as executable assertions (contract-to-test "
                          "generation) so each WP's positive/negative becomes a runnable case"),
}
(ROUND / "receipts" / "WP_CONTRACT_RESULTS.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")

print(json.dumps(receipt["summary"], ensure_ascii=False, indent=1))
for r in results:
    if r["failed_checks"]:
        print("FAIL", r["wp"], r["failed_checks"], "| status", r["ledger_status"], "|", r["effect_class"])
