# Tasks

## 1. Preflight
- [x] 1.1 A00 source register with per-source sha256 (20/20 knowledge base present)
- [x] 1.2 C0-C9 contract authored and compiled: lint/activation/acceptance/compile PROMPT_COMPILE_PASS
- [x] 1.3 HGK typed admission (own project id, TaskSpec segment collision-checked against the live spine)
- [x] 1.4 A03 GitHub freeze: per-PR head, base, changed set, prefix, blob modes, manifest semantics
- [x] 1.5 A04 manifest semantics: every indexed path resolves at that HEAD; first-cut vs final explained

## 2. Security
- [x] 2.1 Scoped secrets scan on the content each PR adds, with a positive control that must fire and a
      clean control that must not
- [x] 2.2 PR #14 config-backup sensitivity review (path/route/credential metadata)
- [x] 2.3 Confirm no `.github/workflows` or hook enters the archive, and archived scripts are not executed

## 3. Authorisation and merge
- [x] 3.1 Record the bounded maintainer approval batch naming each PR's frozen HEAD and prefix
- [x] 3.2 PR #12 out of draft (GraphQL markPullRequestReadyForReview; the REST undraft path 404s)
- [ ] 3.3 Merge #12, #13, #14 each with `sha=<approved head>` and read `main` back
- [ ] 3.4 Rollback pointer per PR (`git revert <merge_sha>`)

## 4. Return pack
- [ ] 4.1 Machine-readable evidence_return_pack per PR
- [ ] 4.2 12/12 disposition of the acceptance report's findings with owner and claim ceiling
- [ ] 4.3 Single evidence MD + handover + self-check with injected mutations
