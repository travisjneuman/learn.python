"""Tests for Module 04 / Project 04 — Authentication.

Tests user registration, login (JWT issuance), and protected todo endpoints.
Uses an in-memory SQLite database and overrides the get_db dependency.

WHY test auth separately from CRUD?
- Authentication introduces a new layer: users must register, log in, and
  send a JWT token. We test each step to verify the full auth flow works.
- Protected endpoints should reject unauthenticated requests with 401/403.
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

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


# ---------------------------------------------------------------------------
# Helper: register and log in
# ---------------------------------------------------------------------------

def register_and_login(username="testuser", password="testpass123"):
    """Register a user and log in, returning the auth header dict.

    This helper simplifies tests that need an authenticated user.
    """
    client.post("/register", json={"username": username, "password": password})
    login_resp = client.post("/login", json={"username": username, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Tests for POST /register
# ---------------------------------------------------------------------------

def test_register_new_user():
    """Registering a new user should return 201 with the user's info."""
    response = client.post("/register", json={"username": "alice", "password": "secret123"})

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_register_duplicate_username():
    """Registering with an existing username should return 400.

    Each username must be unique. The server rejects duplicates.
    """
    client.post("/register", json={"username": "bob", "password": "pass1"})
    response = client.post("/register", json={"username": "bob", "password": "pass2"})

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Tests for POST /login
# ---------------------------------------------------------------------------

def test_login_returns_token():
    """Logging in with valid credentials should return a JWT access token."""
    client.post("/register", json={"username": "carol", "password": "mypass"})
    response = client.post("/login", json={"username": "carol", "password": "mypass"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    """Logging in with the wrong password should return 401 Unauthorized."""
    client.post("/register", json={"username": "dave", "password": "correct"})
    response = client.post("/login", json={"username": "dave", "password": "wrong"})

    assert response.status_code == 401


def test_login_nonexistent_user():
    """Logging in with a username that does not exist should return 401.

    The error message is intentionally vague to avoid leaking whether
    the username exists.
    """
    response = client.post("/login", json={"username": "nobody", "password": "pass"})
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Tests for protected todo endpoints
# ---------------------------------------------------------------------------

def test_list_todos_requires_auth():
    """GET /todos without a token should return 403.

    Protected endpoints require the Authorization: Bearer <token> header.
    """
    response = client.get("/todos")
    assert response.status_code == 403


def test_create_todo_with_auth():
    """An authenticated user should be able to create a todo."""
    headers = register_and_login()

    response = client.post("/todos", json={"title": "Auth Todo"}, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == "Auth Todo"


def test_todos_are_user_scoped():
    """Users should only see their own todos, not other users' todos.

    User A creates a todo. User B should see an empty list.
    """
    headers_a = register_and_login("user_a", "pass_a")
    headers_b = register_and_login("user_b", "pass_b")

    # User A creates a todo.
    client.post("/todos", json={"title": "A's todo"}, headers=headers_a)

    # User B should see no todos.
    response = client.get("/todos", headers=headers_b)
    assert response.json() == []

    # User A should see their todo.
    response = client.get("/todos", headers=headers_a)
    assert len(response.json()) == 1


def test_delete_other_users_todo():
    """A user should not be able to delete another user's todo (404)."""
    headers_a = register_and_login("owner", "pass")
    headers_b = register_and_login("intruder", "pass")

    create_resp = client.post("/todos", json={"title": "Owner's Todo"}, headers=headers_a)
    todo_id = create_resp.json()["id"]

    response = client.delete(f"/todos/{todo_id}", headers=headers_b)
    assert response.status_code == 404
