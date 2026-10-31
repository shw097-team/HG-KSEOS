"""Extract each lane's actual answer text from the dispatcher attempt logs (jsonl event stream).

The dispatch receipt records attribution (lane, rank, arm, nonce, usage) but not the prose; the prose
lives in the attempt stdout as `{"type":"item.completed","item":{"type":"agent_message","text":...}}`.
This pulls the last agent_message per attempt, so the round can quote what the lane actually said.
"""
import glob
import json
import os
import re

ROUND = r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029"
out = {}
for path in sorted(glob.glob(os.path.join(ROUND, "**", "attempt-*-stdout.txt"), recursive=True),
                   key=os.path.getmtime, reverse=True)[:8]:
    try:
        raw = open(path, encoding="utf-8", errors="ignore").read()
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
            item = ev.get("item") or {}
            if item.get("type") == "agent_message" and item.get("text"):
                msgs.append(item["text"])
    if not msgs:
        continue
    text = "\n".join(msgs)
    if "NONCE" not in text:
        continue
    lane = "PLAN" if "R18LANEPLAN" in text or "SPINV-COMMANDER" in text else (
        "VERIFY" if "SPINV-CHALLENGE" in text else "EXECUTE")
    out.setdefault(lane, {"path": path, "text": text})

for lane, d in out.items():
    p = os.path.join(ROUND, "lane" if lane != "VERIFY" else "checker", f"{lane}_ANSWER.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(d["text"])
    print("==", lane, "->", os.path.basename(p), len(d["text"]), "chars")
    print(d["text"][:700].replace("\r", ""))
    print()
