import json
import re

SRC = "IGIL_qv_report.html"
with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()  # keep line endings intact

TAB_OPEN_LINES = {  # 1-indexed line number of the opening <div ... id="tN"> tag
    "overview": 146, "macro_growth": 174, "financials": 236, "moat": 289,
    "management": 339, "valuation": 369, "verdict": 429, "technical": 463,
    "shareholding": 513, "ai_intelligence": 549,
}

def find_matching_close(open_idx0):
    """open_idx0 is 0-indexed line of the opening div. Returns 0-indexed line of matching </div>."""
    depth = 0
    for i in range(open_idx0, len(lines)):
        opens = len(re.findall(r"<div[\s>]", lines[i]))
        closes = lines[i].count("</div>")
        depth += opens - closes
        if depth == 0:
            return i
    raise ValueError("no matching close found")

blocks = {}
bounds = {}
for key, open_line in TAB_OPEN_LINES.items():
    open_idx0 = open_line - 1
    close_idx0 = find_matching_close(open_idx0)
    inner_lines = lines[open_idx0 + 1: close_idx0]  # exclude open+close div lines themselves
    blocks[key] = "".join(inner_lines)
    bounds[key] = (open_idx0 + 2, close_idx0)  # 1-indexed inner range, for reporting

# footer paragraph - exact line-based too
footer_line_idx = next(i for i, l in enumerate(lines) if l.startswith("<footer>"))
footer_p_idx = footer_line_idx + 1  # the <p> line right after
blocks["_footer_note_raw"] = lines[footer_p_idx]

with open("IGIL_blocks.json", "w", encoding="utf-8") as f:
    json.dump(blocks, f, ensure_ascii=False, indent=2)

for k, v in blocks.items():
    b = bounds.get(k, "-")
    print(f"{k}: lines {b}, {len(v)} chars")

# Sanity check: does the extracted text appear verbatim in the source?
full_html = "".join(lines)
for key in TAB_OPEN_LINES:
    ok = blocks[key] in full_html
    print(f"exact-substring-match[{key}] = {ok}")
print(f"exact-substring-match[footer] = {blocks['_footer_note_raw'] in full_html}")
