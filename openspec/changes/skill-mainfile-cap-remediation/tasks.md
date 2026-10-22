# Tasks

- [ ] T1 Pre-flight: skill_guard `pre` baseline; record LF-normalized chars, raw chars, bytes, sha256.
- [ ] T2 Freeze the split manifest (section -> target reference file), pre-registered before editing.
- [ ] T3 Build/verify the mechanical splitter; dry-run on a copy (never in place first).
- [ ] T4 Reverse reconstruction: reinsert slices into pointer positions and prove byte-identity with the pre-split copy.
- [ ] T5 Pointer integrity: every moved section has a 3-line pointer; routing map lists the load path.
- [ ] T6 Index completeness: the support-files index includes the newly created reference files.
- [ ] T7 Add the adversarial-verification-rounds pointer; reconcile duplication with the standalone skill.
- [ ] T8 skill_guard `post` = PASS; keyword grep counts not lower than baseline; 0 new orphans.
- [ ] T9 Cold-start canary: a fresh leaf given only the main file must reach the right reference file.
- [ ] T10 Regrowth guard: declare a ceiling and a check that fails a future round crossing it.
- [ ] T11 Independent checker (not the maker) recomputes T1-T10 numbers from raw bytes; verdict recorded.
