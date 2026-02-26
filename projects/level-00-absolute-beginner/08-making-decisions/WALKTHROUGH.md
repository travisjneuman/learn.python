# Walkthrough: Making Decisions (if / else)

> This guide walks through the **thinking process** for this exercise.
> It does NOT give you the complete solution. For that, see [SOLUTION.md](./SOLUTION.md).

## Before reading this

**Try the exercise yourself first.** Spend at least 15 minutes.
If you have not tried yet, close this file and open the [exercise file](./exercise.py).

---

## Understanding the problem

Programs need to make choices. "If something is true, do this. Otherwise, do something else." This exercise shows you how Python decides which code to run using `if`, `elif`, and `else`.

The exercise file has four examples:
1. A temperature checker (hot or not?)
2. A grade calculator (A, B, C, D, or F)
3. A password checker (right or wrong?)
4. Combining conditions with `and`, `or`, and `not`

## Planning before code

Before writing any `if` statement, ask yourself:

1. **What am I checking?** (a number, a string, a True/False value?)
2. **How many possible outcomes are there?** (two? five?)
3. **What order should I check them?** (does it matter?)

## Step 1: Simple if/else -- two outcomes

The simplest decision has two paths: yes or no.

```python
temperature = 75

if temperature > 80:
    print("It is hot outside.")
else:
    print("It is not too hot.")
```

The indented line under `if` runs when the condition is `True`. The indented line under `else` runs when it is `False`. **Indentation matters** -- use 4 spaces.

### Predict before you scroll

If `temperature` is 75, which message prints? What if you change it to 85?

## Step 2: Multiple conditions with elif

When there are more than two outcomes, use `elif` (short for "else if"):

```python
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
```

Python checks each condition **from top to bottom** and runs the first one that is `True`. Once it finds a match, it skips the rest.

### Predict before you scroll

If `score` is 85, which grade prints? Why does it not also print "Grade: C" even though 85 is also >= 70?

## Step 3: The = vs == trap

This is the single most common mistake for beginners:

```python
# WRONG -- this tries to store 5 in x
if x = 5:

# RIGHT -- this checks if x equals 5
if x == 5:
```

One `=` means "store this value." Two `==` means "are these equal?"

## Common mistakes

| Mistake | Why it happens | How to fix |
|---------|---------------|------------|
| Using `=` instead of `==` | Looks similar, easy to forget | `=` stores, `==` compares -- always use `==` in `if` |
| Forgetting the colon `:` | New syntax to remember | Every `if`, `elif`, `else` line ends with `:` |
| Wrong indentation | Python is picky about spaces | Use exactly 4 spaces for each level |
| Checking conditions in wrong order | `if score >= 70` before `if score >= 90` catches 90+ first | Check the most specific condition first |

## What to explore next

1. Build an age checker that uses `input()` to ask the user their age, then prints whether they are an adult or a minor
2. Change the `temperature` and `score` values in the exercise file, predict the output, then run it -- were you right?
