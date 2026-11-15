#!/usr/bin/env bash
# Closure VERIFY: adversarial re-measurement of A1..A8, the owner receipt and the subset replay.
#
# Deliberately WITHOUT --force-rank: A8 claims that --require-arm now constrains the selection, so a run
# that needs force-rank to reach gpt-6.1-sol would falsify its own claim. The receipt it produces is part
# of the evidence: selection_filter.candidates_after must be exactly the required arm.
set -u
cd /c/Projects/Agent_Workspace/wt-r19-delivery || exit 9
OUT=/c/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/outc
mkdir -p "$OUT"
NONCE=$(python -c "import secrets;print(secrets.token_hex(8))")
echo "nonce=$NONCE"
PYTHONPATH=src python scripts/hgk-lane-dispatch.py \
  --lane VERIFY_SECURITY \
  --brief "C:/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/BRIEF_VERIFY_CLOSURE.md" \
  --prompt "Run nonce: $NONCE. You are the independent VERIFY lane for the R20 closure round. Follow the brief: re-measure C1-C10 yourself, HOLD anything you cannot execute, FAIL anything whose measured number disagrees. Put HOLD above PASS whenever a claim is only true by construction. Write CLOSURE_CHALLENGE_R20.json in your cwd. End your final message with exactly: NONCE=$NONCE" \
  --nonce "$NONCE" \
  --require-arm openai-codex/gpt-6.1-sol \
  --identity-source codex-rollout \
  --codex-home "C:/Users/user/.codex" \
  --allow-human-home-transport \
  --relay-base https://chatgpt.com/backend-api/codex \
  --cwd "C:/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/outc" \
  --timeout 900 \
  --json-out "C:/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/closure_verify_stdout.json" \
  > "/c/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/closure_verify_raw.txt" 2>&1
echo "dispatch_rc=$?"
