"""Tests for Module 04 / Project 05 — Full App.

This is the capstone project for the FastAPI module. Tests cover the
full API: registration, login, CRUD with auth, health check, and
custom error handling. Uses an in-memory test database.

WHY test the full app end-to-end?
- This project combines all previous FastAPI concepts into one app.
- End-to-end tests verify the pieces work together, not just individually.
- They catch integration bugs that unit tests might miss.
"""

import sys
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import Base
from app import app
from auth import get_db

# In-memory test database.
TEST_ENGINE = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


def register_and_login(username="testuser", password="testpass123"):
    """Helper: register a user and return auth headers."""
    client.post("/register", json={"username": username, "password": password})
    login_resp = client.post("/login", json={"username": username, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Tests for health check
# ---------------------------------------------------------------------------

def test_health_check():
    """GET /health should return 200 and a healthy status.

    Health endpoints are public — no auth required.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------------------------------------------------------------------
# Tests for user registration and login
# ---------------------------------------------------------------------------

def test_register_returns_user_info():
    """POST /register should create a user and return their ID and username."""
    response = client.post("/register", json={"username": "alice", "password": "secret"})

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_login_returns_jwt():
    """POST /login with valid credentials should return a JWT token."""
    client.post("/register", json={"username": "bob", "password": "pass123"})
    response = client.post("/login", json={"username": "bob", "password": "pass123"})

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_credentials():
    """POST /login with bad credentials should return 401."""
    client.post("/register", json={"username": "carol", "password": "right"})
    response = client.post("/login", json={"username": "carol", "password": "wrong"})

    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Tests for CRUD with authentication
# ---------------------------------------------------------------------------

def test_create_and_read_todo():
    """Full flow: create a todo, then read it back."""
    headers = register_and_login()

    create_resp = client.post("/todos", json={"title": "Full Test"}, headers=headers)
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]

    get_resp = client.get(f"/todos/{todo_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Full Test"


def test_update_todo():
    """Update a todo's title and completed status."""
    headers = register_and_login()
    create_resp = client.post("/todos", json={"title": "Before"}, headers=headers)
    todo_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/todos/{todo_id}",
        json={"title": "After", "completed": True},
        headers=headers,
    )

    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "After"
    assert update_resp.json()["completed"] is True


def test_delete_todo():
    """Delete a todo and verify it is gone."""
    headers = register_and_login()
    create_resp = client.post("/todos", json={"title": "Ephemeral"}, headers=headers)
    todo_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/todos/{todo_id}", headers=headers)
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/todos/{todo_id}", headers=headers)
    assert get_resp.status_code == 404


def test_unauthenticated_access():
    """Accessing /todos without auth should return 403."""
    response = client.get("/todos")
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Tests for error handling
# ---------------------------------------------------------------------------

def test_404_returns_json():
    """A 404 error should return a JSON body with a 'detail' field.

    The custom exception handler ensures consistent JSON error responses.
    """
    headers = register_and_login()
    response = client.get("/todos/99999", headers=headers)

    assert response.status_code == 404
    assert "detail" in response.json()
