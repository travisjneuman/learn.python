# Diagrams: Context Managers Explained

[Back to concept](../context-managers-explained.md)

---

## The with Statement Lifecycle

A context manager guarantees that setup and cleanup happen, even if an error occurs inside the block.

```mermaid
sequenceDiagram
    participant Code as Your Code
    participant CM as Context Manager
    participant Resource as Resource (file, db, etc.)

    Code->>CM: with open("data.txt") as f:
    CM->>Resource: __enter__(): Open the file
    Resource-->>CM: Return file object
    CM-->>Code: f = file object

    Note over Code: Your code runs here<br/>data = f.read()

    alt No error
        Code->>CM: Block finished normally
        CM->>Resource: __exit__(): Close the file
        Note over Resource: File is safely closed
    else Error raised
        Code->>CM: Exception occurred!
        CM->>Resource: __exit__(): Close the file ANYWAY
        Note over Resource: File is safely closed
        CM-->>Code: Re-raise the exception
    end
```

## Resource Management: With vs Without

Using `with` prevents resource leaks. Without it, you must remember to clean up manually.

```mermaid
flowchart TD
    subgraph RISKY ["Without context manager"]
        R1["f = open('data.txt')"]
        R2["data = f.read()"]
        R3["process(data)"]
        R4{"Did an error<br/>occur?"}
        R4 -->|Yes| R5["File stays OPEN!<br/>Resource leak"]
        R4 -->|No| R6["f.close()"]
        R1 --> R2 --> R3 --> R4
    end

    subgraph SAFE ["With context manager"]
        S1["with open('data.txt') as f:"]
        S2["    data = f.read()"]
        S3["    process(data)"]
        S4["File ALWAYS closes<br/>even if error occurs"]
        S1 --> S2 --> S3 --> S4
    end

    style RISKY fill:#ff6b6b,stroke:#c0392b,color:#fff
    style SAFE fill:#51cf66,stroke:#27ae60,color:#fff
    style R5 fill:#ff6b6b,stroke:#c0392b,color:#fff
```

## Enter and Exit: Behind the Scenes

Every context manager is an object with `__enter__` and `__exit__` methods.

```mermaid
flowchart TD
    WITH["with MyManager() as value:"]
    ENTER["__enter__(self)<br/>Set up the resource<br/>Return something useful"]
    BODY["Your code block runs<br/>using 'value'"]
    EXIT["__exit__(self, exc_type, exc_val, tb)<br/>Clean up the resource<br/>Always runs"]
    DONE["Execution continues<br/>after the with block"]

    WITH --> ENTER --> BODY --> EXIT --> DONE

    style WITH fill:#4a9eff,stroke:#2670c2,color:#fff
    style ENTER fill:#51cf66,stroke:#27ae60,color:#fff
    style BODY fill:#ffd43b,stroke:#f59f00,color:#000
    style EXIT fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Common Context Managers

Python provides context managers for many resources that need cleanup.

```mermaid
flowchart LR
    subgraph FILES ["Files"]
        F1["with open('f.txt') as f:"]
        F2["Auto-closes file"]
        F1 --> F2
    end

    subgraph DB ["Database"]
        D1["with connect(db) as conn:"]
        D2["Auto-commits or rollback"]
        D1 --> D2
    end

    subgraph LOCK ["Threading"]
        L1["with Lock():"]
        L2["Auto-releases lock"]
        L1 --> L2
    end

    subgraph TEMP ["Temp Files"]
        T1["with TemporaryFile() as tmp:"]
        T2["Auto-deletes file"]
        T1 --> T2
    end

    style FILES fill:#4a9eff,stroke:#2670c2,color:#fff
    style DB fill:#51cf66,stroke:#27ae60,color:#fff
    style LOCK fill:#ff922b,stroke:#e8590c,color:#fff
    style TEMP fill:#cc5de8,stroke:#9c36b5,color:#fff
```
