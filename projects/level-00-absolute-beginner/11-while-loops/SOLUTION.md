# Solution: 11-while-loops

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Count from 1 to 5 using a while loop
count = 1  # WHY: Start the counter at 1 — this variable tracks where we are in the count

while count <= 5:                          # WHY: "while count is less than or equal to 5, keep running" — the loop checks this BEFORE each repetition
    print(f"Count is: {count}")            # WHY: Display the current count — runs 5 times with count being 1, 2, 3, 4, 5
    count = count + 1                      # WHY: CRITICAL — increase count by 1 each time. Without this line, count stays at 1 forever and the loop never ends

print("Done counting!")                    # WHY: This is NOT indented, so it runs AFTER the loop finishes — only once, when count reaches 6

# A countdown
print()                                    # WHY: Blank line between examples for readability
countdown = 5                              # WHY: Start at 5 and count down to 1

while countdown > 0:                       # WHY: "while countdown is greater than 0, keep going" — the loop stops when countdown hits 0
    print(countdown)                       # WHY: Prints 5, 4, 3, 2, 1
    countdown = countdown - 1              # WHY: Decrease by 1 each time — eventually countdown reaches 0 and the while condition becomes False

print("Go!")                               # WHY: Runs after the loop ends — the classic "countdown then launch" pattern

# Using a while loop for user input validation
# (This keeps asking until the user gives a valid answer)
print()
print("--- Guessing Game ---")

secret = 7                                 # WHY: The correct answer — in a real game you would randomize this
guess = 0                                  # WHY: Start with a wrong value so the loop runs at least once — 0 is not 7, so the condition is True

while guess != secret:                     # WHY: != means "not equal to" — keep looping as long as the guess is wrong
    guess = int(input("Guess a number between 1 and 10: "))  # WHY: Ask the user for a guess and convert it from text to a number
    if guess < secret:                     # WHY: Give a helpful hint so they can adjust
        print("Too low!")
    elif guess > secret:                   # WHY: The other direction — their guess was too high
        print("Too high!")
                                           # WHY: If neither too low nor too high, it must be correct — the loop condition will be False and the loop ends

print("You got it!")                       # WHY: This runs when the loop exits — meaning guess finally equals secret

# Using "break" to exit a loop early
print()
print("--- Type 'quit' to stop ---")

while True:                                # WHY: "while True" creates a loop that runs forever — the only way to exit is with "break" inside
    text = input("Say something: ")        # WHY: Ask the user for input each time through the loop
    if text == "quit":                     # WHY: Check if the user typed the exit word
        break                              # WHY: "break" immediately exits the loop — Python jumps straight to the first line after the loop
    print(f"You said: {text}")             # WHY: Echo back what they typed — this only runs if they did NOT type "quit" (because break would have exited)

print("Goodbye!")                          # WHY: Runs after break exits the loop — the program ends cleanly
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Use `while count <= 5` instead of `for i in range` | While loops show the mechanics of repetition — you control the starting point, the condition, and the step yourself | A `for` loop would be simpler for counting, but the point is to learn how `while` works and when you would choose it |
| Initialize `guess = 0` before the loop | The while condition `guess != secret` needs `guess` to exist before it is first checked — 0 is a safe "wrong" default | Could use `while True` with a `break`, but the condition-based approach teaches the standard while pattern |
| Show `while True` with `break` | This is the most common real-world while loop pattern — "keep going until something specific happens" | Could always use a condition in the `while` line, but `while True` + `break` is cleaner when the exit condition happens in the middle of the loop |
| Demonstrate the countdown separately | Counting down is a different mental model than counting up — both are important and common | Could combine both in one example, but separating them makes each pattern clearer |

## Alternative approaches

### Approach B: Doubling until a limit (from TRY_THIS.md)

```python
number = 1                                 # WHY: Start with the smallest positive number

while number <= 1000:                      # WHY: Keep doubling as long as the number is 1000 or less
    print(number)                          # WHY: Shows: 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
    number = number * 2                    # WHY: Doubling grows FAST — this is called exponential growth. 10 doublings takes you from 1 to 1024
```

**Trade-off:** This example shows that while loops are not just for counting by 1. The step can be any operation: multiply, divide, add 5, or any other change. The key is that the variable MUST change each time, or the loop runs forever.

### Approach C: A password checker with attempt counting

```python
correct = "python"                         # WHY: The correct password to check against
attempts = 0                               # WHY: Track how many times the user has tried
max_attempts = 3                           # WHY: Limit attempts to prevent unlimited guessing

while attempts < max_attempts:             # WHY: Stop after 3 wrong tries — a common security pattern
    attempt = input("Enter password: ")    # WHY: Ask for the password each time
    attempts = attempts + 1                # WHY: Count this attempt whether it is right or wrong

    if attempt == correct:                 # WHY: Check if the password matches
        print("Welcome!")
        break                              # WHY: Exit the loop immediately on success — no need to keep asking
    else:
        remaining = max_attempts - attempts  # WHY: Calculate how many tries are left
        print(f"Wrong. {remaining} attempts remaining.")

if attempts == max_attempts and attempt != correct:  # WHY: After the loop, check if they used all attempts without success
    print("Account locked.")               # WHY: A real system would lock the account — we just print a message
```

**Trade-off:** This combines a while loop with a counter AND a break, showing a realistic security pattern. It is more complex than the basic examples but demonstrates how while loops work in real programs.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting to update the counter: no `count = count + 1` | Infinite loop — the condition never becomes False, so the loop runs forever | Press Ctrl+C to stop it. Always make sure something inside the loop changes the condition variable |
| Infinite loop from `while True` without a `break` | The program runs forever, printing or asking forever | Every `while True` loop MUST have a `break` somewhere inside it. Double-check before running |
| Off-by-one error: using `<` instead of `<=` | `while count < 5` stops at 4 instead of 5 — you get one fewer repetition than expected | Decide whether you want "less than" or "less than or equal to." Trace through the values mentally: if count starts at 1 and you use `< 5`, the values are 1, 2, 3, 4 (not 5) |
| User types a non-number in the guessing game | `ValueError` from `int()` — the program crashes | For now, just type valid numbers. Error handling (try/except) is a later topic |
| Forgetting `break` exits only the innermost loop | If you have a loop inside a loop, `break` only exits the inner one | Be aware of which loop your `break` belongs to — indentation tells you |

## Key takeaways

1. **While loops repeat code until a condition becomes False** — unlike for loops which iterate through a fixed collection, while loops keep going until you tell them to stop. Use `for` when you know how many times to repeat. Use `while` when you do not know — you are waiting for something to happen.
2. **Every while loop needs an exit strategy** — either the condition variable must change inside the loop (like `count = count + 1`), or there must be a `break` statement. Without one of these, you get an infinite loop. Ctrl+C is your emergency escape when that happens.
3. **`while True` with `break` is the most common real-world pattern** — "run forever, checking inside the loop for a reason to stop" covers user menus, server loops, game loops, and input validation. You will see this pattern constantly in professional code.
