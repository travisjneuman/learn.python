# Solution: 15-putting-it-together

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
def load_students(filename):
    """Read student data from a file and return a list of dictionaries."""
    # WHY: This docstring (the text in triple quotes) describes what the function does — it appears when someone asks for help about the function
    students = []  # WHY: Start with an empty list — we will fill it with one dictionary per student

    for line in open(filename):                 # WHY: Loop through each line in the file — the filename is passed in as a parameter so this function works with ANY file
        line = line.strip()                     # WHY: Remove invisible newline characters from the end of each line
        if not line:                            # WHY: Skip blank lines — "not line" is True when line is an empty string
            continue                            # WHY: Jump to the next line without running the code below

        parts = line.split(",")                 # WHY: Split "Alice,92" into ["Alice", "92"] — the comma is the divider
        name = parts[0]                         # WHY: The first piece is the student's name
        score = int(parts[1])                   # WHY: The second piece is the score — convert from text to a number so we can do math with it

        # Each student is a dictionary with name and score
        student = {"name": name, "score": score}  # WHY: A dictionary groups related data under labels — cleaner than using two separate lists
        students.append(student)                   # WHY: Add this student's dictionary to our list — building the collection one student at a time

    return students  # WHY: Send the complete list back to whoever called this function — the data is now structured and ready to use


def get_letter_grade(score):
    """Convert a numeric score to a letter grade."""
    # WHY: This function answers one question: "what letter grade does this number correspond to?"
    if score >= 90:       # WHY: Check the highest grade first — 90 and above is an A
        return "A"        # WHY: "return" immediately exits the function with this value — no need for elif after a return
    elif score >= 80:     # WHY: Only checked if score was less than 90 — so this catches 80-89
        return "B"
    elif score >= 70:     # WHY: Catches 70-79
        return "C"
    elif score >= 60:     # WHY: Catches 60-69
        return "D"
    else:                 # WHY: Everything below 60 — the catch-all for failing grades
        return "F"


def calculate_average(students):
    """Calculate the average score from a list of student dicts."""
    # WHY: Takes the entire list of student dictionaries and returns one number — the average score
    total = 0                                   # WHY: Accumulator pattern — start at 0 and add each score
    for student in students:                    # WHY: Loop through each student dictionary in the list
        total = total + student["score"]        # WHY: student["score"] gets the numeric score from this student's dictionary
    return total / len(students)                # WHY: Average = sum of all scores / number of students


def print_report(students):
    """Print a formatted grade report for all students."""
    # WHY: This function handles ALL the display logic — it does not return anything, it just prints
    print("=" * 40)                             # WHY: "=" * 40 creates a line of 40 equal signs — a visual header border
    print("       STUDENT GRADE REPORT")        # WHY: Centered title — the spaces before the text push it toward the middle
    print("=" * 40)
    print()                                     # WHY: Blank line after the header for breathing room

    for student in students:                    # WHY: Loop through each student to display their row
        name = student["name"]                  # WHY: Extract the name from the dictionary for readability
        score = student["score"]                # WHY: Extract the score from the dictionary
        grade = get_letter_grade(score)          # WHY: Call our grade function to convert the number to a letter — reusing code we already wrote
        print(f"  {name:<10} {score:>3}  ({grade})")  # WHY: :<10 left-aligns the name in 10 characters, :>3 right-aligns the score in 3 characters — creates neat columns

    print()                                     # WHY: Blank line before the summary section
    print("-" * 40)                             # WHY: Dashes create a visual divider between individual scores and the summary

    average = calculate_average(students)       # WHY: Call our average function — reusing code again
    print(f"  Class Average: {average:.1f}")    # WHY: :.1f formats the number with exactly 1 decimal place — 87.6 not 87.60000
    print(f"  Highest: {max(s['score'] for s in students)}")  # WHY: This is a "generator expression" — it pulls out just the scores and finds the max
    print(f"  Lowest:  {min(s['score'] for s in students)}")  # WHY: Same pattern for the minimum score
    print(f"  Students: {len(students)}")       # WHY: len() counts how many students are in the list
    print("=" * 40)                             # WHY: Closing border to match the opening — creates a visual box around the report


# ---- Main program starts here ----

# Load data from file (reusing sample data from Exercise 14)
students = load_students("../14-reading-files/data/sample.txt")  # WHY: The ../ means "go up one folder" — we are reusing the data file from Exercise 14

# Print the report
print_report(students)  # WHY: One function call produces the entire report — the complexity is hidden inside the function

# Ask the user if they want to look up a specific student
print()
lookup = input("Look up a student by name (or press Enter to skip): ")  # WHY: Give the user an optional interactive feature — pressing Enter gives an empty string

if lookup:                                       # WHY: An empty string is "falsy" — if the user pressed Enter without typing, this block is skipped
    found = False                                # WHY: Track whether we found the student — start by assuming we did not
    for student in students:                     # WHY: Search through every student in the list
        if student["name"].lower() == lookup.lower():  # WHY: .lower() makes the search case-insensitive — "alice" matches "Alice"
            grade = get_letter_grade(student["score"])  # WHY: Get the letter grade for this student's score
            print(f"\n{student['name']} scored {student['score']} ({grade})")  # WHY: Display the student's full information
            found = True                         # WHY: Mark that we found a match so we do not show the "not found" message

    if not found:                                # WHY: After checking all students, if none matched, tell the user
        print(f"\nNo student named '{lookup}' found.")

