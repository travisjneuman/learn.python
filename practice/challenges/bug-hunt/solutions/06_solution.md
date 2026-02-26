# Solution: Comparison Traps

## Bug 1 — `is_empty` uses `is` instead of `==` for strings and lists

**Lines:** `if value is ""` and `if value is []`

**Problem:** `is` checks identity (same object in memory), not equality.
`"" is ""` may work for interned strings in some Python implementations, but
`[] is []` is always `False` because each `[]` creates a new list object.

**Fix:**

```python
def is_empty(value):
    if value is None:
        return True
    if value == "":
        return True
    if value == []:
        return True
    return False
```

Or more concisely: `return value is None or value == "" or value == []`

## Bug 2 — `prices_match` fails for floating point comparison

**Problem:** `0.1 + 0.2` does not equal `0.3` in floating point arithmetic.
`0.1 + 0.2 == 0.30000000000000004`. Direct `==` comparison fails.

**Fix:**

```python
def prices_match(price_a, price_b):
    return abs(price_a - price_b) < 1e-9
```

Or use `math.isclose(price_a, price_b)`.

## Bug 3 — `categorize_values` uses `==` which conflates types

**Lines:** `if v == True` and `elif v == False`

**Problem:** `1 == True` is `True` in Python (bool is a subclass of int).
Similarly `0 == False` is `True`. So `1` goes into the truthy bucket via
`== True`, but `"hello"` and `[1, 2]` are truthy values that don't equal
`True`, so they fall through. The elif means values that are falsy but not
`== False` (like `None`, `""`, `[]`) are also missed.

**Fix:** Use `bool(v)` or just truthiness testing:

```python
def categorize_values(values):
    truthy = []
    falsy = []
    for v in values:
        if v:
            truthy.append(v)
        else:
            falsy.append(v)
    return truthy, falsy
```

## Bug 4 — `validate_age` excludes boundary values 0 and 150

**Line:** `if age is not None and 0 < age < 150:`

**Problem:** `0 < age` excludes age 0 (a valid newborn age), and `age < 150`
excludes exactly 150. The spec says "0 and 150 inclusive".

**Fix:**

```python
if age is not None and 0 <= age <= 150:
```
