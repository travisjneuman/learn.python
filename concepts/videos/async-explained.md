# Async Explained — Video Resources

[← Back to Concept](../async-explained.md)

## Best Single Video

**[Python Tutorial: AsyncIO - Complete Guide to Asynchronous Programming](https://youtube.com/watch?v=oAkLSJNr5zY)** by Corey Schafer (~90 min)
Why: The most thorough free asyncio tutorial available. Uses clear visual animations to show what happens at each step: event loops, coroutines, tasks, futures, and the async/await syntax. Covers create_task, asyncio.gather, TaskGroup, error handling, and refactoring blocking I/O with asyncio.to_thread. Start here for a complete mental model.

## Alternatives

- **[Next-Level Concurrent Programming in Python with Asyncio](https://youtube.com/watch?v=GpqAQxH1Afc)** by ArjanCodes (~25 min) — Picks up where the basics leave off: async generators, async comprehensions, converting blocking code to concurrent code, and how concurrency affects software design. A more architecture-focused perspective.
- **[Asyncio: Understanding Async / Await in Python](https://youtube.com/watch?v=2IW-ZEui4h4)** by ArjanCodes (~20 min) — A gentler introduction focused on the core async/await pattern. Demonstrates the performance difference between synchronous and asynchronous code with a practical API-calling example.

## Deep Dives

- **[Python Threading Tutorial](https://youtube.com/watch?v=IEEhzQoKtQU)** by Corey Schafer (~16 min) — Covers threading as an alternative concurrency model. Understanding threads helps you appreciate when asyncio is the better choice and when threading makes more sense.
- **[Python Multiprocessing Tutorial](https://youtube.com/watch?v=fKl2JW_qrso)** by Corey Schafer (~17 min) — Completes the concurrency picture by explaining multiprocessing for CPU-bound tasks. After watching all three (async, threading, multiprocessing), you will understand which tool to reach for in each situation.

---

*Last verified: February 2026*
