# Parametrize — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently. The goal is to write utility functions and test them using `@pytest.mark.parametrize`. If you can write a parametrized test with three test cases that all pass, you are on the right track.

## Thinking Process

Testing a function with one input proves it works for that input. Testing it with ten inputs proves it handles variety. But writing ten separate test functions that all look nearly identical is tedious and hard to maintain. `@pytest.mark.parametrize` solves this by letting you define one test function and feed it a table of inputs and expected outputs. Pytest runs the function once per row, reporting each as a separate test.

This project has two sides: writing the utility functions and writing the parametrized tests. The functions are deliberately simple — email validation, temperature conversion, palindrome checking, and number clamping. The complexity is not in the logic but in the edge cases: empty strings, boundary values, invalid types. Parametrize is the tool that lets you check all of those edge cases without drowning in duplicate code.

Think of parametrize like a spreadsheet. Each row is a test case. The columns are the inputs and the expected output. You write the test logic once, and pytest fills in the values row by row.

## Step 1: Write the Utility Functions

**What to do:** Implement four small utility functions in `project.py`: `validate_email`, `celsius_to_fahrenheit`, `is_palindrome`, and `clamp`.

**Why:** Each function is a textbook "pure function" — same input, same output, no side effects. This makes them perfect for parametrized testing. Start with the simplest implementation that handles the main cases, then refine edge cases based on your test results.

```python
import re

def validate_email(address):
    if not isinstance(address, str) or not address:
        return False
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, address))

def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32
```

The email validation uses a regex pattern that checks for: something before `@`, something after `@` that contains a dot, and no spaces. It is not perfect (real email validation is surprisingly complex), but it catches the most common mistakes.

**Predict:** Does `validate_email(42)` crash or return False? What about `validate_email(None)`?

## Step 2: Write Your First Parametrized Test

**What to do:** Create `tests/test_utils.py` and write a parametrized test for `validate_email`.

**Why:** The `@pytest.mark.parametrize` decorator takes two arguments: a string naming the parameters (comma-separated), and a list of tuples containing the values. Each tuple becomes one test run. The `ids` parameter gives each test case a human-readable name.

```python
import pytest
from project import validate_email

@pytest.mark.parametrize(
    "email, expected",
    [
        ("user@example.com", True),
        ("name.tag@domain.org", True),
        ("missing-at-sign", False),
        ("", False),
        ("@no-local-part.com", False),
    ],
    ids=[
        "valid-standard",
        "valid-dotted",
        "invalid-missing-at",
        "invalid-empty",
        "invalid-no-local",
    ],
)
def test_validate_email(email, expected):
    assert validate_email(email) == expected
```

Three things to notice:

- **The string `"email, expected"`** names the parameters. These must match the function's parameter names.
- **Each tuple** has exactly two values (matching the two parameter names).
- **`ids`** is a list of strings, one per test case. Without it, pytest shows the raw values, which can be hard to read.

**Predict:** If you run `pytest -v`, what will the test names look like? What happens without the `ids` parameter?

## Step 3: Test Known Conversion Pairs

**What to do:** Write a parametrized test for `celsius_to_fahrenheit` using well-known temperature reference points.

**Why:** Temperature conversion has famous reference points (water freezes at 0C/32F, boils at 100C/212F, and -40 is the same in both scales). These are ideal test cases because you know the exact expected output. Using `pytest.approx()` handles floating-point rounding errors.

```python
@pytest.mark.parametrize(
    "celsius, expected_fahrenheit",
    [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),
        (37, 98.6),
    ],
    ids=["freezing", "boiling", "crossover", "body-temp"],
)
def test_celsius_to_fahrenheit(celsius, expected_fahrenheit):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected_fahrenheit)
```

**`pytest.approx()`** compares floating-point numbers with a small tolerance. Without it, `98.60000000000001 == 98.6` would fail due to floating-point arithmetic quirks.

**Predict:** Why not use `==` directly for the comparison? Try `0.1 + 0.2 == 0.3` in a Python shell to see why.

## Step 4: Test Edge Cases with Boundary Values

**What to do:** Write a parametrized test for `clamp` that covers all three behaviors (in range, below min, above max) plus boundary values.

**Why:** `clamp` has distinct behaviors depending on where the value falls relative to the range. Parametrize lets you lay out all the cases in a clean table. Boundary values (exactly at min, exactly at max, min equals max) are where bugs hide.

```python
@pytest.mark.parametrize(
    "value, min_val, max_val, expected",
    [
        (5, 0, 10, 5),        # In range
        (-3, 0, 10, 0),       # Below minimum
        (15, 0, 10, 10),      # Above maximum
        (0, 0, 10, 0),        # At minimum boundary
        (10, 0, 10, 10),      # At maximum boundary
        (5, 5, 5, 5),         # Single-point range
    ],
    ids=[
        "in-range",
        "below-minimum",
        "above-maximum",
        "at-minimum",
        "at-maximum",
        "single-point-range",
    ],
)
def test_clamp(value, min_val, max_val, expected):
    assert clamp(value, min_val, max_val) == expected
```

**Predict:** What should `clamp(5, 10, 0)` do when min is greater than max? Should it silently swap them, or raise an error?

## Step 5: Test for Expected Exceptions

**What to do:** Write a separate test that verifies `clamp` raises `ValueError` for invalid input.

**Why:** Sometimes the correct behavior is to raise an error. `pytest.raises()` as a context manager catches the exception and verifies both the type and the message. This is a separate test (not parametrized) because you are testing for an exception, not a return value.

```python
def test_clamp_raises_on_invalid_range():
    with pytest.raises(ValueError, match="must not be greater than"):
        clamp(5, 10, 0)
```

The `match` parameter checks that the error message contains the expected text. This prevents false positives — you are not just catching any `ValueError`, you are catching the specific one your function raises.

**Predict:** What happens if `clamp` does not raise an error? Does `pytest.raises` pass or fail?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Parameter count mismatch | Tuple has wrong number of values | Count your parameters: `"a, b"` needs 2-element tuples |
| `ids` list length mismatch | Different number of ids and test cases | One id per test case, or omit `ids` entirely |
| Floating-point comparison fails | `98.6 != 98.60000000000001` | Use `pytest.approx()` for float comparisons |
| Test names unreadable in output | No `ids` parameter | Always add `ids` for parametrized tests |

## Testing Your Solution

```bash
pytest tests/test_utils.py -v
```

Expected output:
```text
tests/test_utils.py::test_validate_email[valid-user@example.com] PASSED
tests/test_utils.py::test_validate_email[invalid-missing-at] PASSED
...
tests/test_utils.py::test_celsius_to_fahrenheit[freezing] PASSED
tests/test_utils.py::test_celsius_to_fahrenheit[boiling] PASSED
...
tests/test_utils.py::test_clamp[in-range] PASSED
tests/test_utils.py::test_clamp[below-minimum] PASSED
...
```

Each parametrized case appears as a separate test with its readable id. All should pass.

## What You Learned

- **`@pytest.mark.parametrize`** runs one test function with many different inputs, eliminating duplicate test code while increasing coverage.
- **The `ids` parameter** gives each test case a human-readable name — critical for understanding which case failed when debugging.
- **`pytest.approx()`** handles floating-point comparison by allowing a small tolerance, preventing false failures from rounding errors.
- **`pytest.raises()`** tests that code raises the correct exception — sometimes the right behavior is to fail loudly, not to return garbage.
