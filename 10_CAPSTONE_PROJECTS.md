# 10 — Capstone Projects (SME-level portfolio)

## Purpose
These are the projects that prove you are an SME, not just learning.

---

## Capstone A — Excel Merger + Validator + Report
- Input folder of Excel files
- Schema normalization + validation
- Master output + critical output + rejects
- Logs + tests + CLI

(Guide: **[05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md)**)

---

## Capstone B — ETL to SQL
- Ingest from Capstone A outputs
- Load staging + promote to reporting table
- Idempotency key
- Daily summary query exported to CSV

(Guide: **[06_SQL.md](./06_SQL.md)**)

---

## Capstone C — SolarWinds Daily Ops Report
- Read Orion alerts + key metrics
- Store in SQL cache
- Output Excel + HTML

(Guide: **[07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)**)

---

## Capstone D — Ops Dashboard
- Streamlit first; optionally Dash later
- Uses SQL cache + (optional) on-demand Orion queries
- Filters + exports + caching
- Document deployment mode

(Guide: **[08_DASHBOARDS.md](./08_DASHBOARDS.md)**)

---

## “SME bonus” capstone ideas (optional)
- A “report scheduler” wrapper that runs multiple tools, rotates logs, and emails results
- A “data quality monitor” that checks missing metadata in SolarWinds and reports drift
- A “CLI toolkit” that becomes your team standard template

Next: **[11_CHECKLISTS.md](./11_CHECKLISTS.md)**
