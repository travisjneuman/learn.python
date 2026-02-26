# Solution: 05-numbers-and-math

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Addition
print("5 + 3 =", 5 + 3)  # WHY: The + operator adds two numbers — Python calculates the result (8) before printing it

# Subtraction
print("10 - 4 =", 10 - 4)  # WHY: The - operator subtracts — works exactly like on paper

# Multiplication (use * not x)
print("6 * 7 =", 6 * 7)  # WHY: The * symbol means multiply — the letter x cannot be used because it could be a variable name

# Division (always gives a decimal result)
print("15 / 4 =", 15 / 4)  # WHY: The / operator divides — it ALWAYS gives a decimal (3.75), even when the answer is a whole number

# Integer division (drops the decimal part)
print("15 // 4 =", 15 // 4)  # WHY: The // operator divides and throws away the decimal part — 15/4 is 3.75, so // gives you 3

# Remainder (called "modulo" — what is left over after division)
print("15 % 4 =", 15 % 4)  # WHY: The % operator gives the remainder — 15 divided by 4 is 3 with 3 left over, so the answer is 3

# Exponent (power)
print("2 ** 8 =", 2 ** 8)  # WHY: The ** operator raises a number to a power — 2**8 means 2 times itself 8 times, which is 256

# Order of operations works like math class: parentheses first
print("(2 + 3) * 4 =", (2 + 3) * 4)  # WHY: Parentheses force 2+3 to happen first (5), then multiply by 4 = 20
print("2 + 3 * 4 =", 2 + 3 * 4)      # WHY: Without parentheses, multiplication happens before addition: 3*4=12, then 2+12=14

# Store results in variables
price = 29.99           # WHY: This is a "float" (decimal number) — prices need decimals for cents
tax_rate = 0.08         # WHY: 8% tax stored as a decimal — 8% means 8/100 which is 0.08
tax_amount = price * tax_rate  # WHY: Calculate how much tax to add: 29.99 * 0.08 = 2.3992
total = price + tax_amount     # WHY: The customer pays price + tax: 29.99 + 2.3992 = 32.3892

print()                         # WHY: Blank line separates the math examples from the practical example
print("Price:", price)          # WHY: Show each step so the learner can follow the calculation
print("Tax:", tax_amount)       # WHY: Notice this prints 2.3992 — ugly for a dollar amount
print("Total:", total)          # WHY: Prints 32.3892 — too many decimal places for money

# Round a number to 2 decimal places
print("Total (rounded):", round(total, 2))  # WHY: round(32.3892, 2) gives 32.39 — the 2 means "keep 2 decimal places"
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Show all 7 math operators in one exercise | Giving a complete reference means you can come back to this file whenever you forget an operator | Could introduce them one at a time across multiple exercises, but having them together is more useful as a reference |
| Use a real-world tax calculation | Practical examples make abstract math feel useful — everyone understands prices and taxes | Could use purely abstract math, but connecting to real life helps motivation |
| Show `round()` for the tax example | Money with 4+ decimal places looks wrong — `round()` is essential for real-world number formatting | Could ignore rounding, but then the output looks broken and learners think they did something wrong |
| Demonstrate order of operations | Parentheses changing the result is a common source of bugs — better to learn now than debug later | Could skip this, but math order errors are one of the most common beginner mistakes |

## Alternative approaches

### Approach B: Building a seconds-per-year calculator with named variables

```python
seconds_per_minute = 60    # WHY: Start with the smallest unit and build up — each variable holds one fact
minutes_per_hour = 60      # WHY: Give every number a name so the math reads like a sentence
hours_per_day = 24         # WHY: If any of these facts changed (like on Mars), you only change one line
days_per_year = 365        # WHY: This is approximate — a real year is 365.25 days, but close enough for learning

# Multiply all the pieces together.
seconds_per_year = seconds_per_minute * minutes_per_hour * hours_per_day * days_per_year
# WHY: 60 * 60 * 24 * 365 = 31,536,000 seconds in a year — using variables makes this readable

print(f"There are {seconds_per_year:,} seconds in a year.")
# WHY: The :, inside the f-string adds commas to large numbers — 31536000 becomes 31,536,000
```

**Trade-off:** This approach emphasizes using descriptive variable names for every number, which makes complex calculations readable. The exercise version shows the operators directly, which is better for learning what each operator does. Both are valid — in real code, you would use variables.

### Approach C: Using modulo (%) for practical even/odd checking

```python
number = 7                           # WHY: Pick any number to test
remainder = number % 2               # WHY: Any number divided by 2 has remainder 0 (even) or 1 (odd)
print(f"{number} % 2 = {remainder}") # WHY: Shows the result — 7 % 2 = 1, meaning 7 is odd

# Check several numbers
for n in [2, 5, 10, 13, 100]:       # WHY: Test multiple numbers to see the pattern
    if n % 2 == 0:                   # WHY: Remainder of 0 means the number divides evenly by 2
        print(f"{n} is even")
    else:
        print(f"{n} is odd")
```

**Trade-off:** This previews loops (Exercise 10) and if/else (Exercise 08), so it goes beyond the current lesson. But seeing a practical use of `%` shows why it exists — it is not just abstract math.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Dividing by zero: `10 / 0` | `ZeroDivisionError` — Python crashes because division by zero is mathematically undefined | Never divide by a variable without checking it is not zero first. You will learn how to check in Exercise 08 |
| Expecting `10 / 2` to give `5` | It gives `5.0` (a float, not an integer) — the `/` operator always produces a decimal number | Use `10 // 2` if you need a whole number result (gives `5`). This catches many beginners off guard |
| Forgetting parentheses in a calculation | `2 + 3 * 4` gives 14, not 20 — multiplication happens before addition, just like in school | Use parentheses to make your intent clear: `(2 + 3) * 4` gives 20. When in doubt, add parentheses |
| Floating-point weirdness: `0.1 + 0.2` | Gives `0.30000000000000004` instead of `0.3` — this is how all computers store decimal numbers | Use `round()` when you need exact decimals. This is not a Python bug — it happens in every programming language |
| Confusing `*` and `**` | `2 * 8` gives 16 (multiplication) but `2 ** 8` gives 256 (exponent) — very different results | `*` is multiply, `**` is "to the power of." Double-check which one you mean |

## Key takeaways

1. **Python has 7 math operators and you now know all of them** — `+` `-` `*` `/` `//` `%` `**`. These cover addition, subtraction, multiplication, division, integer division, remainder, and exponents. Every calculation you will ever write uses some combination of these.
2. **There are two types of numbers: integers (whole) and floats (decimal)** — Python usually handles the difference automatically, but division with `/` always produces a float. Understanding this prevents surprise results in your calculations.
3. **`round()` and parentheses are your friends** — `round()` cleans up messy decimal numbers, and parentheses control the order of math operations. These two tools will save you from the most common number-related bugs in your future programs.
