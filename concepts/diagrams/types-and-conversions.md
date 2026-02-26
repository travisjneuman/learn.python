# Diagrams: Types and Conversions

[Back to concept](../types-and-conversions.md)

---

## Python Type Hierarchy

Everything in Python is an `object`. Here are the most common types.

```mermaid
flowchart TD
    OBJ["object<br/>(the root of everything)"]
    OBJ --> INT["int<br/>whole numbers<br/>42, -7, 0"]
    OBJ --> FLOAT["float<br/>decimal numbers<br/>3.14, -0.5"]
    OBJ --> BOOL["bool<br/>True or False"]
    OBJ --> STR["str<br/>text<br/>&quot;hello&quot;"]
    OBJ --> LIST["list<br/>ordered, changeable<br/>[1, 2, 3]"]
    OBJ --> TUPLE["tuple<br/>ordered, frozen<br/>(1, 2, 3)"]
    OBJ --> DICT["dict<br/>key-value pairs<br/>{&quot;a&quot;: 1}"]
    OBJ --> SET["set<br/>unique items<br/>{1, 2, 3}"]
    OBJ --> NONE["NoneType<br/>nothing<br/>None"]

    BOOL -.->|"bool is a<br/>subtype of int"| INT

    style OBJ fill:#888,stroke:#666,color:#fff
    style INT fill:#4a9eff,stroke:#2670c2,color:#fff
    style FLOAT fill:#51cf66,stroke:#27ae60,color:#fff
    style BOOL fill:#ffd43b,stroke:#f59f00,color:#000
    style STR fill:#ff6b6b,stroke:#c0392b,color:#fff
    style LIST fill:#cc5de8,stroke:#9c36b5,color:#fff
    style TUPLE fill:#20c997,stroke:#0ca678,color:#fff
    style DICT fill:#ff922b,stroke:#e8590c,color:#fff
    style SET fill:#66d9e8,stroke:#22b8cf,color:#000
    style NONE fill:#adb5bd,stroke:#868e96,color:#000
```

## Type Conversion Paths

Some conversions are safe (no data lost). Others are lossy (information disappears).

```mermaid
flowchart LR
    INT["int"]
    FLOAT["float"]
    STR["str"]
    BOOL["bool"]

    INT -->|"Safe<br/>42 -> 42.0"| FLOAT
    FLOAT -->|"Lossy!<br/>42.7 -> 42<br/>decimal lost"| INT
    INT -->|"Safe<br/>42 -> &quot;42&quot;"| STR
    STR -->|"Only if valid<br/>&quot;42&quot; -> 42<br/>&quot;hello&quot; -> ERROR"| INT
    FLOAT -->|"Safe<br/>3.14 -> &quot;3.14&quot;"| STR
    STR -->|"Only if valid<br/>&quot;3.14&quot; -> 3.14"| FLOAT
    BOOL -->|"Safe<br/>True -> 1"| INT
    INT -->|"Safe<br/>0 -> False<br/>anything else -> True"| BOOL

    linkStyle 1 stroke:#ff0000
    linkStyle 3 stroke:#ff8800
    linkStyle 5 stroke:#ff8800

    style INT fill:#4a9eff,stroke:#2670c2,color:#fff
    style FLOAT fill:#51cf66,stroke:#27ae60,color:#fff
    style STR fill:#ff6b6b,stroke:#c0392b,color:#fff
    style BOOL fill:#ffd43b,stroke:#f59f00,color:#000
```

## Truthy and Falsy Decision Tree

Python treats some values as `False` when used in `if` statements.

```mermaid
flowchart TD
    START{"What is<br/>the value?"}
    START -->|"None"| FALSY
    START -->|"0, 0.0, 0j"| FALSY
    START -->|"Empty string: &quot;&quot;"| FALSY
    START -->|"Empty list: []"| FALSY
    START -->|"Empty dict: {}"| FALSY
    START -->|"Empty set: set()"| FALSY
    START -->|"Empty tuple: ()"| FALSY
    START -->|"False"| FALSY
    START -->|"Anything else"| TRUTHY

    FALSY["FALSY<br/>Treated as False"]
    TRUTHY["TRUTHY<br/>Treated as True"]

    TRUTHY --> EX1["42, -1, 3.14<br/>&quot;hello&quot;, &quot; &quot;<br/>[0], {&quot;a&quot;: 1}"]

    style FALSY fill:#ff6b6b,stroke:#c0392b,color:#fff
    style TRUTHY fill:#51cf66,stroke:#27ae60,color:#fff
```
