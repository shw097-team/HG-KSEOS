# Proposal — R15 fallback re-order: delete MiniMax, promote MiMo-V2.6-Flash (fallback1)

## Why

Owner order (2026-10-23): the main model `DEEPSEEK V4.1 FLASH (OPENCODE GO)` must lose
`MiniMax M3.1 Flash` from its fallback-first position; `MiMo-V2.6-Flash (OPENCODE GO)` — previously
fallback-2 — takes fallback-1. The owner also granted maximum pre-authorization to execute the FAR
ruling directly, and mandated all three governed lanes on `opencode-go/deepseek-v4.1-flash`.

Measured on 2026-10-23 (`var/R15-MODEL-FALLBACK-20261023/probes/`):

| arm | protocol probed | result |
|---|---|---|
| `minimax-m3.1-flash-free` | chat/completions | **HTTP 410 `ModelDeprecated`** |
| `minimax-m3.1-flash` | chat/completions | 200 |
| `mimo-v2.6-flash` | chat/completions | 200 |
| `mimo-v2.6-flash` | /v1/messages (anthropic) | **HTTP 400 `ModelProtocolUnsupported`** |
| `mimo-v2.6-flash` | /v1/responses | 200 |
| `deepseek-v4.1-flash` | /v1/messages | 200 |

Two facts follow. **(1)** The arm being deleted is already dead at the provider, and the Hermes
`model.default` pointed at it too — so the configured primary and its "first fallback" were the same
deprecated id. **(2)** MiMo cannot ride the Anthropic wire that this Hermes home declares globally
(`model.api_mode: anthropic_messages`); its live wire is chat/completions, which the fallback
resolver does derive per model (`_fallback_api_mode_resolved` → `opencode_model_api_mode`), but the
derivation is now pinned explicitly on the entry so a future resolver change cannot silently regress it.

## What changes

### 1. Hermes deployment plane (`~/.hermes/config.yaml`)

- `model.default`: `minimax-m3.1-flash-free` → `deepseek-v4.1-flash`.
- `fallback_providers`: the `minimax-m3.1-flash-free` entry is **deleted**; the chain becomes
  `mimo-v2.6-flash (1, api_mode: chat_completions)` → `deepseek-v4.1-flash (2)` →
  `nvidia/deepseek-ai/deepseek-v4.1-flash (3)` → `gpt-6-luna (4)`.
- `model.api_mode`, `moa`, `auxiliary` are **not** touched (non-goals).

### 2. HG-KSEOS declaration plane (candidate)

- `config/lane-route-slots.candidate.json` rev 22 — every lane pool loses the deprecated
  `minimax-m3.1-flash-free` entry; ranks stay contiguous; EXECUTE/VERIFY/PLAN rank-1 remain
  `opencode-go/deepseek-v4.1-flash`.
- `config/model-lane-assignment.json` rev 33 and `config/lane-routing-registry.yaml` epoch 33 —
  follow the pool (derived, not independently declared); history preserved.
- `config/hermes-codex-lane.json` — `model_fallbacks` loses the deprecated id;
  `execute_lane_child_models` pinned to `deepseek-v4.1-flash`; round note appended.
- `AGENTS.md` lane-chain contract section updated to the same truth.

### 3. What is deliberately NOT done

- `mimo-v2.6-flash` is **not** added to the sealed Codex lane: relay 10101's catalog exposes only
  `opencode-go/mimo-v2.6-pro`. Adding it would create a declared-but-unservable arm (TT-R15-A).
- No promotion. Every HG-KSEOS artefact keeps `status: CANDIDATE`; the Hermes config change is a
  deployment-plane change authorized by the owner, not an acceptance.

## Non-goals

- No global wire-protocol change (`model.api_mode`).
- No removal of the `nvidia` or `openai-codex` tail arms.
- No claim of independent model-family verification: all three lanes run one model by owner order
  (`OPEN_OWNER_ORDERED`); process/lane/evidence-path separation only.
