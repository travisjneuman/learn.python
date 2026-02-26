# Solution: Level 6 / Project 02 - Staging Table Loader

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 02 — Staging Table Loader.

Loads CSV data into a SQLite staging table with row-level validation.
Invalid rows are logged and skipped without blocking the overall load.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

STAGING_DDL = """\
CREATE TABLE IF NOT EXISTS staging_events (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT    NOT NULL,
    level     TEXT    NOT NULL,
    source    TEXT    NOT NULL,
    message   TEXT    NOT NULL
);
"""

# WHY frozenset? -- Immutable and O(1) lookup. The set of valid levels
# never changes at runtime, so frozenset communicates "this is a constant"
# and prevents accidental mutation.
VALID_LEVELS = frozenset({"INFO", "WARN", "ERROR", "CRITICAL"})


@dataclass
class LoadResult:
    """Accumulates accept/reject counts during a load."""
    accepted: int = 0
    rejected: int = 0
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_row(row: dict, row_num: int) -> str | None:
    """Return an error string if *row* is invalid, else None.

    WHY validate in Python instead of relying on DB constraints alone? --
    Database constraints (NOT NULL, CHECK) catch errors at insert time but
    give you a generic OperationalError. Python-side validation lets you
    produce specific, human-readable error messages per field per row.
    """
    required = ("timestamp", "level", "source", "message")
    for col in required:
        value = row.get(col, "")
        if not value or not value.strip():
            return f"row={row_num} missing_field={col}"

    # WHY .upper()? -- Normalizes "warn", "Warn", "WARN" to one canonical
    # form so the check works regardless of source casing.
    if row["level"].strip().upper() not in VALID_LEVELS:
        return f"row={row_num} bad_level={row['level']}"

    return None


# ---------------------------------------------------------------------------
# CSV reader
# ---------------------------------------------------------------------------


def load_csv(path: Path) -> list[dict]:
    """Parse a CSV file into a list of row dictionaries.

    WHY csv.DictReader? -- It maps each row to a dict keyed by header
    names, so you access fields by name (row["level"]) instead of by
    index (row[1]). This makes the code self-documenting and resilient
    to column reordering in the source file.
    """
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Database loader
# ---------------------------------------------------------------------------


def create_staging_table(conn: sqlite3.Connection) -> None:
    """Ensure the staging table exists (idempotent via IF NOT EXISTS)."""
    conn.execute(STAGING_DDL)
    conn.commit()


def load_rows(conn: sqlite3.Connection, rows: list[dict]) -> LoadResult:
    """Insert valid rows into staging_events, skip invalid ones.

    WHY row-by-row instead of executemany? -- executemany is faster, but
    if ANY row fails the entire batch is aborted. Row-by-row lets us
    skip bad rows while keeping the good ones.
    """
    result = LoadResult()

    for idx, row in enumerate(rows, start=1):
        error = validate_row(row, idx)
        if error:
            result.rejected += 1
            result.errors.append(error)
            logging.warning("reject %s", error)
            continue

        # WHY .strip() on every value? -- CSV files often have trailing
        # whitespace or newlines. Stripping prevents " INFO" != "INFO"
        # mismatches and invisible data quality bugs.
        conn.execute(
            "INSERT INTO staging_events (timestamp, level, source, message) "
            "VALUES (?, ?, ?, ?)",
            (
                row["timestamp"].strip(),
                row["level"].strip().upper(),
                row["source"].strip(),
                row["message"].strip(),
            ),
        )
        result.accepted += 1

    conn.commit()
    return result


def count_staged(conn: sqlite3.Connection) -> int:
    """Return total row count in the staging table."""
    return conn.execute("SELECT COUNT(*) FROM staging_events").fetchone()[0]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Full pipeline: read CSV -> validate -> load staging -> write summary."""
    rows = load_csv(input_path)

    # WHY try/finally? -- Guarantees the connection is closed even if an
    # exception is thrown during loading. Leaked connections can lock the
    # database file and prevent other processes from accessing it.
    conn = sqlite3.connect(db_path)
    try:
        create_staging_table(conn)
        result = load_rows(conn, rows)
        total = count_staged(conn)
    finally:
        conn.close()

    summary = {
        "input_rows": len(rows),
        "accepted": result.accepted,
        "rejected": result.rejected,
        "errors": result.errors,
        "total_in_staging": total,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("load complete accepted=%d rejected=%d", result.accepted, result.rejected)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Staging Table Loader — CSV to SQLite with validation"
    )
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--db", default=":memory:")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output), db_path=args.db)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Row-by-row inserts instead of `executemany` | Allows skipping individual bad rows while keeping good ones in the same batch | `executemany` -- faster but all-or-nothing on failure |
| Python-side validation before SQL insert | Produces specific, per-field error messages the operator can act on | DB-only constraints (CHECK, NOT NULL) -- catches errors but gives generic messages |
| `frozenset` for `VALID_LEVELS` | Immutable constant with O(1) membership test; signals "do not modify" | A regular `set` -- mutable, could be accidentally changed at runtime |
| Staging table separate from final target | Staging is a scratch area; validates data before touching production tables | Direct insert into production -- simpler but risky if bad data slips through |

## Alternative approaches

### Approach B: Batch insert with SAVEPOINT per row

```python
def load_rows_savepoint(conn: sqlite3.Connection, rows: list[dict]) -> LoadResult:
    """Use SAVEPOINTs to get batch-like performance with row-level recovery."""
    result = LoadResult()
    for idx, row in enumerate(rows, start=1):
        sp = f"sp_row_{idx}"
        conn.execute(f"SAVEPOINT {sp}")
        try:
            conn.execute(
                "INSERT INTO staging_events (timestamp, level, source, message) "
                "VALUES (?, ?, ?, ?)",
                (row["timestamp"], row["level"], row["source"], row["message"]),
            )
            conn.execute(f"RELEASE {sp}")
            result.accepted += 1
        except (sqlite3.IntegrityError, KeyError) as exc:
            conn.execute(f"ROLLBACK TO {sp}")
            conn.execute(f"RELEASE {sp}")
            result.rejected += 1
            result.errors.append(f"row={idx} error={exc}")
    conn.commit()
    return result
```

**Trade-off:** SAVEPOINTs push validation to the database layer, which catches constraint violations Python might miss. However, the error messages are less specific, and the approach is more complex to debug. Better suited when you trust the DB schema to be the source of truth.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| CSV headers don't match expected column names | `row.get("level")` returns `None`; validation rejects every row with "missing_field" | Validate headers before processing: check that `reader.fieldnames` contains all required columns |
| Loading the same file twice | Duplicate rows accumulate because there is no uniqueness constraint | Add a content hash column or use an idempotency key (see Project 03) |
| Forgetting `newline=""` in `open()` | On Windows, `csv.reader` may misparse line endings and produce extra blank rows | Always pass `newline=""` to `open()` when using the `csv` module |
