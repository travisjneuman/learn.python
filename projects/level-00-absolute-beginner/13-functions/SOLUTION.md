# Solution: 13-functions

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Define a simple function
def say_hello():                          # WHY: "def" means "define a function" — you are creating a reusable block of code with the name "say_hello"
    print("Hello! This message comes from a function.")  # WHY: The indented code is the function "body" — it runs every time you call the function

# Call (use) the function
say_hello()   # WHY: Writing the function name with () at the end RUNS the function — "calling" it executes the indented code inside
say_hello()   # WHY: You can call it as many times as you want — the code inside runs again each time, producing the same output

# Functions with parameters — values you pass in
def greet(name):                          # WHY: "name" inside the parentheses is a parameter — a placeholder for a value you will provide when calling the function
    print(f"Hello, {name}! Nice to meet you.")  # WHY: The function uses whatever value was passed in for "name" — different calls produce different output

greet("Alice")   # WHY: Passes "Alice" as the value for the "name" parameter — prints "Hello, Alice! Nice to meet you."
greet("Alice")   # WHY: Same input produces the same output — functions are predictable
greet("Bob")     # WHY: Now "name" is "Bob" — the same function works with any name you give it

# Functions that return a value
def add(a, b):                            # WHY: This function takes two parameters (a and b) — both are values the caller provides
    result = a + b                        # WHY: Calculate the sum and store it in a local variable
    return result                         # WHY: "return" sends the result BACK to whoever called the function — without return, the result would be lost

total = add(5, 3)                         # WHY: Call add() with 5 and 3 — the function returns 8, which gets stored in "total"
print(f"5 + 3 = {total}")                # WHY: Now we can use the returned value however we want — print it, store it, use it in more math

# You can use the returned value directly
print(f"10 + 20 = {add(10, 20)}")        # WHY: add(10, 20) runs, returns 30, and the f-string inserts it — no need to store in a variable first

# Functions with default values
def make_greeting(name, greeting="Hello"):  # WHY: greeting="Hello" sets a default — if the caller does not provide a greeting, "Hello" is used automatically
    return f"{greeting}, {name}!"

print(make_greeting("Alice"))              # WHY: Only provides "name" — greeting uses the default "Hello", result is "Hello, Alice!"
print(make_greeting("Alice", "Hey"))       # WHY: Provides both — "Hey" overrides the default, result is "Hey, Alice!"
print(make_greeting("Alice", "Welcome"))   # WHY: "Welcome" overrides the default, result is "Welcome, Alice!"

# A more practical function
def calculate_tip(meal_price, tip_percent=18):  # WHY: Default tip of 18% — the caller can override it but does not have to
    tip = meal_price * (tip_percent / 100)      # WHY: Convert percentage to decimal (18 becomes 0.18) and multiply by the price
    total = meal_price + tip                     # WHY: The customer pays the meal price plus the tip
    return round(total, 2)                       # WHY: Round to 2 decimal places because this is money — return the final amount

print()
print(f"$50 meal, 18% tip: ${calculate_tip(50)}")       # WHY: Uses default 18% — returns 59.0
print(f"$50 meal, 20% tip: ${calculate_tip(50, 20)}")   # WHY: Overrides with 20% — returns 60.0
print(f"$75 meal, 15% tip: ${calculate_tip(75, 15)}")   # WHY: Different meal price and tip rate — returns 86.25
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Start with a function that takes no parameters | `say_hello()` is the simplest possible function — it shows the `def`/call pattern without the extra complexity of parameters | Could start with a parameterized function, but seeing the bare pattern first makes it easier to add parameters later |
| Show `return` separately from `print()` | These are two different things: `print()` displays text on screen, `return` sends a value back to the caller. Beginners often confuse them | Could use only `print()` inside functions, but then learners miss the critical concept of returning values |
| Use default parameter values | Default values make functions flexible — they work with minimal input but accept customization | Could require all parameters every time, but defaults reduce repetition and make functions friendlier to use |
| Include a practical tip calculator | Real-world examples show WHY functions are useful — "I can calculate any tip with one line of code" is compelling | Abstract math examples work for teaching but do not motivate as well |

## Alternative approaches

### Approach B: Temperature converter (from TRY_THIS.md)

```python
def to_celsius(fahrenheit):               # WHY: A function that converts Fahrenheit to Celsius — wraps the formula in a reusable name
    return (fahrenheit - 32) * 5 / 9      # WHY: The standard conversion formula — subtract 32, multiply by 5, divide by 9

print(to_celsius(212))   # WHY: 212F is boiling water — returns 100.0 (100 Celsius)
print(to_celsius(32))    # WHY: 32F is freezing water — returns 0.0 (0 Celsius)
print(to_celsius(72))    # WHY: 72F is room temperature — returns approximately 22.2 Celsius
```

**Trade-off:** This is a perfect example of why functions exist — you memorize the formula once (inside the function), then use it by name forever. Without the function, you would have to remember `(f - 32) * 5 / 9` every time. The function name `to_celsius` tells you exactly what it does.

### Approach C: A function that returns True or False

```python
def is_even(number):                      # WHY: A function that answers a yes/no question — "is this number even?"
    return number % 2 == 0                # WHY: % 2 gives the remainder when dividing by 2. If it is 0, the number is even. == 0 returns True or False

print(is_even(4))     # WHY: 4 % 2 is 0, so 0 == 0 is True — returns True
print(is_even(7))     # WHY: 7 % 2 is 1, so 1 == 0 is False — returns False

# Use it in a decision
if is_even(10):                           # WHY: The function returns True, so the if-block runs
    print("10 is even")
```

**Trade-off:** Functions that return True or False are called "predicates" — they answer questions. Naming them with `is_` makes the code read like English: `if is_even(number)` reads as "if the number is even." This naming convention is widely used in professional Python code.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Calling a function before defining it | `NameError: name 'say_hello' is not defined` — Python reads top to bottom, so the function must be defined ABOVE the line that calls it | Always put your `def` blocks before the code that calls them. This is why functions are usually at the top of a file |
| Forgetting the parentheses when calling: `say_hello` | No error, but nothing happens — `say_hello` without `()` refers to the function object itself, it does not run the code inside | Always include `()` when calling a function: `say_hello()`. The parentheses mean "run this now" |
| Forgetting `return` in a function that should return a value | The function returns `None` — your variable gets `None` instead of a useful value | If a function calculates something you need, it must have a `return` statement. `print()` inside a function is NOT the same as `return` |
| Wrong number of arguments: `add(5)` when it expects two | `TypeError: add() missing 1 required positional argument: 'b'` — you provided 1 value but the function needs 2 | Check the function definition to see how many parameters it has, and provide exactly that many when calling |
| Confusing `print()` and `return` | `print()` displays on screen but the value is lost. `return` sends the value back so you can store or use it | Use `return` when the caller needs the result. Use `print()` when you just want to display something |

## Key takeaways

1. **Functions are reusable code blocks with names** — you define them once with `def` and call them as many times as you need. Any time you find yourself copying and pasting code, that code should become a function. Functions are the primary tool for organizing programs as they grow.
2. **`return` sends a value back to the caller, `print()` just displays it** — this is the most confused concept in beginner Python. If you need to USE the result of a function (store it, do math with it, pass it to another function), you need `return`. If you just need to SEE something on screen, use `print()`.
3. **Functions break big problems into small, manageable pieces** — instead of one long script, you write small functions that each do one thing well. `calculate_tip()`, `to_celsius()`, `is_even()` — each solves one problem. In Exercise 15, you will see how multiple functions work together to build a complete program.
