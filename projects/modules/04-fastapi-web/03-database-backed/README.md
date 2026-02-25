# Module 04 / Project 03 — Database-Backed API

Home: [README](../../../../README.md)

## Focus

SQLite + SQLAlchemy ORM, database models, FastAPI dependency injection with `Depends()`.

## Why this project exists

The todo API from Project 02 loses all data when the server restarts because it uses an in-memory list. This project replaces that list with a real SQLite database using SQLAlchemy ORM. You will learn how to define database models, create tables, manage database sessions with FastAPI's dependency injection system, and persist data across server restarts.

## Run

```bash
cd projects/modules/04-fastapi-web/03-database-backed
python app.py
```

Then open **http://127.0.0.1:8000/docs** to test the endpoints. Create some todos, stop the server with `Ctrl+C`, start it again, and confirm your todos are still there.

A `todos.db` file will appear in the project directory. This is your SQLite database.

## Expected output

The API behaves identically to Project 02, but data persists:

```bash
# Create a todo
curl -X POST http://127.0.0.1:8000/todos -H "Content-Type: application/json" -d '{"title": "Survive a restart"}'
# Returns: {"id": 1, "title": "Survive a restart", "completed": false, "created_at": "2024-01-15T10:30:00"}

# Stop the server (Ctrl+C), then restart it (python app.py)

# Data is still there
curl http://127.0.0.1:8000/todos
# Returns: [{"id": 1, "title": "Survive a restart", "completed": false, "created_at": "2024-01-15T10:30:00"}]
```

## Alter it

1. Add a `priority` column (integer, default 0) to the Todo model. Update the schemas to include it in create and response models.
2. Add a `GET /todos?completed=true` query parameter to filter todos by completion status.
3. Add a `GET /todos/count` endpoint that returns `{"total": N, "completed": M, "pending": P}`.

## Break it

1. Delete the `todos.db` file while the server is running, then try to create a todo. What happens?
2. Add a new column to the SQLAlchemy model but do not delete the old database. Start the server and try to use the new column. What error do you get?
3. Remove the `yield` from the `get_db` dependency and return the session directly. Create a few todos, then check if the database is growing correctly.

## Fix it

1. Restart the server. SQLAlchemy recreates the database file and tables on startup because of `Base.metadata.create_all()`.
2. Delete `todos.db` and restart the server. In production, you would use a migration tool like Alembic instead of deleting the database.
3. Restore the `yield` and add the `finally` block that closes the session. Without proper cleanup, database connections leak and the application eventually crashes.

## Explain it

1. What is an ORM? How does the SQLAlchemy `Todo` class relate to a database table?
2. What does `Depends(get_db)` do? Why is it better than creating a database session inside each endpoint function?
3. What is the difference between the SQLAlchemy model (`models.py`) and the Pydantic schema (`schemas.py`)? Why do you need both?
4. What does `yield` do in the `get_db` function? What happens in the `finally` block and why is it important?

## Mastery check

You can move on when you can:

- explain the difference between a SQLAlchemy model and a Pydantic schema,
- describe what `Depends()` does and why FastAPI uses it,
- add a new column to the model and update all layers (model, schema, endpoint),
- delete the database and recover by restarting the server.

## Next

Continue to [04-authentication](../04-authentication/).
