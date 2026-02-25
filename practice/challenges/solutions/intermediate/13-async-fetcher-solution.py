"""
Solution: Async Fetcher with Concurrency Limit

Approach: Use asyncio.Semaphore to limit the number of concurrent fetches.
Wrap each fetch in a coroutine that acquires the semaphore before running.
Use asyncio.gather to run all fetches concurrently (up to the semaphore
limit) and collect results in input order.
"""

import asyncio


async def async_fetch_one(url: str, fetch_func) -> str:
    """Fetch a single URL using the provided async function."""
    return await fetch_func(url)


async def async_fetch_all(urls: list[str], fetch_func, max_concurrent: int = 5) -> list[str]:
    """Fetch all URLs with a concurrency limit using a Semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url: str) -> str:
        async with semaphore:
            return await fetch_func(url)

    # gather preserves input order in the results
    tasks = [limited_fetch(url) for url in urls]
    return list(await asyncio.gather(*tasks))


if __name__ == "__main__":
    fetch_count = 0
    max_simultaneous = 0
    current_simultaneous = 0

    async def fake_fetch(url: str) -> str:
        nonlocal fetch_count, max_simultaneous, current_simultaneous
        fetch_count += 1
        current_simultaneous += 1
        max_simultaneous = max(max_simultaneous, current_simultaneous)
        await asyncio.sleep(0.02)
        current_simultaneous -= 1
        return f"result:{url}"

    async def test_basic():
        result = await async_fetch_one("http://example.com", fake_fetch)
        assert result == "result:http://example.com"

    asyncio.run(test_basic())

    async def test_all():
        urls = ["a", "b", "c", "d", "e"]
        results = await async_fetch_all(urls, fake_fetch, max_concurrent=5)
        assert results == ["result:a", "result:b", "result:c", "result:d", "result:e"]

    asyncio.run(test_all())

    max_simultaneous = 0
    current_simultaneous = 0

    async def test_concurrency():
        urls = [f"url{i}" for i in range(10)]
        await async_fetch_all(urls, fake_fetch, max_concurrent=3)
        assert max_simultaneous <= 3, f"Concurrency limit exceeded: {max_simultaneous} > 3"

    asyncio.run(test_concurrency())

    async def test_empty():
        results = await async_fetch_all([], fake_fetch, max_concurrent=5)
        assert results == []

    asyncio.run(test_empty())

    async def test_single():
        results = await async_fetch_all(["only"], fake_fetch, max_concurrent=5)
        assert results == ["result:only"]

    asyncio.run(test_single())

    print("All tests passed!")
