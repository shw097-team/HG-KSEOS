# scheduled-task-console-window

## ADDED Requirements

### Requirement: A governed supervisor task MUST NOT create a visible console window

A scheduled task that supervises a governed service SHALL launch its work through a host that
does not allocate an operator-visible console (or terminal-hosted) window, and SHALL NOT rely on
a window-hiding directive alone on a host whose default terminal host is Windows Terminal.

#### Scenario: Trigger fires with no governed task running

- **WHEN** the supervisor task fires on its repetition trigger while no governed task is executing
- **THEN** the host-measured window instrument observes no visible window of class
  `CASCADIA_HOSTING_WINDOW_CLASS` or `ConsoleWindowClass` attributable to that trigger
- **AND** the supervisor still produces its receipt with a fresh timestamp, proving that the work ran

#### Scenario: Window-hiding directive is insufficient

- **WHEN** a task relies on `<Hidden>true</Hidden>` or a `-WindowStyle Hidden` command-line directive
- **THEN** the round records the measured outcome rather than the declared intent, and treats the
  directive as unproven if the instrument observes a visible window

### Requirement: A supervisor MUST leave an auditable run history

A repeating supervisor SHALL append an immutable record of every run (sequence, timestamp, status,
restart count, health) so that whether the supervisor ever acted can be answered after the fact,
and SHALL NOT allow a recovery action to repeat within a single epoch.

#### Scenario: Steady state over many runs

- **WHEN** the supervisor runs many times while the supervised service is healthy
- **THEN** the history gains exactly one record per run and no earlier record is lost or rewritten
- **AND** the restart count recorded in the history answers whether any recovery ever occurred

#### Scenario: Service unhealthy at trigger time

- **WHEN** the supervised service is unhealthy when the supervisor fires
- **THEN** at most one restart is attempted within that epoch
- **AND** the recovery budget does not consume the following trigger interval

### Requirement: The convergence MUST preserve the governed semantics

A change to a governed supervisor task SHALL preserve its governance arguments, trigger family,
logon type and failure behaviour, and SHALL keep the documented rollback valid.

#### Scenario: Semantics preserved after the change

- **WHEN** the task definition is read back after the change
- **THEN** it still invokes the supervisor with `-Action Run -MaxRestarts 3 -WindowSeconds 300`,
  still carries the logon trigger plus the five-minute repetition, and still fails closed rather
  than looping indefinitely

#### Scenario: Rollback is available

- **WHEN** the preimage recorded before the change is restored
- **THEN** the registered task definition is byte-identically the pre-change definition
