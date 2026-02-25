"""Tests for Module 06 / Project 03 — CRUD Operations.

Tests the Book model and the CRUD functions (list_books, add_book, etc.)
using an in-memory SQLite database. Interactive functions (add_book,
update_status, delete_book) use input(), which we mock in tests.

WHY mock input()?
- The CRUD functions use input() for interactive prompts.
- In tests, we cannot type into the terminal. Mocking input() lets us
  simulate user input programmatically.
"""

import sys
import os
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import Base, Book, list_books, init_db


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Create an in-memory SQLite engine."""
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    """Create a session with some sample books."""
    with Session(engine) as sess:
        books = [
            Book(title="Test Book A", author="Author A", status="available"),
            Book(title="Test Book B", author="Author B", status="checked out"),
        ]
        sess.add_all(books)
        sess.commit()
        yield sess


@pytest.fixture
def empty_session(engine):
    """Create a session with no books."""
    with Session(engine) as sess:
        yield sess


# ---------------------------------------------------------------------------
# Tests for the Book model
# ---------------------------------------------------------------------------

def test_book_default_status(engine):
    """A new Book without an explicit status should default to 'available'.

    The default is set in the mapped_column definition.
    """
    with Session(engine) as sess:
        book = Book(title="New Book", author="New Author")
        sess.add(book)
        sess.commit()
        sess.refresh(book)

        assert book.status == "available"


def test_book_repr(session):
    """Book.__repr__() should include the id, title, and status."""
    book = session.execute(select(Book)).scalars().first()
    repr_str = repr(book)

    assert "Book" in repr_str
    assert book.title in repr_str
    assert book.status in repr_str


# ---------------------------------------------------------------------------
# Tests for list_books()
# ---------------------------------------------------------------------------

def test_list_books_prints_all_titles(session, capsys):
    """list_books() should print all book titles in the database."""
    list_books(session)

    output = capsys.readouterr().out
    assert "Test Book A" in output
    assert "Test Book B" in output


def test_list_books_shows_status(session, capsys):
    """list_books() should include the availability status of each book."""
    list_books(session)

    output = capsys.readouterr().out
    assert "available" in output
    assert "checked out" in output


def test_list_books_empty(empty_session, capsys):
    """list_books() should print a 'no books' message when the table is empty."""
    list_books(empty_session)

    output = capsys.readouterr().out
    assert "No books" in output


# ---------------------------------------------------------------------------
# Tests for CRUD operations via session
# ---------------------------------------------------------------------------

def test_create_book(engine):
    """Adding a Book to the session and committing should persist it."""
    with Session(engine) as sess:
        book = Book(title="Created Book", author="Creator", status="available")
        sess.add(book)
        sess.commit()

        # Verify it was saved by querying.
        found = sess.execute(
            select(Book).where(Book.title == "Created Book")
        ).scalars().first()

        assert found is not None
        assert found.author == "Creator"


def test_update_book_status(session):
    """Changing a Book's status attribute and committing should update the row."""
    book = session.execute(
        select(Book).where(Book.title == "Test Book A")
    ).scalars().first()

    assert book.status == "available"

    book.status = "checked out"
    session.commit()
    session.refresh(book)

    assert book.status == "checked out"


def test_delete_book(session):
    """Deleting a Book and committing should remove it from the database."""
    book = session.execute(
        select(Book).where(Book.title == "Test Book A")
    ).scalars().first()

    session.delete(book)
    session.commit()

    remaining = session.execute(select(Book)).scalars().all()
    titles = [b.title for b in remaining]

    assert "Test Book A" not in titles
    assert len(remaining) == 1


def test_get_by_primary_key(session):
    """session.get(Book, id) should return the book with that primary key.

    .get() is the fastest way to fetch a single row because it checks
    the identity map first (no SQL if the object is already loaded).
    """
    book = session.execute(select(Book)).scalars().first()
    book_id = book.id

    found = session.get(Book, book_id)

    assert found is not None
    assert found.title == book.title
