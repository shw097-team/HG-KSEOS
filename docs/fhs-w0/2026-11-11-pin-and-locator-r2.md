# Lane toolchain pin and locator reproducibility — second measurement pass (2026-11-11)

**Scope**: measured on one Windows host against a FHS-NEXT W0 construction root. It adds
measurements to this branch's subject (lane-routing drift); it proposes no routing change and asks
for no merge beyond documentation.

**Claim ceiling**: `SOURCE_READ` + `HOST_RAW`. No native admission, no release, no acceptance.

## 1. The declared Codex pin does not resolve — and the sanctioned repair pattern already exists

`config/hermes-codex-lane.json` on `main` declares:

```
codex_executable  …/OpenAI/Codex/bin/<hash>/codex.exe
codex_version     0.165.0-alpha.1.2
codex_sha256      0c09e45bc76433756eb2d492f6db0ce6f269967e6618f4a6ae73e2fa239694b8
```

On the measured host that directory does not exist, and **no `codex.exe` on the machine carries that
digest** (six binaries present: 0.147.0-a6.5, 0.163.0-a10.2, 0.164.0-a11.1, 0.166.0-a5.1,
0.166.0-a6, 0.167.0-a3.2). The resolver therefore fails closed:

```
ERR_LANE_TOOLCHAIN_BINARY_MISSING   exit 3
```

Every lane dispatch dies **before any model call**, which from outside is indistinguishable from a
broken lane.

