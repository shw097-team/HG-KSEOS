## Why

The operator mandate `PLAN = gpt-6.1-sol / openai-codex`, `EXECUTE = Codex CLI +
deepseek-v4.1-flash / opencode-go`, `VERIFY-SECURITY = glm-5.3-flash / opencode-go` is
declared but not durably enforced. Governed round FAR-LANE-SOD-003 produced a 25-defect
falsifiable register (lane A). The defects fall into five families: the routing facts are
duplicated across `assignment`, `sod`, `lane_chains`, `effective_wiring` and legacy prose so
no partial edit stays valid (D1, D9, D13, D14); no per-lane dispatch override exists and the
only controls are a global delegation pin and a global fallback chain that mix roles (D2, D3,
D4, D5, D6); liveness of an arm is measured by a direct completion that does not prove the
arm can serve a lane (D7, D8, D11, D12); the mutation/promotion path lacks an immutable event
envelope and a recoverable API (D15, D16, D17, D18, D20, D21, D22); and the checker tooling
scans its own output and returns PASS over broken citations while the contract denominator is
incomplete and named-method adapters are absent (D23, D24, D25). D10 and D19 remain recorded
deviations that must be closed rather than rewritten.

## What Changes

- Add one single-source-of-truth routing registry (`config/lane-routing-registry.yaml`) and
  derive the whole policy from it deterministically, with a strict drift gate that names every
  disagreement as a JSON pointer over each live projection site.
- Add a pre-dispatch SoD gate that refuses when the checker model equals the maker model,
  when the arm is not lane-shaped ADMITTED, or when the policy epoch/source digest is stale.
- Add a lane-shaped admission probe that never infers ADMITTED from a direct completion, and
  an admission record model with ADMITTED / REFUSED / UNPROVEN states.
- Repair the artifact gate so its own output and registered producer outputs are excluded from
  the scan, findings are semantic-stable over identical frozen inputs, and the input digest
  and output path are required.
- Add a fail-closed relay supervisor for the sealed lane that restarts only the HG-KSEOS
  launcher script and reports a JSON lease receipt.
- Adopt all of the above as CANDIDATE; nothing in the live install or the canonical policy is
  changed. Activation requires a separate HGK-authorized generation binding.

## Non-goals

- No production, release, or deploy authorization; `sqs_live_trading: NOT_AUTHORIZED` stands.
- No execution of SQP1 or Stage-3; no Stage-3 contract is compiled here.
- No change to credentials, the Shared Spine schema, or any acceptance receipt.
- No claim that provider separation holds: EXECUTE and VERIFY both use opencode-go, so only
  the model axis is required.

## Impact

Affected: `config/lane-routing-registry.yaml` (new), `src/hg_kseos/lane_policy.py` and
`lane_admission.py` (new), `scripts/hgk-lane-policy.py`, `hgk-lane-guard.py`,
`probe-hgk-lane.py`, `hgk-artifact-gate.py`, `supervise-hgk-opencodex.ps1` (new),
`tests/test_lane_policy.py` (new). Not affected: the live Hermes install,
`%LOCALAPPDATA%\HG-KSEOS\**`, `C:\Users\user\.codex\**`, the Shared Spine database, and
`config/model-lane-assignment.json` (read-only drift source).
