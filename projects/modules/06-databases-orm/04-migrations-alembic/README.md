# Module 06 / Project 04 — Migrations with Alembic

Home: [README](../../../../README.md) · Module: [Databases & ORM](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- What schema migrations are and why you need them
- Setting up Alembic in a project
- Autogenerating migrations from model changes
- Running `upgrade` and `downgrade`
- The migration history chain

## Why this project exists

When your application is live and has real data, you cannot just drop and recreate tables. You need a way to evolve your schema safely — adding columns, changing types, creating indexes — without losing data. Alembic is SQLAlchemy's migration tool. It tracks every schema change as a versioned script that can be applied forward or rolled back.

## Setup

This project is more guide-driven than the others. You will run Alembic commands in your terminal alongside the Python code.

```bash
cd projects/modules/06-databases-orm/04-migrations-alembic
pip install -r ../requirements.txt
```

## Step-by-step guide

### Step 1: Understand the starting models

Look at `project.py`. It defines `Author` and `Book` models — the same ones from Project 02, but without a `genre` column on Book. We will add that column via a migration.

### Step 2: Create the initial database

```bash
python project.py
```

This creates `library.db` with the initial schema (no genre column).

### Step 3: Examine the Alembic setup

The project already has Alembic configured:
- `alembic.ini` — points to the SQLite database
- `alembic/env.py` — imports the models so Alembic can compare them to the database

### Step 4: Create the first migration

Now add the `genre` column to the `Book` model in `project.py`. Uncomment the line marked `# UNCOMMENT FOR MIGRATION`. Then run:

```bash
alembic revision --autogenerate -m "add genre column to books"
```

Alembic compares your models to the database and generates a migration script in `alembic/versions/`.

### Step 5: Apply the migration

```bash
alembic upgrade head
```

This runs the migration, adding the genre column to the existing database without losing any data.

### Step 6: Verify

```bash
python -c "import sqlite3; conn = sqlite3.connect('library.db'); print([col[1] for col in conn.execute('PRAGMA table_info(books)').fetchall()])"
```

You should see `genre` in the column list.

### Step 7: Rollback

```bash
alembic downgrade -1
```

This undoes the last migration, removing the genre column.

## Expected output

```text
$ python project.py
Tables created. Sample data inserted.
Books in database:
  1 | The Pragmatic Programmer     | David Thomas
  2 | Clean Code                   | Robert C. Martin
  3 | Fluent Python                | Luciano Ramalho

$ alembic revision --autogenerate -m "add genre column to books"
Generating .../alembic/versions/xxxx_add_genre_column_to_books.py ... done

$ alembic upgrade head
Running upgrade  -> xxxx, add genre column to books

$ alembic downgrade -1
Running downgrade xxxx -> , add genre column to books
```

## Alter it

1. Add another migration that creates an `isbn` column (String, nullable). Apply it.
2. Create a data migration that sets `genre = "programming"` for all existing books.
3. Add an index on the `genre` column via a migration.

## Break it

1. Manually edit the database schema (add a column by hand) without creating a migration. Now try `--autogenerate`. What happens?
2. Delete a migration file from `alembic/versions/` and try to upgrade. What error do you get?
3. Change a column type in the model without creating a migration. Does the app crash?

## Fix it

1. Use `alembic stamp head` to tell Alembic "the database matches the current models" after a manual fix.
2. Create a manual migration with `alembic revision -m "fix"` and write the upgrade/downgrade yourself.
3. Use `alembic history` to see the full chain of migrations and find where things went wrong.

## Explain it

1. What problem do migrations solve that `create_all()` does not?
2. What is the difference between `--autogenerate` and writing a migration by hand?
3. What does `alembic stamp` do and when would you use it?
4. Why should migration scripts be committed to version control?

## Mastery check

You can move on when you can:
- set up Alembic in a project with existing models,
- generate and apply a migration that adds a column,
- rollback a migration with `downgrade`,
- explain why `create_all()` is not enough for production.

---

## Related Concepts

- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [Quiz: Classes and Objects](../../../../concepts/quizzes/classes-and-objects-quiz.py)

## Next

[Project 05 — Query Optimization](../05-query-optimization/)
