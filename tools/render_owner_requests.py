#!/usr/bin/env python3
"""A6: render the owner-decision packets from the package's own machine artifacts.

Why 8 packets and not 75 tickets: the measured residue is 46 HOLD cells, 18 stages and 11 package holds.
Opened one-by-one that is 75 items -- a governance tax nobody pays, which is how holds become permanent.
The residue collapses by DECISION MAKER:
  * 18 stages -> 3 owners (ProductOwner / ArchitectureOwner / ProgramOwner), 6 stages each (T0..T5);
  * 46 cells  -> 5 reader classes (CALIBRATION 11, HUMAN_DECISION 11, HUMAN_JUDGE 11,
                 TWO_VERSION 8, PERFORMANCE 5);
  * 11 holds  -> 5 external owner classes (SOURCE 2, ABI 4, HOST 3, CHECKER 1, RELEASE 1).

This tool READS the shipped archive (never writes into it) and emits, for each decision maker, a JSON packet
(machine: every id, every satisficing field, the verification command) plus a markdown packet (human:
checkboxes). It does not sign anything and does not invent a verdict: an unsigned packet leaves every id in
its current state.

Usage:
    python tools/render_owner_requests.py --archive <path to r3 zip> --out <dir>
    python tools/render_owner_requests.py --archive <zip> --check     # validate an existing render
Exit: 0 ok, 4 input unreadable, 3 --check found a defect.
"""
from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import sys
import zipfile
from pathlib import Path

STAGE_OWNERS = [("OR-1", "ProductOwner"), ("OR-2", "ArchitectureOwner"), ("OR-3", "ProgramOwner")]
READER_CLASSES = [("OR-4", "CALIBRATION", "受保護校準 Reader 指派人"),
                  ("OR-5", "HUMAN_DECISION", "OWNER（人類決策）"),
                  ("OR-6", "HUMAN_JUDGE", "第二 principal（≠ maker，SoD）"),
                  ("OR-7", "TWO_VERSION", "前後版 Reader 綁定人")]
SIGN_FIELDS = {
    "CALIBRATION": ["reader_id", "reader_authority", "calibration_source_sha256", "calibration_value", "signed_at_utc", "signed_by"],
    "HUMAN_DECISION": ["decision_per_case", "signed_at_utc", "signed_by"],
    "HUMAN_JUDGE": ["judge_principal", "separation_of_duties_statement", "verdict_per_case", "signed_at_utc", "signed_by"],
    "TWO_VERSION": ["older_reader_id", "older_version_sha256", "newer_reader_id", "newer_version_sha256", "signed_at_utc", "signed_by"],
    "PERFORMANCE": ["waiver_basis", "accepted_claim_ceiling", "signed_at_utc", "signed_by"],
}


