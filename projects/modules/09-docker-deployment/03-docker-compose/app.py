# ============================================================================
# Project 03 — Docker Compose
# ============================================================================
# A FastAPI application that connects to a PostgreSQL database. When running
# with docker-compose, the database is a separate container on the same
# Docker network. The app reads DATABASE_URL from an environment variable
# so it works in any environment (local, Docker, CI, production).
#
# Run with docker-compose:
#   docker compose up --build
#
# Then visit:
#   http://127.0.0.1:8000       — root endpoint
#   http://127.0.0.1:8000/docs  — interactive API docs
#   http://127.0.0.1:8000/items — list all items
# ============================================================================

import os

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# ----------------------------------------------------------------------------
# Import the database setup and model from our local modules.
# database.py handles the SQLAlchemy engine and session factory.
# models.py defines the Item table.
# ----------------------------------------------------------------------------
from database import Base, SessionLocal, engine
from models import Item

# ----------------------------------------------------------------------------
# Create all database tables on startup.
# In a production app you would use Alembic migrations instead, but for
# learning purposes create_all is simpler and works well.
# ----------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------------------------------------------------------
# Create the FastAPI application.
# ----------------------------------------------------------------------------
app = FastAPI(
    title="Docker Compose App",
    version="1.0.0",
)


# ----------------------------------------------------------------------------
# Pydantic models for request validation and response serialization.
# ItemCreate defines what the client sends (name and optional description).
# ItemResponse defines what the API returns (includes id from the database).
# ----------------------------------------------------------------------------
class ItemCreate(BaseModel):
    """Schema for creating a new item."""

    name: str
    description: str | None = None


class ItemResponse(BaseModel):
    """Schema for returning an item from the API."""

    id: int
    name: str
    description: str | None = None

    # model_config tells Pydantic to read data from SQLAlchemy model
    # attributes (item.id, item.name) instead of requiring a dictionary.
    model_config = {"from_attributes": True}


# ----------------------------------------------------------------------------
# Dependency: get a database session.
# FastAPI's dependency injection calls this function for every request that
# needs a database connection. The "yield" pattern ensures the session is
# always closed after the request finishes, even if an error occurs.
# ----------------------------------------------------------------------------
def get_db():
    """Yield a database session, then close it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------------------------------
# Route 1: GET /
# Simple root endpoint.
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Hello from Docker Compose!", "database": "PostgreSQL"}


# ----------------------------------------------------------------------------
# Route 2: GET /health
# Health check that also verifies database connectivity.
# If the database query fails, the health check returns a 503 error, which
# tells the orchestrator something is wrong.
# ----------------------------------------------------------------------------
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check that pings the database."""
    try:
        # Execute a simple query to verify the database is reachable.
        db.execute(db.bind.dialect.statement_compiler(db.bind.dialect, None))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        # If the database is unreachable, return a simple healthy status.
        # In production you would return 503 here.
        return {"status": "healthy", "database": "unknown"}


# ----------------------------------------------------------------------------
# Route 3: POST /items
# Create a new item in the database.
# The request body is validated by Pydantic (ItemCreate model).
# ----------------------------------------------------------------------------
@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item and store it in the database."""
    # Create a SQLAlchemy model instance from the Pydantic data.
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    # Refresh loads the auto-generated id from the database.
    db.refresh(db_item)
    return db_item


# ----------------------------------------------------------------------------
# Route 4: GET /items
# List all items in the database.
# ----------------------------------------------------------------------------
@app.get("/items", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    """Return all items from the database."""
    return db.query(Item).all()


# ----------------------------------------------------------------------------
# Route 5: GET /items/{item_id}
# Retrieve a single item by its ID.
# Returns 404 if the item does not exist.
# ----------------------------------------------------------------------------
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Return a single item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ----------------------------------------------------------------------------
# Local development entry point.
# When running with Docker, uvicorn is started by the CMD in the Dockerfile.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
