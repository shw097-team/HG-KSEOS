"""The single routing point for every owner passphrase entry in HGK/PIPD.

Sources, in this order — the tkinter window is the PRIMARY path for a human (FAR-16):

  1. env var            (scripted / CI; never argv, never logged)
  2. console            (only when a real TTY exists AND the caller wants it — an unattended process
                         must never block on getpass, so window-open forces the GUI)
  3. tkinter modal      (masked Entry, topmost, no subprocess: the secret never leaves this process)
  4. OWNER_PROMPT.ps1   (fallback only: HGK_OWNER_UI=ps, or when Tk cannot be imported)

Everything that needs a secret — signing-window open, --repass, --rotate, --seal — goes through
`get_secret()`, so there is exactly one implementation and one audit point (FAR-15 / FAR-16).
"""
from __future__ import annotations

import getpass
import json
import os
import pathlib
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = pathlib.Path(__file__).resolve().parent
UI = HERE / "OWNER_PROMPT.ps1"

# ui_impl is audited by selfcheck C113; keep this tuple authoritative.
UI_IMPLS = ("env", "tty", "tkinter", "powershell")


# --------------------------------------------------------------------------- chime (FAR-17)
def _chime(kind: str) -> None:
    """A short, information-free cue: nothing about the secret or the outcome is encoded in it.

    Measured on this host: MessageBeep 0.00s, PlaySound async 0.07s, Beep 0.12s. winsound is stdlib on
    Windows, needs no process and cannot block the signing path. `HGK_OWNER_CHIME=0` silences it.
    """
    if os.environ.get("HGK_OWNER_CHIME") == "0":
        return
    try:
        import winsound
    except Exception:
        return
    try:
        if kind == "prompt":
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif kind == "refused":
            winsound.MessageBeep(winsound.MB_ICONHAND)
        elif kind in ("closed", "granted"):
            winsound.MessageBeep(winsound.MB_OK)
    except Exception:
        pass


# --------------------------------------------------------------------------- tkinter (primary)
def _tk_secret(purpose: str, *, min_len: int = 12, allow_generate: bool = False,
               verify=None, autofill: str | None = None) -> str:
    """A native modal window. The string goes back to THIS process only; never logged or serialised.

    `autofill` exists for automated widget tests (FAR-16 step 5): it types a throwaway value and
    submits, so the widget wiring is provable without a human and without any real credential.
    """
    import tkinter as tk

    verify = verify or (lambda s: None)
    out: dict[str, str | None] = {"value": None}
    root = tk.Tk()
    root.title("HG-KSEOS owner key — passphrase")
    root.geometry("470x240")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    tk.Label(root, text=purpose, font=("Segoe UI", 11, "bold"), wraplength=440).pack(pady=(14, 2))
    tk.Label(root, text=("Masked input. It is never stored, printed or sent anywhere.\n"
                         "The agent cannot see it."),
             justify="center", fg="#444").pack(pady=(0, 8))
    e1 = tk.Entry(root, show="\u2022", width=40)
    e1.pack(pady=4)
    e2 = None
    if allow_generate and os.environ.get("HGK_OWNER_CONFIRM") == "1":
        tk.Label(root, text="confirm", fg="#666").pack()
        e2 = tk.Entry(root, show="\u2022", width=40)
        e2.pack(pady=4)
    err = tk.Label(root, text="", fg="#b00020", wraplength=440)
    err.pack()
    e1.focus_set()
    _chime("prompt")

    def submit(_evt=None):
        v = e1.get()
        if e2 is not None and v != e2.get():
            err.config(text="passphrases differ")
            return
        if len(v) < min_len:
            err.config(text=f"minimum {min_len} characters (got {len(v)})")
            return
        try:
            verify(v)
        except Exception as exc:                  # wrong passphrase keeps the window open
            err.config(text=str(exc)[:80])
            _chime("refused")
            e1.delete(0, "end")
            return
        out["value"] = v
        _chime("granted")
        root.destroy()

    def cancel(_evt=None):
        root.destroy()

    box = tk.Frame(root)
    box.pack(pady=8)
    tk.Button(box, text="Sign", width=16, command=submit).pack(side="left", padx=6)
    tk.Button(box, text="Cancel", width=10, command=cancel).pack(side="left", padx=6)
    root.bind("<Return>", submit)
    root.bind("<Escape>", cancel)

    if autofill is not None:
        def _auto():
            e1.insert(0, autofill)
            if e2 is not None:
                e2.insert(0, autofill)
            submit()
        root.after(250, _auto)

    root.mainloop()
    if out["value"] is None:
        raise PermissionError("REFUSED_UI_PROMPT_CANCELLED")
    return out["value"]


