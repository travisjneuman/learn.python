# Types and Conversions

Every value in Python has a type. The type determines what you can do with it.

## Basic types

| Type | What it holds | Examples |
|------|--------------|---------|
| `str` | Text (string) | `"hello"`, `'world'`, `"123"` |
| `int` | Whole number | `42`, `-3`, `0` |
| `float` | Decimal number | `3.14`, `-0.5`, `2.0` |
| `bool` | True or False | `True`, `False` |
| `None` | Nothing / empty | `None` |

## Checking a type

```python
print(type("hello"))   # <class 'str'>
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type(True))      # <class 'bool'>
```

## Converting between types

| Function | Converts to | Example |
|----------|------------|---------|
| `str()` | String | `str(42)` → `"42"` |
| `int()` | Integer | `int("42")` → `42` |
| `float()` | Float | `float("3.14")` → `3.14` |
| `bool()` | Boolean | `bool(0)` → `False` |

### Why conversion matters

`input()` always returns a string. If you want to do math with it, you must convert:

```python
age_text = input("Age? ")     # User types 30 → age_text is "30" (string)
age = int(age_text)            # Convert to integer
print(age + 1)                 # 31 (math works now)
```

Without conversion:
```python
print("30" + 1)  # TypeError: can only concatenate str to str
```

## Truthy and falsy values

Python treats some values as True and others as False in conditions:

**Falsy (treated as False):**
- `False`, `0`, `0.0`, `""` (empty string), `[]` (empty list), `{}` (empty dict), `None`

**Truthy (treated as True):**
- Everything else: `True`, any non-zero number, any non-empty string/list/dict

```python
name = ""
if name:
    print("Has a name")
else:
    print("No name")      # This runs because "" is falsy
```

## Common mistakes

**Comparing different types:**
```python
"5" == 5     # False! String "5" is not the same as integer 5
int("5") == 5  # True — convert first
```

**Converting non-numeric strings:**
```python
int("hello")   # ValueError: invalid literal
int("3.14")    # ValueError: cannot convert float string to int directly
float("3.14")  # 3.14 — use float() for decimal strings
```

## Related exercises
- [Level 00, Exercise 05 — Numbers and Math](../projects/level-00-absolute-beginner/05-numbers-and-math/)
- [Level 00, Exercise 07 — User Input](../projects/level-00-absolute-beginner/07-user-input/) (string to number conversion)

---

## Practice This

- [Module: Elite Track / 03 Distributed Cache Simulator](../projects/elite-track/03-distributed-cache-simulator/README.md)
- [Module: Elite Track / 09 Open Source Maintainer Simulator](../projects/elite-track/09-open-source-maintainer-simulator/README.md)
- [Level 0 / 01 Terminal Hello Lab](../projects/level-0/01-terminal-hello-lab/README.md)
- [Level 0 / 04 Yes No Questionnaire](../projects/level-0/04-yes-no-questionnaire/README.md)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 0 / 08 String Cleaner Starter](../projects/level-0/08-string-cleaner-starter/README.md)
- [Level 0 / 13 Alarm Message Generator](../projects/level-0/13-alarm-message-generator/README.md)
- [Level 1 / 02 Password Strength Checker](../projects/level-1/02-password-strength-checker/README.md)
- [Level 2 / 02 Nested Data Flattener](../projects/level-2/02-nested-data-flattener/README.md)
- [Level 3 / 03 Logging Baseline Tool](../projects/level-3/03-logging-baseline-tool/README.md)

**Quick check:** [Take the quiz](quizzes/types-and-conversions-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](how-loops-work.md) | [Home](../README.md) | [Next →](functions-explained.md) |
|:---|:---:|---:|
