"""Tests for Module 03 / Project 03 — POST and Auth.

Tests the three functions: create_post(), get_with_custom_headers(), and
compare_get_and_post(). All HTTP requests are mocked.

WHY test POST requests differently from GET?
- POST sends data in the request body (json=), not the URL.
- We need to verify that the correct data is sent and the response parsed.
"""

import sys
import os
from unittest.mock import patch, MagicMock, call

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import create_post, get_with_custom_headers, compare_get_and_post


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_fake_response(json_data, status_code=200):
    """Create a fake Response with .json(), .status_code, .request."""
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = status_code
    resp.request = MagicMock()
    resp.request.headers = {
        "User-Agent": "learn-python-module03/1.0",
        "Accept": "application/json",
    }
    return resp


# ---------------------------------------------------------------------------
# Tests for create_post()
# ---------------------------------------------------------------------------

@patch("project.requests.post")
def test_create_post_sends_json_body(mock_post, capsys):
    """create_post() should send a POST request with json= (not data=).

    Using json= automatically serializes the dict and sets Content-Type.
    """
    created = {"id": 101, "title": "My First API Post", "body": "...", "userId": 1}
    mock_post.return_value = make_fake_response(created, status_code=201)

    create_post()

    # Verify POST was called with the json keyword argument.
    mock_post.assert_called_once()
    call_kwargs = mock_post.call_args[1]
    assert "json" in call_kwargs
    assert call_kwargs["json"]["title"] == "My First API Post"
    assert call_kwargs["json"]["userId"] == 1


@patch("project.requests.post")
def test_create_post_prints_server_id(mock_post, capsys):
    """create_post() should print the ID assigned by the server."""
    created = {"id": 101, "title": "Test", "body": "Test", "userId": 1}
    mock_post.return_value = make_fake_response(created, status_code=201)

    create_post()

    output = capsys.readouterr().out
    assert "101" in output


# ---------------------------------------------------------------------------
# Tests for get_with_custom_headers()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_custom_headers_sent(mock_get, capsys):
    """get_with_custom_headers() should send User-Agent and Accept headers.

    Custom headers identify your client and tell the server what format
    you want in the response.
    """
    post_data = {"id": 1, "userId": 1, "title": "Test Title", "body": "body"}
    mock_get.return_value = make_fake_response(post_data)

    get_with_custom_headers()

    # Verify headers were passed in the request.
    call_kwargs = mock_get.call_args[1]
    assert "headers" in call_kwargs
    assert call_kwargs["headers"]["User-Agent"] == "learn-python-module03/1.0"
    assert call_kwargs["headers"]["Accept"] == "application/json"


@patch("project.requests.get")
def test_custom_headers_prints_title(mock_get, capsys):
    """get_with_custom_headers() should print the post title from the response."""
    post_data = {"id": 1, "userId": 1, "title": "Test Title", "body": "body"}
    mock_get.return_value = make_fake_response(post_data)

    get_with_custom_headers()

    output = capsys.readouterr().out
    assert "Test Title" in output


# ---------------------------------------------------------------------------
# Tests for compare_get_and_post()
# ---------------------------------------------------------------------------

@patch("project.requests.post")
@patch("project.requests.get")
def test_compare_calls_both_methods(mock_get, mock_post, capsys):
    """compare_get_and_post() should make one GET and one POST request.

    This demonstrates the fundamental difference between the two methods.
    """
    mock_get.return_value = make_fake_response({"id": 1}, status_code=200)
    mock_post.return_value = make_fake_response({"id": 101}, status_code=201)

    compare_get_and_post()

    assert mock_get.call_count == 1
    assert mock_post.call_count == 1


@patch("project.requests.post")
@patch("project.requests.get")
def test_compare_prints_status_codes(mock_get, mock_post, capsys):
    """compare_get_and_post() should print status codes for both requests."""
    mock_get.return_value = make_fake_response({}, status_code=200)
    mock_post.return_value = make_fake_response({}, status_code=201)

    compare_get_and_post()

    output = capsys.readouterr().out
    assert "200" in output
    assert "201" in output
