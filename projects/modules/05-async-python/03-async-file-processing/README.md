# Module 05 / Project 03 — Async File Processing

Home: [README](../../../../README.md) · Module: [Async Python](../README.md)

## Focus

- `aiofiles` for non-blocking file I/O
- Async generators with `async for`
- Processing multiple files concurrently
- Comparing sync vs async file processing

## Why this project exists

File processing is a common task. When you process many files, async lets you read the next file while the OS is still fetching data for the current one. This project shows how async file I/O works and when it helps.

## Run

```bash
cd projects/modules/05-async-python/03-async-file-processing
python project.py
```

## Expected output

```text
--- Generating sample files ---
Created 10 sample files in data/

--- Sync file processing ---
Processed file_01.txt: 50 lines, 250 words
Processed file_02.txt: 50 lines, 248 words
...
Sync total: ~X seconds

--- Async file processing ---
Processed file_03.txt: 50 lines, 252 words
Processed file_01.txt: 50 lines, 250 words
...
Async total: ~X seconds

--- Async generator demo ---
Yielded line 1 from file_01.txt
Yielded line 2 from file_01.txt
...
```

## Alter it

1. Process `.csv` files instead of `.txt` files. Parse them into rows.
2. Add a file size filter — skip files under 100 bytes.
3. Write the summary results to an output file using `aiofiles`.

## Break it

1. Try to process a file that does not exist. What exception do you get?
2. Open many files without closing them (remove `async with`). What happens?
3. Use `open()` (sync) inside an async function. Does it still work? Is it truly async?

## Fix it

1. Add `try/except FileNotFoundError` to handle missing files gracefully.
2. Always use `async with` to ensure files are closed properly.
3. Add a semaphore to limit how many files are open at once.

## Explain it

1. When does async file I/O help vs regular file I/O?
2. What is an async generator and how does `async for` work?
3. Why does `async with aiofiles.open()` matter compared to regular `open()`?
4. When would you use threads instead of async for file processing?

## Mastery check

You can move on when you can:
- use aiofiles to read/write files asynchronously,
- write an async generator that yields lines from a file,
- process multiple files concurrently with gather(),
- explain when async file I/O is beneficial.

## Next

[Project 04 — Producer-Consumer](../04-producer-consumer/)
