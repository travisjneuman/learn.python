"""Level 6 / Project 10 — Table Drift Detector.

Captures table schemas as snapshots and compares them over time to
detect column additions, removals, and type changes (drift).

Key concepts:
- PRAGMA table_info() for introspecting SQLite schemas
- Schema versioning: storing snapshots with timestamps
- Diff computation: comparing two schema snapshots
- Alerting on breaking changes (column removal, type change)
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema for drift tracking
# ---------------------------------------------------------------------------

# WHY store schema snapshots? -- Database schemas change over time as
# developers add/remove/rename columns. By capturing snapshots on each
# run and diffing them, we detect "drift" — unexpected schema changes
# that could break downstream queries or ETL pipelines.
SNAPSHOTS_DDL = """\
CREATE TABLE IF NOT EXISTS schema_snapshots (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    columns    TEXT NOT NULL,
    captured_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def init_tracking_db(conn: sqlite3.Connection) -> None:
    conn.execute(SNAPSHOTS_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Schema introspection
# ---------------------------------------------------------------------------


@dataclass
class ColumnInfo:
    name: str
    col_type: str
    notnull: bool
    default_value: str | None
    pk: bool


def get_table_schema(conn: sqlite3.Connection, table: str) -> list[ColumnInfo]:
    """Read column metadata from PRAGMA table_info."""
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [
        ColumnInfo(
            name=r[1], col_type=r[2], notnull=bool(r[3]),
            default_value=r[4], pk=bool(r[5]),
        )
        for r in rows
    ]


def schema_to_dict(columns: list[ColumnInfo]) -> dict:
    """Convert column list to a serializable dict keyed by column name."""
    return {
        c.name: {"type": c.col_type, "notnull": c.notnull, "pk": c.pk}
        for c in columns
    }


# ---------------------------------------------------------------------------
# Snapshot management
# ---------------------------------------------------------------------------


def save_snapshot(conn: sqlite3.Connection, table: str, schema: dict) -> int:
    """Store a schema snapshot and return its ID."""
    cur = conn.execute(
        "INSERT INTO schema_snapshots (table_name, columns) VALUES (?, ?)",
        (table, json.dumps(schema)),
    )
    conn.commit()
    return cur.lastrowid


def get_latest_snapshot(conn: sqlite3.Connection, table: str) -> dict | None:
    """Retrieve the most recent snapshot for a table."""
    row = conn.execute(
        "SELECT columns FROM schema_snapshots WHERE table_name = ? "
        "ORDER BY id DESC LIMIT 1",
        (table,),
    ).fetchone()
    return json.loads(row[0]) if row else None


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------


@dataclass
class DriftReport:
    table: str
    added_columns: list[str] = field(default_factory=list)
    removed_columns: list[str] = field(default_factory=list)
    type_changes: list[dict] = field(default_factory=list)
    has_drift: bool = False


def detect_drift(old_schema: dict, new_schema: dict, table: str) -> DriftReport:
    """Compare two schema dicts and report differences."""
    report = DriftReport(table=table)

    old_cols = set(old_schema.keys())
    new_cols = set(new_schema.keys())

    report.added_columns = sorted(new_cols - old_cols)
    report.removed_columns = sorted(old_cols - new_cols)

    for col in old_cols & new_cols:
        if old_schema[col]["type"] != new_schema[col]["type"]:
            report.type_changes.append({
                "column": col,
                "old_type": old_schema[col]["type"],
                "new_type": new_schema[col]["type"],
            })

    report.has_drift = bool(
        report.added_columns or report.removed_columns or report.type_changes
    )
    return report


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    """Create tables from config, take snapshots, detect drift."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    config = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_tracking_db(conn)

        reports = []
        for table_cfg in config.get("tables", []):
            table_name = table_cfg["name"]

            # Create or alter the table using the provided DDL
            for ddl in table_cfg.get("ddl_steps", []):
                try:
                    conn.execute(ddl)
                    conn.commit()
                except sqlite3.OperationalError:
                    pass  # e.g. column already exists

            # Get current schema
            columns = get_table_schema(conn, table_name)
            current = schema_to_dict(columns)

            # Compare with previous snapshot
            previous = get_latest_snapshot(conn, table_name)
            if previous:
                drift = detect_drift(previous, current, table_name)
            else:
                drift = DriftReport(table=table_name)

            save_snapshot(conn, table_name, current)

            reports.append({
                "table": table_name,
                "columns": list(current.keys()),
                "has_drift": drift.has_drift,
                "added": drift.added_columns,
                "removed": drift.removed_columns,
                "type_changes": drift.type_changes,
            })

    finally:
        conn.close()

    summary = {
        "tables_checked": len(reports),
        "drift_detected": any(r["has_drift"] for r in reports),
        "reports": reports,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("drift check: %d tables, drift=%s", len(reports), summary["drift_detected"])
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Table Drift Detector — schema comparison over time"
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
