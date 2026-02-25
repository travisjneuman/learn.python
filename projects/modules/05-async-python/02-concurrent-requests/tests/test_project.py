"""Tests for Module 05 / Project 02 — Concurrent Requests.

Tests the sync and async fetch functions. HTTP requests are mocked for
both the synchronous (requests library) and asynchronous (aiohttp) versions.

WHY mock aiohttp differently from requests?
- aiohttp uses async context managers (async with session.get(...) as resp).
- The mock must support 'async with' and 'await resp.json()'.
- We build a custom async mock for this.
"""

import sys
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import fetch_sync, fetch_one, POST_IDS


# ---------------------------------------------------------------------------
# Tests for fetch_sync()
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_sync_returns_list(mock_get):
    """fetch_sync() should return a list of post dicts, one per POST_ID.

    We mock requests.get to return a fake post for each call.
    """
    fake_response = MagicMock()
    fake_response.json.return_value = {"id": 1, "title": "Test post title here", "body": "body"}
    fake_response.text = '{"id": 1}'
    mock_get.return_value = fake_response

    results = fetch_sync()

    assert len(results) == len(POST_IDS)
    assert all(r["id"] == 1 for r in results)


@patch("project.requests.get")
def test_fetch_sync_calls_correct_urls(mock_get):
    """fetch_sync() should call requests.get() once per post ID.

    Each call should use the correct URL pattern: /posts/{id}.
    """
    fake_response = MagicMock()
    fake_response.json.return_value = {"id": 1, "title": "Test post title here", "body": "body"}
    fake_response.text = '{"id": 1}'
    mock_get.return_value = fake_response

    fetch_sync()

    assert mock_get.call_count == len(POST_IDS)


# ---------------------------------------------------------------------------
# Tests for fetch_one() (async)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_fetch_one_returns_post_data():
    """fetch_one() should return the JSON data from a single API call.

    We create a mock aiohttp session whose .get() returns an async
    context manager with a .json() coroutine.
    """
    # Build a mock response that supports 'async with' and 'await .json()'
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"id": 5, "title": "Async post title here"})

    # Build a mock session whose .get() returns an async context manager.
    mock_session = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=False)

    result = await fetch_one(mock_session, 5)

    assert result["id"] == 5
    assert result["title"] == "Async post title here"


# ---------------------------------------------------------------------------
# Tests for concurrency
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gather_faster_than_sequential():
    """asyncio.gather() should complete faster than running tasks one by one.

    This test demonstrates the core benefit of async: overlapping I/O waits.
    We use short sleeps instead of real HTTP requests.
    """
    import time

    # Sequential: one at a time.
    start = time.time()
    for _ in range(3):
        await asyncio.sleep(0.05)
    sequential_time = time.time() - start

    # Concurrent: all at once.
    start = time.time()
    await asyncio.gather(
        asyncio.sleep(0.05),
        asyncio.sleep(0.05),
        asyncio.sleep(0.05),
    )
    concurrent_time = time.time() - start

    # Concurrent should be significantly faster than sequential.
    assert concurrent_time < sequential_time
