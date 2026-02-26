"""Tests for the sales pipeline.

These tests pass on the FIXED version of codebase.py.
If any test fails, you have not found all the bugs yet.
"""

import csv
import os
import tempfile
from datetime import datetime

# These tests import from the parent. Run with:
#   cd practice/code-reading/02_find_the_bugs
#   python -m pytest tests/

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codebase import (
    filter_by_date,
    paginate,
    read_sales,
    summarize_by_category,
    process_pipeline,
)


def _write_csv(filepath, rows):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "product", "quantity", "unit_price"])
        for row in rows:
            writer.writerow(row)


def _sample_rows():
    return [
        ["2024-01-10", "Electronics", "Widget", "2", "50.00"],
        ["2024-01-15", "Electronics", "Gadget", "1", "100.00"],
        ["2024-02-01", "Books", "Novel", "3", "12.99"],
        ["2024-02-15", "Electronics", "Widget", "4", "50.00"],
        ["2024-03-01", "Books", "Textbook", "1", "79.99"],
    ]


# --- Bug 1: resource leak in read_sales ---

def test_read_sales_closes_file(tmp_path):
    """read_sales should not leak file handles."""
    filepath = tmp_path / "sales.csv"
    _write_csv(filepath, _sample_rows())

    # Call read_sales multiple times. If it leaks handles, this will
    # eventually fail on systems with low file descriptor limits.
    for _ in range(100):
        records = read_sales(str(filepath))
    assert len(records) == 5


# --- Bug 2: paginate is off-by-one ---

def test_paginate_page_one():
    """Page 1 should return the first PAGE_SIZE items."""
    items = list(range(25))
    page = paginate(items, 1)
    assert page == list(range(10)), "Page 1 should be items 0-9"


def test_paginate_page_two():
    """Page 2 should return items 10-19."""
    items = list(range(25))
    page = paginate(items, 2)
    assert page == list(range(10, 20)), "Page 2 should be items 10-19"


# --- Bug 3: category whitespace not stripped ---

def test_summarize_strips_whitespace(tmp_path):
    """Categories with trailing spaces should merge with clean categories."""
    filepath = tmp_path / "sales.csv"
    rows = [
        ["2024-01-10", "Electronics", "Widget", "1", "100.00"],
        ["2024-01-11", "Electronics ", "Gadget", "1", "100.00"],
    ]
    _write_csv(filepath, rows)
    records = read_sales(str(filepath))
    summary = summarize_by_category(records)

    assert len(summary) == 1, (
        f"Expected 1 category but got {len(summary)}: {list(summary.keys())}. "
        "Whitespace in category names should be stripped."
    )
    assert summary["Electronics"]["transaction_count"] == 2


# --- Bug 4: filter_by_date boundary ---
# The docstring says [start, end) but verify the implementation matches.

def test_filter_includes_start_date():
    """Records exactly on start_date should be included."""
    records = [
        {"date": datetime(2024, 1, 1), "category": "A", "product": "X", "quantity": 1, "unit_price": 10},
        {"date": datetime(2024, 1, 15), "category": "A", "product": "Y", "quantity": 1, "unit_price": 20},
    ]
    filtered = filter_by_date(records, datetime(2024, 1, 1), datetime(2024, 2, 1))
    assert len(filtered) == 2


def test_filter_excludes_end_date():
    """Records exactly on end_date should NOT be included (half-open interval)."""
    records = [
        {"date": datetime(2024, 1, 15), "category": "A", "product": "X", "quantity": 1, "unit_price": 10},
        {"date": datetime(2024, 2, 1), "category": "A", "product": "Y", "quantity": 1, "unit_price": 20},
    ]
    filtered = filter_by_date(records, datetime(2024, 1, 1), datetime(2024, 2, 1))
    assert len(filtered) == 1, "End date should be exclusive"


# --- Integration test ---

def test_full_pipeline(tmp_path):
    """Full pipeline produces correct output."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    _write_csv(input_path, _sample_rows())

    summary = process_pipeline(
        str(input_path), str(output_path),
        "2024-01-01", "2024-03-01"
    )

    assert "Electronics" in summary
    assert "Books" in summary

    elec = summary["Electronics"]
    assert elec["transaction_count"] == 3
    assert elec["total_revenue"] == 400.00

    books = summary["Books"]
    assert books["transaction_count"] == 1
    assert books["total_revenue"] == 38.97

    assert os.path.exists(output_path)
