"""Tests for Module 01 / Project 03 — Extract Structured Data.

These tests verify that extract_books() parses HTML into a list of
dictionaries with four fields: title, price, rating, availability.
We also test the RATING_MAP constant and the display_table() function.

WHY test with sample HTML?
- It isolates our parsing logic from the real website.
- We can include edge cases (different ratings, availability statuses)
  that might not appear on the live page at any given moment.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import extract_books, RATING_MAP, display_table, fetch_page


# ---------------------------------------------------------------------------
# Sample HTML
# ---------------------------------------------------------------------------

SAMPLE_HTML = """
<html>
<body>
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="book1.html" title="A Great Book">A Great Book</a></h3>
  <p class="price_color">£51.77</p>
  <p class="instock availability">
    <i class="icon-ok"></i>
        In stock
  </p>
</article>
<article class="product_pod">
  <p class="star-rating Five"></p>
  <h3><a href="book2.html" title="Another Title">Another Title</a></h3>
  <p class="price_color">£12.34</p>
  <p class="instock availability">
    <i class="icon-ok"></i>
        In stock
  </p>
</article>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Tests for RATING_MAP
# ---------------------------------------------------------------------------

def test_rating_map_has_all_five_ratings():
    """RATING_MAP should map all five English words to integers 1-5.

    This constant converts CSS class names like 'Three' to the number 3.
    If any mapping is missing, extract_books() would return rating 0.
    """
    assert RATING_MAP["One"] == 1
    assert RATING_MAP["Two"] == 2
    assert RATING_MAP["Three"] == 3
    assert RATING_MAP["Four"] == 4
    assert RATING_MAP["Five"] == 5
    assert len(RATING_MAP) == 5


# ---------------------------------------------------------------------------
# Tests for extract_books()
# ---------------------------------------------------------------------------

def test_extract_books_returns_correct_count():
    """extract_books() should return one dict per <article> in the HTML."""
    books = extract_books(SAMPLE_HTML)
    assert len(books) == 2


def test_extract_books_contains_all_fields():
    """Each book dict should have exactly four keys: title, price, rating, availability.

    These four fields represent the structured data we extract from each product pod.
    """
    books = extract_books(SAMPLE_HTML)

    for book in books:
        assert "title" in book
        assert "price" in book
        assert "rating" in book
        assert "availability" in book


def test_extract_books_title_values():
    """Titles should come from the <a> tag's title attribute, not the visible text."""
    books = extract_books(SAMPLE_HTML)

    assert books[0]["title"] == "A Great Book"
    assert books[1]["title"] == "Another Title"


def test_extract_books_price_values():
    """Prices should be extracted as strings including the currency symbol."""
    books = extract_books(SAMPLE_HTML)

    assert books[0]["price"] == "£51.77"
    assert books[1]["price"] == "£12.34"


def test_extract_books_rating_values():
    """Ratings should be converted from CSS class words to integers via RATING_MAP.

    'Three' -> 3, 'Five' -> 5.
    """
    books = extract_books(SAMPLE_HTML)

    assert books[0]["rating"] == 3
    assert books[1]["rating"] == 5


def test_extract_books_availability_stripped():
    """Availability text should be stripped of surrounding whitespace.

    The raw HTML has lots of extra whitespace around 'In stock'.
    """
    books = extract_books(SAMPLE_HTML)

    assert "In stock" in books[0]["availability"]


def test_extract_books_empty_html():
    """extract_books() should return an empty list if no articles exist."""
    books = extract_books("<html><body></body></html>")
    assert books == []


# ---------------------------------------------------------------------------
# Tests for display_table()
# ---------------------------------------------------------------------------

def test_display_table_prints_all_titles(capsys):
    """display_table() should include every book's title in the output."""
    books = [
        {"title": "Book X", "price": "£1.00", "rating": 4, "availability": "In stock"},
        {"title": "Book Y", "price": "£2.00", "rating": 2, "availability": "In stock"},
    ]

    display_table(books)

    output = capsys.readouterr().out
    assert "Book X" in output
    assert "Book Y" in output


# ---------------------------------------------------------------------------
# Tests for fetch_page()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_page_returns_none_on_error(mock_get):
    """fetch_page() should return None when the server returns a non-200 status."""
    mock_get.return_value = MagicMock(status_code=503)

    result = fetch_page("http://example.com")

    assert result is None
