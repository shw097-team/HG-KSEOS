## Why

The operator mandated a three-lane model segregation on this runtime:
PLAN = GPT 6.1 SOL (OPEN AI OAuth), EXECUTE = DeepSeek V4.1 Flash (OPENCODE GO),
VERIFY / SECURITY = GLM-5.3-Flash (NVIDIA NIM primary, OPENCODE GO fallback).
A predecessor governed round (FAR ROUTE-LANE-001) concluded that the segregation was
"declared and partially wired", that the VERIFY arm had never produced a usable verdict
(one arm silent, one arm over budget), and that the policy file recorded Hermes as having
no per-lane fallback surface at all. A successor round (this one, REQ-FAR-LANE-VERIFY-002)
then measured that a recent governed round's alleged INDEPENDENT verification had in fact
been executed inside the orchestrator's own main loop on the EXECUTOR's model, so the
maker/checker model separation the policy claimed did not hold in practice, and it
measured that the mandated VERIFY model DOES answer today (NVIDIA NIM 200 in 4.48 s;
OPENCODE GO fallback 200 in 1.22 s) while the plain non-Flash sibling still hangs (a 60 s
timeout with no response). The gap is therefore a wiring and evidence problem, not a model
availability problem, and it is unfixed: every round that verifies in-loop silently
collapses maker and checker onto one model.

## What Changes

- Add an explicit, receipted VERIFY-lane dispatch procedure: probe the mandated model on both
  arms before use, point the delegation route at the mandated model for the duration of the
  verify dispatch only, and record the restore step and the authoritative model evidence.
- Recognise and use the per-task model/provider override surface on the kanban dispatcher as
  the per-card routing surface, and correct the policy file's "no per-lane surface" statement.
- State the honest claim ceiling for a round as NO_SUBJECT_STORE_MUTATION plus an enumerated
  write ledger, and forbid blanket no-canonical-mutation wording.
- Land the already-produced candidate repair set through a WorkOrder and the gate before any
  canonical re-verification of the two live-runtime defects D15 and D16, because the suite is
  not hermetic until that repair is applied.

## Impact

Affected: Hermes runtime configuration (delegation route only, restored after each verify
dispatch), the lane policy file's wiring statement, the kanban dispatch surface, and the
round's evidence and claim-ceiling conventions. Not affected: provider credentials, the
canonical spine schema, production or live SQS paths, and any Stage-3 activity.
