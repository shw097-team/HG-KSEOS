"""Trace WP positive and negative oracles to concrete case-register IDs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "subject" / "03_TESTS_AND_READBACK"
REGISTERS = (
    ("BACKED_BY_CHALLENGE96", "challenge96.json"),
    ("BACKED_BY_CELL192", "cells192.json"),
    ("BACKED_BY_B1_CASE", "b1_case_specs.json"),
    ("BACKED_BY_CHILD149", "children149.json"),
)
TOKEN = re.compile(r"[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*")
_CACHE = {}

def load_json(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

def load_register(name):
    if name not in _CACHE:
        _CACHE[name] = load_json(name)
    return _CACHE[name]

def tokens(value):
    return {part.casefold() for part in TOKEN.findall(str(value))}

def case_records(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                return value
    raise ValueError("case register must contain a list of records")

def trace_oracle(node, oracle):
    oracle_tokens = tokens(oracle)
    first_fail_tokens = tokens(node["first_fail"])
    backing = {}
    for label, filename in REGISTERS:
        matches = []
        for case in case_records(load_register(filename)):
            identifier = str(case.get("case_id", case.get("id", "")))
            if tokens(identifier) & (oracle_tokens | first_fail_tokens):
                matches.append(identifier)
        if matches:
            backing[label] = {"count": len(matches), "case_ids": matches[:5]}
    labels = list(backing)
    kind = labels[0] if len(labels) == 1 else ("BACKED_MULTIPLE" if labels else "UNBACKED")
    return {"classification": kind, "backing_registers": backing}

def main():
    graph = load_json("wp_graph.json")
    for _, name in REGISTERS:
        load_register(name)
    load_json("runner_bindings.json")
    load_json("asset_sets.json")
    rows = [{"wp_id": n["id"], "first_fail": n["first_fail"],
             "positive_oracle": n["positive"], "positive": trace_oracle(n, n["positive"]),
             "negative_oracle": n["negative"], "negative": trace_oracle(n, n["negative"])}
            for n in graph["nodes"]]
    pos = [r["wp_id"] for r in rows if r["positive"]["classification"] == "UNBACKED"]
    neg = [r["wp_id"] for r in rows if r["negative"]["classification"] == "UNBACKED"]
    both = sorted(set(pos) & set(neg))
    out = {"schema": "R18.WP21.CELL_TRACE/1",
           "matching_rule": "case ID token equals a declared-oracle token or a WP first_fail token; prose similarity is excluded",
           "wp_count": len(rows), "unbacked_pos": pos, "unbacked_neg": neg, "unbacked_both": both,
           "counts": {"unbacked_pos": len(pos), "unbacked_neg": len(neg), "unbacked_both": len(both)},
           "rows": rows}
    (ROOT / "receipts" / "WP21_CELL_TRACE.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("UNBACKED on both POS and NEG: " + ", ".join(both) if both else
          f"Traced {len(rows)} WPs; UNBACKED on both POS and NEG: none")
    return 1 if both else 0

if __name__ == "__main__":
    raise SystemExit(main())
