# Level 0 / Project 08 - string Cleaner Starter
Home: [README](../../../README.md)

## Focus
- trim, lowercase, and replace transformations

## Why this project exists
Clean messy strings by stripping whitespace, lowercasing, removing special characters, and collapsing multiple spaces. You will build a multi-step cleaning pipeline and see how order of operations matters.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/08-string-cleaner-starter
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== String Cleaning Results ===

  "   Hello,   World!!!"  =>  "hello world"
  "***URGENT*** Check this NOW!"  =>  "urgent check this now"
  "   spaces   everywhere   in   this   line"  =>  "spaces everywhere in this line"

3 lines cleaned. Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `remove_digits()` step that strips all numeric characters from the string.
2. Add a `--steps` flag that lets the user choose which cleaning steps to apply (e.g. `--steps strip,lower`).
3. Re-run script and tests.

## Break it (required)
1. Feed in a string that is already perfectly clean -- does `clean_string()` return it unchanged?
2. Feed in a string of only special characters like `@#$%^&*` -- does the cleaner return an empty string?
3. Feed in a string with tab characters (`\t`) -- does `collapse_spaces()` handle tabs or only spaces?

## Fix it (required)
1. Ensure `collapse_spaces()` also collapses tabs and other whitespace, not just spaces.
2. Handle the all-special-characters case gracefully (return empty string without error).
3. Add a test for the tab-handling edge case.

## Explain it (teach-back)
1. Why does the cleaning pipeline apply steps in a specific order (strip, then lowercase, then remove specials, then collapse)?
2. What happens if you collapse spaces *before* removing special characters?
3. Why does `isalnum()` keep letters and digits but remove punctuation?
4. Where would string cleaning appear in real software (search indexing, data import, form validation)?

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

| [← Prev](../07-first-file-reader/README.md) | [Home](../../../README.md) | [Next →](../09-daily-checklist-writer/README.md) |
|:---|:---:|---:|
