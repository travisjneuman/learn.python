# Level 0 / Project 06 - Word Counter Basic
Home: [README](../../../README.md)

## Focus
- string splitting and counting

## Why this project exists
Count words, lines, and characters in a text file, then find the most frequent words. You will practise string splitting, dictionary-based counting, and building summary statistics.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/06-word-counter-basic
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Word Count Summary ===
  Lines:      3
  Words:      22
  Characters: 156
  Unique:     17

  Top words:
    python     3
    language   2
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add an "average word length" metric to `analyse_text()`.
2. Add a `--top` flag that controls how many top words to display (default 5).
3. Re-run script and tests.

## Break it (required)
1. Use an empty file as input -- does `analyse_text()` crash on division by zero?
2. Use a file with only punctuation like `!!! ??? ...` -- are those counted as words?
3. Use a file with unicode characters like emojis -- does `count_characters()` count them correctly?

## Fix it (required)
1. Add a guard for empty text that returns zero counts without dividing.
2. Ensure `word_frequencies()` strips punctuation before counting so `"hello!"` and `"hello"` are the same word.
3. Add a test for the empty-text edge case.

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

| [← Prev](../05-number-classifier/README.md) | [Home](../../../README.md) | [Next →](../07-first-file-reader/README.md) |
|:---|:---:|---:|
