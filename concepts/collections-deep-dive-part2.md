# Collections Deep Dive — Part 2: deque, namedtuple, ChainMap

[← Part 1: defaultdict, Counter, OrderedDict](./collections-deep-dive-part1.md) · [Back to Overview](./collections-deep-dive.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

This part covers the remaining `collections` types: `deque` for fast double-ended operations, `namedtuple` for lightweight immutable records, and `ChainMap` for layered dict lookups.

## `deque` — double-ended queue

A `deque` (pronounced "deck") is like a list, but optimized for adding and removing items from both ends:

```python
from collections import deque

# Create a deque:
d = deque([1, 2, 3])

# Add to both ends (O(1) — fast):
d.append(4)        # [1, 2, 3, 4]
d.appendleft(0)    # [0, 1, 2, 3, 4]

# Remove from both ends (O(1) — fast):
d.pop()            # 4, deque is [0, 1, 2, 3]
d.popleft()        # 0, deque is [1, 2, 3]

# Rotate:
d = deque([1, 2, 3, 4, 5])
d.rotate(2)        # [4, 5, 1, 2, 3] — rotate right
d.rotate(-2)       # [1, 2, 3, 4, 5] — rotate left
```

`list.insert(0, x)` is O(n) because it shifts every element. `deque.appendleft(x)` is O(1). Use a deque when you need to frequently add or remove from the front.

**Fixed-size buffer:**
```python
# Keep only the last 5 items:
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)
print(recent)    # deque([5, 6, 7, 8, 9], maxlen=5)
```

## `namedtuple` — lightweight immutable objects

A `namedtuple` is like a tuple, but with named fields. Great for simple data containers:

```python
from collections import namedtuple

# Define a type:
Point = namedtuple("Point", ["x", "y"])

# Create instances:
p = Point(3, 4)
print(p.x)       # 3
print(p.y)       # 4
print(p)          # Point(x=3, y=4)

# Still works like a tuple:
x, y = p         # Unpacking
print(p[0])       # 3 (indexing)
```

Real-world example:

```python
User = namedtuple("User", ["name", "email", "role"])

alice = User("Alice", "alice@example.com", "admin")
bob = User("Bob", "bob@example.com", "user")

print(alice.name)    # "Alice"
print(bob.role)      # "user"

# Immutable — you cannot change fields:
alice.name = "Alicia"    # AttributeError!

# Create a modified copy with _replace:
alicia = alice._replace(name="Alicia")
```

For mutable named fields or more features, use `dataclasses` instead. See [Dataclasses Explained](./dataclasses-explained.md).

## `ChainMap` — search multiple dicts as one

A `ChainMap` groups multiple dictionaries together. Lookups search each dict in order until the key is found:

```python
from collections import ChainMap

defaults = {"color": "blue", "size": "medium", "font": "Arial"}
user_prefs = {"color": "red"}
cli_args = {"size": "large"}

# Search CLI args first, then user prefs, then defaults:
config = ChainMap(cli_args, user_prefs, defaults)

print(config["size"])     # "large" (from cli_args)
print(config["color"])    # "red" (from user_prefs)
print(config["font"])     # "Arial" (from defaults)
```

This is useful for configuration systems where you have multiple layers of settings (defaults, user config, command-line overrides).

## Quick reference

| Type | Use when you need... | Example |
|------|---------------------|---------|
| `Counter` | Count occurrences | Word frequency, vote tallying |
| `defaultdict` | Dict with automatic defaults | Grouping, counting, nested dicts |
| `namedtuple` | Immutable record with named fields | Coordinates, database rows, config |
| `deque` | Fast append/pop from both ends | Queues, buffers, sliding windows |
| `OrderedDict` | Order-sensitive equality | Config where order matters |
| `ChainMap` | Layered dict lookups | Multi-level configuration |

## Common Mistakes

**Mutating a namedtuple (you cannot):**
```python
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x = 3    # AttributeError!
# Use p._replace(x=3) to create a new instance
```

---

| [← Part 1: defaultdict, Counter, OrderedDict](./collections-deep-dive-part1.md) | [Overview](./collections-deep-dive.md) |
|:---|---:|
