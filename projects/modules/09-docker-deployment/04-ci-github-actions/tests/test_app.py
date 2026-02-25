# ============================================================================
# tests/test_app.py — Endpoint Tests
# ============================================================================
# These tests verify that the FastAPI endpoints return the expected responses.
# The CI pipeline (GitHub Actions) runs these tests automatically on every
# push. If any test fails, the pipeline fails and the build is marked red.
#
# Run locally:
#   pytest tests/ -v
#
# FastAPI provides a TestClient that sends HTTP requests to your app without
# starting a real server. It is fast and does not require an open port.
# ============================================================================

from fastapi.testclient import TestClient

# ----------------------------------------------------------------------------
# Import the FastAPI app instance so TestClient can send requests to it.
# ----------------------------------------------------------------------------
from app import app

# ----------------------------------------------------------------------------
# Create a test client. This wraps your app and lets you call .get(), .post(),
# etc. as if you were making real HTTP requests.
# ----------------------------------------------------------------------------
client = TestClient(app)


# ----------------------------------------------------------------------------
# Test: GET / returns the welcome message.
# ----------------------------------------------------------------------------
def test_read_root():
    """The root endpoint should return a welcome message and version."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello from CI!"
    assert "version" in data


# ----------------------------------------------------------------------------
# Test: GET /health returns healthy status.
# ----------------------------------------------------------------------------
def test_health_check():
    """The health endpoint should return status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ----------------------------------------------------------------------------
# Test: GET /add/{a}/{b} adds two integers.
# ----------------------------------------------------------------------------
def test_add():
    """The add endpoint should return the sum of two integers."""
    response = client.get("/add/3/5")
    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 3
    assert data["b"] == 5
    assert data["result"] == 8


# ----------------------------------------------------------------------------
# Test: GET /add with non-integer input returns 422.
# FastAPI validates path parameters using type hints. Passing a string
# where an int is expected results in a 422 Unprocessable Entity error.
# ----------------------------------------------------------------------------
def test_add_invalid_input():
    """Non-integer input should return a 422 validation error."""
    response = client.get("/add/three/five")
    assert response.status_code == 422


# ----------------------------------------------------------------------------
# Test: GET /greet/{name} returns a greeting.
# ----------------------------------------------------------------------------
def test_greet():
    """The greet endpoint should return a greeting with the given name."""
    response = client.get("/greet/Alice")
    assert response.status_code == 200
    assert response.json()["greeting"] == "Hello, Alice!"


# ----------------------------------------------------------------------------
# Test: GET /greet/{name}?uppercase=true returns an uppercase greeting.
# ----------------------------------------------------------------------------
def test_greet_uppercase():
    """The uppercase query parameter should uppercase the greeting."""
    response = client.get("/greet/Alice?uppercase=true")
    assert response.status_code == 200
    assert response.json()["greeting"] == "HELLO, ALICE!"
