"""Tests for Module 03 / Project 04 — Error Handling.

Tests the error handling functions and the retry mechanism. We mock
requests to simulate success, HTTP errors, connection errors, and timeouts.

WHY test error handling?
- Error handling code is often the LEAST tested part of a codebase.
- These tests verify our code handles failures gracefully instead of crashing.
- The retry mechanism has subtle logic (exponential backoff) that is easy to get wrong.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import requests as real_requests
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_with_retry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_success_response():
    """Create a fake successful response (200 OK)."""
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"id": 1, "title": "Test"}
    resp.raise_for_status = MagicMock()  # Does nothing (no error)
    return resp


def make_error_response(status_code=500):
    """Create a fake error response that raises HTTPError on raise_for_status()."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.raise_for_status.side_effect = real_requests.exceptions.HTTPError(
        f"{status_code} Server Error"
    )
    return resp


# ---------------------------------------------------------------------------
# Tests for fetch_with_retry()
# ---------------------------------------------------------------------------

@patch("project.time.sleep")  # Mock sleep to keep tests fast
@patch("project.requests.get")
def test_retry_succeeds_on_first_attempt(mock_get, mock_sleep):
    """If the first request succeeds, fetch_with_retry() should return immediately.

    No retries should happen. sleep() should not be called.
    """
    mock_get.return_value = make_success_response()

    result = fetch_with_retry("http://example.com", max_attempts=3)

    assert result is not None
    assert result.status_code == 200
    assert mock_get.call_count == 1
    mock_sleep.assert_not_called()


@patch("project.time.sleep")
@patch("project.requests.get")
def test_retry_succeeds_after_failures(mock_get, mock_sleep):
    """If early attempts fail, fetch_with_retry() should keep trying.

    We simulate: attempt 1 fails (connection error), attempt 2 succeeds.
    """
    mock_get.side_effect = [
        real_requests.exceptions.ConnectionError("Connection failed"),
        make_success_response(),
    ]

    result = fetch_with_retry("http://example.com", max_attempts=3, base_delay=0.01)

    assert result is not None
    assert result.status_code == 200
    assert mock_get.call_count == 2


@patch("project.time.sleep")
@patch("project.requests.get")
def test_retry_returns_none_after_all_attempts_fail(mock_get, mock_sleep):
    """If all attempts fail, fetch_with_retry() should return None.

    This is the fallback when the server is truly unreachable.
    """
    mock_get.side_effect = real_requests.exceptions.ConnectionError("Connection failed")

    result = fetch_with_retry("http://example.com", max_attempts=3, base_delay=0.01)

    assert result is None
    assert mock_get.call_count == 3


@patch("project.time.sleep")
@patch("project.requests.get")
def test_retry_handles_timeout(mock_get, mock_sleep):
    """fetch_with_retry() should catch Timeout exceptions and retry.

    Timeout means the server did not respond within the time limit.
    """
    mock_get.side_effect = [
        real_requests.exceptions.Timeout("Request timed out"),
        make_success_response(),
    ]

    result = fetch_with_retry("http://example.com", max_attempts=3, base_delay=0.01)

    assert result is not None
    assert mock_get.call_count == 2


@patch("project.time.sleep")
@patch("project.requests.get")
def test_retry_handles_http_error(mock_get, mock_sleep):
    """fetch_with_retry() should catch HTTPError from raise_for_status() and retry.

    A 500 Internal Server Error is retryable — the server might recover.
    """
    mock_get.side_effect = [
        make_error_response(500),
        make_success_response(),
    ]

    result = fetch_with_retry("http://example.com", max_attempts=3, base_delay=0.01)

    assert result is not None
    assert mock_get.call_count == 2


@patch("project.time.sleep")
@patch("project.requests.get")
def test_retry_uses_exponential_backoff(mock_get, mock_sleep):
    """The delay between retries should double each time (exponential backoff).

    With base_delay=1:
    - After attempt 1: sleep(1)   (1 * 2^0)
    - After attempt 2: sleep(2)   (1 * 2^1)
    - Attempt 3 is the last, so no sleep after it.
    """
    mock_get.side_effect = real_requests.exceptions.ConnectionError("fail")

    fetch_with_retry("http://example.com", max_attempts=3, base_delay=1)

    # Should sleep twice (not after the last attempt).
    assert mock_sleep.call_count == 2
    # First delay: 1 * 2^0 = 1
    mock_sleep.assert_any_call(1)
    # Second delay: 1 * 2^1 = 2
    mock_sleep.assert_any_call(2)
