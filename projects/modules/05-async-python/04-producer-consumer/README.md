# Module 05 / Project 04 — Producer-Consumer

Home: [README](../../../../README.md) · Module: [Async Python](../README.md)

## Focus

- `asyncio.Queue` for task coordination
- Producer-consumer pattern
- Worker pools with multiple consumers
- Graceful shutdown with sentinel values

## Why this project exists

The producer-consumer pattern is everywhere: web scrapers that fetch URLs (producer) and process pages (consumer), log pipelines that collect events and write them to files, API servers that queue background jobs. This project teaches the pattern using asyncio.Queue.

## Run

```bash
cd projects/modules/05-async-python/04-producer-consumer
python project.py
```

## Expected output

```text
--- Producer-Consumer with asyncio.Queue ---
[Producer] Added job: process_item_1
[Producer] Added job: process_item_2
[Worker-1] Processing: process_item_1 (took 0.5s)
[Worker-2] Processing: process_item_2 (took 0.8s)
[Producer] Added job: process_item_3
...
[Producer] Done — added 20 jobs total
[Worker-1] Shutting down
[Worker-2] Shutting down
[Worker-3] Shutting down
Processed 20 jobs in ~X seconds with 3 workers
```

## Alter it

1. Change the number of workers from 3 to 1, then to 10. How does speed change?
2. Add a priority queue — high priority jobs get processed first.
3. Add a "dead letter queue" for jobs that fail, so they can be retried.

## Break it

1. Remove the sentinel values (None). How do the workers know when to stop?
2. Make the queue size 1 (`asyncio.Queue(maxsize=1)`). What happens?
3. Make a worker raise an exception. Does it crash the other workers?

## Fix it

1. Add proper sentinel handling so workers shut down cleanly.
2. Use `queue.join()` to wait for all items to be processed.
3. Add `try/except` in workers so one failure does not stop the pool.

## Explain it

1. Why use a queue instead of just passing a list to each worker?
2. What is a sentinel value and why is it needed for shutdown?
3. How does `maxsize` affect the producer when the queue is full?
4. How would you implement this pattern with threads instead of async?

## Mastery check

You can move on when you can:
- implement a producer that feeds jobs into an asyncio.Queue,
- create multiple worker consumers that process concurrently,
- shut down workers gracefully with sentinel values,
- explain when to use the producer-consumer pattern.

---

## Related Concepts

- [Async Explained](../../../../concepts/async-explained.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [What is a Variable](../../../../concepts/what-is-a-variable.md)
- [Quiz: Async Explained](../../../../concepts/quizzes/async-explained-quiz.py)

## Next

[Project 05 — Async Web Server](../05-async-web-server/)
