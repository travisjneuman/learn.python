"""Level 6 / Project 15 — Mini Capstone: Full Database ETL Pipeline.

Combines all Level 6 skills into a single ETL pipeline: staging load,
validation, upsert, lineage tracking, incremental watermark, and
health metrics — all backed by SQLite.

Key concepts:
- Multi-stage ETL: extract → validate → load → publish
- Combining patterns: staging, upsert, lineage, watermark, dead-letter
- Transaction safety across the full pipeline
- Generating a consolidated run report
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

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
    conn.executescript(SCHEMA_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Watermark
# ---------------------------------------------------------------------------


def get_watermark(conn: sqlite3.Connection, name: str) -> str | None:
    row = conn.execute("SELECT value FROM watermarks WHERE name = ?", (name,)).fetchone()
    return row[0] if row else None


def set_watermark(conn: sqlite3.Connection, name: str, value: str) -> None:
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
    """Return error string if record is invalid."""
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
    """Validate and stage records, filtering by watermark."""
    result = PipelineResult()

    for rec in records:
        ts = rec.get("ts", "")

        # Incremental filter
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
    """Upsert staged records into the target table."""
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

    # Clear staging after load
    conn.execute("DELETE FROM staging")
    conn.commit()
    return loaded


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

        import time
        start = time.perf_counter()

        watermark = get_watermark(conn, "events_ts")
        stage_result = stage_records(conn, records, watermark)
        loaded = load_to_target(conn)
        stage_result.loaded = loaded

        # Update watermark to max timestamp
        max_ts = conn.execute("SELECT MAX(ts) FROM target").fetchone()[0]
        if max_ts:
            set_watermark(conn, "events_ts", max_ts)

        elapsed = int((time.perf_counter() - start) * 1000)

        # Log the run
        conn.execute(
            "INSERT INTO run_log (status, staged, loaded, rejected, duration_ms) "
            "VALUES (?, ?, ?, ?, ?)",
            ("success", stage_result.staged, loaded, stage_result.rejected, elapsed),
        )
        conn.commit()

        # Gather stats
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
