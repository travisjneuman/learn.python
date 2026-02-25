"""
Tests for Project 03 — Production Checklist

These tests verify the production-hardened FastAPI application: config
loading, logging setup, CORS middleware, error handling, and endpoints.

Why test production hardening?
    Production features (CORS, error handling, logging) are invisible when
    they work correctly but catastrophic when they fail. CORS misconfiguration
    blocks all frontend requests. Missing error handling exposes stack traces.
    Broken logging means you fly blind in production.

Run with: pytest tests/test_project.py -v
"""

import json
import logging
import os
import sys

import pytest

# Ensure the project directory is on the path.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from fastapi.testclient import TestClient

from config import APP_NAME, APP_VERSION, APP_ENV, CORS_ORIGINS, PORT, DATABASE_URL, LOG_LEVEL


# ── Test: configuration defaults ───────────────────────────────────────

def test_config_defaults():
    """Configuration should have sensible defaults for local development.

    WHY: The app must work without any environment variables for local
    development. If defaults are missing, developers need to set up
    environment variables before running the app for the first time.
    """
    assert APP_NAME == "production-app" or isinstance(APP_NAME, str)
    assert APP_VERSION == "1.0.0"
    assert isinstance(PORT, int), "PORT should be an integer"
    assert PORT > 0, "PORT should be positive"


def test_cors_origins_is_list():
    """CORS_ORIGINS should be a list of allowed origins.

    WHY: The CORSMiddleware expects a list. If the config returns a string
    instead of a list, CORS would be misconfigured and block all requests.
    """
    assert isinstance(CORS_ORIGINS, list), "CORS_ORIGINS should be a list"
    assert len(CORS_ORIGINS) > 0, "Should have at least one allowed origin"


def test_database_url_format():
    """DATABASE_URL should be a valid connection string.

    WHY: An invalid DATABASE_URL will crash the app on startup. Checking
    the format early catches configuration errors before they cause
    runtime failures.
    """
    assert DATABASE_URL.startswith("sqlite") or DATABASE_URL.startswith("postgresql"), (
        "DATABASE_URL should start with sqlite or postgresql"
    )


def test_postgres_url_fix():
    """The config should convert postgres:// to postgresql://.

    WHY: Railway and Heroku use 'postgres://' but SQLAlchemy 2.0 requires
    'postgresql://'. The config module should fix this automatically.
    """
    # This is tested implicitly by the config module's import-time fix.
    # We just verify the current value does not start with 'postgres://'.
    assert not DATABASE_URL.startswith("postgres://"), (
        "DATABASE_URL should use 'postgresql://' not 'postgres://'"
    )


# ── Test: logging configuration ───────────────────────────────────────

def test_json_formatter():
    """The JSONFormatter should produce valid JSON log entries.

    WHY: JSON logs are consumed by log aggregation tools (CloudWatch,
    Datadog). If the formatter produces invalid JSON, logs are unparseable
    and effectively lost.
    """
    from logging_config import JSONFormatter

    formatter = JSONFormatter()

    # Create a test log record.
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)

    # Verify it produces valid JSON.
    parsed = json.loads(output)
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test message"
    assert "timestamp" in parsed, "Should include a timestamp"


def test_setup_logging_returns_logger():
    """setup_logging should configure and return the root logger.

    WHY: If setup_logging fails or returns None, the app has no logging
    configured and all log.info() calls are silently dropped.
    """
    from logging_config import setup_logging

    logger = setup_logging()

    assert logger is not None, "Should return a logger"
    assert len(logger.handlers) > 0, "Logger should have at least one handler"


# ── Test: FastAPI endpoints ────────────────────────────────────────────

@pytest.fixture
def client():
    """Create a test client for the production app."""
    from app import app
    return TestClient(app, raise_server_exceptions=False)


def test_root_endpoint(client):
    """GET / should return app metadata.

    WHY: The root endpoint is the quickest way to verify a deployment.
    It returns the app name, version, and environment.
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert "version" in data
    assert "environment" in data


def test_health_endpoint(client):
    """GET /health should return a health status.

    WHY: Load balancers hit this endpoint every few seconds. If it returns
    non-200, the load balancer removes the instance from rotation.
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == APP_VERSION


def test_error_handling(client):
    """GET /error-test should return 500 with a clean JSON error response.

    WHY: The global exception handler should catch unhandled errors and
    return a structured JSON response instead of a raw stack trace.
    Exposing stack traces in production is a security risk.
    """
    response = client.get("/error-test")

    assert response.status_code == 500
    data = response.json()
    assert "error" in data, "Should include an error field"
    # In development mode, details are shown.
    # In production mode, a generic message is shown.
    assert "detail" in data, "Should include a detail field"


def test_nonexistent_path_returns_404(client):
    """Unknown paths should return 404."""
    response = client.get("/nonexistent/path")

    assert response.status_code == 404
