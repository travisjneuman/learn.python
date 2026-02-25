"""Tests for the JSONPlaceholder API client.

These tests hit the real JSONPlaceholder API. This is acceptable because:
- JSONPlaceholder is free and designed for testing
- The tests are read-only (GET requests) or use fake writes (POST)
- No rate limiting or API key required

Run with: pytest tests/ -v
"""

import sys
import os

# Add the parent directory to the path so we can import project.py.
# This is necessary because the tests/ folder is a subdirectory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project import JSONPlaceholderClient


def test_get_post_returns_dict():
    """Fetching a valid post should return a dictionary with expected keys."""
    client = JSONPlaceholderClient()
    post = client.get_post(1)
    client.close()

    assert post is not None
    assert isinstance(post, dict)
    assert "id" in post
    assert "title" in post
    assert "body" in post
    assert "userId" in post
    assert post["id"] == 1


def test_get_post_not_found_returns_none():
    """Fetching a nonexistent post should return None, not raise an error."""
    client = JSONPlaceholderClient()
    post = client.get_post(99999)
    client.close()

    assert post is None


def test_get_posts_returns_list():
    """Fetching posts should return a list of dictionaries."""
    client = JSONPlaceholderClient()
    posts = client.get_posts(limit=5)
    client.close()

    assert isinstance(posts, list)
    assert len(posts) == 5
    assert all(isinstance(p, dict) for p in posts)


def test_get_posts_filter_by_user():
    """Filtering posts by user should return only that user's posts."""
    client = JSONPlaceholderClient()
    posts = client.get_posts(user_id=1)
    client.close()

    assert isinstance(posts, list)
    assert len(posts) > 0
    assert all(p["userId"] == 1 for p in posts)


def test_create_post_returns_with_id():
    """Creating a post should return the post data with a server-assigned ID."""
    client = JSONPlaceholderClient()
    created = client.create_post(
        title="Test Post",
        body="Test body content.",
        user_id=1,
    )
    client.close()

    assert created is not None
    assert isinstance(created, dict)
    assert "id" in created
    assert created["title"] == "Test Post"
    assert created["body"] == "Test body content."
    assert created["userId"] == 1


def test_client_as_context_manager():
    """The client should work as a context manager without errors."""
    with JSONPlaceholderClient() as client:
        post = client.get_post(1)

    assert post is not None
    assert post["id"] == 1
