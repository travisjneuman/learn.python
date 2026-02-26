# Solution: Off By One

## Bug 1 — `print_roster` skips the first student

**Line:** `for i in range(1, len(students)):`

**Problem:** `range(1, len(students))` starts at index 1, skipping Alice at
index 0. Since the function prints 1-based positions using `i` as both the
position label and the index, the first student is never printed.

**Fix:** Start from 0 and display `i + 1` as the position:

```python
for i in range(len(students)):
    print(f"{i + 1}. {students[i]['name']} — Grade: {students[i]['grade']}")
```

## Bug 2 — `average_grade` divides by wrong number

**Line:** `average = total / len(students) + 1`

**Problem:** Operator precedence makes this `(total / len(students)) + 1`.
The intent was probably `total / (len(students) + 1)`, but the real fix is
simply `total / len(students)` — there is no reason to add 1 at all.

**Fix:**

```python
average = total / len(students)
```

## Bug 3 — `top_student` uses wrong key access

**Line:** `return best[0]`

**Problem:** `best` is a dictionary, not a list. `best[0]` tries to use `0`
as a dictionary key, which raises a `KeyError`. The correct key is `"name"`.

**Fix:**

```python
return best["name"]
```
