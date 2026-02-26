# Collections Deep Dive — Part 1: defaultdict, Counter, OrderedDict

[← Back to Overview](./collections-deep-dive.md) · [Part 2: deque, namedtuple, ChainMap →](./collections-deep-dive-part2.md)

---

Python's `collections` module provides specialized container types that go beyond the built-in `list`, `dict`, and `set`. This part covers the three dict-like types: `Counter`, `defaultdict`, and `OrderedDict`.

## Why This Matters

Every program needs to store and organize data. The built-in types handle most cases, but they have gaps. Need to count how often each word appears? `Counter`. Need a dict that automatically handles missing keys? `defaultdict`. Learning these tools saves you from writing (and debugging) boilerplate code.

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

## Common Mistakes

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

---

| [← Overview](./collections-deep-dive.md) | [Part 2: deque, namedtuple, ChainMap →](./collections-deep-dive-part2.md) |
|:---|---:|
