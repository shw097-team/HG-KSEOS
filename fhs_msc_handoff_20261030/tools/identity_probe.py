"""Is the first-work PI identity root-independent?

The delivered PI/TaskSpecSeed/FUO carry different ids when the same bytes are compiled under a
different absolute draft root. This probe isolates the mechanism and tests the receiver-side
repair that needs no change to the original PIPD compiler:

  control : intake() handed an ABSOLUTE source path -> id is a function of the physical root
  repair  : intake() handed a ROOT-RELATIVE source path (cwd = draft root) -> id is a function
            of the bytes only

Exit 0 when the repair reproduces identical identity across two distinct roots.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

READERS = Path(r"C:\wg\repro\03_HANDOFF_EVIDENCE\READERS\PIPD")
sys.path.insert(0, str(READERS / "src"))
from pipd_ls_sp import pipeline  # noqa: E402

GOAL = ("為普通 Goal 產生有來源與可判 POS/NEG 的 Product、Architecture、Program SPEC，"
        "交原 PIPD，再交 Hermes 於原權限下續工")
SRC = Path(r"C:\wg\repro\02_FIRST_WORK\FIRST_WORK_FUNCTIONAL_SOURCE.md")
ROOTS = [Path(r"C:\wg\idprobe\r1"), Path(r"C:\wg\idprobe\r2")]


def compile_at(root: Path, *, relative: bool) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    target = root / SRC.name
    shutil.copy2(SRC, target)
    old = os.getcwd()
    os.chdir(root)
    try:
        src = SRC.name if relative else str(target)
        card = pipeline.intake(GOAL, sources=[src],
                               constraints=["SOURCE_READ then LOCAL_DRAFT", "provider_off=true",
                                            "exact isolated draft outputs"],
                               non_goals=["Native admission", "install/build", "world effect",
                                          "independent acceptance", "release"])
        pi = pipeline.strip_sidecar(pipeline.compile_pi(card, "STANDARD"))
    finally:
        os.chdir(old)
    return {"subject_id": pi["subject_id"], "content_hash": pi["content_hash"],
            "atoms": len(pi["stable_semantic_contract"]["atoms"])}


def main() -> int:
    ctl = [compile_at(r, relative=False) for r in ROOTS]
    rep = [compile_at(r, relative=True) for r in ROOTS]
    out = {
        "control_absolute_path": ctl,
        "control_identical": ctl[0]["content_hash"] == ctl[1]["content_hash"],
        "repair_relative_path": rep,
        "repair_identical": rep[0]["content_hash"] == rep[1]["content_hash"],
        "reading": ("absolute-path intake makes identity a function of the physical draft root; "
                    "root-relative intake makes it a function of the source bytes"),
        "writer_modified": False,
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if (not out["control_identical"] and out["repair_identical"]) else 3


if __name__ == "__main__":
    raise SystemExit(main())
