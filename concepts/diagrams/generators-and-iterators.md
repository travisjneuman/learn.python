# Diagrams: Generators and Iterators

[Back to concept](../generators-and-iterators.md)

---

## The Iterator Protocol

Every `for` loop in Python uses the iterator protocol under the hood. The object must implement `__iter__()` and `__next__()`.

```mermaid
sequenceDiagram
    participant For as for loop
    participant Obj as Iterable Object
    participant Iter as Iterator

    For->>Obj: iter(obj)
    Note over Obj: Calls __iter__()
    Obj-->>For: Returns iterator

    loop Each iteration
        For->>Iter: next(iterator)
        Note over Iter: Calls __next__()
        Iter-->>For: Next value
        Note over For: Bind to loop variable<br/>Execute loop body
    end

    For->>Iter: next(iterator)
    Note over Iter: No more items
    Iter-->>For: Raises StopIteration
    Note over For: Loop ends
```

## Generator Yield and Resume Flow

A generator function pauses at each `yield` and resumes exactly where it left off when `next()` is called again.

```mermaid
sequenceDiagram
    participant Caller as Calling Code
    participant Gen as Generator Function

    Caller->>Gen: gen = count_up(3)
    Note over Gen: Function body does NOT run yet<br/>Returns generator object

    Caller->>Gen: next(gen)
    Note over Gen: Runs until first yield<br/>i = 1
    Gen-->>Caller: yields 1
    Note over Gen: PAUSED — all local<br/>variables preserved

    Caller->>Gen: next(gen)
    Note over Gen: Resumes after yield<br/>i = 2
    Gen-->>Caller: yields 2
    Note over Gen: PAUSED again

    Caller->>Gen: next(gen)
    Note over Gen: Resumes after yield<br/>i = 3
    Gen-->>Caller: yields 3
    Note over Gen: PAUSED again

    Caller->>Gen: next(gen)
    Note over Gen: Loop ends, function returns
    Gen-->>Caller: Raises StopIteration
```

## Lazy vs Eager Evaluation

Eager evaluation builds the entire result in memory. Lazy evaluation produces one item at a time, using almost no memory regardless of size.

```mermaid
flowchart TD
    subgraph EAGER ["Eager: List"]
        E1["numbers = [x*2 for x in range(1_000_000)]"]
        E2["Builds ALL 1 million values<br/>immediately in memory"]
        E3["Memory: ~8 MB"]
        E1 --> E2 --> E3
    end

    subgraph LAZY ["Lazy: Generator"]
        L1["numbers = (x*2 for x in range(1_000_000))"]
        L2["Builds NOTHING yet<br/>Just stores the recipe"]
        L3["Memory: ~100 bytes"]
        L1 --> L2 --> L3
    end

    subgraph USE ["When you iterate"]
        U1["for n in numbers:"]
        U2["Eager: reads from<br/>pre-built list in RAM"]
        U3["Lazy: computes each value<br/>on demand, discards after use"]
        U1 --> U2
        U1 --> U3
    end

    EAGER --> USE
    LAZY --> USE

    style EAGER fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style LAZY fill:#51cf66,stroke:#27ae60,color:#fff
    style USE fill:#4a9eff,stroke:#2670c2,color:#fff
```

## Generator Pipeline

Generators can be chained together into processing pipelines. Each stage pulls one item at a time through the chain.

```mermaid
flowchart LR
    SOURCE["read_lines(file)<br/>yield line"] --> FILTER["non_empty(lines)<br/>yield if line.strip()"]
    FILTER --> PARSE["parse_csv(lines)<br/>yield row dict"]
    PARSE --> TRANSFORM["add_totals(rows)<br/>yield row + total"]
    TRANSFORM --> SINK["write_report(rows)<br/>consume and write"]

    subgraph MEMORY ["Memory at any moment"]
        M1["Only ONE line<br/>in memory at a time"]
        M2["File can be<br/>100 GB — no problem"]
    end

    style SOURCE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style FILTER fill:#ff922b,stroke:#e8590c,color:#fff
    style PARSE fill:#4a9eff,stroke:#2670c2,color:#fff
    style TRANSFORM fill:#51cf66,stroke:#27ae60,color:#fff
    style SINK fill:#ffd43b,stroke:#f59f00,color:#000
    style MEMORY fill:#51cf66,stroke:#27ae60,color:#fff
```
