# FHS W0 — Engineering Entry (2026-11-12)

> Navigation and boundary only. Reading this grants no permission. It is not a WorkOrder, a Permit, a Policy, a
> compiler output, a protected-checker receipt or a release. The control plane is HG-KSEOS; the governance contract is
> Fabric; the product engineering entry is SBL.

## 0. What is published

| item | value |
|---|---|
| lane control plane | epoch **41** (registry `epoch 41` / `contract_epoch 41`, assignment `revision 44` / `registry_epoch 41`, pool `revision 37` / `epoch 41`) |
| OD-4 removal | `mimo-v2.6-pro`, `glm-5.3`, `glm-5.3-flash`, `z-ai/glm-5.3`, `z-ai/glm-5.3-flash`, `minimax-m3.1-flash-free` — absent from every selectable surface |
| merges | PR #20 `e947cef0ea2b`, PR #21 `55b264752e8c`, PR #22 `5bc44ec05e28`, PR #19 `e5b4683c9263` |
| tag | `fhs-w0-epoch41-20261112` |
| routes | PLAN `gpt-6.1-sol` · EXECUTE `deepseek-v4.1-flash` · VERIFY_SECURITY `gpt-6.1-sol` (medium), arms == lane_chains == pool order |

## 1. How to reproduce the green

```bash
# 1. the repository's own drift validator  (expect: fatal false, 0 fatal errors, 0 debt, 87 sites)
python scripts/hgk-lane-policy.py validate

# 2. dispatch a lane turn (expect: ok true, served_arm_assigned true, usage_receipt_ok true)
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY --prompt "echo TOKEN" --nonce TOKEN \
  --pool config/lane-route-slots.candidate.json

# 3. tree-level checks (expect: selfcheck 16/16, G19 394/394)
python ops/selfcheck.py
```

A PASS is a file with a sha256 and a command that reproduces it. A model vote, a manifest entry or a digest match is
not a pass.

## 2. Where the evidence lives

| artefact | path |
|---|---|
| frozen acceptance contract (F1–F7) | `docs/ACCEPTANCE_CONTRACT_FROZEN.json` |
| final verification battery | round `out/W0_FINAL_VERIFICATION_BATTERY.json` |
| evidence index (156 files, hashes) | round `docs/EVIDENCE_INDEX.md` |
| retirement gate (POS/NEG) | round `out/W0_RETIREMENT_GATE{,_NEG}.json` |
| import supersession | `provenance/SOURCE_IMPORT_MAP_R4_OD4.json` |
| primary configuration declaration | `provenance/PRIMARY_CONFIG_DECLARATION.json` |

## 3. Boundaries an external team must respect

1. `config/` is the in-force set; `config.live/` mirrors it byte-identically. Editing one without the other recreates
   the drift class OD-4 closed.
2. Every `ordered_pool` entry needs an integer `rank`, `provider` and `model`; the resolver refuses otherwise
   (`ERR_SLOT_POOL_ENTRY_MALFORMED`).
3. A digest that names a file must be computed from the **git blob** (LF), not from a CRLF checkout. `config/*` is
   pinned to `eol=lf` for that reason.
4. Adding or removing an arm is a control-plane epoch change, not a task-level edit.
5. A retirement carried out by removing arms leaves the old `retired_arms` key empty; a check that reads only that key
   passes vacuously. Use the removal record (`removed_arms_od4` / `removal_od4`), and treat a missing ledger as a
   failure, not an empty set.

## 4. Not claimed

No native admission, no release, no independent external acceptance, no Protected Checker verdict, and no claim that
the historical HOLDs inside the W0 design document are closed. Local verification ≠ external acceptance ≠ release.
