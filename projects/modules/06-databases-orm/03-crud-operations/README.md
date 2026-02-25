# Module 06 / Project 03 — CRUD Operations

Home: [README](../../../../README.md) · Module: [Databases & ORM](../README.md)

## Focus

- Full Create / Read / Update / Delete with SQLAlchemy
- Interactive menu-driven CLI using `input()`
- Session management and commit patterns
- Filtering, searching, and updating rows through the ORM

## Why this project exists

CRUD is the backbone of almost every application. This project puts all four operations together in a working tool you can actually use. The interactive CLI forces you to think about user input, error handling, and database state across multiple operations.

## Run

```bash
cd projects/modules/06-databases-orm/03-crud-operations
python project.py
```

The program starts an interactive menu. It creates a fresh `library.db` with sample data on first run.

## Expected output

```text
Library Management System
=========================

  [1] List all books
  [2] Search books
  [3] Add a book
  [4] Update book status
  [5] Delete a book
  [6] Quit

Choice: 1

All books:
  ID | Title                        | Author             | Status
  ---+------------------------------+--------------------+-----------
   1 | The Pragmatic Programmer     | David Thomas       | available
   2 | Clean Code                   | Robert C. Martin   | available
   3 | Fluent Python                | Luciano Ramalho    | available
   4 | Python Crash Course          | Eric Matthes       | checked out
   5 | Design Patterns              | Gang of Four       | available

Choice: 4
Book ID to update: 1
New status (available / checked out): checked out
Updated 'The Pragmatic Programmer' to 'checked out'.

Choice: 6
Goodbye!
```

## Alter it

1. Add a "return date" column that gets set when a book is checked out. Show it in the listing.
2. Add a menu option to list only checked-out books.
3. Add a confirmation prompt before deleting a book ("Are you sure? y/n").

## Break it

1. Try to update a book ID that does not exist. Does the program crash or handle it?
2. Enter a non-numeric value when asked for a book ID. What happens?
3. Delete a book, then try to update the same ID. What error do you see?

## Fix it

1. Add input validation for book IDs (must be a positive integer, must exist).
2. Wrap database operations in try/except to handle `IntegrityError` and other exceptions.
3. Add `session.rollback()` in the except block so a failed operation does not poison the session.

## Explain it

1. Why do you need `session.commit()` after every change but not after reads?
2. What does `session.get(Book, id)` do differently from `session.query(Book).filter_by(id=id).first()`?
3. What happens to in-memory objects after `session.rollback()`?
4. Why is it important to close or scope sessions properly?

## Mastery check

You can move on when you can:
- perform all four CRUD operations through SQLAlchemy,
- handle missing records and invalid input gracefully,
- explain when to commit and when to rollback,
- build an interactive program that maintains database state.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

[Project 04 — Migrations with Alembic](../04-migrations-alembic/)
