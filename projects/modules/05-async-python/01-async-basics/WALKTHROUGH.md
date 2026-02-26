# Async Basics — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to understand the difference between sequential and concurrent execution using `async`/`await`. If you can write an async function that uses `asyncio.sleep()` and run it with `asyncio.run()`, you are on the right track.

## Thinking Process

Imagine you are cooking dinner. Sequential execution means you boil water, wait until it boils, then chop vegetables, wait until they are chopped, then set the table. Total time: the sum of everything. Concurrent execution means you start the water boiling, chop vegetables while it heats, and set the table during downtime. Total time: roughly the longest single task. The food is the same — you just organized your time better.

Async Python works exactly like that. When one task is waiting (for a network response, a timer, a file read), other tasks can run during that idle time. The key is `await` — it says "I am going to pause here; if anyone else needs the CPU, go ahead." When the thing you awaited finishes, you resume right where you left off.

The critical distinction is between `asyncio.sleep()` and `time.sleep()`. `asyncio.sleep()` cooperates — it lets other tasks run during the wait. `time.sleep()` blocks — it holds onto the CPU and nobody else can run. One is a polite pause; the other is a brick wall.

## Step 1: Define a Coroutine with async def

**What to do:** Write a function using `async def` that simulates a task taking some time.

**Why:** `async def` declares a coroutine — a function that can pause and resume. When you call a regular function, it runs start to finish. When you call a coroutine, it returns a coroutine object that must be scheduled to actually run. This is the fundamental building block of async Python.

```python
import asyncio

async def do_task(name, seconds):
    print(f"  Task {name} starting...")
    await asyncio.sleep(seconds)
    print(f"  Task {name} done after {seconds} second{'s' if seconds != 1 else ''}")
    return f"{name} result"
```

Two details to notice:

- **`async def`** instead of `def` — this makes the function a coroutine.
- **`await asyncio.sleep(seconds)`** pauses this coroutine but lets others run. The `await` keyword is what makes concurrency possible.

**Predict:** What happens if you call `do_task("A", 2)` without `await`? Try it — you will get a coroutine object, not the result.

## Step 2: Run Tasks Sequentially

**What to do:** Write an async function that awaits each task one at a time.

**Why:** Sequential execution is the baseline. Each `await` pauses until the task finishes, then moves to the next one. Total time is the sum of all task durations. This is how regular synchronous code works — one thing at a time. You need to see this before concurrency makes sense.

```python
import time

async def run_sequential():
    print("--- Sequential execution ---")
    start = time.time()

    await do_task("A", 2)
    await do_task("B", 1)
    await do_task("C", 3)

    elapsed = time.time() - start
    print(f"Sequential total: ~{elapsed:.0f} seconds\n")
```

Each `await` blocks the flow — Task B does not start until Task A finishes. The total time is 2 + 1 + 3 = 6 seconds.

**Predict:** If you add a fourth task that takes 4 seconds, what will the total sequential time be?

## Step 3: Run Tasks Concurrently with gather()

**What to do:** Use `asyncio.gather()` to run all tasks at the same time.

**Why:** `gather()` starts all coroutines at once. While Task A is sleeping for 2 seconds, Task B and Task C are also sleeping simultaneously. Nobody blocks anyone else. The total time equals the duration of the longest single task (3 seconds), not the sum.

```python
async def run_concurrent():
    print("--- Concurrent execution ---")
    start = time.time()

    results = await asyncio.gather(
        do_task("A", 2),
        do_task("B", 1),
        do_task("C", 3),
    )

    elapsed = time.time() - start
    print(f"Concurrent total: ~{elapsed:.0f} seconds")
    print(f"Results: {results}\n")
```

The output order changes. Task B finishes first (1 second), then Task A (2 seconds), then Task C (3 seconds). But they all started at the same time.

**Predict:** Look at the concurrent output. The tasks start in order A, B, C, but they finish B, A, C. Why does Task B finish before Task A even though it started after?

## Step 4: Use create_task() for More Control

**What to do:** Use `asyncio.create_task()` to schedule tasks and then await them individually.

**Why:** `gather()` is convenient but gives you all results at once. `create_task()` gives you a Task object for each coroutine, which you can await separately, cancel, or check for errors individually. This is more flexible for complex workflows.

```python
async def run_with_create_task():
    print("--- Using create_task() ---")
    start = time.time()

    task_a = asyncio.create_task(do_task("A", 2))
    task_b = asyncio.create_task(do_task("B", 1))
    task_c = asyncio.create_task(do_task("C", 3))

    result_a = await task_a
    result_b = await task_b
    result_c = await task_c

    elapsed = time.time() - start
    print(f"create_task total: ~{elapsed:.0f} seconds")
```

The tasks start running as soon as you hit the first `await`. Even though you `await task_a` first, all three tasks are already running concurrently.

**Predict:** The total time is still about 3 seconds, same as `gather()`. Why? What would change if you awaited each task immediately after creating it?

## Step 5: Start the Event Loop with asyncio.run()

**What to do:** Write a `main()` coroutine and start it with `asyncio.run()`.

**Why:** `asyncio.run()` is the bridge between synchronous and asynchronous Python. It creates an event loop, runs your main coroutine, and then shuts down the loop. You call it once at the top level — everything inside is async.

```python
async def main():
    await run_sequential()
    await run_concurrent()
    await run_with_create_task()

if __name__ == "__main__":
    asyncio.run(main())
```

**Predict:** What happens if you try to call `asyncio.run()` from inside an async function? Can you nest event loops?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Calling async function without `await` | Forgetting that coroutines must be awaited | Add `await` before every coroutine call |
| Using `time.sleep()` inside async code | Not knowing the difference | Use `asyncio.sleep()` — it cooperates with the event loop |
| `RuntimeError: This event loop is already running` | Calling `asyncio.run()` inside an async context | Use `await` instead; `asyncio.run()` is for the entry point only |
| Tasks appear to run sequentially | Using `await` immediately after each `create_task()` | Create all tasks first, then await them (or use `gather()`) |

## Testing Your Solution

There are no pytest tests for this project — run it and observe the timing:

```bash
python project.py
```

Expected output:
```text
--- Sequential execution ---
  Task A starting...
  Task A done after 2 seconds
  Task B starting...
  Task B done after 1 second
  Task C starting...
  Task C done after 3 seconds
Sequential total: ~6 seconds

--- Concurrent execution ---
  Task A starting...
  Task B starting...
  Task C starting...
  Task B done after 1 second
  Task A done after 2 seconds
  Task C done after 3 seconds
Concurrent total: ~3 seconds
```

The key verification: sequential takes about 6 seconds, concurrent takes about 3 seconds.

## What You Learned

- **`async def`** declares a coroutine — a function that can pause and resume, enabling concurrency without threads.
- **`await`** pauses the current coroutine and lets others run — it is the mechanism that makes concurrent execution possible.
- **`asyncio.gather()`** runs multiple coroutines concurrently and waits for all of them to finish, while **`asyncio.create_task()`** gives you individual handles for more control.
- **`asyncio.sleep()` vs `time.sleep()`** is the critical distinction: `asyncio.sleep()` cooperates with the event loop (others can run), while `time.sleep()` blocks everything.
