# Tasks

## 0. Execution surfaces (default-on)
- [x] HGK typed admission `CNV-EA-R7R11` (1 requirement frozen, 3 TaskSpecs, 3 WorkOrders, checkpoint `CK-R7R11-4181BD0E`)
- [x] KANBAN board `cnv-ea-r7r11-20261016` + SWARM graph (root `t_89469084`, 4 workers, verifier, synthesizer)
- [x] OPENSPEC change record `hgk-cnv-evidence-archive-r7r11-20261016` (this record, `--strict` validation)
- [x] GSTACK named-method route readback for the round flow
- [ ] CODEX CLI EXECUTE lane (bounded writer) + CODEX CLI VERIFY/SECURITY lane (checker)

## 1. A01 prompt compiler (this round only)
- [x] C0-C9 contract `prompt-contract.json` (schema-conformant)
- [x] `lint` / `activation` / `acceptance` exit 0, `PROMPT_COMPILE_PASS`
- [x] `compile --out-dir` -> `thin-prompt.md` + `compiler-receipt.json` (`PROMPT_COMPILE_PASS`)
- [x] `duplication` against the round sources below threshold

## 2. A03 per-PR preflight (eight pull requests)
- [x] live `head`, `base`, `changed_files`, `reviews`, `mergeable_state` for #4..#11
- [x] single evidence prefix + `change_class` re-derivation for each
- [x] prove the reference snapshot is still current (no `PR_HEAD_DRIFT`)

## 3. A04/A05 trusted preflight
- [ ] manifest-vs-tracked-set and current-HEAD determinism per PR, outside the PR
- [ ] trusted secrets/privacy scan over every changed blob
- [ ] no archived `.py`/`.ps1` helper executed

## 4. A06/A07 bounded errata + approval
- [ ] decide errata only on measured defects
- [ ] obtain per-PR maintainer approval (HITL) — evidence-prefix publication approval
- [ ] remote merge (HITL) as repository maintainer

## 5. A08/A09/A10 closure
- [ ] per-PR merge + readback (main, merge commit, tree prefix)
- [ ] K-ledger cross-index metadata errata + ten EIA findings disposition matrix
- [ ] `CONVERGENCE_EVIDENCE_RETURN_PACK` + single evidence MD, published and mirrored
