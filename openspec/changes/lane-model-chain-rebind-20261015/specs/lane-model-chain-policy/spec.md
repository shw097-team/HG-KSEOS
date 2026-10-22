# lane-model-chain-policy

## ADDED Requirements

### Requirement: Declared model chain per lane

The system SHALL declare, for each governance lane, an ordered model chain: exactly one default arm and at least one ordered fallback arm, in ONE authority surface per lane, and the dispatcher/resolver SHALL resolve selections exclusively from that surface.

#### Scenario: PLAN chain matches owner order
- **WHEN** the PLAN lane's declared chain is read
- **THEN** the default arm is openai-codex/gpt-6.1-sol with reasoning_effort medium (OAuth transport), fallback1 is opencode-go/glm-5.3-flash, fallback2 is opencode-go/deepseek-v4.1-flash, in that order

#### Scenario: VERIFY chain matches owner order
- **WHEN** the VERIFY_SECURITY lane's declared chain is read
- **THEN** the default arm is openai-codex/gpt-6.1-sol with reasoning_effort medium (OAuth transport), fallback1 is opencode-go/glm-5.3-flash, fallback2 is opencode-go/deepseek-v4.1-flash, in that order

#### Scenario: EXECUTE chain matches owner order
- **WHEN** the EXECUTE lane's declared chain is read
- **THEN** the default arm is opencode-go/deepseek-v4.1-flash, fallback1 is openai-codex/gpt-6-luna (OAuth transport), fallback2 is nvidia/deepseek-ai/deepseek-v4.1-flash, in that order

### Requirement: Per-session-round user re-selection

The system SHALL honor a user-ordered per-session-round lane model by consuming a round mandate through the existing fail-closed gate, and SHALL refuse to proceed when the ordered arm is not resolvable in the lane's declared chain.

#### Scenario: User names a fallback arm for the round
- **WHEN** the round mandate declares fallback1 of the EXECUTE lane (openai-codex/gpt-6-luna) and the operator dispatches with the matching require-arm
- **THEN** the gate resolves the arm in the lane pool, the dispatcher serves exactly that arm, and the receipt records required_arm == served_arm

#### Scenario: User names an arm outside the declared chain
- **WHEN** the round mandate declares a provider/model combo not present in the lane's ordered pool
- **THEN** the pre-dispatch gate refuses with ERR_MANDATE_ARM_UNRESOLVED before any spawn

### Requirement: Round exclusion lapses across rounds

The system SHALL treat round_model_exclusions as round-scoped: a NEW owner round MUST replace the exclusion block (or clear it), and the gpt-* family MUST NOT be excluded unless the new round's owner order says so.

#### Scenario: New round restores gpt admissibility
- **WHEN** a new round replaces the exclusion block with the current round's scope and no gpt- exclusion
- **THEN** check_exclusions admits openai-codex/gpt-6.1-sol on a governed dispatch
