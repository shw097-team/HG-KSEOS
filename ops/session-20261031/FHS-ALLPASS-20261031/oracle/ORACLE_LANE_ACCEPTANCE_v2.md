# ORACLE — lane acceptance, v2 (2026-10-31)

Supersedes `ORACLE_LANE_ACCEPTANCE.md` (the v1 that the PLAN lane wrote in sitting B). v1 is kept unedited as
evidence: it is the artefact that proves the contract defect, because clause C2 asks every child to echo
`NONCE-PLAN-LANEACC-20261031-A` — sitting B's nonce — and then treats a child that echoes its own nonce as a
failure.

## The defect in v1, measured

| Sitting | Brief's demanded nonce | Lane's own nonce | Child behaviour | Dispatcher code |
| --- | --- | --- | --- | --- |
| B | `…-A` | `…-B` | ran 399 s, exit 0, echoed `…-A` as instructed | `ERR_NO_ARM_EMITTED_NONCE` |
| C | `…-C` | `…-C` | 154.5 s, echoed `…-C`, delivered a verdict | `ok` |

The arm served both times. v1's C2 made a correct child look like a mute arm, and the frozen code then named the
arm as the failure.

## v2 contract

1. One **round seed** per round (`--round-seed FHS-ALLPASS-20261031`), shared by every sitting.
2. One **nonce per sitting**, derived from the seed and the sitting label (`--sitting`), recorded on the receipt
   as `round_seed`, `sitting`, `nonce_contract`.
3. A lane passes only if it echoes the nonce **of its own sitting**. Echoing another sitting's nonce is a FAIL of
   that sitting — never of the arm, and never `ERR_NO_ARM_EMITTED_NONCE`.
4. C1's substance is unchanged: required == served, rank 1, no substitution, no fallback.

## Per-lane transport (measured this round)

| Lane | Arm | Transport |
| --- | --- | --- |
| PLAN | `openai-codex/gpt-6.1-sol` (medium) | OAuth upstream + `--codex-home C:/Users/user/.codex --allow-human-home-transport` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | **default loopback relay** — omit `--relay-base` |
| VERIFY_SECURITY | `openai-codex/gpt-6.1-sol` (medium) | OAuth upstream, as PLAN |

The transport is a property of the **arm's provider**, not a global flag. v1's recipe carried the OAuth
`--relay-base` on every dispatch, and that is why EXECUTE looked unpinnable:

- `--require-arm opencode-go/deepseek-v4.1-flash` **with** `--relay-base …/backend-api/codex` → exit 3 in 2.8 s,
  "model is not supported when using Codex with a ChatGPT account", receipt `required_arm: null`.
- the same pin **without** `--relay-base` → `ok: true` in 2.7 s, `required_arm == served_arm ==
  opencode-go/deepseek-v4.1-flash`, nonce echoed.

D-16 was not the pin. The dispatcher now refuses the incompatible pair before any spawn
(`ERR_RELAY_BASE_INCOMPATIBLE_WITH_ARM`), and the pin is recorded on failure as well as success.

## Sandbox rule (v1 was silent; that silence cost a sitting)

`--guard-subject` is a **digest anchor**, not a write grant. `--sandbox workspace-write` roots at the dispatched
repository, so a subject outside it can be read and hashed but not written. A checker pointed at an outside
subject answers "outside the sandbox's writable roots" — a fact about the write root, not about the arm and not a
FAIL of the subject. v2 requires the subject **inside** the repository
(`HG-KSEOS/fhs_msc_handoff_20261030/WP-FHS-17/`), and the dispatcher emits `WARN_GUARD_SUBJECT_OUTSIDE_REPO`
when it is not.

## What a lane PASS means

That the arm served that sitting, on the transport its provider requires, and echoed that sitting's nonce. It
does **not** mean the model agreed with anything, and it does not mean the subject passed. Lane acceptance and
subject acceptance are different claims and are recorded separately.
