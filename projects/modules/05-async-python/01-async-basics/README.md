# Module 05 / Project 01 — Async Basics

Home: [README](../../../../README.md) · Module: [Async Python](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- `async def` to define coroutines
- `await` to pause and resume
- `asyncio.run()` to start the event loop
- `asyncio.sleep()` vs `time.sleep()`
- `asyncio.gather()` to run tasks concurrently

## Why this project exists

Before you can use async libraries (aiohttp, FastAPI background tasks, etc.), you need to understand what `async` and `await` actually do. This project builds that foundation with simple, visible examples.

## Run

```bash
cd projects/modules/05-async-python/01-async-basics
python project.py
```

## Expected output

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

## Alter it

1. Add a fourth task that takes 1.5 seconds. Run it both ways and compare times.
2. Change `gather()` to use `asyncio.create_task()` instead. What changes?
3. Add `return_exceptions=True` to `gather()` and make one task raise an error.

## Break it

1. Call an async function without `await`. What happens?
2. Use `time.sleep()` instead of `asyncio.sleep()`. Does concurrency still work? Why not?
3. Try to call `asyncio.run()` from inside an already-running event loop.

## Fix it

1. Replace `time.sleep()` with `asyncio.sleep()` to restore concurrency.
2. Add try/except around tasks to handle errors without crashing the whole group.
3. Use `asyncio.wait()` with `return_when=FIRST_COMPLETED` instead of `gather()`.

## Explain it

1. What is a coroutine and how is it different from a regular function?
2. Why does `time.sleep()` break concurrency but `asyncio.sleep()` does not?
3. What does the event loop actually do?
4. When would you use async instead of threads?

## Mastery check

You can move on when you can:
- explain the difference between `async def` and `def`,
- use `gather()` to run multiple coroutines concurrently,
- predict the output order of concurrent tasks,
- explain why `await` is required.

---

## Related Concepts

- [Async Explained](../../../../concepts/async-explained.md)
- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Async Explained](../../../../concepts/quizzes/async-explained-quiz.py)

## Next

[Project 02 — Concurrent Requests](../02-concurrent-requests/)
