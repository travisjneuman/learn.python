"""
Migrations with Alembic — Models that Alembic will manage.

This file defines the Author and Book models for the library database.
The initial version has no 'genre' column on Book. You will add it via
an Alembic migration (see the README for step-by-step instructions).

Key concepts:
- Alembic tracks schema changes as versioned migration scripts
- autogenerate compares your models to the database and creates a script
- upgrade applies migrations forward; downgrade rolls them back
- Migrations are Python files — you can add data migrations too
"""

import os
from sqlalchemy import create_engine, select, ForeignKey, String, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


# ── Base ──────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── Models ────────────────────────────────────────────────────────────

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

    # ── UNCOMMENT FOR MIGRATION ──────────────────────────────────
    # After running "python project.py" once to create the initial database,
    # uncomment the next line, then run:
    #   alembic revision --autogenerate -m "add genre column to books"
    #   alembic upgrade head
    #
    # genre: Mapped[str | None] = mapped_column(String(50), nullable=True)

    author: Mapped["Author"] = relationship(back_populates="books")


# ── Database setup ────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def create_tables():
    """Create tables from models. Only used for initial setup.

    In production, you would NEVER use create_all() after the first deploy.
    Alembic handles all schema changes from that point on.
    """
    Base.metadata.create_all(ENGINE)


def insert_sample_data(session):
    """Insert sample authors and books."""
    # Check if data already exists.
    existing = session.execute(select(Author)).scalars().first()
    if existing:
        return

    david = Author(name="David Thomas")
    robert = Author(name="Robert C. Martin")
    luciano = Author(name="Luciano Ramalho")

    session.add_all([david, robert, luciano])
    session.flush()  # Get IDs assigned before creating books.

    books = [
        Book(title="The Pragmatic Programmer", year=1999, author_id=david.id),
        Book(title="Clean Code", year=2008, author_id=robert.id),
        Book(title="Fluent Python", year=2015, author_id=luciano.id),
    ]
    session.add_all(books)
    session.commit()


def show_books(session):
    """Print all books with their authors."""
    stmt = select(Book).order_by(Book.id)
    books = session.execute(stmt).scalars().all()
    for book in books:
        print(f"  {book.id} | {book.title:<28} | {book.author.name}")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    create_tables()

    with Session(ENGINE) as session:
        insert_sample_data(session)
        print("Tables created. Sample data inserted.")
        print("Books in database:")
        show_books(session)


if __name__ == "__main__":
    main()
