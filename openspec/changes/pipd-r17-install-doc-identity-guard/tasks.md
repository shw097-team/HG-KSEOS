# Tasks — pipd-r17-install-doc-identity-guard

## 1. Guard (F-R6-01 remainder)

- [ ] 1.1 `tests/test_r6_doc_identity_guard.py` exists, stdlib + `unittest`, no network.
- [ ] 1.2 It fails on a paragraph that pairs the preview.4 id with the preview.3 commit without marking
      it preview.3.
- [ ] 1.3 It fails on a fenced build example whose mount pack, release id and release commit name
      different generations.
- [ ] 1.4 It fails on a `dist/mount/` path that does not exist in the tree.
- [ ] 1.5 It fails on a same-file `#fragment` link with no matching heading, in either document.
- [ ] 1.6 It fails if the user guide loses `S4_FULL_PASS NOT_GRANTED` or regains the preview.3-era hold
      sentence.
- [ ] 1.7 Each check has a paired mutation case that makes exactly that check fail.
- [ ] 1.8 The suite passes on the candidate and no workflow file was edited.

## 2. Served-document provenance drift (F-R6-08)

- [ ] 2.1 `docs/install/README.md` records that the served `PIPD_WEB_FALLBACK.md` declares the earlier
      preview.3 provenance, with its served sha256 `c88ddc49...`.
- [ ] 2.2 The note states the correction requires a future release, and the release asset is not
      modified.
- [ ] 2.3 A next-release ticket carries the item.

## 3. Independent verification with the capability gap closed

- [ ] 3.1 The checker is dispatched on a different model axis from the writer, with the arm pinned.
- [ ] 3.2 The checker is given the ability to fetch served bytes and to run the suite, if the lane
      contract permits it; its own NOT_RUNs, if any remain, are recorded rather than replaced.
- [ ] 3.3 The checker's verdict is bound to the frozen candidate commit and tree.

## 4. Control plane (handed over, not applied)

- [ ] 4.1 The `VERIFY_SECURITY` pool ordering defect is documented with a candidate patch, in a
      not-applied form.
- [ ] 4.2 The round records that it did not edit the registry.

## 5. Publication and closeout

- [ ] 5.1 The candidate is committed and pushed; the remote head is read back.
- [ ] 5.2 The evidence packet is emitted and verified against the committed blobs in a fresh fetch.
- [ ] 5.3 A handover record carries the exact subject identity, open tickets, owner decisions, rollback
      pointer and next legal action.
- [ ] 5.4 No secret appears in the diff, the branch, the packet or the logs.
- [ ] 5.5 Owner decisions are requested in one-action form and not executed by the round.
