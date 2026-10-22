# Proposal: strict declaration — no verdict from coerced or lossily-decoded evidence

## Why

The previous round's independent review (pass 6) constructed five false successes against the lane
diligence surface. Two of them live outside its admitted write set, in the route-slot resolver:

- `src/hg_kseos/lane_route_resolver.py:120-123` builds a `PoolEntry` through `int(e["rank"])`,
  `str(e["provider"])`, `str(e["model"])`. A pool declaring rank `1.9` or the JSON integer model `7` is
  silently made to look well-typed, and can then be matched or pinned against a string declaration it does
  not literally satisfy.
- `scripts/hgk-lane-dispatch.py:949` coerces raw declaration ranks the same way.

Three more are inside the dispatcher's carrier handling: `str.splitlines()` (line 273 / 778) also splits
on Unicode line boundaries such as U+2028, and a carrier is accepted without requiring a terminator or
strict UTF-8 validity, so an unterminated, non-UTF-8, or U+2028-terminated carrier can each produce a
success while containing no strictly-decodable nonce.

Those five share one cause: **a verdict decided from evidence the surface had to coerce, substitute or
partially read.** That is a misinformation path inside the component that decides which dispatch arm is
spawned — the exact defect class this work exists to remove.

## What changes

1. The resolver **refuses** a wrongly-typed declaration with a typed error instead of coercing it: `rank`
   must be a JSON integer (`bool` explicitly excluded), `provider` and `model` must be JSON strings.
2. The dispatcher's raw-pool read applies the same exact typing instead of `int()`.
3. A carrier counts only when it is a complete line terminated by LF or CRLF, strictly UTF-8 decodable,
   and a JSON object of the expected shape; the nonce stays decided on the preserved bytes.
4. The previous round's frozen classification, declared-capability skip/override, the lane-home isolation
   refusal, all existing tests and every existing probe must not regress.

## Impact

- Files: `src/hg_kseos/lane_route_resolver.py`, `scripts/hgk-lane-dispatch.py`,
  `config/lane-route-slots.candidate.json`, `tests/test_lane_dispatch_ao_guard.py`.
- The write-set extension to the resolver is the **owner's grant**, recorded in the round's admission
  source locator; the maker does not broaden its own permissions.
- No promotion, no canonical-store write beyond the round's own admitted audit rows, no service restart.

## Not in scope

- No claim that the class is closed everywhere in the product. The claim is bounded to this surface and
  the artifacts it reads.
