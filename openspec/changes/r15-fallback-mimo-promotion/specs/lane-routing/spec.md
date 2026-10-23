# lane-routing — fallback re-order (epoch 33)

## ADDED Requirements

### Requirement: The deprecated arm is deleted from every selectable position

`opencode-go/minimax-m3.1-flash-free` SHALL be removed from every *selectable* position —
the Hermes `model.default`, the Hermes `fallback_providers` chain, and every HG-KSEOS lane
`ordered_pool` — because the provider answers HTTP 410 `ModelDeprecated` for it (measured
2026-10-23). Historical records (change logs, round notes, evidence files) SHALL retain the id
verbatim and SHALL NOT be rewritten.

#### Scenario: No selectable position names the deprecated arm

- **WHEN** the Hermes config and every `ordered_pool` entry are scanned
- **THEN** no `model.default`, no `fallback_providers[].model` and no `ordered_pool[].model`
  equals `minimax-m3.1-flash-free`
- **AND** the string still appears in history/change-log/evidence text, unmodified

### Requirement: MiMo-V2.6-Flash is the first fallback of the main model, on its measured wire

The Hermes fallback chain for the main model `opencode-go/deepseek-v4.1-flash` SHALL place
`opencode-go/mimo-v2.6-flash` at position 1 and SHALL pin `api_mode: chat_completions` on that
entry, because the model answers 200 on `/v1/chat/completions` and 400 `ModelProtocolUnsupported`
on `/v1/messages`.

#### Scenario: The first fallback resolves to a live arm and a live wire

- **WHEN** the fallback chain is loaded
- **THEN** entry 1 is `provider=opencode-go`, `model=mimo-v2.6-flash`, `api_mode=chat_completions`
- **AND** a live probe of that arm on that wire returns HTTP 200
- **AND** `deepseek-v4.1-flash` remains reachable in the chain (position 2) rather than being deleted

### Requirement: Declared default and served session are the same arm

The Hermes `model.default` SHALL equal the arm the governed lanes declare at rank 1
(`opencode-go/deepseek-v4.1-flash`), so an unpinned entry point cannot start a turn on a dead or
different arm. A session pin SHALL NOT be treated as evidence about the lane binding.

#### Scenario: Unpinned entry point starts on the declared arm

- **WHEN** a new session is created without a per-session model pin
- **THEN** `model.default` names `opencode-go/deepseek-v4.1-flash`
- **AND** it equals `ordered_pool[0].model` for PLAN, EXECUTE and VERIFY_SECURITY
