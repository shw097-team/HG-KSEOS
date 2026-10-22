# r9-far-residual-closure

## Purpose

Define the acceptance shape for the two repairs executed under the FAR decision of round
`CNV-PIPD-LS-SP-20261015` R9-0, and the record corrections that accompany them, without converting any local
observation into an acceptance.

## ADDED Requirements

### Requirement: Validator adaptation preserves the hardening it adapts

Any adaptation of the R8-0 validator to the newer `main` contract SHALL preserve every refusal the hardening
added. It SHALL derive a link's endpoint binding from the bundle's own atoms only when no frozen context is
supplied by the caller, and it SHALL refuse a mapping access that is not a mapping rather than raising.

#### Scenario: A legal link beside its endpoints is validated
- **WHEN** a bundle contains a trace atom and a TraceLink that points at its own endpoints, and the caller
  supplies no frozen context
- **THEN** the link is validated against the digests carried by those atoms, and no `UNBOUND_FROZEN_CONTEXT`
  refusal is emitted

#### Scenario: A caller-supplied binding still governs
- **WHEN** the caller supplies a frozen context that does not bind the link's endpoint
- **THEN** the link is refused, exactly as before the adaptation

#### Scenario: The added refusals still fire
- **WHEN** the M04, M06 and M16 probes are executed against the adapted tree
- **THEN** each reports `observed=REJECT` with `validator_verdict=FAIL`

#### Scenario: A non-mapping oracle declaration is refused, not fatal
- **WHEN** a record carries a `risk_guard` that is not a mapping
- **THEN** the validator refuses the record with a typed finding and does not raise an unhandled exception

### Requirement: A guarded apply is reversible and re-measured

A canonical skill apply SHALL capture a byte-for-byte pre-image, write a receipt naming each path's action
class and before/after digest, rehearse the rollback on a copy, and re-run the round's own regression harness
on the applied tree.

#### Scenario: Every regression check passes after the apply
- **WHEN** the repaired candidate is applied and the harness is run against the applied tree and the pre-image
- **THEN** every check C1–C6 reports PASS and the loader lists the skill as available

#### Scenario: A failing check rolls back
- **WHEN** any check fails, or the loader cannot select the applied skill
- **THEN** the rollback is executed, the pre-image digests are re-verified, and the failure is reported with its
  raw output

### Requirement: Corrections are carried in the same record as the claims they correct

A round that withdraws or recalibrates a prior claim SHALL state which reading is withdrawn and which evidence
replaces it, in the same change as its new findings.

#### Scenario: A non-reproducing claim is withdrawn with its measurement
- **WHEN** a prior claim is re-measured and does not reproduce
- **THEN** the record names the prior claim, the measurement that fails to reproduce it, and the surviving fact

#### Scenario: A resolved question is closed by the governing text
- **WHEN** the governing document itself settles a numbered finding
- **THEN** the finding is closed by quoting that text, not by re-interpreting the measurement

## NON-CLAIMS

Passing these scenarios is local candidate evidence. It is not an independent acceptance, a Gate PASS, a
DOC-05 admission, an AO verdict or a release decision, and it does not clear the 221 planned acceptance cases,
the eight Gates, Fresh G1 or the external report's production decision.
