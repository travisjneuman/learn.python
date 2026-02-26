# SQLite Basics — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently. The goal is to create a SQLite database, insert data, and query it using parameterized queries. If you can create a table and insert one row, you are on the right track.

## Thinking Process

A database stores data in tables — like spreadsheets with rows and columns. SQLite is special because it is built into Python (no server to install) and stores everything in a single file. The workflow is always the same: connect to the database, execute SQL statements, and commit your changes.

The most important lesson in this project is not SQL syntax — it is parameterized queries. When you build SQL strings by concatenating user input (`f"WHERE name = '{user_input}'"`, you create a SQL injection vulnerability: a malicious user can type something that breaks out of the string and runs arbitrary SQL commands. Parameterized queries (`WHERE name = ?` with values passed separately) make this impossible because the database treats the values as data, never as code.

Think of it like filling out a form. String concatenation is like letting someone write directly on the form — they could scribble over the instructions. Parameterized queries are like having pre-printed fields where the user can only write inside the boxes.

## Step 1: Connect to the Database

**What to do:** Use `sqlite3.connect()` to open a database file and set up the connection.

**Why:** `sqlite3.connect()` opens an existing database or creates a new one if the file does not exist. Setting `row_factory = sqlite3.Row` lets you access columns by name (`row["title"]`) instead of by index (`row[0]`), which makes your code far more readable.

```python
import os
import sqlite3

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "books.db")

def create_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
```

**Predict:** What happens if you call `sqlite3.connect("books.db")` without creating the `data/` directory first? Where does the file get created?

## Step 2: Create a Table

**What to do:** Execute a `CREATE TABLE IF NOT EXISTS` statement to define the schema.

**Why:** A table defines the structure of your data — what columns exist, what types they hold, and what constraints apply. `IF NOT EXISTS` makes the statement safe to run multiple times — it only creates the table the first time. `conn.commit()` saves the change to disk.

```python
def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            author TEXT   NOT NULL,
            year  INTEGER NOT NULL
        )
    """)
    conn.commit()
```

Four things to notice:

- **`INTEGER PRIMARY KEY AUTOINCREMENT`** gives each row a unique ID that increases automatically. You never set it manually.
- **`TEXT NOT NULL`** means this column must contain text and cannot be empty.
- **Triple-quoted strings** let you write multi-line SQL that is easy to read.
- **`conn.commit()`** is required — without it, the table creation is not saved to disk.

**Predict:** What happens if you remove `NOT NULL` from the title column and then try to insert a row with no title?

## Step 3: Insert Data with Parameterized Queries

**What to do:** Use `executemany()` with `?` placeholders to insert multiple rows safely.

**Why:** `executemany()` runs the same INSERT statement for each tuple in a list. The `?` placeholders get replaced with the tuple values by SQLite — this is a parameterized query. SQLite handles escaping, so special characters in the data (like apostrophes in "O'Reilly") cannot break the SQL.

```python
SAMPLE_BOOKS = [
    ("The Pragmatic Programmer", "David Thomas", 1999),
    ("Clean Code", "Robert C. Martin", 2008),
    ("Fluent Python", "Luciano Ramalho", 2015),
]

def insert_sample_books(conn):
    conn.executemany(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        SAMPLE_BOOKS,
    )
    conn.commit()
```

**Predict:** What happens if you forget `conn.commit()` after inserting? The data appears in memory during the session, but what happens when you close and reopen the connection?

## Step 4: Query Data with SELECT and WHERE

**What to do:** Write functions that query the database using parameterized `WHERE` clauses.

**Why:** `SELECT` retrieves data. `WHERE` filters rows. Always use `?` placeholders for user-provided values — never put variables directly into the SQL string. `cursor.fetchall()` returns all matching rows.

```python
def get_books_by_year(conn, year):
    cursor = conn.execute(
        "SELECT * FROM books WHERE year = ?",
        (year,),
    )
    return cursor.fetchall()

def search_books_by_title(conn, search_term):
    cursor = conn.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        (f"%{search_term}%",),
    )
    return cursor.fetchall()
```

Two details to notice:

- **`(year,)`** is a one-element tuple. The trailing comma is required — without it, `(year)` is just parentheses around the variable, not a tuple.
- **`LIKE` with `%` wildcards** does partial matching. `%Python%` matches any title containing "Python" anywhere.

**Predict:** If you pass `"'; DROP TABLE books; --"` as the `search_term`, what happens? Does the table get dropped?

## Step 5: Demonstrate SQL Injection Safety

**What to do:** Pass a malicious string through a parameterized query and show that it is harmless.

**Why:** This is the whole point of parameterized queries. The dangerous string `'; DROP TABLE books; --` is treated as a plain text value to search for, not as SQL code to execute. The database looks for a book authored by that exact string, finds nothing, and your table is untouched.

```python
def demo_safe_query(conn, dangerous_input):
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
```

**Predict:** What would happen if you used an f-string instead: `f"WHERE author = '{dangerous_input}'"`? (Do not actually run this against a real database.)

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `sqlite3.OperationalError: no such table` | Forgot to call `create_table()` first | Create tables before inserting or querying |
| `(year)` instead of `(year,)` | Forgetting the tuple comma | A one-element tuple needs a trailing comma: `(year,)` |
| Data disappears after restart | Forgot `conn.commit()` | Always commit after INSERT, UPDATE, or DELETE |
| Using f-strings in SQL | It seems simpler | Never do this — use `?` placeholders to prevent SQL injection |

## Testing Your Solution

There are no pytest tests for this project — run it and verify the output:

```bash
python project.py
```

Expected output:
```text
--- Creating database and table ---
Table 'books' created.

--- Inserting sample books ---
Inserted 6 books.

--- All books ---
   1 | The Pragmatic Programmer    | David Thomas       | 1999
   2 | Clean Code                  | Robert C. Martin   | 2008
...

--- Dangerous input safely handled ---
Searching for: '; DROP TABLE books; --
No books found (and the table still exists!).
```

The important verification: the table still exists after the injection attempt.

## What You Learned

- **`sqlite3`** is built into Python and requires no server — it stores the entire database in a single file.
- **`conn.execute()`** runs SQL statements, and **`conn.commit()`** saves changes — without commit, INSERT/UPDATE/DELETE changes are lost when the connection closes.
- **Parameterized queries** (`?` placeholders) prevent SQL injection by treating user input as data, never as executable SQL code.
- **`cursor.fetchall()`** returns all matching rows, and **`row_factory = sqlite3.Row`** lets you access columns by name instead of index.
