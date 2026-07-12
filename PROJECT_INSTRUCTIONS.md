# ARGUS REPORTS — PROJECT INSTRUCTIONS

## STEP 1: Fetch Master Prompt (use PAT from Project Instructions)
```
curl -s -H "Authorization: Bearer [PAT_FROM_PROJECT_INSTRUCTIONS]" \
  -H "Accept: application/vnd.github.v3.raw" \
  "https://api.github.com/repos/dayanandmewara/Argus_reports/contents/prompts/MASTER_BQV_V50.md"
```
Use returned content as your complete framework.

## STEP 2: After Report — Push Both Files

**File 1: HTML Report**
- Path: `stock-reports/[TICKER]_qv_report.html`

**File 2: JSON Data**
- Path: `data/stocks/[TICKER].json`
- Fields (all strings): Ticker, Company, Market, Price at Analysis, Category, Verdict, Stars, Moat, Quality, Val, Mgmt, AI Overlay, AI Score, Phase, Flywheel, Conditions Met, Horizon, Base IV, MoS Entry Zone, Thesis, Report File, Last Analysis Date
- Last Analysis Date = YYYY-MM-DD

**For each file:**
```
1. GET  https://api.github.com/repos/dayanandmewara/Argus_reports/contents/{PATH}
   If 200: capture "sha" | If 404: no sha needed

2. PUT same URL
   Body: {"message":"Update [TICKER]","content":"<base64>","sha":"<from step 1 if 200>"}
   Header: Authorization: Bearer [PAT_FROM_PROJECT_INSTRUCTIONS]
```

**Note:** `data/tracker.csv` auto-rebuilds from JSON — never edit it directly.
