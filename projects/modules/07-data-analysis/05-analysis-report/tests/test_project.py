"""
Tests for Project 05 — Analysis Report

These tests verify the complete analysis pipeline: data preparation,
monthly revenue calculations, product ranking, customer segmentation,
and report export. Each function is tested in isolation with small
inline DataFrames.

Why test an analysis pipeline?
    The pipeline chains multiple transformations. A bug in an early step
    (e.g., wrong date parsing) silently corrupts all downstream steps.
    Testing each step independently makes it easy to pinpoint where things
    break.

Run with: pytest tests/test_project.py -v
"""

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import pytest

from project import (
    clean_and_prepare,
    monthly_revenue,
    top_products,
    customer_segments,
    export_report,
)


@pytest.fixture
def raw_df():
    """Create a small transaction DataFrame mimicking transactions.csv.

    This data is designed to produce predictable results:
    - 2 months of data (Jan and Feb 2024)
    - 2 products (Widget and Gadget)
    - 3 customers with different purchase frequencies
    """
    return pd.DataFrame({
        "date": [
            "2024-01-10", "2024-01-20", "2024-02-05",
            "2024-02-15", "2024-01-25",
        ],
        "product": ["Widget", "Gadget", "Widget", "Widget", "Gadget"],
        "quantity": [2, 1, 3, 1, 2],
        "price": [10.00, 25.00, 10.00, 10.00, 25.00],
        "customer_id": ["C001", "C002", "C001", "C003", "C001"],
    })


@pytest.fixture
def prepared_df(raw_df):
    """Run clean_and_prepare on the raw data, returning a ready DataFrame.

    This fixture is used by tests that need a DataFrame with the 'date'
    column parsed as datetime and the 'revenue' column added.
    """
    return clean_and_prepare(raw_df)


# ── Test: clean_and_prepare ────────────────────────────────────────────

def test_clean_and_prepare_parses_dates(raw_df):
    """clean_and_prepare should convert date strings to datetime objects.

    WHY: Date parsing is the foundation of time-based analysis. If dates
    remain as strings, grouping by month (dt.to_period) will fail.
    """
    result = clean_and_prepare(raw_df)

    assert pd.api.types.is_datetime64_any_dtype(result["date"]), (
        "date column should be datetime after preparation"
    )


def test_clean_and_prepare_adds_revenue_column(raw_df):
    """clean_and_prepare should add a revenue column (quantity * price).

    WHY: Revenue is the key metric for the entire report. If the
    multiplication is wrong, every downstream calculation is wrong.
    """
    result = clean_and_prepare(raw_df)

    assert "revenue" in result.columns, "Should add a 'revenue' column"

    # First row: quantity=2, price=10.00 -> revenue=20.00
    assert result["revenue"].iloc[0] == pytest.approx(20.00)

    # Second row: quantity=1, price=25.00 -> revenue=25.00
    assert result["revenue"].iloc[1] == pytest.approx(25.00)


# ── Test: monthly_revenue ──────────────────────────────────────────────

def test_monthly_revenue_groups_by_month(prepared_df):
    """monthly_revenue should return total revenue per month.

    WHY: Monthly aggregation is the primary time-series view. Incorrect
    period conversion or grouping would merge or split months incorrectly.
    """
    result = monthly_revenue(prepared_df)

    # Our data has January and February transactions.
    assert len(result) == 2, "Should have 2 months of data"


def test_monthly_revenue_sums_correctly(prepared_df):
    """Monthly sums should match hand-calculated values.

    WHY: Aggregation bugs (e.g., mean instead of sum, wrong column) produce
    plausible-looking but incorrect numbers. Testing against known values
    catches these.
    """
    result = monthly_revenue(prepared_df)

    # Jan: (2*10) + (1*25) + (2*25) = 20 + 25 + 50 = 95
    # Feb: (3*10) + (1*10) = 30 + 10 = 40
    total = result.sum()
    assert total == pytest.approx(135.0), "Total revenue should be 135.00"


# ── Test: top_products ─────────────────────────────────────────────────

def test_top_products_ranks_correctly(prepared_df):
    """top_products should rank products by total revenue, highest first.

    WHY: The ranking determines which products appear at the top of the
    report. An incorrect sort order would mislead business decisions.
    """
    result = top_products(prepared_df)

    # Widget: (2*10) + (3*10) + (1*10) = 60
    # Gadget: (1*25) + (2*25) = 75
    # Gadget should be first (highest revenue).
    assert result.index[0] == "Gadget", "Gadget should have the highest revenue"
    assert result.iloc[0] == pytest.approx(75.0)


# ── Test: customer_segments ────────────────────────────────────────────

def test_customer_segments_classifies_correctly(prepared_df):
    """customer_segments should classify customers by purchase frequency.

    WHY: Customer segmentation drives marketing strategy. The classification
    thresholds (1, 2-3, 4+) must be applied correctly.

    Our test data:
    - C001: 3 orders -> Occasional (2-3)
    - C002: 1 order  -> One-time buyer
    - C003: 1 order  -> One-time buyer
    """
    result = customer_segments(prepared_df)

    # Result is a list of dicts with segment, customers, avg_orders.
    segment_dict = {seg["segment"]: seg["customers"] for seg in result}

    assert segment_dict.get("One-time buyer", 0) == 2, "C002 and C003 are one-time"
    assert segment_dict.get("Occasional (2-3)", 0) == 1, "C001 is occasional"


# ── Test: export_report ────────────────────────────────────────────────

def test_export_report_creates_file(prepared_df, tmp_path, monkeypatch):
    """export_report should write a plain-text report file.

    WHY: The report is the final deliverable. If it fails to write or
    writes an empty file, the entire pipeline was pointless.
    """
    import os
    monkeypatch.chdir(tmp_path)
    os.makedirs(tmp_path / "data", exist_ok=True)

    monthly = monthly_revenue(prepared_df)
    product_rev = top_products(prepared_df)
    segments = customer_segments(prepared_df)

    export_report(prepared_df, monthly, product_rev, segments)

    report_path = tmp_path / "data" / "report.txt"
    assert report_path.exists(), "Report file should be created"

    content = report_path.read_text()
    assert "SALES ANALYSIS REPORT" in content, "Report should have a title"
    assert "MONTHLY REVENUE" in content, "Report should include monthly section"
    assert "CUSTOMER SEGMENTS" in content, "Report should include segments section"
