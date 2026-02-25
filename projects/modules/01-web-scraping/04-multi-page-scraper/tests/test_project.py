"""Tests for Module 01 / Project 04 — Multi-Page Scraper.

These tests verify that the scraper correctly fetches multiple pages,
extracts books from each, and combines the results. All HTTP requests
and time.sleep calls are mocked to keep tests fast and network-free.

WHY mock time.sleep?
- The real scraper sleeps 1 second between pages for rate limiting.
- In tests, sleeping wastes time. Mocking it makes tests instant.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_page, extract_books_from_html, scrape_multiple_pages, display_sample


# ---------------------------------------------------------------------------
# Sample HTML for one page of books
# ---------------------------------------------------------------------------

SAMPLE_PAGE_HTML = """
<html>
<body>
<article class="product_pod">
  <h3><a href="book1.html" title="Page Book 1">Page Book 1</a></h3>
  <p class="price_color">£10.00</p>
</article>
<article class="product_pod">
  <h3><a href="book2.html" title="Page Book 2">Page Book 2</a></h3>
  <p class="price_color">£20.00</p>
</article>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Tests for fetch_page()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_page_returns_html_on_success(mock_get):
    """fetch_page() should return the HTML text when status is 200."""
    mock_get.return_value = MagicMock(status_code=200, text="<html></html>")

    result = fetch_page("http://example.com")

    assert result == "<html></html>"


@patch("project.requests.get")
def test_fetch_page_returns_none_on_failure(mock_get):
    """fetch_page() should return None when the request fails (non-200 status).

    This lets the caller skip pages that fail to load.
    """
    mock_get.return_value = MagicMock(status_code=500)

    result = fetch_page("http://example.com")

    assert result is None


# ---------------------------------------------------------------------------
# Tests for extract_books_from_html()
# ---------------------------------------------------------------------------

def test_extract_books_from_html_correct_count():
    """extract_books_from_html() should return one dict per article tag."""
    books = extract_books_from_html(SAMPLE_PAGE_HTML)
    assert len(books) == 2


def test_extract_books_from_html_dict_keys():
    """Each book dict should have 'title' and 'price' keys.

    This project extracts only these two fields per book (unlike project 03
    which also extracts rating and availability).
    """
    books = extract_books_from_html(SAMPLE_PAGE_HTML)

    for book in books:
        assert "title" in book
        assert "price" in book


def test_extract_books_from_html_values():
    """The extracted titles and prices should match what's in the HTML."""
    books = extract_books_from_html(SAMPLE_PAGE_HTML)

    assert books[0]["title"] == "Page Book 1"
    assert books[0]["price"] == "£10.00"
    assert books[1]["title"] == "Page Book 2"
    assert books[1]["price"] == "£20.00"


# ---------------------------------------------------------------------------
# Tests for scrape_multiple_pages()
# ---------------------------------------------------------------------------

@patch("project.time.sleep")  # Mock sleep so tests don't actually wait
@patch("project.fetch_page")
def test_scrape_multiple_pages_combines_results(mock_fetch, mock_sleep):
    """scrape_multiple_pages() should combine books from all fetched pages.

    If each page has 2 books and we scrape 3 pages, we should get 6 books.
    """
    mock_fetch.return_value = SAMPLE_PAGE_HTML

    books = scrape_multiple_pages(3)

    # 3 pages x 2 books per page = 6 books
    assert len(books) == 6


@patch("project.time.sleep")
@patch("project.fetch_page")
def test_scrape_multiple_pages_skips_failed_pages(mock_fetch, mock_sleep):
    """If a page fails to load, scrape_multiple_pages() should skip it.

    We simulate page 2 failing. The scraper should still return books
    from pages 1 and 3.
    """
    # Page 1 succeeds, page 2 fails (returns None), page 3 succeeds
    mock_fetch.side_effect = [SAMPLE_PAGE_HTML, None, SAMPLE_PAGE_HTML]

    books = scrape_multiple_pages(3)

    # 2 successful pages x 2 books = 4 books
    assert len(books) == 4


@patch("project.time.sleep")
@patch("project.fetch_page")
def test_scrape_multiple_pages_respects_rate_limit(mock_fetch, mock_sleep):
    """scrape_multiple_pages() should sleep between pages (but not after the last).

    With 3 pages, there should be 2 sleeps (between page 1-2 and 2-3).
    """
    mock_fetch.return_value = SAMPLE_PAGE_HTML

    scrape_multiple_pages(3)

    # Sleep should be called num_pages - 1 times.
    assert mock_sleep.call_count == 2


# ---------------------------------------------------------------------------
# Tests for display_sample()
# ---------------------------------------------------------------------------

def test_display_sample_shows_limited_output(capsys):
    """display_sample() should only show the first N books."""
    books = [{"title": f"Book {i}", "price": f"£{i}.00"} for i in range(10)]

    display_sample(books, sample_size=3)

    output = capsys.readouterr().out
    assert "Book 1" in output
    assert "Book 3" in output
    # Book 4 should NOT appear in a sample of 3.
    assert "Book 4" not in output
