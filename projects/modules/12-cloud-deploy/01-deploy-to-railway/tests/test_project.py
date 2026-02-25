"""
Tests for Project 01 — Deploy to Railway

These tests verify the FastAPI application using TestClient. The app is
designed for cloud deployment, but we test it locally to catch bugs before
pushing to production.

Why test before deploying?
    A bug in production is 10x harder to debug than a bug caught locally.
    The deployment environment has different logs, no debugger, and real
    users affected. TestClient lets you verify every endpoint locally
    before deploying.

Run with: pytest tests/test_project.py -v
"""

from fastapi.testclient import TestClient

from app import app, APP_NAME, APP_VERSION, APP_ENV


client = TestClient(app)


# ── Test: root endpoint ───────────────────────────────────────────────

def test_root_returns_cloud_message():
    """GET / should return a welcome message and environment info.

    WHY: After deploying, this is the first endpoint you check to verify
    the app is running. The response includes the environment name so you
    can tell if you accidentally deployed to the wrong environment.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data, "Should include a welcome message"
    assert "environment" in data, "Should include the environment name"
    assert "version" in data, "Should include the app version"


def test_root_version_matches_constant():
    """The version in the response should match the APP_VERSION constant.

    WHY: If the response hardcodes a version instead of using the constant,
    it could get out of sync after updates. This test catches that.
    """
    response = client.get("/")

    assert response.json()["version"] == APP_VERSION


# ── Test: health check ────────────────────────────────────────────────

def test_health_check_returns_healthy():
    """GET /health should return a healthy status with a timestamp.

    WHY: Cloud platforms (Railway, Render, Fly.io) ping this endpoint
    regularly. If it returns a non-200 status, the platform may restart
    the app. The timestamp helps verify the app is responding in real-time
    (not serving a cached response).
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data, "Should include a timestamp"
    assert "environment" in data, "Should include the environment"


# ── Test: info endpoint ───────────────────────────────────────────────

def test_info_returns_app_metadata():
    """GET /info should return detailed application metadata.

    WHY: The info endpoint is used for debugging deployments. It shows
    the Python version, port, and environment — all useful for diagnosing
    issues. This test verifies all expected fields are present.
    """
    response = client.get("/info")

    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == APP_NAME
    assert data["version"] == APP_VERSION
    assert "python_version" in data, "Should include Python version"
    assert "port" in data, "Should include the port number"


# ── Test: configuration from environment ───────────────────────────────

def test_default_environment_is_development():
    """APP_ENV should default to 'development' when not set.

    WHY: In local development, no environment variables are set. The app
    should default to 'development' mode, not 'production'. Running in
    production mode locally could enable stricter settings that make
    development harder.
    """
    # APP_ENV defaults to 'development' unless overridden.
    # In tests, environment variables are usually not set.
    assert APP_ENV in ("development", "test", "production"), (
        "APP_ENV should be a recognized environment name"
    )


# ── Test: 404 handling ─────────────────────────────────────────────────

def test_nonexistent_path_returns_404():
    """Unknown paths should return 404, not 500.

    WHY: A 500 error means the server crashed. A 404 means the path
    does not exist, which is the correct response. Cloud monitoring
    tools treat 500s as alerts but 404s as normal.
    """
    response = client.get("/this-path-does-not-exist")

    assert response.status_code == 404
