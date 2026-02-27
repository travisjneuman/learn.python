# Files and Paths Cheat Sheet

> Programs read data from files and write results to files. The `with` statement keeps it safe.

## Key Syntax

```python
# Read an entire file
with open("data.txt") as f:
    contents = f.read()

# Read line by line
with open("data.txt") as f:
    for line in f:
        print(line.strip())

# Write to a file (creates or overwrites)
with open("output.txt", "w") as f:
    f.write("Hello!\n")

# Append to a file (adds to end)
with open("log.txt", "a") as f:
    f.write("New entry\n")
```

## File Modes

| Mode | Meaning | Creates file? | Erases existing? |
|------|---------|:---:|:---:|
| `"r"` | Read (default) | No | No |
| `"w"` | Write | Yes | Yes |
| `"a"` | Append | Yes | No |
| `"r+"` | Read and write | No | No |

## pathlib -- the Modern Way

```python
from pathlib import Path

p = Path("data/sample.txt")
p.exists()          # True or False
p.read_text()       # Read entire file as string
p.write_text("hi")  # Write string to file
p.name              # "sample.txt"
p.stem              # "sample"
p.suffix            # ".txt"
p.parent            # Path("data")

# Build paths safely
folder = Path("data")
file = folder / "output.txt"   # data/output.txt
```

## Common Patterns

```python
# Read lines into a list
lines = Path("data.txt").read_text().splitlines()

# Read CSV-like data
with open("data.csv") as f:
    for line in f:
        columns = line.strip().split(",")

# Write a list of lines
with open("output.txt", "w") as f:
    for item in my_list:
        f.write(f"{item}\n")

# Check before reading
if Path("config.txt").exists():
    config = Path("config.txt").read_text()
```

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| File not found | `FileNotFoundError` | Check the path and current directory |
| Forget `.strip()` | Double-spaced output (extra `\n`) | `line.strip()` removes whitespace |
| Windows backslashes | `\n` in path becomes newline | Use `r"C:\path"` or `Path("C:/path")` |
| Forget `"w"` mode | Cannot write (default is read) | `open("file.txt", "w")` |
| No `with` statement | File stays open if error occurs | Always use `with open(...) as f:` |

## Quick Reference

| Operation | Syntax |
|-----------|--------|
| Read all | `Path("f.txt").read_text()` |
| Write all | `Path("f.txt").write_text("content")` |
| Read lines | `f.read().splitlines()` |
| Write line | `f.write("text\n")` |
| Check exists | `Path("f.txt").exists()` |
| Get filename | `Path("a/b.txt").name` -- `"b.txt"` |
| Get extension | `Path("a/b.txt").suffix` -- `".txt"` |
| Join paths | `Path("a") / "b.txt"` |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../files-and-paths.md)
