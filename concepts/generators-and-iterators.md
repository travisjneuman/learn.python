# Generators and Iterators

A generator is a function that produces values one at a time instead of building an entire list in memory. It uses `yield` instead of `return`. This is how Python handles large datasets without running out of memory.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/generators-and-iterators-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

Imagine you need to process a 10 GB log file. Loading it all into a list would crash your program. A generator reads one line at a time, using almost no memory. Generators are the foundation of lazy evaluation in Python — computing values only when they are needed.

## Visualize It

Watch how `yield` pauses and resumes a function:
[Open in Python Tutor](https://pythontutor.com/render.html#code=def%20count_up%28n%29%3A%0A%20%20%20%20i%20%3D%201%0A%20%20%20%20while%20i%20%3C%3D%20n%3A%0A%20%20%20%20%20%20%20%20yield%20i%0A%20%20%20%20%20%20%20%20i%20%2B%3D%201%0A%0Afor%20num%20in%20count_up%283%29%3A%0A%20%20%20%20print%28num%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## Iterators — the concept behind it all

An **iterator** is any object that produces a sequence of values, one at a time, using `__next__()`. When there are no more values, it raises `StopIteration`.

```python
# A list is iterable — you can get an iterator from it
numbers = [10, 20, 30]
it = iter(numbers)       # Get an iterator

print(next(it))          # 10
print(next(it))          # 20
print(next(it))          # 30
print(next(it))          # StopIteration error — no more values
```

A `for` loop does exactly this behind the scenes: it calls `iter()` to get an iterator, then calls `next()` repeatedly until `StopIteration`.

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

## Memory efficiency — why generators matter

```python
import sys

# List: stores all million values at once
big_list = [i for i in range(1_000_000)]
print(sys.getsizeof(big_list))    # ~8,448,728 bytes (8 MB)

# Generator: stores almost nothing
big_gen = (i for i in range(1_000_000))
print(sys.getsizeof(big_gen))     # ~200 bytes
```

Generators are essential for:
- Reading large files line by line
- Streaming data from APIs
- Processing infinite sequences
- Chaining transformations on large datasets

## Reading a large file with a generator

```python
def read_lines(filepath):
    """Yield one line at a time from a file."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()


# Process a huge file without loading it all:
for line in read_lines("server.log"):
    if "ERROR" in line:
        print(line)
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

## `itertools` — the standard library for iteration

Python's `itertools` module provides powerful building blocks:

```python
import itertools

# chain — combine multiple iterables
list(itertools.chain([1, 2], [3, 4], [5]))    # [1, 2, 3, 4, 5]

# islice — slice a generator (you cannot use [start:stop] on generators)
gen = (x**2 for x in range(100))
list(itertools.islice(gen, 5))                 # [0, 1, 4, 9, 16]

# count — infinite counter
for i in itertools.count(start=10, step=3):
    if i > 20:
        break
    print(i)    # 10, 13, 16, 19

# cycle — repeat an iterable forever
colors = itertools.cycle(["red", "green", "blue"])
for _, color in zip(range(6), colors):
    print(color)    # red, green, blue, red, green, blue
```

See [functools and itertools](./functools-and-itertools.md) for a deeper dive.

## Common Mistakes

**Trying to use a generator twice:**
```python
gen = (x**2 for x in range(5))
print(list(gen))    # [0, 1, 4, 9, 16]
print(list(gen))    # [] — empty! Generators are exhausted after one pass
```

If you need to iterate multiple times, use a list or create the generator again.

**Forgetting that generators are lazy:**
```python
# This does NOT print anything yet:
gen = (print(x) for x in range(5))

# Only prints when you consume it:
list(gen)    # NOW it prints 0, 1, 2, 3, 4
```

**Indexing a generator:**
```python
gen = (x for x in range(10))
gen[3]    # TypeError: 'generator' object is not subscriptable
```

Use `itertools.islice` or convert to a list first.

## Practice

- [Level 2 / 07 Config File Merger](../projects/level-2/07-config-file-merger/README.md)
- [Module 05 Async Python](../projects/modules/05-async-python/) — generators are the foundation of async
- [Module 07 Data Analysis](../projects/modules/07-data-analysis/) — processing large datasets
- [Elite Track / 01 Algorithms Complexity Lab](../projects/elite-track/01-algorithms-complexity-lab/README.md)

**Quick check:** [Take the quiz](quizzes/generators-and-iterators-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [Generator expressions (Python docs)](https://docs.python.org/3/reference/expressions.html#generator-expressions)
- [itertools — Functions creating iterators](https://docs.python.org/3/library/itertools.html)
- [PEP 255 — Simple Generators](https://peps.python.org/pep-0255/)
- [PEP 380 — Syntax for Delegating to a Subgenerator (yield from)](https://peps.python.org/pep-0380/)

---

| [← Prev](context-managers-explained.md) | [Home](../README.md) | [Next →](comprehensions-explained.md) |
|:---|:---:|---:|
