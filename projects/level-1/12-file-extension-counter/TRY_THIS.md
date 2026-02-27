# Try This — Project 12

1. Add a "size by extension" feature that shows not just how many files have each extension, but how much disk space they use in total. Add a `--dir` scan to get real file sizes, then print something like:
   ```text
   .py   5 files   12.4 KB  (50%)
   .txt  3 files    3.1 KB  (30%)
   .md   2 files    1.8 KB  (20%)
   ```
   Hint: use `Path.stat().st_size` to get each file's size in bytes, and accumulate totals in a second dictionary.

2. Add a `--top` flag that only shows the N most common extensions. For example, `--top 3` shows the top 3 extensions and groups everything else under "other":
   ```text
   .py    5 files (50%)  ##########
   .txt   3 files (30%)  ######
   .md    2 files (20%)  ####
   other  1 file         ##
   ```
   Hint: sort by count, slice the first N, and sum the rest into an "other" bucket.

3. Add a `--ignore` flag that skips certain extensions from the count. For example, `--ignore .pyc,.DS_Store` should exclude those files entirely. Also add a built-in "ignore common junk" option that always skips `__pycache__`, `.git`, and `node_modules` directories. Hint: check `Path.parts` to see if any part of the path matches a directory to skip.

---

| [← Prev](../11-command-dispatcher/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../13-batch-rename-simulator/TRY_THIS.md) |
|:---|:---:|---:|
