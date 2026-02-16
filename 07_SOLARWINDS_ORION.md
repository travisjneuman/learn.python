# 07 - SolarWinds Orion + DPA Integration (Read-First, Safe-by-Default)
Home: [README](./README.md)

## Who this is for
- Learners integrating monitoring systems into Python data workflows.
- Teams needing reliable Orion/DPA reporting and downstream dashboards.

## What you will build
- Read-only ingestion jobs for Orion and DPA.
- Shared MSSQL cache tables for dashboard-friendly access.
- A documented field mapping worksheet and data contract.

## Prerequisites
- SQL ETL baseline from [06_SQL.md](./06_SQL.md).
- Orion and DPA read access credentials.
- MSSQL write access to cache schema.

## Step-by-step lab pack

### Step 1 - Read-only policy baseline
Before any code:
- confirm API scopes,
- enforce read-only endpoints,
- define timeout and retry standards.

No write operations are allowed until validation checklist passes.

### Step 2 - Orion ingestion starter
Use:
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [orionsdk-python](https://github.com/solarwinds/orionsdk-python)

Initial pulls:
- active alerts,
- node health,
- interface status,
- capacity/utilization metrics.

### Step 3 - DPA ingestion starter
Use [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm).

Initial pulls:
- monitored instances,
- health and wait metrics,
- alert/event summary.

### Step 4 - Shared MSSQL cache contract
Create cache tables with source metadata:
- `cache_orion_alerts`
- `cache_orion_nodes`
- `cache_dpa_instances`
- `cache_dpa_waits`

Required columns:
- `source_system`
- `collected_at_utc`
- `entity_key`
- `payload_hash`

### Step 5 - Field mapping worksheet
Maintain this worksheet in your project docs:

| Entity | Source system | Collection cadence | Destination table | Owner |
|---|---|---|---|---|
| Active alerts | Orion | Every 15 min | cache_orion_alerts | Monitoring team |
| Node status | Orion | Every 15 min | cache_orion_nodes | Monitoring team |
| Instance health | DPA | Every 30 min | cache_dpa_instances | DBA team |
| Wait metrics | DPA | Hourly | cache_dpa_waits | DBA team |

### Step 6 - Daily ops report build
Outputs:
- `output/solarwinds_daily.xlsx`
- `output/solarwinds_daily.html`
- `logs/solarwinds_run_YYYYMMDD.log`

Include:
- top critical alerts,
- down interface summary,
- DB instance health snapshot,
- stale data warnings.

## Expected output
- Stable read-only ingestion from Orion and DPA.
- Reliable cache tables for dashboards.
- Traceable field mappings and data ownership.

## Break/fix drills
1. Force token/auth failure and verify sanitized error logging.
2. Simulate API timeout and validate retry/backoff.
3. Remove required field from payload transform and verify reject behavior.

## Troubleshooting
- auth errors:
  - validate credential scope,
  - test endpoint manually,
  - confirm clock/time sync for token validity.
- schema drift:
  - compare payload keys against mapping worksheet,
  - route unknown fields to audit logs.
- stale dashboards:
  - verify cache job schedule and `collected_at_utc` freshness checks.

## Mastery check
Advance when you can:
- describe Orion and DPA data contracts,
- prove read-only ingestion reliability,
- explain fallback when source APIs are unavailable.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: vary polling intervals and compare freshness/cost tradeoffs.
- Build: implement both ingestion jobs and cache writes.
- Dissect: annotate one end-to-end payload transform.
- Teach-back: present source-to-cache architecture to a peer.

## Primary Sources
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [orionsdk-python](https://github.com/solarwinds/orionsdk-python)
- [DPA documentation](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_documentation.htm)
- [DPA API guide](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)

## Optional Resources
- [DPA Getting Started](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_getting_started_guide.htm)
- [DPA Administrator Guide](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa_administrator_guide.htm)

## Next
Go to [08_DASHBOARDS.md](./08_DASHBOARDS.md).
