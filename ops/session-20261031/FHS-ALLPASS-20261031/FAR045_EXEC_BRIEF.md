NONCE-ECHO: FAR045-EXEC-FE39C21E

ONE work package. Bounded write. Two files only: scripts/round_close_gate.py and scripts/far_lane_gate.py.

Defect 1 (round_close_gate.py, around line 91): the receipt list defaults to EMPTY and the gate checks only the receipts
the caller supplied. It never derives the required lane set from the mandate. With no blocking TTs and no supplied
receipts its lane checks contribute nothing. "Every supplied receipt passes" does not establish "every required lane
ran" -- that is the vacuous-pass pattern AGENTS.md section 4 forbids.

Fix: derive the required lane set from the mandate (default PLAN, EXECUTE, VERIFY_SECURITY) and refuse when a required
lane has no receipt. A caller may narrow it only by naming the narrowing explicitly, and the narrowing must appear in
the output.

Defect 2 (far_lane_gate.py, around line 40): it requires only PLAN and VERIFY_SECURITY. EXECUTE is absent from its
required set. Fix: require all three by default.

Do not weaken any existing refusal. Do not delete tests. Run the existing suites under tests/ that touch these gates and
report the counts. If a test now fails because the new default is stricter, that test was asserting the vacuous pass --
say so and update it, do not revert the fix.

Begin your reply with the nonce line exactly as given. Report: files changed, the exact refusal codes added, and test
counts before and after.
