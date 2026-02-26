# Generators and Iterators — Part 1: Iterators

[← Back to Overview](./generators-and-iterators.md) · [Part 2: Generators →](./generators-and-iterators-part2.md)

---

An **iterator** is any object that produces a sequence of values, one at a time. Iterators are the foundation of Python's `for` loop and underpin how generators, file objects, and many built-in functions work.

## Why This Matters

Imagine you need to process a 10 GB log file. Loading it all into a list would crash your program. An iterator reads one item at a time, using almost no memory. Understanding the iterator protocol is key to writing memory-efficient Python.

## Visualize It

Watch how `yield` pauses and resumes a function:
[Open in Python Tutor](https://pythontutor.com/render.html#code=def%20count_up%28n%29%3A%0A%20%20%20%20i%20%3D%201%0A%20%20%20%20while%20i%20%3C%3D%20n%3A%0A%20%20%20%20%20%20%20%20yield%20i%0A%20%20%20%20%20%20%20%20i%20%2B%3D%201%0A%0Afor%20num%20in%20count_up%283%29%3A%0A%20%20%20%20print%28num%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## The iterator protocol

An iterator implements two methods:
- `__iter__()` — returns the iterator object itself
- `__next__()` — returns the next value, or raises `StopIteration` when done

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

## Memory efficiency — why iterators matter

```python
import sys

# List: stores all million values at once
big_list = [i for i in range(1_000_000)]
print(sys.getsizeof(big_list))    # ~8,448,728 bytes (8 MB)

# Generator: stores almost nothing
big_gen = (i for i in range(1_000_000))
print(sys.getsizeof(big_gen))     # ~200 bytes
```

Iterators are essential for:
- Reading large files line by line
- Streaming data from APIs
- Processing infinite sequences
- Chaining transformations on large datasets

## Reading a large file with an iterator

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

**Trying to use an iterator twice:**
```python
gen = (x**2 for x in range(5))
print(list(gen))    # [0, 1, 4, 9, 16]
print(list(gen))    # [] — empty! Iterators are exhausted after one pass
```

If you need to iterate multiple times, use a list or create the iterator again.

**Indexing an iterator:**
```python
gen = (x for x in range(10))
gen[3]    # TypeError: 'generator' object is not subscriptable
```

Use `itertools.islice` or convert to a list first.

---

| [← Overview](./generators-and-iterators.md) | [Part 2: Generators →](./generators-and-iterators-part2.md) |
|:---|---:|
