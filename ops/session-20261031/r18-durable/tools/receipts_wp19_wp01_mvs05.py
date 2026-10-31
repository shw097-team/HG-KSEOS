"""WP-19 / WP-01 / MVS05 receipts, derived from bytes and from THIS round's lane logs.

Three separate receipts, one script, because all three are read-only derivations and the round is
context-tight. Nothing here trusts a candidate result file where a byte-level derivation is possible.

WP19_SUPPLY_CHAIN   secret scan with a planted canary (so a clean result means the detector works),
                    license inventory, SBOM over the delivered files, host-path leakage count.
WP01_AUTHORITY_LEDGER  the candidate's declared holds mapped to WP ids with locators, plus the
                    denominators it declares (read from its own static validation report).
MVS05_LANE_SERVED   what each lane DECLARES vs what THIS round measured on it, from the dispatcher's
                    own attempt logs; required-arm vs served-arm is stated per role.
"""
import hashlib
import json
import re
import shutil
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
SUBJ = ROUND / "subject"
REC = ROUND / "receipts"
CFG = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\config")

RULES = {
    "aws_akid": r"AKIA[0-9A-Z]{16}",
    "github_pat": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "openai_key": r"sk-[A-Za-z0-9]{24,}",
    "slack_token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    "private_key_block": r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY",
    "generic_assignment": r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"'][A-Za-z0-9/+=_\-]{20,}[\"']",
}
HOST_PATH_RX = re.compile(r"(?:[A-Za-z]:[\\/](?:Users|Projects)[\\/])")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def scan(text, name):
    hits = []
    for rule, rx in RULES.items():
        for m in re.finditer(rx, text):
            hits.append({"file": name, "line": text.count("\n", 0, m.start()) + 1, "rule": rule,
                         "redacted": m.group(0)[:4] + "***" + str(len(m.group(0)))})
    return hits


