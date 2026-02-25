"""
Query Optimization — Finding and fixing slow database patterns.

This project creates a database with 1000+ rows and demonstrates three
common performance lessons:

1. The N+1 problem: accessing a relationship inside a loop fires one
   query per row. Fix it with eager loading (joinedload).
2. Indexes: without an index, the database scans every row. With an
   index, it jumps straight to matching rows.
3. Bulk operations: inserting rows one at a time is much slower than
   inserting them in bulk.

Key concepts:
- joinedload(): load related objects in the same query (no extra queries)
- Index(): add a database index to speed up searches on a column
- EXPLAIN: a SQL command that shows HOW the database plans to execute a query
- time.perf_counter(): high-resolution timer for measuring code speed
"""

import os
import time
import random
from sqlalchemy import (
    create_engine,
    select,
    text,
    event,
    ForeignKey,
    String,
    Integer,
    Index,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    joinedload,
)


# ── Models ────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")


# ── Database setup ────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "benchmark.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Number of authors and books to generate.
NUM_AUTHORS = 50
NUM_BOOKS = 1000

BOOK_WORDS = [
    "Python", "Advanced", "Learning", "Data", "Web", "Systems",
    "Patterns", "Modern", "Practical", "Essential", "Mastering",
    "Introduction", "Guide", "Handbook", "Complete", "Professional",
]


def generate_sample_data(session):
    """Insert a large dataset for benchmarking.

    Creates NUM_AUTHORS authors and NUM_BOOKS books with random
    titles and years. Each book is assigned to a random author.
    """
    authors = []
    for i in range(NUM_AUTHORS):
        authors.append(Author(name=f"Author {i + 1}"))

    session.add_all(authors)
    session.flush()  # Get IDs assigned.

    books = []
    for i in range(NUM_BOOKS):
        # Random title from two words.
        title = f"{random.choice(BOOK_WORDS)} {random.choice(BOOK_WORDS)} {i + 1}"
        year = random.randint(1990, 2024)
        author = random.choice(authors)
        books.append(Book(title=title, year=year, author_id=author.id))

    session.add_all(books)
    session.commit()

    print(f"Database created with {NUM_AUTHORS} authors and {NUM_BOOKS} books.")


# ── Query counter ─────────────────────────────────────────────────────
#
# This hooks into SQLAlchemy's event system to count how many SQL
# statements are executed. This makes the N+1 problem visible.

query_count = 0


def count_queries(conn, cursor, statement, parameters, context, executemany):
    """Event listener that increments the query counter."""
    global query_count
    query_count += 1


def reset_query_count():
    """Reset the counter to zero before a new measurement."""
    global query_count
    query_count = 0


# Register the listener on our engine.
event.listen(ENGINE, "before_cursor_execute", count_queries)


# ── Demo 1: N+1 problem ──────────────────────────────────────────────
#
# The N+1 problem happens when you load a list of objects (1 query),
# then access a relationship on each object (N more queries).
# Total: 1 + N queries, where N is the number of objects.

def demo_n_plus_one(session):
    """Show the N+1 problem and its fix."""
    print("--- Demo 1: The N+1 problem ---")

    # ── The slow way: N+1 queries ─────────────────────────────────
    #
    # This looks innocent: load all authors, then print their books.
    # But accessing author.books triggers a NEW query for EACH author.

    reset_query_count()
    start = time.perf_counter()

    # 1 query: SELECT * FROM authors
    authors = session.execute(select(Author)).scalars().all()

    total_books = 0
    for author in authors:
        # N queries: SELECT * FROM books WHERE author_id = ? (one per author)
        total_books += len(author.books)

    elapsed_n1 = time.perf_counter() - start
    queries_n1 = query_count

    print(f"N+1 approach: {queries_n1} queries in ~{elapsed_n1:.3f}s")
    print(f"  (1 query for authors + {queries_n1 - 1} queries for each author's books)")

    # ── Expire all objects so the eager-load test starts fresh ────
    session.expire_all()

    # ── The fast way: eager loading ───────────────────────────────
    #
    # joinedload() tells SQLAlchemy to load the books IN THE SAME QUERY
    # as the authors, using a SQL JOIN. One query instead of N+1.

    reset_query_count()
    start = time.perf_counter()

    # 1 query: SELECT * FROM authors JOIN books ON ...
    stmt = select(Author).options(joinedload(Author.books))
    authors = session.execute(stmt).unique().scalars().all()

    total_books = 0
    for author in authors:
        # No extra queries — books are already loaded!
        total_books += len(author.books)

    elapsed_eager = time.perf_counter() - start
    queries_eager = query_count

    print(f"\nEager loading: {queries_eager} query in ~{elapsed_eager:.3f}s")
    print(f"  (1 query with JOIN loads everything at once)")

    if elapsed_n1 > 0 and elapsed_eager > 0:
        speedup = elapsed_n1 / elapsed_eager
        print(f"\nSpeedup: ~{speedup:.0f}x faster with eager loading.")


