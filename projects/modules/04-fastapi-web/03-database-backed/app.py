# ============================================================================
# Project 03 — Database-Backed API
# ============================================================================
# The same todo API from Project 02, but backed by a real SQLite database.
# Data persists across server restarts. This project introduces:
#
# 1. SQLAlchemy ORM for database operations
# 2. Depends() for dependency injection (database sessions)
# 3. Separate files for models, schemas, and database setup
#
# Run: python app.py
# Docs: http://127.0.0.1:8000/docs
# ============================================================================

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

# Import our database setup, models, and schemas from separate files.
# Splitting code into files keeps each file focused on one responsibility.
from database import SessionLocal, engine, Base
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoResponse

# ----------------------------------------------------------------------------
# Create database tables on startup.
# Base.metadata.create_all() reads every model that inherits from Base and
# creates the corresponding table if it does not already exist. This is
# fine for development. In production, you would use Alembic migrations.
# ----------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ============================================================================
# Dependency: get_db
# ============================================================================
# This function provides a database session to each endpoint that needs one.
# FastAPI's Depends() system calls this function before the endpoint runs
# and passes the result as a parameter.
#
# The yield/finally pattern ensures the session is always closed, even if
# the endpoint raises an exception. This prevents database connection leaks.
#
# Think of it like a context manager:
#   with get_db() as db:
#       ... use db ...
#   # db is automatically closed here
# ============================================================================
def get_db():
    """Provide a database session for the duration of a request."""
    db = SessionLocal()
    try:
        yield db  # The endpoint receives this session
    finally:
        db.close()  # Always close, even if an error occurred


# ============================================================================
# Endpoints
# ============================================================================
# Each endpoint receives `db: Session = Depends(get_db)` as a parameter.
# FastAPI sees Depends(get_db), calls get_db(), and passes the resulting
# session as the `db` argument. The endpoint uses this session to query
# and modify the database.
# ============================================================================


@app.get("/todos", response_model=list[TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    """Return all todos from the database.

    db.query(Todo).all() is the SQLAlchemy equivalent of:
        SELECT * FROM todos;
    """
    return db.query(Todo).all()


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Return a single todo by ID.

    db.query(Todo).filter(Todo.id == todo_id).first() is equivalent to:
        SELECT * FROM todos WHERE id = ? LIMIT 1;

    .first() returns None if no row matches, so we check for that and
    raise a 404 if the todo does not exist.
    """
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo in the database.

    Steps:
    1. Create a SQLAlchemy Todo object from the Pydantic input.
    2. Add it to the session (stages it for insertion).
    3. Commit the session (writes to the database).
    4. Refresh the object (reads back server-generated values like id).
    """
    # Create a new Todo ORM object. We unpack the Pydantic model's fields
    # using model_dump(), which converts it to a dictionary.
    db_todo = Todo(**todo.model_dump())

    # Add to session, commit to database, refresh to get generated values.
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo in the database."""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update each field from the request body.
    db_todo.title = todo.title
    db_todo.completed = todo.completed

    # Commit saves the changes to the database.
    db.commit()
    db.refresh(db_todo)

    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo from the database."""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()


# ============================================================================
# Run the server
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
