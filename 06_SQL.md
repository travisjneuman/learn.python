# 06 - SQL Integration (MSSQL-First ETL for Reporting and Dashboards)
Home: [README](./README.md)

## Who this is for
- Learners moving from file automation to data pipelines.
- Teams with MSSQL as a reporting backbone.

## What you will build
- A Python ETL pipeline that ingests validated records into MSSQL.
- Staging and reporting tables with idempotent loads.
- A daily summary query output for dashboard use.

## Prerequisites
- Capstone A outputs from [05_AUTOMATION_FILES_EXCEL.md](./05_AUTOMATION_FILES_EXCEL.md).
- Basic SQL query familiarity.
- DB credentials with insert/select access in target schema.

## Step-by-step lab pack

### Lab 1 - SQL fundamentals in strict order
1. `SELECT` and `WHERE`.
2. `GROUP BY` aggregates.
3. `JOIN` across lookup tables.
4. `INSERT` and `UPDATE` basics.
5. transactions with commit/rollback.

### Lab 2 - Table design
Create tables:
- `staging_alerts`
- `alerts_reporting`

Minimum metadata fields:
- `source_file`
- `ingested_at_utc`
- `idempotency_key`

### Lab 3 - Python connection strategy
Preferred start: `pyodbc`.
Optional scaling path: SQLAlchemy.

Connection requirements:
- no hardcoded secrets,
- explicit timeout,
- retry for transient failures,
- structured error logging.

### Lab 4 - Load strategy
1. Load raw validated rows into `staging_alerts`.
2. Promote clean rows into `alerts_reporting`.
3. Use `idempotency_key` to prevent duplicates.

### Lab 5 - Daily summary output
Generate query output by:
- date,
- severity,
- customer/site.

Export summary to `output/daily_summary.csv` for dashboard consumption.

### Lab 6 - Custom reporting backend integration
For your contractor-built MSSQL reporting DB:
- identify existing table contracts,
- map your ETL output to existing schema,
- avoid direct writes to unmanaged tables until schema ownership is clear.

### Lab 7 - Optional Oracle extension
If Oracle sources are added later:
- ingest to staging only first,
- normalize data types to MSSQL-compatible forms,
- preserve source system metadata.

## Expected output
- Repeatable ETL job with clean staging-to-reporting flow.
- No duplicate records on reruns.
- Usable CSV summary artifacts for dashboards.

## Break/fix drills
1. Force duplicate ingest and prove idempotency key blocks duplicates.
2. Simulate DB timeout and confirm retries/logging.
3. Insert malformed rows in staging and verify promotion filter blocks them.

## Troubleshooting
- connection failures:
  - confirm driver installation,
  - validate host, db name, user,
  - test least-privilege account manually.
- duplicate rows:
  - inspect key generation and unique constraint.
- poor query performance:
  - add indexes on date, severity, idempotency key.

## Mastery check
You are ready for SolarWinds ingestion when you can:
- explain your table contract,
- rerun ETL safely,
- recover from transient DB failures,
- produce daily summaries without manual edits.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: test different idempotency key designs.
- Build: implement full staging -> reporting pipeline.
- Dissect: explain query plans and table role boundaries.
- Teach-back: present ETL data flow and failure strategy.

## Primary Sources
- [SQL Server Python drivers overview](https://learn.microsoft.com/en-gb/sql/connect/python/python-driver-for-sql-server)
- [MSSQL Python quickstart](https://learn.microsoft.com/en-us/sql/connect/python/mssql-python/python-sql-driver-mssql-python-quickstart?view=sql-server-ver17)
- [ODBC connection strings](https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver17)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)

## Optional Resources
- [pyodbc project](https://github.com/mkleehammer/pyodbc)
- [python-oracledb docs](https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html)

## Enterprise sample schemas
- Full schema pack for staging/reporting/cache/marts:
  - [13_ENTERPRISE_SAMPLE_SCHEMAS.md](./13_ENTERPRISE_SAMPLE_SCHEMAS.md)

## Next
Go to [07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md).
