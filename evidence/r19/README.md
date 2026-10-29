# R19 evidence — FHS-MSC Skeleton+Spine r2-revision2 (implementation + verification)

Round `R19-FHS-20261029`, continuation of `R18-FHS-SKELETON-SPINE-20261029`.
Subject: `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` (44 delivered files, 11,664,373 bytes).

This directory is the **public** part: commands, digests, dispositions and claim ceilings.
Raw corpora, databases, keys, tokens and round scratch stay outside the repo.

## What this round actually moved

| WP | before | after | receipt |
|---|---|---|---|
| WP-FHS-18 repair causality | `NOT PROVEN` (procedure mis-targeted; "environment-dependent") | **causal red→repair→green→unpatch→red**, deterministic | `receipts/WP18_CAUSAL_REPAIR_R19.json` |
| WP-FHS-05 PIPD candidates | `HOLD_NO_WRITER_ACK` | **produced by the original writer** (pipd_ls_sp 0.1.1a4): intent card, PI (replay identity), PD, ECP + 3 negative controls | `receipts/WP05_PIPD_WRITER_RECEIPT.json` |
| WP-FHS-19 supply chain | hash inventory only, licence/NOTICE unstated | recomputable inventory of the **delivered** package (2 passes agree), declared imports, 0 secret hits with a planted canary that fires, LICENSE/NOTICE **absent as named findings** | `receipts/WP19_SUPPLY_CHAIN_R19.json` |
| WP-FHS-15/16 disposition | aggregate counts, `invoked 0` | **80 per-ID rows** (25 methods + 24 donors + 31 slots) with install/load/invoke/acceptance state, 0 doc-only rows claiming INSTALLED, plugin manifest re-hashed live | `receipts/WP15_16_ID_LEDGER.json` |
| WP-FHS-21 96-cell oracle | reported 50/46/0 | **recomputed through `evaluate()`**: 679 checks 0 fail, 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY, 27 real CLI process invocations | round receipts (rerun via `tools/`) |
| subject integrity | "83/83" | **44/44 delivered files byte-identical** to the frozen copy, after every run | `SUBJECT_INTEGRITY.json` |

## The one real defect this round found and fixed

`03_TESTS_AND_READBACK/source_manifest.json` pinned 29 documents inside a directory that was later
renamed to `.../FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE/OLD/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_DRAFT/`.
`validate.py`'s `SOURCE-BYTES-UNCHANGED` therefore failed deterministically (2788/1) — not
"environment-dependent" as the previous round recorded.

Repair rule: rewrite a locator **only** when the candidate file's full SHA-256 equals the pinned
SHA-256. Result: **29/29 relocated, 0 unresolved, 0 name-matched**, and `validate.py` runs
**2789/0** with the oracle byte-identical. `RELOCATION_INDEX.json` holds the per-file proof;
`tools/locator_repair_r19.py` regenerates the repaired manifest.

## What is still gated on the owner (and why the agent stopped)

13 work packages have effect class `HOST_OP` / `REPO_WRITE` / `RELEASE`. `native_admission.authorize()`
refuses `REQUEST_SCOPE` unless the exact request digest is already in the protected registry at
`%ProgramData%\HG-KSEOS\native-admission\registry.json`. Writing that registry **is** the act of
granting native authority, so this round ships a pinned plan instead of installing it:

- `owner_gate/REQUEST_DIGESTS.json` — the 13 request digests
- `owner_gate/OWNER_STEP.md` — pinned exec root, HEAD, root_identity, approved-file pins, plan sha256,
  current registry sha256, and the single elevated step the owner performs

No permit was issued, no reference signed, no native effect executed, no promotion, no release,
no `main` merge.

## Claim ceiling

```
AUTHOR_SIDE + ISOLATED_LOCAL  : DONE for the rows above (each receipt names its own ceiling)
NATIVE EFFECT (13 rows)       : NOT RUN  — owner-gated registry revision, plan shipped
INDEPENDENT ACCEPTANCE        : NOT RUN  — no checker verdict is claimed

RELEASE / PRODUCTION / REMOTE : NOT CLAIMED
```

Reproduce: `/goal` was set on the session; every tool here is `python -B`, writes only inside the
round directory, and never touches the source package.