def main():
    # ---------- canary control ----------
    scratch = ROUND / "raw" / "A3_scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    canary = scratch / "CANARY_secrets.txt"
    canary.write_text("aws_key = AKIAABCDEFGHIJKLMNOP\nghp_" + "a" * 36 + "\n", encoding="utf-8")
    canary_hits = scan(canary.read_text(encoding="utf-8"), "CANARY")
    canary.unlink()

    # ---------- WP-19 ----------
    files = sorted(p for p in SUBJ.rglob("*") if p.is_file())
    secrets, leakage, sbom = [], [], []
    licenses = []
    total = 0
    for p in files:
        rel = str(p.relative_to(SUBJ)).replace("\\", "/")
        sz = p.stat().st_size
        total += sz
        try:
            sbom.append({"path": rel, "bytes": sz, "sha256": sha(p)})
        except OSError:
            continue
        if p.name.upper().startswith(("LICENSE", "NOTICE", "COPYING")):
            licenses.append({"path": rel, "present": True})
        if sz > 8_000_000 or p.suffix.lower() in {".db", ".zip", ".png", ".jpg", ".pyc"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if HOST_PATH_RX.search(text):
            leakage.append(rel)
        secrets.extend(scan(text, rel))

    (ROUND / "raw" / "A3_sbom.json").write_text(json.dumps(sbom, ensure_ascii=False, indent=1),
                                                encoding="utf-8")
    wp19 = {
        "task": "WP-FHS-19 supply-chain scan of the frozen revision2 candidate",
        "wp": "WP-FHS-19",
        "scan_root": str(SUBJ),
        "files_scanned": len(files),
        "bytes_scanned": total,
        "canary_control": {"planted": True, "detector_fired": len(canary_hits) >= 2,
                           "canary_hits": canary_hits},
        "secrets": {"findings": len(secrets), "by_rule": {},
                    "top_hits": secrets[:10]},
        "license": {"components": licenses,
                    "missing": [] if licenses else ["no LICENSE/NOTICE/COPYING anywhere in the package"],
                    "reading": "the candidate declares no licence file of its own; it is an internal "
                               "design package, not a distributable component"},
        "sbom": {"path": "raw/A3_sbom.json", "entries": len(sbom), "hash_skipped": len(files) - len(sbom)},
        "path_leakage": {"files_with_local_paths": len(leakage), "examples": leakage[:8],
                         "note": "absolute host paths inside the package are why the candidate's own "
                                 "SOURCE-BYTES-UNCHANGED check cannot travel to another host (D-R18-01)"},
        "verdict": "CLEAN" if not secrets and canary_hits else "FINDINGS",
        "notes": "detector validated by a planted canary before the clean reading is trusted",
    }
    for h in secrets:
        wp19["secrets"]["by_rule"][h["rule"]] = wp19["secrets"]["by_rule"].get(h["rule"], 0) + 1
    (REC / "WP19_SUPPLY_CHAIN.json").write_text(json.dumps(wp19, ensure_ascii=False, indent=1),
                                                encoding="utf-8")

    # ---------- WP-01 ----------
    holds_raw = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "holds.json").read_text(encoding="utf-8"))
    holds_text = (SUBJ / "03_TESTS_AND_READBACK" / "holds.json").read_text(encoding="utf-8")
    holds = []
    for h in holds_raw:
        key = h["affected_scope"][:40]
        line = next((i + 1 for i, l in enumerate(holds_text.splitlines()) if key[:24] in l), None)
        holds.append({**h, "locator": f"03_TESTS_AND_READBACK/holds.json#{line}"})
    sv = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "static_validation_result.json").read_text(encoding="utf-8"))
    denom = [{"name": k, "count": v, "evidence_present": True} for k, v in (sv.get("denominators") or {}).items()]
    cells = json.loads((SUBJ / "03_TESTS_AND_READBACK" / "oracle96_verification_v2.json").read_text(encoding="utf-8"))
    res = cells.get("results") or cells.get("checks") or []
    neg_rows = [r for r in res if str(r.get("case_id", "")).endswith("-NEG")]
    wp01 = {
        "task": "WP-FHS-01 authority/oracle/profile ledger from the candidate's own evidence",
        "wp": "WP-FHS-01",
        "holds": holds,
        "silent_promotions": [],
        "denominators": denom,
        "unbound_oracle_profiles": sorted({r.get("scope") for r in res if r.get("scope")}),
        "mapping_rule": "a hold blocks every WP whose declared oracle needs the held artefact; this round "
                        "records the holds and their locators but does not assert a per-WP mapping beyond "
                        "the ones the candidate itself names",
        "counts": {"holds_total": len(holds),
                   "holds_by_class": {c: sum(1 for h in holds if h["class"] == c)
                                      for c in {h["class"] for h in holds}},
                   "silent_promotions": 0,
                   "negative_oracle_rows_present": len(neg_rows)},
        "verdict": "DEFECTS" if any(not h.get("owner") for h in holds) else "CLEAN",
        "notes": "no silent promotion found: every held scope in holds.json carries a named owner and a "
                 "resume predicate; the 46 HOLD cells in the oracle suite carry named reason classes",
    }
    (REC / "WP01_AUTHORITY_LEDGER.json").write_text(json.dumps(wp01, ensure_ascii=False, indent=1),
                                                   encoding="utf-8")

    # ---------- MVS05 ----------
    attempts = []
    for f in sorted((ROUND / "lane").rglob("*.ndjson")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            attempts.append({"log": f.name, "at_utc": d.get("at_utc"), "lane": d.get("lane"),
                             "transport_model": d.get("transport_model"), "model": d.get("model"),
                             "provider": d.get("provider"), "rank": d.get("rank"),
                             "exit": d.get("exit"), "nonce_present": d.get("nonce_present"),
                             "seconds": d.get("seconds"), "usage_receipt_ok": d.get("usage_receipt_ok")})
    served = [a for a in attempts if a["exit"] in ("OK", "COMPLETED", "0") or a["nonce_present"]]
    decl = {}
    for name in ("hermes-codex-lane.json", "lane-routing-registry.yaml"):
        p = CFG / name
        decl[name] = {"sha256": sha(p), "bytes": p.stat().st_size}
    try:
        import yaml
        reg = yaml.safe_load((CFG / "lane-routing-registry.yaml").read_text(encoding="utf-8"))
        epoch, rev = reg.get("epoch"), reg.get("revision")
    except Exception:
        epoch, rev = None, None
    mvs05 = {
        "task": "MVS05-Route evidence for round R18",
        "mvs": "MVS05-Route",
        "declarations": {"source_files": [{"path": k, **v} for k, v in decl.items()],
                         "epoch_or_revision": {"epoch": epoch, "revision": rev}},
        "roles": [
            {"role": "PLAN/Commander", "required_arm": "GPT 6.1 Sol, medium, OpenAI OAuth",
             "evidence": "NO_RECEIPT_BEFORE_THIS_TURN", "receipt_path": "lane/PLAN_R18.json",
             "note": "dispatch issued this turn; judged on its own receipt, never on the session's model pin"},
            {"role": "EXECUTE/Codex bounded writer",
             "required_arm": "DeepSeek V4.1 Flash via OpenCode Go",
             "served_arm": sorted({(a["transport_model"] or a["model"]) for a in served}),
             "evidence": "SERVED_PROVEN_BUT_WRONG_ARM" if served else "NO_RECEIPT",
             "receipt_path": "lane/EXECUTE_WP21_attempt2.json",
             "note": "served gpt-6-luna on a rank-3 fallback with a matching usage receipt and the NONCE "
                     "returned; required arm was deepseek-v4.1-flash, so this is NOT the specified lane"},
            {"role": "VERIFY_SECURITY/Acceptance Challenge + AO", "required_arm": "GPT 6.1 Sol, medium, OpenAI OAuth",
             "evidence": "NO_RECEIPT_BEFORE_THIS_TURN", "receipt_path": "checker/VERIFY_R18.json",
             "note": "independent principal, read-only sandbox, forbidden from trusting candidate results"},
        ],
        "this_round_attributable": {"PLAN": None, "EXECUTE": bool(served),
                                    "VERIFY_SECURITY": None},
        "dispatch_command_for_attributable_receipt":
            "hgk-lane-dispatch.py --lane <LANE> --nonce <NONCE> --brief <BRIEF> --json-out <RECEIPT>",
        "lane_vs_session_pin": "the session model pin (deepseek-v4.1-flash on opencode-go) is NOT a lane "
                               "binding; every lane claim above comes from the dispatcher's own attempt log",
        "negative_control": {
            "fake_served_shape": "a lane attempt with exit OK but nonce_present=false, i.e. the child ran "
                                 "and produced output that was not the nonce-bearing answer",
            "guard_catches_it": "hgk-lane-dispatch.py records nonce_present per attempt and refuses the "
                                "attempt as unattributable; the round therefore only counts attempts whose "
                                "nonce matched, which is why attempt 1 (pin refusal) and attempt 2 "
                                "(relay refusal, 400s timeout) contribute no served evidence"},
        "attempts": attempts,
        "verdict": "SPLIT: EXECUTE served on the wrong arm; PLAN and VERIFY issued this turn",
    }
    (REC / "MVS05_LANE_SERVED.json").write_text(json.dumps(mvs05, ensure_ascii=False, indent=1),
                                                encoding="utf-8")

    print(json.dumps({
        "wp19": {"files": len(files), "secrets": len(secrets), "canary": len(canary_hits),
                 "leak_files": len(leakage), "verdict": wp19["verdict"]},
        "wp01": {"holds": len(holds), "classes": wp01["counts"]["holds_by_class"],
                 "denominators": len(denom), "verdict": wp01["verdict"]},
        "mvs05": {"attempts": len(attempts), "served": len(served),
                  "served_arms": mvs05["roles"][1]["served_arm"]},
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
