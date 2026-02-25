"""
Challenge 03: Async Web Scraper
Difficulty: Level 7
Topic: Concurrent page fetching with asyncio

Simulate fetching multiple web pages concurrently using asyncio. You will
NOT make real HTTP requests — instead you will use a fake async fetch function
provided below. The goal is to practise asyncio.gather and async/await.

Concepts: async def, await, asyncio.gather, asyncio.sleep.
Review: concepts/async-explained.md

Instructions:
    1. Implement `fetch_page` — an async function that calls the provided
       fetcher, then returns a dict with "url", "status", and "length".
    2. Implement `fetch_all` — takes a list of URLs and a fetcher, fetches
       them ALL concurrently with asyncio.gather, and returns the list of
       result dicts.
    3. Implement `fetch_with_timeout` — same as fetch_page but raises
       asyncio.TimeoutError if the fetch takes longer than *timeout* seconds.
"""

import asyncio
from collections.abc import Awaitable, Callable

# Type alias for the fake fetcher signature
Fetcher = Callable[[str], Awaitable[tuple[int, str]]]


async def fetch_page(url: str, fetcher: Fetcher) -> dict[str, object]:
    """Fetch a single page using *fetcher* and return a result dict.

    The fetcher is an async callable: await fetcher(url) -> (status_code, body).
    Return {"url": url, "status": status_code, "length": len(body)}.
    """
    # YOUR CODE HERE
    ...


async def fetch_all(urls: list[str], fetcher: Fetcher) -> list[dict[str, object]]:
    """Fetch all *urls* concurrently and return a list of result dicts.

    Use asyncio.gather to run all fetches at the same time.
    Return results in the same order as *urls*.
    """
    # YOUR CODE HERE
    ...


async def fetch_with_timeout(
    url: str, fetcher: Fetcher, timeout: float
) -> dict[str, object]:
    """Like fetch_page but raises asyncio.TimeoutError if too slow.

    Use asyncio.wait_for to enforce the timeout.
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
async def _run_tests() -> None:
    # Fake fetcher: returns status 200 and body "content of <url>"
    # with a small simulated delay.
    async def fake_fetcher(url: str) -> tuple[int, str]:
        await asyncio.sleep(0.01)
        return (200, f"content of {url}")

    # Slow fetcher for timeout tests
    async def slow_fetcher(url: str) -> tuple[int, str]:
        await asyncio.sleep(5)
        return (200, "slow")

    # --- fetch_page ---
    result = await fetch_page("https://example.com", fake_fetcher)
    assert result["url"] == "https://example.com"
    assert result["status"] == 200
    assert result["length"] == len("content of https://example.com")

    # --- fetch_all ---
    urls = ["https://a.com", "https://b.com", "https://c.com"]
    results = await fetch_all(urls, fake_fetcher)
    assert len(results) == 3
    assert results[0]["url"] == "https://a.com"
    assert results[2]["url"] == "https://c.com"

    # --- fetch_with_timeout (success) ---
    result = await fetch_with_timeout("https://fast.com", fake_fetcher, timeout=1.0)
    assert result["status"] == 200

    # --- fetch_with_timeout (timeout) ---
    try:
        await fetch_with_timeout("https://slow.com", slow_fetcher, timeout=0.05)
        assert False, "Should have raised TimeoutError"
    except asyncio.TimeoutError:
        pass  # expected

    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(_run_tests())
