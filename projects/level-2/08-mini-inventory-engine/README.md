# Level 2 / Project 08 - Mini Inventory Engine
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/collections-explained.md) | **This project** | — | [Quiz](../../../concepts/quizzes/collections-explained-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/collections-explained.md) | [Browser](../../../browser/level-2.html) |

<!-- modality-hub-end -->

**Estimated time:** 40 minutes

## Focus
- stock add/remove and reorder alerts

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/08-mini-inventory-engine
python project.py --inventory data/sample_input.txt
python project.py --inventory data/sample_input.txt --low-stock
python project.py --inventory data/sample_input.txt --value
python project.py --inventory data/sample_input.txt --search "key"
pytest -q
```

## Expected terminal output
```text
Inventory (10 products):
  bolt: qty=500, $0.50, hardware
  ...
12 passed
```

## Expected artifacts
- Inventory listing on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--remove` command: `--remove "Widget" 5` to decrease stock.
2. Add an `--export` flag that writes current inventory to a new CSV.
3. Add a `--category` filter to show only items in a specific category.

## Break it (required) — Core
1. Add an item with negative quantity — is it allowed?
2. Remove exactly all stock of an item — does it stay at 0 or get deleted?
3. Load a CSV with non-numeric price values — what happens?

## Fix it (required) — Core
1. Add validation that quantity and price must be non-negative.
2. Decide and document what happens when stock reaches 0.
3. Handle CSV parsing errors with try/except and skip bad rows.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why is the inventory stored as a dict-of-dicts instead of a list?
2. How does `dict.get(key, default)` help avoid KeyError?
3. What is the difference between mutating a dict vs returning a new one?
4. Where would this pattern be used in a real e-commerce system?

## Mastery check
You can move on when you can:
- implement add/remove/search from memory,
- explain how nested dicts model real-world entities,
- add a new feature (e.g. price history) without breaking existing code,
- describe why the function returns a result dict instead of raising exceptions.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../07-list-search-benchmark/README.md) | [Home](../../../README.md) | [Next →](../09-config-driven-calculator/README.md) |
|:---|:---:|---:|
