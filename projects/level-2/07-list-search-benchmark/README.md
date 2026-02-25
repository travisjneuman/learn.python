# Level 2 / Project 07 - List Search Benchmark
Home: [README](../../../README.md)

## Focus
- compare search approaches

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/07-list-search-benchmark
python project.py --sizes 100 1000 10000
python project.py --sizes 100 1000 10000 --json
pytest -q
```

## Expected terminal output
```text
=== Search Algorithm Benchmark ===
    Size | Linear(hit) | Binary(hit) | Set(hit) ...
10 passed
```

## Expected artifacts
- Benchmark timing table on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--sorted-linear` variant that searches sorted data linearly with early exit.
2. Add a "speedup" column showing how many times faster binary is vs linear.
3. Plot the results to a text-based bar chart (just using `#` characters).

## Break it (required)
1. Run binary search on UNSORTED data — does it still find elements?
2. Pass a size of 0 — does the benchmark handle an empty list?
3. Use 1 iteration — are the timings meaningful?

## Fix it (required)
1. Add a guard that validates data is sorted before binary search.
2. Handle size=0 gracefully in `generate_test_data`.
3. Add a minimum iteration count warning.

## Explain it (teach-back)
1. What does O(n) vs O(log n) mean in plain language?
2. Why must binary search data be sorted first?
3. Why is set lookup O(1) but building the set is O(n)?
4. When would you choose each search method in practice?

## Mastery check
You can move on when you can:
- implement binary search from memory,
- explain why halving the search space gives O(log n),
- predict which algorithm wins for different use cases,
- describe the trade-off between sort cost and search speed.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../06-records-deduplicator/README.md) | [Home](../../../README.md) | [Next →](../08-mini-inventory-engine/README.md) |
|:---|:---:|---:|
