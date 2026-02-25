"""Tests for Module 03 / Project 01 — First API Call.

These tests verify that fetch_single_post() correctly calls the API,
parses JSON, and prints the expected information. All HTTP requests are
mocked to avoid network dependencies.

WHY mock the API?
- JSONPlaceholder is a free public API — it could be slow, rate-limited,
  or temporarily down.
- Mocking gives us instant, repeatable tests with controlled data.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_single_post


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_POST = {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat",
    "body": "quia et suscipit suscipit recusandae"
}


def make_fake_response(json_data=None, status_code=200):
    """Create a fake requests.Response with .json(), .status_code, .headers, and .request."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or SAMPLE_POST
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}
    # The real response has a .request attribute for inspecting sent headers.
    resp.request = MagicMock()
    resp.request.headers = {"User-Agent": "python-requests/2.31.0"}
    return resp


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_single_post_calls_correct_url(mock_get, capsys):
    """fetch_single_post() should call requests.get() with the post/1 URL.

    This verifies we are hitting the right endpoint.
    """
    mock_get.return_value = make_fake_response()

    fetch_single_post()

    mock_get.assert_called_once_with("https://jsonplaceholder.typicode.com/posts/1")


@patch("project.requests.get")
def test_fetch_single_post_prints_status_code(mock_get, capsys):
    """The output should include the HTTP status code (200)."""
    mock_get.return_value = make_fake_response()

    fetch_single_post()

    output = capsys.readouterr().out
    assert "200" in output


@patch("project.requests.get")
def test_fetch_single_post_prints_title(mock_get, capsys):
    """The output should include the post's title field."""
    mock_get.return_value = make_fake_response()

    fetch_single_post()

    output = capsys.readouterr().out
    assert "sunt aut facere repellat" in output


@patch("project.requests.get")
def test_fetch_single_post_prints_post_id(mock_get, capsys):
    """The output should include the post ID."""
    mock_get.return_value = make_fake_response()

    fetch_single_post()

    output = capsys.readouterr().out
    assert "1" in output


@patch("project.requests.get")
def test_fetch_single_post_prints_content_type(mock_get, capsys):
    """The output should include the Content-Type header from the response."""
    mock_get.return_value = make_fake_response()

    fetch_single_post()

    output = capsys.readouterr().out
    assert "application/json" in output
