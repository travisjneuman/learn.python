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
python project.py
pytest -q
```

The program asks you to enter a file path, then displays its contents with line numbers.

## Expected terminal output
```text
=== File Reader ===
Enter a file path to read (e.g. data/sample_input.txt): data/sample_input.txt

=== Contents of sample_input.txt ===

  1 | Welcome to your first file reader!
  2 |
  3 | This file has several lines of text.

=== Summary ===
  Lines:      3 (2 non-empty)
  Words:      14
  Characters: 57
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Ask the user for a start and end line number to display only a range of the file.
2. After showing the summary, ask "Read another file? (y/n): " and loop if yes.
3. Re-run script and tests.

## Break it (required)
1. Enter a file path that does not exist -- does it show a clear error or crash?
2. Create an empty file and read it -- does `file_summary()` crash or return zero counts?
3. Read a file with very long lines (1000+ characters) -- does line numbering still align correctly?

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
