"""Tests for Module 01 / Project 02 — Parse HTML.

These tests verify that fetch_page() and parse_books() correctly fetch
and parse HTML from books.toscrape.com. All HTTP requests are mocked —
we provide sample HTML that mirrors the real site's structure.

WHY provide sample HTML?
- We control exactly what the parser receives, so tests are deterministic.
- If the real site changes its HTML, our parser tests still pass because
  we are testing OUR parsing logic, not the external site's stability.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_page, parse_books, display_books


# ---------------------------------------------------------------------------
# Sample HTML that mirrors the structure of books.toscrape.com
# ---------------------------------------------------------------------------

SAMPLE_HTML = """
<html>
<body>
<article class="product_pod">
  <h3><a href="catalogue/book1.html" title="Test Book One">Test Book One</a></h3>
  <p class="price_color">£51.77</p>
</article>
<article class="product_pod">
  <h3><a href="catalogue/book2.html" title="Test Book Two">Test Book Two</a></h3>
  <p class="price_color">£23.99</p>
</article>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Tests for fetch_page()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_page_returns_text_on_success(mock_get):
    """fetch_page() should return response.text when status is 200.

    The function returns the raw HTML string so that parse_books() can
    process it. On success (200), we get the text; on failure, we get None.
    """
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.text = "<html>OK</html>"
    mock_get.return_value = fake_response

    result = fetch_page("http://example.com")

    assert result == "<html>OK</html>"


@patch("project.requests.get")
def test_fetch_page_returns_none_on_failure(mock_get):
    """fetch_page() should return None when the HTTP status is not 200.

    This tells the caller that the page could not be fetched, so it
    should skip parsing and display an error message.
    """
    fake_response = MagicMock()
    fake_response.status_code = 500
    mock_get.return_value = fake_response

    result = fetch_page("http://example.com")

    assert result is None


# ---------------------------------------------------------------------------
# Tests for parse_books()
# ---------------------------------------------------------------------------

def test_parse_books_extracts_correct_count():
    """parse_books() should find all <article class='product_pod'> elements.

    Our sample HTML has 2 articles, so we expect 2 books.
    """
    books = parse_books(SAMPLE_HTML)

    assert len(books) == 2


def test_parse_books_extracts_titles():
    """parse_books() should extract the book title from the <a> tag's title attribute.

    The title attribute holds the full title (the visible text may be truncated).
    """
    books = parse_books(SAMPLE_HTML)

    assert books[0][0] == "Test Book One"
    assert books[1][0] == "Test Book Two"


def test_parse_books_extracts_prices():
    """parse_books() should extract the price text from the price_color <p> tag.

    Prices include the currency symbol (£) and are stripped of whitespace.
    """
    books = parse_books(SAMPLE_HTML)

    assert books[0][1] == "£51.77"
    assert books[1][1] == "£23.99"


def test_parse_books_returns_tuples():
    """parse_books() should return a list of (title, price) tuples.

    Each tuple has exactly two elements: the title string and the price string.
    """
    books = parse_books(SAMPLE_HTML)

    for book in books:
        assert isinstance(book, tuple)
        assert len(book) == 2


def test_parse_books_empty_html():
    """parse_books() should return an empty list for HTML with no articles.

    This handles the edge case where the page loads but has no book listings.
    """
    empty_html = "<html><body><p>No books here</p></body></html>"
    books = parse_books(empty_html)

    assert books == []


# ---------------------------------------------------------------------------
# Tests for display_books()
# ---------------------------------------------------------------------------

def test_display_books_shows_all_titles(capsys):
    """display_books() should print every book title in the output."""
    books = [("Book A", "£10.00"), ("Book B", "£20.00")]

    display_books(books)

    output = capsys.readouterr().out
    assert "Book A" in output
    assert "Book B" in output
