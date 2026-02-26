# Level 8 / Project 07 - Concurrency Queue Simulator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Producer-consumer pattern with `threading.Thread`
- Thread-safe message passing via `queue.Queue`
- Backpressure with bounded queues (`maxsize`)
- Graceful shutdown using sentinel values
- Simulation statistics: throughput, queue depth, failure rates

## Why this project exists
Concurrent processing is fundamental to scalable systems — from web servers handling
multiple requests to data pipelines processing millions of events. The producer-consumer
pattern coordinates work between threads without explicit locks. This project simulates
producers pushing work items into a bounded queue and consumers processing them with
configurable failure rates — teaching thread coordination, backpressure, and safe
shutdown, the same architecture behind task workers like Celery, RabbitMQ consumers,
and Kafka pipelines.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/07-concurrency-queue-simulator
python project.py --items 20 --consumers 3 --capacity 10 --failure-rate 0.1
pytest -q
```

## Expected terminal output
```text
{
  "config": {"num_items": 20, "num_consumers": 3, "queue_capacity": 10},
  "stats": {"produced": 20, "consumed": 18, "failed": 2, ...},
  "results_sample": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with simulation results
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `priority` field to `WorkItem` and change consumers to process higher-priority items first (use `queue.PriorityQueue`).
2. Add a `--timeout` flag that limits how long consumers wait for new items.
3. Change `SimulationStats` to track average processing time per consumer thread.

## Break it (required)
1. Set `num_consumers=0` — does the simulation hang or raise an error?
2. Make a producer add items faster than consumers can process — observe queue growth.
3. Remove the sentinel `None` value from the producer — what happens to consumer threads?

## Fix it (required)
1. Validate that `num_consumers >= 1` before starting the simulation.
2. Add a maximum queue size to apply backpressure on producers.
3. Add a test that verifies all consumer threads terminate cleanly.

## Explain it (teach-back)
1. What is the producer-consumer pattern and why is `threading.Queue` thread-safe?
2. How does the sentinel value (`None`) signal consumers to stop — why not just join threads?
3. What is the GIL and how does it affect this threading simulation?
4. When would you use `multiprocessing` instead of `threading` in Python?

## Mastery check
You can move on when you can:
- explain why `queue.Queue` is thread-safe without explicit locks,
- describe how sentinel values enable graceful shutdown,
- run the simulation with different producer/consumer ratios and predict throughput,
- explain the difference between CPU-bound and I/O-bound concurrency in Python.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../06-response-time-profiler/README.md) | [Home](../../../README.md) | [Next →](../08-fault-injection-harness/README.md) |
|:---|:---:|---:|
