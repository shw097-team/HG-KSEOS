"""WP-09 disposition: what the independent challenge lane actually established, and what it did not.

This receipt exists to stop a tempting rounding-up. Three verdict-bearing runs exist, but:
  * every verdict-bearing run inspected the SUBJECT COPY AS IT WAS BEFORE the restore, i.e. a copy that
    this round's own test runs had mutated (FAR-R18-06);
  * the run that served for 191 s on the restored copy produced no VERDICT line;
  * pinning the lane to its required arm is refused with ERR_LANE_REQUIRED_ARM_ABSENT, so the only
    attributable serve is on an out-of-spec arm (opencode-go/deepseek-v4.1-flash).

Conclusion: no admissible independent verdict on the frozen candidate exists yet. WP-09 stays PARTIAL with a
named blocker, and the claim ceiling does not move.
"""
import glob
import json
import os
import re
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
MUTATED_MARKERS = ("5 fail", "78/83", "five of its own frozen", "five checksum mismatches",
                   "five of the 83", "5/83")


def verdicts():
    out = []
    for f in sorted(glob.glob(str(ROUND / "checker" / "attempts*" / "*stdout.txt")),
                    key=os.path.getmtime, reverse=True):
        txt = ""
        try:
            raw = Path(f).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        msgs = []
        for line in raw.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("type") == "item.completed":
                it = ev.get("item") or {}
                if it.get("type") == "agent_message" and it.get("text"):
                    msgs.append(it["text"])
        txt = "\n".join(msgs)
        m = re.search(r"VERDICT:\s*(PASS|HOLD|FAIL)", txt)
        if not m:
            continue
        out.append({"attempt_log": os.path.basename(f),
                    "verdict": m.group(1),
                    "object_mutated_by_this_round": any(k in txt for k in MUTATED_MARKERS),
                    "chars": len(txt)})
    return out


v = verdicts()
dispatch = {}
for name in ("VERIFY_R18.json", "VERIFY2_R18.json", "VERIFY3_R18.json", "VERIFY4_R18.json"):
    p = ROUND / "checker" / name
    if p.is_file():
        d = json.loads(p.read_text(encoding="utf-8"))
        dispatch[name] = {"ok": d.get("ok"), "code": d.get("code"),
                          "served_arm": d.get("used_transport_model"), "rank": d.get("used_rank"),
                          "seconds": d.get("used_seconds"), "nonce_ok": d.get("usage_receipt_ok")}

admissible = [x for x in v if not x["object_mutated_by_this_round"]]
receipt = {
    "schema": "R18.WP09.CHECKER_DISPOSITION/1",
    "wp": "WP-FHS-09",
    "verdict_bearing_attempts": v,
    "admissible_verdicts_on_frozen_copy": admissible,
    "dispatch_receipts": dispatch,
    "disposition": "PARTIAL",
    "blocker": ("no admissible independent verdict: every verdict-bearing run inspected the copy this round "
                "had mutated, the restored-copy run produced no VERDICT line, and the lane refuses "
                "--require-arm gpt-6.1-sol with ERR_LANE_REQUIRED_ARM_ABSENT so the only attributable serve "
                "is on an out-of-spec arm"),
    "next_legal_action": ("repair the VERIFY_SECURITY lane pool so the GPT 6.1 Sol arm is selectable, then "
                         "re-dispatch BRIEF_VERIFY2 with nonce == invocation id against the verified-pristine "
                         "copy"),
    "claim_ceiling": "author-local/static package evidence only; no independent acceptance, no native "
                     "qualification, no release",
    "what_the_verdicts_did_establish": ("the challenge skill did independently detect the copy corruption "
                                        "and the candidate's own non-native scope strings "
                                        "(README.md:13,15; COVERAGE_REPORT.md:45,47)"),
}
(ROUND / "receipts" / "WP09_CHECKER_DISPOSITION.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"verdict_attempts": v, "admissible": len(admissible), "dispatch": dispatch},
                 ensure_ascii=False, indent=1))
