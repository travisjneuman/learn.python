# 13 - Sample Database Schemas
Home: [README](./README.md)

These sample schemas are templates for your learning projects and capstones.
Adjust names and data types for your production standards.

## Schema conventions
- Use UTC timestamps.
- Keep source-system metadata in each table.
- Add unique keys for idempotent loads.
- Separate raw staging from curated reporting tables.

## Example: staging table for Excel ingest
```sql
-- SQLite version (for learning)
CREATE TABLE staging_alerts (
    staging_id INTEGER PRIMARY KEY AUTOINCREMENT,
    load_batch_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_row_num INTEGER,
    customer_name TEXT,
    site_name TEXT,
    ticket_id TEXT,
    status_text TEXT,
    opened_at_raw TEXT,
    payload_hash TEXT NOT NULL,
    ingested_at_utc TEXT NOT NULL,
    ingest_error TEXT
);

-- PostgreSQL version (for production)
CREATE TABLE staging_alerts (
    staging_id BIGSERIAL PRIMARY KEY,
    load_batch_id UUID NOT NULL,
    source_file VARCHAR(260) NOT NULL,
    source_row_num INTEGER,
    customer_name VARCHAR(200),
    site_name VARCHAR(200),
    ticket_id VARCHAR(100),
    status_text VARCHAR(100),
    opened_at_raw VARCHAR(100),
    payload_hash CHAR(64) NOT NULL,
    ingested_at_utc TIMESTAMPTZ NOT NULL,
    ingest_error VARCHAR(500)
);
```

## Example: curated reporting table
```sql
-- SQLite version
CREATE TABLE alerts_reporting (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    idempotency_key TEXT NOT NULL UNIQUE,
    customer_name TEXT NOT NULL,
    site_name TEXT NOT NULL,
    ticket_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    opened_at_utc TEXT NOT NULL,
    source_system TEXT NOT NULL,
    source_entity_key TEXT,
    collected_at_utc TEXT NOT NULL,
    loaded_at_utc TEXT NOT NULL
);

-- PostgreSQL version
CREATE TABLE alerts_reporting (
    alert_id BIGSERIAL PRIMARY KEY,
    idempotency_key CHAR(64) NOT NULL UNIQUE,
    customer_name VARCHAR(200) NOT NULL,
    site_name VARCHAR(200) NOT NULL,
    ticket_id VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    opened_at_utc TIMESTAMPTZ NOT NULL,
    source_system VARCHAR(50) NOT NULL,
    source_entity_key VARCHAR(200),
    collected_at_utc TIMESTAMPTZ NOT NULL,
    loaded_at_utc TIMESTAMPTZ NOT NULL
);
```

## Example: monitoring cache table
```sql
-- SQLite version
CREATE TABLE cache_monitoring_alerts (
    cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system TEXT NOT NULL DEFAULT 'monitoring_api',
    entity_key TEXT NOT NULL,
    alert_name TEXT,
    severity TEXT,
    node_caption TEXT,
    is_active INTEGER NOT NULL,
    payload_hash TEXT NOT NULL,
    collected_at_utc TEXT NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);

-- PostgreSQL version
CREATE TABLE cache_monitoring_alerts (
    cache_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(20) NOT NULL DEFAULT 'monitoring_api',
    entity_key VARCHAR(200) NOT NULL,
    alert_name VARCHAR(300),
    severity VARCHAR(50),
    node_caption VARCHAR(300),
    is_active BOOLEAN NOT NULL,
    payload_hash CHAR(64) NOT NULL,
    collected_at_utc TIMESTAMPTZ NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);
```

## Example: performance monitoring cache table
```sql
-- SQLite version
CREATE TABLE cache_perf_instances (
    cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system TEXT NOT NULL DEFAULT 'perf_api',
    entity_key TEXT NOT NULL,
    instance_name TEXT,
    health_status TEXT,
    wait_category TEXT,
    payload_hash TEXT NOT NULL,
    collected_at_utc TEXT NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);

-- PostgreSQL version
CREATE TABLE cache_perf_instances (
    cache_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(20) NOT NULL DEFAULT 'perf_api',
    entity_key VARCHAR(200) NOT NULL,
    instance_name VARCHAR(300),
    health_status VARCHAR(100),
    wait_category VARCHAR(200),
    payload_hash CHAR(64) NOT NULL,
    collected_at_utc TIMESTAMPTZ NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);
```

## Example: dashboard mart view
```sql
CREATE VIEW vw_ops_dashboard_daily AS
SELECT
    DATE(collected_at_utc) AS snapshot_date,
    severity,
    COUNT(*) AS alert_count
FROM cache_monitoring_alerts
WHERE is_active = 1
GROUP BY DATE(collected_at_utc), severity;
```

## Example index strategy
```sql
CREATE INDEX ix_alerts_reporting_opened_severity
ON alerts_reporting (opened_at_utc, severity);

CREATE INDEX ix_cache_monitoring_alerts_collected
ON cache_monitoring_alerts (collected_at_utc);

CREATE INDEX ix_cache_perf_instances_collected
ON cache_perf_instances (collected_at_utc);
```

## Data governance notes
- Prefer service accounts over personal credentials for scheduled jobs.
- Log source endpoint and load batch for auditability.
- Mask or exclude sensitive payload fields before persistence.
- Validate schema drift and alert on missing critical fields.

## Primary Sources
- [SQLite documentation](https://www.sqlite.org/docs.html)
- [PostgreSQL documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## Optional Resources
- [python-oracledb docs](https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html)

---

| [← Prev](12_SCREENSHOT_CHECKPOINTS.md) | [Home](README.md) | [Next →](14_NAVIGATION_AND_STUDY_WORKFLOW.md) |
|:---|:---:|---:|
