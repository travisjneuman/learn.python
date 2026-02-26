# Solution: Mutable Defaults

## Bug 1 — Mutable default argument in `create_student`

**Line:** `def create_student(name, courses=[]):`

**Problem:** The default `[]` is created once when the function is defined.
Every call that uses the default shares the same list object. Adding a course
to Alice also adds it to Bob.

**Fix:**

```python
def create_student(name, courses=None):
    return {"name": name, "courses": courses if courses is not None else []}
```

## Bug 2 — `merge_students` mutates `student_a`

**Line:** `merged = student_a`

**Problem:** `merged = student_a` does not copy the dictionary — both names
point to the same object. Modifying `merged["name"]` also changes
`student_a["name"]`.

**Fix:**

```python
def merge_students(student_a, student_b):
    merged = {
        "name": f"{student_a['name']} & {student_b['name']}",
        "courses": student_a["courses"] + student_b["courses"],
    }
    return merged
```

## Bug 3 — `build_lookup` uses a list as a dict key

**Line:** `lookup[s["courses"]] = len(s["courses"])`

**Problem:** `s["courses"]` is a list, and lists are unhashable — they cannot
be dictionary keys. This raises `TypeError: unhashable type: 'list'`.

**Fix:** Use the student name as the key:

```python
lookup[s["name"]] = len(s["courses"])
```
