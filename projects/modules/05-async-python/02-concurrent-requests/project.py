"""
Concurrent Requests — Fetching multiple URLs at the same time.

This project compares synchronous requests (one at a time) with
asynchronous requests (all at once) to show the speed difference.

Key concepts:
- aiohttp.ClientSession: an async HTTP client (like requests.Session)
- gather(): run many fetch operations concurrently
- Semaphore: limit how many requests run at the same time
"""

import asyncio
import time

# We use "requests" for the sync version, "aiohttp" for the async version.
import requests
import aiohttp


# ── Configuration ────────────────────────────────────────────────────

# We'll fetch 10 posts from JSONPlaceholder (a free fake API).
BASE_URL = "https://jsonplaceholder.typicode.com"
POST_IDS = list(range(1, 11))  # Posts 1 through 10


# ── Synchronous version ──────────────────────────────────────────────
#
# This fetches one post, waits for the response, then fetches the next.
# Total time ≈ sum of all individual request times.

def fetch_sync():
    print("--- Sync requests (one at a time) ---")
    start = time.time()
    results = []

    for post_id in POST_IDS:
        req_start = time.time()
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        data = response.json()
        elapsed = time.time() - req_start

        title = data["title"][:30]
        print(f"  Fetched post {post_id}: \"{title}...\" ({len(response.text)} chars) in {elapsed:.2f}s")
        results.append(data)

    total = time.time() - start
    print(f"Sync total: ~{total:.1f} seconds for {len(POST_IDS)} requests\n")
    return results


# ── Async version ────────────────────────────────────────────────────
#
# This fires all requests at once and waits for all of them to finish.
# Total time ≈ time of the slowest single request.

async def fetch_one(session, post_id):
    """Fetch a single post using an aiohttp session."""
    req_start = time.time()

    # "async with" ensures the response is properly closed after use.
    async with session.get(f"{BASE_URL}/posts/{post_id}") as response:
        data = await response.json()
        elapsed = time.time() - req_start

        title = data["title"][:30]
        print(f"  Fetched post {post_id}: \"{title}...\" in {elapsed:.2f}s")
        return data


async def fetch_async():
    print("--- Async requests (all at once) ---")
    start = time.time()

    # ClientSession manages connection pooling — it reuses connections
    # to the same server instead of opening a new one each time.
    async with aiohttp.ClientSession() as session:
        # gather() starts ALL requests at the same time.
        # While one request waits for a response, others are also in flight.
        tasks = [fetch_one(session, post_id) for post_id in POST_IDS]
        results = await asyncio.gather(*tasks)

    total = time.time() - start
    print(f"Async total: ~{total:.1f} seconds for {len(POST_IDS)} requests\n")
    return results


# ── Bonus: limited concurrency with semaphore ────────────────────────
#
# Sometimes you don't want to blast a server with 100 requests at once.
# A semaphore limits how many tasks can run at the same time.

async def fetch_one_limited(session, post_id, semaphore):
    """Fetch a single post, but wait for the semaphore first."""
    # "async with semaphore" blocks if too many tasks are already running.
    # Once a task finishes, the semaphore lets the next one through.
    async with semaphore:
        return await fetch_one(session, post_id)


async def fetch_async_limited(max_concurrent=3):
    print(f"--- Async with semaphore (max {max_concurrent} at a time) ---")
    start = time.time()

    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_one_limited(session, post_id, semaphore)
            for post_id in POST_IDS
        ]
        results = await asyncio.gather(*tasks)

    total = time.time() - start
    print(f"Limited async total: ~{total:.1f} seconds for {len(POST_IDS)} requests\n")
    return results


# ── Main ─────────────────────────────────────────────────────────────

async def main():
    # Run the sync version first so you can see the time difference.
    fetch_sync()

    # Then the async version — should be much faster.
    await fetch_async()

    # Then the limited version — faster than sync, slower than unlimited.
    await fetch_async_limited(max_concurrent=3)


if __name__ == "__main__":
    asyncio.run(main())
