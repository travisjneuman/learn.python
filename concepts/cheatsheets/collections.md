# Collections Cheat Sheet

> Python has four main ways to group values: lists, dicts, sets, and tuples.

## Lists -- ordered, changeable, allows duplicates

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")       # Add to end
fruits.insert(0, "avocado") # Insert at position
fruits.remove("banana")     # Remove by value
last = fruits.pop()         # Remove and return last item
fruits[0]                   # First item
fruits[-1]                  # Last item
len(fruits)                 # How many items
"cherry" in fruits          # True
fruits.sort()               # Sort in place
```

## Dicts -- key-value pairs, ordered (3.7+)

```python
person = {"name": "Alice", "age": 30}
person["name"]              # "Alice"
person["city"] = "Denver"   # Add a key
person.get("salary")        # None (safe, no error)
person.get("salary", 0)     # 0 (default if missing)
del person["age"]           # Remove a key
person.keys()               # All keys
person.values()             # All values
person.items()              # All (key, value) pairs
```

## Sets -- unordered, no duplicates

```python
colors = {"red", "blue", "red"}  # {"red", "blue"}
colors.add("green")
colors.discard("red")       # Remove (no error if missing)
"blue" in colors             # True (fast lookup)

# Set math
a | b    # Union (everything)
a & b    # Intersection (overlap)
a - b    # Difference (in a, not in b)
```

## Tuples -- ordered, unchangeable

```python
point = (3, 5)
x, y = point               # Unpack: x=3, y=5
point[0]                    # 3
# point[0] = 10             # Error! Cannot change a tuple
```

## When to Use Which

| Need | Use |
|------|-----|
| Ordered list of items | `list` |
| Labeled data (lookup by name) | `dict` |
| Unique items or fast membership check | `set` |
| Fixed group that should not change | `tuple` |

## Common Patterns

```python
# Loop through a dict
for key, value in person.items():
    print(f"{key}: {value}")

# Count things with a dict
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

# Remove duplicates from a list
unique = list(set(my_list))

# Check if something is in a collection
if "Alice" in names:       # Works for list, set, dict, tuple
    print("Found!")
```

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Empty set | `x = {}` (this is a dict!) | `x = set()` |
| Modify list while looping | `for i in lst: lst.remove(i)` | Build a new list instead |
| Dict key missing | `person["email"]` crashes | `person.get("email")` |
| Mutable dict key | `{[1,2]: "val"}` (lists can't be keys) | Use tuples: `{(1,2): "val"}` |

## Quick Comparison

| Feature | List | Dict | Set | Tuple |
|---------|------|------|-----|-------|
| Syntax | `[1, 2, 3]` | `{"a": 1}` | `{1, 2, 3}` | `(1, 2, 3)` |
| Ordered | Yes | Yes | No | Yes |
| Changeable | Yes | Yes | Yes | No |
| Duplicates | Yes | No (keys) | No | Yes |
| Access by | Index | Key | N/A | Index |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../collections-explained.md)
