# Diagrams: What Is a Variable

[Back to concept](../what-is-a-variable.md)

---

## Variable as a Labeled Box

A variable is a **name** that points to a **value** stored in memory.

```mermaid
flowchart LR
    subgraph Your Code
        A["name = &quot;Alice&quot;"]
        B["age = 25"]
        C["height = 5.6"]
    end

    subgraph Memory
        D["&quot;Alice&quot;<br/>(str)"]
        E["25<br/>(int)"]
        F["5.6<br/>(float)"]
    end

    A -->|points to| D
    B -->|points to| E
    C -->|points to| F
```

## Assignment vs Reassignment

When you reassign a variable, the label moves to a **new** value. The old value is discarded if nothing else points to it.

```mermaid
flowchart TD
    subgraph Step 1: x = 10
        A1["x"] -->|points to| B1["10"]
    end

    subgraph Step 2: x = 20
        A2["x"] -.->|old| B2["10 (abandoned)"]
        A2 -->|now points to| C2["20"]
    end

    subgraph Step 3: y = x
        A3["x"] -->|points to| D3["20"]
        B3["y"] -->|also points to| D3
    end

    Step_1_x_10 --> Step_2_x_20 --> Step_3_y_x

    style B2 fill:#888,stroke:#666,color:#fff
```

## Type Conversion Flowchart

Python can convert between types, but not every conversion works.

```mermaid
flowchart TD
    STR["str<br/>&quot;42&quot;"]
    INT["int<br/>42"]
    FLOAT["float<br/>42.0"]
    BOOL["bool<br/>True"]

    STR -->|"int(&quot;42&quot;) = 42"| INT
    STR -->|"float(&quot;42&quot;) = 42.0"| FLOAT
    INT -->|"str(42) = &quot;42&quot;"| STR
    INT -->|"float(42) = 42.0"| FLOAT
    FLOAT -->|"int(42.9) = 42<br/>loses .9!"| INT
    FLOAT -->|"str(42.0) = &quot;42.0&quot;"| STR
    BOOL -->|"int(True) = 1"| INT
    INT -->|"bool(0) = False<br/>bool(5) = True"| BOOL

    style INT fill:#4a9eff,stroke:#2670c2,color:#fff
    style STR fill:#ff6b6b,stroke:#c0392b,color:#fff
    style FLOAT fill:#51cf66,stroke:#27ae60,color:#fff
    style BOOL fill:#ffd43b,stroke:#f59f00,color:#000
```

## When Does Python Create a New Value?

```mermaid
flowchart TD
    START["You write: x = x + 1"] --> Q1{"Is the type<br/>immutable?"}
    Q1 -->|"Yes (int, str, float,<br/>bool, tuple)"| NEW["Python creates a<br/>NEW value in memory<br/>and re-points x"]
    Q1 -->|"No (list, dict, set)"| MODIFY["Python changes the<br/>EXISTING value<br/>in place"]
    NEW --> NOTE1["Old value is abandoned<br/>if nothing else uses it"]
    MODIFY --> NOTE2["All variables pointing<br/>to it see the change"]
```
