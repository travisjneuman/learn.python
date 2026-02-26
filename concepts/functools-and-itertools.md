# functools and itertools

These two standard library modules are Python's power tools for working with functions and sequences. `functools` gives you tools to transform and optimize functions. `itertools` gives you building blocks for efficient iteration. Together they let you write elegant, memory-efficient code.

## Why This Matters

These modules solve problems you will hit repeatedly: caching expensive computations, chaining sequences, grouping data, generating combinations, and more. Knowing them saves you from reinventing the wheel and produces code that is both faster and more readable.

## functools — function tools

### `functools.lru_cache` — automatic memoization

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

### `functools.partial` — pre-fill function arguments

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

### `functools.reduce` — fold a sequence into one value

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

### `functools.wraps` — preserve function metadata in decorators

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

## itertools — iteration building blocks

### `itertools.chain` — combine multiple iterables

```python
from itertools import chain

a = [1, 2, 3]
b = [4, 5]
c = [6, 7, 8, 9]

list(chain(a, b, c))    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Flatten a list of lists:
nested = [[1, 2], [3], [4, 5, 6]]
list(chain.from_iterable(nested))    # [1, 2, 3, 4, 5, 6]
```

### `itertools.groupby` — group consecutive items

Groups items that have the same key. **Important:** the data must be sorted by the key first.

```python
from itertools import groupby

# Group words by their first letter:
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
# Already sorted by first letter!

for letter, group in groupby(words, key=lambda w: w[0]):
    print(f"{letter}: {list(group)}")
# a: ['apple', 'avocado']
# b: ['banana', 'blueberry']
# c: ['cherry']
```

Real-world example — group log entries by date:

```python
from itertools import groupby

logs = [
    {"date": "2024-01-15", "msg": "User login"},
    {"date": "2024-01-15", "msg": "File upload"},
    {"date": "2024-01-16", "msg": "User logout"},
    {"date": "2024-01-16", "msg": "Error 500"},
]

for date, entries in groupby(logs, key=lambda e: e["date"]):
    print(f"\n{date}:")
    for entry in entries:
        print(f"  {entry['msg']}")
```

### `itertools.product` — cartesian product

All combinations of items from multiple iterables:

```python
from itertools import product

colors = ["red", "blue"]
sizes = ["S", "M", "L"]

for color, size in product(colors, sizes):
    print(f"{color}-{size}")
# red-S, red-M, red-L, blue-S, blue-M, blue-L
```

### `itertools.combinations` and `permutations`

```python
from itertools import combinations, permutations

# Combinations — order does not matter, no repeats:
list(combinations("ABCD", 2))
# [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]

# Permutations — order matters:
list(permutations("ABC", 2))
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]
```

### `itertools.islice` — slice a generator

You cannot use `[start:stop]` on generators. Use `islice` instead:

```python
from itertools import islice

def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

# Get the first 5 values:
list(islice(infinite_counter(), 5))    # [0, 1, 2, 3, 4]

# Skip 10, take 5:
list(islice(infinite_counter(), 10, 15))    # [10, 11, 12, 13, 14]
```

### `itertools.count`, `cycle`, `repeat` — infinite iterators

```python
from itertools import count, cycle, repeat

# count — infinite counter:
for i in count(start=10, step=3):
    if i > 20:
        break
    print(i)    # 10, 13, 16, 19

# cycle — repeat an iterable forever:
colors = cycle(["red", "green", "blue"])
for _, color in zip(range(6), colors):
    print(color)    # red, green, blue, red, green, blue

# repeat — yield the same value:
list(repeat("hello", 3))    # ["hello", "hello", "hello"]
```

### `itertools.starmap` — map with unpacking

```python
from itertools import starmap

pairs = [(2, 3), (4, 5), (6, 7)]

# Without starmap:
results = [pow(a, b) for a, b in pairs]

# With starmap:
list(starmap(pow, pairs))    # [8, 1024, 279936]
```

## Combining functools and itertools

```python
from functools import lru_cache, reduce
from itertools import combinations

# Find all pairs of numbers that sum to a target:
def find_pairs(numbers, target):
    return [
        pair for pair in combinations(numbers, 2)
        if sum(pair) == target
    ]

find_pairs([1, 2, 3, 4, 5], 6)    # [(1, 5), (2, 4)]

# Cached computation with grouped results:
@lru_cache(maxsize=None)
def expensive_lookup(key):
    # Simulate a slow operation
    return key.upper()
```

## Common Mistakes

**Using `groupby` on unsorted data:**
```python
# WRONG — data is not sorted by key:
data = [1, 2, 1, 3, 2]
for key, group in groupby(data):
    print(key, list(group))
# 1 [1]
# 2 [2]
# 1 [1]    ← 1 appears twice because it was not consecutive!
# 3 [3]
# 2 [2]

# RIGHT — sort first:
data = sorted([1, 2, 1, 3, 2])
for key, group in groupby(data):
    print(key, list(group))
# 1 [1, 1]
# 2 [2, 2]
# 3 [3]
```

**Caching functions with unhashable arguments:**
```python
@lru_cache
def process(data):    # TypeError if data is a list!
    return sum(data)

# Fix: convert to tuple
process(tuple([1, 2, 3]))
```

**Consuming a `groupby` group after moving to the next:**
```python
# WRONG — the group iterator is consumed when you advance to the next group
groups = []
for key, group in groupby(sorted_data, key_func):
    groups.append((key, group))    # group is exhausted by the next iteration!

# RIGHT — materialize the group immediately:
groups = [(key, list(group)) for key, group in groupby(sorted_data, key_func)]
```

## Practice

- [Level 2 / 07 Config File Merger](../projects/level-2/07-config-file-merger/README.md)
- [Module 07 Data Analysis](../projects/modules/07-data-analysis/) — data transformation pipelines
- [Module 08 Advanced Testing](../projects/modules/08-testing-advanced/) — parametrize and combinations
- [Elite Track / 01 Algorithms Complexity Lab](../projects/elite-track/01-algorithms-complexity-lab/README.md)

**Quick check:** [Take the quiz](quizzes/functools-and-itertools-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [functools — Higher-order functions (Python docs)](https://docs.python.org/3/library/functools.html)
- [itertools — Functions creating iterators (Python docs)](https://docs.python.org/3/library/itertools.html)
- [Itertools Recipes (Python docs)](https://docs.python.org/3/library/itertools.html#itertools-recipes)

---

| [← Prev](comprehensions-explained.md) | [Home](../README.md) | [Next →](collections-deep-dive.md) |
|:---|:---:|---:|
