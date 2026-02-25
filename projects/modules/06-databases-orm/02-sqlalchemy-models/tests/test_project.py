"""Tests for Module 06 / Project 02 — SQLAlchemy Models.

Tests the Author and Book models, relationships, and query functions
using an in-memory SQLite database.

WHY test ORM models?
- Models define your data schema. If a column type or relationship is wrong,
  the database will not work correctly.
- Testing inserts, queries, and relationships catches schema mismatches early.
"""

import sys
import os

import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import (
    Base,
    Author,
    Book,
    insert_sample_data,
    show_all_authors,
    query_books_after_year,
    query_prolific_authors,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Create an in-memory SQLite engine with all tables."""
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture
def session(engine):
    """Create a session and insert sample data.

    Yields the session for use in tests, then closes it.
    """
    with Session(engine) as sess:
        insert_sample_data(sess)
        yield sess


# ---------------------------------------------------------------------------
# Tests for model definitions
# ---------------------------------------------------------------------------

def test_author_table_name():
    """The Author model should map to the 'authors' table."""
    assert Author.__tablename__ == "authors"


def test_book_table_name():
    """The Book model should map to the 'books' table."""
    assert Book.__tablename__ == "books"


# ---------------------------------------------------------------------------
# Tests for insert_sample_data()
# ---------------------------------------------------------------------------

def test_insert_creates_authors(session):
    """insert_sample_data() should create 3 authors."""
    authors = session.execute(select(Author)).scalars().all()
    assert len(authors) == 3


def test_insert_creates_books(session):
    """insert_sample_data() should create 7 books total."""
    books = session.execute(select(Book)).scalars().all()
    assert len(books) == 7


# ---------------------------------------------------------------------------
# Tests for ORM relationships
# ---------------------------------------------------------------------------

def test_author_has_books_relationship(session):
    """Each Author object should have a .books list populated by the relationship.

    This tests the one-to-many relationship: one author has many books.
    """
    # Robert C. Martin should have 3 books.
    robert = session.execute(
        select(Author).where(Author.name == "Robert C. Martin")
    ).scalars().first()

    assert robert is not None
    assert len(robert.books) == 3


def test_book_has_author_relationship(session):
    """Each Book object should have an .author attribute set by the relationship.

    This tests the many-to-one side: each book belongs to one author.
    """
    book = session.execute(
        select(Book).where(Book.title == "Clean Code")
    ).scalars().first()

    assert book is not None
    assert book.author.name == "Robert C. Martin"


# ---------------------------------------------------------------------------
# Tests for query functions
# ---------------------------------------------------------------------------

def test_query_books_after_year(session, capsys):
    """query_books_after_year(2010) should find books published after 2010.

    The sample data has books from 2011, 2015, 2017, 2022. All should appear.
    """
    query_books_after_year(session, 2010)

    output = capsys.readouterr().out
    # At least these should appear.
    assert "Clean Architecture" in output or "2017" in output
    assert "Fluent Python" in output or "2015" in output


def test_query_prolific_authors(session, capsys):
    """query_prolific_authors(2) should find authors with more than 2 books.

    Robert C. Martin has 3 books, so he should appear. Others should not.
    """
    query_prolific_authors(session, 2)

    output = capsys.readouterr().out
    assert "Robert C. Martin" in output


# ---------------------------------------------------------------------------
# Tests for model __repr__
# ---------------------------------------------------------------------------

def test_author_repr(session):
    """Author.__repr__() should include the id and name."""
    author = session.execute(select(Author)).scalars().first()
    repr_str = repr(author)

    assert "Author" in repr_str
    assert author.name in repr_str


def test_book_repr(session):
    """Book.__repr__() should include the id, title, and year."""
    book = session.execute(select(Book)).scalars().first()
    repr_str = repr(book)

    assert "Book" in repr_str
    assert book.title in repr_str
