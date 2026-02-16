# 06 — SQL Integration (Excel/Reports → Database → Reports/Dashboards)

## Goal
You will move from “report scripts” to “pipelines”:
- ingest spreadsheets
- clean + validate
- load into SQL
- query for reporting and dashboards

---

## SQL basics you must learn (in this order)
1. SELECT + WHERE
2. ORDER BY
3. GROUP BY + aggregates (COUNT/SUM/AVG)
4. JOIN (combine tables)
5. INSERT/UPDATE (write data)
6. Transactions (avoid partial writes)

---

## Python connectivity options
### Option A (common in enterprises): pyodbc
- Direct ODBC driver access to SQL Server.
- Good when you just need to connect and run SQL quickly.

### Option B (recommended long-term): SQLAlchemy
- Lets you write more maintainable code and swap DB backends.
- Strong tutorial path exists in official docs. citeturn1search2

Start with A if needed, but design your code so SQL is centralized and testable.

---

## Capstone B: Ingest + Transform + Load (ETL)

### Tables
- `staging_alerts` (raw ingest)
- `alerts` (cleaned reporting table)

### Workflow
1. Read Excel/CSV output from Capstone A
2. Validate + normalize (same rules as before)
3. Insert into staging
4. Promote to reporting table (dedupe by idempotency key)
5. Generate a “daily summary” query output

### Idempotency key (critical)
If you ingest the same row twice, you should not duplicate it.
A common key:
- hash(Customer + Site + TicketID + Opened)

---

## Dashboard readiness
Once data is in SQL:
- dashboards and reports query SQL (fast, stable)
- SolarWinds can be polled less frequently; SQL becomes your cache

Next: **[07_SOLARWINDS_ORION.md](./07_SOLARWINDS_ORION.md)**
