# 07 - Monitoring & API Integration (Read-First, Safe-by-Default)
Home: [README](./README.md)

## Who this is for
- Learners integrating external monitoring or telemetry APIs into Python data workflows.
- Teams needing reliable API-based reporting and downstream dashboards.

## What you will build
- Read-only ingestion jobs for external monitoring APIs.
- Shared database cache tables for dashboard-friendly access.
- A documented field mapping worksheet and data contract.

## Prerequisites
- SQL ETL baseline from [06_SQL.md](./06_SQL.md).
- API credentials (key or token) for your monitoring platform.
- Database write access to cache schema.

## Step-by-step lab pack

### Step 1 - Read-only policy baseline
Before any code:
- confirm API scopes,
- enforce read-only endpoints,
- define timeout and retry standards.

No write operations are allowed until validation checklist passes.

### Step 2 - Monitoring API ingestion starter
Use any monitoring or telemetry API you have access to. Good free options for learning:
- [OpenWeatherMap API](https://openweathermap.org/api) (weather monitoring)
- [GitHub API](https://docs.github.com/en/rest) (repository/event monitoring)
- [UptimeRobot API](https://uptimerobot.com/api/) (uptime monitoring)

Initial pulls:
- active alerts or events,
- resource/node health status,
- key metrics or utilization data.

### Step 3 - Secondary source ingestion
Add a second data source to practice multi-source integration:
- a different API endpoint from the same platform,
- or a complementary monitoring service.

Initial pulls:
- monitored instances or resources,
- health and performance metrics,
- alert/event summary.

### Step 4 - Shared database cache contract
Create cache tables with source metadata:
- `cache_monitoring_alerts`
- `cache_monitoring_nodes`
- `cache_perf_instances`
- `cache_perf_metrics`

Required columns:
- `source_system`
- `collected_at_utc`
- `entity_key`
- `payload_hash`

### Step 5 - Field mapping worksheet
Maintain this worksheet in your project docs:

| Entity | Source system | Collection cadence | Destination table | Owner |
|---|---|---|---|---|
| Active alerts | Monitoring API | Every 15 min | cache_monitoring_alerts | Monitoring team |
| Node status | Monitoring API | Every 15 min | cache_monitoring_nodes | Monitoring team |
| Instance health | Performance API | Every 30 min | cache_perf_instances | DBA team |
| Performance metrics | Performance API | Hourly | cache_perf_metrics | DBA team |

### Step 6 - Daily ops report build
Outputs:
- `output/monitoring_daily.xlsx`
- `output/monitoring_daily.html`
- `logs/monitoring_run_YYYYMMDD.log`

Include:
- top critical alerts,
- down resource summary,
- instance health snapshot,
- stale data warnings.

## Expected output
- Stable read-only ingestion from monitoring APIs.
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
- describe your API data contracts,
- prove read-only ingestion reliability,
- explain fallback when source APIs are unavailable.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: vary polling intervals and compare freshness/cost tradeoffs.
- Build: implement both ingestion jobs and cache writes.
- Dissect: annotate one end-to-end payload transform.
- Teach-back: present source-to-cache architecture to a peer.

## Primary Sources
- [OpenWeatherMap API](https://openweathermap.org/api)
- [GitHub REST API](https://docs.github.com/en/rest)
- [requests library](https://docs.python-requests.org/en/latest/)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## Optional Resources
- [UptimeRobot API](https://uptimerobot.com/api/)
- [httpx documentation](https://www.python-httpx.org/)

## Sample database schemas
- Use this schema pack for cache and downstream marts:
  - [13_SAMPLE_DATABASE_SCHEMAS.md](./13_SAMPLE_DATABASE_SCHEMAS.md)

## Next

[Next: concepts/http-explained.md →](./concepts/http-explained.md)
