# Solution: 04-variables

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Create a variable called "name" and store the text "Alice" in it.
name = "Alice"  # WHY: The = sign means "put the value on the right into the name on the left" — it is NOT the same as "equals" in math

# Now we can use the variable name instead of typing the text again.
print(name)  # WHY: When Python sees a word without quotes, it looks up the variable and uses the stored value — prints "Alice"

# Create more variables.
age = 30          # WHY: Variables can hold numbers too — no quotes needed for numbers
city = "Denver"   # WHY: Text values always need quotes — without quotes Python would think Denver is another variable name

# Use variables in print statements.
print("Name:", name)   # WHY: Mixing a text label with a variable makes the output readable — prints "Name: Alice"
print("Age:", age)     # WHY: The comma between items adds a space automatically
print("City:", city)   # WHY: Each variable holds its value until you change it or the program ends

# You can change what a variable holds at any time.
# The old value is gone. The new value replaces it.
age = 31  # WHY: This overwrites the old value (30) — the variable now holds 31. The old 30 is gone forever
print("Next year I will be", age)  # WHY: Prints 31, not 30, because we just changed what age holds

# You can use variables in math.
hours_per_day = 8                              # WHY: Give numbers meaningful names so your code reads like English
days_per_week = 5                              # WHY: "days_per_week" is much clearer than just writing the number 5
hours_per_week = hours_per_day * days_per_week  # WHY: Python looks up both variables (8 and 5), multiplies them, and stores 40 in the new variable
print("I work", hours_per_week, "hours per week")  # WHY: Prints "I work 40 hours per week" — the variable holds the calculated result

# You can combine text variables (this is called "concatenation").
first_name = "Alice"                           # WHY: Storing first and last name separately lets you use them independently
last_name = "Neuman"                           # WHY: You might need just the last name for sorting, or just the first for greeting
full_name = first_name + " " + last_name       # WHY: The + joins strings together — the " " in the middle adds a space between them
print("Full name:", full_name)                 # WHY: Prints "Full name: Alice Neuman" — the three strings were glued into one
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Use descriptive variable names like `hours_per_day` | Names that read like English make code self-explanatory — you do not need a comment to understand what `hours_per_day` holds | Could use short names like `h` or `hpd`, but then the code becomes a puzzle to read |
| Use lowercase with underscores (snake_case) | This is Python's official naming convention — all Python programmers use it | Some languages use camelCase (`hoursPerDay`) but that is not the Python way |
| Show variable reassignment (`age = 31`) | Understanding that variables can change is crucial — they are not permanent labels | Could skip this, but then learners would not know variables can be updated |
| Use concatenation with `+` for full_name | Shows how string joining works at a basic level — it is simple and visual | Could use f-strings (`f"{first_name} {last_name}"`), but those come in Exercise 06 |

## Alternative approaches

### Approach B: Using f-strings instead of commas and concatenation

```python
name = "Alice"    # WHY: Same variable creation — this part does not change
age = 30          # WHY: Store the age as a number (no quotes)
city = "Denver"   # WHY: Store the city as text (with quotes)

# f-strings let you embed variables directly in text.
print(f"My name is {name}, I am {age} years old, and I live in {city}.")
# WHY: The f before the quote enables {variable} substitution — cleaner than commas for full sentences

# You can even do math inside the curly braces.
print(f"In 5 years I will be {age + 5}.")
# WHY: Python evaluates {age + 5} as 35 and inserts the result into the string
```

**Trade-off:** f-strings produce cleaner output (no extra spaces from commas) and are the preferred approach in modern Python. However, they require understanding the `f"..."` syntax. The comma approach in the exercise is simpler for an absolute first encounter with variables.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting quotes around text: `name = Alice` | `NameError: name 'Alice' is not defined` — Python thinks Alice is another variable, not text | Text values must always be in quotes: `name = "Alice"` |
| Starting a variable name with a number: `1name = "test"` | `SyntaxError` — variable names must start with a letter or underscore, never a number | Use `name1` instead of `1name`. Letters first, numbers after |
| Using a variable before creating it: `print(score)` when score was never assigned | `NameError: name 'score' is not defined` — Python cannot find a variable with that name | Always assign a value to a variable before trying to use it |
| Confusing `=` (assignment) with `==` (comparison) | `=` stores a value. `==` checks if two things are equal. Using the wrong one gives unexpected results | Remember: one `=` means "store this." Two `==` means "are these equal?" (You will use `==` in Exercise 08) |
| Using spaces or hyphens in variable names: `my-name` or `my name` | `SyntaxError` — Python reads the hyphen as subtraction and the space as two separate things | Use underscores: `my_name`. Only letters, numbers, and underscores are allowed |

## Key takeaways

1. **Variables are named containers for data** — you put a value in (with `=`) and get it back out (by using the name). This is how every program remembers information. Without variables, you would have to re-type every value every time you need it.
2. **Variable names matter** — good names like `hours_per_week` make your code readable. Bad names like `x` make your code a mystery. Write code as if someone else has to read it tomorrow (that someone is usually future-you).
3. **Variables are the foundation of everything that follows** — every concept from here on (math, decisions, loops, functions) builds on the idea of storing and retrieving values by name. Master this, and the rest gets easier.
