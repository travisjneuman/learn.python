# Module 05 — Async Python

Home: [README](../../../README.md) · Modules: [Index](../README.md)

## Prerequisites

- Level 3 complete (you understand packages, error handling, project structure)
- Comfortable with functions and classes

## What you will learn

- How `async` and `await` work under the hood
- Running concurrent tasks with `asyncio`
- Making concurrent HTTP requests with `aiohttp`
- Async generators and file processing
- Producer-consumer patterns with `asyncio.Queue`

## Why async matters

Normal Python runs one thing at a time. When your code waits for a network response or a file read, it just sits there doing nothing. Async lets your code do other work while waiting. This is essential for web servers, scrapers, and anything that talks to external systems.

## Install dependencies

```bash
cd projects/modules/05-async-python
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Projects

| # | Project | Focus |
|---|---------|-------|
| 01 | [Async Basics](./01-async-basics/) | async def, await, asyncio.run(), asyncio.sleep() |
| 02 | [Concurrent Requests](./02-concurrent-requests/) | aiohttp, gather(), fetching multiple URLs at once |
| 03 | [Async File Processing](./03-async-file-processing/) | aiofiles, async generators, processing files concurrently |
| 04 | [Producer-Consumer](./04-producer-consumer/) | asyncio.Queue, task coordination, worker pools |
| 05 | [Async Web Server](./05-async-web-server/) | async FastAPI endpoints, background tasks |

## Related concepts

- [concepts/async-explained.md](../../../concepts/async-explained.md)
- [concepts/decorators-explained.md](../../../concepts/decorators-explained.md)
