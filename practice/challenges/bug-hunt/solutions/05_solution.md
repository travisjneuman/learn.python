# Solution: File Handling Bugs

## Bug 1 — `create_notes_file` opens file in read mode

**Line:** `f = open(NOTES_FILE, "r")`

**Problem:** The file doesn't exist yet, and opening a nonexistent file in
read mode raises `FileNotFoundError`. Should be `"w"` to create and write.

**Fix:**

```python
f = open(NOTES_FILE, "w")
f.write("# My Notes\n")
f.close()
```

## Bug 2 — `add_note` opens file in write mode instead of append

**Line:** `f = open(NOTES_FILE, "w")`

**Problem:** `"w"` truncates the file every time, erasing all previous notes.
Should be `"a"` for append.

**Fix:**

```python
f = open(NOTES_FILE, "a")
```

## Bug 3 — `add_note` never closes the file

**Problem:** The file handle `f` is opened but never closed. This can cause
data loss (buffered writes never flushed) and resource leaks.

**Fix:** Use a `with` statement:

```python
def add_note(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")
```

## Bug 4 — `read_notes` uses ASCII encoding with emoji content

**Line:** `encoding="ascii"`

**Problem:** The third note contains a coffee emoji (☕). ASCII encoding
cannot decode non-ASCII bytes, raising `UnicodeDecodeError`.

**Fix:**

```python
with open(NOTES_FILE, "r", encoding="utf-8") as f:
```

## Bug 5 — `count_notes` leaks a file handle

**Line:** `for line in open(NOTES_FILE):`

**Problem:** The file is opened but never explicitly closed. While Python's
garbage collector may close it eventually, this is bad practice.

**Fix:**

```python
def count_notes():
    count = 0
    with open(NOTES_FILE, encoding="utf-8") as f:
        for line in f:
            if line.startswith("["):
                count += 1
    return count
```
