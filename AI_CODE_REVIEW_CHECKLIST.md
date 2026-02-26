# AI Code Review Checklist

For Levels 5 and above. Use this checklist after writing your solution and before moving on.

---

## Before Asking AI to Review

Complete these checks yourself first. AI review is most useful when you have already caught the obvious issues.

### Does it run without errors?

```bash
python project.py
```

If it crashes, fix it yourself first. Do not ask AI to debug a program you have not tried to run.

### Do all tests pass?

```bash
pytest -q
```

If tests fail, read the failure output. Try to fix it based on what the test expected vs what your code produced. Only ask AI for help after you have attempted a fix.

### Do I understand every line?

Go through your code line by line. For each line, ask yourself: "What does this do? Why is it here? What would happen if I removed it?"

If you cannot answer those questions for any line, that is the line you need to study, not skip.

### Have I tested edge cases?

Think about inputs that are unusual or extreme:
- Empty input (empty string, empty list, empty file)
- Very large input
- Invalid input (wrong type, missing fields, negative numbers)
- Boundary values (zero, one, the maximum)

Try at least two edge cases that the provided tests do not cover. Write them down in `notes.md`.

### Is it idiomatic Python?

Idiomatic means "the way experienced Python programmers would write it." Some questions to ask:
- Am I using list comprehensions where a simple loop would be clearer? Or vice versa?
- Am I using `with open()` for file operations (not bare `open()`)?
- Am I using `f-strings` instead of string concatenation?
- Am I using `pathlib.Path` instead of string manipulation for file paths?
- Are my variable names descriptive and following `snake_case`?

### Could I explain this to someone else?

Imagine a fellow learner asks you how your code works. Could you walk them through it without looking at the code? If not, you do not understand it well enough yet.

### What would I change if I had more time?

Write one or two things you would improve in `notes.md`. This builds the habit of critical self-review that professionals use every day. Examples:
- "I would add better error messages"
- "I would split this long function into two smaller ones"
- "I would add more tests for the edge case where the file is empty"

---

## Asking AI for Code Review

Once you have completed the checklist above, share your code with AI using this format:

```
I wrote this Python code for [project name]. It passes all tests.
Here is my code:

[paste your code]

Please review it for:
1. Code quality and readability
2. Edge cases I might have missed
3. More idiomatic Python alternatives
4. Any potential bugs

Do not rewrite it for me. Point out specific lines and explain what could be improved.
```

**Key phrase: "Do not rewrite it for me."** You want feedback, not a replacement. Rewriting it yourself after getting feedback is where the learning happens.

---

## After AI Review

- [ ] Read each suggestion carefully
- [ ] For each suggestion, decide: do I agree? Why or why not?
- [ ] Implement the changes yourself (do not copy AI rewrites)
- [ ] Run tests again to make sure your changes did not break anything
- [ ] Update `notes.md` with what you learned from the review

---

## Quick Reference

| Step | Check |
|------|-------|
| 1 | Runs without errors |
| 2 | All tests pass |
| 3 | I understand every line |
| 4 | Edge cases tested |
| 5 | Idiomatic Python |
| 6 | Could explain it aloud |
| 7 | Know what I would improve |

---

| [Home](README.md) |
|:---:|
