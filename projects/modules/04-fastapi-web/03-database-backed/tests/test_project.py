"""Tests for Module 04 / Project 03 — Database-Backed API.

Tests the CRUD API with a real SQLite database (in-memory). We override
the get_db dependency to use a test database instead of the production one.

WHY use an in-memory database for tests?
- It is created fresh for each test run (no leftover data).
- It is faster than disk-based SQLite.
- It does not create any database files that need cleanup.
"""

import sys
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import Base
from app import app, get_db

# Create an in-memory SQLite database for testing.
# check_same_thread=False is needed because FastAPI uses multiple threads.
TEST_ENGINE = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


def override_get_db():
    """Provide a test database session instead of the production one.

    This function replaces get_db in the FastAPI app during tests.
    The yield/finally pattern ensures the session is always closed.
    """
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency for all tests.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test and drop them after.

    This gives each test a clean database with no leftover data.
    """
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


# ---------------------------------------------------------------------------
# Tests for POST /todos (Create)
# ---------------------------------------------------------------------------

def test_create_todo():
    """Creating a todo should return 201 with the created data.

    The response includes server-generated fields: id and created_at.
    """
    response = client.post("/todos", json={"title": "Test Todo"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_todo_persists():
    """A created todo should appear in subsequent GET requests.

    This verifies the database write actually persists (commit worked).
    """
    client.post("/todos", json={"title": "Persistent"})

    response = client.get("/todos")
    todos = response.json()

    assert len(todos) == 1
    assert todos[0]["title"] == "Persistent"


# ---------------------------------------------------------------------------
# Tests for GET /todos (Read all)
# ---------------------------------------------------------------------------

def test_list_todos_empty():
    """GET /todos should return an empty list when the database is empty."""
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# Tests for GET /todos/{todo_id} (Read one)
# ---------------------------------------------------------------------------

def test_get_todo_by_id():
    """GET /todos/{id} should return the matching todo."""
    create_resp = client.post("/todos", json={"title": "Find Me"})
    todo_id = create_resp.json()["id"]

    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_todo_not_found():
    """GET /todos/999 should return 404 when no todo has that ID."""
    response = client.get("/todos/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests for PUT /todos/{todo_id} (Update)
# ---------------------------------------------------------------------------

def test_update_todo():
    """PUT /todos/{id} should update the title and completed fields."""
    create_resp = client.post("/todos", json={"title": "Original"})
    todo_id = create_resp.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated", "completed": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


def test_update_todo_not_found():
    """PUT /todos/999 should return 404 when the todo does not exist."""
    response = client.put("/todos/999", json={"title": "X", "completed": False})
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests for DELETE /todos/{todo_id}
# ---------------------------------------------------------------------------

def test_delete_todo():
    """DELETE /todos/{id} should remove the todo and return 204."""
    create_resp = client.post("/todos", json={"title": "Delete Me"})
    todo_id = create_resp.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    # Verify it is gone.
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


def test_delete_todo_not_found():
    """DELETE /todos/999 should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
