# functools and itertools — Part 2: itertools

[← Part 1: functools](./functools-and-itertools-part1.md) · [Back to Overview](./functools-and-itertools.md)

---

The `itertools` module gives you building blocks for efficient iteration. These tools let you chain sequences, generate combinations, group data, and work with infinite iterators — all lazily and memory-efficiently.

## `itertools.chain` — combine multiple iterables

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

## `itertools.groupby` — group consecutive items

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

## `itertools.product` — cartesian product

All combinations of items from multiple iterables:

```python
from itertools import product

colors = ["red", "blue"]
sizes = ["S", "M", "L"]

for color, size in product(colors, sizes):
    print(f"{color}-{size}")
# red-S, red-M, red-L, blue-S, blue-M, blue-L
```

## `itertools.combinations` and `permutations`

```python
from itertools import combinations, permutations

# Combinations — order does not matter, no repeats:
list(combinations("ABCD", 2))
# [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]

# Permutations — order matters:
list(permutations("ABC", 2))
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]
```

## `itertools.islice` — slice a generator

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

## `itertools.count`, `cycle`, `repeat` — infinite iterators

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

## `itertools.starmap` — map with unpacking

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
from itertools import combinations

# Find all pairs of numbers that sum to a target:
def find_pairs(numbers, target):
    return [
        pair for pair in combinations(numbers, 2)
        if sum(pair) == target
    ]

find_pairs([1, 2, 3, 4, 5], 6)    # [(1, 5), (2, 4)]
```

## Common Mistakes (itertools)

**Using `groupby` on unsorted data:**
```python
# WRONG — data is not sorted by key:
data = [1, 2, 1, 3, 2]
for key, group in groupby(data):
    print(key, list(group))
# 1 [1]
# 2 [2]
# 1 [1]    <- 1 appears twice because it was not consecutive!
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

**Consuming a `groupby` group after moving to the next:**
```python
# WRONG — the group iterator is consumed when you advance to the next group
groups = []
for key, group in groupby(sorted_data, key_func):
    groups.append((key, group))    # group is exhausted by the next iteration!

# RIGHT — materialize the group immediately:
groups = [(key, list(group)) for key, group in groupby(sorted_data, key_func)]
```

---

| [← Part 1: functools](./functools-and-itertools-part1.md) | [Overview](./functools-and-itertools.md) |
|:---|---:|
