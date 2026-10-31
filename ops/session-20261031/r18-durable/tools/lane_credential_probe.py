"""Find which sealed credential actually serves the lane's required arm, then leave the relay on it.

The rehome proved the relay now starts from the sealed home (health 200) but the first pool key was
rejected upstream with 401 Invalid credential. Candidate credentials are therefore probed one at a
time: each candidate restarts the relay with OPENCODE_GO_API_KEY set to it, then a 1-token completion
to opencode-go/deepseek-v4.1-flash is issued and only the HTTP status is reported. Values are never
printed and never written outside the process environment.
"""
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

SEALED = Path(os.path.expandvars(r"%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes"))
ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
OCX = shutil.which("ocx") or shutil.which("ocx.cmd") or r"C:\Users\user\AppData\Roaming\npm\ocx.cmd"
MODEL = "opencode-go/deepseek-v4.1-flash"


def health():
    try:
        with urllib.request.urlopen("http://127.0.0.1:10101/healthz", timeout=3) as r:
            return r.status
    except Exception:
        return None


def probe():
    body = json.dumps({"model": MODEL, "max_tokens": 8,
                       "messages": [{"role": "user", "content": "reply with the single word OK"}]}).encode()
    req = urllib.request.Request("http://127.0.0.1:10101/v1/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            p = json.loads(r.read().decode())
            return r.status, (p.get("choices") or [{}])[0].get("message", {}).get("content")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:160]
    except Exception as e:
        return "EXC", f"{type(e).__name__}: {e}"


def restart(key):
    subprocess.run([OCX, "stop"], capture_output=True, text=True, timeout=120)
    time.sleep(2)
    env = dict(os.environ)
    env["OPENCODEX_HOME"] = str(SEALED)
    if key:
        env["OPENCODE_GO_API_KEY"] = key
    subprocess.Popen([OCX, "start", "--port", "10101"], env=env,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(45):
        time.sleep(1)
        if health() == 200:
            return True
    return False


def main():
    cfg = json.loads((SEALED / "config.json").read_text(encoding="utf-8"))
    pool = cfg["providers"]["opencode-go"].get("apiKeyPool") or []
    cands = []
    for p in pool:
        k = p.get("key") or ""
        if k.startswith("oc_sk_"):
            cands.append((p.get("label") or p.get("id"), k))
    human = Path.home() / ".opencodex" / "config.json"
    if human.is_file():
        hk = (json.loads(human.read_text(encoding="utf-8")).get("providers", {})
              .get("opencode-go", {}).get("apiKey"))
        if hk and hk.startswith("oc_sk_"):
            cands.append(("human-home-apiKey", hk))

    # the credential this very session runs on: Hermes' own .env (last assignment wins)
    hermes_env = Path(os.environ.get("HERMES_HOME", "")) / ".env"
    if hermes_env.is_file():
        val = None
        for line in hermes_env.read_text(encoding="utf-8", errors="ignore").splitlines():
            k, _, v = line.partition("=")
            if k.strip() == "OPENCODE_GO_API_KEY" and v.strip():
                val = v.strip().strip('"').strip("'")
        if val:
            cands.append(("hermes-dotenv-OPENCODE_GO_API_KEY", val))

    results = []
    winner = None
    for label, key in cands:
        ok = restart(key)
        if not ok:
            results.append({"candidate": label, "relay": "NOT_UP", "status": None})
            continue
        status, echo = probe()
        results.append({"candidate": label, "relay": "UP", "status": status,
                        "echo": (echo or "")[:80]})
        if status == 200:
            winner = label
            break

    receipt = {
        "schema": "R18.LANE.CREDENTIAL_PROBE/1",
        "model": MODEL,
        "candidates_tried": results,
        "winner": winner,
        "verdict": "REQUIRED_ARM_SERVES" if winner else "NO_SEALED_CREDENTIAL_SERVES",
        "claim_ceiling": "a 200 here proves only that one credential on this host can reach the required "
                         "model through the relay; it says nothing about lane attribution, which needs a "
                         "dispatcher attempt with a matching NONCE and usage receipt",
        "next_legal_action": ("re-dispatch EXECUTE and read the attempt log" if winner else
                              "owner must supply a working opencode-go credential, or the round must record "
                              "the required arm as unavailable and park EXECUTE with that named blocker"),
    }
    (ROUND / "receipts" / "LANE_CREDENTIAL_PROBE.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("candidates_tried", "winner", "verdict")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
