"""
Challenge 09: Async Producer-Consumer
Difficulty: Level 8
Topic: asyncio.Queue producer-consumer pattern

Build a producer-consumer system using asyncio.Queue. Multiple producers
push work items, multiple consumers process them, and a coordinator waits
for everything to finish.

Concepts: asyncio.Queue, asyncio.create_task, sentinel values, task_done().
Review: concepts/async-explained.md

Instructions:
    1. Implement `producer` — puts items into the queue with a small delay.
    2. Implement `consumer` — pulls items, processes them, signals done.
    3. Implement `run_pipeline` — orchestrates producers and consumers.
"""

import asyncio


async def producer(
    name: str,
    items: list[str],
    queue: asyncio.Queue[str | None],
    results: list[str],
) -> None:
    """Put each item from *items* into *queue* with a tiny delay between each.

    After all items are sent, put ONE None sentinel to signal "this producer
    is done." Append "produced:<name>:<item>" to *results* for each item.
    """
    # YOUR CODE HERE
    ...


async def consumer(
    name: str,
    queue: asyncio.Queue[str | None],
    results: list[str],
    num_producers: int,
) -> None:
    """Pull items from *queue* and process them.

    - On receiving a real item, append "consumed:<name>:<item>" to *results*
      and call queue.task_done().
    - On receiving None (sentinel), call queue.task_done() and increment an
      internal counter. When the counter reaches *num_producers*, return
      (all producers are done).
    """
    # YOUR CODE HERE
    ...


async def run_pipeline(
    producer_data: dict[str, list[str]],
    num_consumers: int,
) -> list[str]:
    """Orchestrate the full pipeline.

    Args:
        producer_data: mapping of producer_name -> list of items to produce.
        num_consumers: how many consumer tasks to start.

    Returns:
        The results list containing all "produced:..." and "consumed:..." entries.

    Steps:
        1. Create an asyncio.Queue.
        2. Start a producer task for each entry in producer_data.
        3. Start *num_consumers* consumer tasks.
        4. Wait for all producers to finish.
        5. Wait for the queue to be fully processed (queue.join()).
        6. Cancel consumer tasks and return results.
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
async def _run_tests() -> None:
    results = await run_pipeline(
        producer_data={
            "P1": ["a", "b"],
            "P2": ["c", "d", "e"],
        },
        num_consumers=2,
    )

    produced = [r for r in results if r.startswith("produced:")]
    consumed = [r for r in results if r.startswith("consumed:")]

    # All items were produced
    assert len(produced) == 5, f"Expected 5 produced, got {len(produced)}"
    assert "produced:P1:a" in produced
    assert "produced:P1:b" in produced
    assert "produced:P2:c" in produced

    # All items were consumed
    assert len(consumed) == 5, f"Expected 5 consumed, got {len(consumed)}"
    consumed_items = sorted(r.split(":")[-1] for r in consumed)
    assert consumed_items == ["a", "b", "c", "d", "e"]

    # Single producer, single consumer
    results2 = await run_pipeline({"solo": ["x"]}, num_consumers=1)
    assert "produced:solo:x" in results2
    consumed2 = [r for r in results2 if r.startswith("consumed:")]
    assert len(consumed2) == 1

    print("All tests passed.")


if __name__ == "__main__":
    asyncio.run(_run_tests())
