"""
Tests for Project 03 — Docker Compose

These tests verify the FastAPI application with an in-memory SQLite database,
independent of Docker and PostgreSQL. In production, docker-compose runs the
app with PostgreSQL, but for testing we use SQLite to keep things fast and
self-contained.

Why SQLite for tests?
    The app reads DATABASE_URL from the environment. By default it falls
    back to SQLite. Tests use this default so they run without Docker or
    PostgreSQL. The SQLAlchemy ORM abstracts away database differences, so
    if it works with SQLite, it almost certainly works with PostgreSQL too.

Run with: pytest tests/test_project.py -v
"""

import os
import sys

import pytest

# We need to set up the database import path before importing app modules.
# The app expects to import from "database" and "models" which are sibling files.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Use a temporary in-memory SQLite database for tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_docker_compose.db")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base


@pytest.fixture
def client(tmp_path):
    """Create a test client with a fresh in-memory database.

    WHY: Each test gets its own database so data from one test does not
    leak into another. We override the database dependency to use a
    temporary SQLite file that is cleaned up after the test.
    """
    # Use a temp SQLite database for this test.
    db_url = f"sqlite:///{tmp_path}/test.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    # Import app and override the get_db dependency.
    from app import app, get_db

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Clean up.
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root_returns_message(client):
    """GET / should return a welcome message mentioning Docker Compose.

    WHY: The root endpoint is the simplest check that the app started
    correctly. The message content confirms which project is running.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "Docker Compose" in data["message"]


# ── Test: create and list items ────────────────────────────────────────

def test_create_item(client):
    """POST /items should create a new item and return it with status 201.

    WHY: This tests the full create flow: request validation (Pydantic),
    database insert (SQLAlchemy), and response serialization. If any
    step fails, the response will be wrong.
    """
    response = client.post("/items", json={"name": "Test Widget", "description": "A test item"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"
    assert data["description"] == "A test item"
    assert "id" in data, "Response should include the generated ID"


def test_list_items_after_create(client):
    """GET /items should return all items in the database.

    WHY: Integration test — verifies that POST stores data that GET can
    retrieve. Tests the full read path: database query -> serialization.
    """
    client.post("/items", json={"name": "Item A"})
    client.post("/items", json={"name": "Item B"})

    response = client.get("/items")

    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2, "Should have 2 items after creating 2"


# ── Test: get item by ID ──────────────────────────────────────────────

def test_get_item_by_id(client):
    """GET /items/{id} should return the specific item.

    WHY: Tests path parameter extraction and single-row database lookup.
    """
    create_response = client.post("/items", json={"name": "Specific Item"})
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Specific Item"


def test_get_nonexistent_item_returns_404(client):
    """GET /items/{id} should return 404 for a non-existent ID.

    WHY: Proper 404 responses are essential for API consumers. Returning
    200 with null would be confusing and non-standard.
    """
    response = client.get("/items/9999")

    assert response.status_code == 404


# ── Test: optional description field ──────────────────────────────────

def test_create_item_without_description(client):
    """Creating an item without a description should succeed.

    WHY: The description field is optional (str | None). This test verifies
    that the Pydantic model and database column handle None correctly.
    """
    response = client.post("/items", json={"name": "No Description"})

    assert response.status_code == 201
    assert response.json()["description"] is None