# ── Demo 2: Index performance ─────────────────────────────────────────
#
# A database index is like an index in a book: it lets the database jump
# directly to matching rows instead of scanning every row in the table.

def demo_indexes(session):
    """Show the difference an index makes on search speed."""
    print("\n--- Demo 2: Index performance ---")

    search_year = 2010

    # ── Search WITHOUT an index ───────────────────────────────────
    start = time.perf_counter()
    for _ in range(100):  # Run 100 times to get measurable time.
        session.execute(
            select(Book).where(Book.year == search_year)
        ).scalars().all()
    elapsed_no_index = time.perf_counter() - start

    # Show the query plan without index.
    plan_no_index = session.execute(
        text(f"EXPLAIN QUERY PLAN SELECT * FROM books WHERE year = {search_year}")
    ).fetchall()

    print(f"Search without index: {elapsed_no_index:.4f}s (100 queries)")

    # Show EXPLAIN output.
    print("\nEXPLAIN without index:")
    for row in plan_no_index:
        print(f"  {row[-1]}")  # The last column has the human-readable plan.

    # ── Add an index on the year column ───────────────────────────
    #
    # This creates a B-tree index that the database uses to find rows
    # by year without scanning the entire table.
    session.execute(text("CREATE INDEX IF NOT EXISTS ix_books_year ON books (year)"))
    session.commit()

    # ── Search WITH the index ─────────────────────────────────────
    start = time.perf_counter()
    for _ in range(100):
        session.execute(
            select(Book).where(Book.year == search_year)
        ).scalars().all()
    elapsed_with_index = time.perf_counter() - start

    # Show the query plan with index.
    plan_with_index = session.execute(
        text(f"EXPLAIN QUERY PLAN SELECT * FROM books WHERE year = {search_year}")
    ).fetchall()

    print(f"\nSearch with index:    {elapsed_with_index:.4f}s (100 queries)")

    print("\nEXPLAIN with index:")
    for row in plan_with_index:
        print(f"  {row[-1]}")


# ── Demo 3: Bulk operations ──────────────────────────────────────────
#
# Inserting rows one at a time commits after each insert, which is slow.
# Inserting in bulk batches all the work into one transaction.

def demo_bulk_operations(session):
    """Show the speed difference between one-at-a-time and bulk inserts."""
    print("\n--- Demo 3: Bulk operations ---")

    count = 500

    # Get a valid author_id to use.
    author = session.execute(select(Author)).scalars().first()
    author_id = author.id

    # ── One at a time ─────────────────────────────────────────────
    start = time.perf_counter()
    for i in range(count):
        book = Book(title=f"Single Insert {i}", year=2020, author_id=author_id)
        session.add(book)
        session.commit()  # Commits after EACH insert — slow!
    elapsed_single = time.perf_counter() - start

    print(f"Insert {count} books one-at-a-time: {elapsed_single:.3f}s")

    # ── Bulk insert ───────────────────────────────────────────────
    start = time.perf_counter()
    books = [
        Book(title=f"Bulk Insert {i}", year=2021, author_id=author_id)
        for i in range(count)
    ]
    session.add_all(books)
    session.commit()  # One commit for all inserts — fast!
    elapsed_bulk = time.perf_counter() - start

    print(f"Insert {count} books in bulk:       {elapsed_bulk:.3f}s")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    # Clean up from previous runs.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Create tables.
    Base.metadata.create_all(ENGINE)

    print(f"--- Setting up database with {NUM_AUTHORS} authors and {NUM_BOOKS} books ---")

    with Session(ENGINE) as session:
        # Seed random for reproducible results.
        random.seed(42)
        generate_sample_data(session)

        print()
        demo_n_plus_one(session)

        print()
        demo_indexes(session)

        demo_bulk_operations(session)


if __name__ == "__main__":
    main()
