"""R18: refresh the Codex toolchain pin after an in-place CLI upgrade, then re-designate.

Documented repair (skill hgk-codex-lane-recipe pitfall 20): the Codex CLI auto-updated, so the
declared codex_executable no longer exists and EVERY lane dispatch refuses before spawn with
ERR_LANE_PIN_IDENTITY_INVALID / ERR_LANE_TOOLCHAIN_BINARY_MISSING.

This script changes exactly three values plus one appended history entry, then re-binds
config/active-policy.json to the new declaration bytes. Preimages are kept in
var/R18-FHS-SKELETON-SPINE-20261029/preimage/; rollback is a byte restore of the two files.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HF = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
DECL = HF / "config" / "hermes-codex-lane.json"
POLICY = HF / "config" / "active-policy.json"
PRE = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\preimage")
LIVE_CANDIDATES = sorted((Path.home() / "AppData" / "Local" / "OpenAI" / "Codex" / "bin").glob("*/codex.exe"))
SIDECAR_NAMES = ["codex.exe", "codex-code-mode-host.exe", "codex-command-runner.exe",
                 "codex-windows-sandbox-setup.exe"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def newest():
    return max(LIVE_CANDIDATES, key=lambda p: p.stat().st_mtime)


live = newest()
version = subprocess.run([str(live), "--version"], capture_output=True, text=True,
                         timeout=60).stdout.strip().replace("codex-cli ", "")
live_sha = sha(live)
sidecars = {n: (live.parent / n).is_file() for n in SIDECAR_NAMES}

text = DECL.read_text(encoding="utf-8")
doc = json.loads(text)
old = {"path": doc["codex_executable"], "version": doc["codex_version"], "sha256": doc["codex_sha256"]}

# --- surgical byte edits: only the three pin values, so every other byte is preserved verbatim
lines = text.splitlines(keepends=True)
out = []
changed = 0
for line in lines:
    if line.lstrip().startswith('"codex_executable"'):
        new_path = str(live).replace("\\", "\\\\")
        out.append('  "codex_executable": "%s",\n' % new_path)
        changed += 1
    elif line.lstrip().startswith('"codex_version"'):
        out.append('  "codex_version": "%s",\n' % version)
        changed += 1
    elif line.lstrip().startswith('"codex_sha256"'):
        out.append('  "codex_sha256": "%s",\n' % live_sha)
        changed += 1
    else:
        out.append(line)
new_text = "".join(out)

entry = {
    "at_utc": datetime.now(timezone.utc).isoformat(),
    "round": "R18-FHS-SKELETON-SPINE-20261029",
    "reason": "codex CLI auto-updated in place again; the declared binary no longer existed, so every "
              "lane dispatch refused before spawn with ERR_LANE_PIN_IDENTITY_INVALID / "
              "ERR_LANE_TOOLCHAIN_BINARY_MISSING",
    "from": old,
    "to": {"path": str(live), "version": version, "sha256": live_sha},
    "sidecars_present": sidecars,
    "authorization": "owner blanket repair authorization for this round; agent-executed, not signed",
}
marker = '  "pin_refresh_history": [\n'
assert marker in new_text, "pin_refresh_history anchor not found"
new_text = new_text.replace(marker, marker + "    " + json.dumps(entry, ensure_ascii=False) + ",\n", 1)

DECL.write_bytes(new_text.encode("utf-8"))
new_sha = sha(DECL)
new_bytes = DECL.stat().st_size

# --- re-designate the active policy at the new declaration bytes
pol = json.loads(POLICY.read_text(encoding="utf-8"))
old_pol = {"policy_digest": pol["policy_digest"], "policy_bytes": pol["policy_bytes"]}
order_text = (
    "Owner blanket repair authorization for round R18-FHS-SKELETON-SPINE-20261029 (continuation of the "
    "OWNER B1 continuation authorization of 2026-10-28). Re-designated ONLY because the declared Codex "
    "binary no longer existed on disk: every lane dispatch refused before spawn with "
    "ERR_LANE_PIN_IDENTITY_INVALID / ERR_LANE_TOOLCHAIN_BINARY_MISSING. The policy CONTENT is unchanged "
    "except the three toolchain-pin fields (codex_executable / codex_version / codex_sha256) and the "
    "appended pin_refresh_history entry.")
pol["policy_digest"] = new_sha
pol["policy_bytes"] = new_bytes
pol["declared_by"] = ("R18-FHS-SKELETON-SPINE-20261029 re-designation after a measured toolchain-pin "
                      "refresh (codex %s -> %s); agent executed under the owner blanket repair "
                      "authorization, not signed" % (old["version"], version))
pol["declared_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
pol["order_text"] = order_text
pol["order_digest"] = hashlib.sha256(order_text.encode("utf-8")).hexdigest()
pol["claim_ceiling"] = ("designation only, re-pointed at the refreshed bytes. It signs nothing, changes no "
                        "lane route, and does not prove any native consumption chain. Rollback = restore "
                        "preimage/{hermes-codex-lane.json.bak,active-policy.json.bak} byte for byte.")
pol["supersedes"] = {"policy_digest": old_pol["policy_digest"], "policy_bytes": old_pol["policy_bytes"],
                     "preimage": "var/R18-FHS-SKELETON-SPINE-20261029/preimage/"}
POLICY.write_text(json.dumps(pol, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

receipt = {
    "schema": "R18.HGK.TOOLCHAIN_PIN_REFRESH/1",
    "at_utc": datetime.now(timezone.utc).isoformat(),
    "fields_changed": changed,
    "from": old,
    "to": {"path": str(live), "version": version, "sha256": live_sha},
    "sidecars_present": sidecars,
    "declaration_sha256_after": new_sha,
    "declaration_bytes_after": new_bytes,
    "active_policy_before": old_pol,
    "active_policy_after": {"policy_digest": new_sha, "policy_bytes": new_bytes},
    "preimage_dir": str(PRE),
}
(Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\receipts") /
 "TOOLCHAIN_PIN_REFRESH.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"changed": changed, "to_version": version, "to_sha": live_sha[:16],
                  "decl_sha": new_sha[:16], "decl_bytes": new_bytes,
                  "sidecars": sidecars}, ensure_ascii=False))
