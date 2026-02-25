"""Tests for Module 03 / Project 02 — Query Parameters.

Tests the three functions that demonstrate query parameters: fetching by
user with a params dict, fetching by user with a URL string, and pagination.

WHY test both fetch methods?
- The project teaches two ways to pass query params. Tests verify both
  approaches produce correct API calls and handle responses the same way.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import (
    fetch_posts_by_user_params_dict,
    fetch_posts_by_user_url_string,
    paginate_posts,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_POSTS = [
    {"id": 21, "userId": 3, "title": "Post A", "body": "body A"},
    {"id": 22, "userId": 3, "title": "Post B", "body": "body B"},
]


def make_fake_response(json_data):
    """Create a fake Response object that returns the given JSON data."""
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = 200
    return resp


# ---------------------------------------------------------------------------
# Tests for fetch_posts_by_user_params_dict()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_params_dict_passes_user_id(mock_get):
    """fetch_posts_by_user_params_dict() should pass userId as a query param.

    When using the params dict, requests appends ?userId=3 to the URL.
    We verify the params kwarg is correct.
    """
    mock_get.return_value = make_fake_response(SAMPLE_POSTS)

    fetch_posts_by_user_params_dict(3)

    mock_get.assert_called_once()
    # Check the params keyword argument.
    call_kwargs = mock_get.call_args
    assert call_kwargs[1]["params"] == {"userId": 3}


@patch("project.requests.get")
def test_params_dict_returns_posts(mock_get):
    """The function should return the list of posts from the JSON response."""
    mock_get.return_value = make_fake_response(SAMPLE_POSTS)

    result = fetch_posts_by_user_params_dict(3)

    assert len(result) == 2
    assert result[0]["title"] == "Post A"


# ---------------------------------------------------------------------------
# Tests for fetch_posts_by_user_url_string()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_url_string_includes_user_id(mock_get):
    """fetch_posts_by_user_url_string() should embed userId in the URL string.

    The URL should end with ?userId=3 (built manually with .format()).
    """
    mock_get.return_value = make_fake_response(SAMPLE_POSTS)

    fetch_posts_by_user_url_string(3)

    called_url = mock_get.call_args[0][0]
    assert "userId=3" in called_url


@patch("project.requests.get")
def test_url_string_returns_posts(mock_get):
    """The function should return the parsed JSON posts."""
    mock_get.return_value = make_fake_response(SAMPLE_POSTS)

    result = fetch_posts_by_user_url_string(3)

    assert len(result) == 2


# ---------------------------------------------------------------------------
# Tests for paginate_posts()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_paginate_posts_calls_correct_number_of_pages(mock_get, capsys):
    """paginate_posts() should make one request per page.

    With page_size=5 and num_pages=3, there should be 3 GET calls.
    """
    page_data = [{"id": i, "title": f"Post {i}"} for i in range(5)]
    mock_get.return_value = make_fake_response(page_data)

    paginate_posts(page_size=5, num_pages=3)

    assert mock_get.call_count == 3


@patch("project.requests.get")
def test_paginate_posts_uses_start_and_limit(mock_get, capsys):
    """paginate_posts() should pass _start and _limit as query parameters.

    Page 1: _start=0, _limit=5
    Page 2: _start=5, _limit=5
    """
    page_data = [{"id": 1, "title": "Post 1"}]
    mock_get.return_value = make_fake_response(page_data)

    paginate_posts(page_size=5, num_pages=2)

    # Check the params of the first call (page 1).
    first_call_params = mock_get.call_args_list[0][1]["params"]
    assert first_call_params["_start"] == 0
    assert first_call_params["_limit"] == 5

    # Check the params of the second call (page 2).
    second_call_params = mock_get.call_args_list[1][1]["params"]
    assert second_call_params["_start"] == 5
    assert second_call_params["_limit"] == 5
