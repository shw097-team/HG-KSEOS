# R18-FAR-13 synthesis

## decision_summary
Two of the three blocking items are locally satisfiable by the owner; one is a definition gap that no signature can
close. The owner envelope is sufficient for key custody, not for appraisal independence.

## claim_source_map
- CL1 -> S01:25 [SUPPORTED]
- CL2 -> S01:25,S03 [SUPPORTED_WITH_LIMIT]
- CL3 -> S01:305-309 [SUPPORTED]
- CL4 -> S01,S02 [MISSING]
- CL5 -> S01:445,S03 [SUPPORTED_WITH_LIMIT]

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
