# lane-toolchain-identity

## Purpose

Define the externally observable behaviour of lane toolchain identity: how a lane resolves its CODEX-CLI
binary, what a pre-lane identity preflight must classify, when a declared model deviation may open, and what
a receipt must carry. This capability extends the surface defined by `ao-lane-independent-verify`; it does
not replace it.

## ADDED Requirements

### Requirement: A lane resolves its binary from one declared identity and fails closed on a mismatch

The lane SHALL resolve its CODEX-CLI binary from a single declared identity (declared path + expected
version + expected sha256) and SHALL fail closed, with a typed error naming the offending build, when the
resolved build's version differs from the declared one. A lane SHALL NOT resolve its binary by `find` or
`command -v` discovery. The resolver SHALL print the resolved path, its sha256, and its `--version`.

#### Scenario: a mismatched build fails closed
- **WHEN** the declared identity names version V and the resolvable build reports a different version
- **THEN** the resolver exits non-zero with a typed error naming the offending build (path + version)
- **AND** no lane turn is spawned

#### Scenario: a matching build resolves
- **WHEN** the resolvable build's version equals the declared version
- **THEN** the resolver prints the path, sha256, and `--version` and exits 0

#### Scenario: discovery is not a resolution
- **WHEN** a lane needs its binary
- **THEN** it obtains the identity from the resolver and does not use `find` or `command -v`

### Requirement: A bounded pre-lane identity preflight classifies failures into typed codes

The lane launcher SHALL run a bounded pre-lane identity preflight (one-line echo, budget at most 120
seconds) BEFORE any long lane, and SHALL classify the outcome into `LANE_TOOLCHAIN_MISMATCH` or
`LANE_MODEL_REFUSED`. A models-cache schema error, an unknown subcommand or flag, or an unsupported stdin
form SHALL be classified as `LANE_TOOLCHAIN_MISMATCH`. A genuine provider refusal on the declared model,
from a build that otherwise matches the declared identity, SHALL be classified as `LANE_MODEL_REFUSED`.

#### Scenario: a models-cache schema error is a harness fault
- **WHEN** the resolved build cannot parse the isolated home's `models_cache.json` (`failed to load models cache: missing field ...`)
- **THEN** the class is `LANE_TOOLCHAIN_MISMATCH` and the offending build is named

#### Scenario: an unsupported stdin form is a harness fault
- **WHEN** the resolved build rejects the stdin form (`error: unexpected argument '-' found`)
- **THEN** the class is `LANE_TOOLCHAIN_MISMATCH`
- **AND** the run does not report a model refusal

#### Scenario: a provider refusal on a matching build is a model refusal
- **WHEN** a build matching the declared identity is refused by the provider on the declared model
- **THEN** the class is `LANE_MODEL_REFUSED` and the preflight raw output is recorded

#### Scenario: the preflight is bounded
- **WHEN** the preflight is run
- **THEN** it completes within its budget and does not replace the long lane's own timeout accounting

### Requirement: Only a model refusal opens a declared model deviation, and the receipt is complete

Only `LANE_MODEL_REFUSED` SHALL open a declared model deviation. A `LANE_TOOLCHAIN_MISMATCH` SHALL refuse to
substitute and SHALL name the offending build. Every receipt SHALL carry the CODEX-CLI path and version, the
declared model, the served model, the error class, and the preflight raw output.

#### Scenario: a toolchain mismatch refuses to substitute
- **WHEN** the class is `LANE_TOOLCHAIN_MISMATCH`
- **THEN** no model substitution occurs and the offending build is named in the receipt

#### Scenario: a model refusal may open a deviation
- **WHEN** the class is `LANE_MODEL_REFUSED`
- **THEN** the declared model deviation path is reachable and recorded

#### Scenario: the receipt carries the identity and the evidence
- **WHEN** any preflight run completes
- **THEN** the receipt carries `codex_cli`, `codex_cli_version`, `declared_model`, `served_model`, `error_class`, and the preflight raw output

### Requirement: A verdict is bound to the artifact bytes it saw

A verdict SHALL be bound to the artifact bytes it saw. Any post-verdict rebuild, digest refresh, or
published-asset replacement SHALL invalidate that verdict by policy.

#### Scenario: a post-verdict change invalidates the verdict
- **WHEN** the artifact bytes a verdict saw are rebuilt, re-digested, or replaced after the verdict
- **THEN** the verdict is invalid by policy and must be re-derived
