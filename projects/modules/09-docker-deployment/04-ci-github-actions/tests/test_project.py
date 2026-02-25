"""
Tests for Project 04 — CI with GitHub Actions (test_project.py)

Additional tests that complement test_app.py. These are the kind of tests
that a CI pipeline would run on every push: fast, reliable, and covering
all endpoints.

Why test before CI?
    CI runs your tests automatically, but you should also run them locally
    first. A failing CI build blocks the entire team. Running tests locally
    catches issues before they reach the shared pipeline.

Run with: pytest tests/test_project.py -v
"""

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root_returns_message():
    """GET / should return a message confirming CI is working.

    WHY: In a CI pipeline, this is the smoke test — if it fails, something
    is fundamentally broken (wrong Python version, missing dependencies, etc.).
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello from CI!"
    assert data["version"] == "1.0.0"


# ── Test: health check ────────────────────────────────────────────────

def test_health_check():
    """GET /health should return healthy status.

    WHY: CI pipelines often start the app and hit the health endpoint to
    verify it boots successfully. This test simulates that check.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ── Test: addition endpoint ───────────────────────────────────────────

def test_add_positive_numbers():
    """GET /add/3/5 should return 8.

    WHY: This endpoint demonstrates path parameter extraction and basic
    computation. Testing with known values verifies both the routing
    and the arithmetic.
    """
    response = client.get("/add/3/5")

    assert response.status_code == 200
    data = response.json()
    assert data["a"] == 3
    assert data["b"] == 5
    assert data["result"] == 8


def test_add_negative_numbers():
    """GET /add/-3/5 should return 2.

    WHY: Negative numbers in URL paths can sometimes cause routing issues.
    This test verifies that FastAPI handles them correctly.
    """
    response = client.get("/add/-3/5")

    assert response.status_code == 200
    assert response.json()["result"] == 2


def test_add_zeros():
    """GET /add/0/0 should return 0.

    WHY: Zero is a common edge case. It verifies there is no off-by-one
    error or special-case handling that breaks for zero.
    """
    response = client.get("/add/0/0")

    assert response.status_code == 200
    assert response.json()["result"] == 0


# ── Test: greeting endpoint ───────────────────────────────────────────

def test_greet_default():
    """GET /greet/Alice should return a greeting in normal case.

    WHY: Tests the default behavior (uppercase=False). The greeting should
    be "Hello, Alice!" exactly.
    """
    response = client.get("/greet/Alice")

    assert response.status_code == 200
    assert response.json()["greeting"] == "Hello, Alice!"


def test_greet_uppercase():
    """GET /greet/Alice?uppercase=true should return an uppercased greeting.

    WHY: Tests the optional query parameter. If the parameter is not parsed
    correctly, the greeting would not be uppercased.
    """
    response = client.get("/greet/Alice?uppercase=true")

    assert response.status_code == 200
    assert response.json()["greeting"] == "HELLO, ALICE!"


def test_greet_preserves_name():
    """The greeting should include the exact name from the URL path.

    WHY: URL encoding or string manipulation could alter the name.
    This test verifies the name passes through unchanged (in lowercase mode).
    """
    response = client.get("/greet/Bob")

    assert "Bob" in response.json()["greeting"]
