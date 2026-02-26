# Bridge Exercise: Level 0 to Level 1

You have completed Level 0. You can write functions, run tests, and work with basic data types. Level 1 introduces **file I/O** (reading and writing files) and **basic error handling** (try/except). This bridge exercise gives you a gentle introduction to both.

---

## What Changes in Level 1

In Level 0, your programs mostly worked with hardcoded data or simple command-line arguments. In Level 1, you will read input from files (CSV, JSON, text) and handle things that can go wrong (missing files, bad data, invalid input).

---

## Exercise: Read, Process, Handle Errors

### Step 1: Create a data file

Create a file called `numbers.txt` with this content:

```text
10
20
not_a_number
30
```

Notice that one line is not a valid number. This is intentional.

### Step 2: Write the function

Create `bridge_0_to_1.py`:

```python
from pathlib import Path


def sum_numbers_from_file(filepath):
    """Read a file of numbers (one per line) and return their sum.

    Lines that are not valid numbers are skipped with a warning.
    Returns a dict with 'total', 'valid_count', and 'skipped_lines'.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    total = 0
    valid_count = 0
    skipped_lines = []

    text = path.read_text()
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = float(stripped)
            total += value
            valid_count += 1
        except ValueError:
            skipped_lines.append({"line": line_number, "content": stripped})

    return {
        "total": total,
        "valid_count": valid_count,
        "skipped_lines": skipped_lines,
    }
```

**New concepts introduced:**
- `Path(filepath)` creates a path object. `path.exists()` checks if the file is real.
- `path.read_text()` reads the entire file into a string.
- `try` / `except ValueError` catches the error when `float()` cannot convert a string.
- `enumerate(..., start=1)` gives you both the line number and the line content.

### Step 3: Write the tests

Create `test_bridge_0_to_1.py`:

```python
from pathlib import Path
import pytest
from bridge_0_to_1 import sum_numbers_from_file


def test_valid_numbers(tmp_path):
    f = tmp_path / "nums.txt"
    f.write_text("10\n20\n30\n")
    result = sum_numbers_from_file(f)
    assert result["total"] == 60.0
    assert result["valid_count"] == 3
    assert result["skipped_lines"] == []


def test_skips_bad_lines(tmp_path):
    f = tmp_path / "mixed.txt"
    f.write_text("10\nhello\n20\n")
    result = sum_numbers_from_file(f)
    assert result["total"] == 30.0
    assert result["valid_count"] == 2
    assert len(result["skipped_lines"]) == 1
    assert result["skipped_lines"][0]["content"] == "hello"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        sum_numbers_from_file("nonexistent.txt")


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    result = sum_numbers_from_file(f)
    assert result["total"] == 0
    assert result["valid_count"] == 0
```

**New testing concepts:**
- `tmp_path` is a pytest feature that gives you a temporary folder. Files created there are cleaned up automatically.
- `pytest.raises(FileNotFoundError)` checks that your code raises the expected error.

### Step 4: Run it

```bash
pytest test_bridge_0_to_1.py -v
```

All four tests should pass.

### Step 5: Try it yourself

Add a new function called `write_summary(result, output_path)` that writes the result dict to a JSON file. Then write a test that calls your function and reads the JSON back to verify it.

**Hint:** Use `import json`, `json.dumps()` to write, and `json.loads()` to read.

---

## You Are Ready

If you can read a file, handle errors with try/except, and use `tmp_path` in tests, you are ready for Level 1.

---

| [Level 0 Projects](level-0/README.md) | [Home](../README.md) | [Level 1 Projects](level-1/README.md) |
|:---|:---:|---:|
