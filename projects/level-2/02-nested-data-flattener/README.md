# Level 2 / Project 02 - Nested Data Flattener
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-2.html?ex=2) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you use `isinstance()` to check if a value is a dict or a list?
- Can you explain what recursion is? (A function that calls itself)

## Focus
- flatten lists/dicts to row structures

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/02-nested-data-flattener
python project.py data/sample_input.txt
python project.py data/sample_input.txt --separator /
pytest -q
```

## Expected terminal output
```text
{"server.host": "localhost", "server.port": 8080, ...}
9 passed
```

## Expected artifacts
- Flattened JSON on stdout
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that flattens a nested list into a single list. `[1, [2, [3, 4]], 5]` becomes `[1, 2, 3, 4, 5]`.

**Step 1: Think recursively.** For each item: if it is a list, flatten it. If it is not a list, add it to the result.

```python
def flatten_list(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))  # recurse
        else:
            result.append(item)
    return result
```

**Step 2: Trace it on paper.** `flatten_list([1, [2, [3]]])`:
- item `1`: not a list, append. result = `[1]`
- item `[2, [3]]`: is a list, recurse:
  - item `2`: not a list, append. result = `[2]`
  - item `[3]`: is a list, recurse:
    - item `3`: not a list, append. result = `[3]`
  - extend with `[3]`. result = `[2, 3]`
- extend with `[2, 3]`. result = `[1, 2, 3]`

**The thought process:** Recursion handles arbitrary nesting depth because each level calls the same function. The dict flattener project uses the same approach but builds dot-separated keys instead of a flat list.

## Alter it (required)
1. Add a `--max-depth` flag that stops flattening beyond N levels.
2. Change the separator to `__` (double underscore) and observe the output.
3. Add a `--keys-only` flag that prints just the flattened key names.

## Break it (required)
1. Pass a JSON file whose root is a list `[1, 2, 3]` — what error appears?
2. Create a key that already contains a dot, e.g. `{"a.b": 1}` — what happens?
3. Flatten then unflatten a structure with lists — is the roundtrip perfect?

## Fix it (required)
1. Add a guard in `flatten_from_file` for non-dict JSON roots.
2. Handle keys that contain the separator character (escape or warn).
3. Add a test for empty dict input `{}`.

## Explain it (teach-back)
1. What is recursion and why is it useful for nested data?
2. How does `isinstance(value, dict)` decide the recursion path?
3. Why might flattening lose information about list vs. dict structure?
4. Where would you use flatten/unflatten in real DevOps or data pipelines?

## Mastery check
You can move on when you can:
- trace the recursion for a 3-level nested dict on paper,
- explain the difference between `dict.update()` and `dict[key] = value`,
- add support for a new data type (e.g. sets) without breaking existing tests,
- describe when flattening is useful vs. when it loses information.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Nested Data Flattener. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to understand recursion. Can you trace through a recursive function call step by step, using a simple example like factorial?"
- "Can you explain how `isinstance(value, dict)` works and when to use it instead of `type(value) == dict`?"

---

| [← Prev](../01-dictionary-lookup-service/README.md) | [Home](../../../README.md) | [Next →](../03-data-cleaning-pipeline/README.md) |
|:---|:---:|---:|
