"""R18 obligation ledger + driver.

One row per WP-FHS-00..21 (generated from the package's own typed DAG, never hand-typed),
plus round-level rows for admission, MVS mapping, delivery and handoff.

Usage:
  ledger_driver.py --init                 seed ledger from wp_graph.json
  ledger_driver.py --set WP-FHS-01 status=DONE engineering=VERIFIED evidence=...
  ledger_driver.py --next                 single lowest-id actionable row, or ONLY_BLOCKERS/DONE
  ledger_driver.py --audit                every DONE/REUSE row's evidence must resolve on disk
  ledger_driver.py --report               done/total by class + per-row table
Exit codes: 0 ok/audit-clean, 1 audit-failed, 3 blockers-only, 4 done
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
LEDGER = ROUND / "ledger.json"
SUBJ = ROUND / "subject"
WORKSPACE = Path(r"C:\Projects\Agent_Workspace")

STATUSES = ["PENDING", "IN_PROGRESS", "DONE", "REUSE", "PARTIAL", "HOLD", "PARKED", "CANCELLED"]
CLOSED = {"DONE", "REUSE"}
OWNER_CLASSES = ["AGENT", "OWNER", "HOST", "EXTERNAL_AO"]


def now():
    return datetime.now(timezone.utc).isoformat()


def seed():
    dag = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "wp_graph.json").read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in dag["nodes"]}
    rows = []
    for wp in sorted(nodes):
        n = nodes[wp]
        rows.append({
            "id": wp,
            "name": n["name"],
            "tier": n["tier"],
            "effect_class": n["effect_class"],
            "phase": n["phase"],
            "depends_on": n["depends_on"],
            "output": n["output"],
            "positive": n["positive"],
            "negative": n["negative"],
            "first_fail": n["first_fail"],
            "status": "PENDING",
            "engineering": None,
            "acceptance": "NOT_RUN",
            "evidence": [],
            "owner_class": None,
            "owner": None,
            "next_legal_action": None,
            "resume_predicate": None,
            "ceiling": None,
            "resume_cmd": None,
            "expect": None,
            "note": "",
        })
    for extra in [
        {"id": "R18-ADMIT", "name": "SharedSpine admission + native gate refusal proof",
         "tier": "L1", "effect_class": "SOURCE_READ", "phase": "GOVERN",
         "depends_on": [], "output": "project+22 frozen requirements+typed refusal",
         "status": "DONE", "engineering": "VERIFIED", "acceptance": "LOCAL",
         "evidence": ["var/R18-FHS-SKELETON-SPINE-20261029/receipts/ADMISSION_R18.json"],
         "owner_class": "AGENT", "ceiling": "requirement lineage is native; WorkOrder admission is refused"},
        {"id": "R18-MVS", "name": "MVS01-10 receipt mapping",
         "tier": "L1", "effect_class": "SOURCE_READ", "phase": "GOVERN",
         "depends_on": [], "output": "MVS mapping table with per-group receipts",
         "status": "PENDING", "owner_class": "AGENT"},
        {"id": "R18-DELIVER", "name": "Candidate branch/commit/push/PR per affected repo",
         "tier": "L2", "effect_class": "REPO_WRITE", "phase": "DELIVER",
         "depends_on": [], "output": "branch+commit+PR urls (no main, no force)",
         "status": "PENDING", "owner_class": "AGENT"},
        {"id": "R18-HANDOFF", "name": "STATUS/HANDOFF + RESUME_HERE + machine state",
         "tier": "L1", "effect_class": "LOCAL_DRAFT_WRITE", "phase": "DELIVER",
         "depends_on": [], "output": "handoff pack",
         "status": "PENDING", "owner_class": "AGENT"},
    ]:
        rows.append({k: extra.get(k) for k in
                     ("id", "name", "tier", "effect_class", "phase", "depends_on", "output",
                      "status", "engineering", "acceptance", "evidence", "owner_class",
                      "ceiling", "owner", "next_legal_action", "resume_predicate", "resume_cmd",
                      "expect", "note", "positive", "negative", "first_fail")} |
                    {"evidence": extra.get("evidence", [])})
    return {"schema": "R18.FHS.LEDGER/1", "seeded_utc": now(),
            "source": "03_TESTS_AND_READBACK/wp_graph.json", "rows": rows}


def load():
    if not LEDGER.exists():
        sys.exit("ERR_LEDGER_MISSING: run --init")
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(d):
    LEDGER.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def set_row(wp, pairs):
    d = load()
    row = next((r for r in d["rows"] if r["id"] == wp), None)
    if row is None:
        sys.exit("ERR_UNKNOWN_ROW %s" % wp)
    # D4 (FAR_R18-09): a DONE row must be backed by a consumed owner-delegation permit. Without this the
    # signed delegation is advisory — I could type DONE and nobody would notice, which is the same
    # failure mode as a signature nobody verifies.
    want_done = any(p.partition("=")[0] == "status" and p.partition("=")[2].upper() == "DONE" for p in pairs)
    if want_done:
        permit, err = _permit_for(wp)
        if err:
            sys.exit("REFUSED %s: %s  (run tools/delegation_gate.py --wp %s --class <class> --consume first)"
                     % (wp, err, wp))
        print("PERMIT %s consumed_at=%s delegation=%s" % (wp, permit.get("at_utc"), permit.get("delegation_id")))
    for p in pairs:
        k, _, v = p.partition("=")
        if k == "evidence":
            row["evidence"] = [x for x in v.split(";") if x]
        elif k == "add_evidence":
            row.setdefault("evidence", []).extend(x for x in v.split(";") if x)
        elif k in ("depends_on",):
            continue
        else:
            row[k] = v
    row["updated_utc"] = now()
    save(d)
    print("SET %s status=%s engineering=%s evidence=%d" %
          (wp, row.get("status"), row.get("engineering"), len(row.get("evidence") or [])))


def evidence_paths(row):
    out = []
    for e in row.get("evidence") or []:
        out.append(e)
    return out


def audit():
    d = load()
    bad = []
    checked = 0
    for row in d["rows"]:
        if row["status"] not in CLOSED:
            continue
        if not row.get("evidence"):
            bad.append((row["id"], "NO_EVIDENCE"))
            continue
        for e in row["evidence"]:
            checked += 1
            p = Path(e)
            if not p.is_absolute():
                # evidence paths are written relative to the round root (receipts/...), so resolve
                # there first and fall back to the workspace root for repo-relative paths
                cand = ROUND / e
                p = cand if cand.exists() else (WORKSPACE / e)
            if not p.exists():
                bad.append((row["id"], "MISSING %s" % e))
    print("AUDIT rows_closed=%d evidence_checked=%d unresolved=%d" %
          (sum(1 for r in d["rows"] if r["status"] in CLOSED), checked, len(bad)))
    for b in bad:
        print("  UNRESOLVED", b[0], b[1])
    return 0 if not bad else 1


def deps_done(d, row):
    by = {r["id"]: r for r in d["rows"]}
    return all(by.get(x, {}).get("status") in CLOSED for x in row.get("depends_on") or [])


def next_row():
    d = load()
    rows = [r for r in d["rows"] if r["status"] not in CLOSED and r["status"] != "CANCELLED"]
    ready = [r for r in rows
             if r.get("owner_class") == "AGENT" and r["status"] in ("PENDING", "IN_PROGRESS", "PARTIAL")
             and deps_done(d, r)]
    blocked = [r for r in rows if r["status"] in ("HOLD", "PARKED")]
    blocked_soft = [r for r in rows if r.get("owner_class") in ("OWNER", "HOST", "EXTERNAL_AO")
                    and r["status"] not in CLOSED]
    total = len(d["rows"])
    closed = sum(1 for r in d["rows"] if r["status"] in CLOSED)
    print("PROGRESS %d/%d closed" % (closed, total))
    for r in blocked + blocked_soft:
        print("  BLOCKED %-14s owner_class=%s owner=%s next=%s" %
              (r["id"], r.get("owner_class"), r.get("owner"), (r.get("next_legal_action") or "")[:90]))
    if ready:
        def order_key(x):
            rid = x["id"]
            # WP rows first (by their DAG id), round-level rows last
            return (1 if rid.startswith("R18-") else 0, rid)
        r = sorted(ready, key=order_key)[0]
        print("NEXT %s  %s" % (r["id"], r["name"]))
        print("  resume_cmd: %s" % (r.get("resume_cmd") or "NOT_SET"))
        print("  expect: %s" % (r.get("expect") or "NOT_SET"))
        return 0
    if blocked or blocked_soft:
        print("ONLY_BLOCKERS %d" % (len(blocked) + len(blocked_soft)))
        return 3
    print("DONE")
    return 4


def report():
    d = load()
    rows = d["rows"]
    total = len(rows)
    closed = sum(1 for r in rows if r["status"] in CLOSED)
    by = {}
    for r in rows:
        by[r["status"]] = by.get(r["status"], 0) + 1
    print("TOTAL %d CLOSED %d" % (total, closed))
    print("BY_STATUS", json.dumps(by, ensure_ascii=False))
    for r in rows:
        print("%-16s %-8s %-10s eng=%-9s acc=%-12s ev=%d %s" % (
            r["id"], r["tier"], r["status"], r.get("engineering") or "-",
            r.get("acceptance") or "-", len(r.get("evidence") or []),
            (r.get("note") or "")[:60]))
    return 0



def _permit_for(wp):
    """A WP may only reach DONE if the owner delegation actually authorised an effect on it."""
    import json as _j
    eff = ROUND / "governance" / "delegation_effects.jsonl"
    if not eff.is_file():
        return None, "ERR_NO_DELEGATION_EFFECTS"
    hits = []
    for line in eff.read_text(encoding="utf-8").splitlines():
        try:
            ev = _j.loads(line)
        except Exception:
            continue
        if ev.get("wp") == wp and ev.get("decision") == "PERMIT_DERIVED" and ev.get("recorded"):
            hits.append(ev)
    if not hits:
        return None, "ERR_NO_DERIVED_PERMIT"
    return hits[-1], None


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--init":
        d = seed()
        save(d)
        print("seeded %d rows" % len(d["rows"]))
        return 0
    if args[0] == "--set":
        set_row(args[1], args[2:])
        return 0
    if args[0] == "--next":
        return next_row()
    if args[0] == "--audit":
        return audit()
    if args[0] == "--report":
        return report()
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
