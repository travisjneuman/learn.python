# What is a Variable?

> **Try This First:** Before reading, open Python and type `x = 5` then `print(x)`. Now type `x = "hello"` then `print(x)`. Notice how `x` changed? That is what a variable does.

A variable is a name that holds a value. You create it by writing a name, then `=`, then the value.

```python
name = "Alice"
age = 30
is_student = True
```

## Visualize It

See how Python stores variables in memory step by step:
[Open in Python Tutor](https://pythontutor.com/render.html#code=name%20%3D%20%22Alice%22%0Aage%20%3D%2030%0Anext_year%20%3D%20age%20%2B%201%0Aname%20%3D%20%22Bob%22%0Aprint%28name%2C%20next_year%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

Think of it like a labeled jar. The label is the name. The contents are the value. You can:
- **Look at** the contents: `print(name)` shows `Alice`
- **Replace** the contents: `name = "Alice"` — now it holds `"Alice"`
- **Use** the contents in calculations: `next_year = age + 1`

## Rules for naming variables
- Must start with a letter or underscore (not a number)
- Can contain letters, numbers, and underscores
- Case-sensitive: `Name` and `name` are different variables
- Convention: use `lowercase_with_underscores` (called "snake_case")

## Good names vs bad names

```python
# Good — describes what the value represents
student_count = 42
max_temperature = 98.6
is_active = True

# Bad — vague or misleading
x = 42
temp = 98.6  # temp... temperature? temporary?
flag = True  # flag for what?
```

## Common mistakes

**Using = instead of ==:**
```python
x = 5       # This STORES 5 in x
x == 5      # This CHECKS if x equals 5 (returns True or False)
```

**Forgetting quotes for text:**
```python
name = Alice    # Error! Python thinks Alice is a variable name
name = "Alice"  # Correct — quotes make it text (a string)
```

**Using a variable before creating it:**
```python
print(score)     # Error! score does not exist yet
score = 100      # This line creates it
print(score)     # Now it works
```

## Practice

- [Level 00 / 04 Variables](../projects/level-00-absolute-beginner/04-variables/)
- [Level 00 / 05 Numbers and Math](../projects/level-00-absolute-beginner/05-numbers-and-math/)
- [Level 00 / 06 Strings and Text](../projects/level-00-absolute-beginner/06-strings-and-text/)
- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)

**Quick check:** [Take the quiz](quizzes/what-is-a-variable-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../03_SETUP_ALL_PLATFORMS.md) | [Home](../README.md) | [Next →](../projects/level-00-absolute-beginner/README.md) |
|:---|:---:|---:|
