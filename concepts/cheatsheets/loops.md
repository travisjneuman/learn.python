# Loops Cheat Sheet

> A loop repeats code so you do not have to write the same thing over and over.

## Key Syntax

```python
# For loop — do something for each item
for color in ["red", "blue", "green"]:
    print(color)

# For loop — repeat a number of times
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

# While loop — keep going until a condition is False
count = 1
while count <= 5:
    print(count)
    count += 1
```

## Common Patterns

```python
# Loop through a list with index
for i, item in enumerate(fruits):
    print(f"{i}: {item}")

# Build a new list from a loop
squares = [x * x for x in range(10)]

# Sum values
total = 0
for price in prices:
    total += price

# Search for something
for name in names:
    if name == "Alice":
        print("Found!")
        break              # Stop early

# Skip an item
for n in range(10):
    if n == 5:
        continue           # Skip 5, keep looping
    print(n)
```

## `range()` Recipes

| Call | Produces | Note |
|------|----------|------|
| `range(5)` | 0, 1, 2, 3, 4 | Starts at 0, stops before 5 |
| `range(1, 6)` | 1, 2, 3, 4, 5 | Starts at 1, stops before 6 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 | Step by 2 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 | Count backwards |

## When to Use Which

| For loop | While loop |
|----------|------------|
| You know how many times | You do not know when to stop |
| Going through a list | Waiting for user input |
| Counting with `range()` | Repeating until a condition changes |

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Forget to update while condition | Infinite loop (Ctrl+C to stop) | Add `count += 1` inside the loop |
| Off-by-one with `range()` | `range(5)` gives 0-4, not 1-5 | Use `range(1, 6)` for 1-5 |
| Modify list while looping | Skipped items, strange behavior | Loop over a copy or build a new list |
| Indent code outside the loop | Code runs once, not repeated | Check indentation is inside the `for`/`while` |

## Quick Reference

| Operation | Syntax |
|-----------|--------|
| For each item | `for item in my_list:` |
| Repeat N times | `for i in range(n):` |
| With index | `for i, item in enumerate(my_list):` |
| While condition | `while condition:` |
| Exit loop early | `break` |
| Skip to next iteration | `continue` |
| List comprehension | `[x for x in items if x > 0]` |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../how-loops-work.md)
