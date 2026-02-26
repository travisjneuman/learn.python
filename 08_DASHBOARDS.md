# 08 - Web GUIs and Dashboards (Browser-First Delivery)
Home: [README](./README.md)

## Who this is for
- Learners ready to deliver operational insights to non-technical users.
- Teams that need browser-only access to reporting and health data.

## What you will build
- A browser-consumable dashboard backed by database cache tables.
- Filters, exports, and freshness indicators usable by operations teams.

## Prerequisites
- Cache tables and summaries from [07_MONITORING_API_INTEGRATION.md](./07_MONITORING_API_INTEGRATION.md).
- Clean SQL summary outputs from [06_SQL.md](./06_SQL.md).

## Step-by-step lab pack

### Step 1 - Define dashboard user stories
Examples:
- "Show top critical alerts by site in last 24 hours."
- "Show database instance health for all monitored environments."
- "Export filtered results to CSV."

### Step 2 - Build Streamlit baseline (beginner-first)
- Use [Streamlit get started](https://docs.streamlit.io/get-started).
- Create one page with:
  - date range filter,
  - severity filter,
  - site/customer filter,
  - table and chart outputs,
  - export button.

### Step 3 - Add cache and data freshness
- Query database cache first, not live APIs per request.
- Display `last_refresh_utc` on every page.
- Warn user when data is stale.

### Step 4 - Add advanced option (Dash)
- Implement same features in Dash for more app-like structure.
- Use [Dash tutorial](https://dash.plotly.com/tutorial).

### Step 5 - Add optional service layer (FastAPI)
Use when you need:
- auth integration,
- controlled API surface,
- multiple frontends.

Reference: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/).

### Step 6 - Deployment path options
1. Local-only developer run.
2. Internal server deployment for team use.
3. Future option: host on cloud infrastructure if architecture and security review approves.

## Expected output
- A dashboard accessible in browser with reliable and understandable data.
- A simple deployment and support model documented for your environment.

## Break/fix drills
1. Disable one cache source and validate graceful degradation.
2. Simulate stale data and verify warning banners.
3. Test extremely large result sets and confirm pagination/limits.

## Troubleshooting
- slow page loads:
  - pre-aggregate summary tables,
  - use query limits,
  - add caching.
- confusing UX:
  - remove non-essential charts,
  - prioritize filters and key metrics.
- source outages:
  - serve last known snapshot with explicit timestamp.

## Mastery check
You are done when a non-technical user can:
- open dashboard in browser,
- filter by date/site/severity,
- export needed views,
- trust freshness indicators.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: redesign one dashboard view and test usability.
- Build: implement full baseline with Streamlit first.
- Dissect: review SQL query flow from UI event to data return.
- Teach-back: demo dashboard operation to ops stakeholders.

## Primary Sources
- [Streamlit get started](https://docs.streamlit.io/get-started)
- [Dash tutorial](https://dash.plotly.com/tutorial)
- [Dash deployment](https://dash.plotly.com/deployment)
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI security basics](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)

## Navigation support
- If you want faster progress through this phase with less friction:
  - [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md)

## Next

[Next: projects/level-8/README.md →](./projects/level-8/README.md)
