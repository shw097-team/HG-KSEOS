# skill-mainfile-cap-governance

## ADDED Requirements

### Requirement: Main-file edits are cap-gated before they are attempted
A patch to a skill main file SHALL be measured with the governing convention (text-mode
`len()`, LF-normalized) and SHALL be rejected locally when the resulting length exceeds
100,000 characters.

#### Scenario: Pointer insertion on a full main file
- **WHEN** a pointer line is added to a main file at 99,996 governed characters
- **THEN** the round SHALL first free at least the pointer's character cost, and only then apply the patch

#### Scenario: Measurement conventions disagree
- **WHEN** an independent checker measures bytes or raw CRLF characters and reports "over cap"
- **THEN** the discrepancy SHALL be reported as a convention mismatch, not as a defect in the file

### Requirement: Salvaged lessons are reachable from the main file
Every section relocated to `references/` SHALL be reachable from the main file through a
declared pointer (trigger condition + target path) and a routing-map entry.

#### Scenario: A lesson exists only in references
- **WHEN** a governance lesson is stored in a reference file with no pointer in the main file
- **THEN** the round SHALL record it as an unreachable-lesson finding and add the pointer

### Requirement: Relocation is byte-exact and reversible
Relocating a section SHALL preserve the original bytes of the relocated text, and the round
SHALL prove losslessness by reconstructing the pre-split file from the post-split file.

#### Scenario: Reconstruction mismatch
- **WHEN** the reconstruction differs from the frozen pre-split copy
- **THEN** the round SHALL fail and the subject SHALL be restored from the frozen copy

### Requirement: One authoritative copy per lesson class
Where the same lesson class exists in more than one skill surface, exactly one copy SHALL be
authoritative and the others SHALL become pointers to it.

#### Scenario: Duplicated rule set
- **WHEN** two surfaces carry the same rule set
- **THEN** the round SHALL name the authoritative surface and reduce the other to a pointer

### Requirement: Regrowth is bounded
After a split, a declared main-file ceiling SHALL be checked by a repeatable probe so that a
later round appending lessons fails the probe instead of silently re-crossing the cap.

#### Scenario: Later round appends past the ceiling
- **WHEN** the main file grows past the declared ceiling
- **THEN** the probe SHALL fail and the round SHALL relocate or consolidate before appending
