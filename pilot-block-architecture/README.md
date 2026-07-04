# Argus Block-Render Pilot (isolated experiment)

**This folder is a standalone test. It does not read from or write to
`data/stocks/`, `stock-reports/`, or `prompts/`. Nothing here touches the
production BQV pipeline.**

## What this is

A test of splitting a BQV report into:
- a static template (`template.html.jinja`) — CSS, tab bar, script; identical for every ticker
- per-tab content blocks (`IGIL_blocks.json`) — the actual analysis text, one key per tab
- a small gap-fill file (`IGIL_hero_extra.json`) — a few hero fields not yet in the tracker schema
- a render script (`render.py`) — deterministic, no LLM call: JSON + template → HTML

Goal: stop re-reading and re-writing the whole HTML file for every update —
only touch the block that actually changed, and let a script (not a model)
reassemble the report.

## Result so far

Rebuilt IGIL's real report from data alone. `IGIL_qv_report_REBUILT.html` is
**624 of 626 lines byte-identical** to the original in `stock-reports/`. The
2 differences are documented below — neither is a bug.

Then simulated a small macro update (RBI rate cut) by patching only the
`macro_growth` key in the blocks JSON and re-rendering.
`IGIL_qv_report_PATCHED.html` differs from the REBUILT version in **exactly
the 2 lines that were patched** — nothing else in the 626-line file moved.

## How to run it

```
pip install jinja2
python3 render.py IGIL
```

Produces `IGIL_qv_report_REBUILT.html` in this same folder. Diff it against
`stock-reports/IGIL_qv_report.html` in the main repo to check it still matches.

`bootstrap_extract_blocks.py` is the one-time script that pulled the 10 tab
blocks out of the original hand-written HTML in the first place — only
needed for bootstrapping a ticker that predates this pipeline. A brand-new
report would define its blocks directly.

## Open questions before this goes any further

1. **Hero schema gap.** `IGIL_hero_extra.json` holds 5 fields (sector line,
   category label, AI-overlay qualifier, macro composite, listing-history
   caveat) that exist in the HTML today but not in the 22-field tracker
   JSON. Fold into the main schema, or keep as a separate small per-ticker file?
2. **Tab-bar stability.** The tab bar (10 fixed tabs: Overview, Macro &
   Growth, Financials, Moat, Management, Valuation, Verdict, Technical,
   Shareholding, AI Intelligence) is hardcoded into the template as standard
   across every V5.0 report. Does that still hold once V6's Growth
   Compounder Lens tabs get added?
3. **Thesis reuse.** The hero paragraph currently reuses the tracker's
   `Thesis` field instead of a separately hand-written line. Removes
   duplicate writing, but changes the exact wording shown in the hero —
   confirm that's wanted.

## Known pre-existing inconsistency (not introduced by this pilot)

The original report's `<title>` tag says "International Gemmological
Institute (India)" while the Company field / `<h1>` says "...India) Ltd" —
this difference already existed in the source file.

## Next step, if this looks right

Bootstrap a second ticker (Aye Finance) through the same pipeline to check
the template generalizes past IGIL's specific structure, before touching
anything in the production folders.
