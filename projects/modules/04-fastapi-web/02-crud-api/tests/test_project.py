"""Tests for Module 04 / Project 02 — CRUD API.

Tests all four CRUD operations (Create, Read, Update, Delete) on the
in-memory todo list. Each test clears the state before running to
ensure tests are independent.

WHY clear state between tests?
- The app uses a module-level list (todos) as its "database."
- If one test creates a todo, it stays in memory for the next test.
- Clearing state prevents test order dependencies and flaky failures.
"""

import sys
import os

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module
from app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Clear the in-memory todo list and reset the ID counter before each test.

    autouse=True means this runs automatically before EVERY test in this file.
    """
    app_module.todos.clear()
    app_module.next_id = 1
    yield
    # Cleanup after test (in case of failures).
    app_module.todos.clear()
    app_module.next_id = 1


# ---------------------------------------------------------------------------
# Tests for POST /todos (Create)
# ---------------------------------------------------------------------------

def test_create_todo_returns_201():
    """Creating a todo should return HTTP 201 Created.

    201 is the standard status code for successful resource creation.
    """
    response = client.post("/todos", json={"title": "Buy groceries"})
    assert response.status_code == 201


def test_create_todo_returns_created_data():
    """The response should include the todo with its server-assigned ID.

    The client only sends {title}. The server adds {id, completed}.
    """
    response = client.post("/todos", json={"title": "Buy groceries"})
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["completed"] is False


def test_create_todo_increments_id():
    """Each new todo should get the next sequential ID."""
    client.post("/todos", json={"title": "First"})
    response = client.post("/todos", json={"title": "Second"})

    assert response.json()["id"] == 2


def test_create_todo_missing_title():
    """Creating a todo without a title should return 422.

    Pydantic validates the request body against the TodoCreate schema.
    """
    response = client.post("/todos", json={})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Tests for GET /todos (Read all)
# ---------------------------------------------------------------------------

def test_list_todos_empty():
    """GET /todos should return an empty list when no todos exist."""
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_after_create():
    """GET /todos should return all created todos."""
    client.post("/todos", json={"title": "Todo 1"})
    client.post("/todos", json={"title": "Todo 2"})

    response = client.get("/todos")

    assert response.status_code == 200
    assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# Tests for GET /todos/{todo_id} (Read one)
# ---------------------------------------------------------------------------

def test_get_todo_by_id():
    """GET /todos/1 should return the todo with ID 1."""
    client.post("/todos", json={"title": "My Todo"})

    response = client.get("/todos/1")

    assert response.status_code == 200
    assert response.json()["title"] == "My Todo"


def test_get_todo_not_found():
    """GET /todos/999 should return 404 when the todo does not exist."""
    response = client.get("/todos/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Tests for PUT /todos/{todo_id} (Update)
# ---------------------------------------------------------------------------

def test_update_todo():
    """PUT /todos/1 should update both title and completed status."""
    client.post("/todos", json={"title": "Original"})

    response = client.put("/todos/1", json={"title": "Updated", "completed": True})

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
    """DELETE /todos/1 should remove the todo and return 204 No Content.

    After deletion, GET /todos/1 should return 404.
    """
    client.post("/todos", json={"title": "Delete me"})

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # Verify it is gone.
    response = client.get("/todos/1")
    assert response.status_code == 404


def test_delete_todo_not_found():
    """DELETE /todos/999 should return 404 when the todo does not exist."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
