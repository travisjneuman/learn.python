# Solution: 07-user-input

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Ask for the user's name. The text inside input() is the prompt
# that the user sees.
name = input("What is your name? ")  # WHY: input() pauses the program and waits for the user to type something — the text inside is the question shown on screen

# Now use what they typed.
print(f"Nice to meet you, {name}!")  # WHY: Whatever the user typed is now stored in the "name" variable — we use an f-string to include it in a greeting

# Ask for their favorite color.
color = input("What is your favorite color? ")  # WHY: You can call input() as many times as you need — each call asks one question and stores one answer
print(f"{color} is a great color.")              # WHY: Using the answer immediately makes the program feel conversational and interactive

# IMPORTANT: input() always gives you a string, even if the
# user types a number. If you want to do math with it, you
# must convert it.

age_text = input("How old are you? ")  # WHY: Even if the user types "25", input() gives you the string "25" (text), not the number 25

# Convert the string to a number using int()
age = int(age_text)  # WHY: int() takes the text "25" and turns it into the number 25 — now you can do math with it

# Now you can do math with it.
print(f"You will be {age + 1} next year.")  # WHY: age + 1 works because age is now a number — if we had not converted it, Python would crash here

# You can do the conversion on one line:
# age = int(input("How old are you? "))
# WHY: This is a shortcut that nests the functions — input() runs first, then int() converts the result
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Store input in descriptive variables | `name`, `color`, and `age` make the code self-documenting — you know exactly what each variable holds | Could use generic names like `answer1`, but that makes the code harder to understand |
| Convert age in two steps (input, then int) | Separating the steps makes it clearer what is happening — first get the text, then convert to a number | Could do `int(input("..."))` on one line, but two steps is easier to understand when learning |
| Use `int()` for age, not `float()` | Ages are whole numbers — `int()` gives you a clean number without decimals | `float()` would work but gives you 25.0 instead of 25, which looks odd for an age |
| Include a space at the end of the prompt string | `"What is your name? "` — the space after the `?` prevents the user's typing from bumping against the question mark | Without the space, the user sees `What is your name?Alice` which looks crowded |

## Alternative approaches

### Approach B: A tip calculator (from TRY_THIS.md)

```python
# Ask for the meal price — use float() because prices have decimals.
price = float(input("Meal price: $"))  # WHY: float() converts text to a decimal number — needed for prices like 24.99 that have cents

# Ask for the tip percentage.
tip_pct = float(input("Tip percentage (like 20): "))  # WHY: The user types 20 to mean 20% — we will divide by 100 to get the decimal form

# Calculate the tip amount.
tip = price * (tip_pct / 100)  # WHY: 20% means 20/100 = 0.20 — multiplying the price by 0.20 gives the tip amount

# Show the results.
print(f"Tip: ${round(tip, 2)}")           # WHY: round() ensures the tip has exactly 2 decimal places — money always shows 2 decimals
print(f"Total: ${round(price + tip, 2)}") # WHY: Total is price + tip, rounded to 2 decimals for clean money formatting
```

**Trade-off:** This example uses `float()` instead of `int()` because prices have decimal points. `int()` can only handle whole numbers — typing "24.99" into `int()` would crash. Use `int()` for counting numbers (age, quantity) and `float()` for measurement numbers (price, weight, temperature).

### Approach C: A greeting that builds on itself

```python
first = input("First name? ")              # WHY: Asking for first and last separately gives you more flexibility
last = input("Last name? ")                # WHY: You might need just the first name for a casual greeting
print(f"Hello, {first} {last}!")           # WHY: Combine them with a space in between for the full name
print(f"Can I call you {first}?")          # WHY: Using just the first name shows why splitting the input is useful
```

**Trade-off:** You could ask for the full name in one question (`input("Full name? ")`), but splitting it gives you more control. This is a common pattern: collect specific pieces of data separately so you can use them individually.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User types a word when a number is expected: `int("hello")` | `ValueError: invalid literal for int()` — Python cannot turn the word "hello" into a number | For now, just type valid numbers. In later exercises, you will learn to catch errors with try/except |
| User types a decimal when `int()` is used: `int("3.5")` | `ValueError` — `int()` cannot convert a string with a decimal point | Use `float("3.5")` for decimal numbers, or `int(float("3.5"))` to convert and then drop the decimal |
| User presses Enter without typing anything | `input()` returns an empty string `""` — if you try `int("")`, it crashes with `ValueError` | You can check `if age_text:` before converting, but error handling comes in a later exercise |
| Forgetting the conversion: `age = input("Age? ")` then `age + 1` | `TypeError` — Python tries to add the number 1 to the string "25" and refuses | Always convert with `int()` or `float()` before doing math with user input |
| No space at the end of the prompt: `input("Name?")` | The user's typing appears directly after the question mark: `Name?Alice` — hard to read | Add a space after your prompt text: `input("Name? ")` |

## Key takeaways

1. **`input()` is how you make programs interactive** — it pauses the program, shows a message, and waits for the user to type something. Everything the user types becomes a string, no matter what it looks like. This is the bridge between your code and the person using it.
2. **Always convert user input before doing math** — `input()` gives you text (a string), not a number. Use `int()` for whole numbers and `float()` for decimals. Forgetting to convert is one of the most common beginner bugs, and the error message (`TypeError`) will become very familiar.
3. **User input makes your programs reusable** — instead of hard-coding values like `age = 30`, you can ask the user for their actual age. This is the difference between a static script and a dynamic tool. From here on, almost every program you write will use `input()` in some form.
