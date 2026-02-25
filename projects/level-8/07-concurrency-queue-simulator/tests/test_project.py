"""Tests for Concurrency Queue Simulator.

Covers: work items, producer/consumer, stats, simulation, and error handling.
"""

from __future__ import annotations

import queue
import threading

import pytest

from project import (
    SimulationStats,
    TaskStatus,
    WorkItem,
    WorkResult,
    _SHUTDOWN,
    consumer,
    producer,
    run_simulation,
    send_shutdown,
)


# --- SimulationStats ----------------------------------------------------

class TestSimulationStats:
    def test_avg_processing_zero_consumed(self) -> None:
        stats = SimulationStats()
        assert stats.avg_processing_ms == 0.0

    @pytest.mark.parametrize("consumed,total_ms,expected_avg", [
        (10, 100.0, 10.0),
        (3, 30.0, 10.0),
        (1, 5.5, 5.5),
    ])
    def test_avg_processing_calculation(
        self, consumed: int, total_ms: float, expected_avg: float,
    ) -> None:
        stats = SimulationStats(consumed=consumed, total_processing_ms=total_ms)
        assert stats.avg_processing_ms == expected_avg


# --- Producer -----------------------------------------------------------

class TestProducer:
    def test_enqueues_all_items(self) -> None:
        q: queue.Queue = queue.Queue()
        items = [WorkItem(f"t-{i}", {"i": i}) for i in range(5)]
        stats = SimulationStats()
        producer(q, items, stats=stats)
        assert stats.produced == 5
        assert q.qsize() == 5


# --- Consumer -----------------------------------------------------------

class TestConsumer:
    def test_processes_items_until_shutdown(self) -> None:
        work_q: queue.Queue = queue.Queue()
        result_q: queue.Queue = queue.Queue()
        stats = SimulationStats()

        items = [WorkItem(f"t-{i}", i) for i in range(3)]
        for item in items:
            work_q.put(item)
        work_q.put(_SHUTDOWN)

        consumer("w-0", work_q, result_q, lambda x: x * 2, stats)

        assert stats.consumed == 3
        assert result_q.qsize() == 3

    def test_handles_processing_failure(self) -> None:
        work_q: queue.Queue = queue.Queue()
        result_q: queue.Queue = queue.Queue()
        stats = SimulationStats()

        work_q.put(WorkItem("fail-1", "data"))
        work_q.put(_SHUTDOWN)

        def fail_fn(payload):
            raise ValueError("boom")

        consumer("w-0", work_q, result_q, fail_fn, stats)
        assert stats.failed == 1
        result: WorkResult = result_q.get()
        assert result.status == TaskStatus.FAILED
        assert "boom" in result.error


# --- Full simulation ----------------------------------------------------

class TestSimulation:
    def test_all_items_processed(self) -> None:
        result = run_simulation(
            num_items=10, num_consumers=2,
            queue_capacity=5, processing_time=0.001,
            failure_rate=0.0,
        )
        assert result["stats"]["produced"] == 10
        assert result["stats"]["consumed"] == 10
        assert result["stats"]["failed"] == 0

    def test_failure_rate_produces_failures(self) -> None:
        result = run_simulation(
            num_items=50, num_consumers=2,
            queue_capacity=10, processing_time=0.001,
            failure_rate=1.0,  # all fail
        )
        assert result["stats"]["failed"] == 50
        assert result["stats"]["consumed"] == 0
