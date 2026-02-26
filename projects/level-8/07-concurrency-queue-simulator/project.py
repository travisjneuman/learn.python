"""Concurrency Queue Simulator — producer-consumer with threading.Queue.

Design rationale:
    Concurrent processing is fundamental to scalable systems. This project
    implements the producer-consumer pattern using threading and Queue,
    teaching thread coordination, backpressure, and safe shared-state
    access — foundational patterns for task workers, message brokers,
    and pipeline architectures.

Concepts practised:
    - threading.Thread for concurrent execution
    - queue.Queue for thread-safe message passing
    - producer-consumer pattern
    - backpressure via bounded queues
    - graceful shutdown with sentinel values
    - dataclasses for work items and results
"""

from __future__ import annotations

import argparse
import json
import queue
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# WHY a bounded Queue between producer and consumer? -- Without backpressure,
# a fast producer can overwhelm a slow consumer, exhausting memory. A bounded
# queue.Queue blocks the producer when full, applying backpressure automatically.
# This is the same pattern message brokers (RabbitMQ, Kafka) use at scale.
@dataclass
class WorkItem:
    """A unit of work to be processed by a consumer."""
    task_id: str
    payload: Any
    created_at: float = field(default_factory=time.monotonic)


@dataclass
class WorkResult:
    """Result of processing a work item."""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: str = ""
    duration_ms: float = 0.0
    worker_id: str = ""


@dataclass
class SimulationStats:
    """Accumulated statistics from a simulation run."""
    produced: int = 0
    consumed: int = 0
    failed: int = 0
    total_processing_ms: float = 0.0
    max_queue_depth: int = 0

    @property
    def avg_processing_ms(self) -> float:
        if self.consumed == 0:
            return 0.0
        return round(self.total_processing_ms / self.consumed, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "produced": self.produced,
            "consumed": self.consumed,
            "failed": self.failed,
            "avg_processing_ms": self.avg_processing_ms,
            "max_queue_depth": self.max_queue_depth,
        }


# --- Sentinel value for shutdown ----------------------------------------

_SHUTDOWN = object()


# --- Producer -----------------------------------------------------------

def producer(
    work_queue: queue.Queue,
    items: list[WorkItem],
    rate_limit: float = 0.0,
    stats: SimulationStats | None = None,
) -> None:
    """Push work items into the queue at an optional rate limit.

    After all items are enqueued, pushes a _SHUTDOWN sentinel for each
    consumer so they know to stop.
    """
    for item in items:
        work_queue.put(item)
        if stats:
            stats.produced += 1
            stats.max_queue_depth = max(stats.max_queue_depth, work_queue.qsize())
        if rate_limit > 0:
            time.sleep(rate_limit)


def send_shutdown(work_queue: queue.Queue, num_consumers: int) -> None:
    """Send shutdown sentinels to all consumers."""
    for _ in range(num_consumers):
        work_queue.put(_SHUTDOWN)


# --- Consumer -----------------------------------------------------------

def consumer(
    worker_id: str,
    work_queue: queue.Queue,
    result_queue: queue.Queue,
    process_fn: Callable[[Any], Any],
    stats: SimulationStats | None = None,
) -> None:
    """Pull work items from the queue and process them.

    Stops when it receives the _SHUTDOWN sentinel.
    """
    while True:
        item = work_queue.get()
        if item is _SHUTDOWN:
            work_queue.task_done()
            break

        start = time.perf_counter()
        try:
            result_value = process_fn(item.payload)
            elapsed = (time.perf_counter() - start) * 1000
            result = WorkResult(
                task_id=item.task_id,
                status=TaskStatus.COMPLETED,
                result=result_value,
                duration_ms=round(elapsed, 2),
                worker_id=worker_id,
            )
            if stats:
                stats.consumed += 1
                stats.total_processing_ms += elapsed
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            result = WorkResult(
                task_id=item.task_id,
                status=TaskStatus.FAILED,
                error=str(exc),
                duration_ms=round(elapsed, 2),
                worker_id=worker_id,
            )
            if stats:
                stats.failed += 1

        result_queue.put(result)
        work_queue.task_done()


# --- Simulation runner --------------------------------------------------

def run_simulation(
    num_items: int = 20,
    num_consumers: int = 3,
    queue_capacity: int = 10,
    processing_time: float = 0.01,
    failure_rate: float = 0.0,
) -> dict[str, Any]:
    """Run a producer-consumer simulation.

    Args:
        num_items: Number of work items to produce.
        num_consumers: Number of consumer threads.
        queue_capacity: Max queue size (backpressure).
        processing_time: Simulated processing time per item (seconds).
        failure_rate: Probability of failure for each item (0.0-1.0).
    """
    import random

    work_queue: queue.Queue = queue.Queue(maxsize=queue_capacity)
    result_queue: queue.Queue = queue.Queue()
    stats = SimulationStats()

    # Build work items
    items = [WorkItem(task_id=f"task-{i:04d}", payload={"index": i}) for i in range(num_items)]

    # Processing function that simulates work
    def process(payload: Any) -> dict[str, Any]:
        if random.random() < failure_rate:
            raise RuntimeError(f"Simulated failure for {payload}")
        time.sleep(processing_time)
        return {"processed": True, **payload}

    # Start consumer threads
    consumer_threads: list[threading.Thread] = []
    for i in range(num_consumers):
        t = threading.Thread(
            target=consumer,
            args=(f"worker-{i}", work_queue, result_queue, process, stats),
            daemon=True,
        )
        t.start()
        consumer_threads.append(t)

    # Produce items (runs in main thread for simplicity)
    producer(work_queue, items, stats=stats)
    send_shutdown(work_queue, num_consumers)

    # Wait for all consumers to finish
    for t in consumer_threads:
        t.join(timeout=30)

    # Collect results
    results: list[dict[str, Any]] = []
    while not result_queue.empty():
        r: WorkResult = result_queue.get()
        results.append({
            "task_id": r.task_id,
            "status": r.status.value,
            "worker": r.worker_id,
            "duration_ms": r.duration_ms,
        })

    return {
        "config": {
            "num_items": num_items,
            "num_consumers": num_consumers,
            "queue_capacity": queue_capacity,
        },
        "stats": stats.to_dict(),
        "results_sample": results[:10],
    }


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Producer-consumer queue simulator")
    parser.add_argument("--items", type=int, default=20, help="Number of work items")
    parser.add_argument("--consumers", type=int, default=3, help="Number of consumers")
    parser.add_argument("--capacity", type=int, default=10, help="Queue capacity")
    parser.add_argument("--processing-time", type=float, default=0.01, help="Seconds per item")
    parser.add_argument("--failure-rate", type=float, default=0.1, help="Failure probability")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    output = run_simulation(
        num_items=args.items,
        num_consumers=args.consumers,
        queue_capacity=args.capacity,
        processing_time=args.processing_time,
        failure_rate=args.failure_rate,
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
