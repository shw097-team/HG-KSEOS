# FHS_NEXT W0 — lane-routing divergence report (2026-11-11)

**Status: candidate report, no config change. This branch changes documentation only.**
**Claim ceiling: `SOURCE_READ` + `LOCAL_CHECK`. It is not an owner decision, not a registry epoch
change, not an acceptance, and not a release.**

## 1. What was observed

While running an FHS_NEXT W0 source read against `shw097-team/HG-KSEOS` `main`
(`acd9196fcd748638673848bf62a426dcc3c22dc1`), the lane-routing artefacts in *this* repository and
the lane-routing artefacts on the originating host disagree. Both were hashed and re-read; nothing
was inferred from prose.

| artefact | this repository, `main` | originating host control plane |
|---|---|---|
| `config/lane-routing-registry.yaml` | `epoch: 33`, `status: CANDIDATE`, sha256 `ee8de93c53754fee56873d70a77582b8ada5b9c046836c56a4b96cdbd3181df1` | `epoch: 41`, `status: IN_FORCE`, sha256 `811bf1a5eea4304c057dfc95974e31b4b7655a588091f674db2cf57dbb3055c3` |
| `config/lane-route-slots.candidate.json` | `revision 23`, **no `retired_arms` key** | `revision 36`, `retired_arms` present, `retired_epoch: 41` |
| `config/model-lane-assignment.json` | `revision 35`, `registry_epoch: 34` | `revision 43`, `registry_epoch: 39` |
| PLAN pool rank-4 arm | `opencode-go/mimo-v2.6-pro` | `opencode-go/mimo-v2.6-flash` |

The owner order of 2026-11-09 recorded in the epoch-41 registry retires `opencode-go/mimo-v2.6-pro`
("wrong model family for this lane set; it must never be selected again", replacement
`opencode-go/mimo-v2.6-flash`). That retirement exists **only** in the epoch-41 state.

## 2. Consequence, measured

With `config/` as published here (epoch 33, no retirement ledger), the lane tool that reads the
pool admits the retired arm:

```
$ python tools/fhs_3lm.py --assert-arm opencode-go/mimo-v2.6-pro
{"ok": true, "arm": "opencode-go/mimo-v2.6-pro", "lanes": [["PLAN", 4]]}      # exit 0
```

With the epoch-41 state loaded, the same call refuses with exit 9 and names the replacement.
So a consumer that reads only `main` obtains a selectable arm that the owner has retired.

Separately, the registry epoch and the assignment revision disagree inside *this* repository too
(`registry epoch 33` vs `model-lane-assignment.registry_epoch: 34`, `revision 35`). The lane guard
treats that as `ERR_LANE_STALE_EPOCH` / `ERR_LANE_SOURCE_STALE` and exits 4 — fail-closed, which is
the correct behaviour for a stale pin, but it means the guard cannot reach an ADMIT verdict from the
published configuration.

## 3. What this branch does not do

- It does **not** publish, copy or reconstruct the epoch-41 control-plane state. Publishing a
  control-plane epoch is an owner-ordered operation, not a documentation change.
- It does **not** edit `config/`, `scripts/` or any test expectation.
- It makes **no** admission, acceptance or release claim, and does not assert which epoch the
  owner wants this repository to carry.

## 4. What the owner may want to decide

1. Whether `main` should carry the epoch-41 retirement ledger (an epoch change), or
2. whether this repository is intentionally a CANDIDATE snapshot that must never be read as the
   control plane, in which case a reader-facing marker in `config/` would prevent the mismatch above.

Either decision is the owner's; this report only makes the divergence cheap to see.

## 5. How to reproduce

```bash
# in a checkout of this repository
python tools/fhs_3lm.py --assert-arm opencode-go/mimo-v2.6-pro    # exit 0 here, exit 9 on epoch 41

# hashes
sha256sum config/lane-routing-registry.yaml config/lane-route-slots.candidate.json
# expected here: ee8de93c…1df1 / 628e7db6…c577 is the epoch-41 pool digest, not this one
```

Reproduction was run on Windows with Python 3.11.9, in a workspace that imports these files
byte-identically (`source_sha256 == target_sha256`, 480 files, 0 mismatches).
