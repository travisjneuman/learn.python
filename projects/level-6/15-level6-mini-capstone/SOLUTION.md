# Solution: Level 6 / Project 15 - Level 6 Mini Capstone

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 15 — Mini Capstone: Full Database ETL Pipeline.

Combines all Level 6 skills into a single ETL pipeline: staging load,
validation, upsert, lineage tracking, incremental watermark, and
health metrics — all backed by SQLite.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

# WHY separate staging and target tables? -- Staging is a scratch area
# for raw ingest; target is the clean, deduplicated production table.
# This separation lets you validate and transform in staging without
# risking corruption of production data.
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

CREATE TABLE IF NOT EXISTS lineage (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    record_key TEXT NOT NULL,
    step       TEXT NOT NULL,
    detail     TEXT,
    created    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS watermarks (
    name  TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    status     TEXT NOT NULL,
    staged     INTEGER DEFAULT 0,
    loaded     INTEGER DEFAULT 0,
    rejected   INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    created    TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    # WHY executescript instead of execute? -- The SCHEMA_DDL contains
    # multiple CREATE TABLE statements. executescript handles multiple
    # semicolon-delimited statements in one call; execute() only
    # handles one statement at a time.
    conn.executescript(SCHEMA_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Watermark
# ---------------------------------------------------------------------------


def get_watermark(conn: sqlite3.Connection, name: str) -> str | None:
    """Read the current high-water mark.

    WHY return None for missing? -- First run has no watermark. None
    signals "load everything" to the caller, avoiding a special flag.
    """
    row = conn.execute("SELECT value FROM watermarks WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None


def set_watermark(conn: sqlite3.Connection, name: str, value: str) -> None:
    """Upsert the watermark value."""
    conn.execute(
        "INSERT INTO watermarks (name, value) VALUES (?, ?) "
        "ON CONFLICT(name) DO UPDATE SET value = excluded.value",
        (name, value),
    )


# ---------------------------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------------------------


@dataclass
class PipelineResult:
    staged: int = 0
    loaded: int = 0
    rejected: int = 0
    errors: list[str] = field(default_factory=list)


def validate_record(rec: dict) -> str | None:
    """Return error string if record is invalid.

    WHY validate all four fields? -- Each field is required by the target
    table schema. Catching missing/invalid fields here means the staging
    INSERT never fails with a database constraint error, which would be
    harder to diagnose.
    """
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


def stage_records(
    conn: sqlite3.Connection,
    records: list[dict],
    watermark: str | None,
) -> PipelineResult:
    """Validate and stage records, filtering by watermark.

    WHY combine watermark filtering and validation in one pass? -- Each
    record is touched exactly once. First we check the watermark (skip
    old data), then validate (route to dead-letters or staging). This
    single-pass design avoids iterating the data twice.
    """
    result = PipelineResult()

    for rec in records:
        ts = rec.get("ts", "")

        # WHY filter by watermark first? -- Skipping old records before
        # validation avoids dead-lettering records that are merely stale,
        # not actually invalid.
        if watermark and ts <= watermark:
            continue

        error = validate_record(rec)
        if error:
            conn.execute(
                "INSERT INTO dead_letters (raw, error) VALUES (?, ?)",
                (json.dumps(rec), error),
            )
            conn.execute(
                "INSERT INTO lineage (record_key, step, detail) VALUES (?, 'reject', ?)",
                (rec.get("key", "?"), error),
            )
            result.rejected += 1
            result.errors.append(f"{rec.get('key', '?')}: {error}")
            continue

        conn.execute(
            "INSERT INTO staging (key, name, value, ts) VALUES (?, ?, ?, ?)",
            (rec["key"], rec["name"], float(rec["value"]), ts),
        )
        conn.execute(
            "INSERT INTO lineage (record_key, step, detail) VALUES (?, 'stage', 'validated and staged')",
            (rec["key"],),
        )
        result.staged += 1

    conn.commit()
    return result


def load_to_target(conn: sqlite3.Connection) -> int:
    """Upsert staged records into the target table.

    WHY upsert (ON CONFLICT) instead of plain INSERT? -- The same key
    may appear in multiple runs. ON CONFLICT DO UPDATE merges the new
    data into the existing row, preserving the target as a deduplicated
    current-state table.
    """
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

    # WHY clear staging after load? -- Staging is a scratch area. If
    # we leave old rows, the next run's load_to_target would re-upsert
    # them unnecessarily (idempotent but wasteful).
    conn.execute("DELETE FROM staging")
    conn.commit()
    return loaded


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Full pipeline: read -> validate -> stage -> upsert -> track.

    WHY measure duration? -- The run_log table tracks how long each
    pipeline execution takes. Duration regressions (a run that used
    to take 200ms now takes 5000ms) are an early warning that
    something changed — data volume, missing indexes, etc.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    records = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)

        start = time.perf_counter()

        watermark = get_watermark(conn, "events_ts")
        stage_result = stage_records(conn, records, watermark)
        loaded = load_to_target(conn)
        stage_result.loaded = loaded

        # WHY set watermark from MAX(ts) in target? -- The target table
        # contains all successfully loaded records. Its max timestamp is
        # the authoritative watermark, even if some staged records had
        # higher timestamps but failed to load.
        max_ts = conn.execute("SELECT MAX(ts) FROM target").fetchone()[0]
        if max_ts:
            set_watermark(conn, "events_ts", max_ts)

        elapsed = int((time.perf_counter() - start) * 1000)

        # Log the run for health monitoring
        conn.execute(
            "INSERT INTO run_log (status, staged, loaded, rejected, duration_ms) "
            "VALUES (?, ?, ?, ?, ?)",
            ("success", stage_result.staged, loaded, stage_result.rejected, elapsed),
        )
        conn.commit()

        # Gather final stats
        target_count = conn.execute("SELECT COUNT(*) FROM target").fetchone()[0]
        dl_count = conn.execute("SELECT COUNT(*) FROM dead_letters").fetchone()[0]
        lineage_count = conn.execute("SELECT COUNT(*) FROM lineage").fetchone()[0]

    finally:
        conn.close()

    summary = {
        "input_records": len(records),
        "staged": stage_result.staged,
        "loaded": stage_result.loaded,
        "rejected": stage_result.rejected,
        "errors": stage_result.errors,
        "target_rows": target_count,
        "dead_letters": dl_count,
        "lineage_entries": lineage_count,
        "watermark": max_ts,
        "duration_ms": elapsed,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info(
        "capstone: staged=%d loaded=%d rejected=%d in %dms",
        stage_result.staged, loaded, stage_result.rejected, elapsed,
    )
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Level 6 Mini Capstone — full database ETL pipeline"
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
| Six tables in one schema (staging, target, dead_letters, lineage, watermarks, run_log) | Each table has a single responsibility; combining all Level 6 patterns into one cohesive pipeline | Fewer tables with merged concerns -- simpler schema but each table tries to do too much |
| Watermark filter before validation | Skipping stale records early avoids dead-lettering records that are merely old, not invalid | Validate first, then filter -- wastes effort validating records that will be skipped anyway |
| Staging table cleared after load | Prevents stale records from being re-upserted on the next run; staging is a scratch area | Keep staging as an archive -- useful for debugging but requires a separate cleanup strategy |
| run_log for pipeline execution history | Enables health monitoring (Project 12 pattern); duration tracking catches performance regressions | No logging -- simpler but you lose visibility into pipeline health over time |
| Single-pass pipeline (stage -> load -> watermark -> log) | Each step feeds the next; clear data flow with no circular dependencies | Multi-pass with intermediate files -- more resilient to crashes but much more complex |

## Alternative approaches

### Approach B: Conditional upsert (only update if newer timestamp)

```python
def load_to_target_conditional(conn: sqlite3.Connection) -> int:
    """Only overwrite target rows if the staged data is newer.

    Prevents stale data from overwriting fresher data when records
    arrive out of order across multiple pipeline runs.
    """
    rows = conn.execute("SELECT key, name, value, ts FROM staging").fetchall()
    loaded = 0

    for r in rows:
        key, name, value, ts = r
        conn.execute(
            "INSERT INTO target (key, name, value, ts) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "  name = excluded.name, "
            "  value = excluded.value, "
            "  ts = excluded.ts, "
            "  updated_at = datetime('now') "
            "WHERE excluded.ts > target.ts",  # only if newer
            (key, name, value, ts),
        )
        loaded += 1

    conn.execute("DELETE FROM staging")
    conn.commit()
    return loaded
```

**Trade-off:** The conditional upsert prevents stale data from overwriting newer data, which is critical when records arrive out of chronological order (common with distributed systems). The primary solution unconditionally overwrites, which is simpler but assumes records always arrive in order. In production, the conditional approach is strongly preferred.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| All records are rejected (100% failure rate) | `stage_records` returns `staged=0`; `load_to_target` processes zero rows; watermark does not advance; pipeline completes with no error | This is correct behavior -- but add a warning log when staged == 0 and rejected > 0 so operators notice |
| Corrupted watermark (set to a far-future date) | Every record is filtered out as "already loaded"; pipeline runs but loads nothing | Validate that the new watermark is reasonable; compare against the max timestamp in the source data |
| Running twice with `:memory:` database | The database is fresh each time (no persistence); watermark starts at None; every record is re-loaded | Use `--db data/pipeline.db` for persistent state across runs; `:memory:` is for testing only |
