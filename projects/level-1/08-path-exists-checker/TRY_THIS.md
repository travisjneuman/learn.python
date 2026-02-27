# Try This — Project 08

1. Add a "total size" summary that adds up the sizes of all files found and prints it in a human-readable format at the bottom of the report. Use the `format_size()` function that already exists in the project:
   ```text
   Total size of existing files: 2.3 MB (across 5 files)
   ```

2. Add a `--type` filter flag that shows only files with a specific extension. For example, `--type .py` should show only Python files. Also show how many files were skipped because they did not match:
   ```text
   Showing only .py files:
     FILE  src/main.py  (1.2 KB)
     FILE  src/utils.py (0.8 KB)

   2 shown, 4 skipped (non-.py)
   ```
   Hint: use `Path.suffix` to check each file's extension.

3. Add a `--scan` mode that takes a directory path instead of a file list. It should recursively list all files and subdirectories, grouped by directory. Use `Path.rglob("*")` to walk the tree:
   ```text
   data/
     sample_input.txt   (0.1 KB)
     output.json        (0.3 KB)
   tests/
     test_project.py    (1.5 KB)
   ```

---

| [← Prev](../07-date-difference-helper/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../09-json-settings-loader/TRY_THIS.md) |
|:---|:---:|---:|
