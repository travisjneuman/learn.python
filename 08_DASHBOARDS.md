# 08 — Web GUIs / Dashboards (Internal Tools)

## Goal
Build dashboards that:
- pull from SQL + SolarWinds (directly or via SQL cache)
- render charts/tables
- allow filtering and drill-down
- run locally and (optionally) on an internal server

---

## Recommended order (beginner → advanced)
### 1) Streamlit (fastest path)
- Run apps with: `streamlit run your_script.py` citeturn1search14
- Great for internal dashboards without writing HTML/JS.
Docs:
- Get started citeturn1search0

### 2) Dash (more structured dashboards)
- Strong layout + callbacks model
- Great data grids (AG Grid) for “reporting portals”
Docs:
- “Dash in 20 Minutes” citeturn1search1

### 3) FastAPI (when you need a backend API)
- If you want:
  - authentication integration
  - background jobs
  - a clean API for multiple frontends
Docs:
- FastAPI tutorial citeturn1search2

---

## Capstone D: Ops Dashboard (end-to-end)
Pages/Tabs:
1. Excel Reports (latest outputs + download links)
2. SQL Summary (daily/weekly metrics)
3. SolarWinds Health (alerts, down interfaces, capacity)

Core features:
- date range filters
- site/customer filter
- severity filter
- caching (avoid hammering Orion)
- export buttons (CSV/XLSX)

---

## Deployment options (corporate constraints friendly)
1. **Local-only** (you run it on your laptop)
2. **Internal server** (Windows/Linux VM; service account)
3. **Container** (if allowed)
4. **Reverse proxy** (if required) + auth front-door (depends on org)

You will document your org’s constraints in the Capstone writeup.

Next: **[10_CAPSTONE_PROJECTS.md](./10_CAPSTONE_PROJECTS.md)**
