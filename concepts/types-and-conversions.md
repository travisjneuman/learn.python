# Types and Conversions

Every value in Python has a type. The type determines what you can do with it.

## Visualize It

See how type conversions change values and what happens when they fail:
[Open in Python Tutor](https://pythontutor.com/render.html#code=x%20%3D%20%2242%22%0Aprint%28type%28x%29%29%0A%0Ay%20%3D%20int%28x%29%0Aprint%28type%28y%29%29%0Aprint%28y%20%2B%201%29%0A%0Az%20%3D%20float%28%223.14%22%29%0Aprint%28z%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

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

## Practice

- [Level 00 / 05 Numbers and Math](../projects/level-00-absolute-beginner/05-numbers-and-math/)
- [Level 00 / 07 User Input](../projects/level-00-absolute-beginner/07-user-input/)
- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)
- [Level 0 / 03 Temperature Converter](../projects/level-0/03-temperature-converter/README.md)
- [Level 0 / 04 Yes No Questionnaire](../projects/level-0/04-yes-no-questionnaire/README.md)
- [Level 0 / 08 String Cleaner Starter](../projects/level-0/08-string-cleaner-starter/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 02 Password Strength Checker](../projects/level-1/02-password-strength-checker/README.md)

**Quick check:** [Take the quiz](quizzes/types-and-conversions-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](how-loops-work.md) | [Home](../README.md) | [Next →](functions-explained.md) |
|:---|:---:|---:|
