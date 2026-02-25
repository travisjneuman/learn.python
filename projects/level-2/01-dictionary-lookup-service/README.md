# Level 2 / Project 01 - Dictionary Lookup Service
Home: [README](../../../README.md)

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

## Alter it (required)
1. Add a `--case-sensitive` flag that disables lowercase normalisation.
2. Change `get_close_matches` cutoff from 0.6 to 0.5 — observe more suggestions.
3. Add a `--add` option that appends a new `key=value` line to the dictionary file.

## Break it (required)
1. Create a dictionary file with duplicate keys — which value wins?
2. Put a line with multiple `=` signs — does the definition split correctly?
3. Search for an empty string `""` — what happens?

## Fix it (required)
1. Add a guard for empty search terms in `lookup()`.
2. Add a test that verifies duplicate-key behaviour is intentional.
3. Ensure `=` inside definitions is preserved (split on first `=` only).

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

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-nested-data-flattener/README.md) |
|:---|:---:|---:|
