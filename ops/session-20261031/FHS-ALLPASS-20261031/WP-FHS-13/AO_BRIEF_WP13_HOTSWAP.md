# VERIFY brief — WP-FHS-13, CAP on demand + hot swap (one work package)

You are the independent checker. Decide whether the recorded measurements discharge the five clauses the round's
oracle states. Read the artefacts; do not accept a summary because it says PASS.

Oracle (registered before the check): `C:\Projects\Agent_Workspace\var\FHS-ALLPASS-20261031\wp13\ORACLE_WP13.json`
Verdict on record: `...\wp13\VERDICT_WP13.json`; acceptance record: `...\wp13\ACCEPTANCE_WP13.json`
Measured artefacts: `...\wp13\HOTSWAP_RECEIPT.json`, `...\wp13\HOTSWAP_ABI_RECEIPT.json`,
`...\wp13\abi-run\` (the consumer's own run), `...\wp13\candidate.py`, `...\wp13\candidate_v2.py`,
`...\wp13\target\occupant.py`

The five clauses, verbatim from the oracle:
C1 a Need/Occupant ABI exists with a versioned contract and a Consumer that resolves per call
C2 the CONTROL shows the old occupant serving before the swap
C3 the POS shows the new occupant serving after the swap, reached through the Consumer
C4 the NEG shows the old capability is no longer served by the target
C5 the swap ran under an issuer-signed grant that verifies

For each clause answer PASS or FAIL with the field or command output you relied on. Then answer this, which the
verdict on record does not address:

6. Is the evidence *sufficiently independent*? Say plainly whether the same actor wrote the candidate and ran the
   swap, and whether any artefact shows a second, distinct checker. If the answer is that independence is absent,
   say so — that is a finding about the ceiling, not a reason to fail clauses 1-5.

Write the verdict as the LAST fenced ```json block:

{"requirement":"WP-FHS-13","clauses":[{"id":"C1","verdict":"PASS|FAIL","evidence":"..."}, ...],
 "independence":{"distinct_checker_evidenced":true|false,"note":"..."},"overall":"PASS|FAIL"}

If a clause cannot be judged from these artefacts, answer VOID for it and name what is missing. Read-only.
