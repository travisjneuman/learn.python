"""
Tests for Project 05 — Integration Testing

These tests exercise the FastAPI todo API through HTTP requests using
TestClient. Unlike unit tests that call functions directly, these tests
send real HTTP requests (in memory) and check the full response: status
code, headers, and JSON body.

This is integration testing because we are testing the whole stack:
routing, validation, storage, and serialization all working together.

Run with: pytest tests/ -v
"""


# ── List todos ──────────────────────────────────────────────────────────

# WHY: The simplest possible test. A fresh app should have zero todos.
# If this fails, something is fundamentally broken with the app or fixtures.

def test_list_todos_empty(client):
    """A fresh app should return an empty list of todos."""
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


# ── Create todo ─────────────────────────────────────────────────────────

# WHY: Creating a resource is the most important operation to test.
# We verify: correct status code (201), the response contains the data
# we sent, and the server assigned an ID.

def test_create_todo(client):
    """Creating a todo should return 201 and the created todo data."""
    response = client.post("/todos", json={"title": "Buy groceries"})

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["done"] is False


# WHY: Every created todo must get a unique ID. This test verifies
# the ID is present and is an integer. Without this, we cannot
# retrieve or delete specific todos later.

def test_create_todo_returns_id(client):
    """The created todo should have an integer ID."""
    response = client.post("/todos", json={"title": "Read a book"})
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)


# ── Get todo ────────────────────────────────────────────────────────────

# WHY: Requesting a todo that does not exist should return 404, not crash.
# Error handling is just as important as the happy path — clients need
# predictable error responses to handle failures gracefully.

def test_get_todo_not_found(client):
    """Getting a nonexistent todo should return 404."""
    response = client.get("/todos/999")

    assert response.status_code == 404


# WHY: The create-then-retrieve flow is the most basic data persistence
# test. We create a todo and then fetch it by ID to verify it was stored.

def test_create_and_retrieve_todo(client):
    """A created todo should be retrievable by its ID."""
    # Step 1: Create a todo.
    create_response = client.post("/todos", json={"title": "Write tests"})
    todo_id = create_response.json()["id"]

    # Step 2: Retrieve it by ID.
    get_response = client.get(f"/todos/{todo_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Write tests"
    assert get_response.json()["id"] == todo_id


# ── Delete todo ─────────────────────────────────────────────────────────

# WHY: Deletion must actually remove the resource. We verify this by
# creating a todo, deleting it, and then trying to fetch it (expecting 404).

def test_delete_todo(client):
    """Deleting a todo should remove it. Subsequent GET should return 404."""
    # Create a todo.
    create_response = client.post("/todos", json={"title": "Temporary todo"})
    todo_id = create_response.json()["id"]

    # Delete it.
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

    # Verify it is gone.
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


# WHY: Deleting something that does not exist should return 404, not crash.
# This is the same principle as test_get_todo_not_found — predictable errors.

def test_delete_nonexistent_todo(client):
    """Deleting a nonexistent todo should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404


# ── Validation ──────────────────────────────────────────────────────────

# WHY: FastAPI validates request bodies automatically via Pydantic.
# If someone sends invalid data (missing required fields), the API
# should return 422 (Unprocessable Entity), not crash with a 500.

def test_create_todo_invalid_input(client):
    """Sending invalid data should return 422, not a server error."""
    # Send an empty body — title is required.
    response = client.post("/todos", json={})

    assert response.status_code == 422


# ── Full CRUD flow ──────────────────────────────────────────────────────

# WHY: Individual endpoint tests are important, but this test exercises
# the complete lifecycle of a resource: create, read, list, delete, verify.
# This catches bugs that only appear when operations are combined.

def test_full_crud_flow(client):
    """Test the complete create-read-list-delete lifecycle."""
    # 1. Start with an empty list.
    assert client.get("/todos").json() == []

    # 2. Create two todos.
    resp1 = client.post("/todos", json={"title": "First task"})
    resp2 = client.post("/todos", json={"title": "Second task"})
    id1 = resp1.json()["id"]
    id2 = resp2.json()["id"]

    # 3. Verify both appear in the list.
    all_todos = client.get("/todos").json()
    assert len(all_todos) == 2
    titles = [t["title"] for t in all_todos]
    assert "First task" in titles
    assert "Second task" in titles

    # 4. Delete the first todo.
    assert client.delete(f"/todos/{id1}").status_code == 204

    # 5. Verify only the second remains.
    remaining = client.get("/todos").json()
    assert len(remaining) == 1
    assert remaining[0]["id"] == id2
    assert remaining[0]["title"] == "Second task"

    # 6. Verify the first is gone.
    assert client.get(f"/todos/{id1}").status_code == 404
