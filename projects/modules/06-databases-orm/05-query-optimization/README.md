# Module 06 / Project 05 — Query Optimization

Home: [README](../../../../README.md) · Module: [Databases & ORM](../README.md)

## Focus

- The N+1 query problem and why it kills performance
- Eager loading with `joinedload()` to fix N+1
- Database indexes and when to add them
- Using `EXPLAIN` to understand query plans
- Measuring query performance with timing

## Why this project exists

ORMs make database access easy, but they also make it easy to write slow code without realizing it. The N+1 problem is the most common performance trap: your code looks simple but fires hundreds of queries behind the scenes. This project makes the problem visible with timing and query counts, then shows you how to fix it.

## Run

```bash
cd projects/modules/06-databases-orm/05-query-optimization
python project.py
```

This creates a database with 1000+ rows and runs several experiments. The output includes timing comparisons.

## Expected output

```text
--- Setting up database with 50 authors and 1000 books ---
Database created with 50 authors and 1000 books.

--- Demo 1: The N+1 problem ---
N+1 approach: 51 queries in ~0.08s
  (1 query for authors + 50 queries for each author's books)

Eager loading: 1 query in ~0.01s
  (1 query with JOIN loads everything at once)

Speedup: ~8x faster with eager loading.

--- Demo 2: Index performance ---
Search without index: 0.015s (full table scan)
Search with index:    0.002s (index lookup)

EXPLAIN without index:
  SCAN books

EXPLAIN with index:
  SEARCH books USING INDEX ix_books_year (year=?)

--- Demo 3: Bulk operations ---
Insert 500 books one-at-a-time: 0.45s
Insert 500 books in bulk:       0.02s
```

Exact times will vary on your machine, but the relative differences should be clear.

## Alter it

1. Increase the dataset to 10,000 books. Do the performance differences become more dramatic?
2. Add a compound index on `(author_id, year)`. Test a query that filters on both columns.
3. Try `subqueryload()` instead of `joinedload()`. Compare the generated SQL.

## Break it

1. Access `author.books` inside a loop without eager loading on a large dataset. Time it.
2. Add an index on every column. Does INSERT performance get worse?
3. Use `selectinload()` on a many-to-many relationship with a huge join table.

## Fix it

1. Replace the N+1 loop with a single query using `joinedload()`.
2. Use `bulk_save_objects()` or `add_all()` instead of individual `add()` calls.
3. Add `expire_on_commit=False` to the session to avoid unnecessary re-queries after commit.

## Explain it

1. What is the N+1 problem? Draw it out: how many queries does it generate for N authors?
2. What does a database index actually do? (Think: book index vs reading every page.)
3. What is the difference between `joinedload()`, `subqueryload()`, and `selectinload()`?
4. When should you NOT add an index?

## Mastery check

You can move on when you can:
- identify and fix the N+1 query problem,
- use `joinedload()` to eagerly load relationships,
- add an index and verify it with EXPLAIN,
- explain the tradeoffs of indexing (read speed vs write speed).

---

## Related Concepts

- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Classes and Objects](../../../../concepts/quizzes/classes-and-objects-quiz.py)

## Next

You have completed Module 06. You now understand how Python applications store, retrieve, and manage relational data. Consider Module 04 (FastAPI) to build a web API backed by a database, or Module 10 (Django) for a full-stack application.
