One bounded work package: enforce the mandatory three-lane FAR round lifecycle.

Acceptance:
- PLAN, EXECUTE, and VERIFY_SECURITY are all required by the lifecycle.
- Every typed summary resolves to an in-run raw dispatcher receipt whose digest is unchanged.
- The raw receipt passes lane_evidence_gate with rank 1, success, usage, nonce, exit 0, and exact asked/served arm.
- The synthesis cites all three summaries.
- Omission of any lane blocks closure.
- Promotion rechecks current evidence and becomes invalid after evidence changes.
- Deterministic positive, negative, and boundary tests cover the contract.
- No commit, push, merge, deploy, production claim, or canonical state mutation.

Writer: Codex EXECUTE lane (opencode-go/deepseek-v4.1-flash).
Checker: separate VERIFY_SECURITY lane and fresh-context SWARM checker.
Baseline/rollback: b97fe12bfa172ed64cb762210b0d9f800ac11456.
