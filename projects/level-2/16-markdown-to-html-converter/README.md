# Level 2 / Project 16 - Markdown to HTML Converter
Home: [README](../../../README.md)

## Before You Start

Recall these prerequisites before diving in:
- Can you use `str.startswith()` to check how a line begins?
- Can you use `re.sub(pattern, replacement, text)` to swap matched patterns?

**Estimated time:** 40 minutes

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/files-and-paths.md) | **This project** | --- | [Quiz](../../../concepts/quizzes/files-and-paths-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | --- | — |

<!-- modality-hub-end -->

## Focus
- string parsing line by line with state tracking
- regular expressions for inline pattern replacement
- converting between structured text formats

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Parsing text line by line while tracking state (am I inside a code block? a list?) is the core pattern behind config file readers, log parsers, and template engines. You will build a small but real converter that turns Markdown into HTML, learning how string methods and regex work together to transform structured text.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-2/16-markdown-to-html-converter
python project.py data/sample_input.txt
python project.py data/sample_input.txt --output output.html
pytest -q
```

## Expected terminal output
```text
Converted: data/sample_input.txt -> data/sample_input.html
Output size: 1149 characters
21 passed
```

## Expected artifacts
- An `.html` file generated from the input Markdown
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that converts a simple CSV line into an HTML table row.

**Step 1: Split the line on commas.**

```python
def csv_line_to_tr(line):
    cells = line.strip().split(",")
    cell_html = "".join(f"<td>{cell.strip()}</td>" for cell in cells)
    return f"<tr>{cell_html}</tr>"
```

**Step 2: Test it.** `csv_line_to_tr("name, age, city")` returns `<tr><td>name</td><td>age</td><td>city</td></tr>`.

**Step 3: Handle edge cases.** What if a cell contains a comma inside quotes? The simple `split(",")` breaks down. You would need a smarter parser (like the `csv` module). This is the same lesson the Markdown project teaches: simple parsing works until you hit edge cases, then you need state tracking.

```python
import csv
import io

def csv_line_to_tr_safe(line):
    reader = csv.reader(io.StringIO(line))
    cells = next(reader)
    cell_html = "".join(f"<td>{cell.strip()}</td>" for cell in cells)
    return f"<tr>{cell_html}</tr>"
```

**The thought process:** Start with the simplest approach (split on delimiter). Test it. Discover edge cases. Add state tracking or use a library. This is the same progression you will follow when building the Markdown parser.

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add support for ordered lists (`1. item`, `2. item`) producing `<ol>` and `<li>` tags.
2. Add support for horizontal rules (`---` on its own line) producing `<hr>` tags.
3. Wrap the output in a complete HTML document with `<html>`, `<head>`, and `<body>` tags.

## Break it (required) — Core
1. Feed a file with nested bold inside italic (`*some **bold** here*`) — does it render correctly?
2. Feed a file with an unclosed code block (opening ``` but no closing ```) — what happens?
3. Feed a line that starts with `#` but has no space after it (`#NoSpace`) — does it parse as a heading?

## Fix it (required) — Core
1. Add a guard so `#NoSpace` is treated as a paragraph, not a heading (require space after `#`).
2. Handle unclosed code blocks gracefully by closing them at end of document.
3. Add a test that verifies the unclosed code block behaviour.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the converter process bold (`**`) before italic (`*`) in `convert_inline`?
2. What is a "state machine" and how does the `in_code_block` flag act as one?
3. Why must HTML special characters (`<`, `>`, `&`) be escaped inside code blocks?
4. What is the difference between `re.sub(r"\*(.+?)\*", ...)` (non-greedy) and `re.sub(r"\*(.+)\*", ...)` (greedy)?

## Mastery check
You can move on when you can:
- explain why bold must be parsed before italic and what goes wrong if reversed,
- describe how state tracking (the `in_code_block` flag) changes parsing behaviour,
- add a new Markdown feature (e.g. links or blockquotes) without breaking existing tests,
- explain non-greedy vs. greedy regex matching in your own words.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Strings Work](../../../concepts/how-strings-work.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Markdown to HTML Converter. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to use `re.sub` to match bold text with `**`. Can you explain how non-greedy matching works with a simple example?"
- "Can you explain the difference between `str.startswith` and regex matching for detecting line patterns?"

---

| [← Prev](../15-level2-mini-capstone/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
