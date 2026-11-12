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
| `COPY_REGISTER_CURRENT.json` | **73 groups / 394 copies** (432 found, junctions deduped by real path), every member with path + sha256 + bytes, plus a `lineage` block carrying `old_copies → new_copies → delta` per group |
| `ROUND_DECLARATION.json` | the round's own denominator, the two owner decisions (OD-1 deletion, OD-2 layout), and the verdict rule |
| `G19_REREG_CHECK.json` | **394/394 members re-read; V1 absent 0, V2 digest/size drift 0, V3 count 0, V4 distinct-digest 0, V5 undeclared same-name 0 → PASS** (15.5 s) |
| `OWNER_WAIVER_G19.md` | the ruling, its scope, and its limits |

The previous register declared 90 group entries / 437 copies; grouping case-insensitively collapses the
duplicates to 76 subjects, of which **3 have no copy left** because the owner deleted them
(`W0_r4`, `W0_r7`, the non-normative audit appendix). One further document, `FHS_PIPD-LS-PKG_W0_r6.md`, was
first recorded as missing and then **located by the owner**: it hashes to the declared `9f9eb261c44f…` at
`…/FHS/FHS_PIPD-LS-PKG/實作/W0/OLD/FHS_PIPD-LS-PKG_W0_r6.md`, so the shortfall is two contents, not three. Those three are
kept in the register as `owner_deleted_groups` with `status: OWNER_DELETED_20261112` — the denominator
shrank from 437 to **394** and the record says why, rather than quietly dropping rows. (An earlier revision of
this paragraph said 431; that number has no raw behind it — the register's own denominator and the re-read are
both 394, and the correction is recorded in §7.)

Groups that grew (16 → 18, 17 → 19) did so because archive junctions restored earlier make more copies
visible; each group carries its own delta, so no number moves without a trace.

## What this deliberately does not do

1. **It does not rewrite the past round.** `FHS_W0_R13_ACCEPTANCE_20261108` was measured on 2026-11-11
   against the register as it then stood: 19/22 with G19 `MEMBER_ABSENT`. That number stands as the record of
   that round. Editing `lanes/D/COPY_REGISTER_ALL.json` or `gate_r20.py` to turn it green would be
   retro-fitting a verdict, which is the failure mode the gate was written to catch.
2. **It is not a licence to substitute a different revision.** The archive also holds a file named
   `FHS_PIPD-LS-PKG_W0_r6.md` whose digest is `69a08e7f…`; the declared subject is `9f9eb261…`. Same name is
   not the same document, so that copy is not counted. (The declared revision itself was later found at the
   owner's new path and does match — recorded as a correction, because my earlier "gone" reading was wrong.) This is the distinction a copy register exists to
   make.
3. **It is not an acceptance.** The register answers "where do these documents live and what do they hash
   to", not "is their content correct".

## Effective status

| where | G19 |
|---|---|
| R13 round | `MEMBER_ABSENT` (historical measurement, unchanged) |
| `W0_R2_REREG_20261112` | **PASS**, 394/394 re-read at declared digests |
| blocking? | **no** — owner decision on deleted files and on the layout change |

## 7. Corrections to this document (recorded 2026-11-12, later the same day)

1. **431 → 394** (two places: the denominator sentence and the status table). Basis: the register's own
   denominator is 73 groups / 394 copies, `G19_REREG_CHECK.json` re-read **394/394** with V1–V5 all zero, and
   no raw in either file carries 431. The number was a transcription error in prose, not a second denominator.
2. **The register no longer depends on archive junctions.** Under owner ruling OD-3 the 69 members that lived
   outside the two allowed roots were copied into `FHS_NEXT\roots\legacy_declared\…` (34,095,871 bytes, every
   file hashed against its declared sha256, 0 mismatches), the member paths and the two `roots_scanned`
   entries were re-pointed, and only then were the junctions removed. The re-read after the move is
   **394/394 PASS**. Group counts, copy counts and digests did not move.

Both corrections are additions beside the original text, not rewrites of a past verdict.
