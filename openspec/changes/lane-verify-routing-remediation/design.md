## Context

HG-KSEOS is the sole control plane; the Hermes runtime is its governed Runtime/Orchestration
Plane. A model may therefore only be used by a lane if the round can show, from
authoritative records, which model actually served the call.

## Decisions

1. **Probe before declare.** Every arm of every lane is probed live with a bounded timeout
   and both a catalogue read and a completion attempt before the arm is described as wired.
   Reason: on this host a model the endpoint lists is not necessarily a model that answers
   (the plain GLM-5.3 sibling hangs while the Flash variant answers in seconds).
2. **Route by the delegation pin, restore immediately.** The measured mechanism is to set the
   delegation provider and model to the mandated VERIFY model, dispatch the verify lane, then
   restore. Evidence is the runtime log line naming the model and provider of the verify
   session, never the delegation banner.
3. **Prefer the per-task override where a board drives the dispatch.** The kanban dispatcher
   accepts a per-task model and provider, which scopes the override to one card instead of the
   whole runtime.
4. **Keep the mandated dimension under failover.** If the primary provider degrades, keep the
   model and switch provider to the fallback arm rather than switching to an arbitrary model.
5. **Ceiling wording.** A round claims no mutation of the SUBJECT store and enumerates every
   write it caused; it never claims that no canonical write happened.
6. **Apply before re-verify.** Re-verifying the non-hermetic suite on the canonical store
   before the hermeticity repair lands would itself cause an undisclosed write, so the repair
   lands first, or the re-verification runs against an override store and says so.

## Risks

- A mid-session route change affects any other dispatch issued while it is in force; the
  restore step must be executed immediately and its readback recorded.
- A silent provider downgrade can be mistaken for a routed lane; only the runtime log closes
  this.
- The candidate repair's environment-only database resolver is not a write-denial boundary;
  it must not be treated as one.

## Rollback

Restore the delegation route to its recorded prior value (provider openai-codex, model
gpt-6.1-sol at the time of writing) and read it back; revert the policy-file statement edit;
abandon the change before any spec is promoted.
