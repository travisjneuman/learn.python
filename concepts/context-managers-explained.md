# Context Managers Explained

A context manager is something that sets up a resource when you enter a block and cleans it up when you leave — even if an error occurs. The `with` statement is how you use them. If you have ever written `with open("file.txt") as f:`, you have already used one.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/context-managers-explained.md) | [Quiz](quizzes/context-managers-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/context-managers-explained.md) |

<!-- modality-hub-end -->

## Why This Matters

Resources like files, database connections, and network sockets need to be properly closed when you are done with them. Forgetting to close a file can corrupt data. Forgetting to close a database connection can exhaust the connection pool and crash your server. Context managers make cleanup automatic — you cannot forget.

## Visualize It

Watch how `with` guarantees cleanup, even when an error is raised:
[Open in Python Tutor](https://pythontutor.com/render.html#code=class%20ManagedFile%3A%0A%20%20%20%20def%20__init__%28self%2C%20name%29%3A%0A%20%20%20%20%20%20%20%20self.name%20%3D%20name%0A%20%20%20%20def%20__enter__%28self%29%3A%0A%20%20%20%20%20%20%20%20print%28f%22Opening%20%7Bself.name%7D%22%29%0A%20%20%20%20%20%20%20%20return%20self%0A%20%20%20%20def%20__exit__%28self%2C%20exc_type%2C%20exc_val%2C%20exc_tb%29%3A%0A%20%20%20%20%20%20%20%20print%28f%22Closing%20%7Bself.name%7D%22%29%0A%20%20%20%20%20%20%20%20return%20False%0A%0Awith%20ManagedFile%28%22data.txt%22%29%20as%20f%3A%0A%20%20%20%20print%28%22Working%20with%20file%22%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## The basic pattern — `with` and files

Without a context manager, you must remember to close the file yourself:

```python
# WITHOUT a context manager — risky
f = open("data.txt")
content = f.read()
f.close()    # What if an error happens before this line?
```

With a context manager, cleanup is guaranteed:

```python
# WITH a context manager — safe
with open("data.txt") as f:
    content = f.read()
# f.close() is called automatically, even if an error occurred
```

The `with` statement calls `f.__enter__()` at the start and `f.__exit__()` at the end, no matter what happens inside the block.

## How `__enter__` and `__exit__` work

Any object can be a context manager if it has two special methods:

```python
class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        # Called when entering the `with` block
        self.file = open(self.filename)
        return self.file    # This becomes the `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Called when leaving the `with` block — ALWAYS
        self.file.close()
        return False    # False means: do not suppress exceptions


# Usage:
with ManagedFile("data.txt") as f:
    content = f.read()
```

The three arguments to `__exit__` describe any exception that occurred:
- `exc_type` — the exception class (e.g., `ValueError`), or `None` if no error
- `exc_val` — the exception instance
- `exc_tb` — the traceback object

If `__exit__` returns `True`, the exception is suppressed (swallowed). If it returns `False` (the default), the exception propagates normally. Almost always return `False`.

## The easy way — `contextlib.contextmanager`

Writing a class with `__enter__` and `__exit__` is verbose. The `contextlib` module gives you a decorator that turns a generator function into a context manager:

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename):
    # __enter__: everything before yield
    f = open(filename)
    try:
        yield f    # This value becomes the `as` variable
    finally:
        # __exit__: everything after yield
        f.close()


# Usage — exactly the same:
with managed_file("data.txt") as f:
    content = f.read()
```

The pattern is:
1. **Before `yield`** — setup (like `__enter__`)
2. **`yield value`** — the value assigned by `as`
3. **After `yield`** — cleanup (like `__exit__`), usually in a `finally` block

## Real-world examples

### Database connection

```python
from contextlib import contextmanager
import sqlite3

@contextmanager
def get_db(path):
    conn = sqlite3.connect(path)
    try:
        yield conn
        conn.commit()      # Commit if no errors
    except Exception:
        conn.rollback()    # Rollback on error
        raise              # Re-raise the exception
    finally:
        conn.close()       # Always close


with get_db("app.db") as conn:
    conn.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    # If this block raises, the transaction is rolled back
    # If it succeeds, changes are committed
    # Either way, the connection is closed
```

### Temporary directory

```python
import tempfile
import os

# Python's built-in context manager for temp directories
with tempfile.TemporaryDirectory() as tmpdir:
    path = os.path.join(tmpdir, "temp_file.txt")
    with open(path, "w") as f:
        f.write("temporary data")
    # Work with the directory...
# Directory and all contents are deleted automatically
```

### Timing a block of code

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.2f}s")


with timer("data processing"):
    # ... expensive work here ...
    total = sum(range(10_000_000))
# Prints: data processing: 0.23s
```

### Suppressing specific exceptions

```python
from contextlib import suppress

# Instead of try/except/pass:
with suppress(FileNotFoundError):
    os.remove("temp.txt")
# If the file does not exist, no error — the exception is silently caught
```

### Thread lock

```python
import threading

lock = threading.Lock()

# The lock is a context manager — it acquires on enter, releases on exit
with lock:
    # Only one thread can be here at a time
    shared_data.append(item)
```

## Nesting context managers

You can nest `with` statements, or combine them on one line:

```python
# Nested:
with open("input.txt") as src:
    with open("output.txt", "w") as dst:
        dst.write(src.read())

# Combined (Python 3.1+):
with open("input.txt") as src, open("output.txt", "w") as dst:
    dst.write(src.read())

# Parenthesized (Python 3.10+):
with (
    open("input.txt") as src,
    open("output.txt", "w") as dst,
):
    dst.write(src.read())
```

## Common Mistakes

**Forgetting that `__exit__` always runs:**
```python
# This is fine — __exit__ runs even if you return early
with open("data.txt") as f:
    first_line = f.readline()
    if not first_line:
        return    # File is still closed properly
```

**Suppressing exceptions by accident:**
```python
class BadContextManager:
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return True    # DANGER: swallows ALL exceptions silently!
```

Always return `False` from `__exit__` unless you have a very specific reason to suppress exceptions.

**Using a closed resource outside the `with` block:**
```python
with open("data.txt") as f:
    pass

f.read()    # ValueError: I/O operation on closed file
```

The resource is only valid inside the `with` block.

## Practice

- [Module 06 Databases & ORM](../projects/modules/06-databases-orm/) — database connections with context managers
- [Level 1 / 01 Text Stats](../projects/level-1/01-text-stats/README.md) — file reading with `with`
- [Level 1 / 05 CSV First Reader](../projects/level-1/05-csv-first-reader/README.md) — CSV files with `with`

## Further Reading

- [contextlib — Utilities for with-statement contexts](https://docs.python.org/3/library/contextlib.html)
- [The with statement (Python docs)](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
- [PEP 343 — The "with" Statement](https://peps.python.org/pep-0343/)

---

| [← Prev](async-explained.md) | [Home](../README.md) | [Next →](generators-and-iterators.md) |
|:---|:---:|---:|
