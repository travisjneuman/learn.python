# Regex Explained

A regular expression (regex) is a pattern that describes text. It lets you search for, match, and extract specific patterns from strings — like finding all email addresses in a document or validating that a phone number has the right format. Python's `re` module provides regex support.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/regex-explained.md) | [Quiz](quizzes/regex-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/regex-explained.md) |

<!-- modality-hub-end -->

## Why This Matters

String methods like `.find()` and `.startswith()` work for simple cases, but they fall apart when patterns are complex. "Find every word that starts with a capital letter and ends with a number" is one line of regex but dozens of lines of string manipulation. Regex is a universal skill — the same patterns work in Python, JavaScript, SQL, and most editors.

## The `re` module basics

```python
import re

text = "My phone number is 555-123-4567 and my zip is 97201"

# search — find the first match:
match = re.search(r"\d{3}-\d{3}-\d{4}", text)
if match:
    print(match.group())    # "555-123-4567"

# findall — find ALL matches:
numbers = re.findall(r"\d+", text)
print(numbers)    # ["555", "123", "4567", "97201"]

# sub — replace matches:
cleaned = re.sub(r"\d", "X", text)
print(cleaned)    # "My phone number is XXX-XXX-XXXX and my zip is XXXXX"
```

Always use **raw strings** (`r"..."`) for regex patterns — this prevents Python from interpreting backslashes before the regex engine sees them.

## Character classes

| Pattern | Matches | Example |
|---------|---------|---------|
| `\d` | Any digit (0-9) | `\d+` matches `"42"` |
| `\D` | Any non-digit | `\D+` matches `"hello"` |
| `\w` | Word character (letter, digit, underscore) | `\w+` matches `"hello_42"` |
| `\W` | Non-word character | `\W+` matches `"!! "` |
| `\s` | Whitespace (space, tab, newline) | `\s+` matches `"  \t"` |
| `\S` | Non-whitespace | `\S+` matches `"hello"` |
| `.` | Any character except newline | `a.c` matches `"abc"`, `"a3c"` |
| `[abc]` | Any of a, b, or c | `[aeiou]` matches vowels |
| `[^abc]` | Any character NOT a, b, or c | `[^0-9]` matches non-digits |
| `[a-z]` | Any lowercase letter | `[A-Za-z]` matches any letter |

## Quantifiers — how many?

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*` | Zero or more | `\d*` matches `""`, `"5"`, `"42"` |
| `+` | One or more | `\d+` matches `"5"`, `"42"` but not `""` |
| `?` | Zero or one | `colou?r` matches `"color"` and `"colour"` |
| `{3}` | Exactly 3 | `\d{3}` matches `"123"` |
| `{2,4}` | Between 2 and 4 | `\d{2,4}` matches `"12"`, `"123"`, `"1234"` |
| `{2,}` | 2 or more | `\d{2,}` matches `"12"`, `"123456"` |

## Anchors — where in the string?

| Pattern | Meaning |
|---------|---------|
| `^` | Start of string |
| `$` | End of string |
| `\b` | Word boundary |

```python
# Only match if the entire string is digits:
re.match(r"^\d+$", "12345")    # Match
re.match(r"^\d+$", "123abc")   # No match

# Word boundaries — match whole words:
re.findall(r"\bcat\b", "the cat sat on the catalog")
# ["cat"] — does NOT match "cat" inside "catalog"
```

## Groups — capturing parts of a match

Parentheses `()` create groups that capture parts of the match:

```python
text = "2024-01-15"
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)

if match:
    print(match.group())     # "2024-01-15" (entire match)
    print(match.group(1))    # "2024" (first group)
    print(match.group(2))    # "01" (second group)
    print(match.group(3))    # "15" (third group)
```

Named groups make code more readable:

```python
match = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)

if match:
    print(match.group("year"))     # "2024"
    print(match.group("month"))    # "01"
    print(match.group("day"))      # "15"
```

## `match` vs `search` vs `findall`

```python
text = "hello 42 world 99"

