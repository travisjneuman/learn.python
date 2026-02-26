# Solution: Level 6 / Project 08 - Data Lineage Capture

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 08 — Data Lineage Capture.

Tracks data transformations in a SQLite lineage table so you can
trace any output row back to its source and see every step it
went through.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

# WHY a separate lineage table? -- Lineage metadata (who changed what,
# when, and why) lives apart from the data itself. This separation
# means you can query lineage without touching production tables, and
# lineage survives even if the data table is rebuilt.
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


def init_db(conn: sqlite3.Connection) -> None:
    """Create both tables. Idempotent via IF NOT EXISTS."""
    conn.execute(LINEAGE_DDL)
    conn.execute(DATA_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Lineage recording
# ---------------------------------------------------------------------------


@dataclass
class LineageEntry:
    record_key: str
    step_name: str
    source: str
    destination: str
    transform_desc: str = ""
    parent_id: int | None = None


def record_lineage(conn: sqlite3.Connection, entry: LineageEntry) -> int:
    """Insert a lineage record and return its ID.

    WHY return the ID? -- Each step's lineage ID becomes the parent_id
    for the next step, forming a chain. Without the returned ID, we
    would need an extra SELECT to find the parent.
    """
    cur = conn.execute(
        "INSERT INTO lineage (record_key, step_name, source, destination, "
        "transform_desc, parent_id) VALUES (?, ?, ?, ?, ?, ?)",
        (entry.record_key, entry.step_name, entry.source,
         entry.destination, entry.transform_desc, entry.parent_id),
    )
    conn.commit()
    return cur.lastrowid


def get_lineage_chain(conn: sqlite3.Connection, record_key: str) -> list[dict]:
    """Retrieve the full lineage chain for a given record key.

    WHY ORDER BY id? -- Lineage IDs are auto-incrementing, so ordering
    by ID gives chronological order: ingest -> normalize -> publish.
    """
    rows = conn.execute(
        "SELECT id, step_name, source, destination, transform_desc, parent_id, created_at "
        "FROM lineage WHERE record_key = ? ORDER BY id",
        (record_key,),
    ).fetchall()
    return [
        {
            "id": r[0], "step": r[1], "source": r[2], "destination": r[3],
            "transform": r[4], "parent_id": r[5], "created_at": r[6],
        }
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Simulated pipeline steps
# ---------------------------------------------------------------------------


def step_ingest(conn: sqlite3.Connection, records: list[dict]) -> list[dict]:
    """Step 1: Ingest raw records into the staging area.

    WHY a separate ingest step? -- Capturing the raw data exactly as it
    arrived (before any transformations) provides a baseline. If
    downstream steps produce wrong results, you can compare against
    the raw ingest to find where the error was introduced.
    """
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


def step_normalize(conn: sqlite3.Connection, records: list[dict]) -> list[dict]:
    """Step 2: Normalize values (lowercase keys, strip whitespace).

    WHY chain lineage via parent_id? -- Each step links back to the
    previous step's lineage record, forming a traceable chain. This
    lets you answer "where did this output row come from?" by walking
    the parent_id links back to the original ingestion.
    """
    results = []
    for rec in records:
        key = rec["key"]
        normalized_value = json.dumps({k.lower().strip(): v for k, v in rec.items()})

        conn.execute(
            "INSERT INTO processed_data (key, value, stage) VALUES (?, ?, 'normalized')",
            (key, normalized_value),
        )
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


def step_publish(conn: sqlite3.Connection, records: list[dict]) -> list[dict]:
    """Step 3: Mark records as published (final stage).

    WHY a publish step? -- In real pipelines, publishing means writing
    to the production table or external system. Recording this as a
    lineage step proves the record made it all the way through.
    """
    results = []
    for rec in records:
        key = rec["key"]
        conn.execute(
            "INSERT INTO processed_data (key, value, stage) VALUES (?, ?, 'published')",
            (key, json.dumps({"key": key, "status": "published"})),
        )
        parent_chain = get_lineage_chain(conn, key)
        parent_id = parent_chain[-1]["id"] if parent_chain else None

        lid = record_lineage(conn, LineageEntry(
            record_key=key, step_name="publish",
            source="normalized", destination="output",
            transform_desc="final publish",
            parent_id=parent_id,
        ))
        results.append({"key": key, "lineage_id": lid, "stage": "published"})
    conn.commit()
    return results


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    records = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)

        step_ingest(conn, records)
        step_normalize(conn, records)
        step_publish(conn, records)

        # Build lineage report
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("lineage captured: %d records, %d entries", len(records), total_lineage)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Data Lineage Capture — track every transformation step"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| parent_id linking between lineage entries | Creates a traceable chain from output back to source; enables "where did this row come from?" queries | Flat log (no parent link) -- simpler but you lose the ability to trace a single record's journey through the pipeline |
| Separate lineage table from data table | Lineage metadata lives independently; survives table rebuilds and can be queried without touching production data | Inline lineage columns on data table -- mixes concerns; lineage bloats every data query |
| One lineage record per step per record | Fine-grained traceability; you can see exactly which step a record reached before failure | One record per pipeline run -- cheaper but no per-record visibility |
| `get_lineage_chain` fetches by record_key | Natural query pattern: "show me everything that happened to order-101" | Fetch by parent_id (recursive walk) -- more elegant for complex DAGs but overkill for a linear pipeline |

## Alternative approaches

### Approach B: Recursive CTE for lineage traversal

```python
def trace_lineage_recursive(conn: sqlite3.Connection, lineage_id: int) -> list[dict]:
    """Walk the parent_id chain using a recursive CTE.

    This approach follows the chain from any entry back to its root,
    even if you only know the final lineage ID.
    """
    rows = conn.execute("""
        WITH RECURSIVE chain AS (
            SELECT id, record_key, step_name, parent_id, transform_desc
            FROM lineage WHERE id = ?
            UNION ALL
            SELECT l.id, l.record_key, l.step_name, l.parent_id, l.transform_desc
            FROM lineage l INNER JOIN chain c ON l.id = c.parent_id
        )
        SELECT * FROM chain ORDER BY id
    """, (lineage_id,)).fetchall()
    return [{"id": r[0], "key": r[1], "step": r[2], "parent": r[3]} for r in rows]
```

**Trade-off:** Recursive CTEs can trace arbitrarily deep chains from any starting point, which is powerful for complex DAG-shaped pipelines. However, they are harder to understand and debug. The simple `WHERE record_key = ? ORDER BY id` approach works perfectly for linear pipelines.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Processing the same records twice | Lineage entries are duplicated (ingest appears twice) with no way to distinguish runs | Add a `run_id` column to lineage, or check for existing entries before recording |
| Missing `key` field in a record | `rec.get("key", "unknown")` stores lineage under "unknown", making it impossible to trace back to the source record | Validate that every record has a `key` field before entering the pipeline |
| Skipping the normalize step | Lineage chain has a gap (ingest -> publish); publish's parent_id points to ingest, which is correct but the gap is invisible unless you check step counts | Add a lineage integrity check that verifies every record has entries for all expected steps |
