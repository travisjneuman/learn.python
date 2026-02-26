# Module 06 / Project 02 — SQLAlchemy Models

Home: [README](../../../../README.md) · Module: [Databases & ORM](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- SQLAlchemy's declarative model system
- `DeclarativeBase`, `Mapped`, `mapped_column`
- `create_engine()` and `Session`
- Defining a one-to-many relationship (`relationship`, `ForeignKey`)
- Querying with the ORM vs raw SQL

## Why this project exists

Writing raw SQL works, but it gets tedious and error-prone as your application grows. An ORM lets you define your database schema as Python classes and interact with rows as objects. SQLAlchemy is the most widely used Python ORM and the one you will encounter in FastAPI, Flask, and Django-adjacent projects.

## Run

```bash
cd projects/modules/06-databases-orm/02-sqlalchemy-models
python project.py
```

## Expected output

```text
--- Creating tables ---
Tables created: authors, books

--- Inserting authors and books ---
Added 3 authors with 7 books total.

--- All authors ---
  Author: David Thomas
    - The Pragmatic Programmer (1999)
    - Programming Pearls (2000)
  Author: Robert C. Martin
    - Clean Code (2008)
    - Clean Architecture (2017)
    - The Clean Coder (2011)
  Author: Luciano Ramalho
    - Fluent Python (2015)
    - Fluent Python 2nd Ed (2022)

--- Query: books after 2010 ---
  Clean Architecture (2017) by Robert C. Martin
  The Clean Coder (2011) by Robert C. Martin
  Fluent Python (2015) by Luciano Ramalho
  Fluent Python 2nd Ed (2022) by Luciano Ramalho

--- Query: authors with more than 2 books ---
  Robert C. Martin (3 books)

--- ORM vs raw SQL comparison ---
ORM query returned the same results as raw SQL.
```

## Alter it

1. Add a `Publisher` model with a one-to-many relationship to books. Query all books by a publisher.
2. Add a many-to-many relationship between books and tags (e.g., "programming", "python", "design").
3. Add a `__repr__` method to both models that shows useful debug info.

## Break it

1. Try to create a book with a `author_id` that does not exist. What error do you get?
2. Remove the `back_populates` argument from the relationship. Can you still navigate from author to books?
3. Call `session.add()` without `session.commit()`. Query the data — is it in the database?

## Fix it

1. Add a foreign key constraint check (`PRAGMA foreign_keys = ON` for SQLite) and handle the IntegrityError.
2. Add `cascade="all, delete-orphan"` to the relationship so deleting an author removes their books.
3. Use `session.flush()` to see the auto-generated ID before committing.

## Explain it

1. What is the difference between `session.add()`, `session.flush()`, and `session.commit()`?
2. What does `back_populates` do and why do you need it on both sides?
3. How does SQLAlchemy translate `session.query(Book).filter(Book.year > 2010)` into SQL?
4. What is a foreign key and why does it matter for data integrity?

## Mastery check

You can move on when you can:
- define SQLAlchemy models with columns and relationships,
- create an engine and session to interact with the database,
- insert and query data through the ORM,
- explain the difference between ORM queries and raw SQL.

---

## Related Concepts

- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [Quiz: Classes and Objects](../../../../concepts/quizzes/classes-and-objects-quiz.py)

## Next

[Project 03 — CRUD Operations](../03-crud-operations/)
