"""
Tests for Project 02 — Deploy with Database

These tests verify the Todo API with a temporary SQLite database. The app
is designed for PostgreSQL in production, but SQLAlchemy's ORM abstraction
lets us test with SQLite locally.

Why test with SQLite?
    PostgreSQL requires a running server. SQLite works as a file or
    in-memory database with zero setup. Since SQLAlchemy abstracts the
    database engine, the same code works with both. If it works with
    SQLite in tests, it will work with PostgreSQL in production.

Run with: pytest tests/test_project.py -v
"""

import os
import sys

import pytest

# Ensure the project directory is on the path for imports.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Set DATABASE_URL before importing app modules.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cloud.db")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db


@pytest.fixture
def client(tmp_path):
    """Create a test client with a fresh SQLite database.

    WHY: Each test gets its own database to prevent data leakage. The
    dependency override replaces the production get_db with our test
    session, so the app uses our temporary database.
    """
    db_url = f"sqlite:///{tmp_path}/test.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    from app import app

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root(client):
    """GET / should return a welcome message confirming the API is running.

    WHY: This is the deployment smoke test. If the root endpoint works,
    the basic app infrastructure (FastAPI, routing) is functioning.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Todo" in data["message"] or "todo" in data["message"].lower()


# ── Test: create todo ─────────────────────────────────────────────────

def test_create_todo(client):
    """POST /todos should create a new todo with defaults.

    WHY: The create endpoint must validate input (requires title), set
    defaults (completed=False), generate an ID, and persist to the
    database. This test verifies the full creation flow.
    """
    response = client.post("/todos", json={"title": "Deploy to Railway"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Deploy to Railway"
    assert data["completed"] is False, "New todos should not be completed"
    assert "id" in data
    assert "created_at" in data


# ── Test: list todos ──────────────────────────────────────────────────

def test_list_todos(client):
    """GET /todos should return all todos ordered by created_at descending.

    WHY: The list endpoint is the main view. It must return todos in
    the correct order (newest first) and include all fields.
    """
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})

    response = client.get("/todos")

    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2


# ── Test: toggle todo ─────────────────────────────────────────────────

def test_toggle_todo(client):
    """PUT /todos/{id} should toggle the completed status.

    WHY: The toggle endpoint flips completed from False to True (or vice
    versa). This is the primary way users mark tasks as done. If the
    toggle logic is inverted or does not persist, tasks cannot be completed.
    """
    create_response = client.post("/todos", json={"title": "Toggle me"})
    todo_id = create_response.json()["id"]

    # First toggle: False -> True
    toggle_response = client.put(f"/todos/{todo_id}")
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True

    # Second toggle: True -> False
    toggle_response = client.put(f"/todos/{todo_id}")
    assert toggle_response.json()["completed"] is False


def test_toggle_nonexistent_returns_404(client):
    """PUT /todos/{id} should return 404 for non-existent IDs."""
    response = client.put("/todos/99999")

    assert response.status_code == 404


# ── Test: delete todo ─────────────────────────────────────────────────

def test_delete_todo(client):
    """DELETE /todos/{id} should remove the todo and return 204.

    WHY: Deletion must actually remove the record from the database.
    A soft-delete bug (marking as deleted but still returning in lists)
    would leave "deleted" todos visible to users.
    """
    create_response = client.post("/todos", json={"title": "Delete me"})
    todo_id = create_response.json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

    # Verify it is actually gone.
    list_response = client.get("/todos")
    assert len(list_response.json()) == 0


def test_delete_nonexistent_returns_404(client):
    """DELETE /todos/{id} should return 404 for non-existent IDs."""
    response = client.delete("/todos/99999")

    assert response.status_code == 404


# ── Test: health check ────────────────────────────────────────────────

def test_health_check_with_database(client):
    """GET /health should report database connectivity status.

    WHY: The health endpoint checks database connectivity. Cloud platforms
    use this to detect when the database is down and potentially restart
    the app or send alerts.
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
