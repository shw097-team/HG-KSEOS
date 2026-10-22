# Design: lane-toolchain-identity-and-failure-classification

## Context

The measured A/B is a single-variable experiment: the binary is the only thing that changed (same isolated
CODEX_HOME, same `auth.json`, same model `gpt-6.1-sol`, same reasoning effort, same prompt, same sandbox).
The 0.147 build returns HTTP 400 exit 1; the 0.162 build returns `OK`, 5965 tokens, exit 0. The "provider
block" was therefore a **local toolchain artifact**, and the declared model substitution that followed it
was unnecessary. The design question is: what is the lowest-friction change that makes a lane's identity
deterministic and its failures typed, and which changes would be *too much*?

## D1 — resolve the lane binary from one declared identity, fail closed

**Chosen.** A single resolver `scripts/hgk-lane-toolchain.py` resolves the binary from a DECLARED identity
(declared path + expected version + expected sha256) and prints path, sha256, and `--version`. It **fails
closed** — non-zero, typed, naming the offending build — when the resolved build's version differs from the
declared one. Lane scripts obtain their identity from the resolver and use no `find` / `command -v`.

**Rejected:** keep ad-hoc discovery and merely log the version. The measured failure came precisely from an
unchecked discovery; logging it would have produced the same false green one layer later.
**Rejected:** pin by PATH order. Three builds coexist; PATH order is environmental state, not a declaration,
and the declaration is the whole point.

## D2 — a bounded pre-lane identity preflight with typed classification

**Chosen.** Before any long lane, run a one-line echo (`<=120s` budget) through the resolved
binary + isolated home + declared model, and classify the outcome into typed codes:

| Observed signature | Error class | Meaning |
|---|---|---|
| models-cache schema error (`failed to load models cache: missing field ...`) | `LANE_TOOLCHAIN_MISMATCH` | the build cannot parse the home's newer-schema cache — harness fault |
| `Model metadata for <model> not found` chained after the cache error | `LANE_TOOLCHAIN_MISMATCH` | the build lacks model metadata — harness fault |
| unknown subcommand/flag, or the unsupported stdin form (`error: unexpected argument '-' found`) | `LANE_TOOLCHAIN_MISMATCH` | CLI surface mismatch — harness fault |
| a genuine provider refusal on the declared model, from a build that otherwise matches | `LANE_MODEL_REFUSED` | the provider refuses the declared model |

**Rejected:** classify by exit code alone. HTTP 400 (exit 1) and a harness parse failure both exit non-zero;
the discriminator is the *error class*, not the numeric code.

## D3 — only `LANE_MODEL_REFUSED` opens a declared model deviation

**Chosen.** A `LANE_TOOLCHAIN_MISMATCH` must **refuse to substitute** and must name the offending build
(path + version). Only a `LANE_MODEL_REFUSED` may open a declared model deviation, and the deviation is
what the receipt records.

**Rejected:** substitute the model whenever the declared model fails. The measured A/B shows the "provider
block" was a local toolchain artifact; substituting on it would have masked a harness fault as a provider
policy decision — the exact misinformation path this work exists to remove.

## D4 — verdict bound to the bytes it saw (documented rule, not implemented here)

**Chosen (documented).** A verdict is bound to the artifact bytes it saw; any post-verdict rebuild / digest
refresh / published-asset replacement invalidates that verdict by policy.

**Rejected:** building the invalidation machinery in this change. The rule is a governance declaration; its
enforcement belongs to a later, separately-admitted change. This change only states it.

## Receipt schema (additive)

| Field | Meaning |
|---|---|
| `codex_cli` | resolved path of the lane binary |
| `codex_cli_version` | `--version` of the resolved binary |
| `declared_model` | the model the lane declared |
| `served_model` | the model actually served (`null` when no turn was served) |
| `error_class` | `LANE_TOOLCHAIN_MISMATCH` / `LANE_MODEL_REFUSED` / `null` |
| `preflight_raw` | the preflight's raw output |

## Test strategy

Deterministic only. Coverage: the resolver fails closed on a version mismatch and resolves on a match; the
classifier fires for each signature in D2 on **recorded raw preflight samples**; substitution is refused
under `LANE_TOOLCHAIN_MISMATCH` and permitted under `LANE_MODEL_REFUSED`. No test may depend on the network,
a real model, the relay, or the developer's real Codex home.

## Rollback

Everything is additive: new files plus additive receipt fields. Reverting is deleting the new files and the
additive fields. Nothing here writes the canonical store, so rollback needs no spine action.

## Non-claims

- Not an acceptance. CANDIDATE only — no promotion, no archive, no main-spec write.
- No claim that the host's three coexisting builds are reconciled; only that a lane's identity is declared
  and checked.
- D4 is a documented rule, not an implemented mechanism.
