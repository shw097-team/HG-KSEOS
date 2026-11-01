# R20 close-out index — read this first

**Round:** `R20-FHS-20261029` · **Branch:** `candidate/r19-fhs-implementation` · **PR:** #5
**Claim ceiling:** `AUTHOR_SIDE_LOCAL`. Owner acceptance (T2) and external acceptance (T3) are **NOT_RUN**.
Nothing in this directory is a release, a promotion, or a native acceptance.

## What this round delivered

| Artifact | Binding |
|---|---|
| `package/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip` | sha256 `ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f`, 13,578,117 B, 89 entries, no self-embedding |
| repaired subject (`r2-revision3`) | built from the frozen `r2-revision2` sibling; **the frozen input was never written, moved or repacked** |
| `tables/HOLD_DISPOSITION.tsv` (46 rows) · `tables/STAGE18_TRACE.tsv` (18 rows) | mechanically derived from `oracle96_verification_v2.json` (96 cells = 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY) |
| dispatcher gates + tooling (repo paths `scripts/`, `tools/`, `tests/`, `config/`) | see `analysis/` and `receipts/` in this tree |

## Where the claims come from (audit path)

| Claim | File |
|---|---|
| 29 byte-level locator repairs, hash-gated | `receipts/P1B_LOCATOR_REPAIR.json` (`rows=172 / rewritten=29`) |
| packaging determinism, 88/88 checksums, no self-embed | `receipts/P1D_R20B_CHECKSUM_REPAIR.json` |
| r2 pristine is **2788 passed / 1 failed** (its own 2789/0 was false) | `receipts/validate_r2_pristine.out` |
| r3 fresh: 2789 / 0 | `audit/AUDIT_ROUND.md` (independent extract of the shipped zip) |
| A1–A8 machine items (8 rows, all `ok`) | `receipts/CLOSURE_MACHINE_ITEMS.json` |
| six independent VERIFY rounds (rank 2, `gpt-6.1-sol`, 6× exit 0) | `lane/closure_verify_stdout.json`, `lane/closure_verify_stdout.json.attempts.ndjson` |
| full-suite attribution vs baseline `6086908` | `receipts/BASELINE_FAILED_IDS_6086908.txt` |
| owner window lifecycle (opened → 2 ops → CLOSED) | `closeout/WINDOW_R20_*.json` |
| four-state config measurement of the live control plane | `closeout/CONFIG_FOUR_STATE.json` |

## Reproduce (no credential needed on this public repo)

```bash
git clone https://github.com/shw097-team/HG-KSEOS.git
cd HG-KSEOS && git checkout candidate/r19-fhs-implementation
sha256sum evidence/R20-FHS-20261029/package/*r2-revision3.zip
# expect ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f

python - <<'PY'
import json,pathlib
d=json.loads(pathlib.Path("evidence/R20-FHS-20261029/receipts/CLOSURE_MACHINE_ITEMS.json").read_text(encoding="utf-8"))
rows=d.get("rows") or d.get("items")
print(len(rows), [r.get("ok") for r in rows])
PY
# expect 8 rows, all True

python tools/evidence_reconcile.py     # expect "17 checks / 0 mismatches", rc=0
```

## What is NOT claimed

1. **22 WP are a document-level declaration only.** `01_BODY/11_WORKPACKAGES_AND_DAG.md` declares `22 WorkPackage`;
   the file contains no machine-checkable 22-row table (`^| WP` matches 0). **0/22 have any native acceptance.**
2. **Four VERIFY items are HOLD, not PASS** (C1/C4/C7/C9): the checker's sandbox is read-only and cannot execute
   tests or spawn a lane; escalating it voids the advisory verdict by contract.
3. **74 repo-wide tests still fail** at the published head (`74 failed / 734 passed / 0 errors`). Against baseline
   `6086908` (`88 failed / 686 passed / 2 collection errors`) this is **0 new failure ids, 14 fixed** — the 74 are
   pre-existing, not introduced here.
4. **No OR-1..OR-8 was filled or signed.** The 75 residues (46 cells + 18 stages + 11 holds) are packaged as owner
   requests in `owner_requests/`, awaiting the owner principal.
5. **No merge, tag, release, or promotion.** PR #5 (this branch) and PR #6 (`publish/r20-subset` → `main`) are open.
6. The lane receipts of the earlier R20 passes (`PASS3`–`PASS5`) are **not quotable** — their `nonce_present_raw_stdout`
   field contradicts their own byte-exact stdout (TT-R20-9). Only the six closure-round attempts in
   `lane/closure_verify_stdout.json.attempts.ndjson` carry attributable nonces.

## Known self-inflicted defects, repaired and disclosed

`TT-R20-12` stale codex pin · `TT-R20-13` `_producer` scope (61 green tests went red, then repaired) ·
`TT-R20-17` alias equivalence missing in the verdict path · `TT-R20-18/19` tautological tests ·
`TT-R20-20` overlap check missed alias/case variants. Full ledger: `analysis/` + `_handover` mirror.
