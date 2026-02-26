# Solution: 10-for-loops

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Loop through a list of items
fruits = ["apple", "banana", "cherry", "date"]  # WHY: Create a list of items to loop through

print("My fruits:")
for fruit in fruits:                              # WHY: "for fruit in fruits" means "take each item from the list, one at a time, and call it fruit"
    # This indented code runs once for each fruit.
    # The variable "fruit" holds a different value each time.
    print(f"  - {fruit}")                         # WHY: The first time, fruit is "apple". The second time, "banana". And so on. The loop handles this automatically

# Loop through numbers using range()
# range(5) gives you: 0, 1, 2, 3, 4
print()                                           # WHY: Blank line to separate output sections
print("Counting from 0 to 4:")
for number in range(5):                           # WHY: range(5) creates the sequence 0, 1, 2, 3, 4 — it starts at 0 and stops BEFORE 5
    print(number)                                 # WHY: Each time through the loop, "number" holds the next value in the range

# range(1, 6) gives you: 1, 2, 3, 4, 5
print()
print("Counting from 1 to 5:")
for number in range(1, 6):                        # WHY: range(start, stop) lets you choose where to begin — starts at 1, stops before 6
    print(number)                                 # WHY: This prints 1 through 5 — more natural for counting than starting from 0

# Use a loop to calculate something
scores = [85, 92, 78, 95, 88]                    # WHY: A list of test scores we want to add up
total = 0                                         # WHY: Start with 0 and add each score to it — this is called an "accumulator" pattern

for score in scores:                              # WHY: Visit each score in the list, one at a time
    total = total + score                         # WHY: Add the current score to the running total — after all 5 loops, total will hold the sum of all scores

average = total / len(scores)                     # WHY: Divide the total by the number of scores to get the average — len() counts how many scores there are
print()
print(f"Scores: {scores}")                       # WHY: Show the raw data so the reader can verify the calculation
print(f"Total: {total}")                         # WHY: 85+92+78+95+88 = 438
print(f"Average: {average}")                     # WHY: 438 / 5 = 87.6

# Loop with an if statement inside
print()
print("Numbers from 1 to 10 that are even:")
for number in range(1, 11):                       # WHY: range(1, 11) generates 1 through 10 — remember, the stop value is not included
    if number % 2 == 0:                           # WHY: % 2 gives the remainder when dividing by 2 — even numbers have remainder 0
        print(f"  {number} is even")              # WHY: Only prints when the number is even — the if-statement filters out odd numbers
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Name the loop variable descriptively: `fruit`, `score`, `number` | The variable name should describe what each item IS — `for fruit in fruits` reads like English | Could use `for x in fruits` or `for i in fruits`, but that makes the code harder to understand |
| Use `range(5)` to demonstrate zero-based counting | Reinforces that Python starts counting at 0, which was introduced with list indices in Exercise 09 | Could use `range(1, 6)` to start at 1, but learners need to understand range(n) starts at 0 by default |
| Show the accumulator pattern (total = 0, then add in loop) | This is one of the most important patterns in programming — building up a result one piece at a time | Could use `sum(scores)` (shown in Exercise 09), but understanding HOW sum works internally is more valuable |
| Combine a loop with an if-statement | Shows that you can nest one concept inside another — this is where programming becomes powerful | Could keep them separate, but combining loop + if is such a common pattern that it needs early exposure |

## Alternative approaches

### Approach B: A multiplication table (from TRY_THIS.md)

```python
number = 7                                        # WHY: The number to build a multiplication table for
for i in range(1, 11):                            # WHY: Multiply by 1 through 10 — range(1, 11) gives us exactly that sequence
    print(f"{number} x {i} = {number * i}")       # WHY: Python calculates number * i for each value of i — the f-string formats it neatly
```

Output:
```
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
...
7 x 10 = 70
```

**Trade-off:** This shows the practical power of loops — 10 lines of output from just 3 lines of code. Without a loop, you would need to write 10 separate print statements. The loop does the repetitive work for you.

### Approach C: Counting backwards with range()

```python
for i in range(10, 0, -1):                        # WHY: range(start, stop, step) — start at 10, stop before 0, step by -1 (count down)
    print(i)                                       # WHY: Prints 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
print("Liftoff!")                                  # WHY: This line is NOT indented, so it runs AFTER the loop finishes — only once
```

**Trade-off:** The third argument to `range()` is the step size. `-1` counts backward, `2` would count by twos, `5` would count by fives. Most of the time you will use range with one or two arguments, but the step is useful for countdowns and skipping values.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Forgetting the colon after `for ... in ...:` | `SyntaxError: expected ':'` — the colon tells Python the loop header is done and the body starts next | Every `for` line must end with a colon, just like `if` statements |
| Wrong indentation inside the loop | `IndentationError` — the code inside the loop must be indented by 4 spaces | Lines inside the loop must be indented consistently. Lines that should run after the loop should NOT be indented |
| Expecting `range(5)` to include 5 | It gives 0, 1, 2, 3, 4 — it stops BEFORE the number you give it | `range(n)` produces n numbers starting from 0. If you want 1 to 5, use `range(1, 6)` |
| Modifying a list while looping through it | Items can be skipped or the program can behave unpredictably | Never add or remove items from a list you are currently looping through. Build a new list instead |
| Forgetting to initialize the accumulator: jumping straight to `total = total + score` | `NameError: name 'total' is not defined` — you cannot add to a variable that does not exist yet | Always set your accumulator to a starting value before the loop: `total = 0` |

## Key takeaways

1. **For loops eliminate repetition** — instead of writing the same code 10 or 100 or 1000 times, you write it once and let the loop repeat it. This is the single most powerful idea you have learned so far. Any time you find yourself copying and pasting lines, a loop should replace them.
2. **`range()` generates sequences of numbers on demand** — `range(n)` gives 0 to n-1, `range(start, stop)` gives start to stop-1, and `range(start, stop, step)` lets you control the step size. Combined with a for loop, range() lets you count, iterate, and repeat with precision.
3. **Loops + conditions = smart automation** — nesting an `if` inside a `for` lets you process data selectively. "For each student, if their score is below 70, print a warning" is a pattern you will use in every data-driven program. This combination of loops and conditions is the foundation of data processing.
