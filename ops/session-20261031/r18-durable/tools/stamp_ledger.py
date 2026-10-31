"""Stamp the R18 ledger from what was actually measured this round.

Status vocabulary (the ledger's own): DONE / REUSE / PARTIAL / HOLD / PARKED / NOT_RUN.
Nothing here is aspirational: every DONE/REUSE row names a receipt that exists on disk, and the
ledger's --audit re-checks that. A row is HOLD when the missing thing is an authority I cannot mint,
PARKED when the work is legally deferred to another round, PARTIAL when measured evidence exists but
does not reach the row's own acceptance bar.

Ground truth behind each stamp:
  WP-FHS-00  receipts/WP00_SOURCE_CURRENTNESS.json  (82 manifest rows / 83 checksums / 84 zip members / 22 nodes / 36 edges)
  WP-FHS-18  receipts/WP18_D_R18_01_REPAIR.json + C99 repair + negative control (2 real defects, red->green)
  WP-FHS-21  receipts/ORACLE96_RERUN.json (96 cells, 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL, MATCH)
             + receipts/WP21_SOURCE_BYTES_TRIAGE.json + receipts/WP21_STALE_SOURCE_PIN_MAPPING.json
             ceiling: native_case_pass = 0, independent_verdict = NOT_RUN
  WP-FHS-01  receipts/WP21_SOURCE_BYTES_TRIAGE.json (authority of the pinned source set) - partial
  WP-FHS-02/03/17, 04..14, 15/16, 19, 20: no receipt this round -> PARKED/HOLD with named next step
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
DRIVER = ROOT / "tools" / "ledger_driver.py"
R = "receipts/"

STAMPS = {
    "WP-FHS-00": ("DONE", "VERIFIED",
                  f"{R}WP00_SOURCE_CURRENTNESS.json",
                  "source currentness, 83/83 in-package checksums, 84 zip members byte-identical, 22/36 DAG"),
    "WP-FHS-18": ("DONE", "REPAIRED",
                  f"{R}WP18_D_R18_01_REPAIR.json",
                  "2 real defects found+repaired: D-R18-01 stale source pins (2788/1 -> 2789/0), "
                  "D-R18-02 B1 C99 vacuous predicate (108/108 with a fail-able negative control)"),
    "WP-FHS-21": ("PARTIAL", "MEASURED",
                  f"{R}ORACLE96_RERUN.json",
                  "96 cells reproduced exactly (50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL, 679/0 author checks); "
                  "native_case_pass=0 and independent_verdict=NOT_RUN, so this is author-local evidence only"),
    "WP-FHS-01": ("PARTIAL", "MEASURED",
                  f"{R}WP21_STALE_SOURCE_PIN_MAPPING.json",
                  "authority of the pinned source set measured: 29 pins point at the superseded DRAFT tree "
                  "(20 remapped to changed revision2 bytes, 9 no equivalent); full authority ledger not closed"),
    "WP-FHS-19": ("HOLD", "DEGRADED",
                  "NO_RECEIPT_YET",
                  "supply-chain scan delegated and still outstanding; no claim may be made until the receipt exists"),
    "WP-FHS-15": ("PARKED", "NOT_RUN", "NO_RECEIPT_YET",
                  "TPM 3-SPEC / 18-stage / 24-slot-25-method reuse-verify requires the real plugin invocation "
                  "receipt, which this round did not produce"),
    "WP-FHS-16": ("PARKED", "NOT_RUN", "NO_RECEIPT_YET",
                  "disposition table inherits WP-15's missing invocation receipt"),
    "WP-FHS-05": ("PARKED", "NOT_RUN", "NO_RECEIPT_YET",
                  "PIPD PI/PD/ECP candidates reuse-verify: PIPD promotion stays HOLD without a Writer ACK; "
                  "no Writer ACK was obtainable this round"),
    "WP-FHS-07": ("PARKED", "NOT_RUN", "NO_RECEIPT_YET",
                  "native PLAN Commander A/B/C + PLAN lane: native WorkOrder admission needs an owner-signed "
                  "bundle; self-minting is forbidden"),
}

DEFER = "native effect requires an authority this agent cannot mint (owner-signed native bundle / protected checker inbox)"

for wp in ["WP-FHS-02", "WP-FHS-03", "WP-FHS-04", "WP-FHS-06", "WP-FHS-08", "WP-FHS-09", "WP-FHS-10",
           "WP-FHS-11", "WP-FHS-12", "WP-FHS-13", "WP-FHS-14", "WP-FHS-17", "WP-FHS-20"]:
    STAMPS.setdefault(wp, ("PARKED", "NOT_RUN", "NO_RECEIPT_YET", DEFER))

if __name__ == "__main__":
    base = json.loads((ROOT / "ledger.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in base["rows"]] if isinstance(base, dict) else [r["id"] for r in base]
    missing = [k for k in STAMPS if k not in ids]
    print("ledger rows:", len(ids), "| stamps:", len(STAMPS), "| unknown ids:", missing)
    fail = 0
    for wp, (status, eng, ev, note) in STAMPS.items():
        if wp not in ids:
            continue
        cmd = [sys.executable, "-B", str(DRIVER), "--set", wp, f"status={status}", f"engineering={eng}",
               f"evidence={ev}", f"note={note}"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0:
            fail += 1
            print("SET FAILED", wp, p.returncode, (p.stderr or p.stdout)[:200])
    print("set failures:", fail)
