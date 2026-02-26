# Async Event Loop Deep Dive — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams go deeper into how Python's asyncio event loop schedules coroutines, manages task lifecycles, and coordinates concurrent operations with `gather()` and `wait()`.

## Event Loop Internals

The event loop maintains queues of ready and waiting tasks. Each iteration ("tick") of the loop runs all ready callbacks, checks for completed I/O, and moves newly-ready tasks into the run queue.

```mermaid
flowchart TD
    TICK["Event Loop Tick"] --> READY{"Ready queue<br/>has tasks?"}
    READY -->|"Yes"| RUN["Run next callback<br/>(one at a time)"]
    RUN --> CHECK_MORE{"More ready<br/>callbacks?"}
    CHECK_MORE -->|"Yes"| RUN
    CHECK_MORE -->|"No"| POLL["Poll for I/O events<br/>(select/epoll/kqueue)"]
    READY -->|"No"| POLL

    POLL --> IO_DONE{"I/O completed?"}
    IO_DONE -->|"Yes"| WAKE["Move completed tasks<br/>to ready queue"]
    IO_DONE -->|"No"| TIMERS["Check timers<br/>(sleep, timeout)"]
    WAKE --> TIMERS

    TIMERS --> EXPIRED{"Timers expired?"}
    EXPIRED -->|"Yes"| SCHEDULE["Schedule timer<br/>callbacks as ready"]
    EXPIRED -->|"No"| TICK
    SCHEDULE --> TICK

    style TICK fill:#cc5de8,stroke:#9c36b5,color:#fff
    style RUN fill:#51cf66,stroke:#27ae60,color:#fff
    style POLL fill:#4a9eff,stroke:#2670c2,color:#fff
    style WAKE fill:#ffd43b,stroke:#f59f00,color:#000
```

**Key points:**
- The loop runs one callback at a time (single-threaded concurrency, not parallelism)
- I/O polling is where the loop waits for network responses, file reads, etc.
- Timers handle `asyncio.sleep()` and timeout deadlines
- A "tick" is one full cycle: run ready tasks, poll I/O, check timers, repeat

## Task Lifecycle States

A coroutine goes through several states from creation to completion. Understanding these states helps you debug hanging tasks and cancellation behavior.

```mermaid
stateDiagram-v2
    [*] --> Coroutine: async def my_func()
    Coroutine --> Task: asyncio.create_task(my_func())
    Task --> Pending: Scheduled on event loop
    Pending --> Running: Loop picks this task
    Running --> Awaiting: Hits await expression
    Awaiting --> Pending: Awaited result ready
    Running --> Done: Return value
    Running --> Cancelled: task.cancel() called
    Awaiting --> Cancelled: task.cancel() called
    Pending --> Cancelled: task.cancel() called
    Done --> [*]: result = task.result()
    Cancelled --> [*]: raises CancelledError

    note right of Coroutine: Calling async def<br/>returns a coroutine object<br/>(does NOT start running)
    note right of Task: create_task() wraps<br/>the coroutine and<br/>schedules it
    note left of Cancelled: CancelledError is raised<br/>inside the coroutine at<br/>the current await point
```

**Key points:**
- Calling an `async def` function returns a coroutine object but does NOT start executing it
- `create_task()` wraps the coroutine in a Task and schedules it on the loop
- Cancellation raises `CancelledError` at the coroutine's current `await` point
- A task is "done" when it returns, raises an exception, or is cancelled

## gather() vs wait() vs TaskGroup

Three ways to run multiple coroutines concurrently. Each has different error handling and completion semantics.

```mermaid
flowchart TD
    subgraph GATHER ["asyncio.gather(*coros)"]
        G_START["Start all tasks<br/>concurrently"]
        G_WAIT["Wait for ALL<br/>to complete"]
        G_RESULT["Returns list of results<br/>in original order"]
        G_ERR["If one fails:<br/>cancels others (return_exceptions=False)<br/>or returns exception in list (=True)"]
        G_START --> G_WAIT --> G_RESULT
        G_WAIT --> G_ERR
    end

    subgraph WAIT ["asyncio.wait(tasks, ...)"]
        W_START["Start all tasks<br/>concurrently"]
        W_RETURN["Returns two sets:<br/>(done, pending)"]
        W_MODE["Control when it returns:<br/>FIRST_COMPLETED<br/>FIRST_EXCEPTION<br/>ALL_COMPLETED"]
        W_START --> W_RETURN
        W_RETURN --> W_MODE
    end

    subgraph TASKGROUP ["asyncio.TaskGroup() — Python 3.11+"]
        TG_START["async with TaskGroup() as tg:<br/>    tg.create_task(coro1)<br/>    tg.create_task(coro2)"]
        TG_WAIT["Waits at end of<br/>async with block"]
        TG_ERR["If one fails:<br/>cancels all others,<br/>raises ExceptionGroup"]
        TG_START --> TG_WAIT --> TG_ERR
    end

    style GATHER fill:#51cf66,stroke:#27ae60,color:#fff
    style WAIT fill:#4a9eff,stroke:#2670c2,color:#fff
    style TASKGROUP fill:#cc5de8,stroke:#9c36b5,color:#fff
```

**Key points:**
- `gather()` is simplest: run tasks, get results in order. Best for "do all of these and give me all results"
- `wait()` gives you fine-grained control: react to the first completion or first failure
- `TaskGroup` (Python 3.11+) is the modern approach with structured concurrency and clean cancellation
- `gather(return_exceptions=True)` collects exceptions as values instead of propagating them

## Sequence: Timeout and Cancellation

What happens when a task exceeds a deadline. This shows the mechanics of `asyncio.wait_for()` and how cancellation propagates.

```mermaid
sequenceDiagram
    participant Main as Main Coroutine
    participant Loop as Event Loop
    participant Task as Slow Task
    participant Timer as Timeout Timer

    Main->>Loop: asyncio.wait_for(slow_task(), timeout=2.0)
    Loop->>Task: Start slow_task()
    Loop->>Timer: Set timer for 2.0 seconds

    Note over Task: Working...<br/>await aiohttp.get(slow_url)
    Note over Loop: Loop continues<br/>running other tasks

    Timer-->>Loop: 2.0 seconds elapsed!
    Loop->>Task: task.cancel()
    Note over Task: CancelledError raised<br/>at current await

    alt Task has try/finally
        Note over Task: finally: cleanup()
        Task-->>Loop: Cleanup complete
    else No cleanup
        Task-->>Loop: CancelledError propagates
    end

    Loop-->>Main: raises asyncio.TimeoutError
    Note over Main: Handle timeout gracefully
```

**Key points:**
- `wait_for()` wraps a coroutine with a deadline and cancels it if the deadline passes
- Cancellation gives the task a chance to clean up in `try/finally` blocks
- The caller receives `TimeoutError`, not `CancelledError`
- Always use timeouts for network operations to prevent tasks from hanging forever

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|
