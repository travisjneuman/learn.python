# Diagrams: Type Hints Explained

[Back to concept](../type-hints-explained.md)

---

## Type Annotation Hierarchy

Python's type system forms a hierarchy from simple types to complex generic types.

```mermaid
flowchart TD
    subgraph BASIC ["Basic Types"]
        INT["int"]
        STR["str"]
        FLOAT["float"]
        BOOL["bool"]
    end

    subgraph CONTAINER ["Container Types"]
        LIST["list[int]"]
        DICT["dict[str, int]"]
        SET["set[str]"]
        TUPLE["tuple[int, str]"]
    end

    subgraph SPECIAL ["Special Types"]
        OPT["Optional[str]<br/>= str | None"]
        UNION["Union[int, str]<br/>= int | str"]
        ANY2["Any<br/>(escape hatch)"]
    end

    subgraph ADVANCED ["Advanced Types"]
        CALLABLE["Callable[[int], str]"]
        TYPEVAR["TypeVar('T')"]
        GENERIC["Generic[T]"]
    end

    BASIC --> CONTAINER
    CONTAINER --> SPECIAL
    SPECIAL --> ADVANCED

    style BASIC fill:#4a9eff,stroke:#2670c2,color:#fff
    style CONTAINER fill:#51cf66,stroke:#27ae60,color:#fff
    style SPECIAL fill:#ffd43b,stroke:#f59f00,color:#000
    style ADVANCED fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## How Type Checking Works

Type hints do not run at runtime. A separate tool (mypy, pyright) reads them and reports errors.

```mermaid
flowchart LR
    subgraph WRITE ["You write"]
        CODE["def greet(name: str) -> str:<br/>    return 'Hello, ' + name"]
    end

    subgraph TOOLS ["Tools that read type hints"]
        MYPY["mypy<br/>Static checker"]
        PYRIGHT["pyright<br/>Static checker"]
        IDE["VS Code / PyCharm<br/>Autocomplete + warnings"]
    end

    subgraph RUNTIME ["At runtime"]
        PYTHON["Python ignores<br/>type hints completely"]
        RUNS["Code runs normally<br/>no speed cost"]
        PYTHON --> RUNS
    end

    WRITE --> TOOLS
    WRITE --> RUNTIME

    style WRITE fill:#4a9eff,stroke:#2670c2,color:#fff
    style TOOLS fill:#51cf66,stroke:#27ae60,color:#fff
    style RUNTIME fill:#ffd43b,stroke:#f59f00,color:#000
```

## Optional and Union: Handling Multiple Types

`Optional[X]` means "X or None". `Union[X, Y]` means "X or Y". Modern Python uses `|` syntax.

```mermaid
flowchart TD
    subgraph OPT ["Optional[str]"]
        O1["Value can be str"]
        O2["Value can be None"]
        O3["Same as: str | None"]
        O1 ~~~ O2 ~~~ O3
    end

    subgraph UNI ["Union[int, str]"]
        U1["Value can be int"]
        U2["Value can be str"]
        U3["Same as: int | str"]
        U1 ~~~ U2 ~~~ U3
    end

    subgraph EXAMPLE ["Practical example"]
        E1["def find_user(id: int) -> Optional[User]:"]
        E2["    if found: return User(...)"]
        E3["    if not found: return None"]
        E1 ~~~ E2 ~~~ E3
    end

    OPT --> EXAMPLE
    UNI --> EXAMPLE

    style OPT fill:#4a9eff,stroke:#2670c2,color:#fff
    style UNI fill:#ff922b,stroke:#e8590c,color:#fff
    style EXAMPLE fill:#51cf66,stroke:#27ae60,color:#fff
```

## Generics: Making Reusable Typed Code

Generics let you write functions and classes that work with any type while keeping type safety.

```mermaid
flowchart TD
    subgraph WITHOUT ["Without generics"]
        W1["def first(items: list) -> Any"]
        W2["Type checker loses<br/>track of the type"]
        W1 --> W2
    end

    subgraph WITH ["With generics"]
        G1["T = TypeVar('T')"]
        G2["def first(items: list[T]) -> T"]
        G3["first([1, 2, 3]) → int"]
        G4["first(['a', 'b']) → str"]
        G1 --> G2
        G2 --> G3
        G2 --> G4
    end

    style WITHOUT fill:#ff6b6b,stroke:#c0392b,color:#fff
    style WITH fill:#51cf66,stroke:#27ae60,color:#fff
```
