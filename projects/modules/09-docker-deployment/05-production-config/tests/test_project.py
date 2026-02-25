"""
Tests for Project 05 — Production Config

These tests verify the production-ready FastAPI application: configuration
loading, health check, CORS middleware, and the config endpoint. We mock
the database to avoid requiring PostgreSQL for tests.

Why mock the database in these tests?
    The production config project uses SQLAlchemy with a configurable
    DATABASE_URL. In tests, we either use SQLite (the default) or mock
    the database entirely. This keeps tests fast and self-contained.

Run with: pytest tests/test_project.py -v
"""

import os
import sys

import pytest

# Ensure the project directory is on the path so we can import config, app, etc.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from fastapi.testclient import TestClient

from config import Settings


# ── Test: configuration from environment variables ─────────────────────

def test_settings_defaults():
    """Settings should have sensible defaults for local development.

    WHY: The 12-factor app methodology says every setting should have a
    default. If the defaults are wrong, the app will not work locally
    without explicit configuration, which hurts developer experience.
    """
    s = Settings()

    assert s.APP_NAME == "production-app"
    assert s.APP_VERSION == "1.0.0"
    assert s.DEBUG is False, "Debug should default to False (safe for production)"
    assert s.LOG_LEVEL == "INFO"
    assert s.PORT == 8000


def test_settings_debug_parsing(monkeypatch):
    """DEBUG should parse 'true' (case-insensitive) as True.

    WHY: Environment variables are always strings. The Settings class must
    parse 'true', 'True', 'TRUE' as boolean True. Getting this wrong would
    leave debug mode always off or always on.
    """
    monkeypatch.setenv("DEBUG", "True")

    s = Settings()

    assert s.DEBUG is True


def test_settings_allowed_origins_parsing(monkeypatch):
    """ALLOWED_ORIGINS should be split by comma into a list.

    WHY: CORS origins must be a list, but environment variables are strings.
    The split(',') must handle multiple origins correctly.
    """
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://app.com,https://admin.app.com")

    s = Settings()

    assert len(s.ALLOWED_ORIGINS) == 2
    assert "https://app.com" in s.ALLOWED_ORIGINS
    assert "https://admin.app.com" in s.ALLOWED_ORIGINS


# ── Test: FastAPI application endpoints ────────────────────────────────
# Note: importing app triggers database initialization, so we use SQLite default.

@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with SQLite database.

    WHY: We set DATABASE_URL to a temporary SQLite file so the app
    can initialize without PostgreSQL. This is the same fallback
    the app uses for local development.
    """
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")

    # Re-import to pick up the new DATABASE_URL.
    # We must be careful with module reloading in tests.
    from app import app
    return TestClient(app)


def test_root_endpoint(client):
    """GET / should return app metadata.

    WHY: The root endpoint provides quick verification that the app is
    running and reports which version is deployed. Useful after deployments.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_endpoint(client):
    """GET /health should return a health check with database status.

    WHY: Production health checks must include database connectivity.
    If the database is down, the health check should indicate that
    so the orchestrator can take action.
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data, "Should include overall status"
    assert "database" in data, "Should include database status"
    assert "version" in data, "Should include version for deploy verification"


def test_config_endpoint(client):
    """GET /config should return non-sensitive configuration.

    WHY: The config endpoint is useful for debugging deployments. It must
    NOT include sensitive values like DATABASE_URL or API keys. We verify
    it returns safe-to-share settings only.
    """
    response = client.get("/config")

    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "version" in data
    assert "debug" in data
    # Ensure sensitive data is NOT exposed.
    assert "DATABASE_URL" not in str(data), "Should not expose database URL"
    assert "password" not in str(data).lower(), "Should not expose passwords"


def test_unknown_path_returns_404(client):
    """Requesting an unknown path should return 404.

    WHY: A production app must handle unknown routes gracefully instead of
    crashing or returning misleading responses.
    """
    response = client.get("/this/does/not/exist")

    assert response.status_code == 404
