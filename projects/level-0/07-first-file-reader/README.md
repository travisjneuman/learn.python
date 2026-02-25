# Level 0 / Project 07 - First File Reader
Home: [README](../../../README.md)

## Focus
- opening and reading plain text safely

## Why this project exists
Read a text file, display its contents with line numbers, and build a summary of line counts, word counts, and file metadata. This is your first hands-on practice with file I/O and Path objects.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/07-first-file-reader
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Contents of sample_input.txt ===

  1 | Welcome to your first file reader!
  2 |
  3 | This file has several lines of text.

=== Summary ===
  Lines:      3 (2 non-empty)
  Words:      14
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--start` and `--end` flag to display only a range of line numbers.
2. Add a `--encoding` flag that lets the user specify the file encoding (default to `utf-8`).
3. Re-run script and tests.

## Break it (required)
1. Point `--input` to a file that does not exist -- does it raise `FileNotFoundError` with a clear message?
2. Use an empty file as input -- does `file_summary()` crash or return zero counts?
3. Use a file with very long lines (1000+ characters) -- does line numbering still align correctly?

## Fix it (required)
1. Ensure `read_file_lines()` raises `FileNotFoundError` with the path in the message.
2. Handle the empty-file case by returning a special "(empty file)" message.
3. Add a test for the empty-file edge case.

## Explain it (teach-back)
1. Why does `format_with_line_numbers()` right-justify the line numbers?
2. What does `path.read_text(encoding="utf-8")` do differently from `open(path).read()`?
3. Why track non-empty lines separately in `file_summary()`?
4. Where would file reading with metadata appear in real software (log viewers, code editors, diff tools)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

| [← Prev](../06-word-counter-basic/README.md) | [Home](../../../README.md) | [Next →](../08-string-cleaner-starter/README.md) |
|:---|:---:|---:|
