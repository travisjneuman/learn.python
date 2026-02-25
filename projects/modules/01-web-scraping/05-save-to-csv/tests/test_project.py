"""Tests for Module 01 / Project 05 — Save to CSV.

These tests verify the deduplication logic, CSV writing, and the scraping
pipeline. We mock HTTP requests and use temporary files for CSV output.

WHY use tmp_path?
- pytest's tmp_path fixture provides a unique temporary directory per test.
- Files written there are cleaned up automatically, so tests never leave
  leftover files on disk.
"""

import csv
import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import (
    deduplicate,
    write_csv,
    extract_books_from_html,
    CSV_FIELDS,
    RATING_MAP,
)


# ---------------------------------------------------------------------------
# Sample HTML for extraction tests
# ---------------------------------------------------------------------------

SAMPLE_HTML = """
<html>
<body>
<article class="product_pod">
  <p class="star-rating Four"></p>
  <h3><a href="b.html" title="CSV Book">CSV Book</a></h3>
  <p class="price_color">£15.50</p>
  <p class="instock availability">In stock</p>
</article>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Tests for deduplicate()
# ---------------------------------------------------------------------------

def test_deduplicate_removes_duplicates():
    """deduplicate() should remove books with the same title.

    When two books have the same title, only the first one is kept.
    This prevents duplicate rows in the CSV output.
    """
    books = [
        {"title": "Book A", "price": "£1.00"},
        {"title": "Book B", "price": "£2.00"},
        {"title": "Book A", "price": "£3.00"},  # duplicate title
    ]

    result = deduplicate(books, key="title")

    assert len(result) == 2
    assert result[0]["title"] == "Book A"
    assert result[1]["title"] == "Book B"


def test_deduplicate_preserves_first_occurrence():
    """When duplicates exist, deduplicate() should keep the first one.

    The price of the first 'Book A' (£1.00) should be kept, not the
    duplicate's price (£3.00).
    """
    books = [
        {"title": "Book A", "price": "£1.00"},
        {"title": "Book A", "price": "£3.00"},
    ]

    result = deduplicate(books, key="title")

    assert len(result) == 1
    assert result[0]["price"] == "£1.00"


def test_deduplicate_no_duplicates():
    """deduplicate() should return the same list when there are no duplicates."""
    books = [
        {"title": "Book A", "price": "£1.00"},
        {"title": "Book B", "price": "£2.00"},
    ]

    result = deduplicate(books, key="title")

    assert len(result) == 2


def test_deduplicate_empty_list():
    """deduplicate() should handle an empty list without errors."""
    result = deduplicate([], key="title")
    assert result == []


# ---------------------------------------------------------------------------
# Tests for write_csv()
# ---------------------------------------------------------------------------

def test_write_csv_creates_file(tmp_path):
    """write_csv() should create a CSV file at the specified path.

    tmp_path is a pytest fixture that gives us a temporary directory.
    """
    filepath = str(tmp_path / "output.csv")
    books = [{"title": "T", "price": "£1", "rating": "3 star", "availability": "In stock"}]

    write_csv(books, filepath, CSV_FIELDS)

    assert os.path.exists(filepath)


def test_write_csv_has_correct_header(tmp_path):
    """The CSV file should start with a header row matching CSV_FIELDS.

    CSV_FIELDS defines the column order: title, price, rating, availability.
    """
    filepath = str(tmp_path / "output.csv")
    books = [{"title": "T", "price": "£1", "rating": "3 star", "availability": "In stock"}]

    write_csv(books, filepath, CSV_FIELDS)

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    assert header == CSV_FIELDS


def test_write_csv_has_correct_row_count(tmp_path):
    """The CSV should have one data row per book, plus the header row."""
    filepath = str(tmp_path / "output.csv")
    books = [
        {"title": "A", "price": "£1", "rating": "1 star", "availability": "In stock"},
        {"title": "B", "price": "£2", "rating": "2 star", "availability": "In stock"},
        {"title": "C", "price": "£3", "rating": "3 star", "availability": "In stock"},
    ]

    write_csv(books, filepath, CSV_FIELDS)

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 1 header + 3 data rows = 4 total
    assert len(rows) == 4


def test_write_csv_creates_directories(tmp_path):
    """write_csv() should create parent directories if they don't exist.

    This tests the os.makedirs(exist_ok=True) call in the function.
    """
    filepath = str(tmp_path / "nested" / "dir" / "output.csv")
    books = [{"title": "T", "price": "£1", "rating": "3 star", "availability": "In stock"}]

    write_csv(books, filepath, CSV_FIELDS)

    assert os.path.exists(filepath)


# ---------------------------------------------------------------------------
# Tests for extract_books_from_html()
# ---------------------------------------------------------------------------

def test_extract_books_from_html_returns_all_fields():
    """extract_books_from_html() should return dicts with all four CSV fields.

    Each dict must have: title, price, rating, availability.
    """
    books = extract_books_from_html(SAMPLE_HTML)

    assert len(books) == 1
    book = books[0]
    assert book["title"] == "CSV Book"
    assert book["price"] == "£15.50"
    assert "star" in book["rating"]  # e.g. "4 star"
    assert "In stock" in book["availability"]
