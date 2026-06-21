import json, os, csv, re
from datetime import datetime

STOCKS_DIR = "data/stocks"
OUTPUT_CSV = "data/tracker.csv"

FIELDS = [
    "Ticker", "Company", "Market", "Price at Analysis", "Category",
    "Verdict", "Stars", "Moat", "Quality", "Val", "Mgmt", "AI Overlay",
    "AI Score", "Phase", "Flywheel", "Conditions Met", "Horizon",
    "Base IV", "MoS Entry Zone", "Thesis", "Report File", "Last Analysis Date"
]

def normalize_date(raw):
    raw = (raw or "").strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
        return raw
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw  # leave as-is rather than crash on an unexpected format

def main():
    rows = []
    for fname in sorted(os.listdir(STOCKS_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(STOCKS_DIR, fname), encoding="utf-8") as f:
            data = json.load(f)
        data["Last Analysis Date"] = normalize_date(data.get("Last Analysis Date"))
        rows.append([data.get(field, "") for field in FIELDS])

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
