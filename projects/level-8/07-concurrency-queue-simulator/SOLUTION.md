# Solution: Level 8 / Project 07 - Concurrency Queue Simulator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Concurrency Queue Simulator -- producer-consumer with threading.Queue."""

from __future__ import annotations

import argparse
import json
import queue
import random
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# WHY bounded Queue? -- Without backpressure, a fast producer exhausts
# memory. queue.Queue(maxsize=N) blocks the producer when full. This is
# exactly how RabbitMQ and Kafka apply backpressure at scale.
@dataclass
class WorkItem:
    task_id: str
    payload: Any
    created_at: float = field(default_factory=time.monotonic)

@dataclass
class WorkResult:
    task_id: str
    status: TaskStatus
    result: Any = None
    error: str = ""
    duration_ms: float = 0.0
    worker_id: str = ""

@dataclass
class SimulationStats:
    produced: int = 0
    consumed: int = 0
    failed: int = 0
    total_processing_ms: float = 0.0
    max_queue_depth: int = 0

    @property
    def avg_processing_ms(self) -> float:
        return round(self.total_processing_ms / self.consumed, 2) if self.consumed else 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "produced": self.produced, "consumed": self.consumed,
            "failed": self.failed, "avg_processing_ms": self.avg_processing_ms,
            "max_queue_depth": self.max_queue_depth,
        }

# WHY a unique object sentinel? -- Using None would prevent caching None
# as a payload. A unique object() is identity-comparable and can never
# collide with real data.
_SHUTDOWN = object()

def producer(work_queue: queue.Queue, items: list[WorkItem],
             rate_limit: float = 0.0, stats: SimulationStats | None = None) -> None:
    for item in items:
        work_queue.put(item)  # blocks when queue is full (backpressure)
        if stats:
            stats.produced += 1
            stats.max_queue_depth = max(stats.max_queue_depth, work_queue.qsize())
        if rate_limit > 0:
            time.sleep(rate_limit)

def send_shutdown(work_queue: queue.Queue, num_consumers: int) -> None:
    # WHY one sentinel per consumer? -- Each consumer must receive its own
    # shutdown signal, otherwise N-1 consumers hang forever.
    for _ in range(num_consumers):
        work_queue.put(_SHUTDOWN)

def consumer(worker_id: str, work_queue: queue.Queue, result_queue: queue.Queue,
             process_fn: Callable[[Any], Any], stats: SimulationStats | None = None) -> None:
    while True:
        item = work_queue.get()
        if item is _SHUTDOWN:  # identity check, not equality
            work_queue.task_done()
            break
        start = time.perf_counter()
        try:
            result_value = process_fn(item.payload)
            elapsed = (time.perf_counter() - start) * 1000
            result = WorkResult(task_id=item.task_id, status=TaskStatus.COMPLETED,
                                result=result_value, duration_ms=round(elapsed, 2),
                                worker_id=worker_id)
            if stats:
                stats.consumed += 1
                stats.total_processing_ms += elapsed
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            result = WorkResult(task_id=item.task_id, status=TaskStatus.FAILED,
                                error=str(exc), duration_ms=round(elapsed, 2),
                                worker_id=worker_id)
            if stats:
                stats.failed += 1
        result_queue.put(result)
        work_queue.task_done()  # signals join() that this item is processed

def run_simulation(num_items: int = 20, num_consumers: int = 3,
                   queue_capacity: int = 10, processing_time: float = 0.01,
                   failure_rate: float = 0.0) -> dict[str, Any]:
    work_queue: queue.Queue = queue.Queue(maxsize=queue_capacity)
    result_queue: queue.Queue = queue.Queue()
    stats = SimulationStats()
    items = [WorkItem(task_id=f"task-{i:04d}", payload={"index": i}) for i in range(num_items)]

    def process(payload: Any) -> dict[str, Any]:
        if random.random() < failure_rate:
            raise RuntimeError(f"Simulated failure for {payload}")
        time.sleep(processing_time)
        return {"processed": True, **payload}

    # WHY daemon=True? -- If a consumer hangs, the program still exits.
    consumer_threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer, daemon=True,
                             args=(f"worker-{i}", work_queue, result_queue, process, stats))
        t.start()
        consumer_threads.append(t)

    producer(work_queue, items, stats=stats)
    send_shutdown(work_queue, num_consumers)
    for t in consumer_threads:
        t.join(timeout=30)

    results = []
    while not result_queue.empty():
        r: WorkResult = result_queue.get()
        results.append({"task_id": r.task_id, "status": r.status.value,
                         "worker": r.worker_id, "duration_ms": r.duration_ms})
    return {
        "config": {"num_items": num_items, "num_consumers": num_consumers,
                    "queue_capacity": queue_capacity},
        "stats": stats.to_dict(), "results_sample": results[:10],
    }

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Producer-consumer queue simulator")
    parser.add_argument("--items", type=int, default=20)
    parser.add_argument("--consumers", type=int, default=3)
    parser.add_argument("--capacity", type=int, default=10)
    parser.add_argument("--processing-time", type=float, default=0.01)
    parser.add_argument("--failure-rate", type=float, default=0.1)
    args = parser.parse_args(argv)
    output = run_simulation(num_items=args.items, num_consumers=args.consumers,
                            queue_capacity=args.capacity, processing_time=args.processing_time,
                            failure_rate=args.failure_rate)
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `queue.Queue` for thread coordination | Thread-safe without explicit locks; built-in blocking provides backpressure | Shared list + threading.Lock -- error-prone manual synchronization |
| Sentinel object for shutdown | Clean signal that cannot collide with real payloads | Thread event flag -- requires polling loops, more complex |
| Separate result queue | Decouples production from result collection; results survive consumer crashes | Shared dict with lock -- adds contention and complexity |
| Daemon threads | Program exits cleanly even if a consumer thread hangs | Non-daemon threads -- can cause program to hang if thread gets stuck |

## Alternative approaches

### Approach B: asyncio-based producer-consumer

```python
import asyncio

async def async_consumer(name: str, q: asyncio.Queue):
    while True:
        item = await q.get()
        if item is None:
            q.task_done()
            break
        await asyncio.sleep(0.01)  # simulate async I/O
        q.task_done()

async def main():
    q = asyncio.Queue(maxsize=10)
    consumers = [asyncio.create_task(async_consumer(f"w-{i}", q)) for i in range(3)]
    for i in range(20):
        await q.put({"task": i})
    for _ in consumers:
        await q.put(None)
    await asyncio.gather(*consumers)
```

**Trade-off:** asyncio uses cooperative multitasking on one thread, avoiding the GIL entirely. Better for I/O-bound work with async-native libraries. Use threading when working with blocking libraries (requests, psycopg2), asyncio for async-native code (aiohttp, asyncpg), and multiprocessing for CPU-bound work.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting shutdown sentinels | Consumer threads hang forever; `join()` blocks indefinitely | Always send exactly `num_consumers` sentinels after all items are produced |
| `num_consumers=0` | Producer blocks on full queue with nobody to drain it; deadlock | Validate `num_consumers >= 1` before starting |
| Race condition on shared `stats` | Two threads incrementing `stats.consumed` can lose updates | Use `threading.Lock` for stats, or accept approximate counts |
