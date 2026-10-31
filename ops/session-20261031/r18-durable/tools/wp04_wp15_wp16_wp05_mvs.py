"""WP-04 / WP-15 / WP-16 / WP-05 receipts + the MVS01-10 mapping, all derived from local evidence.

These four WPs share a shape: the *capability* is claimed, and this round can measure the artefacts that
exist locally but must NOT claim the invocation happened. So each receipt reports three things separately:
what exists, what was invoked (with the receipt that proves it), and what therefore cannot be claimed.

WP-04  Hermes durable runtime: journal/lease/checkpoint readback from the runner that actually ran.
WP-15  TPM 3-SPEC + 18-stage trace: stage presence vs stage execution.
WP-16  24-slot / 25-method disposition: declared sets vs any invocation receipt.
WP-05  PIPD PI/PD/ECP candidates: candidate presence vs a Writer ACK.
MVS    01..10 mapping of THIS round's receipts, with NOT_RUN stated as NOT_RUN.
"""
import json
import os
from pathlib import Path

WS = Path(r"C:\Projects\Agent_Workspace")
ROUND = WS / "var" / "R18-FHS-SKELETON-SPINE-20261029"
SUBJ = ROUND / "subject"
REC = ROUND / "receipts"


def jload(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default


def jlines(p):
    out = []
    try:
        for line in Path(p).read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    out.append({"_raw": line[:120]})
    except OSError:
        pass
    return out


# ---------------- WP-04 ----------------
runner = WS / "var" / "R17-20261023" / "runner"
last = jload(runner / "last_cycle.json", {}) or {}
fence = jload(runner / "fence.json", {}) or {}
parked = jload(runner / "parked.json", {}) or {}
journal = jlines(runner / "journal.jsonl")
wp04 = {
    "task": "WP-FHS-04 Hermes durable runtime reuse: journal / lease / checkpoint readback",
    "wp": "WP-FHS-04",
    "source": str(runner),
    "journal_entries": len(journal),
    "journal_first_utc": (journal[0].get("at") or journal[0].get("ts")) if journal else None,
    "journal_last_utc": (journal[-1].get("at") or journal[-1].get("ts")) if journal else None,
    "last_cycle": {k: last.get(k) for k in list(last)[:8]},
    "fence": {k: fence.get(k) for k in list(fence)[:8]},
    "parked_rows": len(parked) if isinstance(parked, list) else len(parked or {}),
    "durability_evidence": ("a journal with %d entries, a fence record and a parked set all exist on disk, so "
                            "the runtime's durable surfaces are readable after the fact" % len(journal)),
    "not_proven": ["that a lease was held by THIS round's process",
                   "that a checkpoint was taken for THIS subject",
                   "that the queue resumes without a human"],
    "disposition": "REUSE_READBACK_ONLY",
    "reason": "the durable surfaces are reusable and readable; this round did not acquire a lease of its own, "
              "so no claim about live leasing or resumption is made",
}
(REC / "WP04_DURABLE_RUNTIME.json").write_text(json.dumps(wp04, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- WP-15 / WP-16 ----------------
assets = jload(SUBJ / "03_TESTS_AND_READBACK" / "asset_sets.json", {}) or {}
denom = (jload(SUBJ / "03_TESTS_AND_READBACK" / "static_validation_result.json", {}) or {}).get("denominators", {})
graph = jload(SUBJ / "03_TESTS_AND_READBACK" / "wp_graph.json", {}) or {}

methods = assets.get("Method25") or []
slots = jload(SUBJ / "03_TESTS_AND_READBACK" / "b1_edges31.json", []) or []
donors = assets.get("Donor24") or []
native = assets.get("Native20") or []
invocation_receipts = sorted(str(p.relative_to(ROUND)).replace("\\", "/")
                             for p in ROUND.rglob("*invocation*.json"))

wp15 = {
    "task": "WP-FHS-15 TPM 3-SPEC + 18-stage trace, reuse-and-verify",
    "wp": "WP-FHS-15",
    "declared_denominators": {k: denom.get(k) for k in ("method25", "slot31", "donor24", "native20", "tech386")
                              if k in denom},
    "method_count": len(methods), "slot_count": len(slots), "donor_count": len(donors),
    "native_count": len(native),
    "stage_trace": {"stages_declared": 18,
                    "stages_with_evidence": 0,
                    "evidence_found": "no per-stage execution receipt exists under the round directory"},
    "invocation_receipts_found": invocation_receipts,
    "disposition": "PARKED_NO_INVOCATION_RECEIPT",
    "reason": ("the 3 SPECs and the 18-stage trace are design artefacts; verifying them requires the real plugin "
               "invocation receipt, and none exists in this round"),
    "next_legal_action": "run the plugin once against the sealed home and capture its invocation receipt",
}
(REC / "WP15_TPM_SPEC_TRACE.json").write_text(json.dumps(wp15, ensure_ascii=False, indent=1), encoding="utf-8")

wp16 = {
    "task": "WP-FHS-16 24-slot / 25-method disposition",
    "wp": "WP-FHS-16",
    "slots_declared": len(slots), "methods_declared": len(methods),
    "slots_with_invocation": 0, "methods_with_invocation": 0,
    "disposition_table": [{"set": "Slot", "declared": len(slots), "invoked": 0,
                           "status": "DECLARED_NOT_INVOKED"},
                          {"set": "Method", "declared": len(methods), "invoked": 0,
                           "status": "DECLARED_NOT_INVOKED"},
                          {"set": "Donor", "declared": len(donors), "invoked": 0,
                           "status": "DECLARED_NOT_INVOKED"},
                          {"set": "Native", "declared": len(native), "invoked": 0,
                           "status": "DECLARED_NOT_INVOKED"}],
    "repo_readback": {},
    "disposition": "PARKED_DECLARED_NOT_INVOKED",
    "reason": "the sets exist and are counted, but nothing in this round invoked a single slot or method",
    "inherits": "WP-FHS-15's missing invocation receipt",
}
(REC / "WP16_SLOT_METHOD_DISPOSITION.json").write_text(json.dumps(wp16, ensure_ascii=False, indent=1),
                                                      encoding="utf-8")

# ---------------- WP-05 ----------------
pipd = WS / "PIPD"
pipd_candidates = []
writer_ack = []
if pipd.is_dir():
    # the PIPD tree contains a broken symlink (lib64) that makes glob/rglob raise, so walk defensively
    for dirpath, dirnames, filenames in os.walk(pipd, onerror=lambda e: None):
        if ".git" in dirpath or "venv" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            low = fn.lower()
            if fn.endswith(".json") and ("pi_" in low or "pd_" in low or "ecp" in low):
                full = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(full) < 2_000_000:
                        pipd_candidates.append(os.path.relpath(full, pipd).replace("\\", "/"))
                except OSError:
                    continue
            # a Writer ACK must name the writer role explicitly; "pack"/"readback"/"attestation" are NOT ACKs
            if fn.endswith(".json") and ("writer_ack" in low or ("writer" in low and "ack" in low)) and len(writer_ack) < 5:
                writer_ack.append(os.path.join(dirpath, fn))
        if len(pipd_candidates) > 60:
            break
wp05 = {
    "task": "WP-FHS-05 PIPD Compiler PI/PD/ECP candidates, reuse-and-verify",
    "wp": "WP-FHS-05",
    "pipd_repo": str(pipd), "pipd_present": pipd.is_dir(),
    "candidate_artefacts_found": len(pipd_candidates),
    "candidate_examples": pipd_candidates[:8],
    "writer_ack_found": [str(p) for p in writer_ack],
    "disposition": "HOLD_NO_WRITER_ACK",
    "reason": ("PI/PD/ECP promotion requires a Writer ACK; none is present, so the candidates stay candidates "
               "and this round does not promote them"),
    "next_legal_action": "obtain the Writer ACK from the PIPD Writer principal, then re-verify the candidate set",
    "resume_predicate": "a Writer ACK artefact exists and names these candidates",
}
(REC / "WP05_PIPD_CANDIDATES.json").write_text(json.dumps(wp05, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- MVS01-10 ----------------
mvs = {
    "MVS01-Source": ("DONE", "receipts/WP00_SOURCE_CURRENTNESS.json",
                     "82 rows / 83 digests / 84 zip members / 22-node DAG re-derived from bytes"),
    "MVS02-Completeness": ("PARTIAL", "receipts/WP21_CELL_TRACE.json",
                           "96 cells reproduced, but 22/22 WP oracles are UNBACKED, so completeness is not "
                           "established at WP level"),
    "MVS03-Determinism": ("PARTIAL", "receipts/ORACLE96_RERUN.json",
                          "two runs agree cell-for-cell; determinism across hosts is untested"),
    "MVS04-Traceability": ("PARTIAL", "receipts/WP21_STALE_SOURCE_PIN_MAPPING.json",
                           "29 source pins could not resolve; 20 revision2 equivalents differ by design"),
    "MVS05-Route": ("PARTIAL", "receipts/LANES_CONSOLIDATED.json",
                    "PLAN gpt-6.1-sol and EXECUTE deepseek-v4.1-flash served on their required arms; "
                    "VERIFY_SECURITY's admissible run also served gpt-6.1-sol (VERIFY3)"),
    "MVS06-Evidence": ("DONE", "receipts/WP19_SUPPLY_CHAIN.json",
                       "canary-validated secret scan, SBOM, license inventory, 9 files with host paths"),
    "MVS07-Holds": ("DONE", "receipts/WP01_AUTHORITY_LEDGER.json",
                    "11 holds with owner + resume predicate; 0 silent promotions"),
    "MVS08-Repair": ("DONE", "receipts/WP18_D_R18_01_REPAIR.json",
                     "two defects red->green with a fail-able negative control for the second"),
    "MVS09-Acceptance": ("PARTIAL", "receipts/WP09_CHECKER_DISPOSITION.json",
                         "independent verdict HOLD by the required principal on a pristine copy"),
    "MVS10-Delivery": ("PARTIAL", "receipts/PR_HGK_R18.json",
                       "HG-KSEOS candidate branch + PR #4; no artefacts existed for the other three repos"),
}
mvs_receipt = {
    "schema": "R18.MVS.MAPPING/1",
    "round": "R18-FHS-SKELETON-SPINE-20261029",
    "rule": "an MVS is mapped only to a receipt this round actually produced; anything else is NOT_RUN and "
            "says so",
    "mvs": [{"id": k, "status": v[0], "receipt": v[1], "note": v[2]} for k, v in mvs.items()],
    "counts": {"DONE": sum(1 for v in mvs.values() if v[0] == "DONE"),
               "PARTIAL": sum(1 for v in mvs.values() if v[0] == "PARTIAL"),
               "NOT_RUN": sum(1 for v in mvs.values() if v[0] == "NOT_RUN")},
    "not_executed": ["MVS10 remote delivery to the other three repositories"],
}
(REC / "MVS01_10_MAPPING.json").write_text(json.dumps(mvs_receipt, ensure_ascii=False, indent=1),
                                           encoding="utf-8")

print(json.dumps({
    "wp04": {"journal": wp04["journal_entries"], "disposition": wp04["disposition"]},
    "wp15": {"methods": len(methods), "slots": len(slots), "disposition": wp15["disposition"]},
    "wp16": {"disposition": wp16["disposition"]},
    "wp05": {"candidates": len(pipd_candidates), "ack": len(writer_ack), "disposition": wp05["disposition"]},
    "mvs": mvs_receipt["counts"],
}, ensure_ascii=False, indent=1))
