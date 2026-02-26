# Diagrams: Dataclasses Explained

[Back to concept](../dataclasses-explained.md)

---

## What @dataclass Auto-Generates

The `@dataclass` decorator reads your field annotations and writes boilerplate methods for you.

```mermaid
flowchart TD
    subgraph YOU_WRITE ["What you write"]
        W1["@dataclass<br/>class Point:<br/>    x: float<br/>    y: float"]
    end

    subgraph AUTO ["What Python generates automatically"]
        A1["__init__(self, x, y)<br/>self.x = x; self.y = y"]
        A2["__repr__(self)<br/>→ Point(x=1.0, y=2.0)"]
        A3["__eq__(self, other)<br/>→ compares x and y"]
    end

    YOU_WRITE -->|"@dataclass reads<br/>the annotations"| A1
    YOU_WRITE --> A2
    YOU_WRITE --> A3

    style YOU_WRITE fill:#4a9eff,stroke:#2670c2,color:#fff
    style AUTO fill:#51cf66,stroke:#27ae60,color:#fff
```

## Field Definition Flow

Each field can have a type, a default, or a `field()` with extra configuration.

```mermaid
flowchart TD
    FIELD["Dataclass field"] --> SIMPLE{"Has a<br/>default value?"}
    SIMPLE -->|No| REQUIRED["x: float<br/>REQUIRED — must be passed"]
    SIMPLE -->|Yes| DEFAULT_TYPE{"Simple value<br/>or mutable?"}
    DEFAULT_TYPE -->|"Simple (int, str, etc.)"| SIMPLE_DEFAULT["x: float = 0.0<br/>Use directly"]
    DEFAULT_TYPE -->|"Mutable (list, dict)"| FACTORY["tags: list = field(<br/>    default_factory=list<br/>)<br/>Each object gets its own list"]

    style REQUIRED fill:#ff922b,stroke:#e8590c,color:#fff
    style SIMPLE_DEFAULT fill:#51cf66,stroke:#27ae60,color:#fff
    style FACTORY fill:#4a9eff,stroke:#2670c2,color:#fff
```

## Frozen vs Mutable Dataclasses

A frozen dataclass prevents modification after creation, making it safe to use as a dict key or in sets.

```mermaid
flowchart TD
    subgraph MUTABLE ["@dataclass (default: mutable)"]
        M1["p = Point(1.0, 2.0)"]
        M2["p.x = 5.0  ← OK"]
        M3["Can modify after creation"]
        M4["Cannot use as dict key"]
        M1 --> M2 --> M3 --> M4
    end

    subgraph FROZEN ["@dataclass(frozen=True)"]
        F1["p = Point(1.0, 2.0)"]
        F2["p.x = 5.0  ← FrozenInstanceError!"]
        F3["Immutable after creation"]
        F4["Safe as dict key or in sets"]
        F1 --> F2 --> F3 --> F4
    end

    style MUTABLE fill:#ffd43b,stroke:#f59f00,color:#000
    style FROZEN fill:#4a9eff,stroke:#2670c2,color:#fff
```

## Regular Class vs Dataclass

A dataclass eliminates the repetitive boilerplate of a regular class for data-holding objects.

```mermaid
flowchart LR
    subgraph REGULAR ["Regular class (~15 lines)"]
        R1["class Point:"]
        R2["    def __init__(self, x, y):"]
        R3["        self.x = x"]
        R4["        self.y = y"]
        R5["    def __repr__(self): ..."]
        R6["    def __eq__(self, other): ..."]
        R1 ~~~ R2 ~~~ R3 ~~~ R4 ~~~ R5 ~~~ R6
    end

    subgraph DATACLASS ["Dataclass (~4 lines)"]
        D1["@dataclass"]
        D2["class Point:"]
        D3["    x: float"]
        D4["    y: float"]
        D1 ~~~ D2 ~~~ D3 ~~~ D4
    end

    REGULAR ---|"Same result,<br/>less code"| DATACLASS

    style REGULAR fill:#ffd43b,stroke:#f59f00,color:#000
    style DATACLASS fill:#51cf66,stroke:#27ae60,color:#fff
```
