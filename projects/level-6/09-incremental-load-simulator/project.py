"""Level 6 / Project 09 — Incremental Load Simulator.

Loads only new or changed records since the last run by tracking
a high-water mark (the latest timestamp already loaded).

Key concepts:
- High-water mark pattern for incremental loading
- Comparison: full load vs incremental load
- Watermark persistence in a metadata table
- Filtering source data by "modified_at > last_watermark"
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
    """Read the current high-water mark for a table."""
    row = conn.execute(
        "SELECT last_value FROM watermarks WHERE table_name = ?", (table,)
    ).fetchone()
    return row[0] if row else None


def set_watermark(conn: sqlite3.Connection, table: str, value: str) -> None:
    """Update (or insert) the high-water mark for a table."""
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

    Each record must have: id, name, modified_at (ISO string).
    """
    stats = LoadStats(total_source=len(source_records))
    watermark = get_watermark(conn, "events")

    # Sort by modified_at so we process in order
    sorted_records = sorted(source_records, key=lambda r: r["modified_at"])

    max_ts = watermark  # track the newest timestamp we load

    for rec in sorted_records:
        ts = rec["modified_at"]
        if watermark and ts <= watermark:
            stats.skipped += 1
            continue

        conn.execute(
            "INSERT OR REPLACE INTO events (id, name, modified_at) VALUES (?, ?, ?)",
            (rec["id"], rec["name"], ts),
        )
        stats.loaded += 1

        if max_ts is None or ts > max_ts:
            max_ts = ts

    conn.commit()

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
