# hgk-r11-session-handover-20261016

## Why

The mission `CNV-PIPD-LS-SP-20261015` has accumulated ten rounds of work whose state lives in round roots, a
shared spine, several stale change records, and an untracked local control plane. A reader of the conversation is
not a usable carrier for that state: the user has explicitly asked to close the session so a NEW session can
continue the remaining work. What is missing is a single entry point plus a machine-readable resume manifest,
measured - not asserted - and published as candidate evidence.

## What Changes

- ADD one handover entry document that a new session reads first: mission anchors, claim ceiling, protected paths,
  the credential PATH (never a value), the lane dispatch helpers, and the standing owner rules.
- ADD a machine-readable resume manifest listing every unfinished item with class, owner, ONE next action,
  locator and the measurement that shows it is unfinished.
- ADD a measured inventory of every open openspec change record with a disposition class
  (CLOSE_CANDIDATE / CONTINUE / OWNER_DECISION / HISTORICAL) and a one-action path per row.
- ADD an integrity audit of everything the new session will rely on (locators, dangling pointers, guard subject).
- NO change to any published R6..R10 packet, to the guard subject, to the lane registry, or to a peer round's tree.

## Impact

- Affected specs: session handover (this change), governance records (read-only inventory).
- Affected code: none in the product; the round adds one local tooling successor and one publication successor.
- Claim ceiling stays `LOCAL / candidate-only`: this change produces a handover, not an acceptance.
