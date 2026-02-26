# Solution: 06-strings-and-text

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Creating strings
greeting = "Hello"  # WHY: A string is any text inside quotes — this stores the word "Hello" in a variable
name = "Alice"      # WHY: Strings can hold names, sentences, single characters, or even empty text ""

# Combining strings (concatenation) — glues them together
message = greeting + ", " + name + "!"  # WHY: The + operator joins strings end-to-end — you must manually add spaces and punctuation
print(message)                           # WHY: Prints "Hello, Alice!" — the four strings were glued into one

# f-strings — the modern, clean way to put variables inside text.
# Put an f before the opening quote, then use {variable_name} inside.
print(f"Hello, {name}! Welcome to Python.")  # WHY: f-strings replace {name} with the actual value "Alice" — much easier to read than concatenation

# You can put any expression inside the curly braces.
age = 30  # WHY: Store a number we will use in the f-strings below
print(f"{name} is {age} years old.")          # WHY: {name} becomes "Alice", {age} becomes 30 — Python does the substitution automatically
print(f"In 10 years, {name} will be {age + 10}.")  # WHY: You can do math inside the braces — {age + 10} becomes 40

# String length — how many characters (including spaces)
sentence = "Python is fun"  # WHY: Store the text so we can measure it
print(f"The sentence '{sentence}' has {len(sentence)} characters.")  # WHY: len() counts every character including spaces — "Python is fun" has 13 characters

# Uppercase and lowercase
print("hello".upper())     # WHY: .upper() creates a new string with all letters capitalized — prints "HELLO"
print("HELLO".lower())     # WHY: .lower() creates a new string with all letters lowercase — prints "hello"
print("hello".title())     # WHY: .title() capitalizes the first letter of each word — prints "Hello"

# Checking what a string contains
email = "user@example.com"  # WHY: Store an email address to search through
print(f"Does the email contain @? {'@' in email}")  # WHY: The "in" keyword checks if one string is found inside another — returns True or False

# Replacing text
old_text = "I like Java"                     # WHY: Store a string we want to modify
new_text = old_text.replace("Java", "Python")  # WHY: .replace() finds "Java" and swaps it with "Python" — creates a NEW string, does not change old_text
print(new_text)                              # WHY: Prints "I like Python" — old_text still holds "I like Java"

# Splitting a string into a list of words
words = "one two three four".split()  # WHY: .split() breaks a string apart at every space, giving you a list of individual words
print(words)                          # WHY: Prints ['one', 'two', 'three', 'four'] — now each word is a separate item you can work with
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Teach both concatenation (+) and f-strings | Concatenation shows how joining works mechanically; f-strings show the modern, preferred way | Could teach only f-strings, but understanding + helps when you see it in other people's code |
| Show `.upper()`, `.lower()`, `.title()` together | These are the three most common case-change methods — seeing them side by side makes the pattern clear | Could introduce them separately, but grouping them helps you remember they are related |
| Demonstrate that strings are immutable | This prevents the common confusion of calling `.replace()` and expecting the original to change | Could skip this concept, but then beginners get silently wrong results |
| Use `in` keyword for checking string contents | `in` is the most readable way to search — it reads like English: "if '@' in email" | Could use `.find()` which returns the position, but `in` is simpler for yes/no checks |

## Alternative approaches

### Approach B: Using string methods for data cleaning

```python
# Real-world use: cleaning up messy user input
raw_name = "   alice JOHNSON   "            # WHY: Real user input often has extra spaces and inconsistent capitalization

clean_name = raw_name.strip()               # WHY: .strip() removes spaces from both ends — "   alice JOHNSON   " becomes "alice JOHNSON"
clean_name = clean_name.title()             # WHY: .title() capitalizes the first letter of each word — "alice JOHNSON" becomes "Alice Johnson"

print(f"Cleaned up: '{clean_name}'")        # WHY: Prints "Alice Johnson" — clean, consistent formatting

# You can chain methods together on one line.
result = "   hello world   ".strip().upper()  # WHY: First strips spaces, then uppercases — "HELLO WORLD"
print(result)                                  # WHY: Chaining keeps code compact, but do not chain too many — readability matters
```

**Trade-off:** Method chaining is concise but can be hard to debug. When learning, it is better to do one step per line so you can `print()` after each step to check your work. Chain methods once you are confident each step does what you expect.

### Approach C: Using string multiplication for decoration

```python
print("=" * 40)           # WHY: Multiplying a string repeats it — "=" * 40 creates a line of 40 equal signs
print("    Welcome to My Program")  # WHY: The spaces indent the text to center it roughly
print("=" * 40)           # WHY: Same line again to create a visual box around the title

print()                    # WHY: Blank line for spacing
print("-" * 20)           # WHY: A shorter divider line using dashes — useful for separating sections
```

**Trade-off:** String multiplication is a quick way to create visual dividers and decoration. It is less common in real programs (which use proper formatting libraries), but very handy for console output.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting the `f` before the quote: `print("{name}")` | Prints the literal text `{name}` instead of the variable's value | The `f` is what tells Python to look inside the curly braces. Without it, `{name}` is just regular text |
| Putting a quote inside a string: `print("He said "hello"")` | `SyntaxError` — Python thinks the string ends at the second quote | Use the other quote type: `print("He said 'hello'")` or `print('He said "hello"')` |
| Expecting `.upper()` to change the original string | The original stays the same — `.upper()` creates a brand new string | Assign the result back: `text = text.upper()` if you want to keep the change |
| Trying to add a number to a string: `"age: " + 25` | `TypeError` — Python refuses to combine text and numbers with `+` | Convert the number first: `"age: " + str(25)` or use an f-string: `f"age: {25}"` |
| Using the wrong index with `[]`: `"hello"[5]` | `IndexError` — "hello" has 5 characters but indices go from 0 to 4 | Remember: counting starts at 0. The last character of "hello" is `"hello"[4]` which is "o" |

## Key takeaways

1. **f-strings are your go-to tool for building text** — any time you need to combine variables with text, use `f"text {variable} more text"`. They are cleaner than concatenation, easier to read, and the standard way to format strings in modern Python.
2. **Strings are immutable, meaning they cannot be changed in place** — methods like `.upper()`, `.replace()`, and `.strip()` always create a new string and leave the original untouched. If you want to keep the result, you must assign it to a variable.
3. **String methods are your text toolbox** — `.upper()`, `.lower()`, `.strip()`, `.replace()`, `.split()`, and `len()` handle the vast majority of text manipulation you will ever need. You will use these constantly in every program that works with text, which is nearly every program.