# --------------------------------------------------------------------------- PowerShell (fallback)
class _Intake(threading.Thread):
    def __init__(self, token: str, verify):
        super().__init__(daemon=True)
        self.token, self.verify = token, verify
        self.port: int | None = None
        self.result: str | None = None
        self._srv: HTTPServer | None = None
        self._ready = threading.Event()

    def run(self) -> None:
        outer = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):  # silence
                return

            def _send(self, code: int, obj: dict) -> None:
                body = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):  # noqa: N802
                if self.path != "/submit":
                    return self._send(404, {"error": "NOT_FOUND"})
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                    data = json.loads(self.rfile.read(n) or b"{}")
                except Exception:
                    return self._send(400, {"error": "BAD_JSON"})
                if data.get("token") != outer.token:
                    return self._send(403, {"error": "REFUSED_BAD_TOKEN"})
                secret = data.get("passphrase") or ""
                if not secret:
                    return self._send(400, {"error": "EMPTY_PASSPHRASE"})
                try:
                    outer.verify(secret)
                except Exception as e:
                    return self._send(400, {"error": f"REFUSED_{type(e).__name__}: {str(e)[:80]}"})
                outer.result = secret
                self._send(200, {"ok": True})

        self._srv = HTTPServer(("127.0.0.1", 0), H)
        self.port = self._srv.server_address[1]
        self._ready.set()
        self._srv.timeout = 1
        while self.result is None:
            try:
                self._srv.handle_request()
            except Exception:
                continue

    def wait_port(self, t: float = 10) -> int:
        self._ready.wait(t)
        assert self.port
        return self.port


def _ps_secret(purpose: str, *, min_len: int, allow_generate: bool, verify, timeout: float) -> str:
    if not UI.is_file():
        raise PermissionError("REFUSED_NO_UI_SCRIPT")
    token = os.urandom(16).hex()
    intake = _Intake(token, verify)
    intake.start()
    port = intake.wait_port()
    cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(UI),
           "-Purpose", purpose, "-Port", str(port), "-Token", token, "-MinLen", str(min_len),
           "-Generate", "1" if allow_generate else "0"]
    # a real console window (not detached) so the owner can see and type into it
    _chime("prompt")
    subprocess.Popen(cmd, creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0x00000010),
                     close_fds=True)
    deadline = time.time() + timeout
    while time.time() < deadline and intake.result is None:
        time.sleep(0.25)
    if intake.result is None:
        raise TimeoutError("REFUSED_UI_PROMPT_TIMEOUT")
    return intake.result


# --------------------------------------------------------------------------- router
def get_secret(purpose: str, *, min_len: int = 12, allow_generate: bool = False,
               env_var: str | None = None, timeout: float = 300, verify=None,
               prefer_ui: bool = False, autofill: str | None = None) -> tuple[str, str]:
    """Return (secret, ui_impl) with ui_impl ∈ UI_IMPLS. The secret is never logged."""
    if env_var and os.environ.get(env_var):
        return os.environ[env_var], "env"

    verify = verify or (lambda s: None)
    want = (os.environ.get("HGK_OWNER_UI") or "").strip().lower()      # "", "tk", "ps"

    # prefer_ui: a terminal that merely *claims* to be a TTY (agent PTYs, background shells) is not
    # a console the owner can see — measured: a window open hung silently on a pipe-fed getpass.
    if (not prefer_ui and want != "ps" and sys.stdin and sys.stdin.isatty()
            and sys.stdout and sys.stdout.isatty()):
        for _ in range(3):
            s = getpass.getpass(f"{purpose} (>= {min_len} chars, never stored): ")
            if len(s) < min_len:
                print(f"  too short ({len(s)}), try again", file=sys.stderr)
                continue
            try:
                verify(s)
            except Exception as e:
                print(f"  rejected: {e}", file=sys.stderr)
                continue
            return s, "tty"
        raise PermissionError("REFUSED_PASSPHRASE_REJECTED")

    if os.environ.get("HGK_NO_UI"):
        raise PermissionError("REFUSED_UI_DISABLED")     # headless / test: never pop a window

    if want != "ps":
        try:
            return _tk_secret(purpose, min_len=min_len, allow_generate=allow_generate,
                              verify=verify, autofill=autofill), "tkinter"
        except ImportError as e:
            if want == "tk":
                raise PermissionError(f"REFUSED_TK_UNAVAILABLE: {e}")
            # otherwise fall through to the PowerShell fallback
    return _ps_secret(purpose, min_len=min_len, allow_generate=allow_generate, verify=verify,
                      timeout=timeout), "powershell"
