# Solution: Level 6 / Project 09 - Incremental Load Simulator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 09 — Incremental Load Simulator.

Loads only new or changed records since the last run by tracking
a high-water mark (the latest timestamp already loaded).
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

TARGET_DDL = """\
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    modified_at TEXT NOT NULL
);
"""

# WHY a separate watermark table? -- Storing the "last loaded timestamp"
# in its own table decouples load tracking from the data itself. This
# means the watermark survives even if the target table is rebuilt, and
# multiple tables can each track their own watermark independently.
WATERMARK_DDL = """\
CREATE TABLE IF NOT EXISTS watermarks (
    table_name TEXT PRIMARY KEY,
    last_value TEXT NOT NULL
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(TARGET_DDL)
    conn.execute(WATERMARK_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Watermark management
# ---------------------------------------------------------------------------


def get_watermark(conn: sqlite3.Connection, table: str) -> str | None:
    """Read the current high-water mark for a table.

    WHY return None for missing watermarks? -- On the very first run,
    no watermark exists. Returning None signals "load everything" to
    the caller, avoiding a special "first run" flag.
    """
    row = conn.execute(
        "SELECT last_value FROM watermarks WHERE table_name = ?", (table,)
    ).fetchone()
    return row[0] if row else None


def set_watermark(conn: sqlite3.Connection, table: str, value: str) -> None:
    """Update (or insert) the high-water mark for a table.

    WHY ON CONFLICT DO UPDATE? -- Upsert pattern: inserts on first run,
    updates on subsequent runs. One statement handles both cases
    atomically, with no check-then-insert race condition.
    """
    conn.execute(
        "INSERT INTO watermarks (table_name, last_value) VALUES (?, ?) "
        "ON CONFLICT(table_name) DO UPDATE SET last_value = excluded.last_value",
        (table, value),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Loading logic
# ---------------------------------------------------------------------------


@dataclass
class LoadStats:
    total_source: int = 0
    loaded: int = 0
    skipped: int = 0
    new_watermark: str | None = None


def incremental_load(
    conn: sqlite3.Connection,
    source_records: list[dict],
) -> LoadStats:
    """Load records whose modified_at is newer than the current watermark.

    WHY sort by modified_at first? -- Sorting ensures we process records
    chronologically. This matters because the watermark advances to the
    maximum timestamp we load. Processing out of order is fine for
    correctness, but sorting makes the watermark progression predictable.
    """
    stats = LoadStats(total_source=len(source_records))
    watermark = get_watermark(conn, "events")

    sorted_records = sorted(source_records, key=lambda r: r["modified_at"])

    max_ts = watermark  # track the newest timestamp we load

    for rec in sorted_records:
        ts = rec["modified_at"]
        # WHY <= instead of <? -- Using <= means records at exactly
        # the watermark timestamp are skipped (already loaded). This
        # prevents re-processing the last loaded record on every run.
        # The trade-off: if two records share the exact same timestamp,
        # only the first one loaded will be kept.
        if watermark and ts <= watermark:
            stats.skipped += 1
            continue

        # WHY INSERT OR REPLACE? -- If a record ID already exists with
        # an older timestamp, we overwrite it with the newer version.
        # This handles both new inserts and updates in one statement.
        conn.execute(
            "INSERT OR REPLACE INTO events (id, name, modified_at) VALUES (?, ?, ?)",
            (rec["id"], rec["name"], ts),
        )
        stats.loaded += 1

        if max_ts is None or ts > max_ts:
            max_ts = ts

    conn.commit()

    # WHY only update watermark if it changed? -- If all records were
    # skipped, the watermark stays the same. Unnecessary writes would
    # bloat the WAL log in a real system.
    if max_ts and max_ts != watermark:
        set_watermark(conn, "events", max_ts)
        stats.new_watermark = max_ts

    return stats


def count_events(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    source_records = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        old_watermark = get_watermark(conn, "events")
        stats = incremental_load(conn, source_records)
        total = count_events(conn)
    finally:
        conn.close()

    summary = {
        "source_records": stats.total_source,
        "loaded": stats.loaded,
        "skipped": stats.skipped,
        "previous_watermark": old_watermark,
        "new_watermark": stats.new_watermark,
        "total_in_target": total,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("incremental load: loaded=%d skipped=%d", stats.loaded, stats.skipped)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Incremental Load Simulator — high-water mark pattern"
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
| Separate watermarks table | Decouples load state from data; multiple tables can track independent watermarks; survives data table rebuilds | Store watermark in a file -- simpler but not atomic with the data transaction |
| `<=` comparison (skip records at or before watermark) | Prevents re-loading the last record on every run | `<` comparison -- would re-load records at exactly the watermark, causing duplicates unless you also dedup |
| Sort source records by modified_at | Ensures chronological processing and predictable watermark progression | Unsorted -- the max_ts tracking still works, but debugging is harder |
| ON CONFLICT upsert for watermark | Handles first-run (INSERT) and subsequent runs (UPDATE) in one atomic statement | Check-then-insert -- two queries with a race condition window |

## Alternative approaches

### Approach B: Change Data Capture (CDC) with row hashing

```python
import hashlib

def load_with_change_detection(
    conn: sqlite3.Connection,
    source_records: list[dict],
) -> LoadStats:
    """Detect changes by comparing row hashes, not timestamps."""
    stats = LoadStats(total_source=len(source_records))

    for rec in source_records:
        row_hash = hashlib.sha256(
            json.dumps(rec, sort_keys=True).encode()
        ).hexdigest()

        existing = conn.execute(
            "SELECT row_hash FROM events WHERE id = ?", (rec["id"],)
        ).fetchone()

        if existing and existing[0] == row_hash:
            stats.skipped += 1  # no change
            continue

        conn.execute(
            "INSERT OR REPLACE INTO events (id, name, modified_at, row_hash) "
            "VALUES (?, ?, ?, ?)",
            (rec["id"], rec["name"], rec["modified_at"], row_hash),
        )
        stats.loaded += 1

    conn.commit()
    return stats
```

**Trade-off:** Hash-based CDC detects changes even when timestamps are missing or unreliable, which is common with legacy sources. But it requires reading the existing hash for every row (SELECT per record), which is slower than a simple watermark comparison. Best used when the source system does not reliably track modification times.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Late-arriving data (timestamp older than watermark) | The record is silently skipped and never loaded -- data loss | Use a "lookback window": set the filter to `watermark - N minutes` to catch late arrivals |
| Corrupted or reset watermark | Next run treats everything as new; full table reload plus potential duplicates if REPLACE is not used | Store watermark backups; validate that the new watermark is always >= the old one |
| Records with identical timestamps | The `<=` filter may skip legitimate new records that share the watermark timestamp | Use a composite watermark (timestamp + sequence ID) or switch to `<` with deduplication |
