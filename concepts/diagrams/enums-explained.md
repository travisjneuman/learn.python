# Diagrams: Enums Explained

[Back to concept](../enums-explained.md)

---

## Enum Value Mapping

An Enum maps meaningful names to fixed values. Each member has a `.name` and a `.value`.

```mermaid
flowchart LR
    subgraph ENUM ["class Color(Enum)"]
        R["RED = 1"]
        G["GREEN = 2"]
        B["BLUE = 3"]
    end

    subgraph ACCESS ["Accessing members"]
        BY_NAME["Color.RED"]
        BY_VAL["Color(1)"]
        NAME_ATTR["Color.RED.name → 'RED'"]
        VAL_ATTR["Color.RED.value → 1"]
    end

    R --> BY_NAME
    R --> BY_VAL
    BY_NAME --> NAME_ATTR
    BY_NAME --> VAL_ATTR

    style ENUM fill:#4a9eff,stroke:#2670c2,color:#fff
    style ACCESS fill:#51cf66,stroke:#27ae60,color:#fff
```

## Enum vs Magic Constants

Enums replace scattered "magic" strings and numbers with a single source of truth.

```mermaid
flowchart TD
    subgraph BAD ["Without Enum: magic values scattered"]
        B1["status = 'active'"]
        B2["if user.status == 'actve':  # typo!"]
        B3["No autocomplete help"]
        B4["No error if you misspell"]
        B1 ~~~ B2 ~~~ B3 ~~~ B4
    end

    subgraph GOOD ["With Enum: safe and clear"]
        G1["status = Status.ACTIVE"]
        G2["if user.status == Status.ACTIVE:"]
        G3["Autocomplete works"]
        G4["Typo = immediate error"]
        G1 ~~~ G2 ~~~ G3 ~~~ G4
    end

    style BAD fill:#ff6b6b,stroke:#c0392b,color:#fff
    style GOOD fill:#51cf66,stroke:#27ae60,color:#fff
```

## Choosing the Right Enum Type

Python provides several Enum base classes for different use cases.

```mermaid
flowchart TD
    START{"What kind of<br/>values do you need?"}
    START -->|"Named labels<br/>(no math)"| ENUM["Enum<br/>class Color(Enum):<br/>    RED = 1"]
    START -->|"Integer values<br/>(comparisons, math)"| INT_ENUM["IntEnum<br/>class Priority(IntEnum):<br/>    LOW = 1"]
    START -->|"String values<br/>(JSON, APIs)"| STR_ENUM["StrEnum<br/>class Status(StrEnum):<br/>    ACTIVE = 'active'"]
    START -->|"Combinable flags<br/>(permissions)"| FLAG["Flag<br/>class Perm(Flag):<br/>    READ = 1<br/>    WRITE = 2"]

    style ENUM fill:#4a9eff,stroke:#2670c2,color:#fff
    style INT_ENUM fill:#51cf66,stroke:#27ae60,color:#fff
    style STR_ENUM fill:#ff922b,stroke:#e8590c,color:#fff
    style FLAG fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Flag Enum Composition

Flag enums let you combine members with bitwise OR to represent sets of permissions.

```mermaid
flowchart TD
    subgraph FLAGS ["class Permission(Flag)"]
        R["READ = 1   (binary: 001)"]
        W["WRITE = 2  (binary: 010)"]
        X["EXECUTE = 4 (binary: 100)"]
    end

    subgraph COMBINE ["Combining with |"]
        RW["READ | WRITE = 3  (011)"]
        RWX["READ | WRITE | EXECUTE = 7  (111)"]
    end

    subgraph CHECK ["Checking with in"]
        C1["READ in RW  → True"]
        C2["EXECUTE in RW  → False"]
        C3["WRITE in RWX  → True"]
    end

    R --> RW
    W --> RW
    R --> RWX
    W --> RWX
    X --> RWX
    RW --> C1
    RW --> C2
    RWX --> C3

    style FLAGS fill:#4a9eff,stroke:#2670c2,color:#fff
    style COMBINE fill:#ffd43b,stroke:#f59f00,color:#000
    style CHECK fill:#51cf66,stroke:#27ae60,color:#fff
```
