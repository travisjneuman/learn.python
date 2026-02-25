"""
Producer-Consumer — Coordinating tasks with asyncio.Queue.

The producer-consumer pattern separates "creating work" from "doing work".
A producer puts jobs on a queue. Workers (consumers) take jobs off the
queue and process them. The queue acts as a buffer between the two.

Key concepts:
- asyncio.Queue: a thread-safe, async-aware queue
- Producer: adds items to the queue
- Consumer (worker): takes items and processes them
- Sentinel values: special values that tell workers to stop
"""

import asyncio
import random
import time


# ── Configuration ────────────────────────────────────────────────────

NUM_JOBS = 20       # Total jobs the producer will create
NUM_WORKERS = 3     # Number of concurrent workers
QUEUE_SIZE = 10     # Max items in the queue at once (0 = unlimited)


# ── Producer ─────────────────────────────────────────────────────────
#
# The producer generates jobs and puts them on the queue.
# If the queue is full (maxsize reached), it waits until a worker
# takes something off.

async def producer(queue, num_jobs):
    """Generate jobs and put them on the queue."""
    for i in range(1, num_jobs + 1):
        job = f"process_item_{i}"

        # put() is async — if the queue is full, this awaits until space opens.
        await queue.put(job)
        print(f"  [Producer] Added job: {job}")

        # Simulate variable production speed.
        await asyncio.sleep(random.uniform(0.05, 0.15))

    # Send a sentinel (None) for each worker so they know to stop.
    # Without this, workers would wait forever for new jobs.
    for _ in range(NUM_WORKERS):
        await queue.put(None)

    print(f"  [Producer] Done — added {num_jobs} jobs total")


# ── Consumer (Worker) ────────────────────────────────────────────────
#
# Each worker runs in a loop, pulling jobs from the queue and
# processing them. When it gets a None (sentinel), it stops.

async def worker(name, queue, results):
    """Pull jobs from the queue and process them."""
    while True:
        # get() is async — if the queue is empty, this awaits until
        # the producer adds something.
        job = await queue.get()

        # Check for sentinel value — means "no more work, shut down".
        if job is None:
            print(f"  [{name}] Shutting down")
            break

        # Simulate processing time (0.2 to 1.0 seconds).
        process_time = random.uniform(0.2, 1.0)
        await asyncio.sleep(process_time)

        result = f"{job} -> done by {name}"
        results.append(result)
        print(f"  [{name}] Processed: {job} (took {process_time:.1f}s)")

        # Tell the queue this job is done.
        # This is used by queue.join() to know when all work is complete.
        queue.task_done()


# ── Run the producer-consumer pipeline ───────────────────────────────

async def run_pipeline():
    print(f"--- Producer-Consumer with asyncio.Queue ---")
    print(f"    {NUM_JOBS} jobs, {NUM_WORKERS} workers, queue size {QUEUE_SIZE}\n")
    start = time.time()

    # Create the queue with a max size.
    # If maxsize=0, the queue has no limit.
    queue = asyncio.Queue(maxsize=QUEUE_SIZE)
    results = []

    # Start the producer and all workers concurrently.
    # The producer feeds jobs into the queue.
    # Workers pull jobs out and process them.
    producer_task = asyncio.create_task(producer(queue, NUM_JOBS))

    worker_tasks = [
        asyncio.create_task(worker(f"Worker-{i+1}", queue, results))
        for i in range(NUM_WORKERS)
    ]

    # Wait for the producer to finish adding all jobs.
    await producer_task

    # Wait for all workers to finish processing.
    await asyncio.gather(*worker_tasks)

    elapsed = time.time() - start
    print(f"\nProcessed {len(results)} jobs in {elapsed:.1f} seconds with {NUM_WORKERS} workers")


# ── Bonus: using queue.join() ────────────────────────────────────────
#
# queue.join() waits until every item that was put() on the queue
# has been processed (task_done() called). This is an alternative
# to sentinel values for knowing when all work is done.

async def run_with_join():
    print("\n--- Alternative: using queue.join() ---\n")
    queue = asyncio.Queue()
    results = []

    # Put all jobs on the queue upfront.
    for i in range(1, 11):
        queue.put_nowait(f"batch_item_{i}")

    # Create workers as background tasks.
    workers = []
    for i in range(3):
        # Workers run forever until cancelled.
        task = asyncio.create_task(worker_with_join(f"JoinWorker-{i+1}", queue, results))
        workers.append(task)

    # Wait until all items have been processed.
    await queue.join()

    # Cancel workers (they're still waiting for more items).
    for task in workers:
        task.cancel()

    print(f"  All {len(results)} items processed using queue.join()\n")


async def worker_with_join(name, queue, results):
    """Worker that uses task_done() without sentinel values."""
    while True:
        job = await queue.get()
        process_time = random.uniform(0.1, 0.5)
        await asyncio.sleep(process_time)
        results.append(f"{job} -> {name}")
        print(f"  [{name}] Processed: {job}")
        queue.task_done()


# ── Main ─────────────────────────────────────────────────────────────

async def main():
    await run_pipeline()
    await run_with_join()


if __name__ == "__main__":
    asyncio.run(main())
