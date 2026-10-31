"""Close-out pass: refresh MVS mapping (MVS10 now executed for HG-KSEOS), handoff files, Kanban view.

Nothing here invents a result: MVS10 is only marked executed for the one repo that actually received a
push (HG-KSEOS). Fabric/PIPD/SBL had no publishable artefact this round, so their MVS10 stays NOT_RUN with
that scope statement, which is what the earlier receipt already said.
"""
import json
import pathlib
import subprocess
import time

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
PY = __import__("sys").executable
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---------------------------------------------------------------- MVS mapping refresh
mvs = {
    "schema": "R18.MVS01_10_MAPPING/2",
    "refreshed_utc": now,
    "evidence_basis": "this round's own receipts; a mission is DONE only where a receipt exists",
    "rows": [
        {"mvs": "MVS01", "status": "DONE", "evidence": "receipts/WP00_SOURCE_CURRENTNESS.json",
         "note": "source/manifest/ZIP/DAG currentness measured"},
        {"mvs": "MVS02", "status": "PARTIAL", "evidence": "receipts/WP0203_17_BINDINGS.json",
         "note": "Fabric policy present but carries no epoch; binding not demonstrable"},
        {"mvs": "MVS03", "status": "PARTIAL", "evidence": "receipts/WP0203_17_BINDINGS.json",
         "note": "Issuer module present, registry present, registry_rev None -> issuance unproven"},
        {"mvs": "MVS04", "status": "DONE", "evidence": "receipts/WP04_DURABLE_RUNTIME.json",
         "note": "journal/fence/parked readback (257 entries); no live lease held by this round"},
        {"mvs": "MVS05", "status": "PARTIAL", "evidence": "receipts/LANES_CONSOLIDATED.json, checker/VERIFY6_R18.json",
         "note": "EXECUTE and PLAN compliant; VERIFY compliant only via --force-rank 2, toolchain dirty"},
        {"mvs": "MVS06", "status": "DONE", "evidence": "receipts/WP_CONTRACT_RESULTS.json",
         "note": "22/22 contract checks over declared fields"},
        {"mvs": "MVS07", "status": "DONE", "evidence": "receipts/VALIDATE_RERUN.json, receipts/ORACLE96_RERUN.json",
         "note": "2789/0 and 50/46/0 reproduced on an isolated copy"},
        {"mvs": "MVS08", "status": "DONE", "evidence": "receipts/WP19_SUPPLY_CHAIN.json",
         "note": "supply-chain scan incl. planted canary"},
        {"mvs": "MVS09", "status": "PARTIAL", "evidence": "checker/VERDICT_FORCE_RANK2.md",
         "note": "independent verdict is HOLD; no acceptance"},
        {"mvs": "MVS10", "status": "PARTIAL",
         "evidence": "PR #4 https://github.com/shw097-team/HG-KSEOS/pull/4 (branch head b2159b09)",
         "note": ("EXECUTED for HG-KSEOS only: candidate branch pushed and PR updated 2026-10-29. "
                  "Fabric/PIPD/SBL received no publishable artefact this round -> NOT_RUN with scope "
                  "statement, not a silent PASS")},
    ],
    "claim_ceiling": "mapping of receipts that exist; it is not an acceptance and not a release",
}
(ROUND / "receipts" / "MVS01_10_MAPPING.json").write_text(json.dumps(mvs, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")

# ---------------------------------------------------------------- ledger + kanban view
subprocess.run([PY, "-B", str(ROUND / "tools" / "kanban_reconcile.py")], capture_output=True, text=True, timeout=300)
led = json.loads((ROUND / "ledger.json").read_text(encoding="utf-8"))
counts = {}
for r in led["rows"]:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

# ---------------------------------------------------------------- machine state
state = json.loads((ROUND / "SESSION_STATE.json").read_text(encoding="utf-8"))
state["refreshed_utc"] = now
state["ledger"] = counts
state["driver"] = {"script": "tools/r18_autodriver.py", "cron_job": "2897733e2ca1",
                   "schedule": "every 30m", "no_agent": True,
                   "journal": "receipts/DRIVER_JOURNAL.jsonl",
                   "state_file": "DRIVER_STATE.json",
                   "gateway_pid_at_start": 23508}
state["delivery"] = {"branch": "candidate/r18-openspec-only", "head": "b2159b09",
                     "pr": "https://github.com/shw097-team/HG-KSEOS/pull/4",
                     "repos_published": ["HG-KSEOS"], "repos_not_run": ["Fabric", "PIPD", "SBL"]}
state["owner_delegation"] = {
    "delegation_id": "R18-CANON-6733b6bb",
    "owner_fingerprint": "412b351937be72a1",
    "identity": "CANONICAL_HGK_OWNER (~/.hgk-owner/owner.key.enc)",
    "window": "WIN-796b69117680", "window_budget": "8h / 40 ops",
    "wp_allowlist": ["WP-FHS-00", "WP-FHS-01", "WP-FHS-09", "WP-FHS-19", "WP-FHS-21", "WP-FHS-06", "WP-FHS-18"],
    "gate_matrix": "receipts/DELEGATION_GATE_MATRIX_CANONICAL.json (7/7 permit, 6/6 refuse)",
    "second_key": "RETIRED (governance/SECOND_KEY_RETIRED.json)",
}
(ROUND / "SESSION_STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- RESUME_HERE refresh
(ROUND / "RESUME_HERE.md").write_text(
    "# RESUME_HERE — R18 FHS-MSC Skeleton+Spine\n\n"
    "Read in this order. Do not re-derive what is measured.\n\n"
    "1. `FAR_R18_11_WHY_IT_STOPS.md` — why the round kept stopping and what replaced it (driver + cron).\n"
    "2. `FAR_R18_10_CONCURRENT_SESSION_RECHECK.md` — the duplicate owner key and the diverged branches.\n"
    "3. `FAR_R18_07_STOP_REVIEW_AND_OWNER_ENVELOPE.md` — the delegation design (T1/T2/T3).\n"
    "4. `STATUS_HANDOFF.md` — measured results and ceilings.\n"
    "5. `SESSION_STATE.json` — machine-readable state.\n\n"
    "## Current facts (verified)\n\n"
    "- ledger: %s\n"
    "- owner delegation: `R18-CANON-6733b6bb`, canonical owner `412b3519…`, window `WIN-796b69117680`.\n"
    "- gate: 7/7 POS permits, 6/6 NEG refusals (`receipts/DELEGATION_GATE_MATRIX_CANONICAL.json`).\n"
    "- delivery: `candidate/r18-openspec-only` @ `b2159b09`, PR #4.\n"
    "- unattended driver: `tools/r18_autodriver.py`, cron `2897733e2ca1` every 30m, gateway PID 23508.\n\n"
    "## Do not do this again\n\n"
    "- do not treat PARTIAL as terminal; that is what made the round look finished while 18 rows were open;\n"
    "- do not create a second owner key: the canonical one is `~/.hgk-owner/owner.key.enc`;\n"
    "- do not delete or force-push the other candidate branch — it diverges, it is not stale;\n"
    "- do not present a signature over a payload as an Issuer PERMIT.\n" % json.dumps(counts, ensure_ascii=False),
    encoding="utf-8")

print(json.dumps({"ledger": counts, "mvs10": "PARTIAL(executed for HG-KSEOS)",
                  "resume_here": "rewritten", "mvs": "receipts/MVS01_10_MAPPING.json"}, ensure_ascii=False))
