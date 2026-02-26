# Module 02 / Project 04 -- File Processor CLI

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Building a practical CLI that does real work on files
- Using `rich.progress` for progress bars
- File globbing with `pathlib.Path.glob()`
- Writing structured output to a report file

## Why this project exists

The previous projects taught you Click's API in isolation. This project puts it all together into something you could actually use: a tool that scans a directory of text files, computes statistics (word count, longest line, average line length), and shows a progress bar while it works. It also introduces the Rich library, which is the standard for beautiful terminal output in Python.

## Run

```bash
cd projects/modules/02-cli-tools/04-file-processor-cli

# Process the sample data files
python project.py --directory data

# Process and save a report
python project.py --directory data --output report.txt

# Process only .txt files (the default)
python project.py --directory data --pattern "*.txt"
```

## Expected output

```text
$ python project.py --directory data
Processing files...
 ━━━━━━━━━━━━━━━━━━━━ 100% 3/3

Results:
────────────────────────────────
sample1.txt
  Words: 52   Longest line: 68 chars   Avg line length: 38.2 chars

sample2.txt
  Words: 41   Longest line: 55 chars   Avg line length: 32.7 chars

sample3.txt
  Words: 67   Longest line: 72 chars   Avg line length: 41.5 chars

────────────────────────────────
Total files: 3
Total words: 160
```

(Exact numbers depend on the sample files.)

## Alter it

1. Add a `--sort` option that sorts results by word count (ascending or descending).
2. Add a `--min-words` filter that only includes files with at least N words in the report.
3. Add a `--verbose` flag that also prints the first line of each file as a preview.

## Break it

1. Point `--directory` at a folder that does not exist. What happens?
2. Put a binary file (like a `.png`) in the data folder and run the processor. What error do you get?
3. Remove the `rich` import and try to run the script. How does the error message help you diagnose the issue?

## Fix it

1. Add a check for missing directories and print a helpful error before crashing.
2. Wrap the file-reading code in a try/except that skips binary or unreadable files with a warning.
3. Reinstall `rich` (`pip install rich`) and confirm the progress bar reappears.

## Explain it

1. What does `pathlib.Path.glob("*.txt")` return and how is it different from `os.listdir()`?
2. How does `rich.progress.track()` know when to update the progress bar?
3. Why is it better to pass `--directory` as an option than to hardcode a path?
4. What would you change to make this tool handle thousands of files efficiently?

## Mastery check

You can move on when you can:
- use `Path.glob()` to find files matching a pattern,
- add a Rich progress bar to any loop,
- write a CLI that reads from a directory and writes a report,
- handle missing or unreadable files without crashing.

---

## Related Concepts

- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Files and Paths](../../../../concepts/quizzes/files-and-paths-quiz.py)

## Next

Continue to [05 - Typer Migration](../05-typer-migration/).
