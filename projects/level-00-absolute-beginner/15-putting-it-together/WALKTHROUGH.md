# Walkthrough: Putting It Together

> This guide walks through the **thinking process** for this exercise.
> It does NOT give you the complete solution. For that, see [SOLUTION.md](./SOLUTION.md).

## Before reading this

**Try the exercise yourself first.** Spend at least 20 minutes.
If you have not tried yet, close this file and open the [exercise file](./exercise.py).

---

## Understanding the problem

This exercise combines everything from Exercises 01-14 into one program: a student grade reporter. It reads student names and scores from a file, calculates grades, computes an average, and lets the user look up a student by name.

The program uses: variables, strings, user input, conditions, lists, dictionaries, loops, functions, and file reading. If you can understand this, you are ready for Level 0.

## Planning before code

Break the program into four jobs:

1. **Load data** -- read student names and scores from a file
2. **Convert scores to grades** -- turn numbers into letter grades (A, B, C, D, F)
3. **Calculate stats** -- find the average, highest, and lowest scores
4. **Display results** -- print a formatted report and handle a student lookup

## Step 1: Loading data from a file

The data file (`../14-reading-files/data/sample.txt`) looks like this:

```
Alice,92
Bob,87
Charlie,95
```

Each line has a name and a score separated by a comma. You need to read each line, split it on the comma, and store the result.

```python
line = "Alice,92"
parts = line.split(",")
name = parts[0]          # "Alice"
score = int(parts[1])    # 92
```

### Predict before you scroll

Why do we need `int()` around `parts[1]`? What would happen if we skipped it and tried to compare the score to 90?

## Step 2: Converting scores to letter grades

This is a classic `if/elif/else` chain. Think about the order:

```python
def get_letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    # ... continue for C, D, F
```

Why check `>= 90` first? Because if you checked `>= 60` first, a score of 95 would match that condition and get a "D".

## Step 3: Calculating the class average

To get an average, you need two things: the total of all scores and the count of students.

```python
total = 0
for student in students:
    total = total + student["score"]
average = total / len(students)
```

### Predict before you scroll

If there are 5 students with scores [92, 87, 95, 78, 91], what would the average be?

## Step 4: The student lookup

The program asks the user to type a student name. You loop through the list and compare names. Using `.lower()` on both sides makes the search case-insensitive (typing "alice" finds "Alice").

```python
if student["name"].lower() == lookup.lower():
    # found them
```

## Common mistakes

| Mistake | Why it happens | How to fix |
|---------|---------------|------------|
| `int("92\n")` crashes | File lines can have newline characters | Use `.strip()` before splitting |
| Grade logic gives wrong letter | Conditions checked in wrong order | Check highest threshold first (>= 90 before >= 80) |
| Student lookup is case-sensitive | "alice" does not match "Alice" | Use `.lower()` on both strings before comparing |
| Division error with empty list | `len(students)` is 0 | Check if the list is empty before dividing |

## What to explore next

1. Add a feature that prints only students who scored below 80
2. Save the report to a new file using `open("report.txt", "w")` instead of just printing it
