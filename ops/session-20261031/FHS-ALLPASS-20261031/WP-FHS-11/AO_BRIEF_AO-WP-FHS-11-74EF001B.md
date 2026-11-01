# VERIFY brief — WP-FHS-11, the NINE cells (one work package)

> Third sitting. The first said clause 3 and 4 FAIL (the receipt dropped `completed`; the roll-up counted six
> carried rows without opening their receipts). The second said clause 4 still FAIL, with the reason that matters:
> four of the six carried `archive_prefix` values no longer match `PIPD/dist/prof-*/export_manifest.json`. Both
> findings were acted on. All nine cells are now re-measured against today's manifests — there are no carried rows
> left to argue about. Judge what is in the files now.

You are the independent checker. The maker produced receipts; your job is to decide whether the CLAIMS survive
an independent read of the artefacts. Do not take the maker's summary as evidence, and do not accept a receipt
because it says PASS.

Subject (read-only, on this machine):
- `C:\Projects\Agent_Workspace\HG-KSEOS\ops\session-20261031\FHS-ALLPASS-20261031\WP-FHS-11\NINE_CELL_TABLE.json`
- `C:\Projects\Agent_Workspace\HG-KSEOS\ops\session-20261031\FHS-ALLPASS-20261031\WP-FHS-11\hermes-cells\HERMES_CELL_LITE.json`
- `...\hermes-cells\HERMES_CELL_STANDARD.json`
- `...\hermes-cells\HERMES_CELL_ASSURED.json`
- the archives the digests refer to: `C:\Projects\Agent_Workspace\PIPD\dist\prof-LITE\export_manifest.json`,
  `...\prof-STANDARD\export_manifest.json`, `...\prof-ASSURED\export_manifest.json`
- the script that produced them: `C:\Projects\Agent_Workspace\HG-KSEOS\scripts\wp11_hermes_cells.py`
- the tool that derived the table: `C:\Projects\Agent_Workspace\HG-KSEOS\scripts\wp11_nine_cell_rollup.py`

Decide each clause PASS or FAIL, naming the command output or the exact field you relied on:

1. For each of the three Hermes cells the positive answer contains the token that was issued for THAT cell
   (not a token from another cell) and the archive sha256 of THAT profile read from PIPD's own export manifest.
2. In each cell the probe skill was removed before the negative run, and the negative answer contains neither
   the token nor the digest.
3. The served model/provider recorded in each receipt is a real measurement (the receipt carries a Hermes usage
   file's `model`, `provider`, `completed`), not a maker-supplied string.
4. `NINE_CELL_TABLE.json` is arithmetic over its cells: denominator 9, and every cell's verdict is either PASS
   with its own measured fields or an explicit non-PASS. Look for any cell that is PASS without a receipt.
5. The three Hermes cells' loader half is honestly described: the host loads a skill INDEX into context and
   fetches the body on demand, so "the model half" had to be measured by having the host load the body through
   its own loader. Say whether the receipts measure that, or something weaker that resembles it.

Write your verdict JSON as the LAST fenced ```json block of your reply, in this shape:

{"requirement":"WP-FHS-11","clauses":[{"id":1,"verdict":"PASS|FAIL","evidence":"..."}, ...],"overall":"PASS|FAIL"}

If you cannot judge a clause from the artefacts alone, say VOID for that clause and name what is missing. A
clause you cannot judge is not a PASS. Do not modify anything: read-only.


---

Before you finish, echo this nonce verbatim on its own line: NONCE-ECHO: AO-WP-FHS-11-74EF001B