# match — only checks the BEGINNING of the string:
re.match(r"\d+", text)         # None (string starts with "hello")
re.match(r"\d+", "42 cats")    # Match: "42"

# search — finds the FIRST match anywhere:
re.search(r"\d+", text)        # Match: "42"

# findall — finds ALL matches, returns a list:
re.findall(r"\d+", text)       # ["42", "99"]

# finditer — like findall but returns match objects:
for m in re.finditer(r"\d+", text):
    print(f"Found {m.group()} at position {m.start()}")
```

## `re.compile` — precompile for performance

If you use the same pattern many times, compile it once:

```python
pattern = re.compile(r"\d{3}-\d{3}-\d{4}")

# Now use the pattern object:
pattern.search(text1)
pattern.findall(text2)
pattern.sub("XXX-XXX-XXXX", text3)
```

This is faster when the pattern is used in a loop.

## Common patterns

```python
# Email (simplified):
email_pattern = r"[\w.+-]+@[\w-]+\.[\w.]+"
re.findall(email_pattern, "Contact alice@example.com or bob@test.org")
# ["alice@example.com", "bob@test.org"]

# URL:
url_pattern = r"https?://[\w./\-?=&#]+"
re.findall(url_pattern, "Visit https://example.com/page?id=1")

# Phone number (US):
phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

# IP address:
ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

# Extract key=value pairs:
kv_pattern = r"(\w+)=(\w+)"
re.findall(kv_pattern, "name=Alice age=30 city=Portland")
# [("name", "Alice"), ("age", "30"), ("city", "Portland")]
```

## Flags

```python
# Case-insensitive matching:
re.findall(r"python", "Python PYTHON python", re.IGNORECASE)
# ["Python", "PYTHON", "python"]

# Multiline — ^ and $ match start/end of each line:
re.findall(r"^\w+", "hello\nworld\nfoo", re.MULTILINE)
# ["hello", "world", "foo"]

# DOTALL — . matches newlines too:
re.search(r"hello.world", "hello\nworld", re.DOTALL)
# Match: "hello\nworld"

# VERBOSE — add comments to complex patterns:
pattern = re.compile(r"""
    (\d{4})    # year
    -
    (\d{2})    # month
    -
    (\d{2})    # day
""", re.VERBOSE)
```

## Common Mistakes

**Forgetting the raw string:**
```python
# WRONG — Python interprets \b as backspace:
re.search("\bword\b", text)

# RIGHT — raw string:
re.search(r"\bword\b", text)
```

**Greedy vs lazy matching:**
```python
text = "<b>bold</b> and <b>more bold</b>"

# Greedy (default) — matches as MUCH as possible:
re.search(r"<b>.*</b>", text).group()
# "<b>bold</b> and <b>more bold</b>"

# Lazy (add ?) — matches as LITTLE as possible:
re.search(r"<b>.*?</b>", text).group()
# "<b>bold</b>"
```

**Not checking for `None` from `search()`:**
```python
# WRONG — crashes if no match:
result = re.search(r"\d+", "no numbers here").group()

# RIGHT — check first:
match = re.search(r"\d+", "no numbers here")
if match:
    result = match.group()
```

## Practice

- [Level 1 / 08 Log Level Counter](../projects/level-1/08-log-level-counter/README.md)
- [Module 01 Web Scraping](../projects/modules/01-web-scraping/) — extracting data from HTML
- [Module 02 CLI Tools](../projects/modules/02-cli-tools/) — parsing user input

**Quick check:** [Take the quiz](quizzes/regex-explained-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [re — Regular expression operations (Python docs)](https://docs.python.org/3/library/re.html)
- [Regular Expression HOWTO (Python docs)](https://docs.python.org/3/howto/regex.html)
- [regex101.com — interactive regex tester](https://regex101.com/)

---

| [← Prev](args-kwargs-explained.md) | [Home](../README.md) | [Next →](reading-documentation.md) |
|:---|:---:|---:|
