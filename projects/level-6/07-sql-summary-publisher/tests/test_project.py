"""Tests for SQL Summary Publisher.

Validates aggregate queries, report formatting, and end-to-end
summary generation using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    SummaryReport,
    build_summary,
    format_text_report,
    run,
    seed_sales,
    SALES_DDL,
)

SAMPLE_SALES = [
    {"region": "North", "product": "Widget", "quantity": 10, "revenue": 99.90, "sale_date": "2025-01-01"},
    {"region": "North", "product": "Gadget", "quantity": 5, "revenue": 124.75, "sale_date": "2025-01-02"},
    {"region": "South", "product": "Widget", "quantity": 20, "revenue": 199.80, "sale_date": "2025-01-03"},
    {"region": "South", "product": "Bolt", "quantity": 100, "revenue": 50.00, "sale_date": "2025-01-04"},
]


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.execute(SALES_DDL)
    seed_sales(c, SAMPLE_SALES)
    yield c
    c.close()


class TestBuildSummary:
    def test_total_counts(self, conn: sqlite3.Connection) -> None:
        report = build_summary(conn)
        assert report.total_sales == 4
        assert report.total_revenue == pytest.approx(474.45)

    def test_by_region(self, conn: sqlite3.Connection) -> None:
        report = build_summary(conn)
        regions = {r["region"]: r for r in report.by_region}
        assert "North" in regions
        assert "South" in regions
        assert regions["South"]["revenue"] > regions["North"]["revenue"]

    def test_by_product(self, conn: sqlite3.Connection) -> None:
        report = build_summary(conn)
        products = {p["product"] for p in report.by_product}
        assert products == {"Widget", "Gadget", "Bolt"}

    def test_top_sale(self, conn: sqlite3.Connection) -> None:
        report = build_summary(conn)
        assert report.top_sale["product"] == "Widget"
        assert report.top_sale["region"] == "South"

    @pytest.mark.parametrize("count", [0, 1, 4])
    def test_various_data_sizes(self, count: int) -> None:
        c = sqlite3.connect(":memory:")
        c.execute(SALES_DDL)
        seed_sales(c, SAMPLE_SALES[:count])
        report = build_summary(c)
        assert report.total_sales == count
        c.close()


class TestFormatText:
    def test_contains_key_sections(self) -> None:
        report = SummaryReport(
            total_sales=2, total_revenue=100.0,
            by_region=[{"region": "East", "count": 2, "revenue": 100.0, "avg_revenue": 50.0}],
            by_product=[{"product": "X", "quantity": 5, "revenue": 100.0}],
        )
        text = format_text_report(report)
        assert "SALES SUMMARY" in text
        assert "East" in text
        assert "$100.00" in text


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    inp = tmp_path / "sales.json"
    inp.write_text(json.dumps(SAMPLE_SALES), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["total_sales"] == 4
    assert out.exists()
    assert out.with_suffix(".txt").exists()
