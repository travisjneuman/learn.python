# Level 0 / Project 06 - Word Counter Basic
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/errors-and-debugging.md) | **This project** | — | [Quiz](../../../concepts/quizzes/errors-and-debugging-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/errors-and-debugging.md) | [Browser](../../../browser/level-0.html) |

<!-- modality-hub-end -->

**Estimated time:** 20 minutes

## Focus
- string splitting and counting

## Why this project exists
Count words, lines, and characters in a text file, then find the most frequent words. You will practise string splitting, dictionary-based counting, and building summary statistics.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/06-word-counter-basic
python project.py
pytest -q
```

Type or paste text, then press Enter on a blank line to see the analysis.

## Expected terminal output
```text
=== Word Counter ===
Type or paste text below. Enter a blank line when done.

Python is a great language.
Python is easy to learn.
Python is powerful and fun.

=== Word Count Summary ===
  Lines:      3
  Words:      16
  Characters: 80
  Unique:     11

  Top words:
    python: 3
    is: 3
    a: 1
    great: 1
    language: 1
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add an "average word length" metric to `analyse_text()`.
2. Ask the user "How many top words to show? " and use that number instead of the default 5.
3. Re-run script and tests.

## Break it (required) — Core
1. Enter no text (just press Enter immediately) -- does `analyse_text()` crash?
2. Enter only punctuation like `!!! ??? ...` -- are those counted as words?
3. Enter unicode characters like emojis -- does `count_characters()` count them correctly?

## Fix it (required) — Core
1. Add a guard for empty text that returns zero counts without dividing.
2. Ensure `word_frequencies()` strips punctuation before counting so `"hello!"` and `"hello"` are the same word.
3. Add a test for the empty-text edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `word_frequencies()` use `.lower()` before counting?
2. What does `dict.get(key, 0) + 1` do and why is it better than checking `if key in dict`?
3. Why separate `count_words()`, `count_lines()`, and `count_characters()` into their own functions?
4. Where would word counting appear in real software (search engines, document analysis, readability scores)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Word Counter Basic. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to count word frequencies using a dictionary. Can you show me how `dict.get(key, 0)` works with a simple example that is not about words?"
- "Can you explain the difference between `.split()` and `.split(' ')` with examples?"

---

| [← Prev](../05-number-classifier/README.md) | [Home](../../../README.md) | [Next →](../07-first-file-reader/README.md) |
|:---|:---:|---:|
