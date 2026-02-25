# Files and Paths

Programs read data from files and write results to files. Understanding how to work with files and their locations (paths) is essential.

## Reading a file

The simplest way:
```python
contents = open("data.txt").read()
print(contents)
```

The better way (automatically closes the file when done):
```python
with open("data.txt") as f:
    contents = f.read()
    print(contents)
```

## Reading line by line

```python
with open("data.txt") as f:
    for line in f:
        line = line.strip()  # Remove the newline character
        print(line)
```

## Writing to a file

```python
with open("output.txt", "w") as f:
    f.write("Hello, world!\n")
    f.write("Second line.\n")
```

- `"w"` means write (creates new file or overwrites existing)
- `"a"` means append (adds to end of existing file)
- `"r"` means read (default, what `open()` uses without a mode)

## What is a path?

A path is the address of a file on your computer:
- **Windows:** `C:\Users\Travis\projects\data.txt`
- **Mac/Linux:** `/Users/Travis/projects/data.txt`

### Relative vs absolute paths

- **Absolute:** Full address from the root — `C:\Users\Travis\projects\data.txt`
- **Relative:** Address from where you are now — `data.txt` or `../other_folder/file.txt`

`..` means "go up one folder." So `../data.txt` means "go up one folder, then find data.txt."

### Using pathlib (the modern way)

```python
from pathlib import Path

# Create a path
data_file = Path("data/sample.txt")

# Check if it exists
if data_file.exists():
    contents = data_file.read_text()

# Get parts of the path
data_file.name       # "sample.txt"
data_file.stem       # "sample"
data_file.suffix     # ".txt"
data_file.parent     # Path("data")
```

You will use `pathlib` starting in Level 0. For Level 00, plain `open()` is fine.

## Common mistakes

**File not found:**
```python
open("data.txt")  # FileNotFoundError if data.txt is not in your current folder
```
Fix: make sure you are in the right directory (`cd` to the project folder first).

**Forgetting to strip newlines:**
```python
for line in open("data.txt"):
    print(line)  # Double-spaced output because each line has \n
    # Fix: print(line.strip())
```

**Using backslashes on Windows:**
```python
# Wrong (backslash is an escape character)
path = "C:\Users\Travis\new_file.txt"  # \n becomes a newline!

# Right
path = "C:\\Users\\Travis\\new_file.txt"  # Escaped backslashes
path = r"C:\Users\Travis\new_file.txt"    # Raw string (r prefix)
path = Path("C:/Users/Travis/new_file.txt")  # Forward slashes work too
```

## Related exercises
- [Level 00, Exercise 14 — Reading Files](../projects/level-00-absolute-beginner/14-reading-files/)
