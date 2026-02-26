# Solution: Level 0 / Project 04 - Yes No Questionnaire

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Yes/No Questionnaire.

Present questions one at a time, collect yes/no answers,
tally the results, and show a summary.

Concepts: boolean logic, input normalisation, counters, lists, dicts.
"""


def normalise_answer(raw: str) -> str:
    """Convert a raw answer string to 'yes', 'no', or 'invalid'.

    WHY normalise? -- Users type in many ways: 'YES', 'y', 'Yeah'.
    Normalising means we only have to check a small set of values
    instead of every possible spelling.
    """
    # WHY strip().lower(): strip() removes leading/trailing whitespace
    # (e.g. "  yes  " becomes "yes").  lower() converts uppercase to
    # lowercase (e.g. "YES" becomes "yes").  Together, they handle the
    # most common input variations in two method calls.
    cleaned = raw.strip().lower()

    # WHY use tuples for membership checks: Checking `cleaned in (...)`
    # is faster and more readable than writing six if/elif branches.
    # Adding a new synonym (e.g. "sure") means adding one string.
    if cleaned in ("yes", "y", "yeah", "yep", "true", "1"):
        return "yes"
    if cleaned in ("no", "n", "nah", "nope", "false", "0"):
        return "no"

    # WHY return "invalid" instead of raising an error: In a questionnaire,
    # invalid answers are data points too — we count them.  Raising an error
    # would stop the whole program on one bad answer.
    return "invalid"


def tally_answers(answers: list) -> dict:
    """Count how many yes, no, and invalid answers were given.

    WHY return a dict? -- Dicts let us label each count with a
    descriptive key, making the output self-documenting.
    """
    # WHY initialise all keys to 0: Starting with known keys means
    # we never hit a KeyError when incrementing.  This is safer than
    # using dict.get() for beginners.
    counts = {"yes": 0, "no": 0, "invalid": 0}

    for answer in answers:
        # WHY normalise inside the tally: Each raw answer gets cleaned
        # before counting.  The caller passes raw strings; this function
        # handles normalisation internally.
        normalised = normalise_answer(answer)
        counts[normalised] += 1

    total = len(answers)
    counts["total"] = total

    # WHY check total > 0: Dividing by zero crashes.  If no answers
    # were given, percentages should be 0.0, not an error.
    if total > 0:
        counts["yes_percent"] = round(counts["yes"] / total * 100, 1)
        counts["no_percent"] = round(counts["no"] / total * 100, 1)
    else:
        counts["yes_percent"] = 0.0
        counts["no_percent"] = 0.0

    return counts


if __name__ == "__main__":
    questions = [
        "Do you enjoy learning new things?",
        "Have you used a computer before today?",
        "Do you like solving puzzles?",
        "Are you excited to learn Python?",
        "Do you prefer working alone?",
    ]

    print("=== Yes/No Questionnaire ===")
    print(f"Answer {len(questions)} questions with yes or no.\n")

    answers = []
    # WHY enumerate with start=1: It gives us a human-friendly number
    # (1, 2, 3...) alongside each question.  Computers count from 0,
    # but humans count from 1.
    for i, question in enumerate(questions, start=1):
        answer = input(f"  {i}. {question} ")
        answers.append(answer)

    tally = tally_answers(answers)

    print("\n=== Results ===")
    print(f"  Total responses: {tally['total']}")
    print(f"  Yes: {tally['yes']} ({tally['yes_percent']}%)")
    print(f"  No:  {tally['no']} ({tally['no_percent']}%)")
    print(f"  Invalid: {tally['invalid']}")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `normalise_answer()` accepts many synonyms for yes/no | Real users type "y", "YES", "Yeah" — accepting common variants reduces "invalid" counts and improves user experience | Accept only "yes" and "no" exactly — simpler code but frustrating for users who type "y" |
| Return `"invalid"` for unrecognised input | Invalid answers are counted and reported, giving the questionnaire administrator useful data about question clarity | Raise `ValueError` — stops the program; or silently skip — loses data |
| `tally_answers()` calls `normalise_answer()` internally | The caller passes raw strings and gets clean results. Normalisation is an implementation detail hidden from the caller | Require the caller to normalise first — splits responsibility and risks forgotten normalisation |
| Percentages use `round(..., 1)` | One decimal place (e.g. `80.0%`) is precise enough for a survey and avoids long floating-point decimals | No rounding — `80.00000000000001%` looks broken to a beginner |

## Alternative approaches

### Approach B: Using `collections.Counter` for tallying

```python
from collections import Counter

def tally_answers(answers: list) -> dict:
    normalised = [normalise_answer(a) for a in answers]
    counter = Counter(normalised)

    total = len(answers)
    return {
        "yes": counter.get("yes", 0),
        "no": counter.get("no", 0),
        "invalid": counter.get("invalid", 0),
        "total": total,
        "yes_percent": round(counter.get("yes", 0) / total * 100, 1) if total else 0.0,
        "no_percent": round(counter.get("no", 0) / total * 100, 1) if total else 0.0,
    }
```

**Trade-off:** `Counter` from the standard library does the counting in one line — no manual loop needed. However, at Level 0, understanding the manual counting loop (`counts[key] += 1`) teaches the fundamental pattern behind tools like `Counter`. Once you understand the manual approach, you can switch to `Counter` in later projects for brevity.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters only spaces or blank for every answer | `normalise_answer("   ")` returns `"invalid"` because `"".strip()` is empty, which does not match any yes/no variant. All answers count as invalid | Already handled — the function returns `"invalid"` for empty strings |
| User enters `"YES!!!"` with punctuation | `normalise_answer("YES!!!")` returns `"invalid"` because `"yes!!!"` does not match `"yes"` | Strip punctuation before checking: `cleaned = raw.strip().lower().strip("!?.")` |
| Empty answers list (`tally_answers([])`) | Returns `{"yes": 0, "no": 0, "invalid": 0, "total": 0, "yes_percent": 0.0, "no_percent": 0.0}` — no crash | Already handled by the `if total > 0` guard |
| User types `"y e s"` with spaces between letters | `normalise_answer("y e s")` returns `"invalid"` because `"y e s"` does not match any variant | Could remove internal spaces, but that risks false positives. Better to accept this as invalid |

## Key takeaways

1. **Input normalisation is fundamental.** Users never type exactly what you expect. Stripping whitespace and lowering case before comparison handles 90% of input variations. This pattern appears in form validation, search engines, and database queries.
2. **Guard against division by zero.** Whenever you divide, ask: "Can the denominator ever be zero?" If yes, check first. This is one of the most common beginner bugs and appears in every project that computes averages or percentages.
3. **Membership testing with `in` is cleaner than chained `if/elif`.** Writing `if x in ("yes", "y", "yeah")` is shorter and easier to extend than writing separate branches for each value. You will use this pattern in data validation, command parsing, and filtering.
4. **Returning "invalid" instead of crashing builds robust programs.** In real applications, bad input is normal — you handle it, count it, and keep going. This is an early lesson in defensive programming that becomes critical as your programs grow.
