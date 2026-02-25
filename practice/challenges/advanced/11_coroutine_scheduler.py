"""
Challenge 11: Coroutine Scheduler
Difficulty: Level 9
Topic: Simple cooperative task scheduler

Build a cooperative multitasking scheduler using plain Python generators
(NOT asyncio). Each "task" is a generator that yields to give up control.
The scheduler round-robins between tasks until all are complete.

This is how early async frameworks (like Twisted) worked before asyncio.

Concepts: generators as coroutines, send(), round-robin scheduling, yield.
Review: concepts/async-explained.md, concepts/functions-explained.md

Instructions:
    1. Implement `Scheduler.add_task` — register a generator-based task.
    2. Implement `Scheduler.run` — execute all tasks round-robin.
    3. Implement `Scheduler.run_with_priority` — higher priority = more turns.
"""

from collections import deque
from collections.abc import Generator
from typing import Any


class Scheduler:
    """A cooperative round-robin scheduler for generator-based tasks.

    Each task is a generator that yields a string message on each step.
    The scheduler collects these messages in execution order.
    """

    def __init__(self) -> None:
        self._tasks: deque[tuple[str, Generator[str, None, None], int]] = deque()
        self.log: list[str] = []

    def add_task(
        self, name: str, task: Generator[str, None, None], priority: int = 1
    ) -> None:
        """Register a task with a name and optional priority (default 1).

        Priority determines how many times the task runs per round in
        run_with_priority(). For run(), priority is ignored.
        """
        # YOUR CODE HERE
        ...

    def run(self) -> list[str]:
        """Execute all tasks in round-robin order.

        On each iteration:
        1. Pop the next task from the front of the queue.
        2. Advance it with next().
        3. Append "<name>:<yielded_message>" to self.log.
        4. If the task is not exhausted, push it to the back of the queue.
        5. If StopIteration, the task is done — do not re-queue it.

        Return self.log when all tasks are complete.
        """
        # YOUR CODE HERE
        ...

    def run_with_priority(self) -> list[str]:
        """Like run(), but high-priority tasks get more turns per round.

        A task with priority=2 gets next() called TWICE (if still alive)
        before moving to the next task. Priority=3 means three calls, etc.

        If the task exhausts during its priority turns, stop early for that task.
        """
        # YOUR CODE HERE
        ...


# ---------------------------------------------------------------------------
# Helper: sample task generators
# ---------------------------------------------------------------------------
def counting_task(prefix: str, n: int) -> Generator[str, None, None]:
    """Yield '<prefix>-<i>' for i in 1..n."""
    for i in range(1, n + 1):
        yield f"{prefix}-{i}"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Basic round-robin ---
    s = Scheduler()
    s.add_task("A", counting_task("a", 2))
    s.add_task("B", counting_task("b", 3))

    log = s.run()
    # Round 1: A yields a-1, B yields b-1
    # Round 2: A yields a-2, B yields b-2
    # Round 3: A is done, B yields b-3
    assert log == ["A:a-1", "B:b-1", "A:a-2", "B:b-2", "B:b-3"], f"Got {log}"

    # --- Single task ---
    s2 = Scheduler()
    s2.add_task("solo", counting_task("s", 2))
    assert s2.run() == ["solo:s-1", "solo:s-2"]

    # --- Empty scheduler ---
    s3 = Scheduler()
    assert s3.run() == []

    # --- Priority scheduling ---
    s4 = Scheduler()
    s4.add_task("fast", counting_task("f", 4), priority=2)
    s4.add_task("slow", counting_task("s", 2), priority=1)

    log4 = s4.run_with_priority()
    # Round 1: fast gets 2 turns (f-1, f-2), slow gets 1 turn (s-1)
    # Round 2: fast gets 2 turns (f-3, f-4), slow gets 1 turn (s-2)
    assert log4 == [
        "fast:f-1", "fast:f-2", "slow:s-1",
        "fast:f-3", "fast:f-4", "slow:s-2",
    ], f"Got {log4}"

    # Priority task finishes mid-turn
    s5 = Scheduler()
    s5.add_task("short", counting_task("x", 1), priority=3)
    s5.add_task("long", counting_task("y", 2), priority=1)
    log5 = s5.run_with_priority()
    # Round 1: short gets 3 turns but only has 1 yield, then long gets 1 turn
    # Round 2: long gets 1 turn
    assert log5 == ["short:x-1", "long:y-1", "long:y-2"], f"Got {log5}"

    print("All tests passed.")
