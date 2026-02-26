# Testing Strategies

Testing is how you prove your code works — and keep it working as you make changes. A good test suite catches bugs before users do, gives you confidence to refactor, and serves as living documentation of how your code should behave.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/testing-strategies-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

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

## Parametrized tests — test many inputs at once

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (1.5, 2.5, 4.0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

One test function, five test cases. Each runs independently — if one fails, the others still run.

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

## Test doubles — stub, mock, fake, spy

When your code depends on external systems (APIs, databases, file systems), you replace them with test doubles:

| Type | What it does | Example |
|------|-------------|---------|
| **Stub** | Returns pre-programmed responses | Fake API that always returns `{"status": "ok"}` |
| **Mock** | Records calls and verifies expectations | Check that `send_email()` was called with the right arguments |
| **Fake** | Working implementation with shortcuts | In-memory database instead of PostgreSQL |
| **Spy** | Wraps real object, records calls | Real email sender that also logs what was sent |

### Using `unittest.mock`

```python
from unittest.mock import patch, MagicMock

# The code we are testing:
def get_weather(city):
    import requests
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()["temperature"]

# The test — mock the API call:
def test_get_weather():
    with patch("requests.get") as mock_get:
        # Configure the mock to return fake data:
        mock_get.return_value.json.return_value = {"temperature": 72}

        result = get_weather("Portland")

        assert result == 72
        mock_get.assert_called_once_with("https://api.weather.com/Portland")
```

### Using `monkeypatch` (pytest's approach)

```python
def test_get_weather(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"temperature": 72}

    def fake_get(url):
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    result = get_weather("Portland")
    assert result == 72
```

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

## Code coverage with `pytest-cov`

Coverage measures what percentage of your code is executed by tests:

```bash
# Install:
pip install pytest-cov

# Run with coverage report:
pytest --cov=myproject

# Show which lines are NOT covered:
pytest --cov=myproject --cov-report=term-missing

# Generate HTML report:
pytest --cov=myproject --cov-report=html
```

Example output:
```
----------- coverage: ... -----------
Name              Stmts   Miss  Cover   Missing
------------------------------------------------
calculator.py        10      2    80%   15-16
test_calculator.py   20      0   100%
------------------------------------------------
TOTAL                30      2    93%
```

Aim for 80%+ coverage on critical code. 100% coverage does not mean zero bugs — it means every line ran, not that every scenario was tested.

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

## Common Mistakes

**Testing the framework instead of your code:**
```python
# WRONG — this tests that Python's dict works, not your code:
def test_dict():
    d = {"a": 1}
    assert d["a"] == 1
```

**Hard-coding values that match test data:**
```python
# WRONG — hard-coded to pass the test, not solve the problem:
def fizzbuzz(n):
    if n == 3: return "Fizz"    # Only works for 3, not 6, 9, 12...

# RIGHT — actual logic:
def fizzbuzz(n):
    if n % 3 == 0: return "Fizz"
```

**Not testing edge cases:**
Always test: empty input, zero, negative numbers, None, very large values, and boundary conditions.

## Practice

- [Level 0 projects](../projects/level-0/) — all projects include test suites
- [Module 08 Advanced Testing](../projects/modules/08-testing-advanced/) — parametrize, mocking, hypothesis
- [Elite Track / 05 Performance Profiler Workbench](../projects/elite-track/05-performance-profiler-workbench/README.md)

**Quick check:** [Take the quiz](quizzes/testing-strategies-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock (Python docs)](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)

---

| [← Prev](collections-deep-dive.md) | [Home](../README.md) | [Next →](debugging-methodology.md) |
|:---|:---:|---:|
