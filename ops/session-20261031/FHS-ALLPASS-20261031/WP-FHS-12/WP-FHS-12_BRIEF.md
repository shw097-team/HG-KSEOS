# WP-FHS-12 brief — W18 Ordinary Goal in a fresh PID

## What the delivery asks (04_FABRIC_HGK_CONTROL §4.4)

Three normal situations, all without pasting the B1 long prompt:

1. **first valid source** -> the first legal FUO
2. **same WorkID, new process** -> check Scope/Policy/World, resume the unfinished part, replay no effect
3. **source or policy changed** -> invalidate only the affected plans, re-check Admission, keep unrelated results

Any of `Default Profile / Skills / Served` not truly read back -> `W18_NORMAL_HOLD`. It must never be reported as
AUTO_READY on the strength of a config file.

## What was attempted here

`hermes -z "<ordinary goal>" --pass-session-id` in a clean cwd, twice (serve, then resume).

## What happened

The one-shot CLI cannot start an agent at all on this host:

```
RuntimeError: Failed to initialize OpenAI client:
  No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'
```

The bundled `openai` package under `D:\Hermes-Recovery\h22` is older than the code that imports it. This is a
host runtime dependency defect, not a WP-FHS-12 design gap and not a missing capability: the desktop session
serving this very turn runs the same agent loop and reaches its model fine (provider `opencode-go`,
`deepseek-v4.1-flash`), because that path does not construct the OpenAI client.

## Verdict

`W18_NORMAL_HOLD` — and the HOLD is honest for a reason the spec anticipated: Served was not read back, so nothing
may be claimed. The exact unblock is one dependency upgrade in the bundled runtime, followed by re-running the two
commands unchanged.
