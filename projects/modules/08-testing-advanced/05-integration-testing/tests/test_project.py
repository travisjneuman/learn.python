"""
Tests for Project 05 — Integration Testing (test_project.py)

Additional integration tests that complement test_integration.py. These
test the Todo API's full request-response cycle using FastAPI's TestClient.

What is integration testing?
    Unlike unit tests that test a single function in isolation, integration
    tests verify that multiple components work together. Here we test the
    entire HTTP request flow: URL routing -> view function -> data storage
    -> response serialization.

Run with: pytest tests/test_project.py -v
"""

import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture
def client():
    """Create a test client with a fresh app instance.

    WHY: create_app() returns a new FastAPI app with empty storage each time.
    This ensures tests are isolated — creating a todo in one test does not
    affect another test. TestClient makes HTTP requests without starting
    a real server.
    """
    app = create_app()
    return TestClient(app)


# ── Test: list todos (empty) ──────────────────────────────────────────

def test_list_todos_empty(client):
    """GET /todos should return an empty list when no todos exist.

    WHY: The API should return 200 with an empty list, not a 404 or error.
    This is a common convention: "the collection exists, it just has no items."
    """
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == [], "Empty app should return empty list"


# ── Test: create todo ─────────────────────────────────────────────────

def test_create_todo(client):
    """POST /todos should create a new todo and return it with status 201.

    WHY: 201 means "Created" — the standard HTTP status for successful
    resource creation. The response should include the generated ID and
    the default done=False.
    """
    response = client.post("/todos", json={"title": "Learn pytest"})

    assert response.status_code == 201, "Should return 201 Created"

    data = response.json()
    assert data["title"] == "Learn pytest"
    assert data["done"] is False, "New todos should not be done"
    assert "id" in data, "Response should include the generated ID"


def test_create_todo_appears_in_list(client):
    """After creating a todo, it should appear in GET /todos.

    WHY: This is a true integration test — it verifies that POST creates
    data that GET can retrieve. If storage is broken, POST might return
    success but GET would return empty.
    """
    client.post("/todos", json={"title": "Buy groceries"})

    response = client.get("/todos")
    todos = response.json()

    assert len(todos) == 1, "Should have 1 todo after creating one"
    assert todos[0]["title"] == "Buy groceries"


# ── Test: get specific todo ───────────────────────────────────────────

def test_get_todo_by_id(client):
    """GET /todos/{id} should return the specific todo.

    WHY: Retrieving a single resource by ID is a fundamental CRUD operation.
    This test verifies the path parameter extraction and storage lookup work.
    """
    create_response = client.post("/todos", json={"title": "Read a book"})
    todo_id = create_response.json()["id"]

    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Read a book"
    assert response.json()["id"] == todo_id


def test_get_nonexistent_todo_returns_404(client):
    """GET /todos/{id} should return 404 for a non-existent ID.

    WHY: 404 is the correct HTTP response for "resource not found."
    Returning 200 with null or an empty object would confuse API consumers.
    """
    response = client.get("/todos/9999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ── Test: delete todo ─────────────────────────────────────────────────

def test_delete_todo(client):
    """DELETE /todos/{id} should remove the todo and return 204.

    WHY: 204 means "No Content" — the standard response for successful
    deletion. The todo should be gone from the list after deletion.
    """
    create_response = client.post("/todos", json={"title": "Delete me"})
    todo_id = create_response.json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204, "Should return 204 No Content"

    # Verify the todo is actually gone.
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404, "Deleted todo should return 404"


def test_delete_nonexistent_todo_returns_404(client):
    """DELETE /todos/{id} should return 404 for a non-existent ID.

    WHY: You cannot delete something that does not exist. Returning 204
    for a non-existent resource would be misleading.
    """
    response = client.delete("/todos/9999")

    assert response.status_code == 404


# ── Test: multiple todos ──────────────────────────────────────────────

def test_multiple_todos_have_unique_ids(client):
    """Each created todo should receive a unique ID.

    WHY: If the ID counter is broken, multiple todos could get the same ID,
    causing data corruption when retrieving or deleting by ID.
    """
    r1 = client.post("/todos", json={"title": "First"})
    r2 = client.post("/todos", json={"title": "Second"})
    r3 = client.post("/todos", json={"title": "Third"})

    ids = {r1.json()["id"], r2.json()["id"], r3.json()["id"]}

    assert len(ids) == 3, "Each todo should have a unique ID"


# ── Test: validation ──────────────────────────────────────────────────

def test_create_todo_requires_title(client):
    """POST /todos without a title should return a validation error.

    WHY: The TodoCreate schema requires a title field. FastAPI/Pydantic
    should reject requests that do not include it and return 422
    (Unprocessable Entity).
    """
    response = client.post("/todos", json={})

    assert response.status_code == 422, "Missing required field should return 422"
