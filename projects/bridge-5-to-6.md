# Bridge Exercise: Level 5 to Level 6

You have completed Level 5. You can build multi-file ETL pipelines, handle configuration, and write resilient code. Level 6 introduces **SQL databases**, **APIs**, and **decorators**. This bridge exercise gives you a gentle first encounter with decorators and a simple API call.

---

## What Changes in Level 6

In Level 5, you read and wrote files (CSV, JSON, text). In Level 6, you will:
- Store and query data in **SQL databases** (SQLite)
- Call **web APIs** to fetch data over the internet
- Use **decorators** to add behavior to functions without modifying them

---

## Part 1: Decorators

A decorator is a function that wraps another function. The `@` syntax is shorthand.

### Exercise: A timing decorator

Create `bridge_5_to_6.py`:

```python
import time
import functools
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def timed(func):
    """Decorator that logs how long a function takes to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s took %.4f seconds", func.__name__, elapsed)
        return result
    return wrapper


@timed
def slow_sum(numbers):
    """Sum a list of numbers with a fake delay."""
    time.sleep(0.1)  # simulate slow work
    return sum(numbers)
```

**What is happening:**
- `timed` takes a function as input and returns a new function (`wrapper`) that does the same thing plus logs the time.
- `@timed` above `slow_sum` is the same as writing `slow_sum = timed(slow_sum)`.
- `@functools.wraps(func)` preserves the original function's name and docstring.

Try it:

```python
from bridge_5_to_6 import slow_sum
result = slow_sum([1, 2, 3, 4, 5])
# Output: slow_sum took 0.1003 seconds
print(result)  # 15
```

### Challenge

Write a `@retry(max_attempts=3)` decorator that retries a function up to 3 times if it raises an exception. This pattern is used constantly in production code that talks to unreliable services.

---

## Part 2: Your First API Call

APIs let your program talk to other programs over the internet. You send a request, you get a response.

### Exercise: Fetch data from a public API

Add to `bridge_5_to_6.py`:

```python
import json
from urllib.request import urlopen
from urllib.error import URLError


def fetch_random_fact():
    """Fetch a random fact from a public API.

    Returns a dict with 'fact' and 'length' keys.
    Returns None if the request fails.
    """
    url = "https://catfact.ninja/fact"
    try:
        with urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {"fact": data["fact"], "length": data["length"]}
    except (URLError, KeyError, json.JSONDecodeError) as e:
        logger.error("Failed to fetch fact: %s", e)
        return None
```

**What is happening:**
- `urlopen(url)` sends an HTTP GET request (like visiting a URL in your browser).
- The response comes back as bytes, so we decode it to a string, then parse the JSON.
- `try/except` handles network errors, missing keys, and bad JSON.

Try it (requires internet):

```python
from bridge_5_to_6 import fetch_random_fact
fact = fetch_random_fact()
if fact:
    print(f"Did you know? {fact['fact']}")
```

---

## Part 3: Test What You Can

Create `test_bridge_5_to_6.py`:

```python
import time
from bridge_5_to_6 import slow_sum, timed


def test_slow_sum():
    result = slow_sum([1, 2, 3])
    assert result == 6


def test_timed_preserves_function_name():
    assert slow_sum.__name__ == "slow_sum"


def test_timed_preserves_docstring():
    assert "Sum a list" in slow_sum.__doc__


def test_custom_decorated_function():
    @timed
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add.__name__ == "add"
```

**Note:** We do not test `fetch_random_fact()` here because it requires a network connection. In Level 6, you will learn to use **mocking** to test code that talks to external services without actually calling them.

Run: `pytest test_bridge_5_to_6.py -v`

---

## You Are Ready

If you can write and apply a decorator, make an HTTP request and parse JSON, and handle errors from external services, you are ready for Level 6.

---

| [Level 5 Projects](level-5/README.md) | [Home](../README.md) | [Level 6 Projects](level-6/README.md) |
|:---|:---:|---:|
