"""Tests for Module 03 / Project 05 — API Client Class.

Tests the JSONPlaceholderClient class: URL building, get/create methods,
error handling, and context manager support. All HTTP requests go through
the client's Session, which we mock.

WHY test a class?
- The client encapsulates shared state (base_url, session, headers).
- Testing each method verifies the interface other code depends on.
- Testing the context manager ensures resources are cleaned up properly.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import requests as real_requests
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import JSONPlaceholderClient


# ---------------------------------------------------------------------------
# Tests for _build_url()
# ---------------------------------------------------------------------------

def test_build_url_appends_path():
    """_build_url() should combine the base URL and path without double slashes."""
    client = JSONPlaceholderClient(base_url="https://api.example.com")

    url = client._build_url("/posts/1")

    assert url == "https://api.example.com/posts/1"


def test_build_url_strips_trailing_slash():
    """_build_url() should handle a trailing slash in the base URL gracefully.

    If the user passes 'https://api.example.com/', the slash should be stripped
    before appending the path to avoid 'https://api.example.com//posts'.
    """
    client = JSONPlaceholderClient(base_url="https://api.example.com/")

    url = client._build_url("/posts")

    assert url == "https://api.example.com/posts"


# ---------------------------------------------------------------------------
# Tests for get_post()
# ---------------------------------------------------------------------------

@patch("project.requests.Session")
def test_get_post_returns_dict_on_success(MockSession):
    """get_post() should return the parsed JSON dict when the request succeeds."""
    mock_session = MagicMock()
    MockSession.return_value = mock_session

    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": 1, "title": "Test", "userId": 1}
    fake_response.raise_for_status = MagicMock()
    mock_session.get.return_value = fake_response

    client = JSONPlaceholderClient()
    result = client.get_post(1)

    assert result is not None
    assert result["id"] == 1
    assert result["title"] == "Test"


@patch("project.requests.Session")
def test_get_post_returns_none_on_404(MockSession):
    """get_post() should return None when the post does not exist (404).

    Instead of raising an exception, the client converts 404 into None
    so callers can check with a simple 'if post is None'.
    """
    mock_session = MagicMock()
    MockSession.return_value = mock_session

    fake_response = MagicMock()
    fake_response.status_code = 404
    mock_session.get.return_value = fake_response

    client = JSONPlaceholderClient()
    result = client.get_post(99999)

    assert result is None


@patch("project.requests.Session")
def test_get_post_returns_none_on_connection_error(MockSession):
    """get_post() should return None when the request fails with a network error.

    The client catches RequestException and returns None instead of crashing.
    """
    mock_session = MagicMock()
    MockSession.return_value = mock_session
    mock_session.get.side_effect = real_requests.exceptions.ConnectionError("fail")

    client = JSONPlaceholderClient()
    result = client.get_post(1)

    assert result is None


# ---------------------------------------------------------------------------
# Tests for get_posts()
# ---------------------------------------------------------------------------

@patch("project.requests.Session")
def test_get_posts_returns_list(MockSession):
    """get_posts() should return a list of post dicts."""
    mock_session = MagicMock()
    MockSession.return_value = mock_session

    fake_response = MagicMock()
    fake_response.json.return_value = [{"id": 1}, {"id": 2}]
    fake_response.raise_for_status = MagicMock()
    mock_session.get.return_value = fake_response

    client = JSONPlaceholderClient()
    result = client.get_posts(limit=2)

    assert len(result) == 2


@patch("project.requests.Session")
def test_get_posts_returns_empty_list_on_error(MockSession):
    """get_posts() should return an empty list when the request fails.

    This is safer than returning None because callers can always iterate
    over the result without checking for None first.
    """
    mock_session = MagicMock()
    MockSession.return_value = mock_session
    mock_session.get.side_effect = real_requests.exceptions.Timeout("timeout")

    client = JSONPlaceholderClient()
    result = client.get_posts()

    assert result == []


# ---------------------------------------------------------------------------
# Tests for create_post()
# ---------------------------------------------------------------------------

@patch("project.requests.Session")
def test_create_post_returns_created_data(MockSession):
    """create_post() should return the server's response (with assigned ID)."""
    mock_session = MagicMock()
    MockSession.return_value = mock_session

    fake_response = MagicMock()
    fake_response.json.return_value = {"id": 101, "title": "New Post", "body": "body", "userId": 1}
    fake_response.raise_for_status = MagicMock()
    mock_session.post.return_value = fake_response

    client = JSONPlaceholderClient()
    result = client.create_post(title="New Post", body="body", user_id=1)

    assert result is not None
    assert result["id"] == 101


@patch("project.requests.Session")
def test_create_post_returns_none_on_error(MockSession):
    """create_post() should return None when the POST request fails."""
    mock_session = MagicMock()
    MockSession.return_value = mock_session
    mock_session.post.side_effect = real_requests.exceptions.ConnectionError("fail")

    client = JSONPlaceholderClient()
    result = client.create_post(title="T", body="B", user_id=1)

    assert result is None


# ---------------------------------------------------------------------------
# Tests for context manager
# ---------------------------------------------------------------------------

@patch("project.requests.Session")
def test_context_manager_closes_session(MockSession):
    """Using the client as a context manager should close the session on exit.

    The 'with' block calls __enter__ and __exit__, and __exit__ calls close().
    """
    mock_session = MagicMock()
    MockSession.return_value = mock_session

    with JSONPlaceholderClient() as client:
        pass  # Do nothing — just test the cleanup.

    mock_session.close.assert_called_once()
