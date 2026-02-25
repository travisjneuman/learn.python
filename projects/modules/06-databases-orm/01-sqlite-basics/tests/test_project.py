"""Tests for Module 06 / Project 01 — SQLite Basics.

Tests the database functions using an in-memory SQLite database instead
of a file-based one. This keeps tests isolated and fast.

WHY use in-memory SQLite for tests?
- No files are created on disk (nothing to clean up).
- Each test gets a fresh database (no leftover data from previous runs).
- In-memory databases are faster than disk-based ones.
"""

import sys
import os
import sqlite3

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import (
    create_table,
    insert_sample_books,
    get_all_books,
    get_books_by_year,
    search_books_by_title,
    get_books_by_author,
    demo_safe_query,
    SAMPLE_BOOKS,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """Create a fresh in-memory SQLite database with the books table and sample data.

    The connection uses row_factory=sqlite3.Row so rows support column access
    by name (row["title"]) — same as the production code.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    create_table(conn)
    insert_sample_books(conn)
    yield conn
    conn.close()


@pytest.fixture
def empty_db():
    """Create a fresh in-memory database with the table but NO data.

    Useful for testing empty-table edge cases.
    """
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    create_table(conn)
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# Tests for create_table()
# ---------------------------------------------------------------------------

def test_create_table_creates_books_table():
    """create_table() should create a 'books' table in the database.

    We verify by querying SQLite's internal schema table.
    """
    conn = sqlite3.connect(":memory:")
    create_table(conn)

    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    tables = cursor.fetchall()

    assert len(tables) == 1
    conn.close()


# ---------------------------------------------------------------------------
# Tests for insert_sample_books()
# ---------------------------------------------------------------------------

def test_insert_sample_books_count(db):
    """insert_sample_books() should insert all 6 sample books."""
    books = get_all_books(db)
    assert len(books) == len(SAMPLE_BOOKS)


def test_insert_sample_books_data(db):
    """The inserted books should match the SAMPLE_BOOKS data."""
    books = get_all_books(db)
    titles = [row["title"] for row in books]

    assert "The Pragmatic Programmer" in titles
    assert "Clean Code" in titles
    assert "Fluent Python" in titles


# ---------------------------------------------------------------------------
# Tests for get_all_books()
# ---------------------------------------------------------------------------

def test_get_all_books_returns_rows(db):
    """get_all_books() should return all rows from the books table."""
    books = get_all_books(db)
    assert len(books) == 6


def test_get_all_books_empty_table(empty_db):
    """get_all_books() should return an empty list when the table has no rows."""
    books = get_all_books(empty_db)
    assert books == []


# ---------------------------------------------------------------------------
# Tests for get_books_by_year()
# ---------------------------------------------------------------------------

def test_get_books_by_year_found(db):
    """get_books_by_year(2015) should return the two books published in 2015.

    'Fluent Python' and 'Python Crash Course' are both from 2015.
    """
    books = get_books_by_year(db, 2015)
    assert len(books) == 2


def test_get_books_by_year_not_found(db):
    """get_books_by_year(2000) should return an empty list if no books match."""
    books = get_books_by_year(db, 2000)
    assert len(books) == 0


# ---------------------------------------------------------------------------
# Tests for search_books_by_title()
# ---------------------------------------------------------------------------

def test_search_by_title_partial_match(db):
    """search_books_by_title('Python') should find books with 'Python' in the title.

    Uses LIKE with % wildcards for partial matching.
    """
    books = search_books_by_title(db, "Python")

    titles = [row["title"] for row in books]
    assert "Fluent Python" in titles
    assert "Python Crash Course" in titles


def test_search_by_title_no_match(db):
    """search_books_by_title('Nonexistent') should return an empty list."""
    books = search_books_by_title(db, "Nonexistent")
    assert len(books) == 0


# ---------------------------------------------------------------------------
# Tests for get_books_by_author()
# ---------------------------------------------------------------------------

def test_get_books_by_author_found(db):
    """get_books_by_author() should return books by the specified author."""
    books = get_books_by_author(db, "David Thomas")
    assert len(books) == 1
    assert books[0]["title"] == "The Pragmatic Programmer"


def test_get_books_by_author_not_found(db):
    """get_books_by_author() should return an empty list for unknown authors."""
    books = get_books_by_author(db, "Unknown Author")
    assert len(books) == 0


# ---------------------------------------------------------------------------
# Tests for SQL injection safety
# ---------------------------------------------------------------------------

def test_parameterized_query_prevents_injection(db):
    """Parameterized queries should treat dangerous input as a plain string value.

    The input '; DROP TABLE books; -- is an SQL injection attempt.
    With parameterized queries, it becomes a literal search term and
    finds no results (instead of dropping the table).
    """
    dangerous_input = "'; DROP TABLE books; --"
    books = get_books_by_author(db, dangerous_input)

    # The query should find nothing (the input is not a real author name).
    assert len(books) == 0

    # The books table should still exist and contain data.
    all_books = get_all_books(db)
    assert len(all_books) == 6
