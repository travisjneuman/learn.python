# Async Explained

Async lets your program do other work while waiting for slow operations (network requests, file reads, database queries).

## The problem async solves

Normal (synchronous) code runs one line at a time:

```python
# This takes 3 seconds total — each request waits for the previous one.
data1 = fetch("https://api1.com")    # 1 second
data2 = fetch("https://api2.com")    # 1 second
data3 = fetch("https://api3.com")    # 1 second
```

With async, all three requests happen at the same time:

```python
# This takes ~1 second total — all three run concurrently.
data1, data2, data3 = await asyncio.gather(
    fetch("https://api1.com"),
    fetch("https://api2.com"),
    fetch("https://api3.com"),
)
```

## Key vocabulary

| Term | Meaning |
|------|---------|
| **Coroutine** | A function defined with `async def`. It can pause and resume. |
| **await** | Pauses the current coroutine until the awaited operation finishes. |
| **Event loop** | The engine that runs coroutines. It decides which one to run next. |
| **Concurrent** | Multiple tasks making progress at the same time (not necessarily in parallel). |

## The basics

```python
import asyncio

async def greet(name, delay):
    await asyncio.sleep(delay)    # Pause without blocking others
    print(f"Hello, {name}!")

async def main():
    # Run two greetings concurrently.
    await asyncio.gather(
        greet("Alice", 2),
        greet("Bob", 1),
    )
    # Output: "Hello, Bob!" (after 1s), then "Hello, Alice!" (after 2s)

asyncio.run(main())
```

## How the event loop works (simplified)

1. You give the event loop some coroutines to run.
2. It starts running the first one.
3. When that coroutine hits `await`, the event loop pauses it and runs another one.
4. When the awaited operation finishes, the event loop resumes that coroutine.
5. This continues until all coroutines are done.

Think of it like a chef cooking multiple dishes. While one dish is in the oven (waiting), the chef works on another. No time is wasted just standing around.

## `asyncio.sleep()` vs `time.sleep()`

```python
# BAD — blocks everything. No other coroutine can run.
import time
time.sleep(5)

# GOOD — pauses this coroutine. Others can run while we wait.
await asyncio.sleep(5)
```

`time.sleep()` is like the chef standing in front of the oven doing nothing. `asyncio.sleep()` is like the chef setting a timer and working on something else.

## `gather()` vs `create_task()`

```python
# gather() — start all at once, wait for all to finish.
results = await asyncio.gather(task_a(), task_b(), task_c())

# create_task() — start a task in the background, get result later.
task = asyncio.create_task(task_a())
# ... do other things ...
result = await task
```

## When to use async

**Good fit:**
- Making many HTTP requests
- Web servers handling many clients (FastAPI)
- Chat applications, WebSockets
- Scraping multiple pages

**Bad fit:**
- CPU-heavy work (math, image processing) — use `multiprocessing` instead
- Simple scripts that do one thing at a time
- When you don't need concurrency

## Common mistakes

**Forgetting to `await`:**
```python
result = some_async_function()    # Returns a coroutine object, not the result!
result = await some_async_function()    # Actually runs and returns the result
```

**Using `time.sleep()` in async code:**
```python
async def bad():
    time.sleep(5)    # Blocks the entire event loop!

async def good():
    await asyncio.sleep(5)    # Only pauses this coroutine
```

**Calling `asyncio.run()` inside async code:**
```python
async def bad():
    asyncio.run(other_coroutine())    # Error: can't start a new loop inside one!

async def good():
    await other_coroutine()    # Just await it directly
```

## Related exercises

- [Module 05 — Async Python](../projects/modules/05-async-python/) (full hands-on async module)
