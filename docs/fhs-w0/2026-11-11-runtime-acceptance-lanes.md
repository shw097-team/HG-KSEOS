# HG-KSEOS lane-routing — runtime acceptance note (2026-11-11, second pass)

**Scope of this note**: measured runtime facts about the lane control plane, taken from a
FHS-NEXT W0 construction root on 2026-11-11 (18:00–19:00 +08:00). It adds measurements to the
existing report on this branch; it does not repeat it and it does not ask for a merge of
anything else.

**Claim ceiling**: `SOURCE_READ` on the repositories + `HOST_RAW` on one Windows host.
Nothing here is a native admission, a policy ratification, a release, or an acceptance of any
subject. A turn that serves an arm proves routing/transport only.

**Repository state read at the time of writing** (GitHub API, not a local clone):

| repo | ref | registry/blob | value |
|---|---|---|---|
| `shw097-team/HG-KSEOS` | `main` | `config/lane-routing-registry.yaml` | `status: CANDIDATE`, `epoch: 33`, **no `retired_arms` block** |
| `shw097-team/HG-KSEOS` | `main` | `config/lane-route-slots.candidate.json` | PLAN rank 4 still `opencode-go/mimo-v2.6-pro`, `retired_arms: []` |
| live control plane (this host) | `IN_FORCE` | epoch 41 registry | `epoch: 41`, `retired_arms: opencode-go/mimo-v2.6-pro` → replacement `opencode-go/mimo-v2.6-flash` |

So the divergence originally reported on this branch **still holds two days later**, and it is
not a documentation gap: the published pool still contains the arm the owner retired.

## What was measured this round

**D1 — epoch divergence, re-measured.** `--assert-arm opencode-go/mimo-v2.6-pro` against the
published copy exits **0** (the arm is admitted, rank 4). The same call against the live epoch-41
copy exits **9** (`RETIRED_ARM`, replacement named). One arm, two answers, decided by which copy is
loaded.

**D2 — retirement is enforced on configuration, not on transport.** With the live registry
loaded, the plan-lane retirement ledger is present and `lane_arm_retirement_check.py` reports
`verdict: PASS`, `retired_still_live: []` over the three config files it reads. The relay catalog
on the same host still lists the retired model, and a direct completion request to
`opencode-go/mimo-v2.6-pro` through the loopback relay returned **HTTP 200** with a real usage
payload. Retirement therefore holds at selection time and does not hold at request time. (The
checker *does* bite when the arm is injected into a live pool — measured exit **4** on the injected
fixture — so the checker is not vacuous; it simply does not read the relay catalog.)

**D3 — the declared Codex toolchain pin no longer resolves.** `config/hermes-codex-lane.json`
pin at `main`:

```
codex_executable  …/OpenAI/Codex/bin/0ab0e7a8f3779036/codex.exe
codex_version     0.165.0-alpha.1.2
codex_sha256      0c09e45bc76433756eb2d492f6db0ce6f269967e6618f4a6ae73e2fa239694b8
```

On the measured host that path does not exist (installed builds are `5449c1f0f26f1f98` =
`0.167.0-alpha.3.2`, sha256 `4f91ae86895ff124760d70ed1630e2354ca874765c9bb61ae524b600327efc17`, and
`8dbccda2214d0643`, which carries `rg.exe` only). The resolver therefore fails closed:

```
ERR_LANE_TOOLCHAIN_BINARY_MISSING: declared binary does not exist: …\0ab0e7a8f3779036\codex.exe   exit 3
```

Every lane dispatch without an explicit operator override dies **before any model call**, which
from the outside is indistinguishable from a broken lane. This is the same failure class the repo
already recorded as a pin-refresh repair; the pin has drifted again.

**D4 — the dispatcher's assignment gate reads the published copy only.**
`scripts/hgk-lane-dispatch.py` hard-codes `ASSIGNMENT_FILE = ROOT/config/model-lane-assignment.json`.
A live-epoch arm therefore cannot be dispatched even when the operator passes the live pool:
`--pool config.live/lane-route-slots.candidate.json --require-arm opencode-go/mimo-v2.6-flash`
→ `ERR_LANE_REQUIRED_ARM_ABSENT`, and with the published pool → `ERR_ARM_NOT_IN_ASSIGNMENT`
(the published assignment chain has no `mimo-v2.6-flash` row for `VERIFY_SECURITY`). The in-force
epoch-41 assignment *does* carry it at index 1.

**D5 — a stale `transport_model` admits the writer's model as a checker arm.** The published
assignment row is:

```json
{"role": "VERIFY_SECURITY", "assigned_provider": "openai-codex", "assigned_model": "gpt-6.1-sol",
 "transport_model": "opencode-go/deepseek-v4.1-flash",
 "authority": "owner-order-20261024-s205-od01-plan-verify-gpt61sol-execute-deepseek"}
```

The gate composes the selectable set from `assigned_provider/assigned_model` **plus**
`transport_model`, so `opencode-go/deepseek-v4.1-flash` — the EXECUTE rank-1 writer arm — is listed
as assignable for `VERIFY_SECURITY`. The SoD gate does refuse the same-model pairing when it is
actually attempted (measured: exit **2**, `ERR_LANE_SOD_VIOLATION`), so the control holds at the
last gate. The exposure is that the *declaration* offers the writer's arm to the checker lane; the
only reason it cannot be used is a second gate noticing.

**D6 — stale epoch and missing admission evidence are separable refusals.** Same guard,
`--expected-epoch 33` → exit **4** (`ERR_LANE_STALE_EPOCH`, `live_epoch=35`), and a bare
`--admission ADMITTED` with no probe receipt → exit **3** (`ERR_LANE_NOT_ADMITTED`,
"a bare ADMITTED string is not admissible"). Both are correct and both are distinguishable from
the SoD refusal, which is the property a caller needs.

## What this note does not claim

- It does not propose a new epoch, a new arm, or a new retirement. Lane routing is the owner's.
- It does not touch `main`, does not merge, and carries no evidence pack, key, database or raw
  lane output.
- It does not claim the host it was measured on is representative; it is one Windows host with
  one installed Codex build and one relay.

Reproduction for D3 (no secrets involved):

```bash
python scripts/hgk-lane-toolchain.py --verify          # exit 3 on the drifted pin
python scripts/lane_arm_retirement_check.py            # exit 0 on the published copy (no ledger)
python scripts/hgk-lane-guard.py --lane VERIFY_SECURITY \
  --maker-lane EXECUTE --maker-engine codex-cli --maker-model deepseek-v4.1-flash \
  --target-engine codex-cli --target-model deepseek-v4.1-flash --target-provider opencode-go \
  --admission ADMITTED --expected-epoch 41             # exit 2, ERR_LANE_SOD_VIOLATION
```
