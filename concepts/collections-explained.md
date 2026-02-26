# Collections: Lists, Dicts, Sets

> **Try This First:** Before reading, try this in Python: `fruits = ['apple', 'banana']; fruits.append('cherry'); print(fruits)`. What does the list look like after `append`?

Python has several ways to group multiple values together.

## Visualize It

See how lists, dicts, and sets store data differently in memory:
[Open in Python Tutor](https://pythontutor.com/render.html#code=fruits%20%3D%20%5B%22apple%22%2C%20%22banana%22%5D%0Afruits.append%28%22cherry%22%29%0A%0Aperson%20%3D%20%7B%22name%22%3A%20%22Alice%22%2C%20%22age%22%3A%2030%7D%0Aperson%5B%22city%22%5D%20%3D%20%22Denver%22%0A%0Acolors%20%3D%20%7B%22red%22%2C%20%22blue%22%2C%20%22red%22%7D%0Aprint%28len%28colors%29%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

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

## Dictionaries — key-value pairs, insertion-ordered (Python 3.7+), changeable

```python
person = {"name": "Alice", "age": 30}
person["name"]            # "Alice"
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
| Ordered | Yes | Yes* | No | Yes |
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

## Practice

- [Level 00 / 09 Lists](../projects/level-00-absolute-beginner/09-lists/)
- [Level 00 / 12 Dictionaries](../projects/level-00-absolute-beginner/12-dictionaries/)
- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 0 / 09 Daily Checklist Writer](../projects/level-0/09-daily-checklist-writer/README.md)
- [Level 0 / 10 Duplicate Line Finder](../projects/level-0/10-duplicate-line-finder/README.md)
- [Level 0 / 12 Contact Card Builder](../projects/level-0/12-contact-card-builder/README.md)
- [Level 1 / 05 Csv First Reader](../projects/level-1/05-csv-first-reader/README.md)
- [Level 1 / 09 Json Settings Loader](../projects/level-1/09-json-settings-loader/README.md)
- [Level 1 / 12 File Extension Counter](../projects/level-1/12-file-extension-counter/README.md)
- [Level 1 / 14 Basic Expense Tracker](../projects/level-1/14-basic-expense-tracker/README.md)
- [Level 2 / 01 Dictionary Lookup Service](../projects/level-2/01-dictionary-lookup-service/README.md)
- [Level 2 / 02 Nested Data Flattener](../projects/level-2/02-nested-data-flattener/README.md)

**Quick check:** [Take the quiz](quizzes/collections-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../projects/level-0/README.md) | [Home](../README.md) | [Next →](files-and-paths.md) |
|:---|:---:|---:|
