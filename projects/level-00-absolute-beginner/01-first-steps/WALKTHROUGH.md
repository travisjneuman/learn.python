# Walkthrough: First Steps

> This guide walks through the **thinking process** for this exercise.
> It does NOT give you the complete solution. For that, see [SOLUTION.md](./SOLUTION.md).

## Before reading this

**Try the exercise yourself first.** Spend at least 10 minutes.
If you have not tried yet, close this file and open the [exercise file](./exercise.py).

---

## Understanding the problem

You need to open Python in interactive mode (the `>>>` prompt) and type simple commands. This is not about writing a program yet -- it is about seeing that Python responds to what you type.

Think of it like a conversation: you type something, Python answers.

## Planning before code

There are only two things to do:

1. **Open Python** in your terminal so you see the `>>>` prompt
2. **Type commands** and watch what Python gives back

## Step 1: Get into interactive mode

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

```
python
```

You should see something like:

```
Python 3.12.0
>>>
```

That `>>>` is Python waiting for you. If you see it, you are in.

### What if it does not work?

- On some systems you need `python3` instead of `python`
- If you get "command not found", Python is not installed yet -- go back to the setup guide

## Step 2: Try math

Type this and press Enter:

```python
2 + 2
```

Python should answer `4`. That is it. You just made a computer do math.

### Predict before you scroll

What do you think `5 * 6` will give you? What about `100 / 4`? Think about it, then try each one.

## Step 3: Try printing text

Type this:

```python
print("Hello, I am learning Python!")
```

Python prints your message back. The `print()` function is how you tell Python to display something.

## Step 4: Leave interactive mode

When you are done experimenting, type:

```python
exit()
```

## Step 5: Run the exercise file

Now try running the file itself:

```
python exercise.py
```

This runs all the commands in the file at once instead of one at a time.

## Common mistakes

| Mistake | Why it happens | How to fix |
|---------|---------------|------------|
| `python` shows "not found" | Python is not installed or not in your PATH | Reinstall Python and check "Add to PATH" |
| Typing `python exercise.py` inside `>>>` | You are already in Python -- this command is for the terminal | Type `exit()` first to get back to the terminal |
| Forgetting quotes around text | Python treats unquoted words as variable names | Always put text in quotes: `"like this"` |

## What to explore next

1. Try calculating your age in days: `your_age * 365`
2. Try exponents with `**`: what is `2 ** 10`?
