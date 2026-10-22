## 1. Route the VERIFY lane for real

- [ ] 1.1 Probe both mandated arms and one live sibling with bounded timeouts; record http code, elapsed seconds and whether content came back
- [ ] 1.2 Record the current delegation route (provider and model) as the restore point, with a readback
- [ ] 1.3 Set the delegation route to the mandated VERIFY model, dispatch the verify lane, then restore the route and read both values back
- [ ] 1.4 Capture the runtime log line that names the verify session's model and provider as the authoritative routing evidence

## 2. Correct the policy statement

- [ ] 2.1 Amend the lane policy file to state that a per-task model/provider override exists on the kanban dispatch surface, and that only a lane-name-indexed fallback registry is absent
- [ ] 2.2 Reconcile the policy file's verify-lane model field with its own claim-ceiling text so both name the same model

## 3. Land the candidate repair set

- [ ] 3.1 Admit a TaskSpec and a WorkOrder for the candidate repair set under the existing admission pattern
- [ ] 3.2 Apply the candidate patch inside an admitted isolated worktree, then run the suite and record the counts
- [ ] 3.3 Obtain an independent check from a lane on a different model, made to the checker as a claim-based brief

## 4. Re-verify the two live-runtime defects on the canonical store

- [ ] 4.1 Only after 3.2 lands, run the suite against the canonical store and record the store's event count before and after
- [ ] 4.2 If the repair has not landed, run against an override store and state in the handoff that the canonical store was not exercised
- [ ] 4.3 Record both defects' status as re-derived rather than repeated

## 5. Evidence and handoff

- [ ] 5.1 Freeze artifacts first, generate the single evidence file last, mirror it to the declared roots and confirm the digests are equal
- [ ] 5.2 State the claim ceiling as no mutation of the subject store plus the enumerated write ledger
