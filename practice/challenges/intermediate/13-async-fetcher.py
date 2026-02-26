"""
Challenge: Async Fetcher with Concurrency Limit
Difficulty: Intermediate
Concepts: asyncio, coroutines, semaphores, gather, async/await
Time: 45 minutes

Implement an async fetcher that processes URLs with a concurrency limit.
Since we cannot make real HTTP requests in tests, simulate fetching with
an async function.

1. `async_fetch_one(url, fetch_func)` -- call the async fetch_func with the url and return the result.
2. `async_fetch_all(urls, fetch_func, max_concurrent)` -- fetch all URLs concurrently,
   but limit concurrency to max_concurrent simultaneous fetches using an asyncio.Semaphore.
   Return results in the same order as the input URLs.

Examples:
    async def fake_fetch(url):
        await asyncio.sleep(0.01)
        return f"content of {url}"

    results = asyncio.run(async_fetch_all(["a", "b", "c"], fake_fetch, max_concurrent=2))
    # ["content of a", "content of b", "content of c"]
"""

import asyncio


async def async_fetch_one(url: str, fetch_func) -> str:
    """Fetch a single URL using the provided async fetch function. Implement this coroutine."""
    # Hint: Just await fetch_func(url) and return the result.
    pass


async def async_fetch_all(urls: list[str], fetch_func, max_concurrent: int = 5) -> list[str]:
    """Fetch all URLs with a concurrency limit. Return results in order. Implement this coroutine."""
    # Hint: Create a Semaphore, wrap each fetch in a semaphore-guarded coroutine, use asyncio.gather.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    fetch_count = 0
    max_simultaneous = 0
    current_simultaneous = 0

    async def fake_fetch(url: str) -> str:
        global fetch_count, max_simultaneous, current_simultaneous
        fetch_count += 1
        current_simultaneous += 1
        max_simultaneous = max(max_simultaneous, current_simultaneous)
        await asyncio.sleep(0.02)
        current_simultaneous -= 1
        return f"result:{url}"

    # Test 1: Basic fetch
    async def test_basic():
        result = await async_fetch_one("http://example.com", fake_fetch)
        assert result == "result:http://example.com", "Basic fetch failed"

    asyncio.run(test_basic())

    # Test 2: Fetch all returns correct results in order
    async def test_all():
        urls = ["a", "b", "c", "d", "e"]
        results = await async_fetch_all(urls, fake_fetch, max_concurrent=5)
        assert results == ["result:a", "result:b", "result:c", "result:d", "result:e"], "Order failed"

    asyncio.run(test_all())

    # Test 3: Concurrency is limited
    max_simultaneous = 0
    current_simultaneous = 0

    async def test_concurrency():
        urls = [f"url{i}" for i in range(10)]
        await async_fetch_all(urls, fake_fetch, max_concurrent=3)
        assert max_simultaneous <= 3, f"Concurrency limit exceeded: {max_simultaneous} > 3"

    asyncio.run(test_concurrency())

    # Test 4: Empty URL list
    async def test_empty():
        results = await async_fetch_all([], fake_fetch, max_concurrent=5)
        assert results == [], "Empty URL list failed"

    asyncio.run(test_empty())

    # Test 5: Single URL
    async def test_single():
        results = await async_fetch_all(["only"], fake_fetch, max_concurrent=5)
        assert results == ["result:only"], "Single URL failed"

    asyncio.run(test_single())

    print("All tests passed!")
