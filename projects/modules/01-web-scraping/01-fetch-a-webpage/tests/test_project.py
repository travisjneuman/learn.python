"""Tests for Module 01 / Project 01 — Fetch a Webpage.

These tests verify that fetch_page() and display_response_info() work
correctly WITHOUT making real HTTP requests. We use unittest.mock.patch
to replace requests.get() with a fake that returns controlled data.

WHY mock HTTP requests?
- Tests should be fast and not depend on network access.
- The real server might be slow, down, or rate-limit us.
- Mocking lets us test our code in isolation from external services.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

# Add the project directory to the Python path so we can import project.py.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_page, display_response_info


# ---------------------------------------------------------------------------
# Helpers: create fake response objects
# ---------------------------------------------------------------------------

def make_fake_response(status_code=200, text="<html>Hello</html>", headers=None):
    """Build a MagicMock that behaves like a requests.Response object.

    MagicMock is a flexible fake object — you can set any attribute on it,
    and it will just work. This is much simpler than creating a real Response.
    """
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.headers = headers or {"Content-Type": "text/html; charset=utf-8"}
    return response


# ---------------------------------------------------------------------------
# Tests for fetch_page()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_page_returns_response_object(mock_get):
    """fetch_page() should return the response object from requests.get().

    We check that:
    1. requests.get() is called with the URL we pass in.
    2. The return value is the response object (not .text, not .json()).
    """
    fake = make_fake_response()
    mock_get.return_value = fake

    result = fetch_page("http://example.com")

    # The function should have called requests.get with our URL.
    mock_get.assert_called_once_with("http://example.com")

    # The function should return the full response object.
    assert result is fake


@patch("project.requests.get")
def test_fetch_page_passes_through_error_status(mock_get):
    """fetch_page() should return the response even when the status is not 200.

    The function itself does not raise on error status codes — that is
    handled by the caller (main). We verify the response comes back as-is.
    """
    fake = make_fake_response(status_code=404, text="Not Found")
    mock_get.return_value = fake

    result = fetch_page("http://example.com/missing")

    assert result.status_code == 404


# ---------------------------------------------------------------------------
# Tests for display_response_info()
# ---------------------------------------------------------------------------

def test_display_response_info_prints_status_code(capsys):
    """display_response_info() should print the status code of the response.

    capsys is a pytest fixture that captures stdout. We call the function,
    then check that the captured output contains the expected text.
    """
    fake = make_fake_response(status_code=200, text="A" * 600)

    display_response_info(fake)

    output = capsys.readouterr().out
    assert "200" in output


def test_display_response_info_prints_content_type(capsys):
    """display_response_info() should print the Content-Type header."""
    fake = make_fake_response(headers={"Content-Type": "text/html"})

    display_response_info(fake)

    output = capsys.readouterr().out
    assert "text/html" in output


def test_display_response_info_prints_content_length(capsys):
    """display_response_info() should print the character count of the body.

    We pass a body with a known length and verify the number appears in output.
    """
    body = "x" * 42
    fake = make_fake_response(text=body)

    display_response_info(fake)

    output = capsys.readouterr().out
    assert "42" in output


def test_display_response_info_shows_preview(capsys):
    """display_response_info() should show the first 500 characters of the body.

    If the body is longer than 500 characters, only the first 500 should appear.
    """
    body = "Hello World! " * 100  # Much longer than 500 chars
    fake = make_fake_response(text=body)

    display_response_info(fake)

    output = capsys.readouterr().out
    # The preview should contain text from the body.
    assert "Hello World!" in output
