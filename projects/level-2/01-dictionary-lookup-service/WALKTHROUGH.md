# Dictionary Lookup Service — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently.

## Thinking Process

When you see "dictionary lookup service," your first question should be: where does the data come from, and what format is it in? The data lives in a text file with one `key=value` pair per line. So the first job is parsing that file into a Python dict. Think about what could go wrong at this stage -- definitions that contain `=` signs, duplicate keys, and inconsistent capitalization.

Next, think about what happens when someone searches for a term that does not exist. You could just say "not found," but a better experience is to suggest close matches. This is where the `difflib` module comes in -- it can find strings that are similar to the search term. Think of it like a spell checker: you type "pythn" and it says "did you mean python?"

Finally, consider normalization. If the dictionary has "Python" and the user searches for "python," should that match? Almost certainly yes. Normalizing to lowercase at both load time and search time solves this cleanly.

## Step 1: Load the Dictionary File

**What to do:** Write a function that reads a text file and builds a Python dict from `key=value` lines.

**Why:** Everything else depends on having the data in a Python dict. Get this right first, and the rest flows naturally.

```python
def load_dictionary(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8").splitlines()

    entries = {
        parts[0].strip().lower(): parts[1].strip()
        for line in raw
        if "=" in line
        for parts in [line.split("=", 1)]
    }
    return entries
```

Three details to notice:

- **`line.split("=", 1)`** splits on the **first** `=` only. This is critical because definitions might contain `=` signs (like `formula=E=mc2`). Without the `1`, that would break into three parts.
- **`.lower()` on keys** makes lookups case-insensitive.
- **`if "=" in line`** skips blank lines and comments.

**Predict:** If the file has two lines with the same key (e.g., `python=...` appears twice), which definition ends up in the dict? The first one or the last one?

## Step 2: Look Up a Single Term

**What to do:** Write a `lookup()` function that searches the dictionary for a term and returns a structured result dict.

**Why:** Returning a structured dict (not just a string) means the caller can programmatically check `result["found"]` and decide what to do. This is better than returning `None` or raising an exception for missing terms.

```python
import difflib

def lookup(dictionary: dict[str, str], term: str) -> dict:
    normalised = term.strip().lower()

    try:
        definition = dictionary[normalised]
        return {
            "found": True,
            "term": normalised,
            "definition": definition,
            "suggestions": [],
        }
    except KeyError:
        suggestions = difflib.get_close_matches(
            normalised, dictionary.keys(), n=3, cutoff=0.6
        )
        return {
            "found": False,
            "term": normalised,
            "definition": None,
            "suggestions": suggestions,
        }
```

The function uses `try/except KeyError` instead of `if term in dictionary`. Both work, but `try/except` is considered more Pythonic when you expect the key to usually exist (the "happy path" is fast). This is the **EAFP** pattern (Easier to Ask Forgiveness than Permission).

**Predict:** If the dictionary contains "python" and the user searches for "pythn" (a typo), will `get_close_matches` find it? What if they search for "xyz"?

## Step 3: Batch Lookup with Enumerate

**What to do:** Write a `batch_lookup()` function that processes a list of terms and tracks their original position using `enumerate()`.

**Why:** When looking up multiple terms, the caller needs to know which result corresponds to which input. `enumerate` gives you the index alongside each item -- this is cleaner than manually tracking a counter variable.

```python
def batch_lookup(dictionary: dict[str, str], terms: list[str]) -> list[dict]:
    results = []
    for idx, term in enumerate(terms):
        result = lookup(dictionary, term)
        result["index"] = idx
        results.append(result)
    return results
```

**Predict:** If you pass `["Python", "PYTHON", "python"]`, how many unique lookups effectively happen? Are all three results identical?

## Step 4: Compute Dictionary Statistics

**What to do:** Write a `dictionary_stats()` function that uses sets and `sorted()` with a key function.

**Why:** This step practices two important patterns: set comprehensions (for unique first letters) and sorting with a custom key function (sorting terms by definition length, not alphabetically).

```python
def dictionary_stats(dictionary: dict[str, str]) -> dict:
    first_letters: set[str] = {k[0] for k in dictionary if k}

    sorted_by_length = sorted(
        dictionary.keys(),
        key=lambda k: len(dictionary[k]),
        reverse=True,
    )

    return {
        "total_entries": len(dictionary),
        "unique_first_letters": sorted(first_letters),
        "longest_definitions": sorted_by_length[:5],
        "shortest_definitions": sorted_by_length[-5:],
    }
```

The set comprehension `{k[0] for k in dictionary if k}` extracts the first character of every key. Since it is a set, duplicates are automatically removed. The `if k` guard prevents a crash on empty-string keys.

**Predict:** What does `sorted(first_letters)` do that the set alone does not? (Hint: sets have no guaranteed order.)

## Step 5: Wire Up the CLI

**What to do:** Use `argparse` to create `--dict`, `--lookup`, and `--stats` command-line options, then call your functions from `main()`.

**Why:** A CLI makes your tool usable from the terminal. `argparse` handles parsing, validation, and help text so you do not have to write that boilerplate yourself.

```python
def main() -> None:
    args = parse_args()
    dictionary = load_dictionary(Path(args.dict))

    if args.stats:
        stats = dictionary_stats(dictionary)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        return

    if args.lookup:
        results = batch_lookup(dictionary, args.lookup)
    else:
        samples = list(dictionary.keys())[:3] + ["nonexistent"]
        results = batch_lookup(dictionary, samples)

    for r in results:
        term = r["term"]
        if r["found"]:
            print(f"  {term}: {r['definition']}")
        else:
            print(f"  {term}: not found — suggestions: {r['suggestions']}")
```

**Predict:** What happens if the user runs the script with no `--lookup` and no `--stats`? Trace through the code to find out.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `line.split("=")` breaks definitions containing `=` | Default split divides on every `=` | Use `split("=", 1)` to split on first `=` only |
| Lookup is case-sensitive | Forgetting to normalize | `.lower()` both the keys (at load time) and the search term |
| `dictionary[term]` crashes on missing key | Using direct access without handling | Either use `try/except KeyError` or `dictionary.get(term)` |
| `get_close_matches` returns nothing useful | Cutoff is too high for the input | Lower the cutoff (try 0.5) or check that the dictionary has enough entries |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
9 passed
```

You can also test from the command line:

```bash
python project.py --dict data/sample_input.txt --lookup python java haskell
python project.py --dict data/sample_input.txt --stats
```

## What You Learned

- **Dict comprehensions** build dictionaries in a single expression, which is more readable than a loop when the logic is straightforward.
- **`try/except KeyError` vs `dict.get()`** are two ways to handle missing keys -- `try/except` is better when you expect the key to usually exist (the happy path is fast), while `.get()` is better when missing keys are common.
- **`difflib.get_close_matches`** provides fuzzy string matching using sequence similarity -- it compares character patterns, not meanings, so "pythn" matches "python" but "snake" does not.
