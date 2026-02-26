# Collections Deep Dive

Python's `collections` module provides specialized container types that go beyond the built-in `list`, `dict`, and `set`. They solve common patterns like counting items, creating lightweight objects, and handling missing dictionary keys — all with less code and better performance than rolling your own solution.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/collections-deep-dive-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

Every program needs to store and organize data. The built-in types handle most cases, but they have gaps. Need to count how often each word appears? `Counter`. Need a dict that automatically handles missing keys? `defaultdict`. Need a lightweight immutable object with named fields? `namedtuple`. Learning these tools saves you from writing (and debugging) boilerplate code.

## `Counter` — count things

The most intuitive way to count occurrences:

```python
from collections import Counter

# Count letters in a string:
letter_counts = Counter("mississippi")
print(letter_counts)
# Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})

# Count words in a list:
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_counts = Counter(words)
print(word_counts)
# Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# Most common items:
word_counts.most_common(2)
# [('apple', 3), ('banana', 2)]
```

Counter supports math operations:

```python
a = Counter("aabbcc")
b = Counter("aabbd")

a + b     # Counter({'a': 4, 'b': 4, 'c': 2, 'd': 1})
a - b     # Counter({'c': 2}) — only positive counts
a & b     # Counter({'a': 2, 'b': 2}) — minimum of each
a | b     # Counter({'a': 2, 'b': 2, 'c': 2, 'd': 1}) — maximum of each
```

## `defaultdict` — dicts with automatic defaults

A `defaultdict` never raises `KeyError` — it creates a default value automatically for missing keys:

```python
from collections import defaultdict

# Group items by category:
animals = [("cat", "Felix"), ("dog", "Rex"), ("cat", "Whiskers"), ("dog", "Buddy")]

groups = defaultdict(list)    # Missing keys get an empty list
for category, name in animals:
    groups[category].append(name)

print(groups)
# defaultdict(<class 'list'>, {'cat': ['Felix', 'Whiskers'], 'dog': ['Rex', 'Buddy']})
```

Compare with regular dict:
```python
# Without defaultdict — verbose:
groups = {}
for category, name in animals:
    if category not in groups:
        groups[category] = []
    groups[category].append(name)

# With defaultdict — clean:
groups = defaultdict(list)
for category, name in animals:
    groups[category].append(name)
```

Common default factories:
```python
defaultdict(list)     # Missing keys → empty list []
defaultdict(int)      # Missing keys → 0
defaultdict(set)      # Missing keys → empty set set()
defaultdict(str)      # Missing keys → empty string ""
defaultdict(dict)     # Missing keys → empty dict {}
```

Counting with `defaultdict(int)`:
```python
word_count = defaultdict(int)
for word in "the cat sat on the mat".split():
    word_count[word] += 1
# {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
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

## `OrderedDict` — dict that remembers insertion order

Since Python 3.7, regular dicts maintain insertion order. So when is `OrderedDict` still useful?

```python
from collections import OrderedDict

# OrderedDict considers order in equality checks:
d1 = OrderedDict([("a", 1), ("b", 2)])
d2 = OrderedDict([("b", 2), ("a", 1)])
d1 == d2    # False — different order!

# Regular dicts do not:
{"a": 1, "b": 2} == {"b": 2, "a": 1}    # True

# OrderedDict has move_to_end:
od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")        # a moves to end: OrderedDict([('b', 2), ('c', 3), ('a', 1)])
od.move_to_end("c", last=False)  # c moves to start: OrderedDict([('c', 3), ('b', 2), ('a', 1)])
```

Use `OrderedDict` when order matters for equality comparison or when you need `move_to_end()`. Otherwise, use a regular dict.

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

**Forgetting that defaultdict creates entries on access:**
```python
d = defaultdict(list)
if d["missing_key"]:    # This CREATES the key with an empty list!
    pass

# Use "key in d" to check without creating:
if "missing_key" in d:
    pass
```

**Using Counter with non-hashable items:**
```python
# Lists are not hashable:
Counter([[1, 2], [3, 4]])    # TypeError!
# Convert to tuples first:
Counter([(1, 2), (3, 4)])    # OK
```

## Practice

- [Level 1 / 08 Log Level Counter](../projects/level-1/08-log-level-counter/README.md) — Counter
- [Level 2 / 07 Config File Merger](../projects/level-2/07-config-file-merger/README.md) — ChainMap, defaultdict
- [Module 07 Data Analysis](../projects/modules/07-data-analysis/) — data aggregation with Counter

**Quick check:** [Take the quiz](quizzes/collections-deep-dive-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [collections — Container datatypes (Python docs)](https://docs.python.org/3/library/collections.html)
- [Collections Abstract Base Classes](https://docs.python.org/3/library/collections.abc.html)

---

| [← Prev](functools-and-itertools.md) | [Home](../README.md) | [Next →](testing-strategies.md) |
|:---|:---:|---:|
