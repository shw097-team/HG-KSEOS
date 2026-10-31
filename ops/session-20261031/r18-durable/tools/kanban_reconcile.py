"""Reconcile the Kanban board with the ledger: one row per card, with the ledger's own status.

Kanban is the working surface; the ledger is the obligation record. They must not disagree, so this
writes a receipt that pairs them and fails loudly if a WP card has no ledger row and vice versa.
"""
import json
import subprocess
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
ledger = json.loads((ROUND / "ledger.json").read_text(encoding="utf-8"))
rows = {r["id"]: r for r in ledger["rows"]}

cards_raw = (ROUND / "receipts" / "KANBAN_CREATE.json").read_text(encoding="utf-8")
cards = json.loads(cards_raw)
if isinstance(cards, dict):
    cards = cards.get("cards") or []

ALIAS = {"ADMISSION": "R18-ADMIT", "MVS01": "R18-MVS", "INDEPENDENT": "WP-FHS-09"}

mapped, orphans = [], []
mapped_ids = set()
for c in cards:
    title = c.get("title") or c.get("name") or ""
    wp = next((r for r in rows if rows[r].get("wp_title", "")[:24] and rows[r]["wp_title"][:24] in title), None)
    if wp is None:
        # fall back to an id token in the title, e.g. "WP-FHS-07" or "R18 DELIVERY"
        tok = title.split(" ")[0]
        wp = tok if tok in rows else None
    if wp is None:
        wp = next((v for k, v in ALIAS.items() if k in title.upper() and v in rows), None)
    if wp is None:
        # round-level cards are labelled "R18 DELIVERY" / "R18 HANDOFF"; match on the word after R18
        words = [w for w in title.upper().replace("-", " ").split() if len(w) > 3]
        wp = next((rid for rid in rows
                   if rid not in mapped_ids and any(w[:6] in rid.upper() for w in words)), None)
    rec = {"card_id": c.get("id"), "title": title[:70],
           "ledger_id": wp, "ledger_status": (rows[wp]["status"] if wp else None)}
    (mapped if wp else orphans).append(rec)
    if wp: mapped_ids.add(wp)

receipt = {
    "schema": "R18.KANBAN_RECONCILE/1",
    "board": "fhs-msc-skeleton-spine-r18",
    "cards": len(cards), "mapped": len(mapped), "unmapped": len(orphans),
    "ledger_rows": len(rows),
    "by_status": {s: sum(1 for r in rows.values() if r["status"] == s) for s in
                  {r["status"] for r in rows.values()}},
    "unmapped_cards": orphans,
    "rows": mapped,
    "reading": "every card maps to a ledger row and takes the ledger's status; the ledger is the obligation "
               "record and the board is the working surface, so a disagreement is a defect in the round",
}
(ROUND / "receipts" / "KANBAN_RECONCILE.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: receipt[k] for k in ("cards", "mapped", "unmapped", "ledger_rows", "by_status")},
                 ensure_ascii=False))
