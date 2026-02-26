# Solution: Level 0 / Project 08 - String Cleaner Starter

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: String Cleaner Starter.

Type messy strings and see them cleaned: strip whitespace,
normalise case, remove special characters, collapse spaces.

Concepts: string methods (strip, lower, replace), loops, character filtering.
"""


def strip_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace from a string.

    WHY strip? -- User input and file data often have invisible
    spaces or tabs at the beginning or end.  strip() removes them.
    """
    # WHY not lstrip() or rstrip(): strip() removes from both ends.
    # Using it is safer than picking a direction because you cannot
    # predict which side has the extra whitespace.
    return text.strip()


def normalise_case(text: str) -> str:
    """Convert a string to lowercase.

    WHY lowercase? -- Normalising case makes comparisons simpler.
    'Hello' and 'hello' become the same string.
    """
    return text.lower()


def remove_special_characters(text: str) -> str:
    """Keep only letters, digits, and spaces.

    WHY check each character? -- We loop through the string and
    keep only the characters we want.  isalnum() checks if a
    character is a letter or digit.
    """
    cleaned = []
    for char in text:
        # WHY isalnum() or space: isalnum() returns True for letters
        # (a-z, A-Z) and digits (0-9).  We also keep spaces because
        # they separate words.  Everything else (punctuation, symbols)
        # is dropped.
        if char.isalnum() or char == " ":
            cleaned.append(char)
    # WHY "".join(): We built a list of characters.  join() glues them
    # back into a single string.  This is faster than string concatenation
    # with += because strings are immutable — each += creates a new string.
    return "".join(cleaned)


def collapse_spaces(text: str) -> str:
    """Replace multiple consecutive spaces with a single space.

    WHY a while loop? -- We keep replacing double-spaces until none
    remain.  This is a simple approach that handles any number of
    consecutive spaces (3, 5, 10 — all reduced to 1).
    """
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def clean_string(text: str) -> str:
    """Apply all cleaning steps in order.

    WHY chain steps? -- Each function does one small job.
    Chaining them together creates a pipeline where the output
    of one step becomes the input of the next.
    """
    # WHY this specific order:
    # 1. strip_whitespace: Remove outer whitespace first so it does not
    #    interfere with later steps.
    # 2. normalise_case: Lowercase before removing specials so the
    #    character filter sees consistent input.
    # 3. remove_special_characters: Strip punctuation and symbols.
    #    This may leave gaps where characters were removed.
    # 4. collapse_spaces: Clean up any double-spaces created by the
    #    removal step.
    result = strip_whitespace(text)
    result = normalise_case(result)
    result = remove_special_characters(result)
    result = collapse_spaces(result)
    return result


if __name__ == "__main__":
    print("=== String Cleaner ===")
    print("Type messy strings and see them cleaned.")
    print("Enter a blank line to quit.\n")

    count = 0

    while True:
        text = input("Enter messy text: ")

        if text == "":
            break

        cleaned = clean_string(text)
        # WHY !r format: The !r flag shows the string with quotes and
        # escape characters visible.  "hello" displays as 'hello',
        # making it clear where the string starts and ends.
        print(f"  BEFORE: {text!r}")
        print(f"  AFTER:  {cleaned!r}")
        print()
        count += 1

    print(f"Cleaned {count} strings. Goodbye!")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Each cleaning step is a separate function | Each can be tested independently: `assert collapse_spaces("a  b") == "a b"`. Steps can be reused or reordered | One monolithic `clean_string()` that does everything — harder to test, debug, and customise |
| Pipeline order: strip, lower, remove, collapse | Stripping first removes noise. Lowering before filtering keeps filtering logic simple. Collapsing last fixes gaps left by character removal | Different order — e.g., collapsing before removing specials would miss gaps created by removal |
| `remove_special_characters()` uses a list and `join()` | Building a list and joining is O(n). Concatenating with `+=` is O(n^2) because each `+=` creates a new string in memory | Use `+=` string concatenation — simpler syntax but gets slow on long strings |
| `collapse_spaces()` uses a while loop with `replace()` | Simple and correct for any number of consecutive spaces. Easy for beginners to understand | Use `" ".join(text.split())` — more Pythonic but harder to explain at Level 0 |

## Alternative approaches

### Approach B: One-pass cleaning with `split()` and `join()`

```python
def clean_string(text: str) -> str:
    # Strip and lowercase.
    text = text.strip().lower()

    # Remove special characters.
    cleaned = "".join(c for c in text if c.isalnum() or c == " ")

    # split() + join() handles both collapsing spaces AND stripping
    # edges in one step.  split() with no arguments splits on any
    # whitespace and discards empty strings.
    return " ".join(cleaned.split())
```

**Trade-off:** This approach is more concise and arguably more Pythonic. `" ".join(text.split())` replaces both `strip_whitespace()` and `collapse_spaces()` in one line. The generator expression `(c for c in text if ...)` replaces the explicit for loop. However, it combines multiple concepts into dense expressions that may overwhelm a Level 0 learner. The pipeline approach makes each step visible and debuggable — you can print the intermediate result after each step to see what changed.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Input is already clean (e.g. `"hello world"`) | Each step is a no-op: strip does nothing, lower does nothing, no specials to remove, no doubles to collapse. Returns `"hello world"` unchanged | Already handled — the pipeline is idempotent by design |
| Input is only special characters (e.g. `"@#$%^&*"`) | `remove_special_characters()` strips everything, leaving an empty string `""`. `collapse_spaces()` gets `""` and returns `""` | Already handled — returns empty string without error |
| Input has tab characters (e.g. `"hello\tworld"`) | `strip_whitespace()` removes leading/trailing tabs. But internal tabs survive because `remove_special_characters()` only keeps `isalnum()` and `" "`. A tab is not a space, so it gets removed, joining the words: `"helloworld"` | To preserve word boundaries, replace tabs with spaces before filtering: `text = text.replace("\t", " ")` |
| Input has newline characters | Same as tabs — `\n` is not `isalnum()` or `" "`, so it gets removed. Words across lines would merge | Replace `\n` with spaces before filtering to preserve word boundaries |
| Very long input (millions of characters) | The while loop in `collapse_spaces()` runs at most log2(max_consecutive_spaces) times. For normal text, this is 2-3 iterations | Already efficient enough for any realistic input |

## Key takeaways

1. **Small, single-purpose functions compose into powerful pipelines.** Each cleaning step does one thing. Chaining them creates a multi-step transformation that is easy to test, debug, and extend. This "pipeline" pattern appears in data processing, web frameworks, and Unix command-line tools.
2. **String building with lists and `join()` is faster than `+=`.** Because strings are immutable in Python, each `+=` creates a brand-new string, copying all previous characters. Appending to a list and joining once at the end is O(n) instead of O(n^2).
3. **Order of operations matters in data cleaning.** If you collapse spaces before removing special characters, the removal step might create new double-spaces that never get cleaned. The order strip-lower-remove-collapse is a reliable default sequence.
4. **`isalnum()` is your go-to character filter.** It returns `True` for letters and digits, `False` for everything else. Combined with the space check, it handles the most common "keep only clean characters" use case. You will use this pattern in search indexing, form validation, and data import pipelines.
