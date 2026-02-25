# Level 0 / Project 15 - Level 0 Mini Toolkit
Home: [README](../../../README.md)

## Focus
- combine basics into one tiny utility

## Why this project exists
Combine everything from Level 0 into one multi-tool CLI. Choose between word counting, duplicate detection, and string cleaning -- all in a single script. This capstone shows how small functions compose into larger programs.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/15-level0-mini-toolkit
python project.py --input data/sample_input.txt --tool all
pytest -q
```

## Expected terminal output
```text
=== Mini Toolkit (all) ===

  [wordcount] 5 lines, 18 words
  [duplicates] 2 duplicate lines found
  [clean] 5 lines cleaned

Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a fourth tool: "reverse" that reverses the order of lines in the file.
2. Add an `--all` flag that runs every tool and combines results into one report.
3. Re-run script and tests.

## Break it (required)
1. Pass `--tool unknown_tool` -- does `run_tool()` raise `ValueError` with a helpful message?
2. Use an empty file as input -- do all three tools handle it without crashing?
3. Pass no `--tool` flag at all -- what is the default behaviour?

## Fix it (required)
1. Ensure `run_tool()` raises `ValueError` listing the valid tool names.
2. Handle empty-file input gracefully for each tool (return zero counts, empty list, unchanged string).
3. Add a test for the unknown-tool error message.

## Explain it (teach-back)
1. Why does `run_tool()` use an if/elif chain instead of a dict mapping tool names to functions?
2. What does `run_all_tools()` demonstrate about combining small functions into larger workflows?
3. Why is the `--tool` argument a `choices` list in argparse?
4. Where would multi-tool CLIs appear in real software (git, docker, kubectl)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

| [← Prev](../14-line-length-summarizer/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