print("\nDone!")  # WHY: A clean exit message — the program is finished
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Organize code into 4 separate functions | Each function does one job: load data, convert grade, calculate average, print report. This makes the code easy to understand, test, and reuse | Could write everything in one long script, but that becomes messy and hard to modify as the program grows |
| Use a list of dictionaries for student data | Each student is a dictionary `{"name": "Alice", "score": 92}` — grouped data stays together and is accessed by label | Could use two parallel lists (names and scores) like Exercise 14, but dictionaries are cleaner when data belongs together |
| Make the search case-insensitive with `.lower()` | Users should not have to worry about capitalization — "alice", "Alice", and "ALICE" should all find the same student | Could require exact case, but that frustrates users and is bad user experience |
| Use string formatting (`:<10`, `:>3`, `:.1f`) | Aligned columns make the report professional and readable — without formatting, the output looks ragged | Could use plain `print()` without formatting, but the output would be harder to read |
| Separate the main program from the function definitions | Functions at the top, main logic at the bottom is the standard Python file layout — it makes the flow clear | Could interleave definitions and calls, but that makes the code harder to follow |

## Alternative approaches

### Approach B: Adding a new student interactively

```python
# After printing the report, ask if the user wants to add a student.
add_more = input("\nAdd a new student? (yes/no): ")

if add_more.lower() == "yes":
    new_name = input("Student name: ")                    # WHY: Get the new student's name from the user
    new_score = int(input("Score (0-100): "))             # WHY: Get their score and convert to a number

    new_student = {"name": new_name, "score": new_score}  # WHY: Create a dictionary in the same format as the others
    students.append(new_student)                           # WHY: Add to the existing list — the list grows by one

    print("\nUpdated Report:")
    print_report(students)                                 # WHY: Reprint the entire report — the new student now appears and the averages update automatically
```

**Trade-off:** This extends the program with write capability. Notice how adding one student automatically updates all the statistics because `print_report()` recalculates everything. This is the power of functions — change the data, call the function again, and everything stays correct.

### Approach C: Saving the report to a file

```python
def save_report(students, filename):
    """Save the grade report to a text file."""
    with open(filename, "w") as f:                        # WHY: "w" means write mode — creates the file or overwrites it if it exists
        f.write("Student Report\n")                       # WHY: .write() puts text into the file instead of the screen
        f.write("Name, Score, Grade\n")                   # WHY: A header row to label the columns
        f.write("-" * 30 + "\n")                          # WHY: A divider line for readability

        for student in students:
            grade = get_letter_grade(student["score"])     # WHY: Reusing our existing function — it works the same whether we print or write to file
            f.write(f"{student['name']}, {student['score']}, {grade}\n")  # WHY: \n adds a newline — without it, everything would be on one line

        average = calculate_average(students)
        f.write(f"\nAverage: {average:.1f}\n")            # WHY: Include the summary stats in the file too

save_report(students, "report.txt")                       # WHY: Creates a file called report.txt in the current folder with the full report
print("Report saved to report.txt")
```

**Trade-off:** Writing to a file is the mirror of reading from one. `open(filename, "w")` opens for writing (vs reading). `.write()` is like `print()` but goes to a file instead of the screen. This is how real programs produce output files, logs, and exports.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| The data file path is wrong | `FileNotFoundError` — Python cannot find `../14-reading-files/data/sample.txt` | Make sure you run the script from inside the `15-putting-it-together` folder. The `../` path assumes you are there |
| A line in the data file has no comma | `IndexError: list index out of range` — `.split(",")` produces one item, and `parts[1]` does not exist | Ensure the data file follows the `name,score` format with exactly one comma per line |
| The score in the file is not a number | `ValueError: invalid literal for int()` — `int("abc")` crashes | All scores must be whole numbers. Check your data file for typos |
| The student list is empty (empty file) | `ZeroDivisionError` in `calculate_average()` — dividing by `len([])` which is 0 | Check `if len(students) > 0` before calculating the average. Real programs always handle empty data |
| User types a name that does not exist in the data | The program prints "No student named 'xyz' found." — not a crash, but can confuse the user | The code already handles this with the `found` flag pattern — but showing available names would improve the experience |

## Key takeaways

1. **This program demonstrates how everything connects** — variables store data, functions organize logic, if-statements make decisions, loops process collections, dictionaries group related data, and file reading brings in external information. Every concept from Exercises 01-14 plays a role here. This is what real programming looks like: small tools working together.
2. **Functions are the architecture of programs** — `load_students()`, `get_letter_grade()`, `calculate_average()`, and `print_report()` each handle one responsibility. When you need to change how grades are calculated, you change ONE function. When you need to change the display, you change ONE function. This separation is the key to building programs that do not collapse under their own complexity.
3. **You are ready for Level 0** — if you understood this exercise, you have the foundation to build real Python programs. Level 0 introduces testing, error handling, and more structured project organization, but the core concepts — variables, functions, loops, conditions, lists, dictionaries, and files — are the tools you just learned. Everything from here builds on top of what you already know.
