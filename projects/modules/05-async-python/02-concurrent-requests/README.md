# Module 05 / Project 02 — Concurrent Requests

Home: [README](../../../../README.md) · Module: [Async Python](../README.md)

## Focus

- `aiohttp` for async HTTP requests
- `aiohttp.ClientSession` for connection reuse
- `asyncio.gather()` to fetch multiple URLs at once
- Comparing sync vs async request times

## Why this project exists

The real power of async shows up when you need to fetch data from many sources. Instead of waiting for each response before making the next request, you fire them all at once. This project makes that difference concrete.

## Run

```bash
cd projects/modules/05-async-python/02-concurrent-requests
pip install -r ../requirements.txt
python project.py
```

## Expected output

```text
--- Sync requests (one at a time) ---
Fetched post 1: "sunt aut facere..." (270 chars) in 0.3s
Fetched post 2: "qui est esse..." (230 chars) in 0.2s
...
Sync total: ~2.5 seconds for 10 requests

--- Async requests (all at once) ---
Fetched post 1: "sunt aut facere..." (270 chars) in 0.3s
Fetched post 3: "ea molestias..." (250 chars) in 0.3s
...
Async total: ~0.4 seconds for 10 requests
```

## Alter it

1. Increase from 10 to 50 URLs. How do the sync vs async times compare now?
2. Add a semaphore (`asyncio.Semaphore(5)`) to limit concurrent requests to 5 at a time.
3. Fetch from two different API endpoints in the same `gather()` call.

## Break it

1. Remove `async with session:` and just use `session = aiohttp.ClientSession()`. What happens?
2. Fetch a URL that does not exist. How does error handling differ from sync?
3. Set a very short timeout (0.001 seconds). What exception do you get?

## Fix it

1. Add `try/except` around each fetch so one failure does not crash the whole batch.
2. Add `asyncio.wait_for()` with a timeout per request.
3. Close the session properly in a `finally` block if you removed the `async with`.

## Explain it

1. Why is `aiohttp` needed instead of just using `requests` with `asyncio`?
2. What does `ClientSession` do that individual requests do not?
3. How does a semaphore help when making hundreds of requests?
4. What happens if you `await` each request individually instead of using `gather()`?

## Mastery check

You can move on when you can:
- use aiohttp to fetch multiple URLs concurrently,
- explain why requests (sync) cannot be used with asyncio effectively,
- add error handling per-request in a batch,
- use a semaphore to limit concurrency.

## Next

[Project 03 — Async File Processing](../03-async-file-processing/)
