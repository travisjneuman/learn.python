# 30 - Levels 6 to 8 Deep Guide (Professional System Builder)
Home: [README](./README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

This guide is where you build professional data/integration/dashboard capability.

## Objective
Master SQL reliability, Orion/DPA integration behavior, and browser-first dashboard robustness.

## Required docs
- [06_SQL.md](./06_SQL.md)
- [07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)
- [08_DASHBOARDS.md](./08_DASHBOARDS.md)
- [13_ENTERPRISE_SAMPLE_SCHEMAS.md](./13_ENTERPRISE_SAMPLE_SCHEMAS.md)
- [projects/level-6/README.md](./projects/level-6/README.md)
- [projects/level-7/README.md](./projects/level-7/README.md)
- [projects/level-8/README.md](./projects/level-8/README.md)

## Non-negotiable safety rules
1. Read-only first for source systems.
2. Stage first, report later (no direct mart writes).
3. Log run id, source timestamp, batch id, and row counts.
4. Keep reruns idempotent by design.

## Level-6 run pattern (SQL-focused)
```bash
cd <repo-root>/projects/level-6/01-mssql-connection-simulator
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... "project": "MSSQL Connection Simulator" ...
2 passed
```

## Level-7 run pattern (Orion + DPA focused)
```bash
cd <repo-root>/projects/level-7/01-orion-query-adapter
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... "project": "Orion Query Adapter" ...
2 passed
```

## Level-8 run pattern (dashboard-resilience focused)
```bash
cd <repo-root>/projects/level-8/01-dashboard-kpi-assembler
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... "project": "Dashboard KPI Assembler" ...
2 passed
```

## Real-environment command template (when you wire real systems)
Use placeholder values first, then replace safely:
```bash
# examples only: use safe, read-first credentials and endpoints
export SW_ORION_URL="https://your-orion-server:17778"
export SW_DPA_URL="https://your-dpa-server"
export SQL_SERVER="your-sql-server"
export SQL_DATABASE="your-reporting-db"
python your_ingestion_job.py --mode read-only --dry-run
```

Expected output:
```text
connection successful
records fetched: <n>
dry-run complete (no writes)
```

## Exit gate (must pass before level 9)
1. You can explain lineage from source to dashboard.
2. You can recover safely from timeout/auth/schema-drift failure.
3. You can prove idempotent reruns in your ETL flow.

## Primary Sources
- [MSSQL Python quickstart](https://learn.microsoft.com/en-us/sql/connect/python/mssql-python/python-sql-driver-mssql-python-quickstart?view=sql-server-ver17)
- [ODBC connection strings](https://learn.microsoft.com/en-us/sql/connect/odbc/dsn-connection-string-attribute?view=sql-server-ver17)
- [OrionSDK](https://github.com/solarwinds/OrionSDK)
- [DPA API docs](https://documentation.solarwinds.com/en/success_center/dpa/content/dpa-use-the-api.htm)
- [Streamlit get started](https://docs.streamlit.io/get-started)

## Optional Resources
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [python-oracledb docs](https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html)

## Next
Go to [31_LEVEL_9_TO_10_AND_BEYOND.md](./31_LEVEL_9_TO_10_AND_BEYOND.md).
