# G19 re-declared after an owner layout optimisation — new round, new denominator

**Round**: `W0_R2_REREG_20261112` · **Basis**: owner decision, recorded in the round declaration
**Claim ceiling**: declared inventory + local re-read. Not an acceptance, not a release, not native.

## What the owner decided

The copy-register check (G19) had been failing on 308 members whose declared paths no longer existed. The
owner's ruling: those paths were changed **by the owner personally** as a layout optimisation, and three
documents were **deleted by the owner personally to free local disk space**. Both are owner actions on
historical material, and neither is a defect of the subject under test.

So the right response is not to argue with the measurement and not to edit the past verdict — it is to
re-declare the register against the layout that exists now, with a new denominator and new digests, and to
let a re-read produce a fresh verdict.

## What was produced

| artefact | content |
|---|---|
| `COPY_REGISTER_CURRENT.json` | **73 groups / 431 copies**, every member with path + sha256 + bytes, plus a `lineage` block carrying `old_copies → new_copies → delta` per group |
| `ROUND_DECLARATION.json` | the round's own denominator, the two owner decisions (OD-1 deletion, OD-2 layout), and the verdict rule |
| `G19_REREG_CHECK.json` | **431/431 members re-read; V1 absent 0, V2 digest/size drift 0, V3 count 0, V4 distinct-digest 0, V5 undeclared same-name 0 → PASS** (15.5 s) |
| `OWNER_WAIVER_G19.md` | the ruling, its scope, and its limits |

The previous register declared 90 group entries / 437 copies; grouping case-insensitively collapses the
duplicates to 76 subjects, of which **3 have no copy left** because the owner deleted them. Those three are
kept in the register as `owner_deleted_groups` with `status: OWNER_DELETED_20261112` — the denominator
shrank from 437 to 431 and the record says why, rather than quietly dropping rows.

Groups that grew (16 → 18, 17 → 19) did so because archive junctions restored earlier make more copies
visible; each group carries its own delta, so no number moves without a trace.

## What this deliberately does not do

1. **It does not rewrite the past round.** `FHS_W0_R13_ACCEPTANCE_20261108` was measured on 2026-11-11
   against the register as it then stood: 19/22 with G19 `MEMBER_ABSENT`. That number stands as the record of
   that round. Editing `lanes/D/COPY_REGISTER_ALL.json` or `gate_r20.py` to turn it green would be
   retro-fitting a verdict, which is the failure mode the gate was written to catch.
2. **It is not a licence to substitute a different revision.** The archive holds a file named
   `FHS_PIPD-LS-PKG_W0_r6.md` whose digest is `69a08e7f…`; the declared subject is `9f9eb261…`. Same name is
   not the same document, so it is not counted as a copy. This is the distinction a copy register exists to
   make.
3. **It is not an acceptance.** The register answers "where do these documents live and what do they hash
   to", not "is their content correct".

## Effective status

| where | G19 |
|---|---|
| R13 round | `MEMBER_ABSENT` (historical measurement, unchanged) |
| `W0_R2_REREG_20261112` | **PASS**, 431/431 re-read at declared digests |
| blocking? | **no** — owner decision on deleted files and on the layout change |
