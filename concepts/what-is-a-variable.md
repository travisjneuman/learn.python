# What is a Variable?

A variable is a name that holds a value. You create it by writing a name, then `=`, then the value.

```python
name = "Alice"
age = 30
is_student = True
```

Think of it like a labeled jar. The label is the name. The contents are the value. You can:
- **Look at** the contents: `print(name)` shows `Alice`
- **Replace** the contents: `name = "Alice"` — now it holds `"Alice"`
- **Use** the contents in calculations: `next_year = age + 1`

## Rules for naming variables
- Must start with a letter or underscore (not a number)
- Can contain letters, numbers, and underscores
- Case-sensitive: `Name` and `name` are different variables
- Convention: use `lowercase_with_underscores` (called "snake_case")

## Good names vs bad names

```python
# Good — describes what the value represents
student_count = 42
max_temperature = 98.6
is_active = True

# Bad — vague or misleading
x = 42
temp = 98.6  # temp... temperature? temporary?
flag = True  # flag for what?
```

## Common mistakes

**Using = instead of ==:**
```python
x = 5       # This STORES 5 in x
x == 5      # This CHECKS if x equals 5 (returns True or False)
```

**Forgetting quotes for text:**
```python
name = Alice    # Error! Python thinks Alice is a variable name
name = "Alice"  # Correct — quotes make it text (a string)
```

**Using a variable before creating it:**
```python
print(score)     # Error! score does not exist yet
score = 100      # This line creates it
print(score)     # Now it works
```

## Related exercises
- [Level 00, Exercise 04 — Variables](../projects/level-00-absolute-beginner/04-variables/)

---

## Practice This

- [Module: 04 Fastapi Web / 01 Hello Fastapi](../projects/modules/04-fastapi-web/01-hello-fastapi/README.md)
- [Module: 05 Async Python / 04 Producer Consumer](../projects/modules/05-async-python/04-producer-consumer/README.md)
- [Module: 07 Data Analysis / 01 Pandas Basics](../projects/modules/07-data-analysis/01-pandas-basics/README.md)
- [Module: 09 Docker Deployment / 03 Docker Compose](../projects/modules/09-docker-deployment/03-docker-compose/README.md)

**Quick check:** [Take the quiz](quizzes/what-is-a-variable-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../03_SETUP_ALL_PLATFORMS.md) | [Home](../README.md) | [Next →](../projects/level-00-absolute-beginner/README.md) |
|:---|:---:|---:|
