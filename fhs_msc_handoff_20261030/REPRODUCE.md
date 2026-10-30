# Reproduce

Python 3.11. No network. Nothing here writes into the delivered package.
`PKG` = unpacked `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`; `WORK` = a scratch directory you own.

## 0. Restore the canonical layout (F-02)

```bash
cd "$PKG" && mv 01_FHS-MSC_PIPD-LS-PKG_BODY 01_SUBSTANTIVE_BODY
```

Skip this and verification reports 429 missing rows. That is the defect, not corruption.

## 1. Payload integrity — expect 909/909

```bash
python tools/verify_package.py "$PKG"
```

Expect `A_payload_manifest: PASS, rows 909, match 909, mismatch 0, missing 0`; `B_undeclared_files:
REVIEW` listing exactly the two manifests (declared self-excluded); `D_relative_links: PASS, links 30,
broken 0`. `C_delivery_manifest` stays `FAIL` — that is F-01 and it is real.

## 2. Seal — expect two byte-reproducible archives

```bash
python tools/seal_package.py "$PKG" "$WORK/seal"
python tools/seal_package.py "$PKG" "$WORK/seal2"
sha256sum "$WORK"/seal/*.zip "$WORK"/seal2/*.zip
```

On these inputs: body `483623` / `07d62b49…`, evidence `25987085` / `9497133b…`, identical in `seal2`.
`PACKAGE_READBACK.json` in `$WORK/seal` carries the per-entry CRC32/bytes/SHA-256 readback. Different
inputs give different hashes — the recipe reproduces, not the value.

## 3. First work — expect 24 clauses, 24 atoms, 3 SPECs

`03_HANDOFF_EVIDENCE/QA_TOOLS/prepare.py` hard-codes the author's base path:

```python
BASE=Path(r'C:\Users\user\Documents\Codex\2026-10-30\codex-fhs-msc-pipd-ls-pkg\outputs\FHS-MSC_STATIC_REPAIR_2026-10-30_v1')
DEST=BASE.parent/'FHS-MSC_HANDOFF_PATCH_2026-10-30_v1'
```

Copy the tooling out, point `DEST` at an empty path you own, keep `BASE` as the static-repair baseline it
names, then:

```bash
python prepare.py      # snapshots the four readers + TPM plugin; refuses if DEST exists
python first_work.py   # 24 clauses, 24 atoms, PI reader PASS, 3 SPECs, KnownAnswer_reasked 0
```

## 4. The 35-check harness — 34/35 as shipped, 35/35 after one repair

```bash
python check_first_work.py     # 34 pass / 1 fail: EXISTING_5_AFFECTED_TESTS (F-03)
```

Apply only this ordering change in your copy:

```python
# add before:  suite=unittest.defaultTestLoader.loadTestsFromNames(
sys.path.insert(0, plain(E / 'READERS/PIPD'))
# and drop the same insert from the line that precedes  buf=io.StringIO()
```

```bash
python check_first_work.py     # 35 pass / 0 fail
```

## 5. Structural checks — six PASS, one REVIEW

```bash
python tools/exec_checks.py "$WORK/repro"
```

Expect `D1` PASS (22 nodes / 36 edges / acyclic), `D2_wp15_closure` **REVIEW** (declared `[00,01,15]` vs
edge-derived `[00,15]`), `D3`–`D7` PASS, `overall: REVIEW`. A tool printing `PASS` here is hiding F-05.

## 6. Identity scope — control differs, repair matches

```bash
python tools/identity_probe.py
```

Expect `control_identical: false` and `repair_identical: true` (`PI-d0974c55d63bc021` at both roots).
Proves F-04 without touching the PIPD writer.

## 7. Five affected tests in the live PIPD repo

```bash
cd C:/Projects/Agent_Workspace/PIPD
python -m unittest -v \
  tests.test_atomic_requirements.ClauseBoundCompiler.test_every_atom_traces_orphan_free \
  tests.test_atomic_requirements.ClauseBoundCompiler.test_normative_claim_without_source_is_refused \
  tests.test_atomic_requirements.ClauseBoundCompiler.test_semantic_collapse_is_refused \
  tests.test_negative_and_rollback.TestNegative.test_workorder_candidate_must_be_candidate_only \
  tests.test_negative_and_rollback.TestNegative.test_execution_binding_ack_requires_receiver_binding
```

Expect `Ran 5 tests ... OK` at PIPD `995c7ad0c69a05a0c5cf6528155a62020ce31f87`.

## 8. Lanes (needs the local relay and a codex CLI)

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
python scripts/hgk-lane-dispatch.py --lane EXECUTE \
  --prompt "Reply with exactly: NONCE-CHECK-1" --nonce NONCE-CHECK-1 \
  --require-assigned-arms --identity-source codex-rollout \
  --codex-executable "C:/Users/user/AppData/Local/OpenAI/Codex/bin/22cfb1d302613eae/codex.exe" \
  --relay-base http://127.0.0.1:10102/v1
```

Expect `ok: true`, `used_transport_model: opencode-go/deepseek-v4.1-flash`, nonce echoed. Without
`--codex-executable` you get `ERR_LANE_PIN_IDENTITY_INVALID` (F-06). The `VERIFY_SECURITY` lane currently
returns an upstream 401 for `gpt-6.1-sol` (F-10) — that is a blocked gate, not a passing one.
`--json-out` is ignored by this revision; redirect stdout if you want the receipt on disk.

## What cannot be reproduced

The two archives named in `SHA256_DELIVERY_MANIFEST.md`: the bytes are not in the delivery (F-01). Do not
"fix" their hashes; replace the claim with a fresh seal.
