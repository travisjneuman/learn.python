# Files and Paths

> **Try This First:** Before reading, try this in Python: `open('test.txt', 'w').write('hello')` then `print(open('test.txt').read())`. You just wrote to a file and read it back.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/files-and-paths.md) | [Quiz](quizzes/files-and-paths-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/files-and-paths.md) |

<!-- modality-hub-end -->

Programs read data from files and write results to files. Understanding how to work with files and their locations (paths) is essential.

## Visualize It

See how Python reads a file and processes it line by line:
[Open in Python Tutor](https://pythontutor.com/render.html#code=from%20pathlib%20import%20Path%0A%0Ap%20%3D%20Path%28%22data.txt%22%29%0Aprint%28p.name%29%0Aprint%28p.stem%29%0Aprint%28p.suffix%29%0Aprint%28p.parent%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

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
- **Windows:** `C:\Users\alice\projects\data.txt`
- **Mac/Linux:** `/Users/alice/projects/data.txt`

### Relative vs absolute paths

- **Absolute:** Full address from the root — `C:\Users\alice\projects\data.txt`
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
path = "C:\Users\alice\new_file.txt"  # \n becomes a newline!

# Right
path = "C:\\Users\\alice\\new_file.txt"  # Escaped backslashes
path = r"C:\Users\alice\new_file.txt"    # Raw string (r prefix)
path = Path("C:/Users/alice/new_file.txt")  # Forward slashes work too
```

## Practice

- [Level 00 / 14 Reading Files](../projects/level-00-absolute-beginner/14-reading-files/)
- [Level 0 / 01 Terminal Hello Lab](../projects/level-0/01-terminal-hello-lab/README.md)
- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)
- [Level 0 / 03 Temperature Converter](../projects/level-0/03-temperature-converter/README.md)
- [Level 0 / 04 Yes No Questionnaire](../projects/level-0/04-yes-no-questionnaire/README.md)
- [Level 0 / 05 Number Classifier](../projects/level-0/05-number-classifier/README.md)
- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 0 / 08 String Cleaner Starter](../projects/level-0/08-string-cleaner-starter/README.md)
- [Level 0 / 09 Daily Checklist Writer](../projects/level-0/09-daily-checklist-writer/README.md)

**Quick check:** [Take the quiz](quizzes/files-and-paths-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](collections-explained.md) | [Home](../README.md) | [Next →](../projects/level-1/README.md) |
|:---|:---:|---:|
