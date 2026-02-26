# Testing Strategies — Part 2: Advanced Testing

[← Part 1: Unit Testing](./testing-strategies-part1.md) · [Back to Overview](./testing-strategies.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

This part covers mocking, parametrized tests, code coverage, and common testing mistakes — the tools and techniques that take your test suite from basic to professional.

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

---

| [← Part 1: Unit Testing](./testing-strategies-part1.md) | [Overview](./testing-strategies.md) |
|:---|---:|
