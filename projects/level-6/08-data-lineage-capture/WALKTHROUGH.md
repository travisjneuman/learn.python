# Data Lineage Capture — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to build a system that tracks every transformation a data record passes through, so you can trace any output row back to its original source. If you can insert records into a SQLite table and link them with a `parent_id` column, you already have the key insight.

## Thinking Process

Imagine you receive a report that says a customer was charged the wrong amount. You need to answer: where did this number come from? Was it the raw input, or was it changed during normalization, or during the publish step? Data lineage answers this question by recording a breadcrumb trail at every transformation step.

The mental model is a linked list stored in a database. Each step in the pipeline creates a lineage record that points back to the previous step's record via `parent_id`. The ingest step has no parent (it is the root). The normalize step links to the ingest record. The publish step links to the normalize record. To trace the full history, you follow the `parent_id` chain backwards.

The key design decision is separating the business logic (actually transforming data) from the lineage recording (writing metadata about what happened). Each pipeline step does its work AND records a lineage entry. This separation means you could change the transformation logic without breaking the audit trail, or add new pipeline steps without modifying the lineage infrastructure.

## Step 1: Define the Database Schema

**What to do:** Write SQL DDL statements for two tables: `lineage` (tracks the transformation chain) and `processed_data` (stores the actual data at each stage).

**Why:** The `lineage` table is the audit trail. Its `parent_id` column creates a linked chain from the final output back to the original input. The `processed_data` table stores what the data looked like at each stage, while lineage stores metadata about what happened.

```python
LINEAGE_DDL = """\
CREATE TABLE IF NOT EXISTS lineage (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    record_key     TEXT NOT NULL,
    step_name      TEXT NOT NULL,
    source         TEXT NOT NULL,
    destination    TEXT NOT NULL,
    transform_desc TEXT,
    parent_id      INTEGER,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

DATA_DDL = """\
CREATE TABLE IF NOT EXISTS processed_data (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    key   TEXT NOT NULL,
    value TEXT NOT NULL,
    stage TEXT NOT NULL
);
"""
```

**Predict:** Why does the `lineage` table have `parent_id` as a nullable column? Which lineage records will have `parent_id = NULL`?

## Step 2: Create the Lineage Entry Dataclass and Recording Function

**What to do:** Define a `LineageEntry` dataclass to hold the metadata for one step, then write a `record_lineage()` function that inserts it into the database and returns the new row's ID.

**Why:** The dataclass gives you a typed container so you cannot accidentally swap the `source` and `destination` arguments. Returning the `lastrowid` is critical because the next step needs it as its `parent_id`.

```python
@dataclass
class LineageEntry:
    record_key: str
    step_name: str
    source: str
    destination: str
    transform_desc: str = ""
    parent_id: int | None = None

def record_lineage(conn: sqlite3.Connection, entry: LineageEntry) -> int:
    cur = conn.execute(
        "INSERT INTO lineage (record_key, step_name, source, destination, "
        "transform_desc, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
        (entry.record_key, entry.step_name, entry.source,
         entry.destination, entry.transform_desc, entry.parent_id),
    )
    conn.commit()
    return cur.lastrowid
```

**Predict:** What does `cur.lastrowid` return? Why is it important to capture this value rather than querying the table for the max ID afterwards?

## Step 3: Build the Ingest Step (Root of the Chain)

**What to do:** Write `step_ingest()` that takes raw records, inserts them into `processed_data` with stage `'raw'`, and records a lineage entry with no parent.

**Why:** The ingest step is the starting point of every lineage chain. Since there is no previous step, `parent_id` is `None`. Every subsequent step will link back to this root.

```python
def step_ingest(conn: sqlite3.Connection, records: list[dict]) -> list[dict]:
    results = []
    for rec in records:
        key = rec.get("key", "unknown")
        conn.execute(
            "INSERT INTO processed_data (key, value, stage) VALUES (?, ?, 'raw')",
            (key, json.dumps(rec)),
        )
        lid = record_lineage(conn, LineageEntry(
            record_key=key, step_name="ingest",
            source="input_file", destination="staging",
            transform_desc="raw ingest, no transformation",
        ))
        results.append({"key": key, "lineage_id": lid, "stage": "raw"})
    conn.commit()
    return results
```

**Predict:** If you have 3 input records, how many rows will be in the `lineage` table after this step completes?

## Step 4: Build the Normalize Step (Chaining via parent_id)

**What to do:** Write `step_normalize()` that transforms data (lowercase keys, strip whitespace), inserts into `processed_data` with stage `'normalized'`, and records a lineage entry that links to the previous step.

**Why:** This is where the chain forms. Before recording lineage, you query `get_lineage_chain()` to find the most recent lineage entry for this record, then use its ID as your `parent_id`. This creates the backward link.

