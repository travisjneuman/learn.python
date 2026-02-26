# Level 2 / Project 06 - Records Deduplicator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | [Walkthrough](./WALKTHROUGH.md) | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

**Estimated time:** 35 minutes

## Focus
- dedupe logic with stable keys

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/06-records-deduplicator
python project.py data/sample_input.txt --keys name email
python project.py data/sample_input.txt --keys email --keep last
python project.py data/sample_input.txt --keys email --show-groups
pytest -q
```

## Expected terminal output
```text
{"total_records": 9, "unique_count": 7, ...}
Unique records (7): ...
9 passed
```

## Expected artifacts
- Dedup results on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--output` flag that writes unique records to a new CSV file.
2. Add a `--case-sensitive` flag that disables lowercase normalisation.
3. Add a count of how many times each duplicate key appeared.

## Break it (required) — Core
1. Use a key field that does not exist in the CSV — what happens?
2. Feed a CSV where every row is identical — is the output correct?
3. Use an empty file — does it crash?

## Fix it (required) — Core
1. Validate that key_fields exist in the headers before processing.
2. Handle the all-duplicates case gracefully.
3. Add a test for missing key fields raising a clear error.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why are sets used for tracking seen keys instead of lists?
2. What is the time complexity of `set.add()` vs `list.append()` for lookups?
3. How does the `keep="last"` mode differ in implementation from `keep="first"`?
4. When would you use deduplication in a real data pipeline?

## Mastery check
You can move on when you can:
- explain O(1) vs O(n) lookup time for sets vs lists,
- implement dedup with configurable key fields from memory,
- describe the difference between exact and fuzzy deduplication,
- add a new keep mode (e.g. "all") without breaking existing tests.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Records Deduplicator. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to use a set to track items I have already seen. Can you explain why sets are faster than lists for membership checks?"
- "Can you explain the difference between `keep='first'` and `keep='last'` deduplication strategies with a simple example?"

---

| [← Prev](../05-text-report-generator/README.md) | [Home](../../../README.md) | [Next →](../07-list-search-benchmark/README.md) |
|:---|:---:|---:|
