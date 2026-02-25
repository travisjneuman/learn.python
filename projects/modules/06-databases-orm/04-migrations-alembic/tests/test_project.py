"""Tests for Module 06 / Project 04 — Migrations with Alembic.

Tests the Author and Book models and the helper functions. Alembic
migration scripts themselves are not tested here (they are run manually),
but we verify the models work correctly with an in-memory database.

WHY not test Alembic migrations directly?
- Alembic migrations are run as CLI commands (alembic upgrade head).
- Testing them requires a real database file and a running Alembic environment.
- Instead, we test the models that Alembic manages, which gives us confidence
  that the schema is correct.
"""

import sys
import os

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import Base, Author, Book, insert_sample_data, show_books


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Create an in-memory database with all tables."""
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    """Create a session and insert sample data."""
    with Session(engine) as sess:
        insert_sample_data(sess)
        yield sess


# ---------------------------------------------------------------------------
# Tests for model creation
# ---------------------------------------------------------------------------

def test_tables_created(engine):
    """create_all() should create both 'authors' and 'books' tables."""
    table_names = list(Base.metadata.tables.keys())

    assert "authors" in table_names
    assert "books" in table_names


# ---------------------------------------------------------------------------
# Tests for insert_sample_data()
# ---------------------------------------------------------------------------

def test_insert_creates_authors(session):
    """insert_sample_data() should create 3 authors."""
    authors = session.execute(select(Author)).scalars().all()
    assert len(authors) == 3


def test_insert_creates_books(session):
    """insert_sample_data() should create 3 books (one per author)."""
    books = session.execute(select(Book)).scalars().all()
    assert len(books) == 3


def test_insert_is_idempotent(session):
    """Calling insert_sample_data() twice should not duplicate data.

    The function checks if data already exists before inserting.
    """
    insert_sample_data(session)  # Call again

    authors = session.execute(select(Author)).scalars().all()
    assert len(authors) == 3


# ---------------------------------------------------------------------------
# Tests for relationships
# ---------------------------------------------------------------------------

def test_book_has_author(session):
    """Each Book should have an .author relationship pointing to an Author."""
    book = session.execute(
        select(Book).where(Book.title == "Clean Code")
    ).scalars().first()

    assert book is not None
    assert book.author is not None
    assert book.author.name == "Robert C. Martin"


def test_author_has_books(session):
    """Each Author should have a .books list with their Book objects."""
    author = session.execute(
        select(Author).where(Author.name == "David Thomas")
    ).scalars().first()

    assert author is not None
    assert len(author.books) == 1
    assert author.books[0].title == "The Pragmatic Programmer"


# ---------------------------------------------------------------------------
# Tests for foreign key constraints
# ---------------------------------------------------------------------------

def test_book_author_id_is_set(session):
    """Every book should have a valid author_id that references an existing author."""
    books = session.execute(select(Book)).scalars().all()
    author_ids = {a.id for a in session.execute(select(Author)).scalars().all()}

    for book in books:
        assert book.author_id in author_ids


# ---------------------------------------------------------------------------
# Tests for show_books()
# ---------------------------------------------------------------------------

def test_show_books_prints_all_titles(session, capsys):
    """show_books() should print every book's title."""
    show_books(session)

    output = capsys.readouterr().out
    assert "The Pragmatic Programmer" in output
    assert "Clean Code" in output
    assert "Fluent Python" in output


def test_show_books_prints_author_names(session, capsys):
    """show_books() should print the author name for each book."""
    show_books(session)

    output = capsys.readouterr().out
    assert "David Thomas" in output
    assert "Robert C. Martin" in output
    assert "Luciano Ramalho" in output
