# Proposal: lane toolchain identity — one declared lane binary, a bounded pre-lane identity preflight, and typed failure classification

## Why

- Three different Codex CLI builds exist simultaneously on this host: 0.147.0-alpha.6.5 at C:/Users/user/AppData/Local/HG-KSEOS/runtime/codex-0.147.0-alpha.6.5/codex.exe, 0.154.0-alpha.6.2 at C:/Users/user/AppData/Local/HG-KSEOS/codex-hermes/.sandbox-bin/codex.exe, and 0.162.0-alpha.17.2 at C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe.
- A VERIFY/SECURITY lane resolved the OLD 0.147 build by ad-hoc disk/PATH discovery. That build cannot parse the isolated CODEX_HOME's newer-schema models_cache.json (`failed to load models cache: missing field `supports_parallel_tool_calls``), therefore has no model metadata (`Model metadata for `gpt-6.1-sol` not found`), therefore the ChatGPT(OAuth) backend answers HTTP 400 `The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.` The old build also rejects `codex exec ... -` (`error: unexpected argument '-' found`), so the lane lost its command-line model pin.
- Measured A/B, single variable = the binary, everything else identical (same isolated CODEX_HOME, same auth.json, same model gpt-6.1-sol, same reasoning effort, same prompt, same sandbox): 0.147 build => HTTP 400 exit 1; 0.162 build => `OK`, 5965 tokens, exit 0. So the 'provider block' was a LOCAL TOOLCHAIN ARTIFACT and the subsequent declared model substitution was unnecessary.

## What changes

1. **One canonical lane-toolchain resolver** (`scripts/hgk-lane-toolchain.py`): resolves the lane binary from a single DECLARED identity, prints path + sha256 + `--version`, and FAILS CLOSED when the resolved build's version differs from the declared one. Lane scripts must not use `find` / `command -v` discovery.
2. **A bounded pre-lane identity preflight** (one-line echo, <=120s budget) run BEFORE any long lane, classifying failures into typed codes: `LANE_TOOLCHAIN_MISMATCH` (models-cache schema error, unknown subcommand/flag, stdin form unsupported -> a harness fault) versus `LANE_MODEL_REFUSED` (a genuine provider refusal on the declared model).
3. **Only `LANE_MODEL_REFUSED` may open a declared model deviation.** A `LANE_TOOLCHAIN_MISMATCH` must refuse to substitute and must name the offending build. The receipt must carry: `codex_cli` path + version, `declared_model`, `served_model`, error class, and the preflight raw output.
4. **A governance rule** (documented, not necessarily implemented in this change): a verdict is bound to the artifact bytes it saw; any post-verdict rebuild / digest refresh / published-asset replacement invalidates that verdict by policy.

## Impact

- New files only: `scripts/hgk-lane-toolchain.py` (the resolver) plus an additive preflight entry point the lane launcher invokes before the long turn.
- Existing lane scripts consume the resolver's identity instead of discovering a binary by hand; the declared lane identity becomes the single source of truth for which build a lane runs.
- New receipt fields (`codex_cli`, `codex_cli_version`, `declared_model`, `served_model`, `error_class`, `preflight_raw`) are additive; a consumer matching on the existing fallback code keeps working.
- No promotion, no archive, no main-spec write, no `config/` or route edits. Everything is additive.

## Out of scope / Non-goals

- Not an acceptance. This is a CANDIDATE change: nothing is promoted, archived, or written to the canonical store.
- No install, removal or relocation of any Codex build. This change makes a lane's identity honest and checked; it does not curate the host's three coexisting binaries. Which builds should exist is the owner's call.
- The governance rule (piece 4) is declared and documented here; its enforcement machinery is not built in this change.
- No provider/model routing change: a `LANE_MODEL_REFUSED` still needs the owner's existing declared-deviation path, unchanged.
