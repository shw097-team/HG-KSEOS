# Skill main-file cap remediation (hgk-governed-execution SKILL.md)

## Why

`hgk-governed-execution/SKILL.md` measures 99,996 of the 100,000 governed characters
(`MAX_SKILL_CONTENT_CHARS`, LF-normalized `len()`), i.e. **4 characters of headroom**. Any
`skill_manage(action='patch')` that adds a pointer line is rejected before it reaches disk.

Consequence: governance lessons that belong in `references/` can be written (supporting-file
writes are separate), but the main file **cannot advertise them**. The main file's routing map
and its `references/adversarial-verification-rounds.md` therefore stay disconnected, and every
new governed round that appends a lesson to the main file pushes it further past the cap.

## What Changes

- Establish a **main-file size budget gate** before any lesson-append patch: measure with the
  governing convention (text-mode `len()`), require the post-patch length <= 100,000.
- Re-apply the **validated mechanical split** (WO-HGK-SKILL-SPLIT-001 method: byte-exact section
  relocation + 3-line pointer per section + routing-map entry) with a **pre-registered manifest**,
  so the flat 60k-char `Execution-method invariants` section is decomposed by a declared rule,
  not by hand editing.
- Add the missing **pointer** for the adversarial-verification-rounds material and reconcile the
  **duplication** between the in-skill reference file and the standalone skill of the same name.
- Add a **regrowth guard**: after the split, a repeat offender check fails the round if the main
  file re-crosses a declared ceiling.

## Impact

- Affected capability: `skill-mainfile-cap-governance` (new delta spec).
- Subject: the skill store under the Hermes home (`skills/software-development/`).
- Non-goals: no change to Hermes runtime code; no promotion of candidate material; no agent
  self-acceptance; no canonical mutation outside the admitted WorkOrder.
- Rollback: keep the pre-split byte-identical copy and the reverse-reconstruction check from
  WO-HGK-SKILL-SPLIT-001.
