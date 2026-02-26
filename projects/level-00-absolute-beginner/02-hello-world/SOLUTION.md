# Solution: 02-hello-world

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Display the classic first-program message.
print("Hello, world!")  # WHY: This is the traditional first program in every language — it proves you can make the computer display text

# Print a custom message to show you can change the text.
print("My name is Python and I do what you tell me.")  # WHY: Demonstrates that you can put any text inside the quotes

# Print a number — no quotes needed for numbers.
print(42)  # WHY: Numbers do not need quotes because Python already knows they are numbers, not commands

# Print a math result — Python calculates it first, then displays the answer.
print(7 + 3)  # WHY: Python does the math (7+3=10) and then prints the result — you never see "7 + 3", just "10"

# Print text and a calculated number together using a comma.
print("The answer is", 6 * 7)  # WHY: The comma lets you mix text and numbers — Python adds a space between them automatically

# Print a blank line to create visual spacing.
print()  # WHY: An empty print() outputs a blank line — useful for making output easier to read

# Show that single quotes and double quotes both work.
print('Single quotes work too.')   # WHY: Python treats 'text' and "text" exactly the same — use whichever you prefer
print("Double quotes also work.")  # WHY: Most programmers pick one style and stick with it — double quotes are more common in Python
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Start with `"Hello, world!"` | This is a tradition going back to 1978 — nearly every programmer's first program prints this message | Could use any message, but this connects you to millions of other learners |
| Use double quotes for strings | Double quotes are the most common convention in Python and many other languages | Single quotes work identically — `'Hello'` and `"Hello"` do exactly the same thing |
| Show commas for mixing text and numbers | Commas are the simplest way to combine different types in `print()` — no conversion needed | Could use f-strings (covered in Exercise 06), but commas are simpler for beginners |
| Include `print()` with no arguments | Blank lines make output much easier to read, and this teaches that print() can be called empty | Could skip blank lines, but cluttered output is harder to understand |

## Alternative approaches

### Approach B: Using f-strings (a preview of Exercise 06)

```python
name = "Alice"                        # WHY: Store your name in a variable so you can reuse it
age = 25                              # WHY: Store a number in a variable
print(f"Hello, my name is {name}!")   # WHY: f-strings let you insert variables directly into text — the f before the quote enables this
print(f"I am {age} years old.")       # WHY: {age} gets replaced with the value 25 when Python runs this line
print(f"Next year I will be {age + 1}.")  # WHY: You can even do math inside the curly braces
```

**Trade-off:** f-strings are more powerful and readable than commas, but they require understanding variables first (Exercise 04). For this exercise, plain `print()` with commas is the right starting point.

### Approach C: Using string concatenation (joining strings with +)

```python
print("Hello" + ", " + "world" + "!")  # WHY: The + operator glues strings together — but you must handle spaces yourself
print("The answer is " + str(42))      # WHY: You cannot use + to join a string and a number — str() converts the number to text first
```

**Trade-off:** Concatenation with `+` requires you to manually add spaces and convert numbers to strings with `str()`. Commas handle this automatically. Concatenation is useful when you need precise control over spacing.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Mismatched quotes: `print("Hello')` | `SyntaxError` — Python sees a double quote opening but a single quote closing, and they do not match | Always use the same quote type to open and close: `"Hello"` or `'Hello'` |
| Forgetting the parentheses: `print "Hello"` | `SyntaxError` — Python 3 requires parentheses around everything you print | Always write `print("text")` with parentheses |
| No quotes around text: `print(Hello)` | `NameError: name 'Hello' is not defined` — Python thinks Hello is a variable name, not text | Wrap text in quotes so Python knows it is a string: `print("Hello")` |
| Forgetting the closing quote: `print("Hello)` | `SyntaxError: unterminated string literal` — Python reached the end of the line without finding the closing quote | Always close your quotes — most code editors highlight unclosed strings |
| Trying to use `+` with a string and number: `print("age: " + 25)` | `TypeError` — Python refuses to glue text and numbers together with `+` | Use a comma instead: `print("age:", 25)` or convert: `print("age: " + str(25))` |

## Key takeaways

1. **`print()` is your primary tool for seeing what your program does** — every time you want to check a value, display a result, or show a message, you will use `print()`. It is the most used function in all of Python.
2. **Strings (text) must always be wrapped in quotes** — without quotes, Python thinks your words are commands or variable names. Quotes are how Python tells the difference between code and data.
3. **You can mix text and numbers in `print()` using commas** — Python automatically adds a space between each item. This simple technique carries you through most beginner programs before you learn fancier methods like f-strings.
