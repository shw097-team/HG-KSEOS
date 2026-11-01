## 1. Source freeze and governance binding

- [ ] 1.1 Canonical package root recorded verbatim; MANIFEST.md rows, artifact_checksums.sha256 rows and all
      outer-ZIP members re-derived from bytes (82 / 83 / 84) with zero mismatch.
- [ ] 1.2 22-WP typed DAG re-derived: node count, edge count, edge types, dependency/edge set equality,
      acyclicity, and per-node required fields; no unknown node references.
- [ ] 1.3 SharedSpine project `FHS-MSC-R18-20261029` started; one requirement per WP-FHS node registered and
      frozen with an idempotency key.
- [ ] 1.4 Native admission refusal measured (`ERR_NATIVE_BUNDLE_REQUIRED`) so the gate is proven to fire
      rather than assumed.

## 2. L0/L1 execution (agent-closeable)

- [ ] 2.1 WP-00 Source/Host discovery receipt PASS.
- [ ] 2.2 WP-01 authority/oracle/profile ledger with file#line locators and a silent-promotion check.
- [ ] 2.3 WP-19 supply-chain scan with a planted canary, license/NOTICE inventory, SBOM and path-leakage class.
- [ ] 2.4 WP-21 96-cell oracle suite re-executed on the isolated copy; disposition distribution reported.
- [ ] 2.5 Candidate's own author validator re-executed; measured counts compared with the claimed 2789/0.
- [ ] 2.6 WP-15 / WP-16 / WP-05 / WP-07 / WP-04 reuse-and-verify receipts against existing artefacts.
- [ ] 2.7 WP-21 cell/oracle traceability matrix built by the EXECUTE lane.

## 3. Bounded repair

- [ ] 3.1 Every RED found in section 2 reduced to its first_fail cone, patched, and re-run GREEN.
- [ ] 3.2 Residue named per defect with the evidence that would close it; no oracle weakened.
- [ ] 3.3 Probe defects found in this round's own instruments recorded with the correction applied.

## 4. Native-gated packages (typed PARK)

- [ ] 4.1 WP-02 / WP-03 / WP-17 measured against existing bindings; parked with owner + next legal action.
- [ ] 4.2 WP-06 / WP-08 / WP-10 / WP-11 / WP-12 / WP-13 / WP-14 / WP-20 parked per WP (no family-level
      blocker inference, no fabricated permit).

## 5. Independent acceptance and delivery

- [ ] 5.1 Frozen subject handed to a different-principal checker lane; verdict recorded with its ceiling.
- [ ] 5.2 MVS01–10 mapping from this round's real receipts; MVS10 remains not executed.
- [ ] 5.3 Candidate branch + commit + push + PR per affected repo (no main, no force-push, no merge/tag/release).
- [ ] 5.4 STATUS/HANDOFF + RESUME_HERE + machine-readable state; Kanban cards reconciled to ledger rows.
