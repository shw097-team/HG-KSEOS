#!/usr/bin/env bash
# Codex cell, clean cwd, NATIVE path for -C (the first run failed with os error 2 because an MSYS /tmp path
# was handed to a native binary -- the same path-translation trap as everywhere else on this host).
set -u
MAN="C:/Projects/Agent_Workspace/PIPD/dist/fhs-wp11-portable-sp/export_manifest.json"
ARCH=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['archive']['sha256'])" "$MAN")
SCRATCH="$TMPDIR"
[ -d "$SCRATCH" ] || SCRATCH="$LOCALAPPDATA/Temp"
WORK=$(mktemp -d "$SCRATCH/fhs-cx-XXXXXX")
WINDIR=$(cygpath -w "$WORK")
TOKEN="WP11-CLEAN-$(python -c "import secrets;print(secrets.token_hex(5).upper())")"
CODEX=$(command -v codex)
echo "cwd(msys)=$WORK cwd(native)=$WINDIR token=$TOKEN codex=$CODEX"
echo "cwd entries before: $(ls -A "$WORK" | wc -l)"
CS="$HOME/.codex/skills/fhs-wp11-probe"
mkdir -p "$CS"
printf -- '---\nname: fhs-wp11-probe\ndescription: WP-11 host cell probe.\n---\n# probe\nBUNDLE_ARCHIVE_SHA256: %s\nWhen asked for the WP-11 host cell token, answer with exactly this one line and nothing else:\nTRIGGER_TOKEN: %s\n' "$ARCH" "$TOKEN" > "$CS/SKILL.md"
Q="What is the WP-11 host cell token? Answer with the single line only."
TRIG=$(timeout 200 "$CODEX" exec --skip-git-repo-check -C "$WINDIR" "$Q" 2>&1 | tail -5)
rm -rf "$CS"
NEG=$(timeout 200 "$CODEX" exec --skip-git-repo-check -C "$WINDIR" "$Q" 2>&1 | tail -5)
python - "$TOKEN" "$WINDIR" "$TRIG" "$NEG" <<'PY'
import json,sys
tok,w,trig,neg = sys.argv[1:5]
d={"host":"codex","cwd":w,"token":tok,
   "design":"token lives only in the host skill file; the cwd is empty, outside every repo, and given to the native binary as a Windows path",
   "trigger_has_token":tok in trig,"nontrigger_has_token":tok in neg,
   "trigger_tail":trig.strip().splitlines()[-1][:140] if trig.strip() else "",
   "nontrigger_tail":neg.strip().splitlines()[-1][:160] if neg.strip() else ""}
open("C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp11/clean_codex_cell.json","w",encoding="utf-8").write(json.dumps(d,ensure_ascii=False,indent=1))
print(json.dumps(d,ensure_ascii=False,indent=1))
PY
rm -rf "$WORK"
