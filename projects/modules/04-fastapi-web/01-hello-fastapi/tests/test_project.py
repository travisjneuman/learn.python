"""Tests for Module 04 / Project 01 — Hello FastAPI.

Tests the three endpoints (/, /items/{item_id}, /health) using FastAPI's
TestClient. TestClient lets you make HTTP requests to your FastAPI app
without starting a real server.

WHY use TestClient instead of requests?
- TestClient runs the app in-process (no port, no network).
- Tests are fast and don't conflict with anything else running on your machine.
- You get the same request/response interface as a real HTTP client.
"""

import sys
import os

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app

# Create a TestClient that sends requests to our FastAPI app.
client = TestClient(app)


# ---------------------------------------------------------------------------
# Tests for GET /
# ---------------------------------------------------------------------------

def test_root_returns_200():
    """The root endpoint should return HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_returns_welcome_message():
    """The root endpoint should return a JSON body with a greeting message.

    FastAPI automatically converts the returned dict to JSON.
    """
    response = client.get("/")
    data = response.json()

    assert "message" in data
    assert data["message"] == "Hello, FastAPI!"


# ---------------------------------------------------------------------------
# Tests for GET /items/{item_id}
# ---------------------------------------------------------------------------

def test_read_item_returns_item_id():
    """GET /items/42 should return a JSON body with item_id = 42.

    The {item_id} path parameter is extracted from the URL and passed
    to the function. FastAPI validates it as an int automatically.
    """
    response = client.get("/items/42")

    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == 42


def test_read_item_with_query_param():
    """GET /items/42?q=search should include q='search' in the response.

    Query parameters are optional (default None). When provided, they
    appear in the response dict.
    """
    response = client.get("/items/42?q=search")

    assert response.status_code == 200
    data = response.json()
    assert data["q"] == "search"


def test_read_item_without_query_param():
    """GET /items/42 without ?q should return q=None in the response.

    The q parameter defaults to None when not provided.
    """
    response = client.get("/items/42")

    data = response.json()
    assert data["q"] is None


def test_read_item_validates_id_type():
    """GET /items/abc should return 422 because item_id must be an integer.

    FastAPI uses the type hint (item_id: int) to validate the path parameter.
    If the value cannot be converted to int, FastAPI returns 422 Unprocessable Entity.
    """
    response = client.get("/items/abc")

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Tests for GET /health
# ---------------------------------------------------------------------------

def test_health_returns_200():
    """The health endpoint should always return 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_healthy_status():
    """The health endpoint should return {"status": "healthy"}.

    Monitoring tools check this endpoint to verify the server is running.
    """
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "healthy"
