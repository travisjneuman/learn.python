"""Tests for Module 05 / Project 04 — Producer-Consumer.

Tests the producer, worker, and pipeline functions using asyncio.Queue.
We use short sleep times and small job counts to keep tests fast.

WHY test async coordination?
- The producer-consumer pattern has subtle bugs: deadlocks, missed sentinels,
  items left in the queue. Tests catch these by running the full pipeline
  and verifying all jobs were processed.
"""

import sys
import os
import asyncio
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import producer, worker, run_pipeline, worker_with_join


# ---------------------------------------------------------------------------
# Tests for producer()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_producer_adds_jobs_to_queue():
    """producer() should put the specified number of jobs on the queue.

    After producing all jobs, it adds sentinel values (None) for each worker.
    """
    queue = asyncio.Queue()

    with patch("project.asyncio.sleep", return_value=None):
        # We need to set NUM_WORKERS so the producer knows how many sentinels to add.
        with patch("project.NUM_WORKERS", 2):
            await producer(queue, num_jobs=5)

    # The queue should contain 5 jobs + 2 sentinel Nones = 7 items.
    assert queue.qsize() == 7


@pytest.mark.asyncio
async def test_producer_sends_sentinel_values():
    """producer() should add one None sentinel per worker.

    Sentinel values tell workers to shut down. Without them, workers
    would wait forever for more jobs.
    """
    queue = asyncio.Queue()

    with patch("project.asyncio.sleep", return_value=None):
        with patch("project.NUM_WORKERS", 3):
            await producer(queue, num_jobs=2)

    # Drain the queue and count the Nones.
    items = []
    while not queue.empty():
        items.append(queue.get_nowait())

    sentinel_count = items.count(None)
    assert sentinel_count == 3


# ---------------------------------------------------------------------------
# Tests for worker()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_worker_processes_jobs():
    """worker() should process jobs from the queue until it receives None.

    Each processed job is added to the results list.
    """
    queue = asyncio.Queue()
    results = []

    # Add 3 jobs and a sentinel.
    for i in range(3):
        await queue.put(f"job_{i}")
    await queue.put(None)  # Sentinel to stop the worker.

    with patch("project.asyncio.sleep", return_value=None):
        await worker("TestWorker", queue, results)

    assert len(results) == 3


@pytest.mark.asyncio
async def test_worker_stops_on_sentinel():
    """worker() should stop when it receives None (sentinel value).

    After receiving None, the worker exits its loop and does not process
    any further items.
    """
    queue = asyncio.Queue()
    results = []

    await queue.put("job_1")
    await queue.put(None)
    await queue.put("job_2")  # This should NOT be processed.

    with patch("project.asyncio.sleep", return_value=None):
        await worker("TestWorker", queue, results)

    assert len(results) == 1
    assert "job_1" in results[0]


# ---------------------------------------------------------------------------
# Tests for worker_with_join()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_worker_with_join_processes_items():
    """worker_with_join() should process all items and call task_done().

    When task_done() is called for every item, queue.join() unblocks.
    """
    queue = asyncio.Queue()
    results = []

    for i in range(3):
        queue.put_nowait(f"item_{i}")

    with patch("project.asyncio.sleep", return_value=None):
        task = asyncio.create_task(worker_with_join("JW", queue, results))

        # Wait for all items to be processed.
        await asyncio.wait_for(queue.join(), timeout=5.0)

        # Cancel the worker (it loops forever otherwise).
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    assert len(results) == 3


# ---------------------------------------------------------------------------
# Tests for run_pipeline() (integration)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_run_pipeline_processes_all_jobs(capsys):
    """run_pipeline() should process all jobs across all workers.

    We patch module constants to use small numbers for fast tests.
    """
    with patch("project.NUM_JOBS", 6), \
         patch("project.NUM_WORKERS", 2), \
         patch("project.QUEUE_SIZE", 4), \
         patch("project.asyncio.sleep", return_value=None), \
         patch("project.random.uniform", return_value=0):
        await run_pipeline()

    output = capsys.readouterr().out
    assert "Processed" in output