def read_tsv(zf: zipfile.ZipFile, name: str) -> list[dict]:
    raw = zf.read(name).decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw), delimiter="\t"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    try:
        zf = zipfile.ZipFile(a.archive)
    except Exception as exc:  # noqa: BLE001
        print(f"archive unreadable: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4
    with zf:
        cells = read_tsv(zf, "03_TESTS_AND_READBACK/HOLD_DISPOSITION.tsv")
        stages = read_tsv(zf, "03_TESTS_AND_READBACK/STAGE18_TRACE.tsv")
        holds_doc = json.loads(zf.read("03_TESTS_AND_READBACK/holds.json").decode("utf-8"))
    holds = holds_doc if isinstance(holds_doc, list) else (holds_doc.get("holds") or holds_doc.get("rows") or [])

    packets: dict[str, dict] = {}
    for pid, owner in STAGE_OWNERS:
        rows = [r for r in stages if r.get("owner_to_consumer", "").split("→")[0].strip() == owner]
        packets[pid] = {
            "schema": "R20.OWNER_REQUEST/1", "id": pid, "kind": "stage_artifacts",
            "signer": owner, "count": len(rows),
            "ids": [{"stage": r["stage"], "output_contract": r["output_contract"],
                     "current_status": r["status"]} for r in rows],
            "you_must_either": [
                "publish a machine artifact that instantiates each output_contract, or",
                "sign a per-stage typed waiver naming the stage and the accepted claim ceiling"],
            "fill": ["artifact_path_or_waiver_per_stage", "signed_at_utc", "signed_by"],
            "verify": f"python tools/check_stage_artifacts.py --owner {owner}",
            "if_unsigned": f"{len(rows)}/18 stages stay ABSENT; nothing else changes",
            "claim_ceiling": "an artifact proves an instance exists; it does not prove the package is accepted",
        }
    for pid, klass, signer in READER_CLASSES:
        rows = [r for r in cells if r.get("reader_class") == klass]
        packets[pid] = {
            "schema": "R20.OWNER_REQUEST/1", "id": pid, "kind": "hold_cells",
            "signer": signer, "reader_class": klass, "count": len(rows),
            "ids": [{"case_id": r["case_id"], "axis": r.get("axis"),
                     "first_fail": r.get("first_fail"),
                     "next_legal_action": r.get("next_legal_action"),
                     "source_alias": r.get("source_alias"), "source_line": r.get("source_line")} for r in rows],
            "fill": SIGN_FIELDS.get(klass, ["signed_at_utc", "signed_by"]),
            "verify": f"python tools/requalify_hold_cells.py --class {klass}",
            "if_unsigned": f"{len(rows)} cells stay HOLD (never converted to PASS)",
            "claim_ceiling": "requalification re-runs these cells against YOUR reader; it is not an agent verdict",
        }
    perf = [r for r in cells if r.get("reader_class") == "PERFORMANCE"]
    # PERFORMANCE cells have no bound threshold, so requalification cannot close them: re-running changes
    # nothing. They ride OR-5 as an explicit, revocable waiver -- a fabricated threshold would be the
    # forbidden move (DOC-00:1582 "no Gate relaxation"), and leaving them out of every packet would hide
    # 5 of the 46 holds from the owner.
    if perf:
        or5 = packets["OR-5"]
        or5["waiver_ids"] = [{"case_id": r["case_id"], "axis": r.get("axis"),
                              "first_fail": r.get("first_fail"),
                              "why_waiver": "no bound performance threshold exists in any source for this axis"}
                             for r in perf]
        or5["count"] += len(perf)
        or5["ids"] = or5["ids"] + [{"case_id": r["case_id"], "axis": r.get("axis"),
                                    "first_fail": r.get("first_fail"), "next_legal_action": "PERFORMANCE_UNOBSERVED waiver",
                                    "source_alias": r.get("source_alias"), "source_line": r.get("source_line")}
                                   for r in perf]
        or5["fill"] = ["decision_per_case", "performance_waiver_accepted (true/false)",
                       "waiver_basis", "signed_at_utc", "signed_by"]
    packets["OR-8"] = {
        "schema": "R20.OWNER_REQUEST/1", "id": "OR-8", "kind": "external_holds",
        "signer": "5 external owner classes (SOURCE/ABI/HOST/CHECKER/RELEASE)", "count": len(holds),
        "classes": dict(collections.Counter(h.get("class") for h in holds)),
        "ids": [{"class": h.get("class"), "affected_scope": h.get("affected_scope"),
                 "owner": h.get("owner"), "next_legal_action": h.get("next_legal_action"),
                 "resume_predicate": h.get("resume_predicate")} for h in holds],
        "also_open": ["CR-ORACLE-001 (DOC-07 vs DOC-03 writer authority)",
                      "N11/N14 chapter split ruling (DOC-00:1546 TT-003)",
                      f"PERFORMANCE cells ({len(perf)}) with no bound threshold -- waiver rides OR-5"],
        "fill": ["per_id_reply_or_supersession", "signed_at_utc", "signed_by"],
        "verify": "python tools/check_external_holds.py --receipts-dir _handover/R20-FHS-20261029/owner_receipts",
        "if_unsigned": f"{len(holds)} holds stay OPEN; affected consumers keep DOC_ROUTE_HOLD (DOC-00:1582)",
        "claim_ceiling": "release gate is owner-only (DOC-02:10643); this packet cannot substitute for it",
    }

    total = sum(len(p.get("ids") or []) for p in packets.values())
    print(f"packets={len(packets)} ids_across_packets={total} cells={len(cells)} stages={len(stages)} holds={len(holds)}")

    if a.check:
        problems = []
        if len(packets) != 8:
            problems.append(f"expected 8 packets, got {len(packets)}")
        if sum(p["count"] for p in packets.values() if p["kind"] == "hold_cells") != len(cells):
            problems.append("hold-cell packets do not cover every cell exactly once")
        if sum(p["count"] for p in packets.values() if p["kind"] == "stage_artifacts") != len(stages):
            problems.append("stage packets do not cover every stage exactly once")
        for p in packets.values():
            if not p.get("verify") or not p.get("claim_ceiling"):
                problems.append(f"{p['id']} missing verify/claim_ceiling")
        for pr in problems:
            print("DEFECT", pr)
        return 0 if not problems else 3

    out = Path(a.out or "_handover/R20-FHS-20261029/owner_requests")
    out.mkdir(parents=True, exist_ok=True)
    for pid, p in packets.items():
        (out / f"{pid}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1) + "\n",
                                         encoding="utf-8", newline="\n")
        lines = [f"# {pid} — {p['kind']} for {p['signer']}", "",
                 f"- items: **{p['count']}**",
                 f"- verify after signing: `{p['verify']}`",
                 f"- if unsigned: {p['if_unsigned']}",
                 f"- claim ceiling: {p['claim_ceiling']}", "",
                 "## Items", "", "| # | id | current | next legal action |", "|---|---|---|---|"]
        for i, it in enumerate(p["ids"], 1):
            ident = it.get("stage") or it.get("case_id") or it.get("affected_scope")
            cur = it.get("current_status") or it.get("first_fail") or it.get("class")
            nxt = it.get("next_legal_action") or it.get("output_contract") or ""
            lines.append(f"| {i} | `{ident}` | {cur} | {nxt} |")
        lines += ["", "## What to fill", "", ", ".join(f"`{f}`" for f in p["fill"]), "",
                  "Signature is the OWNER's act. The agent prepares the packet and verifies the result; it "
                  "does not sign, and a packet left unsigned changes no state.", ""]
        (out / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {len(packets) * 2} files to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
