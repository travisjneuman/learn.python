# Solution: Level 6 / Project 10 - Table Drift Detector

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [README](./README.md) hints or re-read the
> relevant [concept docs](../../../concepts/) first.

---

## Complete solution

```python
"""Level 6 / Project 10 — Table Drift Detector.

Captures table schemas as snapshots and compares them over time to
detect column additions, removals, and type changes (drift).
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
    """Read column metadata from PRAGMA table_info.

    WHY PRAGMA instead of querying sqlite_master? -- PRAGMA table_info()
    returns structured column metadata (name, type, nullability, PK)
    in a single call. Parsing the CREATE TABLE DDL from sqlite_master
    would require regex and be fragile with edge cases.
    """
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [
        ColumnInfo(
            name=r[1], col_type=r[2], notnull=bool(r[3]),
            default_value=r[4], pk=bool(r[5]),
        )
        for r in rows
    ]


def schema_to_dict(columns: list[ColumnInfo]) -> dict:
    """Convert column list to a serializable dict keyed by column name.

    WHY dict keyed by name? -- Set operations (added = new - old,
    removed = old - new) become trivial on dict keys. Comparing
    attributes (type changes) is a simple dict lookup per column.
    """
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
    """Retrieve the most recent snapshot for a table.

    WHY ORDER BY id DESC LIMIT 1? -- Auto-incrementing ID guarantees
    the highest ID is the most recent snapshot. Using id instead of
    captured_at avoids clock skew issues.
    """
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
    """Compare two schema dicts and report differences.

    WHY set operations for diff? -- Converting dict keys to sets gives
    us added (new - old), removed (old - new), and common (old & new)
    columns in O(n) time. This is the standard algorithm for diffing
    two collections.
    """
    report = DriftReport(table=table)

    old_cols = set(old_schema.keys())
    new_cols = set(new_schema.keys())

    report.added_columns = sorted(new_cols - old_cols)
    report.removed_columns = sorted(old_cols - new_cols)

    # WHY check type changes on the intersection? -- Only columns
    # present in both snapshots can have changed type. New/removed
    # columns are already reported separately.
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

            # WHY execute DDL steps from config? -- This simulates a
            # real environment where schemas evolve over time. The first
            # DDL creates the table; subsequent DDLs (ALTER TABLE) modify
            # it. We catch OperationalError because ALTER TABLE ADD
            # COLUMN fails silently if the column already exists.
            for ddl in table_cfg.get("ddl_steps", []):
                try:
                    conn.execute(ddl)
                    conn.commit()
                except sqlite3.OperationalError:
                    pass

            columns = get_table_schema(conn, table_name)
            current = schema_to_dict(columns)

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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| JSON-serialized schema snapshots | Easy to store, diff, and inspect; human-readable in the database | Binary format -- faster but not human-readable and not portable across systems |
| Set operations for drift detection | O(n) added/removed/common computation using Python's built-in set math | Linear scan comparing lists -- O(n*m) and harder to read |
| Snapshot-based comparison (not live-to-live) | Snapshots create a historical record; you can compare any two points in time, not just "now vs last" | Live comparison only -- loses history; you can only see the current state |
| PRAGMA table_info for introspection | Returns structured metadata directly; no regex parsing needed | Parsing CREATE TABLE DDL from sqlite_master -- fragile with complex DDL syntax |

## Alternative approaches

### Approach B: Hash-based drift detection

```python
import hashlib

def schema_hash(schema: dict) -> str:
    """Generate a deterministic hash of the schema for quick comparison."""
    canonical = json.dumps(schema, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()

def quick_drift_check(old_schema: dict, new_schema: dict) -> bool:
    """Fast check: did anything change at all?"""
    return schema_hash(old_schema) != schema_hash(new_schema)

# Usage: if quick_drift_check(old, new):
#            report = detect_drift(old, new, table)  # expensive detailed diff
```

**Trade-off:** Hash comparison is O(1) for the "no change" case (the common case), which is efficient when checking hundreds of tables. But when drift IS detected, you still need the full diff to know WHAT changed. Use the hash as a fast pre-filter before the detailed comparison.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Running twice with the same schema | Second run compares identical snapshots and correctly reports no drift; but two snapshots are stored | This is correct behavior -- the snapshots serve as an audit trail. Consider adding a dedup check if storage is a concern |
| Checking a non-existent table | `PRAGMA table_info(no_such_table)` returns an empty result; `schema_to_dict` produces `{}`; drift from previous snapshot shows all columns "removed" | Check that `PRAGMA table_info` returns at least one row before proceeding; raise a clear error if the table does not exist |
| SQLite's weak type system | SQLite allows any type name in CREATE TABLE (e.g., `BANANA`); PRAGMA returns it verbatim, so type comparisons may flag meaningless "changes" | Normalize type names to SQLite's five affinities (TEXT, INTEGER, REAL, BLOB, NUMERIC) before comparing |
