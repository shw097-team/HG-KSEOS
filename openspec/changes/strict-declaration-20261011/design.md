# Design: strict declaration

## The operative rule

> A declared value is admitted only at its exact JSON type, and a record counts as evidence only when it
> is a complete, LF-terminated, strictly UTF-8-decodable JSON value read in full. No verdict may be
> decided from a coerced, substituted, split-invented or partially read value.

## Decision: amend the admitted write set (OQ11 option (a))

The alternative — accepting the residual — was rejected because the residual would live in the component
that decides **which arm is spawned**. A pool whose declaration is coerced can select or exclude an arm
against a declaration it does not literally satisfy, and that misinformation would then have to be
disclosed forever as a known false green on a governance surface. The friction of the amendment is
bounded: three constructor calls in one untracked candidate module, one raw-rank read, no promotion.
Authority: the owner's order for this turn, recorded in the admission source locator.

## Type discipline

| Field | Admissible | Rejected |
|---|---|---|
| `rank` | JSON integer, `bool` explicitly excluded (Python `bool` is an `int` subclass) | float (`1.9`), string (`"1"`), `true`/`false`, `null`, object, array |
| `provider`, `model` | JSON string | integer (`7`), `true`, `null`, object, array |
| `role`, `transport`, `engine` | absent, or JSON string | any non-string present value |

A wrong type raises the existing typed `LaneRouteError` class under a **new code** so a caller can tell a
TYPE defect from a missing key (`ERR_SLOT_POOL_ENTRY_MALFORMED` stays for a missing/structural defect).
A well-typed pool takes the identical code path, so non-regression is provable by the same suite.

## Carrier discipline

1. Iterate the captured stream as **bytes split on `b"\n"`** — never `str.splitlines()`, which also splits
   on U+2028, U+2029, `\x85`, `\x0b` and `\x0c`, inventing line boundaries the protocol does not have.
2. A trailing fragment with no terminator is **not** a row.
3. Decode each line with `errors="strict"`; an invalid byte makes the line **not** a row (it must never
   become a surrogate or U+FFFD).
4. Strip one trailing `\r` so a CRLF stream still parses.
5. The nonce check stays on the **preserved bytes** (`nonce.encode("utf-8") in raw_bytes`).
6. A line that decodes but is not a JSON object of the expected shape is a typed rejection recorded as a
   detail, never a top-level code (the previous round's precedence table still governs the top-level code).

Acceptance evidence that this does not over-block: the live EXECUTE and VERIFY/SECURITY lanes must still
turn green under the same rule — the real Codex CLI emits newline-terminated UTF-8 JSON lines. That is a
measurement, not an assumption.

## Risk and rollback

- Risk: an over-strict rule rejects real lane output. Mitigation: the live-lane turns in this same round
  are the counter-evidence; and the pre-change bytes of all four files are backed up before the writer runs.
- Rollback: byte copy from the round's `rollback/` directory.

## Non-claims

- Not an acceptance. No claim that the class is closed everywhere in the product.
- The previous round's oracle is **not** amended.
