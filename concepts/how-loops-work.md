# How Loops Work

> **Try This First:** Before reading, open Python and type `for i in range(5): print(i)`. Watch what happens. How many numbers print? Does it start at 0 or 1?

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/how-loops-work.md) | [Quiz](quizzes/how-loops-work-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/how-loops-work.md) |

<!-- modality-hub-end -->

A loop repeats code. Instead of writing the same thing 100 times, you write it once and let the loop handle repetition.

## Visualize It

Watch how a for loop steps through a list, one item at a time:
[Open in Python Tutor](https://pythontutor.com/render.html#code=colors%20%3D%20%5B%22red%22%2C%20%22blue%22%2C%20%22green%22%5D%0Afor%20color%20in%20colors%3A%0A%20%20%20%20print%28color%29%0A%0Acount%20%3D%201%0Awhile%20count%20%3C%3D%203%3A%0A%20%20%20%20print%28count%29%0A%20%20%20%20count%20%2B%3D%201&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

Python has two kinds of loops:

## For loops — "do this for each item"

```python
colors = ["red", "blue", "green"]
for color in colors:
    print(color)
```

Output:
```
red
blue
green
```

The variable `color` takes a different value each time through the loop. First it is `"red"`, then `"blue"`, then `"green"`.

### Looping over numbers with range()

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):    # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (step by 2)
    print(i)
```

## While loops — "keep doing this until something changes"

```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
```

The loop checks the condition (`count <= 5`) before each repetition. When it becomes False, the loop stops.

## When to use which

| Use a **for** loop when... | Use a **while** loop when... |
|---|---|
| You know how many times to repeat | You do not know when to stop |
| You are going through a list | You are waiting for a condition |
| `for item in my_list:` | `while not done:` |

## The walrus operator `:=` in loops (Python 3.8+)

The walrus operator lets you assign a value and use it in the same expression. This is especially useful in `while` loops:

```python
# Without walrus — must call input() in two places:
line = input("Enter text (or 'quit'): ")
while line != "quit":
    print(f"You said: {line}")
    line = input("Enter text (or 'quit'): ")

# With walrus — cleaner:
while (line := input("Enter text (or 'quit'): ")) != "quit":
    print(f"You said: {line}")
```

Reading a file in chunks:

```python
# Read a large file 8KB at a time:
with open("big_file.txt") as f:
    while chunk := f.read(8192):
        process(chunk)
```

The walrus operator assigns the result of the right side to the variable and returns it, so the `while` condition can test the value in the same line.

## Common mistakes

**Forgetting to update the while condition (infinite loop):**
```python
count = 1
while count <= 5:
    print(count)
    # Missing: count = count + 1
    # This loop NEVER ends! Press Ctrl+C to stop it.
```

**Off-by-one errors with range():**
```python
range(5)     # Gives 0,1,2,3,4 — NOT 1,2,3,4,5
range(1, 5)  # Gives 1,2,3,4   — NOT 1,2,3,4,5
range(1, 6)  # Gives 1,2,3,4,5 — this is what you want
```

**Modifying a list while looping over it:**
```python
# WRONG — unpredictable behavior
for item in my_list:
    if item == "bad":
        my_list.remove(item)

# RIGHT — loop over a copy or build a new list
good_items = [item for item in my_list if item != "bad"]
```

## Practice

- [Level 00 / 10 For Loops](../projects/level-00-absolute-beginner/10-for-loops/)
- [Level 00 / 11 While Loops](../projects/level-00-absolute-beginner/11-while-loops/)
- [Level 0 / 05 Number Classifier](../projects/level-0/05-number-classifier/README.md)
- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 0 / 10 Duplicate Line Finder](../projects/level-0/10-duplicate-line-finder/README.md)
- [Level 0 / 11 Simple Menu Loop](../projects/level-0/11-simple-menu-loop/README.md)
- [Level 1 / 05 CSV First Reader](../projects/level-1/05-csv-first-reader/README.md)
- [Level 1 / 12 File Extension Counter](../projects/level-1/12-file-extension-counter/README.md)

**Quick check:** [Take the quiz](quizzes/how-loops-work-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../04_FOUNDATIONS.md) | [Home](../README.md) | [Next →](types-and-conversions.md) |
|:---|:---:|---:|
