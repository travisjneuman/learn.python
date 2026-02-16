# 13 - Enterprise Sample Schemas (MSSQL + Orion + DPA)
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
CREATE TABLE dbo.staging_alerts (
    staging_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    load_batch_id UNIQUEIDENTIFIER NOT NULL,
    source_file NVARCHAR(260) NOT NULL,
    source_row_num INT NULL,
    customer_name NVARCHAR(200) NULL,
    site_name NVARCHAR(200) NULL,
    ticket_id NVARCHAR(100) NULL,
    status_text NVARCHAR(100) NULL,
    opened_at_raw NVARCHAR(100) NULL,
    payload_hash CHAR(64) NOT NULL,
    ingested_at_utc DATETIME2(0) NOT NULL,
    ingest_error NVARCHAR(500) NULL
);
```

## Example: curated reporting table
```sql
CREATE TABLE dbo.alerts_reporting (
    alert_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    idempotency_key CHAR(64) NOT NULL UNIQUE,
    customer_name NVARCHAR(200) NOT NULL,
    site_name NVARCHAR(200) NOT NULL,
    ticket_id NVARCHAR(100) NOT NULL,
    severity NVARCHAR(50) NOT NULL,
    opened_at_utc DATETIME2(0) NOT NULL,
    source_system NVARCHAR(50) NOT NULL,
    source_entity_key NVARCHAR(200) NULL,
    collected_at_utc DATETIME2(0) NOT NULL,
    loaded_at_utc DATETIME2(0) NOT NULL
);
```

## Example: Orion cache table
```sql
CREATE TABLE dbo.cache_orion_alerts (
    cache_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_system NVARCHAR(20) NOT NULL DEFAULT 'orion',
    entity_key NVARCHAR(200) NOT NULL,
    alert_name NVARCHAR(300) NULL,
    severity NVARCHAR(50) NULL,
    node_caption NVARCHAR(300) NULL,
    is_active BIT NOT NULL,
    payload_hash CHAR(64) NOT NULL,
    collected_at_utc DATETIME2(0) NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);
```

## Example: DPA cache table
```sql
CREATE TABLE dbo.cache_dpa_instances (
    cache_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_system NVARCHAR(20) NOT NULL DEFAULT 'dpa',
    entity_key NVARCHAR(200) NOT NULL,
    instance_name NVARCHAR(300) NULL,
    health_status NVARCHAR(100) NULL,
    wait_category NVARCHAR(200) NULL,
    payload_hash CHAR(64) NOT NULL,
    collected_at_utc DATETIME2(0) NOT NULL,
    UNIQUE (source_system, entity_key, collected_at_utc)
);
```

## Example: dashboard mart view
```sql
CREATE VIEW dbo.vw_ops_dashboard_daily AS
SELECT
    CAST(collected_at_utc AS DATE) AS snapshot_date,
    severity,
    COUNT(*) AS alert_count
FROM dbo.cache_orion_alerts
WHERE is_active = 1
GROUP BY CAST(collected_at_utc AS DATE), severity;
```

## Example index strategy
```sql
CREATE INDEX IX_alerts_reporting_opened_severity
ON dbo.alerts_reporting (opened_at_utc, severity);

CREATE INDEX IX_cache_orion_alerts_collected
ON dbo.cache_orion_alerts (collected_at_utc);

CREATE INDEX IX_cache_dpa_instances_collected
ON dbo.cache_dpa_instances (collected_at_utc);
```

## Data governance notes
- Prefer service accounts over personal credentials for scheduled jobs.
- Log source endpoint and load batch for auditability.
- Mask or exclude sensitive payload fields before persistence.
- Validate schema drift and alert on missing critical fields.

## Primary Sources
- [SQL Server Python drivers overview](https://learn.microsoft.com/en-gb/sql/connect/python/python-driver-for-sql-server)
- [MSSQL Python quickstart](https://learn.microsoft.com/en-us/sql/connect/python/mssql-python/python-sql-driver-mssql-python-quickstart?view=sql-server-ver17)
- [ODBC connection string keywords](https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver17)
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)

## Optional Resources
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [python-oracledb docs](https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html)

## Next
Go to [14_NAVIGATION_AND_STUDY_WORKFLOW.md](./14_NAVIGATION_AND_STUDY_WORKFLOW.md).
