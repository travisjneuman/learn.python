# Solution: 14-reading-files

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Read the entire file as one big string
contents = open("data/sample.txt").read()  # WHY: open() finds and opens the file, .read() grabs ALL the text as one long string
print("--- Raw file contents ---")
print(contents)                            # WHY: Prints everything in the file at once — useful for seeing what the data looks like before processing it

# Read the file line by line
print("--- Line by line ---")
lines = open("data/sample.txt").readlines()  # WHY: .readlines() splits the file into a list where each item is one line (including the newline character at the end)

for line in lines:                          # WHY: Loop through each line in the list — each line is a string like "Alice,92\n"
    # .strip() removes the newline character at the end of each line
    clean_line = line.strip()               # WHY: .strip() removes invisible whitespace characters (spaces, tabs, newline) from both ends of the string
    if clean_line:                          # WHY: An empty string is "falsy" in Python — this skips blank lines that have no data
        print(clean_line)

# Parse the data — each line has "name,score"
print()
print("--- Parsed data ---")

names = []    # WHY: Create an empty list to collect all the names as we find them in the file
scores = []   # WHY: Create an empty list to collect all the scores — keeping them in separate lists lets us use sum(), max(), min() later

for line in open("data/sample.txt"):        # WHY: You can loop directly over an open file — Python gives you one line at a time, which is memory-efficient
    line = line.strip()                     # WHY: Remove the newline character from the end — "Alice,92\n" becomes "Alice,92"
    if not line:                            # WHY: "not line" is True when line is empty — skip blank lines so we do not try to process nothing
        continue                            # WHY: "continue" skips the rest of this loop iteration and jumps to the next line in the file

    # .split(",") breaks the line at every comma
    parts = line.split(",")                 # WHY: "Alice,92".split(",") gives you ["Alice", "92"] — a list of two items, split at the comma
    name = parts[0]                         # WHY: The first item (index 0) is the name — "Alice"
    score = int(parts[1])                   # WHY: The second item (index 1) is the score as text — int() converts "92" to the number 92

    names.append(name)                      # WHY: Add this student's name to our names list — building up the collection one item at a time
    scores.append(score)                    # WHY: Add their score to the scores list — after the loop, both lists will have all the data

    print(f"  {name}: {score}")             # WHY: Display each parsed student as we process them — indented with 2 spaces for readability

# Calculate stats from the file data
print()
print(f"Students: {len(names)}")            # WHY: len() counts how many names we collected — same as the number of students in the file
print(f"Highest score: {max(scores)}")      # WHY: max() finds the largest number in the scores list — the best score
print(f"Lowest score: {min(scores)}")       # WHY: min() finds the smallest number — the score that needs the most improvement
print(f"Average: {sum(scores) / len(scores)}")  # WHY: Average = total of all scores / number of students — sum() adds them all up
```

The data file (`data/sample.txt`) contains:
```
Alice,92
Bob,87
Charlie,95
Diana,78
Eve,91
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Show three different ways to read a file | `.read()` (all at once), `.readlines()` (list of lines), and `for line in open()` (one at a time) — each has its use case | Could show just one method, but understanding the options helps you choose the right tool for each situation |
| Use `.strip()` on every line | Files include invisible newline characters (`\n`) at the end of each line — stripping them prevents bugs in comparisons and display | Could leave them and deal with the extra whitespace, but that leads to subtle bugs |
| Keep names and scores in separate parallel lists | Two lists (names and scores) let us use `max(scores)`, `min(scores)`, and `sum(scores)` directly | Could use a list of dictionaries (shown in Exercise 15), which is more organized but more complex for a first file-reading exercise |
| Use `continue` to skip blank lines | `continue` is cleaner than wrapping the entire loop body in an `if` block — it handles the special case early and keeps the main logic clean | Could use `if clean_line:` to wrap the body, which also works but adds indentation |

## Alternative approaches

### Approach B: Finding the top student

```python
best_name = ""       # WHY: Track the name of the student with the highest score — start empty
best_score = 0       # WHY: Track the highest score seen so far — start at 0 so any real score will be higher

for line in open("data/sample.txt"):
    line = line.strip()
    if not line:
        continue

    parts = line.split(",")              # WHY: Split "Alice,92" into ["Alice", "92"]
    name = parts[0]
    score = int(parts[1])

    if score > best_score:               # WHY: If this student's score beats the current best, update our records
        best_score = score               # WHY: Remember the new highest score
        best_name = name                 # WHY: Remember WHO has the highest score

print(f"Top student: {best_name} with {best_score}")  # WHY: After checking all students, the best one is stored in these variables
```

**Trade-off:** This approach finds the best student in a single pass through the file — it does not need to store all the data first. For huge files with millions of lines, this is more memory-efficient than loading everything into lists. For small files, either approach works fine.

### Approach C: Using `with open()` (the safer way)

```python
with open("data/sample.txt") as f:        # WHY: "with" automatically closes the file when the indented block ends — prevents resource leaks
    for line in f:                         # WHY: Loop through the file line by line — same as before, but now the file closes automatically
        line = line.strip()
        if line:
            parts = line.split(",")
            print(f"{parts[0]}: {parts[1]}")
# WHY: At this point (no longer indented), the file is guaranteed to be closed
```

**Trade-off:** `with open()` is the professional way to read files in Python. The simple `open()` used in the exercise works for learning, but it does not guarantee the file gets closed properly. In real programs, always use `with open()`. You will learn this pattern fully in Level 0.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| File does not exist: `open("wrong_name.txt")` | `FileNotFoundError: No such file or directory` — Python cannot find the file at that path | Double-check the filename and make sure you are running the script from the correct folder. The path is relative to where you run `python exercise.py` |
| File has unexpected format: a line without a comma | `IndexError: list index out of range` — `.split(",")` produces only one item, so `parts[1]` does not exist | Always inspect your data file first. For robust code, check `len(parts)` before accessing `parts[1]` |
| Score is not a number: `int("abc")` | `ValueError: invalid literal for int()` — Python cannot convert non-numeric text to a number | Make sure your data file has the correct format: `name,number` on each line. No extra text in the score column |
| Running from the wrong directory | The program looks for `data/sample.txt` relative to where you ran the command — if you are in the wrong folder, it will not find the file | Always `cd` into the `14-reading-files` directory before running `python exercise.py` |
| Encoding issues with special characters | `UnicodeDecodeError` if the file contains characters not in the default encoding | For now, stick to basic ASCII text (regular English letters and numbers). Encoding is an advanced topic |

## Key takeaways

1. **Reading files is how programs interact with stored data** — every real application reads files: spreadsheets, logs, settings, databases, web pages. The pattern you learned here (open the file, loop through lines, split each line into pieces, process the pieces) is the universal foundation of data processing.
2. **Always clean your data with `.strip()` and check for empty lines** — real-world data is messy. Lines have invisible newline characters, files have blank lines, and formats vary. Getting in the habit of stripping and validating every line saves you hours of debugging later.
3. **`.split()` is the bridge between raw text and usable data** — a file is just a long string of text. `.split(",")` turns that text into structured pieces you can work with. This same concept scales to CSV files, JSON data, log files, and any text-based data format. In Exercise 15, you will combine file reading with functions and dictionaries to build a complete data processing program.
