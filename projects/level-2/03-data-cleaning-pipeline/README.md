# Level 2 / Project 03 - Data Cleaning Pipeline
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-2.html?ex=3) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you use a set to track items you have already seen? (`seen = set()`)
- Can you chain string methods? (`text.strip().lower().replace(" ", "")`)

**Estimated time:** 30 minutes

## Focus
- standardize text and required fields

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/03-data-cleaning-pipeline
python project.py data/sample_input.txt
python project.py data/sample_input.txt --filter "@.*\."
pytest -q
```

## Expected terminal output
```text
=== Cleaning Stats ===
{"original_count": 10, "cleaned_count": 7, ...}
11 passed
```

## Expected artifacts
- Cleaning stats and cleaned records on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a cleaning step that normalizes phone numbers (strip dashes/parens).
2. Write rejected records to a separate `quarantine.txt` with reasons.
3. Add a `--dry-run` flag that reports stats without writing output.

## Break it (required) — Core
1. Feed a file where every line is whitespace — does it crash or return empty?
2. Use a bad regex pattern in `--filter` (e.g. `[unclosed`) — what happens?
3. Feed records with mixed encodings — does normalise_case break?

## Fix it (required) — Core
1. Wrap `re.compile` in a try/except for invalid regex patterns.
2. Add a test for all-blank input files.
3. Handle encoding errors gracefully with a `try/except UnicodeDecodeError`.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the pipeline run steps in a specific order (strip before dedupe)?
2. How does using a set for deduplication achieve O(1) lookup?
3. What is the difference between `re.search` and `re.match`?
4. Where would you use a data cleaning pipeline in a real data workflow?

## Mastery check
You can move on when you can:
- explain why pipeline step ordering matters,
- describe how sets enable fast deduplication,
- add a new cleaning step without modifying existing ones,
- explain regular expressions used in `filter_by_pattern`.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Data Cleaning Pipeline. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to run cleaning steps in a specific order. Can you explain why the order matters when you strip whitespace before deduplicating?"
- "Can you explain `re.search` vs `re.match` with a simple example?"

---

| [← Prev](../02-nested-data-flattener/README.md) | [Home](../../../README.md) | [Next →](../04-error-safe-divider/README.md) |
|:---|:---:|---:|
