# FHS-MSC handoff execution — requirement delta

## ADDED Requirements

### Requirement: Delivered payload integrity is verifiable from the manifests alone

A receiver SHALL be able to verify every payload row of the delivery against
`SHA256_PAYLOAD_MANIFEST.json` using only the delivered tree, and the count of rows that resolve SHALL
equal the count of rows declared.

#### Scenario: canonical layout resolves every row

- **WHEN** the delivered tree is unpacked with the directory names the manifest addresses
- **THEN** all 909 rows match on byte length and SHA-256, with zero mismatch and zero missing
- **AND** the two files present but undeclared are the two manifests, which declare themselves excluded

#### Scenario: a renamed top-level directory is a named defect, not corruption

- **WHEN** the top-level book directory arrives under a different name than the manifest addresses
- **THEN** the verifier reports the alias explicitly
- **AND** the receiver does not conclude that the payload is missing

### Requirement: A sealing claim exists only when the sealed bytes exist

Any statement that the delivery was sealed into archives SHALL be accompanied by the archive bytes, or
by a readback manifest whose archives are present and digest-matching.

#### Scenario: declared archives are absent

- **WHEN** the delivery manifest lists archives that are not present in the delivery
- **THEN** the receiver reports the absence and does not treat the declared digests as verified
- **AND** any replacement seal is labelled a new artefact, never a reproduction of the declared one

### Requirement: The first work is reproducible on a clean root

Re-executing `WP-FHS-15` from the delivered tooling SHALL produce the three SPECs, the source readback
and the 22-WP DAG byte-identically, and SHALL report how every other artefact differs.

#### Scenario: deterministic artefacts reproduce

- **WHEN** the first work is re-executed in an isolated root
- **THEN** `ProductSPEC`, `ArchitectureSPEC`, `ProgramSPEC`, `SourceReadback` and `ORIGINAL_22_WP_DAG`
  are byte-identical to the delivery

#### Scenario: identity artefacts differ for a stated, tested reason

- **WHEN** `PI-PKG`, `TaskSpecSeed` or `ExecutionHandoff` differ
- **THEN** the difference is attributed to a tested mechanism, with a control and a repair, not to
  "timestamps"

### Requirement: The package's own acceptance harness runs on the package

The 35-check harness shipped with the delivery SHALL execute successfully against the delivered
snapshot, or its failure SHALL be recorded with the failing check named and the cause isolated.

#### Scenario: harness fails as shipped

- **WHEN** the harness is run from the delivered files without modification
- **THEN** the failing check, the exception and the ordering cause are recorded
- **AND** the repaired result is recorded separately, never replacing the as-shipped record

### Requirement: Declared dependency closures are derivable from typed edges

A declared `dependency_closure` SHALL equal the ancestor set computed from the typed `depends_on` edges
of its work package, or the divergence SHALL be reported to the owner who owns the graph.

#### Scenario: declaration and graph disagree

- **WHEN** the declared closure contains a work package that is not an ancestor in the typed graph
- **THEN** the verifier reports REVIEW with both sets
- **AND** the receiver does not re-type the original graph to make the declaration true

### Requirement: Lane turns produce receipts that survive their own success

A lane dispatch SHALL write its receipt whenever a spawn completed, and a served-arm assertion SHALL
compare like with like.

#### Scenario: receipt assembly fails after a successful spawn

- **WHEN** the model answers and the dispatcher then raises while building the receipt
- **THEN** the turn is counted as lost evidence and the defect is recorded with before/after digests

#### Scenario: served arm carries a transport prefix

- **WHEN** the rollout identity reports a provider and a slash-form model while the assignment lists the
  bare arm
- **THEN** the comparison is normalised, or both raw and normalised values are emitted, so a correct
  turn cannot read as an unassigned arm

## MODIFIED Requirements

None. This change is additive and modifies no existing normative requirement.

## REMOVED Requirements

None.
