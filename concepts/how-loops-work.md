# How Loops Work

A loop repeats code. Instead of writing the same thing 100 times, you write it once and let the loop handle repetition.

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

## Related exercises
- [Level 00, Exercise 10 — For Loops](../projects/level-00-absolute-beginner/10-for-loops/)
- [Level 00, Exercise 11 — While Loops](../projects/level-00-absolute-beginner/11-while-loops/)

---

## Practice This

- [Module: Elite Track / 07 Observability Slo Platform](../projects/elite-track/07-observability-slo-platform/README.md)
- [Level 0 / 01 Terminal Hello Lab](../projects/level-0/01-terminal-hello-lab/README.md)
- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)
- [Level 0 / 03 Temperature Converter](../projects/level-0/03-temperature-converter/README.md)
- [Level 0 / 04 Yes No Questionnaire](../projects/level-0/04-yes-no-questionnaire/README.md)
- [Level 0 / 05 Number Classifier](../projects/level-0/05-number-classifier/README.md)
- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 0 / 08 String Cleaner Starter](../projects/level-0/08-string-cleaner-starter/README.md)
- [Level 0 / 09 Daily Checklist Writer](../projects/level-0/09-daily-checklist-writer/README.md)

**Quick check:** [Take the quiz](quizzes/how-loops-work-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)
