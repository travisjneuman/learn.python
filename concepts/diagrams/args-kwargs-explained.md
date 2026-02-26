# Diagrams: *args and **kwargs Explained

[Back to concept](../args-kwargs-explained.md)

---

## Argument Passing Flow

Python matches arguments to parameters by position first, then by name.

```mermaid
flowchart TD
    CALL["greet('Alice', 'Bob', greeting='Hi')"]

    subgraph MATCHING ["Python matches arguments"]
        POS["Positional args<br/>'Alice' and 'Bob'"]
        KW["Keyword arg<br/>greeting='Hi'"]
    end

    subgraph FUNC ["def greet(*args, greeting='Hello')"]
        ARGS["args = ('Alice', 'Bob')"]
        KWARG["greeting = 'Hi'"]
    end

    CALL --> MATCHING
    POS --> ARGS
    KW --> KWARG

    style POS fill:#4a9eff,stroke:#2670c2,color:#fff
    style KW fill:#ff922b,stroke:#e8590c,color:#fff
    style ARGS fill:#4a9eff,stroke:#2670c2,color:#fff
    style KWARG fill:#ff922b,stroke:#e8590c,color:#fff
```

## *args: Collecting Extra Positional Arguments

`*args` gathers any number of positional arguments into a tuple.

```mermaid
flowchart LR
    subgraph CALL ["add(1, 2, 3, 4, 5)"]
        A1["1"]
        A2["2"]
        A3["3"]
        A4["4"]
        A5["5"]
    end

    PACK["* packs them<br/>into a tuple"]

    subgraph FUNC ["def add(*args)"]
        T["args = (1, 2, 3, 4, 5)"]
        LOOP["for num in args:<br/>    total += num"]
        RES["return 15"]
        T --> LOOP --> RES
    end

    A1 --> PACK
    A2 --> PACK
    A3 --> PACK
    A4 --> PACK
    A5 --> PACK
    PACK --> T

    style CALL fill:#4a9eff,stroke:#2670c2,color:#fff
    style PACK fill:#ffd43b,stroke:#f59f00,color:#000
    style FUNC fill:#51cf66,stroke:#27ae60,color:#fff
```

## **kwargs: Collecting Extra Keyword Arguments

`**kwargs` gathers any number of keyword arguments into a dictionary.

```mermaid
flowchart LR
    subgraph CALL ["build_profile(name='Alice', age=30, city='NYC')"]
        K1["name='Alice'"]
        K2["age=30"]
        K3["city='NYC'"]
    end

    PACK["** packs them<br/>into a dict"]

    subgraph FUNC ["def build_profile(**kwargs)"]
        D["kwargs = {<br/>  'name': 'Alice',<br/>  'age': 30,<br/>  'city': 'NYC'<br/>}"]
    end

    K1 --> PACK
    K2 --> PACK
    K3 --> PACK
    PACK --> D

    style CALL fill:#ff922b,stroke:#e8590c,color:#fff
    style PACK fill:#ffd43b,stroke:#f59f00,color:#000
    style FUNC fill:#51cf66,stroke:#27ae60,color:#fff
```

## Parameter Order Rule

When combining all parameter types, they must appear in this exact order.

```mermaid
flowchart LR
    P1["1. Regular params<br/>def f(a, b)"]
    P2["2. *args<br/>def f(a, b, *args)"]
    P3["3. Keyword-only<br/>def f(a, *args, flag=True)"]
    P4["4. **kwargs<br/>def f(a, *args, flag=True, **kwargs)"]

    P1 --> P2 --> P3 --> P4

    style P1 fill:#4a9eff,stroke:#2670c2,color:#fff
    style P2 fill:#51cf66,stroke:#27ae60,color:#fff
    style P3 fill:#ffd43b,stroke:#f59f00,color:#000
    style P4 fill:#ff922b,stroke:#e8590c,color:#fff
```
