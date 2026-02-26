# Diagrams: Comprehensions Explained

[Back to concept](../comprehensions-explained.md)

---

## List Comprehension Data Flow

A list comprehension takes an iterable, optionally filters it, transforms each item, and collects results.

```mermaid
flowchart LR
    INPUT["Input iterable<br/>[1, 2, 3, 4, 5, 6]"]
    FILTER["Filter (optional)<br/>if x % 2 == 0"]
    TRANSFORM["Transform<br/>x ** 2"]
    OUTPUT["Output list<br/>[4, 16, 36]"]

    INPUT --> FILTER --> TRANSFORM --> OUTPUT

    style INPUT fill:#4a9eff,stroke:#2670c2,color:#fff
    style FILTER fill:#ffd43b,stroke:#f59f00,color:#000
    style TRANSFORM fill:#cc5de8,stroke:#9c36b5,color:#fff
    style OUTPUT fill:#51cf66,stroke:#27ae60,color:#fff
```

## Comprehension vs Loop: Side by Side

Every comprehension can be rewritten as a for loop. The comprehension is just more concise.

```mermaid
flowchart TD
    subgraph LOOP ["For Loop (4 lines)"]
        L1["squares = []"]
        L2["for x in range(5):"]
        L3["    squares.append(x ** 2)"]
        L4["# squares = [0, 1, 4, 9, 16]"]
        L1 --> L2 --> L3 --> L4
    end

    subgraph COMP ["Comprehension (1 line)"]
        C1["squares = [x ** 2 for x in range(5)]"]
        C2["# squares = [0, 1, 4, 9, 16]"]
        C1 --> C2
    end

    LOOP ---|"Same result,<br/>less code"| COMP

    style LOOP fill:#ffd43b,stroke:#f59f00,color:#000
    style COMP fill:#51cf66,stroke:#27ae60,color:#fff
```

## Anatomy of a Comprehension

Breaking down the parts of `[expression for item in iterable if condition]`.

```mermaid
flowchart TD
    FULL["[x * 2  for x in range(10)  if x > 3]"]
    FULL --> PART_OUT["x * 2<br/>OUTPUT expression<br/>What goes into the result"]
    FULL --> PART_FOR["for x in range(10)<br/>ITERATION<br/>What we loop over"]
    FULL --> PART_IF["if x > 3<br/>FILTER (optional)<br/>Which items to keep"]

    PART_FOR -->|"x = 0, 1, 2, ... 9"| PART_IF
    PART_IF -->|"Keeps: 4, 5, 6, 7, 8, 9"| PART_OUT
    PART_OUT -->|"Result"| RESULT["[8, 10, 12, 14, 16, 18]"]

    style PART_OUT fill:#51cf66,stroke:#27ae60,color:#fff
    style PART_FOR fill:#4a9eff,stroke:#2670c2,color:#fff
    style PART_IF fill:#ffd43b,stroke:#f59f00,color:#000
    style RESULT fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## List vs Dict vs Set Comprehension

The brackets you use determine what type of collection you get.

```mermaid
flowchart TD
    subgraph LIST_COMP ["List Comprehension [ ]"]
        LC["[x**2 for x in range(4)]"]
        LR2["Result: [0, 1, 4, 9]"]
        LC --> LR2
    end

    subgraph DICT_COMP ["Dict Comprehension { : }"]
        DC["{x: x**2 for x in range(4)}"]
        DR["Result: {0: 0, 1: 1, 2: 4, 3: 9}"]
        DC --> DR
    end

    subgraph SET_COMP ["Set Comprehension { }"]
        SC["{x % 3 for x in range(6)}"]
        SR["Result: {0, 1, 2}"]
        SC --> SR
    end

    style LIST_COMP fill:#4a9eff,stroke:#2670c2,color:#fff
    style DICT_COMP fill:#ff922b,stroke:#e8590c,color:#fff
    style SET_COMP fill:#cc5de8,stroke:#9c36b5,color:#fff
```
