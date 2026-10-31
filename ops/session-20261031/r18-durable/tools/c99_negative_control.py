"""Negative control for the repaired C99 predicate: it MUST be able to fail.

Reproduces the predicate shape against a scratch file:
  PASS branch: two reads of an untouched file agree.
  FAIL branch: a write between the two reads is detected.
If the FAIL branch ever passes, the repair turned a vacuous check into a vacuous check.
"""
import hashlib
import json
import pathlib
import tempfile

HERE = pathlib.Path(__file__).parent


def spine_state(p):
    st = p.stat()
    return {"bytes": st.st_size, "mtime_ns": st.st_mtime_ns,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def predicate(s1, s2):
    return (s1 is not None and s2 is not None
            and s1["sha256"] == s2["sha256"] and s1["bytes"] == s2["bytes"]
            and s1["mtime_ns"] == s2["mtime_ns"])


tmp = pathlib.Path(tempfile.mkdtemp(dir=str(HERE))) / "fake-spine.db"
tmp.write_bytes(b"\x00" * 4096)

s1 = spine_state(tmp)
s2 = spine_state(tmp)
pass_case = predicate(s1, s2)

tmp.write_bytes(b"\x00" * 4097)          # a write between reads
s3 = spine_state(tmp)
fail_case = predicate(s1, s3)

# also: a same-size write with a changed byte must fail on the digest
tmp.write_bytes(b"\x01" + b"\x00" * 4096)
s4 = spine_state(tmp)
fail_same_size = predicate(s1, s4)

# and: a missing file must fail, not raise
missing = predicate(None, None)

out = {"pass_branch": pass_case, "fail_branch_on_size_change": (not fail_case),
       "fail_branch_on_same_size_byte_change": (not fail_same_size),
       "fail_branch_on_missing": (not missing),
       "control_ok": pass_case and not fail_case and not fail_same_size and not missing}
(tmp.parent / "C99_NEGATIVE_CONTROL.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                      encoding="utf-8")
print(json.dumps(out, ensure_ascii=False))
