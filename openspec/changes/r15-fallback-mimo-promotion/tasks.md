# Tasks — R15 fallback re-order (delete MiniMax, promote MiMo-V2.6-Flash)

Ceiling: CANDIDATE-ONLY for every HG-KSEOS artefact. The Hermes config change is a deployment-plane
change authorized by the owner; local green is not an acceptance and not a release.

## 0. Pre-flight

- [ ] 0.1 Measure all four candidate arms on every relevant wire; store raw JSON under
  `var/R15-MODEL-FALLBACK-20261023/probes/` (chat/completions, /v1/messages, /v1/responses)
- [ ] 0.2 Capture the Hermes config baseline + sha256 before any write
- [ ] 0.3 Capture the protocol resolver table (`_OPENCODE_API_MODE_PREFIXES`) as code truth

## 1. HG-KSEOS admission

- [ ] 1.1 Issue real WorkOrders through `ProjectLifecycleController` (project `HGK-PRJ-R15-20261023r15`)
- [ ] 1.2 Read the work orders back **from the spine**, not from the objects that wrote them

## 2. Governed execution surfaces

- [ ] 2.1 KANBAN — board + gate cards for the open obligations
- [ ] 2.2 SWARM — genuine parallel independent lanes with raw receipts
- [ ] 2.3 GSTACK — registry `ACTIVE_SELECTED` + `route(flow)` evidence
- [ ] 2.4 OPENSPEC — this change validates (`openspec validate --strict`)

## 3. Apply (atomic, bounded writer = Codex EXECUTE lane)

- [ ] 3.1 `~/.hermes/config.yaml`: `model.default` → `deepseek-v4.1-flash`; delete the deprecated
  fallback entry; `mimo-v2.6-flash` at position 1 with `api_mode: chat_completions`
- [ ] 3.2 `config/lane-route-slots.candidate.json` rev 22 — deprecated arm removed from every pool
- [ ] 3.3 `config/model-lane-assignment.json` rev 33 — derived from the pool
- [ ] 3.4 `config/lane-routing-registry.yaml` epoch 33 — fallbacks + source pin
- [ ] 3.5 `config/hermes-codex-lane.json` — fallbacks / child models / round note
- [ ] 3.6 `AGENTS.md` lane-chain contract + `config/hermes.json` owner mandate

## 4. Self-check and self-repair

- [ ] 4.1 V1 live protocol re-probe of every arm left in the chain
- [ ] 4.2 V2 config load + per-entry api_mode resolution (mimo → chat_completions, gpt-6-luna →
  codex_responses)
- [ ] 4.3 V3 test denominator by SET comparison (NEW must be 0)
- [ ] 4.4 V4 dead-id scan: no selectable position names the deprecated arm
- [ ] 4.5 Repair every finding, then re-run the affected set + full denominator

## 5. Independent acceptance

- [ ] 5.1 Codex `VERIFY_SECURITY` lane (separate process, own evidence path, `served_arm ==
  require_arm == opencode-go/deepseek-v4.1-flash`) emits a verdict
- [ ] 5.2 Record the verdict through `spine.record_workorder_result` (maker does not self-judge)

## 6. Evolution

- [ ] 6.1 Register TTs found this round (relay catalog gap; resolver dependency)
- [ ] 6.2 Update the SBL/HGK skills with what this round actually measured
