# Diagrams: Async Explained

[Back to concept](../async-explained.md)

---

## Event Loop State Machine

The event loop is the engine that runs async code. It cycles through coroutines, running whichever one is ready and pausing those that are waiting.

```mermaid
stateDiagram-v2
    [*] --> Created: async def called
    Created --> Scheduled: asyncio.create_task()
    Scheduled --> Running: Event loop picks it up
    Running --> Suspended: Hits await (I/O, sleep)
    Suspended --> Scheduled: Awaited operation completes
    Running --> Done: Returns a value
    Running --> Error: Raises exception
    Done --> [*]
    Error --> [*]

    note right of Running: Only ONE coroutine<br/>runs at a time
    note right of Suspended: Event loop runs<br/>other tasks while waiting
```

## Async/Await Execution Flow

This shows how three concurrent tasks share a single thread. The event loop switches between them whenever one hits an `await`.

```mermaid
sequenceDiagram
    participant Loop as Event Loop
    participant A as Task A (fetch user)
    participant B as Task B (fetch posts)
    participant C as Task C (fetch comments)

    Note over Loop: asyncio.gather(A, B, C)

    Loop->>A: Start Task A
    Note over A: Send HTTP request
    A-->>Loop: await response (I/O wait)

    Loop->>B: Start Task B
    Note over B: Send HTTP request
    B-->>Loop: await response (I/O wait)

    Loop->>C: Start Task C
    Note over C: Send HTTP request
    C-->>Loop: await response (I/O wait)

    Note over Loop: All 3 requests in flight<br/>Loop waits for first completion

    Note over B: Response arrives first!
    Loop->>B: Resume Task B
    Note over B: Parse JSON, return data
    B-->>Loop: Task B done

    Note over A: Response arrives
    Loop->>A: Resume Task A
    Note over A: Parse JSON, return data
    A-->>Loop: Task A done

    Note over C: Response arrives
    Loop->>C: Resume Task C
    Note over C: Parse JSON, return data
    C-->>Loop: Task C done

    Note over Loop: All tasks complete<br/>Total time ≈ slowest task
```

## Concurrent vs Parallel Execution

Concurrent means tasks take turns on one thread. Parallel means tasks literally run at the same time on multiple cores.

```mermaid
flowchart TD
    subgraph SYNC ["Synchronous (blocking)"]
        direction LR
        S1["Task A<br/>1 sec"] --> S2["Task B<br/>1 sec"] --> S3["Task C<br/>1 sec"]
    end
    SYNC_TIME["Total: 3 seconds"]

    subgraph CONCURRENT ["Concurrent (asyncio)"]
        direction LR
        CA["Task A starts"] -.->|"await"| CB["Task B starts"] -.->|"await"| CC["Task C starts"]
        CC -.->|"all complete"| CDONE["All done"]
    end
    CONC_TIME["Total: ~1 second<br/>One thread, interleaved"]

    subgraph PARALLEL ["Parallel (multiprocessing)"]
        direction LR
        PA["Core 1: Task A"]
        PB["Core 2: Task B"]
        PC["Core 3: Task C"]
    end
    PAR_TIME["Total: ~1 second<br/>Multiple cores, truly simultaneous"]

    SYNC --- SYNC_TIME
    CONCURRENT --- CONC_TIME
    PARALLEL --- PAR_TIME

    style SYNC fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CONCURRENT fill:#51cf66,stroke:#27ae60,color:#fff
    style PARALLEL fill:#4a9eff,stroke:#2670c2,color:#fff
    style SYNC_TIME fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style CONC_TIME fill:#51cf66,stroke:#27ae60,color:#fff
    style PAR_TIME fill:#4a9eff,stroke:#2670c2,color:#fff
```

## When to Use Which Approach

A decision tree for choosing between sync, async, and multiprocessing.

```mermaid
flowchart TD
    START["What kind of work?"] --> Q1{"Waiting on I/O?<br/>(network, files, DB)"}

    Q1 -->|"Yes"| Q2{"Multiple I/O<br/>operations?"}
    Q1 -->|"No"| Q3{"CPU-heavy?<br/>(math, image processing)"}

    Q2 -->|"Yes"| ASYNC["Use asyncio<br/>async/await + gather()"]
    Q2 -->|"No, just one"| SYNC_OK["Plain sync is fine<br/>requests.get()"]

    Q3 -->|"Yes"| Q4{"Need shared memory?"}
    Q3 -->|"No"| SYNC["Plain sync is fine<br/>No concurrency needed"]

    Q4 -->|"Yes"| THREAD["Use threading<br/>with locks"]
    Q4 -->|"No"| MULTI["Use multiprocessing<br/>One process per core"]

    style ASYNC fill:#51cf66,stroke:#27ae60,color:#fff
    style SYNC_OK fill:#4a9eff,stroke:#2670c2,color:#fff
    style SYNC fill:#4a9eff,stroke:#2670c2,color:#fff
    style THREAD fill:#ffd43b,stroke:#f59f00,color:#000
    style MULTI fill:#cc5de8,stroke:#9c36b5,color:#fff
```
