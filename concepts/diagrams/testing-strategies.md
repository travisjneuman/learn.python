# Diagrams: Testing Strategies

[Back to concept](../testing-strategies.md)

---

## The Testing Pyramid

More unit tests at the base, fewer integration tests in the middle, and a small number of end-to-end tests at the top. The pyramid reflects speed, cost, and quantity.

```mermaid
flowchart TD
    subgraph PYRAMID ["Testing Pyramid"]
        E2E["End-to-End Tests<br/>Few, slow, expensive<br/>Test full user workflows"]
        INT["Integration Tests<br/>Moderate count<br/>Test components working together"]
        UNIT["Unit Tests<br/>Many, fast, cheap<br/>Test individual functions"]
    end

    E2E --- INT --- UNIT

    subgraph TRAITS ["Characteristics"]
        direction LR
        SPEED["Speed: Unit > Integration > E2E"]
        COUNT["Count: Unit > Integration > E2E"]
        SCOPE["Scope: E2E > Integration > Unit"]
        COST["Cost: E2E > Integration > Unit"]
    end

    style E2E fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style INT fill:#ffd43b,stroke:#f59f00,color:#000
    style UNIT fill:#51cf66,stroke:#27ae60,color:#fff
    style TRAITS fill:#4a9eff,stroke:#2670c2,color:#fff
```

## Test Types Compared

What each test type covers and how they differ in scope.

```mermaid
flowchart LR
    subgraph UNIT_TEST ["Unit Test"]
        UF["Test one function<br/>in isolation"]
        UF --> UM["Mock all<br/>dependencies"]
        UM --> UR["Assert return value<br/>or side effect"]
    end

    subgraph INT_TEST ["Integration Test"]
        IF["Test multiple<br/>components together"]
        IF --> ID["Real database<br/>or file system"]
        ID --> IR["Assert correct<br/>interaction"]
    end

    subgraph E2E_TEST ["End-to-End Test"]
        EF["Test full workflow<br/>as a user would"]
        EF --> ES["Real server,<br/>real browser"]
        ES --> ER["Assert user-visible<br/>outcome"]
    end

    subgraph EXAMPLE ["Example: User signup"]
        EX_U["Unit: hash_password()<br/>returns correct hash"]
        EX_I["Integration: create_user()<br/>writes to real database"]
        EX_E["E2E: Fill signup form,<br/>click submit, see dashboard"]
    end

    style UNIT_TEST fill:#51cf66,stroke:#27ae60,color:#fff
    style INT_TEST fill:#ffd43b,stroke:#f59f00,color:#000
    style E2E_TEST fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style EXAMPLE fill:#4a9eff,stroke:#2670c2,color:#fff
```

## TDD Cycle: Red-Green-Refactor

Test-Driven Development follows a strict cycle: write a failing test first, make it pass with minimal code, then clean up.

```mermaid
flowchart TD
    RED["RED<br/>Write a failing test<br/>for the next feature"] --> GREEN["GREEN<br/>Write the simplest code<br/>that makes the test pass"]
    GREEN --> REFACTOR["REFACTOR<br/>Clean up the code<br/>without changing behavior"]
    REFACTOR --> CHECK{"All tests<br/>still pass?"}
    CHECK -->|"Yes"| NEXT{"More features<br/>to build?"}
    CHECK -->|"No"| FIX["Fix the code<br/>until tests pass"]
    FIX --> CHECK
    NEXT -->|"Yes"| RED
    NEXT -->|"No"| DONE["Done!"]

    style RED fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style GREEN fill:#51cf66,stroke:#27ae60,color:#fff
    style REFACTOR fill:#4a9eff,stroke:#2670c2,color:#fff
    style CHECK fill:#ffd43b,stroke:#f59f00,color:#000
    style DONE fill:#cc5de8,stroke:#9c36b5,color:#fff
```

## Pytest Fixture Lifecycle

Fixtures provide test dependencies. They set up before the test and tear down after, with different scopes controlling how often.

```mermaid
sequenceDiagram
    participant Pytest as pytest runner
    participant Fix as @pytest.fixture
    participant Test as test_function

    Note over Pytest: Collect tests<br/>Resolve fixture dependencies

    Pytest->>Fix: Call fixture function
    Note over Fix: SETUP phase<br/>Create database connection<br/>Seed test data

    Fix-->>Pytest: yield db_connection

    Pytest->>Test: test_create_user(db_connection)
    Note over Test: Run assertions<br/>assert user.name == "Alice"
    Test-->>Pytest: Test passed or failed

    Pytest->>Fix: Resume after yield
    Note over Fix: TEARDOWN phase<br/>Delete test data<br/>Close connection

    Note over Pytest: Fixture scopes control reuse:<br/>function = once per test (default)<br/>class = once per test class<br/>module = once per file<br/>session = once per entire run
```
