# Collections: Lists, Dicts, Sets

Python has several ways to group multiple values together.

## Lists — ordered, changeable, allows duplicates

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")     # Add to end
fruits[0]                 # "apple" (first item)
fruits[-1]                # "date" (last item)
len(fruits)               # 4
"banana" in fruits        # True
```

Use lists when: you have an ordered collection of similar items (scores, names, files).

## Dictionaries — key-value pairs, unordered, changeable

```python
person = {"name": "Travis", "age": 30}
person["name"]            # "Travis"
person["city"] = "Denver" # Add new key
person.get("salary")      # None (safe access, no error)
```

Use dicts when: you have labeled data (a person's details, configuration, lookup table).

## Sets — unordered, no duplicates

```python
colors = {"red", "blue", "green", "red"}
print(colors)             # {"red", "blue", "green"} — duplicate removed
colors.add("yellow")
"red" in colors           # True
```

Use sets when: you need unique values or want to check membership quickly.

## Tuples — ordered, unchangeable

```python
point = (3, 5)
x = point[0]             # 3
y = point[1]             # 5
# point[0] = 10          # Error! Tuples cannot be changed
```

Use tuples when: you have a fixed group of values that should not change (coordinates, RGB colors).

## Quick comparison

| Feature | List | Dict | Set | Tuple |
|---------|------|------|-----|-------|
| Syntax | `[1, 2, 3]` | `{"a": 1}` | `{1, 2, 3}` | `(1, 2, 3)` |
| Ordered | Yes | No* | No | Yes |
| Changeable | Yes | Yes | Yes | No |
| Duplicates | Yes | No (keys) | No | Yes |
| Access by | Index | Key | N/A | Index |

*Dicts maintain insertion order in Python 3.7+ but are not indexed by position.

## Common mistakes

**Empty dict vs empty set:**
```python
empty_dict = {}     # This is a dict, NOT a set
empty_set = set()   # This is how you make an empty set
```

**Modifying a list while iterating:**
```python
# Wrong
for item in items:
    items.remove(item)

# Right — build a new list
items = [item for item in items if item != "remove_me"]
```

## Related exercises
- [Level 00, Exercise 09 — Lists](../projects/level-00-absolute-beginner/09-lists/)
- [Level 00, Exercise 12 — Dictionaries](../projects/level-00-absolute-beginner/12-dictionaries/)
