# Module 06 — Databases & ORM

Home: [README](../../../README.md) · Modules: [Index](../README.md)

## Prerequisites

- Level 3 complete (you understand packages, error handling, project structure)
- Comfortable with classes, context managers, and file I/O

## What you will learn

- How relational databases store and relate data
- Writing SQL with Python's built-in `sqlite3` module
- Defining models and relationships with SQLAlchemy ORM
- Full CRUD operations through an ORM session
- Managing schema changes with Alembic migrations
- Spotting and fixing common query performance problems

## Why databases matter

Every real application stores data somewhere. Flat files (CSV, JSON) work for small things, but they fall apart when you need to search, relate, or update data reliably. Relational databases solve this with tables, indexes, and transactions. An ORM (Object-Relational Mapper) lets you work with database rows as Python objects instead of writing raw SQL for everything.

## Install dependencies

```bash
cd projects/modules/06-databases-orm
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Project 01 uses only the built-in `sqlite3` module, so it works without installing anything. Projects 02-05 require SQLAlchemy and Alembic.

## Projects

| # | Project | Focus |
|---|---------|-------|
| 01 | [SQLite Basics](./01-sqlite-basics/) | sqlite3 module, CREATE TABLE, INSERT, SELECT, parameterized queries |
| 02 | [SQLAlchemy Models](./02-sqlalchemy-models/) | Declarative models, engine, Session, Base, relationships |
| 03 | [CRUD Operations](./03-crud-operations/) | Create/Read/Update/Delete with SQLAlchemy, interactive CLI |
| 04 | [Migrations with Alembic](./04-migrations-alembic/) | Schema migrations — init, autogenerate, upgrade, downgrade |
| 05 | [Query Optimization](./05-query-optimization/) | Indexes, eager/lazy loading, N+1 problem, EXPLAIN |

## Related concepts

- [concepts/classes-explained.md](../../../concepts/classes-explained.md)
- [concepts/context-managers-explained.md](../../../concepts/context-managers-explained.md)
