"""Tests for the API client.

These tests mock the network calls so they run without internet access.
They must pass before AND after your refactoring.

Run with:
    cd practice/challenges/refactoring/03_copy_paste_api
    python -m pytest tests/
"""

import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from messy import get_users, get_posts, get_comments, get_todos, get_albums, BASE_URL


def _mock_response(data):
    """Create a mock HTTP response."""
    mock = MagicMock()
    mock.read.return_value = json.dumps(data).encode("utf-8")
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


@patch("messy.urllib.request.urlopen")
def test_get_users(mock_urlopen):
    mock_urlopen.return_value = _mock_response([{"id": 1, "name": "Alice"}])
    result = get_users()
    assert result == [{"id": 1, "name": "Alice"}]


@patch("messy.urllib.request.urlopen")
def test_get_posts(mock_urlopen):
    mock_urlopen.return_value = _mock_response([{"id": 1, "title": "Hello"}])
    result = get_posts()
    assert result == [{"id": 1, "title": "Hello"}]


@patch("messy.urllib.request.urlopen")
def test_get_comments(mock_urlopen):
    mock_urlopen.return_value = _mock_response([{"id": 1, "body": "Great post"}])
    result = get_comments()
    assert result == [{"id": 1, "body": "Great post"}]


@patch("messy.urllib.request.urlopen")
def test_get_todos(mock_urlopen):
    mock_urlopen.return_value = _mock_response([{"id": 1, "completed": False}])
    result = get_todos()
    assert result == [{"id": 1, "completed": False}]


@patch("messy.urllib.request.urlopen")
def test_get_albums(mock_urlopen):
    mock_urlopen.return_value = _mock_response([{"id": 1, "title": "Photos"}])
    result = get_albums()
    assert result == [{"id": 1, "title": "Photos"}]


@patch("messy.urllib.request.urlopen")
def test_handles_http_error(mock_urlopen):
    import urllib.error
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://test", code=404, msg="Not Found", hdrs={}, fp=None
    )
    result = get_users()
    assert result is None


@patch("messy.urllib.request.urlopen")
def test_handles_url_error(mock_urlopen):
    import urllib.error
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
    result = get_posts()
    assert result is None


def test_base_url_defined():
    assert BASE_URL == "https://jsonplaceholder.typicode.com"
