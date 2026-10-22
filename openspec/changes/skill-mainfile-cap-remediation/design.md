# Design decisions

## D1 Measurement convention is part of the contract
`skill_manager_tool._validate_content_size` receives `Path.read_text(encoding='utf-8')` output
(line 488), so CRLF collapses to LF before `len()` is taken. Report the **LF-normalized** count as
governing; report bytes and raw-CRLF counts as secondary. A checker that scores bytes will
disagree with the gate by ~1.2k chars.

## D2 Split before slim
`references/oversized-skill-handling-route.md` ranks mechanical split+route first and forbids
hand-slimming. The 2026-08-14 hand-slim precedent produced two structural breakages and four
tool-limit failures; the 2026-08-15 mechanical split passed with a byte-identical reconstruction.
Reuse the proven route.

## D3 The 60k section needs a declared rule, not a heading split
The section has 0 `###` headings and 0 bold heading lines; a heading-based splitter cannot touch
it. Its 35 lettered blocks use **non-unique labels** (a, b, c, g, i, z repeat), so a label-keyed
split collides. The manifest must key on (start_line, char_span) captured from the frozen copy.

## D4 Pointers are load-bearing, not cosmetic
Moved material is unreachable unless the main file names the trigger and the target path. Plan for
the exact pointer text and its character cost *before* the split, since the 4-char headroom makes
pointer insertion the binding constraint.

## D5 Duplication is a defect class
The same rules currently exist in the in-skill reference file and in a standalone skill created
later by the curator. Two copies drift. One must be authoritative; the other becomes a pointer.
