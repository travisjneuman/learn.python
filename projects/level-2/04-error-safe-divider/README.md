# Level 2 / Project 04 - Error Safe Divider
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-2.html?ex=4) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you write a `try/except` block that catches a specific exception type?
- Can you explain the difference between `ValueError` and `TypeError`?

## Focus
- exception handling and graceful failure

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/04-error-safe-divider
python project.py --input data/sample_input.txt
python project.py --interactive
pytest -q
```

## Expected terminal output
```text
=== Division Results ===
  [OK] 100 / 5 = 20.0
  [FAIL] 10 / 0 = Cannot divide by zero
9 passed
```

## Expected artifacts
- Division results and summary on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add support for integer division (`//`) with a `--integer` flag.
2. Add a `--precision` argument to control decimal places in results.
3. Return results sorted by value (largest first) when `--sorted` is passed.

## Break it (required)
1. Pass `float('inf')` as a numerator — what result do you get?
2. Pass an extremely large number — does Python overflow?
3. Use a file with no valid operations — does the summary crash?

## Fix it (required)
1. Add a check for `float('inf')` and `float('nan')` results.
2. Handle the empty-results case in `summarise_results`.
3. Add tests for infinity and NaN edge cases.

## Explain it (teach-back)
1. What is the difference between `except ValueError` and a bare `except`?
2. Why is catching specific exceptions better than catching `Exception`?
3. How does `try/except/else/finally` work — what runs when?
4. When would error-safe patterns like this be critical in production?

## Mastery check
You can move on when you can:
- list 5 built-in exception types and when each occurs,
- explain exception hierarchy (BaseException vs Exception),
- write a try/except that catches multiple specific types,
- describe why bare `except:` is dangerous.

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

- "I am working on Error Safe Divider. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to understand `try/except/else/finally`. Can you explain what runs in each block with a simple example?"
- "Can you explain the Python exception hierarchy and why catching `Exception` is different from catching `BaseException`?"

---

| [← Prev](../03-data-cleaning-pipeline/README.md) | [Home](../../../README.md) | [Next →](../05-text-report-generator/README.md) |
|:---|:---:|---:|
