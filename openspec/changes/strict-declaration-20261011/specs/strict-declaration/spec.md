# Strict declaration

## ADDED Requirements

### Requirement: A declared value is admitted only at its exact JSON type

The route-slot resolver SHALL admit a pool entry only when `rank` is a JSON integer and `provider` and
`model` are JSON strings, and SHALL raise the typed `LaneRouteError` class when they are not, instead of
coercing them.

#### Scenario: a fractional rank is refused
- **WHEN** a pool declares `"rank": 1.9`
- **THEN** loading raises a typed `LaneRouteError` and no lane is returned
- **AND** the entry is not silently rounded to rank 1

#### Scenario: a boolean rank is refused
- **WHEN** a pool declares `"rank": true`
- **THEN** loading raises a typed `LaneRouteError`
- **AND** the value is not accepted merely because Python's `bool` is an `int` subclass

#### Scenario: an integer model is refused
- **WHEN** a pool declares `"model": 7`
- **THEN** loading raises a typed `LaneRouteError`
- **AND** the value is not made to match a declaration of the string `"7"`

#### Scenario: a well-typed pool is unaffected
- **WHEN** a pool declares an integer `rank` and string `provider`/`model`
- **THEN** it loads exactly as before, through the same code path

### Requirement: A record counts as evidence only when it is complete and strictly decodable

The lane dispatcher SHALL treat a captured line as a candidate record only when it is terminated by LF or
CRLF, is strictly UTF-8 decodable, and parses as a JSON object of the expected shape. It SHALL NOT split
the captured stream on Unicode line boundaries.

#### Scenario: an unterminated carrier is not a row
- **WHEN** the captured stream ends with a complete-looking JSON object that has no line terminator
- **THEN** it does not count as a row and cannot produce a success

#### Scenario: an invalid UTF-8 carrier is not a row
- **WHEN** a line contains a byte that is not valid UTF-8
- **THEN** the line is not a row, is counted as undecodable, and cannot satisfy the nonce
- **AND** no substituted character or surrogate is produced from it

#### Scenario: a U+2028 terminator does not invent a line boundary
- **WHEN** a carrier is terminated by U+2028 rather than LF or CRLF
- **THEN** it is not split into a valid row

#### Scenario: a CRLF stream still parses
- **WHEN** the stream is CRLF-terminated
- **THEN** each line parses as a row exactly as with LF

### Requirement: The previous round's frozen behaviour does not regress

The dispatcher's classification of a responding arm that emitted no nonce, the skip of a declared
not-dispatchable arm and its `--force-rank` override, and the lane-home isolation refusal SHALL all
continue to hold, and the existing tests and probes SHALL continue to pass.

#### Scenario: the frozen classification still holds
- **WHEN** an arm answers with a valid usage receipt and no nonce
- **THEN** the code is the requirement's nonce-absent code with the arm named

#### Scenario: existing gates stay green
- **WHEN** the suite and the permanent probes are run after the change
- **THEN** every pre-existing test and probe still passes
