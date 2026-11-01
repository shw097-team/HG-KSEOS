I’ll read the AO brief and repository rules, then run the authorized read-only review.


The receipts record v1 before the swap and v2 afterward, including a run through the ABI consumer. I’m checking the consumer code, grant verification, and actor records to assess the five clauses and the independence ceiling.


I found a later grant-bound rerun, but it uses a different target and candidate from the ABI run named in the brief. It cannot retroactively authorize that earlier swap. The prior checker receipt also has `ok: false` and no accepted serving arm, so it does not establish a passing independent-checker lane.


**FAIL for the swap named in the brief:** C1–C4 pass; C5 fails. The later grant-bound rerun verifies cryptographically, but uses a different target and candidate and does not authorize the earlier ABI swap.

A separate checker attempt is evidenced, but its receipt fails `lane_evidence_gate.py` with `dispatch_not_ok`. This review makes no canonical acceptance claim. No files were changed.

NONCE-ECHO: AO-WP-FHS-13-62CCAC70

```json
{
  "requirement": "WP-FHS-13",
  "clauses": [
    {
      "id": "C1",
      "verdict": "PASS",
      "evidence": "PIPD/src/pipd_ls_sp/abi.py defines ABI_VERSION=1, Need, Occupant, and Consumer.__call__ resolving through Registry on every call. Read-only checks confirmed the same Consumer observes registry replacement and rejects missing needs, version mismatches, missing methods, and duplicate bindings."
    },
    {
      "id": "C2",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: before.identity and control.identity are cap-attest-v1; both have served=true; before.via=abi-consumer."
    },
    {
      "id": "C3",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: pos.identity=cap-attest-v2, served=true, via=abi-consumer, origin=abi-run/occupant.py. Read-only Consumer invocation returned cap-attest-v2; candidate and installed target digests match the receipt."
    },
    {
      "id": "C4",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: neg.identity=cap-attest-v2, distinct from control.identity=cap-attest-v1. For this identity fixture, the target no longer returns the old identity. NEG reuses the POS observation rather than recording a separate invocation."
    },
    {
      "id": "C5",
      "verdict": "FAIL",
      "evidence": "Neither named HOTSWAP receipt contains a grant binding. PROBE-WP13-A1 was issued 100 seconds after the ABI swap and covers abi.py/hotswap.py rather than its target/candidate. The later HOTSWAP_GRANT_BOUND_RECEIPT.json has a valid signature, matching grant digest, and valid historical time window, but concerns target_grant/occupant.py and candidate_grant.py, a different swap."
    }
  ],
  "independence": {
    "distinct_checker_evidenced": true,
    "note": "A separate checker attempt appears in AO_RECEIPT_AO-WP-FHS-13-9CB0D7AA.json, but its ok=false and lane gate returns LANE_CLAIM_UNSUPPORTED. Qualified independence is therefore unestablished. Original receipts do not identify candidate-author and swap-runner actors. The later wp13_grant_bound_swap.py uses one maker workflow to write the candidate and run the swap; it provides no actor separation. Independence limits assurance separately from C1-C5."
  },
  "overall": "FAIL"
}
```