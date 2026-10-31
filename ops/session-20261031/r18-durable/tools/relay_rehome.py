"""Bring the dedicated Codex-lane relay up on the SEALED home with its own credential.

Diagnosis this fixes: the relay that was running had been started from the human config
(C:\\Users\\user\\.opencodex\\config.json), which has no credential for the opencode-go models the
EXECUTE lane declares. Every required-arm attempt therefore failed fast with
  502 Bad Gateway: Provider unreachable: openai-chat requires a non-empty credential (authMode: key)
while a Codex-native arm (gpt-6-luna) served instead - i.e. the lane silently ran on the wrong arm.

This script:
  1. stops any relay on 10101,
  2. starts `ocx` with OPENCODEX_HOME = the sealed lane home and OPENCODE_GO_API_KEY taken from that
     home's own apiKeyPool (never printed, never written anywhere new),
  3. waits for healthz,
  4. proves the required arm answers by issuing one 1-token completion to
     opencode-go/deepseek-v4.1-flash and printing only its HTTP status and model echo.
"""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

SEALED = Path(os.path.expandvars(r"%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes"))
ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")


def health(timeout=3.0):
    try:
        with urllib.request.urlopen("http://127.0.0.1:10101/healthz", timeout=timeout) as r:
            return r.status
    except Exception:
        return None


def main():
    cfg = json.loads((SEALED / "config.json").read_text(encoding="utf-8"))
    pool = cfg["providers"]["opencode-go"].get("apiKeyPool") or []
    key = next((p["key"] for p in pool if p.get("key", "").startswith("oc_sk_")), None)
    if not key:
        raise SystemExit("ERR_NO_POOL_KEY: sealed home has no literal pool key")

    import shutil as _sh
    ocx = _sh.which("ocx") or _sh.which("ocx.cmd") or r"C:\Users\user\AppData\Roaming\npm\ocx.cmd"
    if not ocx:
        raise SystemExit("ERR_OCX_NOT_FOUND")
    before = health()
    subprocess.run([ocx, "stop"], capture_output=True, text=True, timeout=120, shell=False)
    time.sleep(2)
    env = dict(os.environ)
    env["OPENCODEX_HOME"] = str(SEALED)
    env["OPENCODE_GO_API_KEY"] = key
    proc = subprocess.Popen([ocx, "start", "--port", "10101"], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(40):
        time.sleep(1)
        if health() == 200:
            break
    after = health()

    body = json.dumps({"model": "opencode-go/deepseek-v4.1-flash", "max_tokens": 8,
                       "messages": [{"role": "user", "content": "reply with the single word OK"}]}).encode()
    req = urllib.request.Request("http://127.0.0.1:10101/v1/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    status, echo = None, None
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            status = r.status
            payload = json.loads(r.read().decode())
            echo = {"model": payload.get("model"), "choices": len(payload.get("choices") or [])}
    except urllib.error.HTTPError as e:
        status, echo = e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        status, echo = "EXC", {"error": f"{type(e).__name__}: {e}"}

    receipt = {
        "schema": "R18.LANE.RELAY_REHOME/1",
        "sealed_home": str(SEALED),
        "health_before": before, "health_after": after,
        "credential_source": "sealed apiKeyPool literal oc_sk_* entry (value never printed)",
        "pool_entries": len(pool),
        "required_arm_probe": {"model": "opencode-go/deepseek-v4.1-flash", "http_status": status,
                               "echo": echo},
        "verdict": "REQUIRED_ARM_SERVES" if status == 200 else "REQUIRED_ARM_STILL_BROKEN",
        "relay_pid": proc.pid,
        "reading": "the lane's required arm can only serve through the sealed home; the human home has no "
                   "opencode-go credential, which is what made every required-arm attempt fail fast and let "
                   "an out-of-spec arm serve in its place",
    }
    (ROUND / "receipts" / "RELAY_REHOME.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1),
                                                          encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("health_before", "health_after", "required_arm_probe",
                                              "verdict", "pool_entries")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
