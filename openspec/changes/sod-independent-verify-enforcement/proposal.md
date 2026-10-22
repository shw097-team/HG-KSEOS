# Proposal: enforce independent VERIFY at the canonical spine (SOD deviation 1)

## Why
Fabric/control/ACCEPTANCE_POLICY.yaml ratifies maker_final_pass:false, missing_required_raw_evidence:FAIL_CLOSED
and subject_digest_mismatch:FAIL_CLOSED, and SOD_POLICY.yaml ratifies incompatible_roles (maker/final_checker).
Measured: 0 of those rules had any implementing code on the canonical spine path, so a round could be recorded
complete with EXECUTE having run and no independent VERIFY having run (live example: WO-REQ-HGK-SOD-FIX1-20261009
VERIFIED while its acceptance stayed NOT_RUN).

## What changes
1. lifecycle: remove the EXECUTING -> EVOLUTION_REVIEW skip edge; require registered independent-verify evidence
   before EVOLUTION_REVIEW or DELIVERED (ERR_VERIFY_REQUIRED).
2. spine.record_workorder_result / spine.resolve_acceptance (including the idempotent replay path): require
   evidence existence, kind=INDEPENDENT_VERIFY_VERDICT, producer and checker != writer, and a locator re-hash match.
3. spine.register_evidence: optional subject_digest; validation only for the governed kind (backward compatible).
4. evidence_refs gains a nullable subject_digest (forward-only migration, authored not run in the candidate round).

## Impact
Canonical acceptance fixtures that register non-file-backed evidence must be aligned in the same ChangeSet
(measured: 15 of 24 tests fail against the strengthened primitive until aligned).

## Out of scope
Raw file writes and direct sqlite writes remain possible (schema.sql has zero TRIGGERs) - universal prevention
is a separate decision.
