# Testing Strategies — Part 1: Unit Testing and Integration Testing

[← Back to Overview](./testing-strategies.md) · [Part 2: Advanced Testing →](./testing-strategies-part2.md)

---

Testing is how you prove your code works — and keep it working as you make changes. A good test suite catches bugs before users do, gives you confidence to refactor, and serves as living documentation of how your code should behave.

## Why This Matters

Without tests, every change is a gamble. You fix one bug and introduce two more. With tests, you can change code boldly — if something breaks, a test will tell you immediately. Professional codebases have hundreds or thousands of tests that run automatically on every commit.

## The test pyramid

The test pyramid is a model for how many of each type of test you should have:

```
        /  E2E  \          Few — slow, expensive, brittle
       /----------\
      / Integration \      Some — test component interactions
     /----------------\
    /    Unit Tests     \  Many — fast, focused, isolated
   ----------------------
```

- **Unit tests** — test a single function or class in isolation. Fast, cheap, write lots of them.
- **Integration tests** — test how components work together (e.g., your code + database).
- **End-to-end (E2E) tests** — test the whole system from the user's perspective (e.g., browser tests).

Most of your tests should be unit tests. Integration and E2E tests are important but slower and harder to maintain.

## Unit tests with pytest

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# test_calculator.py
import pytest
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

```bash
# Run tests:
pytest

# Run with verbose output:
pytest -v

# Run a specific file:
pytest test_calculator.py

# Run a specific test:
pytest test_calculator.py::test_add
```

## Fixtures — shared setup

Fixtures provide reusable setup for tests:

```python
import pytest
import sqlite3

@pytest.fixture
def db():
    """Create an in-memory database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users (name) VALUES ('Alice')")
    conn.execute("INSERT INTO users (name) VALUES ('Bob')")
    conn.commit()
    yield conn    # Provide the connection to the test
    conn.close()   # Cleanup after the test

def test_count_users(db):
    cursor = db.execute("SELECT COUNT(*) FROM users")
    assert cursor.fetchone()[0] == 2

def test_find_user(db):
    cursor = db.execute("SELECT name FROM users WHERE name = ?", ("Alice",))
    assert cursor.fetchone()[0] == "Alice"
```

Each test gets a fresh database — tests do not affect each other.

## TDD — Test-Driven Development

Write the test first, then write the code to make it pass:

### The Red-Green-Refactor cycle

1. **Red** — Write a failing test for the feature you want
2. **Green** — Write the minimum code to make the test pass
3. **Refactor** — Clean up the code while keeping tests green

```python
# Step 1: RED — write the test (it fails because fizzbuzz does not exist)
def test_fizzbuzz_regular_number():
    assert fizzbuzz(1) == "1"

def test_fizzbuzz_three():
    assert fizzbuzz(3) == "Fizz"

def test_fizzbuzz_five():
    assert fizzbuzz(5) == "Buzz"

def test_fizzbuzz_fifteen():
    assert fizzbuzz(15) == "FizzBuzz"

# Step 2: GREEN — write the minimum code to pass
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

# Step 3: REFACTOR — the code is already clean, move on
```

## Testing best practices

**Test behavior, not implementation:**
```python
# BAD — tests the internal structure:
def test_user_dict():
    user = create_user("Alice")
    assert user._data["name"] == "Alice"

# GOOD — tests the behavior:
def test_user_name():
    user = create_user("Alice")
    assert user.name == "Alice"
```

**Each test should test one thing:**
```python
# BAD — tests too many things:
def test_everything():
    user = create_user("Alice")
    assert user.name == "Alice"
    assert user.is_active
    assert len(get_all_users()) == 1
    delete_user(user)
    assert len(get_all_users()) == 0

# GOOD — separate tests:
def test_create_user_sets_name():
    user = create_user("Alice")
    assert user.name == "Alice"

def test_new_user_is_active():
    user = create_user("Alice")
    assert user.is_active
```

**Tests should be independent:**
Tests must not depend on each other or on execution order. Each test should set up its own data and clean up after itself.

---

| [← Overview](./testing-strategies.md) | [Part 2: Advanced Testing →](./testing-strategies-part2.md) |
|:---|---:|
