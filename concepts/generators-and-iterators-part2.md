# Generators and Iterators — Part 2: Generators

[← Part 1: Iterators](./generators-and-iterators-part1.md) · [Back to Overview](./generators-and-iterators.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

A **generator** is a function that produces values one at a time using `yield` instead of `return`. Generators are the easy way to create iterators — they handle the protocol automatically and let you write lazy, memory-efficient code.

## Generators — the easy way to make iterators

Writing a class with `__iter__` and `__next__` is tedious. A **generator function** does the same thing with much less code:

```python
def count_up(n):
    """Yield numbers from 1 to n."""
    i = 1
    while i <= n:
        yield i     # Pause here, produce a value
        i += 1      # Resume here on next call

# Usage:
for num in count_up(5):
    print(num)      # 1, 2, 3, 4, 5
```

When Python hits `yield`, the function **pauses** and gives back the value. Next time you ask for a value, it **resumes** right where it left off.

A generator function does not run when you call it — it returns a generator object:

```python
gen = count_up(3)       # Nothing runs yet
print(type(gen))        # <class 'generator'>
print(next(gen))        # 1 — now it runs until the first yield
print(next(gen))        # 2
print(next(gen))        # 3
```

## Generator expressions — one-liners

Just like list comprehensions create lists, **generator expressions** create generators:

```python
# List comprehension — builds the entire list in memory
squares_list = [x**2 for x in range(1_000_000)]    # Uses ~8 MB

# Generator expression — computes one value at a time
squares_gen = (x**2 for x in range(1_000_000))      # Uses ~100 bytes
```

The only syntax difference is `()` instead of `[]`. Use generator expressions when you only need to iterate once and do not need to index or re-use the data.

```python
# Common pattern: pass directly to a function
total = sum(x**2 for x in range(100))    # No extra brackets needed
```

## Chaining generators (pipelines)

Generators compose beautifully into processing pipelines:

```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

def filter_errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line

def extract_timestamp(lines):
    for line in lines:
        yield line.split(" ")[0]    # First word is the timestamp

# Chain them together — no intermediate lists:
lines = read_lines("server.log")
errors = filter_errors(lines)
timestamps = extract_timestamp(errors)

for ts in timestamps:
    print(ts)
```

Each generator pulls one value at a time from the previous one. The entire file is never loaded into memory.

## `yield from` — delegating to another generator

When one generator needs to yield all values from another, use `yield from`:

```python
def count_up(n):
    for i in range(1, n + 1):
        yield i

def count_down(n):
    for i in range(n, 0, -1):
        yield i

def up_and_down(n):
    yield from count_up(n)       # Yields 1, 2, ..., n
    yield from count_down(n)     # Then n, n-1, ..., 1


list(up_and_down(3))    # [1, 2, 3, 3, 2, 1]
```

Without `yield from`, you would need a loop: `for x in count_up(n): yield x`.

## `send()` and `throw()` — advanced two-way communication

Generators can receive values, not just produce them:

```python
def running_average():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average    # Receive a value, send back the average
        total += value
        count += 1
        average = total / count


avg = running_average()
next(avg)              # Prime the generator (advance to first yield)
print(avg.send(10))    # 10.0
print(avg.send(20))    # 15.0
print(avg.send(30))    # 20.0
```

This is an advanced pattern. You will not need it often, but it powers frameworks like `asyncio` under the hood.

## Common Mistakes

**Forgetting that generators are lazy:**
```python
# This does NOT print anything yet:
gen = (print(x) for x in range(5))

# Only prints when you consume it:
list(gen)    # NOW it prints 0, 1, 2, 3, 4
```

---

| [← Part 1: Iterators](./generators-and-iterators-part1.md) | [Overview](./generators-and-iterators.md) |
|:---|---:|
