#!/usr/bin/env bash
# One WP-11 host cell: a named host must reach a named Service Profile's content and report its digest.
#
# Design, and why each part is there:
#   * the cwd is a fresh directory OUTSIDE every repo, holding only the unpacked SP -- so the host cannot answer by
#     reading a workspace file it already had;
#   * the probe lives on the HOST's own surface (~/.codex/skills, ~/.claude/agents), never in the cwd;
#   * the answer must contain the SP archive digest AND a fresh random token, so "it answered something" is not
#     mistaken for "it reached this SP";
#   * the negative is the same question after the probe is removed: it must NOT produce the token.
#
# Usage: sp_cell.sh <codex|claude> <LITE|STANDARD>
set -u
HOST="$1"; SP="$2"
DIST="C:/Projects/Agent_Workspace/PIPD/dist/prof-$SP"
DISTU=$(cygpath -u "$DIST")   # MSYS tar mishandles a native drive-colon path
MAN="$DIST/export_manifest.json"
ARCH=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['archive']['sha256'][:12])" "$MAN")
SCRATCH="${TMPDIR:-$LOCALAPPDATA/Temp}"
WORK=$(mktemp -d "$SCRATCH/fhs-sp-XXXXXX")
WINDIR=$(cygpath -w "$WORK")
TOKEN="SP-BADGE-${SP}-$(python -c "import secrets;print(secrets.token_hex(4).upper())")"

# unpack the SP into the clean cwd
tar -xzf "$DISTU/prof-$SP.tar.gz" -C "$WORK" || { echo "EXTRACT_FAILED"; rm -rf "$WORK"; exit 3; }

Q="Answer two questions in two lines. (1) In export_manifest.json in this working directory, what are the first 12 characters of the archive sha256? (2) What is the SP-BADGE value for this environment?"

if [ "$HOST" = "codex" ]; then
  CODEX=$(command -v codex)
  CS="$HOME/.codex/skills/fhs-sp-probe"
  mkdir -p "$CS"
  printf -- '---\nname: fhs-sp-probe\ndescription: WP-11 SP probe.\n---\n# probe\nSP=%s\nARCHIVE_SHA256=%s\nSP-BADGE: %s\n' "$SP" "$ARCH" "$TOKEN" > "$CS/SKILL.md"
  TRIG=$(timeout 240 "$CODEX" exec --skip-git-repo-check -C "$WINDIR" "$Q" 2>&1 | tail -6)
  rm -rf "$CS"
  NEG=$(timeout 240 "$CODEX" exec --skip-git-repo-check -C "$WINDIR" "$Q" 2>&1 | tail -6)
elif [ "$HOST" = "claude" ]; then
  CA="$HOME/.claude/agents/fhs-sp-probe.md"
  printf -- '---\nname: fhs-sp-probe\ndescription: WP-11 SP probe.\n---\nSP=%s\nARCHIVE_SHA256=%s\nSP-BADGE: %s\n' "$SP" "$ARCH" "$TOKEN" > "$CA"
  export ANTHROPIC_BASE_URL=http://127.0.0.1:10101
  export ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-local-relay}"   # the loopback relay is the transport; any bearer satisfies it
  TRIG=$(cd "$WORK" && timeout 240 claude -p "$Q" --agent fhs-sp-probe --model gpt-5.6-sol 2>&1 | tail -6)
  rm -f "$CA"
  NEG=$(cd "$WORK" && timeout 240 claude -p "$Q" --model gpt-5.6-sol 2>&1 | tail -6)   # no --agent: the probe is gone
else
  echo "unknown host $HOST"; rm -rf "$WORK"; exit 2
fi

python - "$HOST" "$SP" "$ARCH" "$TOKEN" "$WINDIR" "$TRIG" "$NEG" <<'PY'
import json, sys, pathlib
host, sp, arch, tok, w, trig, neg = sys.argv[1:8]
d = {"host": host, "sp": sp, "archive_prefix": arch, "token": tok, "cwd": w,
     "trigger_has_digest": arch in trig, "trigger_has_token": tok in trig,
     "nontrigger_has_token": tok in neg,
     "verdict": ("PASS" if (arch in trig and tok in trig and tok not in neg) else "FAIL"),
     "trigger_tail": (trig.strip().splitlines()[-1][:150] if trig.strip() else ""),
     "nontrigger_tail": (neg.strip().splitlines()[-1][:150] if neg.strip() else "")}
p = pathlib.Path(r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp11") / f"SP_CELL_{host}_{sp}.json"
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
print(json.dumps(d, ensure_ascii=False, indent=1))
PY
rm -rf "$WORK"
