# Solution: Level 0 / Project 06 - Word Counter Basic

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Word Counter Basic.

Type or paste text, then see word count, line count, character count,
and the most frequent words.

Concepts: string splitting, counting with dicts, sorting, text analysis.
"""


def count_words(text: str) -> int:
    """Count the number of words in a string.

    WHY split()? -- Calling split() with no arguments splits on any
    whitespace (spaces, tabs, newlines) and ignores leading/trailing
    whitespace automatically.  split(" ") would create empty strings
    from consecutive spaces; split() does not.
    """
    return len(text.split())


def count_lines(text: str) -> int:
    """Count the number of lines in a string.

    WHY splitlines()? -- It handles all line-ending styles
    (\\n, \\r\\n, \\r) so the count is correct on any OS.
    """
    # WHY check for empty text first: An empty string has no lines,
    # but splitlines("") returns [] which has length 0.  This guard
    # makes the intent explicit rather than relying on that behaviour.
    if not text:
        return 0
    return len(text.splitlines())


def count_characters(text: str) -> int:
    """Count the total number of characters (including spaces)."""
    # WHY len(): len() on a string counts every character — letters,
    # digits, spaces, punctuation, everything.  It is the simplest
    # possible implementation.
    return len(text)


def word_frequencies(text: str) -> dict:
    """Build a dictionary mapping each word to its frequency.

    WHY lowercase? -- So "The" and "the" count as the same word.
    This is called normalisation.
    """
    freq = {}
    for word in text.lower().split():
        # WHY strip punctuation: "hello!" and "hello" should be the same
        # word.  Stripping common punctuation from the edges handles cases
        # like quotes, commas, and exclamation marks around words.
        cleaned = word.strip(".,!?;:\"'()-")
        if cleaned:
            # WHY if/else instead of dict.get(): At Level 0, seeing the
            # explicit "is the key already there?" check makes the counting
            # pattern crystal clear.  Later you will learn dict.get() and
            # collections.Counter as shortcuts.
            if cleaned in freq:
                freq[cleaned] += 1
            else:
                freq[cleaned] = 1
    return freq


def top_words(freq: dict, n: int = 5) -> list:
    """Return the top-n most frequent words as (word, count) pairs.

    WHY sorted with key? -- sorted() can sort by any criterion.
    Using key=lambda item: item[1] sorts by the count (second element).
    reverse=True puts the highest counts first.
    """
    items = list(freq.items())
    # WHY .sort() with key: The lambda function tells Python to compare
    # items by their second element (the count) instead of the first
    # (the word).  This is how you do custom sorting in Python.
    items.sort(key=lambda item: item[1], reverse=True)
    # WHY [:n]: Slicing takes only the first n items from the sorted list.
    return items[:n]


def analyse_text(text: str) -> dict:
    """Run all analyses and return a summary dict.

    WHY bundle into one function? -- The caller gets a complete analysis
    with one call.  The dict structure makes it easy to print, save as
    JSON, or pass to another function.
    """
    freq = word_frequencies(text)
    top = top_words(freq, 5)

    return {
        "lines": count_lines(text),
        "words": count_words(text),
        "characters": count_characters(text),
        "unique_words": len(freq),
        # WHY list of dicts for top_words: Each entry has named fields
        # ("word" and "count") instead of tuple positions.  This makes
        # the data self-documenting when saved as JSON.
        "top_words": [{"word": w, "count": c} for w, c in top],
    }


if __name__ == "__main__":
    print("=== Word Counter ===")
    print("Type or paste text below. Enter a blank line when done.\n")

    lines = []
    while True:
        line = input()
        # WHY check for empty string: An empty line (just pressing Enter)
        # signals the user is done typing.  This is a common pattern for
        # multi-line interactive input.
        if line == "":
            break
        lines.append(line)

    if not lines:
        print("No text entered.")
    else:
        text = "\n".join(lines)
        summary = analyse_text(text)

        print("\n=== Word Count Summary ===")
        print(f"  Lines:      {summary['lines']}")
        print(f"  Words:      {summary['words']}")
        print(f"  Characters: {summary['characters']}")
        print(f"  Unique:     {summary['unique_words']}")
        print("\n  Top words:")
        for entry in summary["top_words"]:
            print(f"    {entry['word']}: {entry['count']}")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Separate functions for `count_words`, `count_lines`, `count_characters` | Each metric is independently testable. `assert count_words("hello world") == 2` is a one-line test | One big `analyse_text()` that computes everything — harder to test individual metrics |
| Manual dict counting in `word_frequencies()` | Shows the fundamental counting pattern explicitly: check if key exists, increment or initialise. This is the foundation for `Counter` | Use `collections.Counter(words)` — one line but hides the learning opportunity at Level 0 |
| `word_frequencies()` lowercases and strips punctuation | "The", "the", and "the," should all count as the same word. Without normalisation, frequencies would be fragmented | Keep case and punctuation — more "accurate" but gives misleading counts for text analysis |
| `top_words()` uses `lambda` for sorting | Introduces the concept of sorting by a custom criterion, which is essential for many Python tasks | Sort manually with a loop to find the max n times — works but is O(n*k) instead of O(n log n) |

## Alternative approaches

### Approach B: Using `collections.Counter`

```python
from collections import Counter

def word_frequencies(text: str) -> dict:
    words = text.lower().split()
    cleaned = [w.strip(".,!?;:\"'()-") for w in words if w.strip(".,!?;:\"'()-")]
    return dict(Counter(cleaned))

def top_words(freq: dict, n: int = 5) -> list:
    # Counter has a built-in most_common() method.
    return Counter(freq).most_common(n)
```

**Trade-off:** `Counter` reduces the entire counting loop to one line and provides `most_common(n)` for free. This is the approach you would use in real projects. However, at Level 0, understanding the manual `if key in dict` pattern is essential because it teaches how dictionaries work under the hood. Once you understand the manual approach, `Counter` is just a convenience wrapper.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters no text (presses Enter immediately) | `lines` is empty, program prints "No text entered." — no crash | Already handled by the `if not lines` check |
| Text contains only punctuation like `"!!! ??? ..."` | `word_frequencies()` strips all punctuation, leaving empty strings. The `if cleaned:` guard skips them, so the frequency dict is empty | Already handled by the `if cleaned` check after stripping |
| Text contains unicode like emojis | `len("hello ")` returns 7 (counts the emoji as one character). `split()` treats the emoji as part of a word. Results are technically correct | Already works. Python 3 handles unicode natively |
| Very large text (millions of words) | The dict grows large but Python handles it. `sort()` on a large list may be slow | For Level 0 this is fine. Production code would use streaming or database approaches |
| Words separated by tabs or multiple spaces | `split()` (no arguments) handles any whitespace correctly, splitting `"hello\t\tworld"` into `["hello", "world"]` | Already handled by using `split()` without arguments |

## Key takeaways

1. **Dictionary-based counting is one of the most common patterns in programming.** The loop `if key in dict: dict[key] += 1; else: dict[key] = 1` appears in word counting, log analysis, vote tallying, inventory tracking, and hundreds of other domains. Master this pattern.
2. **`split()` without arguments is smarter than `split(" ")`.** It splits on any whitespace, handles consecutive spaces, and strips leading/trailing whitespace. Always prefer `split()` over `split(" ")` for general text processing.
3. **Normalisation before counting prevents fragmented results.** If you count "The" and "the" separately, your frequency data is misleading. Lowercasing and stripping punctuation gives you the true word frequencies.
4. **Sorting with a `key` function unlocks custom ordering.** `sorted(items, key=lambda x: x[1], reverse=True)` sorts by the second element in descending order. This pattern works for sorting any data by any criterion — prices, dates, scores, or frequencies.
