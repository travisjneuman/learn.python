"""Tests for ETL Health Dashboard Feed.

Validates run recording, health metric computation, and
recent-runs retrieval using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    compute_health,
    get_recent_runs,
    init_db,
    record_run,
    run,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


SAMPLE_RUNS = [
    {"job_name": "daily_etl", "status": "success", "rows_in": 100, "rows_out": 95, "duration_ms": 1200, "started_at": "2025-01-01T06:00:00"},
    {"job_name": "daily_etl", "status": "success", "rows_in": 110, "rows_out": 108, "duration_ms": 1100, "started_at": "2025-01-02T06:00:00"},
    {"job_name": "daily_etl", "status": "failure", "rows_in": 50, "rows_out": 0, "duration_ms": 500, "started_at": "2025-01-03T06:00:00"},
    {"job_name": "hourly_sync", "status": "success", "rows_in": 20, "rows_out": 20, "duration_ms": 200, "started_at": "2025-01-03T07:00:00"},
]


class TestRecordRun:
    def test_returns_id(self, conn: sqlite3.Connection) -> None:
        rid = record_run(conn, SAMPLE_RUNS[0])
        assert rid > 0

    def test_multiple_runs(self, conn: sqlite3.Connection) -> None:
        for r in SAMPLE_RUNS:
            record_run(conn, r)
        count = conn.execute("SELECT COUNT(*) FROM etl_runs").fetchone()[0]
        assert count == 4


class TestHealthMetrics:
    def test_overall_stats(self, conn: sqlite3.Connection) -> None:
        for r in SAMPLE_RUNS:
            record_run(conn, r)
        health = compute_health(conn)
        assert health.total_runs == 4
        assert health.successes == 3
        assert health.failures == 1
        assert health.success_rate == 75.0

    def test_per_job_breakdown(self, conn: sqlite3.Connection) -> None:
        for r in SAMPLE_RUNS:
            record_run(conn, r)
        health = compute_health(conn)
        job_names = {j["job"] for j in health.jobs}
        assert job_names == {"daily_etl", "hourly_sync"}

    @pytest.mark.parametrize("status,expected_successes", [
        ("success", 1),
        ("failure", 0),
    ])
    def test_single_run_rate(self, conn: sqlite3.Connection, status: str, expected_successes: int) -> None:
        record_run(conn, {"job_name": "test", "status": status, "started_at": "2025-01-01T00:00:00"})
        health = compute_health(conn)
        assert health.successes == expected_successes


class TestRecentRuns:
    def test_limit(self, conn: sqlite3.Connection) -> None:
        for r in SAMPLE_RUNS:
            record_run(conn, r)
        recent = get_recent_runs(conn, limit=2)
        assert len(recent) == 2


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    inp = tmp_path / "runs.json"
    inp.write_text(json.dumps(SAMPLE_RUNS), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["runs_recorded"] == 4
    assert summary["success_rate"] == 75.0
    assert out.exists()
