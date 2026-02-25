"""
Tests for Project 01 — First Dockerfile

These tests verify the FastAPI application itself, NOT the Docker container.
Docker testing requires a running Docker daemon, but the Python app can be
tested with FastAPI's TestClient, which simulates HTTP requests without
starting a real server.

Why test the app separately from Docker?
    Docker packages your app; it does not change how it works. If the app
    works correctly in tests, it will work correctly inside a container
    (as long as the Dockerfile is set up properly). Testing the app is
    fast and reliable; testing Docker requires a running daemon.

Run with: pytest tests/test_project.py -v
"""

from fastapi.testclient import TestClient

from app import app


# ── Create the test client ─────────────────────────────────────────────
# TestClient wraps the FastAPI app so you can make HTTP requests without
# starting uvicorn. It is the standard way to test FastAPI applications.

client = TestClient(app)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root_returns_welcome_message():
    """GET / should return a welcome message and version.

    WHY: The root endpoint is the first thing you check after deploying.
    If it works, the basic build-and-run pipeline is functioning. The
    response includes a version so you can verify which build is running.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data, "Response should include a message"
    assert "Docker" in data["message"], "Message should mention Docker"
    assert data["version"] == "1.0.0", "Version should be 1.0.0"


# ── Test: health check endpoint ───────────────────────────────────────

def test_health_check_returns_healthy():
    """GET /health should return a healthy status.

    WHY: Health check endpoints are called by container orchestrators
    (Kubernetes, Docker Swarm) to determine if the container is alive.
    If this endpoint fails, the orchestrator might restart the container
    unnecessarily.
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy", "Health check should report healthy"


# ── Test: response content type ───────────────────────────────────────

def test_root_returns_json():
    """The root endpoint should return JSON content type.

    WHY: FastAPI returns JSON by default, but if a custom response class
    is accidentally used, the content type could change. API consumers
    rely on the Content-Type header to parse responses correctly.
    """
    response = client.get("/")

    assert "application/json" in response.headers["content-type"]


# ── Test: unknown endpoint returns 404 ─────────────────────────────────

def test_unknown_endpoint_returns_404():
    """Requesting a non-existent path should return 404.

    WHY: A well-behaved API returns 404 for unknown paths, not 500 or 200.
    This verifies that FastAPI's default routing is working correctly.
    """
    response = client.get("/nonexistent")

    assert response.status_code == 404
