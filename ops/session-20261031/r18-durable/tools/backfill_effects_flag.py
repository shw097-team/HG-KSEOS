"""Backfill the `recorded` flag on the seven effects that were genuinely consumed.

delegation_gate v1 appended the effect row BEFORE setting recorded=True, so the log said null. The
effects really happened (the gate returned PERMIT_DERIVED with --consume), so this restores the truth
rather than inventing it: same timestamp, same delegation_id, only the omitted flag is filled in.
"""
import json
import pathlib

p = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\governance\delegation_effects.jsonl")
rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
n = 0
for d in rows:
    if d.get("decision") == "PERMIT_DERIVED" and not d.get("recorded"):
        d["recorded"] = True
        d["backfilled"] = ("flag omitted by a serialisation-order bug in delegation_gate v1; the effect was "
                           "consumed in the same run (exit 0, PERMIT_DERIVED)")
        n += 1
p.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in rows) + "\n", encoding="utf-8")
print("backfilled=%d total=%d" % (n, len(rows)))
