# Errors and Debugging

Errors are not failures. They are Python telling you exactly what went wrong and where. Learning to read error messages is one of the most valuable skills in programming.

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

## Related exercises
- [Level 00, Exercise 08 — Making Decisions](../projects/level-00-absolute-beginner/08-making-decisions/) (introduces error patterns)
- [Level 00, Exercise 14 — Reading Files](../projects/level-00-absolute-beginner/14-reading-files/) (FileNotFoundError)

---

## Practice This

- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 11 Command Dispatcher](../projects/level-1/11-command-dispatcher/README.md)
- [Level 10 / 01 Enterprise Python Blueprint](../projects/level-10/01-enterprise-python-blueprint/README.md)
- [Level 10 / 02 Autonomous Run Orchestrator](../projects/level-10/02-autonomous-run-orchestrator/README.md)
- [Level 10 / 03 Policy As Code Validator](../projects/level-10/03-policy-as-code-validator/README.md)
- [Level 10 / 04 Multi Tenant Data Guard](../projects/level-10/04-multi-tenant-data-guard/README.md)
- [Level 10 / 05 Compliance Evidence Builder](../projects/level-10/05-compliance-evidence-builder/README.md)
- [Level 10 / 06 Resilience Chaos Workbench](../projects/level-10/06-resilience-chaos-workbench/README.md)
- [Level 10 / 07 High Risk Change Gate](../projects/level-10/07-high-risk-change-gate/README.md)
- [Level 10 / 08 Zero Downtime Migration Lab](../projects/level-10/08-zero-downtime-migration-lab/README.md)

**Quick check:** [Take the quiz](quizzes/errors-and-debugging-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../09_QUALITY_TOOLING.md) | [Home](../README.md) | [Next →](the-terminal-deeper.md) |
|:---|:---:|---:|
