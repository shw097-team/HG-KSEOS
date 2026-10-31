#!/usr/bin/env bash
# Clean-cwd host cell test: the token must live only in the host's own skill/agent file,
# never in the working tree, or "the model said the token" proves nothing about loading.
set -u
MAN="C:/Projects/Agent_Workspace/PIPD/dist/fhs-wp11-portable-sp/export_manifest.json"
ARCH=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['archive']['sha256'])" "$MAN")
WORK=$(mktemp -d "${TMPDIR:-/tmp}/fhs-cell-XXXXXX")
TOKEN="WP11-CLEAN-$(python -c "import secrets;print(secrets.token_hex(5).upper())")"
OUT="C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp11/clean_cell_runs.json"
CODEX=$(command -v codex); CLAUDE=$(command -v claude)
echo "cwd=$WORK token=$TOKEN codex=$CODEX claude=$CLAUDE"
echo "cwd contents before: $(ls -A "$WORK" | wc -l) entries"

emit_skill() {
  printf -- '---\nname: fhs-wp11-probe\ndescription: WP-11 host cell probe.\n---\n# probe\nBUNDLE_ARCHIVE_SHA256: %s\nWhen asked for the WP-11 host cell token, answer with exactly this one line and nothing else:\nTRIGGER_TOKEN: %s\n' "$ARCH" "$TOKEN"
}
emit_agent() {
  printf -- '---\nname: "fhs-wp11-probe"\ndescription: "WP-11 Claude Code host cell probe."\nmodel: "gpt-5.6-sol"\n---\nBUNDLE_ARCHIVE_SHA256: %s\nWhen asked for the WP-11 host cell token, answer with exactly this one line and nothing else:\nTRIGGER_TOKEN: %s\n' "$ARCH" "$TOKEN"
}
Q="What is the WP-11 host cell token? Answer with the single line only."

# ---- codex ----
CS="$HOME/.codex/skills/fhs-wp11-probe"
mkdir -p "$CS"; emit_skill > "$CS/SKILL.md"
cd "$WORK" || exit 1
TRIG_CX=$(timeout 200 "$CODEX" exec --skip-git-repo-check -C "$WORK" "$Q" 2>&1 | tail -4)
rm -rf "$CS"
NEG_CX=$(timeout 200 "$CODEX" exec --skip-git-repo-check -C "$WORK" "$Q" 2>&1 | tail -4)

# ---- claude ----
CA="$HOME/.claude/agents/fhs-wp11-probe.md"
emit_agent > "$CA"
export ANTHROPIC_BASE_URL=http://127.0.0.1:10101 ANTHROPIC_AUTH_TOKEN=local-relay
TRIG_CL=$(timeout 200 "$CLAUDE" -p "$Q" --agent fhs-wp11-probe 2>&1 | tail -3)
rm -f "$CA"
NEG_CL=$(timeout 200 "$CLAUDE" -p "$Q" --model gpt-5.6-sol 2>&1 | tail -3)

python - "$TOKEN" "$WORK" "$OUT" "$TRIG_CX" "$NEG_CX" "$TRIG_CL" "$NEG_CL" <<'PY'
import json,sys
tok,work,out,tcx,ncx,tcl,ncl = sys.argv[1:8]
d={"cwd":work,"token":tok,"design":"token exists only in the host skill/agent file; cwd is empty and outside every repo",
   "codex":{"trigger_has_token":tok in tcx,"nontrigger_has_token":tok in ncx,
            "trigger_tail":tcx.strip().splitlines()[-1][:120] if tcx.strip() else "",
            "nontrigger_tail":ncx.strip().splitlines()[-1][:140] if ncx.strip() else ""},
   "claude_code":{"trigger_has_token":tok in tcl,"nontrigger_has_token":tok in ncl,
            "trigger_tail":tcl.strip().splitlines()[-1][:120] if tcl.strip() else "",
            "nontrigger_tail":ncl.strip().splitlines()[-1][:140] if ncl.strip() else ""}}
open(out,"w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False,indent=1))
print(json.dumps(d,ensure_ascii=False,indent=1))
PY
rm -rf "$WORK"
