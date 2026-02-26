# Diagrams: Functions Explained

[Back to concept](../functions-explained.md)

---

## Function Call Sequence

When you call a function, Python jumps into it, does work, then comes back with a result.

```mermaid
sequenceDiagram
    participant Caller as Your Code
    participant Func as Function

    Caller->>Func: Call: greet("Alice")
    Note over Func: name = "Alice"
    Note over Func: Run the function body
    Note over Func: Build result: "Hello, Alice!"
    Func-->>Caller: Return: "Hello, Alice!"
    Note over Caller: Continue with the result
```

## Parameter Passing Flow

Arguments are values you send IN. The return value is what comes back OUT.

```mermaid
flowchart LR
    subgraph Caller
        A1["area = calculate(5, 3)"]
    end

    subgraph "Function: calculate(width, height)"
        B1["width = 5"]
        B2["height = 3"]
        B3["result = 5 * 3"]
        B4["return 15"]
        B1 --> B2 --> B3 --> B4
    end

    A1 -->|"arguments go IN<br/>5 and 3"| B1
    B4 -->|"return value<br/>comes OUT: 15"| A1

    style A1 fill:#4a9eff,stroke:#2670c2,color:#fff
    style B4 fill:#51cf66,stroke:#27ae60,color:#fff
```

## Call Stack: Nested Function Calls

When functions call other functions, Python stacks them up and unwinds when each one finishes.

```mermaid
flowchart TD
    subgraph "Step 1: main() runs"
        S1["main() calls greet()"]
    end

    subgraph "Step 2: greet() runs"
        S2["greet() calls format_name()"]
    end

    subgraph "Step 3: format_name() runs"
        S3["format_name() returns &quot;ALICE&quot;"]
    end

    subgraph "Step 4: Unwinding"
        S4["greet() gets &quot;ALICE&quot;, returns &quot;Hello, ALICE!&quot;"]
    end

    subgraph "Step 5: Done"
        S5["main() gets &quot;Hello, ALICE!&quot;"]
    end

    S1 --> S2 --> S3 --> S4 --> S5
```

## Scope Chain: Where Python Looks for Names

When you use a variable name, Python searches in this order (LEGB rule).

```mermaid
flowchart TD
    LOOKUP["Python sees a name<br/>like x"] --> L{"1. Local?<br/>Inside this function?"}
    L -->|Found| DONE(["Use that value"])
    L -->|Not found| E{"2. Enclosing?<br/>Inside an outer function?"}
    E -->|Found| DONE
    E -->|Not found| G{"3. Global?<br/>At the top level<br/>of the file?"}
    G -->|Found| DONE
    G -->|Not found| B{"4. Built-in?<br/>Python built-in names?<br/>(print, len, range)"}
    B -->|Found| DONE
    B -->|Not found| ERR["NameError!<br/>Python cannot find it"]

    style L fill:#4a9eff,stroke:#2670c2,color:#fff
    style E fill:#51cf66,stroke:#27ae60,color:#fff
    style G fill:#ffd43b,stroke:#f59f00,color:#000
    style B fill:#cc5de8,stroke:#9c36b5,color:#fff
    style ERR fill:#ff6b6b,stroke:#c0392b,color:#fff
```
