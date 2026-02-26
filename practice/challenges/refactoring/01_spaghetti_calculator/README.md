# Refactoring 01 — Spaghetti Calculator

Open `messy.py`. This is a working arithmetic expression evaluator. It parses strings like `"3 + 4 * (2 - 1)"` and returns the correct result.

The code works. But it is nearly unreadable: single-letter variable names, cryptic function names, magic numbers, no error handling, and no documentation.

## Your mission

Refactor this code so that a teammate could read it and understand what it does. The tests in `tests/test_messy.py` must pass before and after every change you make.

## Refactoring goals

1. **Rename everything.** Replace `_p`, `_t`, `_f`, `s`, `r`, `v`, `n`, `d`, `j`, `i` with descriptive names. What do these functions actually do? What do these variables hold?

2. **Extract constants.** The magic value `99999999` for division by zero is a code smell. Raise a `ZeroDivisionError` instead.

3. **Add error handling.** What happens with malformed input like `"3 + + 4"` or `"(3 + 4"` (unmatched parenthesis)? After refactoring, these should raise a clear `ValueError`.

4. **Add type hints.** Every function should have type annotations on its parameters and return value.

5. **Add docstrings.** Every function should have a one-line docstring explaining what it does.

## Process

```
1. Run tests           ->  all pass (baseline)
2. Rename one thing    ->  run tests  ->  all pass
3. Rename another      ->  run tests  ->  all pass
4. Extract constant    ->  run tests  ->  all pass
5. Add error handling  ->  run tests  ->  all pass (add new tests too)
6. Add type hints      ->  run tests  ->  all pass
7. Add docstrings      ->  done
```

## What you are practicing

- Reading and understanding code with poor naming
- Systematic refactoring (one small change at a time)
- Keeping tests green throughout
- Choosing good names for functions and variables
