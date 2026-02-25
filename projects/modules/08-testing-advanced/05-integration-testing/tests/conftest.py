"""
conftest.py — Shared Fixtures for Integration Tests

The key fixture here is `client`, which creates a fresh FastAPI app
and wraps it in a TestClient for each test. This means every test
starts with empty storage — no leftover data from previous tests.

TestClient is from Starlette (which FastAPI is built on). It lets you
make HTTP requests to your FastAPI app without starting a real server.
The requests happen in-memory, so tests are fast and reliable.
"""

import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture
def client():
    """
    Create a fresh TestClient for each test.

    create_app() returns a new FastAPI instance with empty storage.
    TestClient wraps it so we can make requests like client.get("/todos").

    Because this fixture has the default scope ("function"), every test
    gets its own app with its own empty storage. No state leaks.
    """
    app = create_app()
    return TestClient(app)
