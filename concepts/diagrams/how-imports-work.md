# Diagrams: How Imports Work

[Back to concept](../how-imports-work.md)

---

## Import Resolution Path

When you write `import something`, Python follows a specific search order to find it.

```mermaid
flowchart TD
    START["import something"] --> CACHE{"1. Already in<br/>sys.modules cache?"}
    CACHE -->|Yes| USE_CACHED(["Use cached module"])
    CACHE -->|No| BUILTIN{"2. Is it a<br/>built-in module?<br/>(sys, os, math)"}
    BUILTIN -->|Yes| LOAD_BUILTIN(["Load built-in"])
    BUILTIN -->|No| SYSPATH{"3. Search sys.path<br/>directories in order"}
    SYSPATH --> DIR1["Current directory<br/>(script location)"]
    DIR1 -->|Not found| DIR2["PYTHONPATH<br/>environment variable"]
    DIR2 -->|Not found| DIR3["Standard library<br/>directories"]
    DIR3 -->|Not found| DIR4["Site-packages<br/>(pip-installed)"]
    DIR4 -->|Not found| ERR["ModuleNotFoundError!"]
    DIR1 -->|Found| LOAD(["Load & cache module"])
    DIR2 -->|Found| LOAD
    DIR3 -->|Found| LOAD
    DIR4 -->|Found| LOAD

    style CACHE fill:#4a9eff,stroke:#2670c2,color:#fff
    style BUILTIN fill:#51cf66,stroke:#27ae60,color:#fff
    style SYSPATH fill:#ffd43b,stroke:#f59f00,color:#000
    style ERR fill:#ff6b6b,stroke:#c0392b,color:#fff
    style LOAD fill:#51cf66,stroke:#27ae60,color:#fff
    style USE_CACHED fill:#51cf66,stroke:#27ae60,color:#fff
```

## Package vs Module

A module is a single `.py` file. A package is a directory with an `__init__.py`.

```mermaid
flowchart TD
    subgraph MODULE ["Module (single file)"]
        M1["math_helpers.py"]
        M2["import math_helpers"]
        M3["math_helpers.add(1, 2)"]
        M1 ~~~ M2 ~~~ M3
    end

    subgraph PACKAGE ["Package (directory)"]
        P0["mypackage/"]
        P1["  __init__.py"]
        P2["  utils.py"]
        P3["  models.py"]
        P0 ~~~ P1 ~~~ P2 ~~~ P3
    end

    subgraph USAGE ["How you import them"]
        U1["from mypackage import utils"]
        U2["from mypackage.models import User"]
        U1 ~~~ U2
    end

    PACKAGE --> USAGE

    style MODULE fill:#4a9eff,stroke:#2670c2,color:#fff
    style PACKAGE fill:#ff922b,stroke:#e8590c,color:#fff
    style USAGE fill:#51cf66,stroke:#27ae60,color:#fff
```

## Import Styles Compared

Different import styles give you different names to use in your code.

```mermaid
flowchart LR
    subgraph STYLE1 ["import math"]
        A1["Imports the whole module"]
        A2["Use as: math.sqrt(16)"]
        A1 ~~~ A2
    end

    subgraph STYLE2 ["from math import sqrt"]
        B1["Imports just sqrt"]
        B2["Use as: sqrt(16)"]
        B1 ~~~ B2
    end

    subgraph STYLE3 ["from math import sqrt as s"]
        C1["Imports sqrt with alias"]
        C2["Use as: s(16)"]
        C1 ~~~ C2
    end

    subgraph STYLE4 ["from math import *"]
        D1["Imports everything"]
        D2["Risky: name collisions!"]
        D1 ~~~ D2
    end

    style STYLE1 fill:#51cf66,stroke:#27ae60,color:#fff
    style STYLE2 fill:#4a9eff,stroke:#2670c2,color:#fff
    style STYLE3 fill:#ffd43b,stroke:#f59f00,color:#000
    style STYLE4 fill:#ff6b6b,stroke:#c0392b,color:#fff
```
