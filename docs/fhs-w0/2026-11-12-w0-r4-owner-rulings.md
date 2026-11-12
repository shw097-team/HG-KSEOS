# W0 R4 — owner rulings of 2026-11-12, and what they changed

**Round**: `W0_R4_OWNER_RULINGS_20261112` · **Workspace**: `C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\W0_R4_OWNER_RULINGS_20261112`
**Claim ceiling**: `SOURCE_READ + HOST_RAW + AUTHOR_DESIGN + LOCAL_CHECK`. No ACK, no native admission, no release.
**Relation to the closed round**: this document adds measurements and one register path rewrite. It does not
edit any verdict of `FHS_W0_R13_ACCEPTANCE_20261108`.

## 1. OD-3 — where artefacts may live

Owner ruling, verbatim: *every artefact must live under `FHS_NEXT` or `FHS_NEXT_Workspace`; a plan that
violates this is void and may never be used as a HOLD; G19 must not go red — move it to the compliant
location and correct the register and the corpus locator so later work can find it.*

Applied, in this order:

1. 69 register members that lived under `C:\Projects\Agent_Workspace\{worktrees, FHS_W1_Work_Final}` were
   copied to `FHS_NEXT\roots\legacy_declared\…` — **34,095,871 bytes**, every file hashed against the
   register's declared sha256, **0 mismatches**.
2. The register's 69 member paths and 2 `roots_scanned` entries were rewritten to that location. Group
   counts, copy counts and every digest are unchanged; the previous file is kept as
   `COPY_REGISTER_PRE_OD3.json` and the new one carries an `owner_ruling` block.
3. `ops/tools/gate_corpus.py` dropped a stale search root (its content lives at the HANDOFF-PATCH-v1 path
   already listed) and now also searches the compliant copy. Matching is still digest equality against
   `lanes/A/SOURCE_LOCK_V3.json`.
4. Only then were the two junctions removed (`rc 0`).

Re-run after the move: **G19 394/394 PASS**, **gate_corpus 31/31, missing 0**, `selfcheck` **16/16**.
The register still *reads* 309 documents under `知識庫/` and 16 under `FHS/`; those are the owner's canonical
files, not products of this work, and relocating them would break every other locator.

## 2. P0-03 / G16a — rebuilt from the repository, then passed

The three dependency subjects were not on this host, so they were materialised from the public repository at
the commits the descriptor names, under `FHS_NEXT\roots\subjects\`:

| subject | commit | files | bytes | pyproject sha256 | declares `cryptography` |
|---|---|---:|---:|---|---|
| `hgk-local` | `6c9fc73377c1` | 2,184 | 75,968,493 | `6d9e9e445a6c…` | yes |
| `hgk-worktree` | `a7046a36956e` | 757 | 80,578,970 | `0e06e26975d9…` | no |
| `hgk-main` | `acd9196fcd74` | 757 | 80,587,007 | `0e06e26975d9…` | no |

Descriptor corrections, all of them locator facts rather than claims:
`path` → the rebuilt tree; `source_root` → `<tree>/src` (the gate scans `source_root`/`source_files`, not the
tree root); `hgk-main`'s `source_files` → the real path `src/hg_kseos/fhs/issuer_binding.py`;
`hgk-main.scan_complete` `false → true`, because the whole tree is on disk now and the old note said so.
`lanes/B/TREE_IDENTITY.json` is byte-identical to the closed round — the gate's own re-derivation is what
decides.

Result: **G16a PASS** — “3 subjects agree with what can be verified here”. The gate moved from
`18/22, G16a: ABSENT` to **`19/22`**. G16b is no longer “not looked at” but a real coverage gap:
`cryptography` and `yaml` are imported and not declared for `hgk-main`/`hgk-worktree`, `yaml` for
`hgk-local`. `G19` inside that view still fails on the closed round's own lineage register; that is the
historical artefact, superseded by the re-registered 394/394, and it is not edited.

## 3. P0-05 / P0-06 — caller wiring and the missing maker precondition

The origin receipt carries no caller (`role_binding_source: null`, `required_arm: null`): a served turn could
not be attributed. The origin dispatcher also runs without a maker. Neither is repairable inside this root
without editing the origin, so the repair is an entry that enforces the preconditions and then calls the
origin dispatcher unchanged:

`lane_dispatch_guarded.py` — maker required, maker ≠ checker, maker must be a declared arm, binding must
exist and match the live epoch and pool, then a composite record binds
`caller_id = sha256(lane, maker, checker, binding sha, nonce, prompt sha, workorder)` to the origin receipt
sha256.

Measured: five NEG shapes fail closed (`ERR_MAKER_MISSING` 3, `ERR_LANE_SOD_VIOLATION` 2,
`ERR_MAKER_NOT_IN_ASSIGNMENT` 4, `ERR_BINDING_MISSING` 5, `ERR_BINDING_STALE` 5); one POS turn
**SERVED** with `caller_id FHS-CALLER-ba80a29d…`, usage receipt ok, nonce echoed.

Recorded, not hidden: the bound slot was `PLAN/opt1` = `deepseek-v4.1-flash`, the served arm was
`gpt-6.1-sol` (pool rank 1). The dispatcher still does not consume the FHS-3L&M binding record; that wire is
a W1 change in HGK.

## 4. H1 — five epoch numbers in play

| surface | value |
|---|---|
| published `config/lane-routing-registry.yaml` | epoch **33** |
| published `config/model-lane-assignment.json` | `revision` **35**, `registry_epoch` **34** |
| live `config.live/lane-routing-registry.yaml` | epoch **41** |
| live `config.live/model-lane-assignment.json` | `revision` **43**, `registry_epoch` **39** |

`hgk-lane-guard.py` derives `live_epoch` from `registry.source_of_routes.path`'s `revision` (35), compares it
with the registry's epoch (33) and refuses with `ERR_LANE_STALE_EPOCH` before any dispatch. The closed round's
own `VERIFY_R26_VERDICT.json` records `config/` at **epoch 41** with `mimo-v2.6-flash` as PLAN `arms[3]` and a
passing retirement sweep, so the published copy is the stale mirror. Two candidate owner decisions remain:
**H1-A** publish epoch 41 as the single in-force set, or **H1-B** declare the live overlay authoritative and
demote the published copy to lineage. This document does not decide it.

## 5. H11 / H14 — the retired arm is still declared and still reachable

The published registry still lists `transport_model: opencode-go/mimo-v2.6-pro` as an arm; `retired_arms`
in the live overlay records it retired at epoch 41. A direct POST to the relay with that arm answers
**HTTP 200 with an empty body** — the transport does not refuse it, so retirement is enforced only at
guard/dispatch. Not repaired here: the pool and registry are origin objects, and the relay is a host service.

## 6. What this round did not do

No ACK, native admission, release or merge. The lane bindings, the guarded entry and the rebuilt subjects are
local control-plane records and local files. Nothing in `Fabric/`, `SBL/` or `HG-KSEOS/` was edited.
