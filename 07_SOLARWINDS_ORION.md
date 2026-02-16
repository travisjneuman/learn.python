# 07 — SolarWinds Orion Integration (SQL + Reporting + Automation)

## Goal
Use Orion data as a first-class input to your reporting and dashboards.

Primary references:
- Orion SDK repo (samples/tools) citeturn0search23
- Python client for Orion API citeturn0search3

Reality note:
- Orion documentation can be scattered; you will rely heavily on:
  - the SDK tooling
  - example queries
  - exploring entities/fields
  - controlled read-only scripts first

---

## What you will build first (safe, read-only)
### Capstone C: SolarWinds Daily Ops Report
Inputs:
- Orion API (alerts, nodes, interfaces, volumes, etc.)

Outputs:
- `output/solarwinds_daily.xlsx`
- `output/solarwinds_daily.html`
- `logs/solarwinds_run.log`

Features:
- top N active alerts by severity
- down interfaces in last 24 hours
- capacity metrics (top utilizations)
- “exceptions” list (devices missing required metadata)

---

## Recommended learning progression
1. Connect and run a simple query (read-only)
2. Enumerate what entities exist in *your* environment
3. Build a “data contract” (which fields you rely on)
4. Store results in SQL (so dashboards don’t hit Orion constantly)
5. Only then consider write actions (acknowledge alerts, add notes), and only if your org permits it

---

## Practical tip: treat Orion like an external API
- Always:
  - set timeouts
  - handle authentication failures
  - retry transient errors
  - log request/response metadata (sanitized)

Next: **[08_DASHBOARDS.md](./08_DASHBOARDS.md)**