```python
def step_normalize(conn: sqlite3.Connection, records: list[dict]) -> list[dict]:
    results = []
    for rec in records:
        key = rec["key"]
        normalized_value = json.dumps({k.lower().strip(): v for k, v in rec.items()})
        conn.execute(
            "INSERT INTO processed_data (key, value, stage) VALUES (?, ?, 'normalized')",
            (key, normalized_value),
        )
        # Look up the previous step's lineage ID to create the chain
        parent_chain = get_lineage_chain(conn, key)
        parent_id = parent_chain[-1]["id"] if parent_chain else None

        lid = record_lineage(conn, LineageEntry(
            record_key=key, step_name="normalize",
            source="staging", destination="normalized",
            transform_desc="lowercase keys, strip whitespace",
            parent_id=parent_id,
        ))
        results.append({"key": key, "lineage_id": lid, "stage": "normalized"})
    conn.commit()
    return results
```

**Predict:** After both ingest and normalize run on 3 records, how many rows are in the `lineage` table? What does the `parent_id` of each normalize entry point to?

## Step 5: Build the Publish Step and Query Function

**What to do:** Write `step_publish()` following the same pattern as normalize (chain lineage via parent_id). Write `get_lineage_chain()` to retrieve all lineage entries for a given record key, ordered by ID.

**Why:** The publish step completes the chain: ingest -> normalize -> publish. The `get_lineage_chain()` function is what makes lineage useful. Given any record key, it returns the full audit trail showing every transformation that record went through.

```python
def get_lineage_chain(conn: sqlite3.Connection, record_key: str) -> list[dict]:
    rows = conn.execute(
        "SELECT id, step_name, source, destination, transform_desc, parent_id, created_at "
        "FROM lineage WHERE record_key = ? ORDER BY id",
        (record_key,),
    ).fetchall()
    return [
        {"id": r[0], "step": r[1], "source": r[2], "destination": r[3],
         "transform": r[4], "parent_id": r[5], "created_at": r[6]}
        for r in rows
    ]
```

**Predict:** For a record with key `"order-101"`, what would the lineage chain look like? How many entries, and what are their step names?

## Step 6: Orchestrate the Full Pipeline

**What to do:** Write a `run()` function that loads input records from a JSON file, runs all three pipeline steps in order, builds a lineage report for each record, and writes a JSON summary.

**Why:** The orchestrator proves the pipeline works end-to-end. The output shows you the total number of lineage entries and the full chain for each record, which you can use to verify that the parent_id links are correct.

```python
def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    records = json.loads(input_path.read_text(encoding="utf-8"))
    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        step_ingest(conn, records)
        step_normalize(conn, records)
        step_publish(conn, records)

        lineage_report = {}
        for rec in records:
            key = rec.get("key", "unknown")
            lineage_report[key] = get_lineage_chain(conn, key)

        total_lineage = conn.execute("SELECT COUNT(*) FROM lineage").fetchone()[0]
    finally:
        conn.close()

    summary = {
        "records_processed": len(records),
        "pipeline_steps": 3,
        "total_lineage_entries": total_lineage,
        "lineage": lineage_report,
    }
    output_path.write_text(json.dumps(summary, indent=2))
    return summary
```

**Predict:** With 3 input records and 3 pipeline steps, what should `total_lineage_entries` be? (3 records x 3 steps = ?)

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Forgetting to pass `parent_id` when recording lineage | Each step works independently, so it is easy to forget to look up the previous step | Always query `get_lineage_chain()` before recording, and use the last entry's ID |
| Using the wrong key to look up lineage | If you use `rec["id"]` instead of `rec["key"]`, the chain breaks | Be consistent: always use the `record_key` field |
| Not committing after each step | Without `conn.commit()`, the lineage records from step 1 are invisible to step 2's queries | Call `conn.commit()` at the end of each step function |
| Processing records in a different order across steps | If ingest processes records A, B, C but normalize processes C, B, A, the parent_id links could get confused | Use `ORDER BY id` in queries to ensure consistent ordering |

## Testing Your Solution

```bash
pytest -q
```

You should see 6+ tests pass. The tests verify that lineage entries are created with correct parent chains, that the full pipeline runs end-to-end, and that the output JSON has the expected structure.

## What You Learned

- **Data lineage** creates an audit trail that lets you trace any output row back through every transformation to its original source. This is not optional in regulated industries (finance, healthcare) where you must prove where every number came from.
- **parent_id chains** in a database table create a linked list structure. Each record points to its predecessor, forming a traceable path. This same pattern appears in git commits, file system directories, and comment threads.
- **Separating business logic from metadata recording** keeps your pipeline functions clean. Each step does its transformation work AND records what it did, but the lineage infrastructure is reusable across any pipeline.
