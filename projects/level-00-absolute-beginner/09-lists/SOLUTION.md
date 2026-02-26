# Solution: 09-lists

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Create a list
colors = ["red", "blue", "green", "yellow"]  # WHY: Square brackets [] create a list — commas separate each item. This stores 4 color names in order
print("Colors:", colors)                      # WHY: Printing a list shows all items with brackets and commas — helpful for checking what is inside

# Access items by position (called "index").
# IMPORTANT: Counting starts at 0, not 1.
print("First color:", colors[0])    # WHY: Index 0 is the first item ("red") — computers count from 0, not 1. This is universal across all programming
print("Second color:", colors[1])   # WHY: Index 1 is the second item ("blue") — so index 2 is the third, index 3 is the fourth, and so on
print("Last color:", colors[-1])    # WHY: Index -1 is a shortcut for the last item ("yellow") — -2 would be second-to-last, and so on

# How many items are in the list?
print("Number of colors:", len(colors))  # WHY: len() counts the items — useful for knowing the size of your data. This list has 4 items

# Add an item to the end
colors.append("purple")                  # WHY: .append() adds one item to the END of the list — the list is now 5 items long
print("After adding purple:", colors)    # WHY: Prints ["red", "blue", "green", "yellow", "purple"] — purple was tacked onto the end

# Remove an item by value
colors.remove("blue")                    # WHY: .remove() finds the FIRST occurrence of "blue" and takes it out — the list shrinks by one
print("After removing blue:", colors)    # WHY: Prints ["red", "green", "yellow", "purple"] — blue is gone, everything shifted to fill the gap

# Check if something is in the list
if "red" in colors:                      # WHY: "in" checks if a value exists anywhere in the list — returns True or False
    print("Red is in the list!")

if "orange" not in colors:               # WHY: "not in" is the opposite check — True if the value does NOT exist in the list
    print("Orange is NOT in the list.")

# Lists can hold numbers too
scores = [95, 87, 92, 78, 100]           # WHY: Lists work with any type of data — numbers, strings, even other lists
print("Scores:", scores)
print("Highest:", max(scores))           # WHY: max() finds the largest number in the list — saves you from writing a loop to find it manually
print("Lowest:", min(scores))            # WHY: min() finds the smallest number — paired with max() you get the full range
print("Total:", sum(scores))             # WHY: sum() adds all the numbers together — 95+87+92+78+100 = 452
print("Average:", sum(scores) / len(scores))  # WHY: Average = total / count — sum() gives the total, len() gives the count. 452 / 5 = 90.4

# Lists can hold a mix of types (but usually you keep them uniform)
mixed = ["Alice", 30, True, 3.14]        # WHY: Python allows mixing types, but in practice you rarely do this — keep lists uniform for clarity
print("Mixed list:", mixed)

# Sort a list
numbers = [5, 2, 8, 1, 9, 3]            # WHY: An unsorted list of numbers
numbers.sort()                            # WHY: .sort() rearranges the list from smallest to largest — it changes the list in place (does not create a new one)
print("Sorted:", numbers)                # WHY: Prints [1, 2, 3, 5, 8, 9] — the original order is gone. If you needed the original, you should have copied first
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Start counting from 0 | This is not a choice — all programming languages count from 0. Learning this now prevents confusion forever | There is no alternative. `colors[1]` is always the second item, never the first. This is the hardest thing for beginners to accept, but it becomes natural quickly |
| Use `.append()` to add items | `.append()` is the most common way to grow a list — it adds to the end, which is fast and predictable | `.insert(0, "purple")` adds to a specific position, but it is slower and less common |
| Use `.remove()` by value | Removing by value is more intuitive for beginners — you say "remove blue" not "remove the item at position 1" | `del colors[1]` or `colors.pop(1)` removes by position, which is useful when you know the index |
| Show `max()`, `min()`, `sum()`, `len()` | These four built-in functions cover 90% of what you need to do with number lists | Could write manual loops for each, but Python provides these functions specifically to save you time |

## Alternative approaches

### Approach B: Building a list from user input

```python
foods = []                                        # WHY: Start with an empty list — the brackets with nothing inside create a list with zero items

print("Enter 3 of your favorite foods:")
for i in range(3):                                # WHY: range(3) runs the loop 3 times — asking for one food each time
    food = input(f"Food {i + 1}: ")               # WHY: i starts at 0 so we add 1 for display — shows "Food 1:", "Food 2:", "Food 3:"
    foods.append(food)                            # WHY: Each answer is added to the end of the list, growing it one item at a time

print(f"\nYour foods: {foods}")                   # WHY: \n adds a blank line before the result — prints the complete list
print(f"You entered {len(foods)} foods.")          # WHY: len() confirms the list has exactly 3 items — useful for debugging
```

**Trade-off:** Building a list item-by-item with `.append()` is the standard pattern in Python. The exercise creates lists with all items at once (`[item1, item2, item3]`), which is fine when you know the data ahead of time. Use `.append()` when the data comes in one piece at a time (like from user input or a file).

### Approach C: Using sorted() instead of .sort()

```python
original = [5, 2, 8, 1, 9, 3]           # WHY: The original unsorted list
ordered = sorted(original)               # WHY: sorted() creates a NEW sorted list — the original stays unchanged
print("Original:", original)             # WHY: Still [5, 2, 8, 1, 9, 3] — untouched
print("Sorted copy:", ordered)           # WHY: [1, 2, 3, 5, 8, 9] — a brand new list in order
```

**Trade-off:** `.sort()` changes the list permanently — the original order is lost. `sorted()` creates a new list and keeps the original. Use `sorted()` when you need both the original and the sorted version.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Accessing an index that does not exist: `colors[99]` | `IndexError: list index out of range` — the list does not have 100 items | Check `len(colors)` first. Remember: a list with 4 items has valid indices 0, 1, 2, and 3 |
| Off-by-one error: thinking `colors[4]` is the 4th item | `IndexError` — in a 4-item list, the last valid index is 3 (because counting starts at 0) | Index 0 is the 1st item, index 3 is the 4th item. The pattern is: position = index + 1 |
| Removing an item that is not in the list: `colors.remove("pink")` | `ValueError: list.remove(x): x not in list` — Python cannot remove what does not exist | Check first with `if "pink" in colors:` before calling `.remove()` |
| Confusing `.append()` and `.extend()` | `colors.append(["pink", "brown"])` adds a list inside your list (nested). `.extend()` adds each item individually | Use `.append()` for one item, `.extend()` for adding multiple items from another list |
| Modifying a list while looping through it | Unexpected behavior — items can be skipped or the loop can crash | Create a new list or loop through a copy: `for item in colors.copy():` |

## Key takeaways

1. **Lists are ordered collections that grow and shrink** — they are the most versatile data structure in Python. Any time you have multiple items of the same kind (names, scores, files, products), a list is your first choice. You will use lists in nearly every program you write.
2. **Indexing starts at 0, and this is non-negotiable** — the first item is `[0]`, not `[1]`. This is the single most common source of confusion for new programmers, and it never fully goes away. The payoff is that negative indices work beautifully: `[-1]` is always the last item.
3. **`append`, `remove`, `sort`, `in`, `len`, `sum`, `max`, `min` are your list toolkit** — these operations handle the vast majority of what you will need to do with lists. In Exercise 10, you will combine lists with loops, which is where the real power of lists comes alive.
