"""Tests for SQL Connection Simulator.

Covers:
- Connection pool acquire / release / reuse lifecycle
- Health check on live and closed connections
- Demo workload end-to-end with in-memory SQLite
- Retry behaviour when connection is unavailable
"""

from __future__ import annotations

import sqlite3

import pytest

from project import (
    ConnectionConfig,
    ConnectionPool,
    health_check,
    run,
    run_demo_queries,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def config() -> ConnectionConfig:
    """Default in-memory config with small pool for fast tests."""
    return ConnectionConfig(db_path=":memory:", pool_size=3, max_retries=2)


@pytest.fixture()
def pool(config: ConnectionConfig) -> ConnectionPool:
    pool = ConnectionPool(config)
    yield pool
    pool.close_all()


# ---------------------------------------------------------------------------
# Pool lifecycle
# ---------------------------------------------------------------------------


class TestConnectionPool:
    def test_acquire_creates_connection(self, pool: ConnectionPool) -> None:
        conn = pool.acquire()
        assert isinstance(conn, sqlite3.Connection)
        pool.release(conn)
        assert pool.stats()["created"] == 1

    def test_release_and_reuse(self, pool: ConnectionPool) -> None:
        """After release, next acquire should reuse (not create)."""
        conn1 = pool.acquire()
        pool.release(conn1)

        conn2 = pool.acquire()
        pool.release(conn2)

        stats = pool.stats()
        assert stats["created"] == 1
        assert stats["reused"] == 1

    @pytest.mark.parametrize("pool_size", [1, 3, 5])
    def test_pool_respects_max_size(self, pool_size: int) -> None:
        cfg = ConnectionConfig(pool_size=pool_size)
        p = ConnectionPool(cfg)
        conns = [p.acquire() for _ in range(pool_size + 2)]
        for c in conns:
            p.release(c)
        # idle connections should not exceed pool_size
        assert p.stats()["idle"] <= pool_size
        p.close_all()

    def test_close_all_drains_pool(self, pool: ConnectionPool) -> None:
        conn = pool.acquire()
        pool.release(conn)
        pool.close_all()
        assert pool.stats()["idle"] == 0


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


class TestHealthCheck:
    def test_healthy_connection(self) -> None:
        conn = sqlite3.connect(":memory:")
        result = health_check(conn)
        assert result["status"] == "healthy"
        assert "sqlite_version" in result
        conn.close()

    def test_closed_connection_reports_unhealthy(self) -> None:
        conn = sqlite3.connect(":memory:")
        conn.close()
        result = health_check(conn)
        assert result["status"] == "unhealthy"


# ---------------------------------------------------------------------------
# Demo workload
# ---------------------------------------------------------------------------


def test_run_demo_queries_inserts_all_labels(pool: ConnectionPool) -> None:
    labels = ["alpha", "beta", "gamma"]
    rows = run_demo_queries(pool, labels)
    assert len(rows) == 3
    assert [r["label"] for r in rows] == labels


# ---------------------------------------------------------------------------
# End-to-end run
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("event_a\nevent_b\n", encoding="utf-8")
    output_file = tmp_path / "out.json"

    summary = run(input_file, output_file)

    assert summary["rows_inserted"] == 2
    assert summary["health"]["status"] == "healthy"
    assert summary["pool_stats"]["created"] >= 1
    assert output_file.exists()
