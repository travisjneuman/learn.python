# functools and itertools — Part 1: functools

[← Back to Overview](./functools-and-itertools.md) · [Part 2: itertools →](./functools-and-itertools-part2.md)

---

The `functools` module gives you tools to transform and optimize functions. These solve problems you will hit repeatedly: caching expensive computations, pre-filling arguments, folding sequences, and preserving metadata in decorators.

## Why This Matters

These tools save you from reinventing the wheel and produce code that is both faster and more readable. `lru_cache` alone can turn a function that takes minutes into one that returns instantly.

## `functools.lru_cache` — automatic memoization

Caches the results of a function so repeated calls with the same arguments are instant:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)    # Returns instantly — without cache, this would take forever
```

`maxsize=128` keeps the 128 most recent results. Use `maxsize=None` for unlimited cache (careful with memory). Arguments must be hashable (no lists or dicts).

## `functools.partial` — pre-fill function arguments

Creates a new function with some arguments already filled in:

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

square(5)    # 25
cube(3)      # 27
```

Useful for callbacks and configuration:

```python
import json
from functools import partial

# Create a pre-configured JSON dumper:
pretty_json = partial(json.dumps, indent=2, sort_keys=True)
print(pretty_json({"b": 2, "a": 1}))
# {
#   "a": 1,
#   "b": 2
# }
```

## `functools.reduce` — fold a sequence into one value

Applies a function cumulatively to items in a sequence, reducing it to a single value:

```python
from functools import reduce

# Sum (just to illustrate — use sum() in practice):
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, numbers)    # 15

# Find the longest string:
words = ["cat", "elephant", "dog"]
longest = reduce(lambda a, b: a if len(a) >= len(b) else b, words)
# "elephant"

# Flatten nested lists:
nested = [[1, 2], [3, 4], [5]]
flat = reduce(lambda a, b: a + b, nested)    # [1, 2, 3, 4, 5]
```

For simple operations, prefer built-in functions (`sum`, `max`, `min`). Use `reduce` when no built-in fits.

## `functools.wraps` — preserve function metadata in decorators

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)    # Copies name, docstring, etc. from the original
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Say hello."""
    return f"Hello, {name}"

print(greet.__name__)    # "greet" (without @wraps, this would be "wrapper")
print(greet.__doc__)     # "Say hello."
```

See [Decorators Explained](./decorators-explained.md) for more on this pattern.

## Common Mistakes (functools)

**Caching functions with unhashable arguments:**
```python
@lru_cache
def process(data):    # TypeError if data is a list!
    return sum(data)

# Fix: convert to tuple
process(tuple([1, 2, 3]))
```

---

| [← Overview](./functools-and-itertools.md) | [Part 2: itertools →](./functools-and-itertools-part2.md) |
|:---|---:|
