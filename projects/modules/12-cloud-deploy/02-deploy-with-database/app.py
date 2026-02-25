"""
Deploy with Database — FastAPI app backed by PostgreSQL (or SQLite locally).

This app reads DATABASE_URL from the environment. In production (Railway),
this points to PostgreSQL. In local development, it falls back to SQLite.

Key concepts:
- DATABASE_URL: standard connection string format
- create_all on startup: creates tables if they don't exist
- Depends(get_db): gives each request its own database session
"""

import os
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Todo

# ── Create tables on startup ─────────────────────────────────────────
# In production, you'd use Alembic migrations instead of create_all().
# But for learning, this is simpler — it creates tables that don't exist.
Base.metadata.create_all(bind=engine)

# ── App setup ────────────────────────────────────────────────────────

APP_ENV = os.environ.get("APP_ENV", "development")

app = FastAPI(
    title="Todo API (Cloud)",
    description="A todo API deployed to the cloud with a real database",
    version="1.0.0",
)


# ── Pydantic schemas ─────────────────────────────────────────────────

class TodoCreate(BaseModel):
    title: str

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Endpoints ────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "message": "Todo API is running",
        "environment": APP_ENV,
        "docs": "/docs",
    }


@app.get("/health")
async def health(db: Session = Depends(get_db)):
    """Health check that also verifies database connectivity."""
    try:
        # Simple query to check the database is reachable.
        db.execute(Todo.__table__.select().limit(1))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "environment": APP_ENV,
    }


@app.get("/todos", response_model=list[TodoResponse])
async def list_todos(db: Session = Depends(get_db)):
    """List all todos."""
    return db.query(Todo).order_by(Todo.created_at.desc()).all()


@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo."""
    db_todo = Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    """Toggle a todo's completed status."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Todo API ({APP_ENV}) on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
