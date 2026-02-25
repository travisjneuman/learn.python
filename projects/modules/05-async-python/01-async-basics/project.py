"""
Async Basics — Understanding async/await and the event loop.

This project shows the difference between running tasks one-at-a-time
(sequential) and running them at the same time (concurrent) using asyncio.

Key concepts:
- async def: declares a coroutine (a function that can pause and resume)
- await: pauses the coroutine until the awaited thing finishes
- asyncio.run(): starts the event loop and runs your main coroutine
- asyncio.gather(): runs multiple coroutines concurrently
- asyncio.sleep(): pauses WITHOUT blocking other tasks (unlike time.sleep)
"""

import asyncio
import time


# ── A simple async task ──────────────────────────────────────────────
#
# This function is a "coroutine" because it uses "async def".
# When you call it, it does NOT run immediately — it returns a coroutine
# object. You must "await" it or pass it to gather() to actually run it.

async def do_task(name, seconds):
    """Simulate a task that takes some time (like a network request)."""
    print(f"  Task {name} starting...")
    # asyncio.sleep() pauses THIS coroutine but lets others run.
    # This is the key difference from time.sleep(), which blocks everything.
    await asyncio.sleep(seconds)
    print(f"  Task {name} done after {seconds} second{'s' if seconds != 1 else ''}")
    return f"{name} result"


# ── Sequential execution ─────────────────────────────────────────────
#
# Running tasks one after another. Each task must finish before the
# next one starts. Total time = sum of all task times.

async def run_sequential():
    print("--- Sequential execution ---")
    start = time.time()

    # Each "await" waits for the task to finish before moving on.
    await do_task("A", 2)
    await do_task("B", 1)
    await do_task("C", 3)

    elapsed = time.time() - start
    print(f"Sequential total: ~{elapsed:.0f} seconds\n")


# ── Concurrent execution ─────────────────────────────────────────────
#
# Running tasks at the same time. asyncio.gather() starts all tasks
# and waits for ALL of them to finish. Total time = longest task time.

async def run_concurrent():
    print("--- Concurrent execution ---")
    start = time.time()

    # gather() starts all three tasks at once.
    # While Task A is sleeping, Task B and C are also sleeping.
    # Nobody blocks anyone else.
    results = await asyncio.gather(
        do_task("A", 2),
        do_task("B", 1),
        do_task("C", 3),
    )

    elapsed = time.time() - start
    print(f"Concurrent total: ~{elapsed:.0f} seconds")
    print(f"Results: {results}\n")


# ── Bonus: creating tasks explicitly ─────────────────────────────────
#
# asyncio.create_task() schedules a coroutine to run soon.
# This gives you more control than gather().

async def run_with_create_task():
    print("--- Using create_task() ---")
    start = time.time()

    # create_task() schedules the coroutine and returns a Task object.
    # The task starts running as soon as we hit an "await" anywhere.
    task_a = asyncio.create_task(do_task("A", 2))
    task_b = asyncio.create_task(do_task("B", 1))
    task_c = asyncio.create_task(do_task("C", 3))

    # Now we await each task to get its result.
    result_a = await task_a
    result_b = await task_b
    result_c = await task_c

    elapsed = time.time() - start
    print(f"create_task total: ~{elapsed:.0f} seconds")
    print(f"Results: {[result_a, result_b, result_c]}\n")


# ── Main entry point ─────────────────────────────────────────────────

async def main():
    await run_sequential()
    await run_concurrent()
    await run_with_create_task()


if __name__ == "__main__":
    # asyncio.run() creates an event loop, runs main(), then closes the loop.
    # This is the standard way to start an async program.
    asyncio.run(main())
