# Diagrams: Decorators Explained

[Back to concept](../decorators-explained.md)

---

## How a Decorator Wraps a Function

A decorator takes your function, wraps it with extra behavior, and gives you the wrapped version back.

```mermaid
sequenceDiagram
    participant Python as Python Interpreter
    participant Dec as @timer decorator
    participant Orig as Original greet()
    participant Wrap as Wrapped greet()

    Note over Python: Sees @timer above greet()
    Python->>Dec: timer(greet)
    Note over Dec: Creates wrapper function<br/>that calls greet() inside
    Dec-->>Python: Returns wrapper
    Note over Python: greet now points<br/>to the wrapper
    Python->>Wrap: greet("Alice")
    Note over Wrap: Before: start = time()
    Wrap->>Orig: Call original greet("Alice")
    Note over Orig: "Hello, Alice!"
    Orig-->>Wrap: Return result
    Note over Wrap: After: print elapsed time
    Wrap-->>Python: Return "Hello, Alice!"
```

## Before and After: What @decorator Does

The `@decorator` syntax is shorthand for reassigning the function name.

```mermaid
flowchart LR
    subgraph WITHOUT ["Without @ syntax"]
        W1["def greet(name):<br/>    return f'Hello, {name}'"]
        W2["greet = timer(greet)"]
        W1 --> W2
    end

    subgraph WITH ["With @ syntax (same thing!)"]
        D1["@timer<br/>def greet(name):<br/>    return f'Hello, {name}'"]
    end

    WITHOUT ---|"These are<br/>identical"| WITH

    style WITHOUT fill:#ffd43b,stroke:#f59f00,color:#000
    style WITH fill:#51cf66,stroke:#27ae60,color:#fff
```

## Stacking Multiple Decorators

Decorators stack from bottom to top. The closest decorator to the function runs first.

```mermaid
flowchart TD
    subgraph CODE ["Your Code"]
        C1["@bold<br/>@italic<br/>def greet(name):<br/>    return f'Hello, {name}'"]
    end

    subgraph ORDER ["Execution Order"]
        S1["1. Python defines greet()"]
        S2["2. @italic wraps greet<br/>greet = italic(greet)"]
        S3["3. @bold wraps the result<br/>greet = bold(italic(greet))"]
        S1 --> S2 --> S3
    end

    subgraph CALL ["When you call greet('Alice')"]
        R1["bold wrapper runs first"]
        R2["italic wrapper runs next"]
        R3["original greet runs last"]
        R4["Result bubbles back up"]
        R1 --> R2 --> R3 --> R4
    end

    CODE --> ORDER --> CALL

    style CODE fill:#4a9eff,stroke:#2670c2,color:#fff
    style ORDER fill:#ff922b,stroke:#e8590c,color:#fff
    style CALL fill:#51cf66,stroke:#27ae60,color:#fff
```

## Common Decorator Pattern

The structure every decorator follows: take a function, define a wrapper, return the wrapper.

```mermaid
flowchart TD
    A["def my_decorator(func):"] --> B["    def wrapper(*args, **kwargs):"]
    B --> C["        # Code BEFORE the function"]
    C --> D["        result = func(*args, **kwargs)"]
    D --> E["        # Code AFTER the function"]
    E --> F["        return result"]
    F --> G["    return wrapper"]

    style A fill:#cc5de8,stroke:#9c36b5,color:#fff
    style B fill:#4a9eff,stroke:#2670c2,color:#fff
    style C fill:#ffd43b,stroke:#f59f00,color:#000
    style D fill:#51cf66,stroke:#27ae60,color:#fff
    style E fill:#ffd43b,stroke:#f59f00,color:#000
    style F fill:#51cf66,stroke:#27ae60,color:#fff
    style G fill:#cc5de8,stroke:#9c36b5,color:#fff
```
