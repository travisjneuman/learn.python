"""
CRUD Operations — A library management system using SQLAlchemy.

This project builds an interactive CLI that lets you create, read, update,
and delete books in a SQLite database. It demonstrates the full lifecycle
of working with an ORM: defining models, opening sessions, making changes,
and committing or rolling back.

Key concepts:
- session.add(): stage a new object for insertion
- session.get(): fetch one row by primary key (fast, uses identity map)
- session.execute(select(...)): run a query that may return multiple rows
- session.delete(): mark an object for deletion
- session.commit(): save all staged changes to the database
- session.rollback(): undo all staged changes since the last commit
"""

import os
from sqlalchemy import create_engine, select, String, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)


# ── Models ────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    # Status is either "available" or "checked out".
    status: Mapped[str] = mapped_column(String(20), default="available")

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', status='{self.status}')"


# ── Database setup ────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)

SAMPLE_BOOKS = [
    Book(title="The Pragmatic Programmer", author="David Thomas", status="available"),
    Book(title="Clean Code", author="Robert C. Martin", status="available"),
    Book(title="Fluent Python", author="Luciano Ramalho", status="available"),
    Book(title="Python Crash Course", author="Eric Matthes", status="checked out"),
    Book(title="Design Patterns", author="Gang of Four", status="available"),
]


def init_db():
    """Create tables and insert sample data if the database is empty."""
    Base.metadata.create_all(ENGINE)
    with Session(ENGINE) as session:
        # Only insert sample data if the table is empty.
        count = session.execute(select(Book)).scalars().first()
        if count is None:
            session.add_all(SAMPLE_BOOKS)
            session.commit()


# ── CRUD functions ────────────────────────────────────────────────────
#
# Each function takes a session and performs one operation. This keeps
# the code organized and testable — you could call these from a web
# framework just as easily as from this CLI.

def list_books(session):
    """Read: show all books in the database."""
    books = session.execute(select(Book).order_by(Book.id)).scalars().all()

    if not books:
        print("No books in the library.")
        return

    print(f"\n{'All books:'}")
    print(f"  {'ID':>3} | {'Title':<28} | {'Author':<18} | {'Status'}")
    print(f"  {'---':>3}+{'------------------------------':>30}+{'--------------------':>20}+-----------")
    for book in books:
        print(f"  {book.id:>3} | {book.title:<28} | {book.author:<18} | {book.status}")


def search_books(session):
    """Read: search books by title or author."""
    term = input("Search term: ").strip()
    if not term:
        print("No search term entered.")
        return

    # ilike() does a case-insensitive LIKE search.
    # The % wildcards match any characters before and after the term.
    stmt = select(Book).where(
        Book.title.ilike(f"%{term}%") | Book.author.ilike(f"%{term}%")
    )
    books = session.execute(stmt).scalars().all()

    if not books:
        print(f"No books matching '{term}'.")
        return

    print(f"\nResults for '{term}':")
    for book in books:
        print(f"  {book.id:>3} | {book.title:<28} | {book.author:<18} | {book.status}")


def add_book(session):
    """Create: add a new book to the database."""
    title = input("Title: ").strip()
    author = input("Author: ").strip()

    if not title or not author:
        print("Title and author are required.")
        return

    book = Book(title=title, author=author, status="available")
    session.add(book)
    session.commit()
    print(f"Added '{title}' by {author} (ID: {book.id}).")


def update_status(session):
    """Update: change a book's availability status."""
    raw_id = input("Book ID to update: ").strip()

    # Validate input: must be a positive integer.
    try:
        book_id = int(raw_id)
    except ValueError:
        print(f"'{raw_id}' is not a valid ID.")
        return

    # session.get() fetches by primary key. Returns None if not found.
    book = session.get(Book, book_id)
    if book is None:
        print(f"No book with ID {book_id}.")
        return

    new_status = input("New status (available / checked out): ").strip().lower()
    if new_status not in ("available", "checked out"):
        print(f"Invalid status: '{new_status}'. Use 'available' or 'checked out'.")
        return

    # Just set the attribute — SQLAlchemy tracks the change.
    book.status = new_status
    session.commit()
    print(f"Updated '{book.title}' to '{new_status}'.")


def delete_book(session):
    """Delete: remove a book from the database."""
    raw_id = input("Book ID to delete: ").strip()

    try:
        book_id = int(raw_id)
    except ValueError:
        print(f"'{raw_id}' is not a valid ID.")
        return

    book = session.get(Book, book_id)
    if book is None:
        print(f"No book with ID {book_id}.")
        return

    title = book.title
    session.delete(book)
    session.commit()
    print(f"Deleted '{title}'.")


# ── Menu loop ─────────────────────────────────────────────────────────
#
# A simple dictionary maps choices to functions. This is cleaner than
# a long if/elif chain and makes it easy to add new options.

MENU = """
Library Management System
=========================

  [1] List all books
  [2] Search books
  [3] Add a book
  [4] Update book status
  [5] Delete a book
  [6] Quit
"""


def main():
    init_db()

    # Map menu choices to functions.
    # Each function takes a session as its only argument.
    actions = {
        "1": list_books,
        "2": search_books,
        "3": add_book,
        "4": update_status,
        "5": delete_book,
    }

    print(MENU)

    with Session(ENGINE) as session:
        while True:
            choice = input("Choice: ").strip()

            if choice == "6":
                print("Goodbye!")
                break

            action = actions.get(choice)
            if action is None:
                print(f"Invalid choice: '{choice}'. Enter 1-6.")
                continue

            try:
                action(session)
            except Exception as e:
                # If anything goes wrong, rollback so the session stays clean.
                session.rollback()
                print(f"Error: {e}")

            print()  # Blank line between actions for readability.


if __name__ == "__main__":
    main()
