# Level 6 Mini Capstone — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone combines everything from Level 6 into a single ETL pipeline: staging, validation, upsert, lineage tracking, watermarking, and dead-letter handling. If you have completed projects 01-14 in this level, you already know each piece individually. The challenge here is wiring them together into one coherent system.

## Thinking Process

Think of this project as building a small data warehouse. Real data pipelines face a messy reality: some input records are invalid, some have already been processed before, and the pipeline might run multiple times on the same data. You need to handle all of this gracefully.

The pipeline flows through distinct stages, each with a specific job. First, you read records and check the watermark to skip already-processed data. Then you validate each record: good ones go to staging, bad ones go to the dead-letter table with an explanation of what went wrong. Staged records get upserted into the target table (insert if new, update if existing). Finally, the watermark advances so the next run knows where you left off. At every step, lineage records track what happened to each record.

The key insight is that these are not independent features bolted together at random. They form a deliberate sequence where each stage protects the next. Validation prevents garbage from reaching the target table. The watermark prevents duplicate processing. The dead-letter table preserves rejected records for inspection instead of silently dropping them. Lineage gives you visibility into what happened and why. Removing any one of these stages creates a specific vulnerability.

## Step 1: Define the Database Schema

**What to do:** Create six tables: `staging` (temporary holding area), `target` (clean production data), `dead_letters` (rejected records), `lineage` (audit trail), `watermarks` (incremental position tracking), and `run_log` (pipeline execution history).

**Why:** Each table serves a distinct purpose. The staging/target separation means raw data never touches production tables directly. Dead letters preserve rejected records instead of losing them. Watermarks enable incremental processing so you do not reprocess the entire dataset every time.

```python
SCHEMA_DDL = """\
CREATE TABLE IF NOT EXISTS staging (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    key  TEXT NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    ts   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS target (
    key        TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    value      REAL NOT NULL,
    ts         TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS dead_letters (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    raw     TEXT NOT NULL,
    error   TEXT NOT NULL,
    created TEXT NOT NULL DEFAULT (datetime('now'))
);
-- Plus lineage, watermarks, and run_log tables
"""
```

**Predict:** Why does the `target` table use `key TEXT PRIMARY KEY` while `staging` uses `id INTEGER PRIMARY KEY AUTOINCREMENT`? What does this tell you about the difference between staging and target?

## Step 2: Build the Validation and Staging Function

**What to do:** Write `validate_record()` to check required fields and `stage_records()` to process each record: skip records older than the watermark, validate remaining records, stage good ones, and send bad ones to the dead-letter table.

**Why:** This is the gatekeeper. It makes three decisions per record: (1) Is it already processed? Skip via watermark. (2) Is it valid? Stage it. (3) Is it invalid? Dead-letter it with a reason. Every decision is also recorded in the lineage table.

```python
def validate_record(rec: dict) -> str | None:
    """Return error string if record is invalid, None if valid."""
    if not rec.get("key", "").strip():
        return "missing_key"
    if not rec.get("name", "").strip():
        return "missing_name"
    try:
        float(rec["value"])
    except (KeyError, ValueError, TypeError):
        return "invalid_value"
    if not rec.get("ts", "").strip():
        return "missing_timestamp"
    return None

def stage_records(conn, records, watermark):
    result = PipelineResult()
    for rec in records:
        ts = rec.get("ts", "")
        if watermark and ts <= watermark:
            continue  # already processed in a previous run
        error = validate_record(rec)
        if error:
            # Send to dead-letter table with error reason
            conn.execute("INSERT INTO dead_letters (raw, error) VALUES (?, ?)",
                        (json.dumps(rec), error))
            result.rejected += 1
            continue
        # Stage the valid record
        conn.execute("INSERT INTO staging (key, name, value, ts) VALUES (?, ?, ?, ?)",
                    (rec["key"], rec["name"], float(rec["value"]), ts))
        result.staged += 1
    conn.commit()
    return result
```

**Predict:** If the watermark is `"2025-01-10T00:00:00"` and a record has timestamp `"2025-01-10T00:00:00"` (exactly equal), is it processed or skipped? Look at the `<=` comparison carefully.

## Step 3: Build the Upsert Load Function

**What to do:** Write `load_to_target()` that reads all staged records and upserts them into the target table using SQLite's `INSERT ... ON CONFLICT DO UPDATE` syntax. After loading, clear the staging table.

**Why:** Upsert means "insert if the key is new, update if it already exists." This makes the pipeline idempotent: running it twice on the same data produces the same result. The staging table is cleared after loading because it is a scratch area, not permanent storage.

