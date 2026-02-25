"""Level 6 / Project 12 — ETL Health Dashboard Feed.

Records ETL job runs with status, timing, and row counts in SQLite,
then generates health metrics suitable for a monitoring dashboard.

Key concepts:
- Job run tracking: start/end times, status, row counts
- Aggregate health metrics: success rate, avg duration, throughput
- Time-windowed queries for "last N runs" analysis
- Publishing metrics as JSON for dashboard consumption
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

RUNS_DDL = """\
CREATE TABLE IF NOT EXISTS etl_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name    TEXT NOT NULL,
    status      TEXT NOT NULL CHECK(status IN ('success','failure','running')),
    rows_in     INTEGER NOT NULL DEFAULT 0,
    rows_out    INTEGER NOT NULL DEFAULT 0,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    started_at  TEXT NOT NULL,
    finished_at TEXT
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(RUNS_DDL)
    conn.commit()


# ---------------------------------------------------------------------------
# Run recording
# ---------------------------------------------------------------------------


def record_run(conn: sqlite3.Connection, run_data: dict) -> int:
    """Insert an ETL run record and return its ID."""
    cur = conn.execute(
        "INSERT INTO etl_runs (job_name, status, rows_in, rows_out, "
        "duration_ms, started_at, finished_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            run_data["job_name"],
            run_data["status"],
            run_data.get("rows_in", 0),
            run_data.get("rows_out", 0),
            run_data.get("duration_ms", 0),
            run_data["started_at"],
            run_data.get("finished_at"),
        ),
    )
    conn.commit()
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Health metrics
# ---------------------------------------------------------------------------


@dataclass
class HealthMetrics:
    total_runs: int = 0
    successes: int = 0
    failures: int = 0
    success_rate: float = 0.0
    avg_duration_ms: float = 0.0
    total_rows_in: int = 0
    total_rows_out: int = 0
    jobs: list[dict] = field(default_factory=list)


def compute_health(conn: sqlite3.Connection) -> HealthMetrics:
    """Compute aggregate health metrics across all recorded runs."""
    m = HealthMetrics()

    row = conn.execute(
        "SELECT COUNT(*), "
        "SUM(CASE WHEN status='success' THEN 1 ELSE 0 END), "
        "SUM(CASE WHEN status='failure' THEN 1 ELSE 0 END), "
        "COALESCE(AVG(duration_ms), 0), "
        "COALESCE(SUM(rows_in), 0), "
        "COALESCE(SUM(rows_out), 0) "
        "FROM etl_runs"
    ).fetchone()

    m.total_runs = row[0]
    m.successes = row[1]
    m.failures = row[2]
    m.avg_duration_ms = round(row[3], 1)
    m.total_rows_in = row[4]
    m.total_rows_out = row[5]
    m.success_rate = round(m.successes / m.total_runs * 100, 1) if m.total_runs else 0.0

    # Per-job breakdown
    for r in conn.execute(
        "SELECT job_name, COUNT(*) AS runs, "
        "SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) AS ok, "
        "AVG(duration_ms) AS avg_ms "
        "FROM etl_runs GROUP BY job_name ORDER BY runs DESC"
    ).fetchall():
        m.jobs.append({
            "job": r[0], "runs": r[1], "successes": r[2],
            "avg_duration_ms": round(r[3], 1),
        })

    return m


def get_recent_runs(conn: sqlite3.Connection, limit: int = 10) -> list[dict]:
    """Return the most recent runs for dashboard display."""
    rows = conn.execute(
        "SELECT id, job_name, status, rows_in, rows_out, duration_ms, started_at "
        "FROM etl_runs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [
        {"id": r[0], "job": r[1], "status": r[2], "rows_in": r[3],
         "rows_out": r[4], "duration_ms": r[5], "started_at": r[6]}
        for r in rows
    ]


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path, db_path: str = ":memory:") -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    runs = json.loads(input_path.read_text(encoding="utf-8"))

    conn = sqlite3.connect(db_path)
    try:
        init_db(conn)
        for r in runs:
            record_run(conn, r)

        health = compute_health(conn)
        recent = get_recent_runs(conn)
    finally:
        conn.close()

    summary = {
        "runs_recorded": len(runs),
        "total_runs": health.total_runs,
        "success_rate": health.success_rate,
        "avg_duration_ms": health.avg_duration_ms,
        "total_rows_in": health.total_rows_in,
        "total_rows_out": health.total_rows_out,
        "per_job": health.jobs,
        "recent_runs": recent,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("health: %d runs, %.1f%% success", health.total_runs, health.success_rate)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ETL Health Dashboard Feed — job run tracking & metrics"
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
