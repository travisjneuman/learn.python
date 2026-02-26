# Debugging Methodology — Part 1: Approach and Mental Models

[← Back to Overview](./debugging-methodology.md) · [Part 2: Tools and Techniques →](./debugging-methodology-part2.md)

---

Debugging is the systematic process of finding and fixing bugs. It is not about staring at code until you see the problem — it is a repeatable method that works on any bug, in any language. The best debuggers are not the smartest programmers; they are the most methodical.

## Why This Matters

You will spend more time debugging than writing new code. A systematic approach turns frustrating hours of "why does this not work?" into a predictable process. The method described here — Reproduce, Isolate, Hypothesize, Test, Fix, Verify, Prevent — works for everything from a typo to a race condition.

## The 7-step method

### 1. Reproduce — make the bug happen reliably

Before fixing anything, you need to see the bug yourself. Write down the exact steps:

```
1. Run `python app.py`
2. Enter username "alice"
3. Enter password "test123"
4. Click "View Profile"
5. ERROR: KeyError: 'email'
```

If you cannot reproduce the bug, you cannot verify you fixed it. Ask: "Does this happen every time? Only with certain inputs? Only on certain machines?"

### 2. Isolate — narrow down where the bug is

Remove variables until you find the smallest piece of code that still has the bug:

```python
# The program is 500 lines. Where is the bug?

# Start by adding print statements at key points:
print("DEBUG: got to step 1")
print(f"DEBUG: user_data = {user_data}")
print("DEBUG: got to step 2")

# Or use the binary search method:
# 1. Add a print halfway through the code
# 2. Is the data correct at that point?
#    - YES → bug is in the second half
#    - NO  → bug is in the first half
# 3. Repeat until you find the exact line
```

### 3. Hypothesize — form a theory

Based on the error and where it occurs, make a specific guess:

- "The `email` key is missing because the API response changed format"
- "The variable is None because the database query returned no results"
- "The loop runs one too many times because I used `<=` instead of `<`"

Do NOT start changing code randomly. Have a theory first.

### 4. Test — verify your hypothesis

Test your theory with the smallest possible experiment:

```python
# Hypothesis: user_data doesn't have an 'email' key
# Test: print the actual keys
print(f"DEBUG: keys = {user_data.keys()}")

# Hypothesis: the API is returning a different format
# Test: print the raw response
print(f"DEBUG: response = {response.json()}")
```

If your hypothesis was wrong, go back to step 3 with new information.

### 5. Fix — make the minimum change

Fix only the bug. Do not refactor surrounding code, add features, or "improve" things. Keep the change as small as possible:

```python
# Before (buggy):
email = user_data["email"]

# After (fixed):
email = user_data.get("email", "no-email@example.com")
```

### 6. Verify — confirm the fix works

Run the same reproduction steps from step 1. The bug should be gone. Also check that you did not break anything else — run the test suite.

### 7. Prevent — stop this bug from coming back

Write a test that catches this specific bug:

```python
def test_missing_email_field():
    user_data = {"name": "Alice"}    # No email key
    result = process_user(user_data)
    assert result.email == "no-email@example.com"
```

Ask: "Why did this bug happen? Could it happen elsewhere? Is there a systematic fix?"

## Debugging strategies by error type

### `TypeError`
Usually means you passed the wrong type. Print the types of all arguments:
```python
print(f"DEBUG: {type(x)=}, {type(y)=}")
```

### `KeyError` / `IndexError`
Print the actual keys/length before accessing:
```python
print(f"DEBUG: keys = {data.keys()}")
print(f"DEBUG: len = {len(my_list)}")
```

### `AttributeError`
The object is not the type you think. Print what it actually is:
```python
print(f"DEBUG: {type(obj)=}, {dir(obj)=}")
```

### Logic errors (wrong output, no crash)
Add assertions to check your assumptions:
```python
assert len(results) > 0, "Expected results but got empty list"
assert isinstance(user, dict), f"Expected dict, got {type(user)}"
```

---

| [← Overview](./debugging-methodology.md) | [Part 2: Tools and Techniques →](./debugging-methodology-part2.md) |
|:---|---:|
