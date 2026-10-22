# R11-0 tasks - complete SESSION closure + handover

## 1. Admission and control-plane records
- [x] 1.1 [ADMIT] HGK typed admission for ChangeSet R11-0 (own project id).
- [x] 1.2 [BUILD] OPENSPEC change `hgk-r11-session-handover-20261016` validated `--strict`.
- [x] 1.3 [BUILD] KANBAN/SWARM board with root + worker cards for this round.

## 2. FAR research (scope: SESSION closure and handover)
- [x] 2.1 [FAR] Read-only fan-out over the closure/handover subject set, writing into `R11/FAR/ws*/`.
- [x] 2.2 [FAR] Orchestrator re-derivation of every decisive child claim before use.
- [x] 2.3 [FAR] FAR run artifacts under the Fabric research home with a free run id.

## 3. Handover product
- [x] 3.1 [BUILD] Handover entry document (single entry point for a new session).
- [x] 3.2 [BUILD] Machine-readable resume manifest (open items, owners, one-action steps, blockers).
- [x] 3.3 [BUILD] Measured inventory of every open openspec change record.
- [ ] 3.4 [BUILD] Carried-over findings/blockers from R10, each labelled carried-over vs re-measured.

## 4. Self-check, repair, acceptance
- [x] 4.1 [SELF] Self-check: links, counts and digests inside the handover product.
- [x] 4.2 [VERIFY] Independent checker on the mandate's arm; adjudicate its verdict item by item.
- [x] 4.3 [JSON] Classify every open governance record (close / continue / owner decision) with a locator.

## 5. Publication
- [x] 5.1 [PUB] Packet prepare + M2 trusted-scope/secrets gate.
- [x] 5.2 [PUB] Push to Fabric and read back blob-by-blob.
- [x] 5.3 [PUB] Draft PR for the external acceptance officer.
- [x] 5.4 [PUB] Independent re-verification of the remote state.

## 6. Self-research/learning/iteration/evolution
- [x] 6.1 [EVO] Self-research / learning / iteration / evolution set for this round.

## 7. Measurements and corrections recorded while executing
- [x] 7.1 [MEASURED] HGK typed admission `CNV-R11-HANDOVER` -> 6 work orders `WO-TS-HANDOVER-01..06`.
- [x] 7.2 [MEASURED] An openspec delta spec MUST live at `changes/<change>/specs/<capability>/spec.md` and the
  change ALSO needs `proposal.md`; a root-level `spec.md` fails `--strict` (learned here, cost one cycle).
- [x] 7.3 [MEASURED] The KANBAN graph is built in one call: `kanban boards create <slug>` -> `kanban boards
  switch <slug>` -> `kanban swarm "<goal>" --worker <profile>:<title> --verifier ... --synthesizer ... --json`.
  (`kanban create`/`add --board` are NOT the forms; the board comes from the switched-active board.)
- [x] 7.4 [MEASURED] `SELFCHECK_R11.json`: 0 non-resolving absolute path references in the handover document;
  the package anchor matches 2,689,181 bytes and sha256 `96d9d564…`; inventory = 24 records.
- [x] 7.5 [MEASURED] Publication packet v2: 37 files, HEAD `23fd70e133a8d464b773baedda1d1aa1a0685c3b`, M2 PASS
  (39 blobs, 131,157 bytes, hard_secrets 0, soft_candidates 0). The first attempt failed on a `Path`-vs-`str`
  defect this round introduced when injecting verbatim FAR transfers; fixed and re-run (disclosed, not hidden).
- [x] 7.6 [OPEN] Final packet after the FAR research and the checker verdict land.
- [x] 8.1 [MEASURED] Publication FINAL: branch `evidence/cnv-pipd-ls-sp-20261015-r11`, head
  `5e055ea28e445cd6c965036ef64fbf679a5b8f34`, MANIFEST 75/75, M2 PASS (77 blobs, 438,866 B, hard 0), readback 0
  mismatches, **Draft PR #11**. First cut `51c804ad` missed `SELF_EVOLUTION_R11.*` (written after staging); the
  round found that itself, disclosed it in its ledger, re-cut and re-pushed.
- [x] 8.2 [MEASURED] External readback via the GitHub API: PR #11 head == local head; `main` `b8ff8104`, r6
  `a10f7bea`, r7 `04a1e118`, r8 `3af41480`, r9 `5cd47cea`, r10 `34d57124` all unchanged; peer PRs #6/#8/#10
  untouched.
- [x] 8.3 [MEASURED] The checker ran ON THE MANDATED ARM with a real pool receipt (rank 1,
  `opencode-go/deepseek-v4.1-flash`, exit 0, 543.73 s) and returned PARTIALLY_VERIFIED (4 CONFIRMED / 3 REFUTED);
  all three refutations were accepted and corrected, and the writer/checker same-arm residual is stated.
