# HG-KSEOS native source — B1 review baseline

Private, allowlisted source export of the existing HGK control plane. This
repository is a code delivery location, not another issuer or control plane.

The initial baseline contains tracked Python/SQL sources and the two focused
Shared Spine / ordering test files. It intentionally has no original Git history,
runtime DB, credentials, raw evidence, personal knowledge base, or historic
untracked data. `SOURCE_EXPORT.json` binds every exported source file to the
original local HEAD. Later B1 commits contain only the reviewed repair WriteSet.

Python >=3.12. B1 crypto tests require the existing `cryptography` runtime;
cross-language canonicalization tests require Node.js. Run tests with
`PYTHONPATH=src;tests` in your shell environment and `python -m unittest`.

Maker test success is not native admission or independent acceptance. Owner
protected trust registration, actual policy/TaskKind/Oracle issuance, live
effects and independent checker acceptance remain separate requirements.


## B1 closure 2026-10-28

`b1_closure_20261028/` is the evidence index for the FHS-MSC B1 bootstrap-repair round (PKG_00~08) on the HG-KSEOS side.

- `b1_closure_20261028/EVIDENCE_INDEX.md` — question → file#line → the command that reproduces it
- `b1_closure_20261028/MANIFEST.json` — per-file bytes + sha256 (the packet is verifiable offline)
- `b1_closure_20261028/HANDOVER.md` — ten-point orientation for an external reviewer

Claim ceiling (measured, not asserted): `mission_complete true` under `b1_closure_20261028/evidence/GATES.json`
means the gate conjunction passed, no residual blocker remained, and every blocking declaration was
owner-ruled. It does **not** mean release (`release: NOT_RUN`), promotion, or third-party acceptance.
Databases, raw lane output, the owner key envelope and credentials are excluded by design.
