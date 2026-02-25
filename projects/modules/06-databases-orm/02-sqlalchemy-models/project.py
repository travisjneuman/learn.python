"""
SQLAlchemy Models — Defining tables as Python classes.

This project shows how SQLAlchemy's ORM lets you work with database rows
as Python objects. Instead of writing CREATE TABLE and INSERT INTO by hand,
you define classes that map to tables and let SQLAlchemy generate the SQL.

Key concepts:
- DeclarativeBase: the base class all your models inherit from
- Mapped / mapped_column: declare column types with Python type hints
- relationship(): define how models connect to each other
- create_engine(): set up the database connection
- Session: a workspace for talking to the database (add, query, commit)

SQLAlchemy 2.0 style — uses the modern mapped_column syntax, not the
older Column() style you may see in tutorials written before 2023.
"""

import os
from sqlalchemy import create_engine, select, func, ForeignKey, String, Integer, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


# ── Define the base class ─────────────────────────────────────────────
#
# All models inherit from this. DeclarativeBase replaces the older
# declarative_base() function from SQLAlchemy 1.x.

class Base(DeclarativeBase):
    pass


# ── Author model ──────────────────────────────────────────────────────
#
# Each Author has an id and a name. The "books" relationship creates a
# Python list of Book objects on each Author instance. You never have to
# write a JOIN yourself — just access author.books.

class Author(Base):
    __tablename__ = "authors"

    # Mapped[int] tells SQLAlchemy (and your editor) the column type.
    # mapped_column() configures the database column.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # One-to-many: one author has many books.
    # back_populates links this relationship to Book.author.
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"


# ── Book model ────────────────────────────────────────────────────────
#
# Each Book belongs to one Author via author_id (a foreign key).
# The "author" relationship gives you the Author object directly —
# book.author.name works without writing any SQL.

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # ForeignKey points to the authors table's id column.
    # This is how the database enforces that every book has a valid author.
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    # Many-to-one: each book has one author.
    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', year={self.year})"


# ── Database setup ────────────────────────────────────────────────────

# The database file lives next to this script.
DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")
# "echo=False" silences SQL logging. Set to True to see every SQL statement.
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def create_tables():
    """Create all tables defined by models that inherit from Base."""
    # This generates CREATE TABLE statements from your model definitions.
    Base.metadata.create_all(ENGINE)
    table_names = list(Base.metadata.tables.keys())
    print(f"Tables created: {', '.join(table_names)}")


# ── Insert sample data ───────────────────────────────────────────────

def insert_sample_data(session):
    """Create authors and books, demonstrating the ORM insert pattern."""

    # Create Author objects. No SQL runs yet — these are just Python objects.
    david = Author(name="David Thomas")
    robert = Author(name="Robert C. Martin")
    luciano = Author(name="Luciano Ramalho")

    # Create Book objects and assign them to authors.
    # Setting author=david automatically sets author_id when committed.
    davids_books = [
        Book(title="The Pragmatic Programmer", year=1999, author=david),
        Book(title="Programming Pearls", year=2000, author=david),
    ]
    roberts_books = [
        Book(title="Clean Code", year=2008, author=robert),
        Book(title="Clean Architecture", year=2017, author=robert),
        Book(title="The Clean Coder", year=2011, author=robert),
    ]
    lucianos_books = [
        Book(title="Fluent Python", year=2015, author=luciano),
        Book(title="Fluent Python 2nd Ed", year=2022, author=luciano),
    ]

    # session.add_all() stages all objects for insertion.
    # SQLAlchemy figures out the correct INSERT order (authors first, then books).
    all_books = davids_books + roberts_books + lucianos_books
    session.add_all([david, robert, luciano])
    session.add_all(all_books)

    # commit() sends the INSERT statements to the database and saves them.
    session.commit()
    print(f"Added {len([david, robert, luciano])} authors with {len(all_books)} books total.")


# ── Query demonstrations ─────────────────────────────────────────────

def show_all_authors(session):
    """Print every author and their books using the ORM relationship."""
    # select() builds a SELECT statement. scalars() returns model objects.
    authors = session.execute(select(Author).order_by(Author.name)).scalars().all()

    for author in authors:
        print(f"  Author: {author.name}")
        # author.books is a Python list — SQLAlchemy loads it automatically.
        for book in author.books:
            print(f"    - {book.title} ({book.year})")


def query_books_after_year(session, year):
    """Find books published after a given year, showing the join."""
    # The ORM automatically joins authors and books when you access book.author.
    stmt = (
        select(Book)
        .where(Book.year > year)
        .order_by(Book.year)
    )
    books = session.execute(stmt).scalars().all()

    for book in books:
        # book.author.name triggers a lazy load if not already loaded.
        print(f"  {book.title} ({book.year}) by {book.author.name}")


def query_prolific_authors(session, min_books):
    """Find authors with more than a certain number of books.

    This demonstrates GROUP BY and HAVING through the ORM.
    func.count() generates COUNT() in SQL.
    """
    stmt = (
        select(Author.name, func.count(Book.id).label("book_count"))
        .join(Book)
        .group_by(Author.id)
        .having(func.count(Book.id) > min_books)
    )
    results = session.execute(stmt).all()

    for name, count in results:
        print(f"  {name} ({count} books)")


def compare_orm_vs_raw(session):
    """Show that ORM queries produce the same results as raw SQL.

    This helps you understand what the ORM generates under the hood.
    """
    # ORM query
    orm_books = session.execute(
        select(Book.title).where(Book.year > 2010).order_by(Book.title)
    ).scalars().all()

    # Raw SQL query (using text() for safety)
    raw_books = session.execute(
        text("SELECT title FROM books WHERE year > :year ORDER BY title"),
        {"year": 2010},
    ).scalars().all()

    if orm_books == raw_books:
        print("ORM query returned the same results as raw SQL.")
    else:
        print("Results differ — something is wrong!")
        print(f"  ORM: {orm_books}")
        print(f"  Raw: {raw_books}")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    # Clean up from previous runs.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    print("--- Creating tables ---")
    create_tables()

    # Session is a context manager — it auto-closes when the block ends.
    with Session(ENGINE) as session:
        print("\n--- Inserting authors and books ---")
        insert_sample_data(session)

        print("\n--- All authors ---")
        show_all_authors(session)

        print("\n--- Query: books after 2010 ---")
        query_books_after_year(session, 2010)

        print("\n--- Query: authors with more than 2 books ---")
        query_prolific_authors(session, 2)

        print("\n--- ORM vs raw SQL comparison ---")
        compare_orm_vs_raw(session)


if __name__ == "__main__":
    main()
