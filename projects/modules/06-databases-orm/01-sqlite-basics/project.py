"""
SQLite Basics — Raw SQL with Python's built-in sqlite3 module.

This project creates a small books database, inserts sample data,
and demonstrates different ways to query it. The key lesson is
parameterized queries: never build SQL strings with f-strings or
.format() — always use ? placeholders to prevent SQL injection.

Key concepts:
- sqlite3.connect(): opens (or creates) a database file
- cursor.execute(): runs a single SQL statement
- cursor.fetchall(): retrieves all rows from the last query
- conn.commit(): saves changes to disk (INSERT/UPDATE/DELETE need this)
- parameterized queries: use ? placeholders, pass values as a tuple
"""

import os
import sqlite3


# ── Database setup ────────────────────────────────────────────────────
#
# We store the database file in a data/ subdirectory to keep things tidy.
# os.makedirs with exist_ok=True creates the directory if it doesn't exist.

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "books.db")


def create_connection():
    """Open a connection to the SQLite database file.

    sqlite3.connect() creates the file if it doesn't exist.
    Setting row_factory to sqlite3.Row lets us access columns by name.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # This makes rows behave like dictionaries — row["title"] works.
    conn.row_factory = sqlite3.Row
    return conn


# ── Create the table ──────────────────────────────────────────────────
#
# CREATE TABLE IF NOT EXISTS is safe to run multiple times.
# Each column has a type: INTEGER, TEXT, etc. SQLite is flexible about
# types, but declaring them is good practice.

def create_table(conn):
    """Create the books table if it doesn't already exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            author TEXT   NOT NULL,
            year  INTEGER NOT NULL
        )
    """)
    conn.commit()
    print("Table 'books' created.")


# ── Insert sample data ───────────────────────────────────────────────
#
# executemany() runs the same INSERT for each tuple in the list.
# The ? placeholders get replaced with the tuple values — this is a
# parameterized query. SQLite handles escaping, so special characters
# in the data cannot break the SQL.

SAMPLE_BOOKS = [
    ("The Pragmatic Programmer", "David Thomas", 1999),
    ("Clean Code", "Robert C. Martin", 2008),
    ("Fluent Python", "Luciano Ramalho", 2015),
    ("Python Crash Course", "Eric Matthes", 2015),
    ("Design Patterns", "Gang of Four", 1994),
    ("Refactoring", "Martin Fowler", 1999),
]


def insert_sample_books(conn):
    """Insert sample books into the database."""
    conn.executemany(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        SAMPLE_BOOKS,
    )
    conn.commit()
    print(f"Inserted {len(SAMPLE_BOOKS)} books.")


# ── Display helpers ───────────────────────────────────────────────────

def print_books(rows):
    """Print a list of book rows in a readable format."""
    for row in rows:
        print(f"  {row['id']:>2} | {row['title']:<28} | {row['author']:<18} | {row['year']}")


# ── Query functions ───────────────────────────────────────────────────
#
# Each function demonstrates a different kind of SELECT query.
# Notice that every query uses ? placeholders for user-provided values.

def get_all_books(conn):
    """Fetch every book in the table, ordered by ID."""
    cursor = conn.execute("SELECT * FROM books ORDER BY id")
    return cursor.fetchall()


def get_books_by_year(conn, year):
    """Fetch books published in a specific year.

    The (year,) is a one-element tuple. The trailing comma is required —
    without it, Python treats the parentheses as grouping, not a tuple.
    """
    cursor = conn.execute(
        "SELECT * FROM books WHERE year = ?",
        (year,),  # <-- parameterized: safe from injection
    )
    return cursor.fetchall()


def search_books_by_title(conn, search_term):
    """Search for books whose title contains the search term.

    The LIKE operator with % wildcards does partial matching.
    We wrap the search term in % on both sides to match anywhere in the title.
    """
    cursor = conn.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        (f"%{search_term}%",),
    )
    return cursor.fetchall()


def get_books_by_author(conn, author):
    """Fetch books by a specific author.

    This is the simplest parameterized query — exact match on one column.
    """
    cursor = conn.execute(
        "SELECT * FROM books WHERE author = ?",
        (author,),
    )
    return cursor.fetchall()


# ── SQL injection demo ───────────────────────────────────────────────
#
# This shows what WOULD happen if you used string formatting instead of
# parameterized queries. With parameterized queries, the dangerous input
# is treated as a plain string value, not as SQL code.

def demo_safe_query(conn, dangerous_input):
    """Show that parameterized queries handle dangerous input safely."""
    print(f"Searching for: {dangerous_input}")
    cursor = conn.execute(
        "SELECT * FROM books WHERE author = ?",
        (dangerous_input,),
    )
    rows = cursor.fetchall()
    if rows:
        print_books(rows)
    else:
        print("No books found (and the table still exists!).")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    # Remove old database so we start fresh each run.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = create_connection()

    print("--- Creating database and table ---")
    create_table(conn)

    print("\n--- Inserting sample books ---")
    insert_sample_books(conn)

    print("\n--- All books ---")
    print_books(get_all_books(conn))

    print("\n--- Books by year 2015 ---")
    print_books(get_books_by_year(conn, 2015))

    print("\n--- Books with 'Python' in the title ---")
    print_books(search_books_by_title(conn, "Python"))

    print("\n--- Parameterized query demo ---")
    author = "Robert C. Martin"
    print(f"Searching for author: {author}")
    print_books(get_books_by_author(conn, author))

    print("\n--- Dangerous input safely handled ---")
    demo_safe_query(conn, "'; DROP TABLE books; --")

    # Always close the connection when done.
    conn.close()


if __name__ == "__main__":
    main()
