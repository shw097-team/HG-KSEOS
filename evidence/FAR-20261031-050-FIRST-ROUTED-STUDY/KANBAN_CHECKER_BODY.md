Independent gate/checker task for the single work package t_e400cb8c.

The checker must start from the candidate diff and raw test evidence, re-derive every decisive claim, and must not use the writer's implementation summary as its oracle. It is read-only: no repair, WorkOrder creation, promotion, release, deploy, commit, or canonical state mutation.

Oracle registered before checking:
1. Exactly PLAN, EXECUTE, and VERIFY_SECURITY are required.
2. Each summary binds run, lane, nonce, exact required arm, question digest, in-run raw receipt path, and raw receipt digest.
3. Each raw receipt is re-read, digest-matched, and judged by lane_evidence_gate with rank 1, ok, usage_receipt_ok, nonce, exit 0, and exact asked==served identity.
4. Synthesis cites all three typed summaries.
5. Omission of any one lane yields INVALID_RESEARCH.
6. Path escape, raw tampering, malformed receipt, missing transport identity, and alternate closure state are refused.
7. Publication status is derived by re-running the gate; a marker alone is insufficient and later evidence changes invalidate it.
8. The deterministic focused suite must pass.
9. Claim ceiling: candidate implementation only; no canonical acceptance, production, or release.

Return PASS only if every oracle item is supported by re-derivable evidence. Return FAIL with exact counterexamples. Return INCONCLUSIVE when evidence is missing; INCONCLUSIVE is not acceptance.
