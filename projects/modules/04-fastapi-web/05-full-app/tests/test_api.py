# ============================================================================
# tests/test_api.py — Integration tests for the full todo API
# ============================================================================
# These tests use FastAPI's TestClient, which simulates HTTP requests without
# starting a real server. TestClient is built on top of httpx, so the API
# calls look just like real HTTP requests.
#
# Key testing patterns demonstrated here:
# 1. Using a separate test database (in-memory SQLite) so tests do not
#    affect production data.
# 2. Overriding FastAPI dependencies to swap the database session.
# 3. Testing both success cases and error cases (401, 404, etc.).
# 4. Chaining requests (register -> login -> use token -> CRUD operations).
#
# Run: pytest tests/ -v
# ============================================================================

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from auth import get_db
from app import app

# ============================================================================
# Test database setup
# ============================================================================
# We use an in-memory SQLite database for tests. This means:
# - Tests start with a clean database every time.
# - Tests run faster (no disk I/O).
# - Tests do not affect the real database.
#
# "sqlite:///" (no file path) creates an in-memory database.
# ============================================================================
SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    """Provide a test database session instead of the real one.

    This function replaces get_db in the app. Every endpoint that uses
    Depends(get_db) will receive a session connected to the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------------------------------
# Override the get_db dependency so the app uses our test database.
# dependency_overrides is a dict that maps original dependencies to
# replacement functions. This is one of FastAPI's most powerful testing
# features.
# ----------------------------------------------------------------------------
app.dependency_overrides[get_db] = override_get_db


# ============================================================================
# Fixtures
# ============================================================================
# Fixtures run before each test. They set up the environment and clean up
# afterward. The `yield` splits setup (before yield) and teardown (after).
# ============================================================================

@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test, drop them after.

    autouse=True means this fixture runs for every test automatically.
    You do not need to include it as a parameter in each test function.
    """
    # Create all tables in the test database.
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after the test. This ensures each test starts fresh.
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Provide a TestClient instance for making requests."""
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Register a user, log in, and return the Authorization headers.

    Many tests need an authenticated user. This fixture handles the
    register + login flow and returns ready-to-use headers.
    """
    # Register a test user.
    client.post("/register", json={"username": "testuser", "password": "testpass123"})

    # Log in to get a token.
    response = client.post("/login", json={"username": "testuser", "password": "testpass123"})
    token = response.json()["access_token"]

    # Return headers that include the Bearer token.
    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# Tests
# ============================================================================


def test_register_user(client):
    """Test that a new user can register successfully."""
    response = client.post(
        "/register",
        json={"username": "newuser", "password": "password123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data
    # The password should never appear in the response.
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_user(client):
    """Test that registering with an existing username returns 400."""
    # Register the first time.
    client.post("/register", json={"username": "duplicate", "password": "pass1"})

    # Try to register again with the same username.
    response = client.post("/register", json={"username": "duplicate", "password": "pass2"})

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login(client):
    """Test that a registered user can log in and receive a token."""
    # Register first.
    client.post("/register", json={"username": "loginuser", "password": "secret"})

    # Log in.
    response = client.post("/login", json={"username": "loginuser", "password": "secret"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test that wrong password returns 401 Unauthorized."""
    client.post("/register", json={"username": "wrongpass", "password": "correct"})

    response = client.post("/login", json={"username": "wrongpass", "password": "incorrect"})

    assert response.status_code == 401


def test_create_todo(client, auth_headers):
    """Test creating a new todo with authentication."""
    response = client.post(
        "/todos",
        json={"title": "Write tests"},
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_list_todos(client, auth_headers):
    """Test listing todos returns only the authenticated user's todos."""
    # Create two todos.
    client.post("/todos", json={"title": "Todo 1"}, headers=auth_headers)
    client.post("/todos", json={"title": "Todo 2"}, headers=auth_headers)

    # List todos.
    response = client.get("/todos", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


def test_update_todo(client, auth_headers):
    """Test updating a todo's title and completion status."""
    # Create a todo.
    create_response = client.post(
        "/todos",
        json={"title": "Original title"},
        headers=auth_headers,
    )
    todo_id = create_response.json()["id"]

    # Update it.
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "Updated title", "completed": True},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is True


def test_delete_todo(client, auth_headers):
    """Test deleting a todo."""
    # Create a todo.
    create_response = client.post(
        "/todos",
        json={"title": "To be deleted"},
        headers=auth_headers,
    )
    todo_id = create_response.json()["id"]

    # Delete it.
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it is gone.
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_unauthorized_access(client):
    """Test that accessing protected endpoints without a token returns 403.

    FastAPI's HTTPBearer returns 403 Forbidden when no credentials are
    provided (as opposed to 401 when credentials are invalid). This is
    the expected behavior for missing Bearer tokens.
    """
    # Try to list todos without authentication.
    response = client.get("/todos")
    assert response.status_code == 403
