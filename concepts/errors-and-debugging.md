# Errors and Debugging

> **Try This First:** Before reading, try running `print(1/0)` in Python. What happens? Read the error message -- it tells you exactly what went wrong.

Errors are not failures. They are Python telling you exactly what went wrong and where. Learning to read error messages is one of the most valuable skills in programming.

## Visualize It

See what happens when Python hits an error — watch the execution stop:
[Open in Python Tutor](https://pythontutor.com/render.html#code=x%20%3D%2010%0Ay%20%3D%200%0Aprint%28%22before%22%29%0Aresult%20%3D%20x%20%2F%20y%0Aprint%28%22after%22%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## Anatomy of an error message

```
Traceback (most recent call last):
  File "exercise.py", line 5, in <module>
    print(score)
NameError: name 'score' is not defined
```

Read it bottom-up:
1. **`NameError: name 'score' is not defined`** — what went wrong
2. **`File "exercise.py", line 5`** — where it happened
3. **`print(score)`** — the exact line that caused it

## Common error types

| Error | Meaning | Example |
|-------|---------|---------|
| `SyntaxError` | Python cannot understand your code | Missing colon, unmatched quotes |
| `NameError` | You used a name that does not exist | Typo in variable name |
| `TypeError` | Wrong type for the operation | Adding a string and a number |
| `IndexError` | List index out of range | `my_list[99]` when list has 5 items |
| `KeyError` | Dict key does not exist | `my_dict["missing_key"]` |
| `FileNotFoundError` | File does not exist at that path | Wrong filename or directory |
| `ValueError` | Right type but wrong value | `int("hello")` |
| `IndentationError` | Indentation is inconsistent | Mixed tabs and spaces |

## Debugging strategy

When something goes wrong:

1. **Read the error message.** It usually tells you exactly what happened.
2. **Look at the line number.** Go to that line in your file.
3. **Check spelling.** Typos in variable names cause `NameError`.
4. **Print things.** Add `print(variable_name)` before the error line to see what values actually are.
5. **Simplify.** Remove code until you find the smallest version that still breaks.

## The print() debugging method

The simplest debugging technique: print values to see what is happening.

```python
data = load_file("input.txt")
print("data is:", data)          # What did we actually load?
print("type is:", type(data))    # Is it a list? a string? None?
print("length is:", len(data))   # How many items?

for item in data:
    print("processing:", item)   # See each item as it is processed
```

## Common mistakes and fixes

**SyntaxError — missing colon:**
```python
if x > 5       # Missing colon!
    print("big")

if x > 5:      # Fixed
    print("big")
```

**TypeError — mixing strings and numbers:**
```python
age = 30
print("I am " + age)           # Error! Cannot add string + int
print("I am " + str(age))      # Fixed with str()
print(f"I am {age}")           # Better — use f-string
```

**IndentationError:**
```python
if True:
print("hello")     # Error! Must be indented

if True:
    print("hello") # Fixed — 4 spaces of indentation
```

## Practice

- [Level 00 / 08 Making Decisions](../projects/level-00-absolute-beginner/08-making-decisions/)
- [Level 00 / 14 Reading Files](../projects/level-00-absolute-beginner/14-reading-files/)
- [Level 00 / 15 Putting It Together](../projects/level-00-absolute-beginner/15-putting-it-together/)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 08 Path Exists Checker](../projects/level-1/08-path-exists-checker/README.md)
- [Level 1 / 11 Command Dispatcher](../projects/level-1/11-command-dispatcher/README.md)
- [Level 2 / 04 Error Safe Divider](../projects/level-2/04-error-safe-divider/README.md)
- [Level 2 / 11 Retry Loop Practice](../projects/level-2/11-retry-loop-practice/README.md)

**Quick check:** [Take the quiz](quizzes/errors-and-debugging-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../09_QUALITY_TOOLING.md) | [Home](../README.md) | [Next →](the-terminal-deeper.md) |
|:---|:---:|---:|
