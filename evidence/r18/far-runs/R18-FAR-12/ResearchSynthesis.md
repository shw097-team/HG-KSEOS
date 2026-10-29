# R18-FAR-12 synthesis

## decision_summary
Of the seven questions, five describe violations or assumptions that the artefacts in this directory refute or
confirm by measurement. Two are environment facts. None require a second human.

## claim_source_map
- CL1 -> S01,S07 [SUPPORTED_WITH_LIMIT]
- CL2 -> S06,S07 [SUPPORTED]
- CL3 -> S07 [SUPPORTED]
- CL4 -> S01,S07 [SUPPORTED]
- CL5 -> S07 [SUPPORTED_WITH_LIMIT]
- CL6 -> S03 [SUPPORTED]
- CL7 -> S02 [SUPPORTED]
- CL8 -> S01 [SUPPORTED_WITH_LIMIT]
- CL9 -> S04 [SUPPORTED]

## confidence_by_claim
minimum 0.75 (CL8), median 0.95.

## supporting_evidence
Local receipts named in ResearchSourceDenominator.tsv, all read this round.

## counterevidence
My earlier FAR_R18_12 memo asserted "cannot be solved without another principal"; S03 shows authorize() is
local software with a 6-requirement contract. The memo is superseded by this run.

## unresolved_disagreement
None between sources; the disagreement was between my prose and my measurements.

## missing_unverified
No native execution receipt exists, so CL8 stays SUPPORTED_WITH_LIMIT.

## cost_operational_tradeoff
Remediation mechanisms are all local files plus one cron tick: near-zero cost, no new service.

## recommended_disposition
RESEARCH_PASS_CANDIDATE with four HGK-route remediations (state machine, lane enforcement, stop guard, issuer path).

## nonclaims
No claim about the package's acceptance status, native qualification, or release readiness.
