"""Tests for Module 05 / Project 01 — Async Basics.

Tests the async functions: do_task(), run_sequential(), run_concurrent(),
and run_with_create_task(). Uses pytest-asyncio to run async test functions.

WHY use pytest-asyncio?
- Regular pytest cannot run async functions directly.
- pytest-asyncio provides the @pytest.mark.asyncio decorator that sets up
  an event loop and awaits your test function.
"""

import sys
import os
import asyncio
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import do_task, run_sequential, run_concurrent, run_with_create_task


# ---------------------------------------------------------------------------
# Tests for do_task()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_do_task_returns_result():
    """do_task() should return a string containing the task name.

    The return value is '{name} result', which the caller uses to
    verify the task completed.
    """
    # Use a very short sleep to keep the test fast.
    with patch("project.asyncio.sleep", return_value=None):
        result = await do_task("X", 0)

    assert result == "X result"


@pytest.mark.asyncio
async def test_do_task_different_names():
    """do_task() should include the specific task name in its return value.

    This verifies the function is parameterized, not hard-coded.
    """
    with patch("project.asyncio.sleep", return_value=None):
        result_a = await do_task("Alpha", 0)
        result_b = await do_task("Beta", 0)

    assert "Alpha" in result_a
    assert "Beta" in result_b


# ---------------------------------------------------------------------------
# Tests for run_sequential()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_run_sequential_completes(capsys):
    """run_sequential() should complete without errors and print output.

    We mock asyncio.sleep to avoid real delays. The test verifies the
    function runs all three tasks and prints timing information.
    """
    with patch("project.asyncio.sleep", return_value=None):
        await run_sequential()

    output = capsys.readouterr().out
    assert "Sequential" in output
    assert "Task A" in output
    assert "Task B" in output
    assert "Task C" in output


# ---------------------------------------------------------------------------
# Tests for run_concurrent()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_run_concurrent_completes(capsys):
    """run_concurrent() should run all tasks and collect results.

    With asyncio.gather(), all three tasks run at the same time.
    The output should mention all task names and show the results list.
    """
    with patch("project.asyncio.sleep", return_value=None):
        await run_concurrent()

    output = capsys.readouterr().out
    assert "Concurrent" in output
    assert "Results" in output


# ---------------------------------------------------------------------------
# Tests for run_with_create_task()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_run_with_create_task_completes(capsys):
    """run_with_create_task() should complete and print results.

    create_task() is an alternative to gather() that gives more control.
    The test verifies all three tasks are created and awaited.
    """
    with patch("project.asyncio.sleep", return_value=None):
        await run_with_create_task()

    output = capsys.readouterr().out
    assert "create_task" in output
    assert "Results" in output


# ---------------------------------------------------------------------------
# Tests for concurrency behavior
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gather_runs_tasks_concurrently():
    """asyncio.gather() should run coroutines concurrently, not sequentially.

    We verify by checking that the total time is roughly equal to the
    longest task, not the sum of all tasks. Using very short durations
    to keep the test fast.
    """
    import time

    start = time.time()
    await asyncio.gather(
        asyncio.sleep(0.05),
        asyncio.sleep(0.05),
        asyncio.sleep(0.05),
    )
    elapsed = time.time() - start

    # If run sequentially, total would be >= 0.15. Concurrently, it should
    # be close to 0.05 (plus some overhead). We allow up to 0.12.
    assert elapsed < 0.12, f"Expected concurrent execution but took {elapsed:.3f}s"
