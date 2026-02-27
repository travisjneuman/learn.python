# Try This — Project 13

1. Add a new rule: `number` that adds a sequential number prefix to each filename. The first file becomes `001_filename.txt`, the second `002_filename.txt`, and so on. You will need to change `simulate_batch()` slightly because this rule depends on the file's position in the list, not just its name. Hint: use `enumerate()` and `str.zfill(3)` to zero-pad the number.

2. Add a `--chain` flag that applies multiple rules in sequence. For example, `--chain lower,replace_spaces` should first lowercase the filename, then replace spaces with underscores:
   ```text
   My Report (Final).docx
     lower           => my report (final).docx
     replace_spaces  => my_report_(final).docx
   ```
   Show the intermediate result after each rule so the user can see the transformation step by step.

3. Add an `--apply` flag that actually renames files on disk (not just a simulation). But add a safety check: before renaming, ask the user to confirm by printing the full plan and waiting for `y/n` input. Also create a `undo_plan.json` file that maps new names back to original names, so you could reverse the operation later:
   ```python
   # Safety prompt
   answer = input(f"Rename {count} files? (y/n): ")
   if answer.lower() != "y":
       print("Aborted.")
   ```

---

| [← Prev](../12-file-extension-counter/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../14-basic-expense-tracker/TRY_THIS.md) |
|:---|:---:|---:|
