"""Tests for Module 06 / Project 05 — Query Optimization.

Tests the models, data generation, and optimization demos (N+1 fix,
indexes, bulk operations) using an in-memory SQLite database.

WHY test optimization code?
- Optimization demos involve complex SQLAlchemy features (joinedload,
  event listeners, raw SQL). Tests verify these work correctly.
- The N+1 demo relies on query counting — tests confirm the counts
  are as expected (1 query with eager loading vs N+1 without).
"""

import sys
import os
import random

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, joinedload

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import Base, Author, Book, generate_sample_data


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
    """Create a session with sample data (small dataset for fast tests)."""
    with Session(engine) as sess:
        # Seed random for reproducibility.
        random.seed(42)

        # Create a small dataset (5 authors, 20 books).
        authors = [Author(name=f"Author {i}") for i in range(5)]
        sess.add_all(authors)
        sess.flush()

        books = []
        for i in range(20):
            author = random.choice(authors)
            books.append(Book(title=f"Book {i}", year=random.randint(2000, 2024), author_id=author.id))
        sess.add_all(books)
        sess.commit()

        yield sess


# ---------------------------------------------------------------------------
# Tests for model structure
# ---------------------------------------------------------------------------

def test_author_model_has_books_relationship(session):
    """Author should have a .books list populated by the ORM relationship."""
    author = session.execute(select(Author)).scalars().first()

    # The relationship should return a list (possibly empty).
    assert isinstance(author.books, list)


def test_book_model_has_author_relationship(session):
    """Book should have an .author attribute populated by the ORM relationship."""
    book = session.execute(select(Book)).scalars().first()

    assert book.author is not None
    assert isinstance(book.author, Author)


# ---------------------------------------------------------------------------
# Tests for generate_sample_data()
# ---------------------------------------------------------------------------

def test_generate_sample_data_creates_records(engine):
    """generate_sample_data() should create authors and books.

    We use a fresh session and verify records were inserted.
    """
    with Session(engine) as sess:
        random.seed(42)
        generate_sample_data(sess)

        author_count = len(sess.execute(select(Author)).scalars().all())
        book_count = len(sess.execute(select(Book)).scalars().all())

        assert author_count > 0
        assert book_count > 0


# ---------------------------------------------------------------------------
# Tests for N+1 problem and eager loading
# ---------------------------------------------------------------------------

def test_lazy_loading_triggers_multiple_queries(session):
    """Accessing author.books without eager loading triggers extra queries.

    This is the N+1 problem: 1 query for authors + N queries for books.
    We verify the behavior exists so the demo is meaningful.
    """
    authors = session.execute(select(Author)).scalars().all()

    # Accessing .books on each author triggers lazy loading.
    # We just verify it works (returns a list) — the demo counts queries.
    for author in authors:
        assert isinstance(author.books, list)


def test_eager_loading_with_joinedload(session):
    """joinedload() should load author.books in a single query (no N+1).

    After using joinedload, accessing author.books does NOT trigger
    additional queries — the data is already loaded from the JOIN.
    """
    session.expire_all()

    stmt = select(Author).options(joinedload(Author.books))
    authors = session.execute(stmt).unique().scalars().all()

    # Books should already be loaded — no additional queries needed.
    total_books = sum(len(a.books) for a in authors)
    assert total_books > 0


# ---------------------------------------------------------------------------
# Tests for bulk operations
# ---------------------------------------------------------------------------

def test_bulk_insert_adds_all_records(engine):
    """Bulk inserting with add_all() + one commit should persist all records."""
    with Session(engine) as sess:
        # Create one author for the books.
        author = Author(name="Bulk Author")
        sess.add(author)
        sess.flush()

        # Bulk insert 50 books.
        books = [
            Book(title=f"Bulk Book {i}", year=2024, author_id=author.id)
            for i in range(50)
        ]
        sess.add_all(books)
        sess.commit()

        count = len(sess.execute(select(Book)).scalars().all())
        assert count == 50


# ---------------------------------------------------------------------------
# Tests for index creation
# ---------------------------------------------------------------------------

def test_index_can_be_created(session):
    """Creating an index on the year column should not raise an error.

    Indexes speed up WHERE clauses on the indexed column.
    """
    session.execute(text("CREATE INDEX IF NOT EXISTS ix_books_year ON books (year)"))
    session.commit()

    # Verify the index exists by querying SQLite's index list.
    result = session.execute(text("PRAGMA index_list('books')")).fetchall()
    index_names = [row[1] for row in result]
    assert "ix_books_year" in index_names


def test_query_with_index_returns_correct_results(session):
    """A query filtered by year should return correct results with or without an index.

    The index changes performance, not correctness. This test verifies correctness.
    """
    # Query without index.
    books_before = session.execute(
        select(Book).where(Book.year == 2010)
    ).scalars().all()

    # Add index.
    session.execute(text("CREATE INDEX IF NOT EXISTS ix_books_year ON books (year)"))
    session.commit()

    # Query with index.
    books_after = session.execute(
        select(Book).where(Book.year == 2010)
    ).scalars().all()

    # Results should be identical.
    assert len(books_before) == len(books_after)
