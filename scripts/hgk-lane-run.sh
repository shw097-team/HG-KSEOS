#!/usr/bin/env bash
# hgk-lane-run.sh — the ONLY sanctioned way to invoke scripts/hgk-lane-dispatch.py.
#
# Why this exists (measured 2026-10-29, two named defects, both maker-side):
#   D-A  "--force-rank 2" pins the ladder to one arm. It is a PROBE flag: it exists so a receipt
#        can prove a SPECIFIC arm serves. Used for a production run it converts a capacity blip
#        into ERR_LANE_ALL_ROUTES_EXHAUSTED (observed: 4 declared arms, 1 tried, 59.18s, no receipt).
#        Nobody authorised it; it was copied out of a proof recipe into a run.
#   D-B  The dispatcher spawns the lane as a foreground child of its caller. When the caller dies
#        (tool-level timeout), the lane dies with it and --json-out is never written (observed:
#        two attempt dirs at 22:42 / 22:48, zero receipts, zero live processes). The dispatcher
#        already ships the cure -- --attempt-log-dir (full stdout+stderr+hash into the receipt) and
#        --prior-attempt-dir (a retry refuses to spawn while the prior attempt is still alive) --
#        and both were simply not passed.
#   Root rule: proof mode and run mode are different protocols. This wrapper has one switch.
#
# Usage:
#   ./scripts/hgk-lane-run.sh run   PLAN|EXECUTE|VERIFY_SECURITY <nonce> <brief> [lane_timeout]
#   ./scripts/hgk-lane-run.sh probe PLAN|EXECUTE|VERIFY_SECURITY <nonce> <brief> <rank> <arm> [lane_timeout]
#
# run   = ladder allowed, detached (survives the parent), full attempt log, resumable.
# probe = single arm pinned, cheap, proves required==served for that arm; never used for work.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_BASE="${HGK_LANE_OUT:-$ROOT/../var/lane-runs}"
PARENT_BUDGET_S="${HGK_PARENT_BUDGET_S:-900}"

MODE="${1:?mode: run|probe}"; LANE="${2:?lane}"; NONCE="${3:?nonce}"; BRIEF="${4:?brief absolute path}"
case "$MODE" in
  run)   LT="${5:-260}"; MAXC=4; FORCE=(); REQ=() ;;
  probe) RANK="${5:?rank}"; ARM="${6:?provider/model}"; LT="${7:-260}"; MAXC=1
         FORCE=(--force-rank "$RANK"); REQ=(--require-arm "$ARM") ;;
  *) echo "mode must be run|probe" >&2; exit 2 ;;
esac

# D-B guard: a run that cannot finish inside the parent's budget is refused, not started.
if (( LT * MAXC > PARENT_BUDGET_S )); then
  echo "REFUSED: lane_timeout(${LT}s) x candidates(${MAXC}) = $((LT*MAXC))s > parent budget ${PARENT_BUDGET_S}s." >&2
  echo "          raise HGK_PARENT_BUDGET_S or lower lane_timeout. Do NOT start a child you will kill." >&2
  exit 3
fi

RUN_ID="$(date +%Y%m%dT%H%M%S)"
ATT="$OUT_BASE/$LANE/$NONCE-$RUN_ID"
mkdir -p "$ATT"
PRIOR=""; [ -d "$OUT_BASE/$LANE" ] && PRIOR="$(ls -d "$OUT_BASE/$LANE"/*/ 2>/dev/null | tail -1 || true)"

ARGS=(--lane "$LANE" --max-candidates "$MAXC" "${FORCE[@]}" "${REQ[@]}"
      --identity-source codex-rollout --codex-home "${HGK_CODEX_HOME:-C:/Users/user/.codex}" --allow-human-home-transport
      --sandbox workspace-write --allow-sandbox-escalation --guard-subject "${HGK_GUARD_SUBJECT:-C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2}"
      --timeout "$LT" --nonce "$NONCE"
      --attempt-log-dir "$ATT" --output-root "$OUT_BASE"
      --json-out "$ATT/receipt.json"
      --prompt "Read ${BRIEF} and do exactly what it says. Begin your reply with the token ${NONCE} on its own line.")
[ -n "$PRIOR" ] && [ "$PRIOR" != "$ATT/" ] && ARGS+=(--prior-attempt-dir "${PRIOR%/}")

echo "MODE=$MODE LANE=$LANE NONCE=$NONCE candidates=$MAXC timeout=$LT  ->  $ATT"
echo "receipt: $ATT/receipt.json"
# Detached: the lane's liveness must not be owned by this shell (D-B). setsid when available.
cd "$ROOT"
if command -v setsid >/dev/null 2>&1; then
  setsid "${PYTHON:-.venv/Scripts/python.exe}" scripts/hgk-lane-dispatch.py "${ARGS[@]}" \
    >"$ATT/dispatch.log" 2>&1 &
else
  nohup "${PYTHON:-.venv/Scripts/python.exe}" scripts/hgk-lane-dispatch.py "${ARGS[@]}" \
    >"$ATT/dispatch.log" 2>&1 &
fi
echo "detached pid $!  (read $ATT/receipt.json; do NOT poll-block the parent on it)"
