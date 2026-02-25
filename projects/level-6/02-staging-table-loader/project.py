"""Level 6 / Project 02 — Staging Table Loader.

Loads CSV data into a SQLite staging table with row-level validation.
Invalid rows are logged and skipped without blocking the overall load.

Key concepts:
- csv.DictReader for parsing structured text files
- CREATE TABLE with column constraints (NOT NULL, CHECK)
- executemany vs. row-by-row inserts (and why we choose row-by-row here)
- Row-level validation: reject bad rows, keep the rest
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

    Checks every required column is present and non-empty, and that the
    level value is one of the known constants.
    """
    required = ("timestamp", "level", "source", "message")
    for col in required:
        value = row.get(col, "")
        if not value or not value.strip():
            return f"row={row_num} missing_field={col}"

    if row["level"].strip().upper() not in VALID_LEVELS:
        return f"row={row_num} bad_level={row['level']}"

    return None


# ---------------------------------------------------------------------------
# CSV reader
# ---------------------------------------------------------------------------


def load_csv(path: Path) -> list[dict]:
    """Parse a CSV file into a list of row dictionaries."""
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Database loader
# ---------------------------------------------------------------------------


def create_staging_table(conn: sqlite3.Connection) -> None:
    """Ensure the staging table exists (idempotent)."""
    conn.execute(STAGING_DDL)
    conn.commit()


def load_rows(conn: sqlite3.Connection, rows: list[dict]) -> LoadResult:
    """Insert valid rows into staging_events, skip invalid ones.

    We insert row-by-row (not executemany) so that one bad row does not
    abort the entire batch.  In production you might use a savepoint per
    row for even finer control.
    """
    result = LoadResult()

    for idx, row in enumerate(rows, start=1):
        error = validate_row(row, idx)
        if error:
            result.rejected += 1
            result.errors.append(error)
            logging.warning("reject %s", error)
            continue

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
    """Full pipeline: read CSV → validate → load staging → write summary."""
    rows = load_csv(input_path)

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
