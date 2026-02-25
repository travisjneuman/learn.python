"""Tests for Query Performance Checker.

Validates query plan analysis, index creation, and before/after
comparison using in-memory SQLite.
"""

from __future__ import annotations

import sqlite3

import pytest

from project import (
    QueryReport,
    analyze_query,
    create_index,
    explain_query,
    run,
    seed_orders,
    ORDERS_DDL,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.execute(ORDERS_DDL)
    seed_orders(c, count=100)
    yield c
    c.close()


class TestExplainQuery:
    def test_returns_plan_lines(self, conn: sqlite3.Connection) -> None:
        lines = explain_query(conn, "SELECT * FROM orders WHERE customer = 'alice'")
        assert len(lines) >= 1
        # Should mention SCAN or SEARCH
        assert any("SCAN" in ln or "SEARCH" in ln for ln in lines)

    def test_plan_after_index(self, conn: sqlite3.Connection) -> None:
        create_index(conn, "orders", "customer")
        lines = explain_query(conn, "SELECT * FROM orders WHERE customer = 'alice'")
        assert any("INDEX" in ln for ln in lines)


class TestAnalyzeQuery:
    def test_no_index_detected(self, conn: sqlite3.Connection) -> None:
        report = analyze_query(conn, "SELECT * FROM orders WHERE customer = 'bob'")
        assert report.uses_index is False
        assert report.elapsed_ms >= 0

    def test_index_detected_after_create(self, conn: sqlite3.Connection) -> None:
        create_index(conn, "orders", "customer")
        report = analyze_query(conn, "SELECT * FROM orders WHERE customer = 'bob'")
        assert report.uses_index is True

    @pytest.mark.parametrize(
        "sql",
        [
            "SELECT * FROM orders WHERE amount > 20",
            "SELECT * FROM orders ORDER BY created_at",
        ],
    )
    def test_suggestion_present_without_index(self, conn: sqlite3.Connection, sql: str) -> None:
        report = analyze_query(conn, sql)
        assert report.suggestion  # non-empty suggestion


class TestCreateIndex:
    def test_index_creation_returns_ddl(self, conn: sqlite3.Connection) -> None:
        ddl = create_index(conn, "orders", "product")
        assert "idx_orders_product" in ddl

    def test_idempotent(self, conn: sqlite3.Connection) -> None:
        create_index(conn, "orders", "product")
        create_index(conn, "orders", "product")  # should not raise


def test_run_end_to_end(tmp_path) -> None:
    inp = tmp_path / "queries.txt"
    inp.write_text("SELECT * FROM orders WHERE customer = 'alice'\n", encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["queries_analyzed"] == 1
    assert len(summary["indexes_created"]) >= 1
    assert out.exists()
