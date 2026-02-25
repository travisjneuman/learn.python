# Module 06 / Project 01 — SQLite Basics

Home: [README](../../../../README.md) · Module: [Databases & ORM](../README.md)

## Focus

- Python's built-in `sqlite3` module (no install needed)
- Creating tables with `CREATE TABLE`
- Inserting rows with `INSERT INTO`
- Querying data with `SELECT` and `WHERE`
- Parameterized queries to prevent SQL injection

## Why this project exists

Before you learn an ORM like SQLAlchemy, you should understand what it does under the hood. SQLite ships with Python and requires no server setup. This project teaches you raw SQL through Python so that when you see ORM code later, you understand what it translates to.

## Run

```bash
cd projects/modules/06-databases-orm/01-sqlite-basics
python project.py
```

This creates a `data/books.db` file. Delete it and re-run to start fresh.

## Expected output

```text
--- Creating database and table ---
Table 'books' created.

--- Inserting sample books ---
Inserted 6 books.

--- All books ---
  1 | The Pragmatic Programmer    | David Thomas       | 1999
  2 | Clean Code                  | Robert C. Martin   | 2008
  3 | Fluent Python               | Luciano Ramalho    | 2015
  4 | Python Crash Course         | Eric Matthes       | 2015
  5 | Design Patterns             | Gang of Four       | 1994
  6 | Refactoring                 | Martin Fowler      | 1999

--- Books by year 2015 ---
  3 | Fluent Python               | Luciano Ramalho    | 2015
  4 | Python Crash Course         | Eric Matthes       | 2015

--- Books with 'Python' in the title ---
  3 | Fluent Python               | Luciano Ramalho    | 2015
  4 | Python Crash Course         | Eric Matthes       | 2015

--- Parameterized query demo ---
Searching for author: Robert C. Martin
  2 | Clean Code                  | Robert C. Martin   | 2008

--- Dangerous input safely handled ---
Searching for: '; DROP TABLE books; --
No books found (and the table still exists!).
```

## Alter it

1. Add a `genre` column to the books table. Insert books with genres and query by genre.
2. Add an `UPDATE` statement that changes a book's year. Verify it worked with a `SELECT`.
3. Add a `DELETE` statement that removes a book by ID. Print the table before and after.

## Break it

1. Use string formatting (`f"... WHERE author = '{author}'"`) instead of parameterized queries. Pass in `'; DROP TABLE books; --` and see what happens.
2. Try to insert a row with the wrong number of values. Read the error message.
3. Remove the `conn.commit()` call after inserts. Query the data — is it there? Restart and check again.

## Fix it

1. Replace the string-formatted query with a parameterized one (`?` placeholders).
2. Add `try/except` around database operations to handle `sqlite3.Error` gracefully.
3. Use a context manager (`with conn:`) to ensure commits happen automatically.

## Explain it

1. What is SQL injection and why are parameterized queries the fix?
2. What does `conn.commit()` do? What happens to your data without it?
3. What is the difference between `conn.execute()` and `cursor.execute()`?
4. Why does SQLite not need a separate server process?

## Mastery check

You can move on when you can:
- create a table and insert rows using `sqlite3`,
- write `SELECT` queries with `WHERE` clauses,
- explain why parameterized queries matter,
- use `conn.commit()` and understand transactions.

## Next

[Project 02 — SQLAlchemy Models](../02-sqlalchemy-models/)
