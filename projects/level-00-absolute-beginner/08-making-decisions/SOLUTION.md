# Solution: 08-making-decisions

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Simple if/else
temperature = 75  # WHY: Store a temperature value so we can make a decision based on it

if temperature > 80:                  # WHY: Check if the temperature is above 80 — the > symbol means "greater than"
    print("It is hot outside.")       # WHY: This line ONLY runs if the condition above is True — the indentation (4 spaces) marks it as belonging to the "if"
else:                                 # WHY: "else" catches everything that did NOT match the "if" condition
    print("It is not too hot.")       # WHY: Since 75 is not greater than 80, this line runs — only ONE of the two branches executes

# if / elif / else — multiple conditions
score = 85  # WHY: Store a test score to convert into a letter grade

if score >= 90:                       # WHY: Check the highest grade first — >= means "greater than or equal to"
    print("Grade: A")
elif score >= 80:                     # WHY: "elif" means "else if" — only checked if the previous condition was False
    print("Grade: B")                 # WHY: 85 >= 80 is True, so this runs — Python stops checking and skips the rest
elif score >= 70:                     # WHY: This is never reached because 85 already matched the previous condition
    print("Grade: C")
elif score >= 60:                     # WHY: Skipped — once a match is found, all remaining elif and else are ignored
    print("Grade: D")
else:                                 # WHY: The "catch-all" — runs only if NONE of the above conditions were True
    print("Grade: F")

# Comparison operators:
#   ==   equal to (TWO equals signs, not one!)
#   !=   not equal to
#   >    greater than
#   <    less than
#   >=   greater than or equal to
#   <=   less than or equal to
# WHY: These six operators are how you ask Python yes-or-no questions about values

# Checking equality
password = "secret123"  # WHY: Store the correct password so we can compare the user's input against it

if password == "secret123":           # WHY: == (two equals signs) checks if two values are the same — one = would STORE a value, not compare
    print("Access granted.")          # WHY: The password matches, so this runs
else:
    print("Access denied.")           # WHY: This would run if the password did not match

# Combining conditions with "and" / "or"
age = 25             # WHY: Two separate facts that must both be true for the decision
has_license = True   # WHY: True and False are special values called "booleans" — they represent yes/no

if age >= 16 and has_license:         # WHY: "and" means BOTH conditions must be True — you need to be old enough AND have a license
    print("You can drive.")           # WHY: 25 >= 16 is True AND has_license is True, so both conditions pass
else:
    print("You cannot drive.")        # WHY: This runs if either condition is False (too young OR no license)

# "not" flips a condition
is_raining = False  # WHY: Store a True/False value representing the current weather

if not is_raining:                    # WHY: "not" reverses True to False and False to True — "not False" becomes True
    print("No umbrella needed.")      # WHY: Since is_raining is False, "not is_raining" is True, so this runs
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Check grades from highest to lowest | When using `elif`, order matters — checking >= 90 first means anything that passes is definitely an A. If you checked >= 60 first, everything above 60 would get a D | Could check for exact ranges (`80 <= score < 90`), but the cascading elif pattern is cleaner and more common |
| Use `==` for password comparison | Demonstrates the critical difference between `=` (assignment) and `==` (comparison) — confusing them is the most common beginner bug with if-statements | Could compare using other methods, but `==` is the standard approach |
| Show `and`, `or`, `not` as English words | Python uses English words instead of symbols like `&&` and `\|\|` (used in other languages) — this makes Python more readable | No alternative — this is Python syntax, but it is worth noting because other languages do it differently |
| Use `True` and `False` with capital letters | These are Python's built-in boolean values — they must be capitalized exactly (True, not true) | `1` and `0` also work as True/False, but `True`/`False` are more readable |

## Alternative approaches

### Approach B: A number guessing game (from TRY_THIS.md)

```python
secret = 7                                    # WHY: The number the player needs to guess — in a real game you would randomize this
guess = int(input("Guess a number 1-10: "))   # WHY: Get the player's guess and convert from text to a number

if guess == secret:                           # WHY: Check if they guessed correctly — == compares the two numbers
    print("Correct!")
elif guess < secret:                          # WHY: If wrong, give a helpful hint about the direction
    print("Too low!")
else:                                         # WHY: If it is not correct and not too low, it must be too high
    print("Too high!")
```

**Trade-off:** This is a great practical example because it uses `if`, `elif`, and `else` together with user input. The limitation is it only gives one guess. In Exercise 11 (while loops), you will make this into a real game with multiple attempts.

### Approach C: Using `or` for multiple valid answers

```python
answer = input("Do you like Python? (yes/y/yeah): ").lower()  # WHY: .lower() converts "YES", "Yes", "yes" all to "yes" — makes comparison easier

if answer == "yes" or answer == "y" or answer == "yeah":       # WHY: "or" means ANY ONE of these being True is enough — the user can type any of the three options
    print("Great choice!")
else:
    print("Give it time, you will love it!")
```

**Trade-off:** Using `or` with multiple checks handles real-world messiness where users type things differently. The `.lower()` trick further reduces variation. In later lessons, you will learn even cleaner ways to do this (like checking `if answer in ["yes", "y", "yeah"]`).

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Using `=` instead of `==`: `if x = 5:` | `SyntaxError` — Python catches this because you cannot assign a value inside an if-statement | Remember: one `=` stores a value, two `==` compares values. Read the error message — it often suggests using `==` |
| Wrong indentation after `if:` | `IndentationError` — the code inside an if-block must be indented by exactly 4 spaces | Use consistent indentation. Most code editors add it automatically when you type `if something:` and press Enter |
| Forgetting the colon at the end: `if score >= 90` | `SyntaxError: expected ':'` — every if, elif, and else line must end with a colon | The colon tells Python "the condition ends here, the indented code below is what to do" |
| Checking `elif` after `else` | `SyntaxError` — `else` must always be the last option because it catches everything remaining | Order your blocks as: `if` (first check), then `elif` (additional checks), then `else` (everything else) at the end |
| Comparing different types: `"5" == 5` | Returns `False` — the string "5" is not the same as the number 5 even though they look similar | Make sure you are comparing the same types. Convert with `int()` if needed: `int("5") == 5` is `True` |

## Key takeaways

1. **if/elif/else gives your programs the ability to think** — instead of blindly running every line, your code can now look at data and choose what to do. This is the difference between a calculator (does the same thing every time) and an intelligent program (responds to different situations).
2. **Indentation is not just formatting in Python, it is structure** — the 4 spaces before a line tell Python "this code belongs to the if-block above." Get indentation wrong and your program either crashes or does the wrong thing. This is unique to Python and is one of the reasons Python code looks clean.
3. **`==`, `and`, `or`, and `not` are the building blocks of all decisions** — every smart feature in every program (login checks, search filters, game logic, form validation) is built from these simple comparison and combination tools. Master them and you can make any decision in code.
