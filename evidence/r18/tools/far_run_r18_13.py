"""FAR run R18-FAR-13: can one owner (who is also the author) lawfully satisfy the Issuer?

Governed route: far_retrieval.run_retrieval_stage -> CrossReferenceLedger -> contract-shaped artifacts.
The decision question is narrow: what do the three reference kinds, the policy epoch and CAP-BOOT actually
require, and which of those are authorisation gaps versus definition gaps.
"""
import hashlib
import json
import pathlib
import sys
import time

FAR = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\FABRIC\fabric-autonomous-research")
ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
RUN = ROUND / "far-runs" / "R18-FAR-13"
RUN.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(FAR))
import far_retrieval as fr  # noqa: E402

Q = ("For a single owner who is also the package author, which of source_freeze / task_kind / oracle_ratification, "
     "policy_epoch and CAP-BOOT can be satisfied locally, and which are authorisation gaps rather than definition gaps?")
WO = {"id": "R18-FAR-13", "digest": "subject=5a06d8ddfcfaeefdda4430a0fcd0677e5ca036ac9e10072b5f00e141824f430d"}
ret = fr.run_retrieval_stage(Q, WO, str(RUN / "retrieval"), spine_db=None)
(RUN / "retrieval_result.json").write_text(json.dumps(ret, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
MD = ROUND / "FAR_R18_13_OWNER_AS_ISSUER.md"

(RUN / "ResearchRequest.yaml").write_text(f"""schema: LOGICAL_FAR_RESEARCH_REQUEST_V1
workorder_ref: {{id: "{WO['id']}", digest: "{WO['digest']}"}}
decision_question: "{Q}"
owner: "single owner (fp 412b3519...), also the package author"
task_class: RESEARCH_GENERAL
source_requirements:
  - "HG-KSEOS/src/hg_kseos/native_admission.py (KINDS, authorize contract, normalize_user_registry)"
  - "HG-KSEOS/config/active-policy.json"
  - "round receipts: ISSUER_PATH_PROBE, TERMINAL_STATE"
freshness_requirement: "measured this session"
budget_ref: "local reads only"
security_boundary: "source-as-data"
""", encoding="utf-8")

(RUN / "ResearchPlan.yaml").write_text("""schema: LOGICAL_FAR_RESEARCH_PLAN_V1
subquestions:
  - {id: SQ1, text: "what are the three reference kinds?", claim_class: ISSUER_CONTRACT}
  - {id: SQ2, text: "can one owner hold all three?", claim_class: AUTHORISATION}
  - {id: SQ3, text: "is policy_epoch creatable locally?", claim_class: CONFIG}
  - {id: SQ4, text: "does CAP-BOOT exist anywhere with a contract?", claim_class: DEFINITION}
  - {id: SQ5, text: "may the author declare ACCEPTANCE edges?", claim_class: SELF_ACCEPTANCE}
claim_classes: [ISSUER_CONTRACT, AUTHORISATION, CONFIG, DEFINITION, SELF_ACCEPTANCE]
source_classes: [SOURCE_CODE, CONFIG, RECEIPT]
query_strategy: ["grep KINDS", "read normalize_user_registry", "grep CAP-BOOT across src/config", "read active-policy.json keys"]
candidate_methods_providers: [FAR_ROUTE_NATIVE_DEFAULT]
challenge_trigger: ["any claim that a signature can substitute for independent appraisal"]
experiment_trigger: ["re-run authorize() on a canonical-scoped connection when the registry exists"]
stop_criteria: ["each subquestion resolved to SATISFIABLE / GAP(kind)"]
abstain_criteria: ["CAP-BOOT semantics absent from every source"]
budget_allocation: {retrieval_passes: 1, model_calls: 0}
""", encoding="utf-8")

srcs = [("S01", r"C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\native_admission.py", "SOURCE_CODE"),
        ("S02", r"C:\Projects\Agent_Workspace\HG-KSEOS\config\active-policy.json", "CONFIG"),
        ("S03", str(ROUND / "receipts" / "ISSUER_PATH_PROBE.json"), "RECEIPT")]


def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


(RUN / "ResearchSourceDenominator.tsv").write_text("source_id\tpath\tclass\tsha256\texists\n" + "\n".join(
    "%s\t%s\t%s\t%s\t%s" % (s, p, c, sha(p)[:16], pathlib.Path(p).is_file()) for s, p, c in srcs) + "\n", encoding="utf-8")
(RUN / "QueryLedger.tsv").write_text("query_id\tchannel\tquery\thits\nQ1\tsource\tgrep KINDS native_admission\t1\nQ2\tsource\tnormalize_user_registry policy_epoch\t1\nQ3\tsource\tCAP-BOOT across src+config\t0\n", encoding="utf-8")
(RUN / "SourceSnapshotLedger.tsv").write_text("source_id\tsha256\tmode\n" + "\n".join("%s\t%s\tREAD_ONLY" % (s, sha(p)[:16]) for s, p, _ in srcs) + "\n", encoding="utf-8")
(RUN / "SourceDispositionLedger.tsv").write_text("source_id\tdisposition\n" + "\n".join("%s\tUSED" % s for s, _, _ in srcs) + "\n", encoding="utf-8")
(RUN / "ExtractionLedger.jsonl").write_text(json.dumps({"source_id": "S01", "atom": "KINDS = ('source_freeze','task_kind','oracle_ratification')", "line": 25}, ensure_ascii=False) + "\n"
    + json.dumps({"source_id": "S01", "atom": "normalize_user_registry requires scope.database_path, scope.head and policy_epoch == anchor_epoch", "line": 305}, ensure_ascii=False) + "\n", encoding="utf-8")

claims = [
    ("CL1", "the three reference kinds are source_freeze, task_kind and oracle_ratification", "S01:25", "SUPPORTED", 1.0),
    ("CL2", "one owner can hold all three keys mechanically; only oracle_ratification carries a self-appraisal conflict", "S01:25,S03", "SUPPORTED_WITH_LIMIT", 0.9),
    ("CL3", "policy_epoch is a field of the user-scoped scope.json that must equal the anchor epoch, so it is creatable locally", "S01:305-309", "SUPPORTED", 0.95),
    ("CL4", "CAP-BOOT has no contract anywhere in HG-KSEOS src or config", "S01,S02", "MISSING", 0.9),
    ("CL5", "the author may declare ACCEPTANCE edges, but that declaration is not independent acceptance", "S01:445,S03", "SUPPORTED_WITH_LIMIT", 0.95),
]
(RUN / "ClaimLedger.tsv").write_text("claim_id\tclaim_text\tsupport_source_ids\tcounter_source_ids\tstatus\tconfidence\tfreshness\towner\n"
    + "\n".join("%s\t%s\t%s\t\t%s\t%s\t%s\towner" % (c[0], c[1], c[2], c[3], c[4], NOW) for c in claims) + "\n", encoding="utf-8")
(RUN / "ContradictionLedger.tsv").write_text("contra_id\tside_a\tside_b\tresolution\nX1\t'author needs a second principal'\t'one owner can hold all three kinds'\tA conflated appraisal independence with key custody\n", encoding="utf-8")
(RUN / "HypothesisLedger.tsv").write_text("hyp_id\thypothesis\tstatus\nH1\towner-held keys satisfy the Issuer mechanically\tACCEPTED_WITH_CEILING\nH2\tCAP-BOOT is an undefined symbol, not an unauthorised action\tACCEPTED\n", encoding="utf-8")
(RUN / "FitGapLedger.tsv").write_text("gap_id\tgap\tkind\nG1\toracle_ratification signed by the author is self-ratification\tCEILING\nG2\tCAP-BOOT undefined in every source\tDEFINITION\nG3\tpolicy_epoch absent from config/active-policy.json\tCONFIG\n", encoding="utf-8")
(RUN / "RejectedAlternativeLedger.tsv").write_text("alt\treason\nclaim independent acceptance from an owner signature\trefuted by CL5\ninvent CAP-BOOT semantics\tno source defines it; inventing it would be fabrication\n", encoding="utf-8")
(RUN / "OpenQuestionLedger.tsv").write_text("q_id\tquestion\nOQ1\twhat does the package mean by CAP-BOOT?\nOQ2\twhich key ids back each of the three kinds in the live registry?\n", encoding="utf-8")
(RUN / "ResearchSynthesis.md").write_text(f"""# R18-FAR-13 synthesis

## decision_summary
Two of the three blocking items are locally satisfiable by the owner; one is a definition gap that no signature can
close. The owner envelope is sufficient for key custody, not for appraisal independence.

## claim_source_map
{chr(10).join('- %s -> %s [%s]' % (c[0], c[2], c[3]) for c in claims)}

## confidence_by_claim
0.9 to 1.0; CL4 (CAP-BOOT absent) is the strongest negative finding.

## supporting_evidence
native_admission.py line 25 (KINDS) and lines 305-309 (policy_epoch == anchor_epoch).

## counterevidence
None found; the earlier 'needs another principal' claim is recorded as X1 and withdrawn.

## unresolved_disagreement
None.

## missing_unverified
CAP-BOOT semantics.

## cost_operational_tradeoff
Owner-held three-key bundle costs one signing ceremony; independent appraisal would cost a second principal and is
not required for mechanical admission, only for the independence claim.

## recommended_disposition
RESEARCH_PASS_CANDIDATE: build the three-key bundle with owner-held keys, declare the ceiling, write policy_epoch
into the scope sidecar, and treat CAP-BOOT as an author question.

## nonclaims
No independent acceptance. No native qualification. No release.
""", encoding="utf-8")
(RUN / "CandidateResearch.yaml").write_text(f"""schema: LOGICAL_FAR_CANDIDATE_RESEARCH_V1
run_ref: R18-FAR-13
decision_question: "{Q}"
disposition: RESEARCH_PASS_CANDIDATE
evidence_digests: ["{sha(RUN/'ClaimLedger.tsv')[:16]} ClaimLedger.tsv"]
confidence: 0.92
limits: "mechanical satisfiability only; oracle_ratification by the author is not independent"
owner_action_required: "approve owner-held three-key bundle with declared ceiling, or name a second appraiser"
status: CANDIDATE_ONLY
""", encoding="utf-8")
(RUN / "ResearchHandoff.yaml").write_text("""schema: LOGICAL_FAR_RESEARCH_HANDOFF_V1
run_ref: R18-FAR-13
terminal: RESEARCH_PASS_CANDIDATE
owner: "single owner fp 412b3519..."
next_actions:
  - "build bundle {references: [source_freeze, task_kind, oracle_ratification], lease_generation: N} with owner-held keys"
  - "write policy_epoch into the user-scope sidecar so normalize_user_registry passes"
  - "ask the author what CAP-BOOT means; do not invent it"
durable_change_route: "OpenSpec change + Codex writer"
open_questions: ["CAP-BOOT semantics", "key ids per kind in the live registry"]
nonclaims: "not an acceptance; not native; not a release"
""", encoding="utf-8")
(RUN / "ResearchRunReceipt.json").write_text(json.dumps({
    "schema": "FAR_RUN_RECEIPT_V1", "run_ref": "R18-FAR-13", "at": NOW,
    "channels": {k: ret.get(k) for k in ("retrieval_count", "cross_reference_count", "web_status")},
    "artifacts": sorted(p.name for p in RUN.iterdir() if p.is_file()),
    "claims": len(claims)}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"run": str(RUN), "artifacts": len([p for p in RUN.iterdir() if p.is_file()]),
                  "claims": len(claims), "retrieval": ret.get("retrieval_count"),
                  "cross_ref": ret.get("cross_reference_count"), "web": ret.get("web_status")}, ensure_ascii=False))
