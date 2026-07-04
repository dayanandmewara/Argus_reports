"""
Deterministic render step. Takes:
  - <TICKER>.json         (the existing 22-field tracker record)
  - <TICKER>_blocks.json  (per-tab content — new, currently only bootstrapped from history)
  - <TICKER>_hero_extra.json (small gap-fill fields not yet in the tracker schema)
  - template.html.jinja   (the static shell, built once)
and produces <TICKER>_qv_report_REBUILT.html.

No model call happens in this script. This is meant to run in a bash sandbox
today, or as a GitHub Action on push, tomorrow.
"""
import json
import sys
from jinja2 import Environment, FileSystemLoader

TICKER = sys.argv[1] if len(sys.argv) > 1 else "IGIL"

tracker = json.load(open(f"{TICKER}.json", encoding="utf-8"))
blocks = json.load(open(f"{TICKER}_blocks.json", encoding="utf-8"))
extra = json.load(open(f"{TICKER}_hero_extra.json", encoding="utf-8"))

ctx = {
    "ticker": tracker["Ticker"],
    "company": tracker["Company"],
    "market": tracker["Market"],
    "verdict": tracker["Verdict"].replace("★", " ★", 1) if "★" in tracker["Verdict"] and " ★" not in tracker["Verdict"] else tracker["Verdict"],
    "stars": int(tracker["Stars"]),
    "category": tracker["Category"],
    "price": tracker["Price at Analysis"],
    "thesis": tracker["Thesis"],
    "framework_version": extra.get("framework_version", "V5.0"),
    "sector_line": extra.get("sector_line", ""),
    "category_label": extra.get("category_label", ""),
    "ai_overlay": extra.get("ai_overlay", tracker.get("AI Overlay", "")),
    "macro_composite": extra.get("macro_composite", ""),
    "history_caveat": extra.get("history_caveat", ""),
    "footer_note": blocks["_footer_note_raw"].rstrip("\n"),
    "blocks": {k: v for k, v in blocks.items() if not k.startswith("_")},
}

env = Environment(loader=FileSystemLoader("."), keep_trailing_newline=True, autoescape=True)
tpl = env.get_template("template.html.jinja")
output = tpl.render(**ctx)

out_path = f"{TICKER}_qv_report_REBUILT.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Wrote {out_path} ({len(output)} chars)")
