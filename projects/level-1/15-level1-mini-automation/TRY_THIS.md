# Try This — Project 15

1. Add a Step 6: `step_export_csv()` that writes the transformed, filtered records to a CSV file. Use Python's `csv.writer` to create a file with headers `name,status,value`. After writing, print how many rows were exported and the file path:
   ```python
   import csv

   def step_export_csv(records, output_path):
       with open(output_path, "w", newline="", encoding="utf-8") as f:
           writer = csv.writer(f)
           writer.writerow(["name", "status", "value"])
           for r in records:
               writer.writerow([r["name"], r["status"], r["value"]])
       return len(records)
   ```

2. Add a `--dry-run` flag that runs every pipeline step but skips writing any output files. Instead, it prints what each step would do and how many records it would process. This is useful for testing the pipeline logic without creating files:
   ```text
   [DRY RUN] Step 1: Would read 10 lines from data/sample_input.txt
   [DRY RUN] Step 2: Would parse 8 records (2 skipped)
   [DRY RUN] Step 3: Would keep 6 active records (2 filtered)
   [DRY RUN] Step 4: Would transform 6 records
   [DRY RUN] Step 5: Summary -- total value: $350.00
   [DRY RUN] No files written.
   ```

3. Add error recovery to the pipeline. Right now, if one record has bad data, the whole pipeline could fail. Wrap each step in a try/except and collect errors into an `errors` list. At the end, print a report showing which records failed and at which step, alongside the successful results:
   ```text
   Pipeline complete: 7 records processed, 1 error

   Errors:
     Line 5: "bad | data" -- ValueError at step_transform (could not convert to float)
   ```
   This teaches a real-world pattern: pipelines should not stop completely because of one bad record.

---

| [← Prev](../14-basic-expense-tracker/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
