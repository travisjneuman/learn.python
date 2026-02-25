"""
Tests for Project 02 — Multi-Stage Build

These tests verify the FastAPI application. The focus of this project is
the Dockerfile (single-stage vs multi-stage), but the app code should
still be tested to ensure it works correctly before containerization.

Why the same tests as Project 01?
    The app code is nearly identical to Project 01. The Dockerfiles are
    different, but the Python application is the same. We test the app
    here to verify it works independently of which Dockerfile is used.

Run with: pytest tests/test_project.py -v
"""

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root_returns_welcome_message():
    """GET / should return a welcome message mentioning multi-stage build.

    WHY: This endpoint confirms the correct app is running. The message
    differs from Project 01 to verify you deployed the right image.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "multi-stage" in data["message"].lower(), (
        "Message should mention multi-stage build"
    )


# ── Test: health check ────────────────────────────────────────────────

def test_health_check_returns_healthy():
    """GET /health should return a healthy status.

    WHY: The health endpoint is critical for container orchestration.
    It must work regardless of which Dockerfile built the image.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ── Test: version consistency ──────────────────────────────────────────

def test_root_includes_version():
    """The root endpoint should report the application version.

    WHY: After building and deploying, you need to verify which version
    is running. The version in the response should match app.version.
    """
    response = client.get("/")
    data = response.json()

    assert "version" in data, "Response should include a version field"
    assert data["version"] == "1.0.0"


# ── Test: app metadata ────────────────────────────────────────────────

def test_app_title():
    """The FastAPI app should have the expected title.

    WHY: The app title appears in the auto-generated /docs page. Verifying
    it confirms the right application is being tested.
    """
    assert app.title == "Multi-Stage Build App"
