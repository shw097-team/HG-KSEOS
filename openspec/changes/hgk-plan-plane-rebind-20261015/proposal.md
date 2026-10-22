# Change: hgk-plan-plane-rebind-20261015

## Why
The in-Hermes PLAN & Orchestrator plane was rebound to `opencode-go/glm-5.3-flash` at
`model-lane-assignment.json` revision 19 (owner order 2026-10-15, `declared_at_utc`
2026-10-15T11:25:47Z) because the `openai-codex/gpt-6.1-sol` arm was measured exhausted
(`status=429`, `2026-10-15T19:00:30` local).

That premise no longer holds: on the same arm, four VERIFY_SECURITY lane turns completed today
with `required_arm == served_arm == openai-codex/gpt-6.1-sol` and `usage_receipt_ok: true`
(ACC8 566.65s, ACC9 473.58s, ACC10 316.8s, ACC11 in flight). The current session mandate again
names PLAN = GPT 6.1 SOL-MEDIUM (OpenAI OAuth).

## What changes
- Bind the **PLAN & Orchestrator plane** to `gpt-6.1-sol` / `openai-codex` / effort `medium`, in the
  **governed profile only** (`<HERMES_HOME>/profiles/hgk-governed/config.yaml`), alongside
  `governed_runtime`. The canonical default profile is NOT touched (O4).
- No route, registry, relay or dispatcher change.

## Plane separation this relies on (from `effective_wiring.main_agent`)
| Plane | Binding surface |
|---|---|
| PLAN & Orchestrator (in-Hermes) | `config.yaml model.default` + `model.provider` |
| session model service | per-session picker (`state.db::sessions.model`), pinned at session start |
| EXECUTE | Codex CLI sealed lane (`--lane EXECUTE`) |
`--lane` accepts `PLAN | EXECUTE | VERIFY_SECURITY`, so PLAN is a first-class lane token.

## Not claimed
- PLAN = VERIFY = the same model, so **plan-vs-checker model independence is ABSENT**; only process
  independence (separate process, read-only, fresh context, forced re-derivation) remains.
- A binding is a DECLARATION. That the PLAN plane is *served* by gpt-6.1-sol must be shown by a
  served-arm receipt from a session started after the rebind; this change does not assert it.
- KANBAN / SWARM / OPENSPEC are orchestration surfaces, NOT model routers: enabling them does not by
  itself route PLAN to any model. GSTACK has no separate implementation in this repo.
