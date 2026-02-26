# Level 2 / Project 01 - Dictionary Lookup Service
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-2.html?ex=1) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you use `dict.get(key, default)` to safely look up a key that might not exist?
- Can you write a dictionary comprehension? (`{k: v for k, v in items}`)

**Estimated time:** 30 minutes

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | [Walkthrough](./WALKTHROUGH.md) | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

## Focus
- nested lookup safety and defaults

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/01-dictionary-lookup-service
python project.py --dict data/sample_input.txt --lookup python java haskell
python project.py --dict data/sample_input.txt --stats
pytest -q
```

## Expected terminal output
```text
[{"found": true, "term": "python", "definition": "A high-level ...", ...}, ...]
9 passed
```

## Expected artifacts
- JSON lookup results on stdout
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that looks up country codes (like "US" -> "United States") with fuzzy matching for typos.

**Step 1: Build the lookup dictionary.**

```python
from difflib import get_close_matches

COUNTRIES = {"us": "United States", "uk": "United Kingdom", "ca": "Canada", "de": "Germany"}

def lookup_country(code):
    code_lower = code.strip().lower()
    if code_lower in COUNTRIES:
        return {"found": True, "code": code_lower, "name": COUNTRIES[code_lower]}
    # Try fuzzy matching
    suggestions = get_close_matches(code_lower, COUNTRIES.keys(), n=3, cutoff=0.6)
    return {"found": False, "code": code_lower, "suggestions": suggestions}
```

**Step 2: Test it.** `lookup_country("US")` returns found. `lookup_country("ux")` returns not found, but suggests "us" and "uk".

**Step 3: Handle edge cases.** What if code is empty? `get_close_matches` will not crash, but we should return a clear result.

```python
if not code or not code.strip():
    return {"found": False, "code": "", "suggestions": []}
```

**The thought process:** Normalize input first (lowercase, strip). Try exact match. If that fails, try fuzzy match. Always return a structured result. This is the same pattern the dictionary lookup project uses.

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--case-sensitive` flag that disables lowercase normalisation.
2. Change `get_close_matches` cutoff from 0.6 to 0.5 — observe more suggestions.
3. Add a `--add` option that appends a new `key=value` line to the dictionary file.

## Break it (required) — Core
1. Create a dictionary file with duplicate keys — which value wins?
2. Put a line with multiple `=` signs — does the definition split correctly?
3. Search for an empty string `""` — what happens?

## Fix it (required) — Core
1. Add a guard for empty search terms in `lookup()`.
2. Add a test that verifies duplicate-key behaviour is intentional.
3. Ensure `=` inside definitions is preserved (split on first `=` only).

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the code normalise keys to lowercase?
2. How does `difflib.get_close_matches` decide what is "close"?
3. What is the difference between `str.split("=")` and `str.split("=", 1)`?
4. When would you use a dictionary lookup service in a real codebase?

## Mastery check
You can move on when you can:
- explain how dict comprehensions differ from regular for-loop dict building,
- describe what `try/except KeyError` does vs. `dict.get()`,
- add a new feature (e.g. reverse lookup) without breaking existing tests,
- explain fuzzy matching in your own words.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Dictionary Lookup Service. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to use `difflib.get_close_matches`. Can you explain how the cutoff parameter works with a simple example?"
- "Can you explain the difference between `str.split('=')` and `str.split('=', 1)` with examples?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-nested-data-flattener/README.md) |
|:---|:---:|---:|