```python
def load_to_target(conn: sqlite3.Connection) -> int:
    rows = conn.execute("SELECT key, name, value, ts FROM staging").fetchall()
    loaded = 0
    for r in rows:
        conn.execute(
            "INSERT INTO target (key, name, value, ts) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "name = excluded.name, value = excluded.value, "
            "ts = excluded.ts, updated_at = datetime('now')",
            (r[0], r[1], r[2], r[3]),
        )
        conn.execute(
            "INSERT INTO lineage (record_key, step, detail) VALUES (?, 'load', 'upserted to target')",
            (r[0],),
        )
        loaded += 1
    conn.execute("DELETE FROM staging")
    conn.commit()
    return loaded
```

**Predict:** What does `excluded.name` mean in the `ON CONFLICT` clause? (Hint: `excluded` refers to the row that would have been inserted if there was no conflict.)

## Step 4: Implement Watermark Management

**What to do:** Write `get_watermark()` and `set_watermark()` functions that read and update a named watermark value in the `watermarks` table.

**Why:** The watermark is how the pipeline remembers its progress. After processing, you set the watermark to the maximum timestamp seen. On the next run, any records with timestamps at or before the watermark are skipped. This enables incremental processing: only new data gets processed.

```python
def get_watermark(conn, name):
    row = conn.execute("SELECT value FROM watermarks WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None

def set_watermark(conn, name, value):
    conn.execute(
        "INSERT INTO watermarks (name, value) VALUES (?, ?) "
        "ON CONFLICT(name) DO UPDATE SET value = excluded.value",
        (name, value),
    )
```

**Predict:** If you corrupt the watermark to a far-future date like `"2099-01-01"`, what happens on the next pipeline run? Would any records pass the watermark filter?

## Step 5: Wire the Orchestrator Together

**What to do:** Write the `run()` function that executes the full pipeline: load input, initialize the database, get the current watermark, stage records, load to target, update the watermark, log the run, and write the output summary.

**Why:** The orchestrator is where all the individual pieces come together. The order matters: watermark check must happen before staging (to skip old records), staging must happen before loading (to validate first), and watermark update must happen after loading (to record the new position).

```python
def run(input_path, output_path, db_path=":memory:"):
    records = json.loads(input_path.read_text())
    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        watermark = get_watermark(conn, "events_ts")
        stage_result = stage_records(conn, records, watermark)
        loaded = load_to_target(conn)

        max_ts = conn.execute("SELECT MAX(ts) FROM target").fetchone()[0]
        if max_ts:
            set_watermark(conn, "events_ts", max_ts)

        # Log the run for auditability
        conn.execute(
            "INSERT INTO run_log (status, staged, loaded, rejected) VALUES (?, ?, ?, ?)",
            ("success", stage_result.staged, loaded, stage_result.rejected),
        )
        conn.commit()
    finally:
        conn.close()
    # ... build and write summary
```

**Predict:** If you run this pipeline twice with the same input file and a persistent database (not `:memory:`), what happens on the second run? How many records get staged?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using `:memory:` for testing incremental behavior | In-memory databases disappear when the connection closes, so watermarks are lost | Use a file-based database path to test watermark persistence across runs |
| Forgetting to clear staging after load | Old staged records accumulate and get reloaded on every run | Always `DELETE FROM staging` after the upsert step completes |
| Not handling all-rejection batches | If every record is invalid, `staged` and `loaded` are both 0, which can cause issues if downstream code assumes at least one record | Check for `staged == 0` and handle it gracefully (the pipeline should still succeed) |
| Comparing timestamps as strings without consistent formatting | `"2025-1-5"` sorts differently than `"2025-01-05"` as strings | Ensure all timestamps use ISO 8601 format with zero-padding (`YYYY-MM-DDTHH:MM:SS`) |

## Testing Your Solution

```bash
pytest -q
```

You should see 6+ tests pass. The tests verify validation logic, watermark-based filtering, upsert behavior, dead-letter recording, and the full pipeline end-to-end.

## What You Learned

- **ETL pipelines** (Extract, Transform, Load) are the backbone of data engineering. The staging-validation-upsert pattern used here is the same pattern used in production data warehouses processing billions of rows.
- **Watermarks** enable incremental processing by remembering how far the pipeline has progressed. Without them, you would need to reprocess all data from scratch on every run, which becomes impossibly slow as datasets grow.
- **Dead-letter tables** preserve rejected records with their error reasons instead of silently dropping them. This is essential for debugging: when a stakeholder asks "why is this record missing from the report?", you can check the dead-letter table for the answer.