**The repo already answered this.** R18 applied
`ops/session-20261031/r18-durable/receipts/TOOLCHAIN_PIN_REFRESH.json`: three fields changed, sidecars
checked, `preimage_dir` recorded, rollback = byte restore — and the reason recorded verbatim was
"re-designated ONLY because the declared Codex binary no longer existed". The host also carries a
content-addressed store at `%LOCALAPPDATA%\HG-KSEOS\toolchain\codex\0.164.0-alpha.11.1\` with its own
`MANIFEST.json`, whose own upgrade policy notes that the vendor cache may rotate and cannot touch the
pinned copy. The pin has simply drifted again.

Repair applied here, without touching the origin file:

| | before | after |
|---|---|---|
| declaration | origin `config/hermes-codex-lane.json` | overlay `config.live/hermes-codex-lane.live.json` |
| version | 0.165.0-alpha.1.2 | **0.167.0-alpha.3.2** |
| digest | (binary absent) | `4f91ae86…`, verified |
| sidecars | — | 4/4 present |
| check exit | 3 | 0 |

The overlay records `origin_declaration_sha256`, so "the origin bytes were not edited" is checkable
rather than asserted. Note the store's `0.164.0-alpha.11.1` ships `codex.exe` **alone**; the four-file
layout (code-mode-host / command-runner / windows-sandbox-setup) exists only in the
`0.167.0-alpha.3.2` directory, which is why that build was chosen.

## 2. Most "missing fixture" failures were a moved root, not missing evidence

A suite run in the new tree reported 171 failed / 555 passed. Grouping the file-not-found events by
**where the path pointed** (not by exception type) gave:

| target of the missing path | events | what it actually was |
|---|---|---|
| pre-move root `…/Agent_Workspace/HG-KSEOS/…` | **104** | the file is present at the moved root `…/Agent_Workspace/FHS/HG-KSEOS/…` — a stale absolute path |
| `<tree>/TEST_RESULTS/…` | 65 | the harness creates temp dirs under a root-level directory that did not exist |
| `<tree>/PIPD/skills/pipd-*/tests/cases.yaml` | 50 | the retired line's read-only tree is the only place those cases live |
| worktree-only source files | ~10 | present in the local worktree, absent from the published repos |

Restoring the paths (junctions + a declared addendum import; **no origin file edited**) moved the
suite to:

| step | failed | passed |
|---|---|---|
| baseline | 171 | 555 |
| + pre-move root reachable | 120 | 606 |
| + `TEST_RESULTS` present | 95 | 631 |
| + `PIPD` cases reachable, addendum sources imported | **83** | **644** |

Errors 17 → 16. What remains is 14 genuinely absent historical artefacts (handoff deliveries), 5
assertions that fail *because* the published registry is epoch 33 while the live plane is 41 (the
divergence this branch documents), 13 assertion-level items, and 1 native-bundle hold.

**Lesson worth carrying**: classify a missing path by its target, not by the exception. Otherwise a
path repair looks like a policy question ("must we import history?") and gets deferred for the wrong
reason.

## 3. The acceptance gate re-runs, but its verdict is not reproducible today

`tools/gate_r20.py` (R20/GSTACK v6) executed in place against the R13 round:

- selftest: every mutation **fired** (G10…G29) — the gate is not a rubber stamp;
- full, no sources: **17/22 PASS, 3 blocking fail, 1 reporting open**;
- full, with the declared 31-document corpus passed in: 18/22 PASS, 2 blocking fail, 1 reporting open;
- full, with the corpus **and** the 26 deleted roots restored as junctions from the 2026-11-10 archive:
  **19/22 PASS, 1 blocking fail, 2 reporting open** (recorded 21/22 on 2026-11-09).

**G11/G13 are recoverable, and the recovery is worth recording**: the gate re-hashes the round's own
31 declared documents (`lanes/A/SOURCE_LOCK_V3.json`, `file` + `declared.sha256` each). Those 31 files
exist on this host but split across two directories under different names (14 + 17), so a plain
`--sources <dir>` can never satisfy it. Building a corpus **view** matched by declared sha256 only
(31/31 matched, 0 substituted) lets G11 and G13 re-derive the totals from the documents themselves.

**And the deleted inputs were recoverable after all.** They sit in `G:\Projects\封存\FHS_封存_20261110_已分類可封存`:
`worktrees/r4-hgk` with its `pyproject.toml`, the other 16 worktrees, six round directories, and
`FHS_W1_Work_Final/…/sources`. Twenty-six junctions restored the declared absolute paths without copying a
byte, after which **G16a passes by real re-derivation** and G19 advances from `ROOT_ABSENT` to
`MEMBER_ABSENT` (308 of 437 declared copies).

The 308 absent members are all under the old `知識庫/實作相關DOC/Fabric vNext/…` layout. That tree still
exists, reorganised, one level deeper (`…/FHS／FHS-MSC／SBL/Fabric/Fabric vNext`), and a digest scan of
all 8,105 files under `…/FHS／FHS-MSC／SBL` found **302 of the 308 members (103 of 106 distinct contents)
byte-identical**, living now under `FHS\FHS-MSC` (255), `Fabric\Fabric vNext` (43) and
`FHS\FHS_PIPD-LS-PKG` (4). Only **6 members / 3 distinct contents** are genuinely gone:
`FHS_PIPD-LS-PKG_W0_r4.md`, `FHS_PIPD-LS-PKG_W0_r6.md` and the `…HIGH_RETENTION…非規範性審計證據附錄.md`
appendix. So G19's red is **path drift, not data loss** — and it still fails, correctly, because it asks
whether the copy sits at its declared path. Mapping: `_local/W0_R2_G19_PATH_MAP.json`.
G16b stays OPEN for a different reason: its `hgk-main`
subject records `scan_complete: false` because only three files were materialised at the pinned commit —
a limitation of the subject, reported rather than passed. G22 mirrors those two rows.

## 4. One governance gap the second pass exposed

The mandated checker model for this round was the same model as the writer. The guard refuses that
pair **when the caller declares the maker**:

```
hgk-lane-guard.py --maker-model deepseek-v4.1-flash --target-model deepseek-v4.1-flash  -> exit 2
                                                                        ERR_LANE_SOD_VIOLATION
```

but a dispatch that declares **no maker** runs the writer's model as the checker with no refusal
(measured: `ok: true`, `served_arm == required_arm == opencode-go/deepseek-v4.1-flash`). So SoD is
enforced at the guard when asked, and not enforced by the dispatcher by default. Combined with the
published `VERIFY_SECURITY` row's stale `transport_model` (reported earlier on this branch), the
declaration and the enforcement disagree in the same direction.

That is a governance question for the owner, not something this note fixes: the fix is either to make
`--maker-*` mandatory for `VERIFY_SECURITY`, or to derive the maker from the lane's own writer
assignment instead of trusting the caller.
