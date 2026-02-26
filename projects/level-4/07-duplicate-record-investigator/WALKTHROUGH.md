# Duplicate Record Investigator — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 30 minutes attempting it independently.

## Thinking Process

This project goes beyond simple deduplication (Level 2, project 06). There, you checked for exact matches. Here, you investigate **fuzzy duplicates** -- records that are not identical but are probably the same entity. "Jon Smith" and "John Smith" are likely the same person. "alice@gmail.com" and "alice@gmial.com" are probably the same email with a typo.

The key question is: how do you quantify "similarity" between two strings? This project uses **character bigrams** and **Jaccard similarity**. Break each string into pairs of consecutive characters ("hello" becomes {"he", "el", "ll", "lo"}), then compare the sets. The ratio of shared bigrams to total bigrams gives a similarity score between 0 and 1.

Think about the algorithm structure: you need to compare every record against every other record. That is an O(n^2) nested loop. For small datasets (hundreds to low thousands of rows), this is fine. For larger datasets, you would need more sophisticated techniques like blocking or locality-sensitive hashing -- but those are beyond the scope of this project.

## Step 1: Generate Character Bigrams

**What to do:** Write a function that breaks a string into a set of two-character substrings.

**Why:** Bigrams capture local character patterns, making similarity robust to typos and minor variations. "Jon" and "John" share the bigram "Jo" and score as similar. Single-character comparison would not capture this kind of structural similarity.

```python
def bigrams(text: str) -> set[str]:
    t = text.lower().strip()
    return {t[i:i + 2] for i in range(len(t) - 1)} if len(t) >= 2 else {t}
```

This is a set comprehension. For `"hello"`, it produces `{"he", "el", "ll", "lo"}`. The `if len(t) >= 2` guard handles single-character strings that cannot form bigrams.

**Predict:** What bigrams does `"Jon"` produce? What about `"John"`? How many bigrams do they share?

## Step 2: Compute Jaccard Similarity

**What to do:** Write a function that computes the Jaccard similarity coefficient between two strings using their bigram sets.

**Why:** Jaccard similarity is the ratio of the intersection to the union of two sets: `|A & B| / |A | B|`. It produces a number between 0 (no overlap) and 1 (identical sets). This is simpler to implement than edit distance and works well for short strings.

```python
def jaccard_similarity(a: str, b: str) -> float:
    set_a = bigrams(a)
    set_b = bigrams(b)
    if not set_a and not set_b:
        return 1.0  # both empty = same
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0
```

**Predict:** What is the Jaccard similarity between "hello" and "hallo"? Work it out by hand:
- bigrams("hello") = {"he", "el", "ll", "lo"}
- bigrams("hallo") = {"ha", "al", "ll", "lo"}
- intersection = ?
- union = ?
- similarity = ?

## Step 3: Compare All Record Pairs

**What to do:** Write the `find_duplicates()` function that compares every pair of records for both exact and fuzzy matches.

**Why:** The nested loop examines all unique pairs. For each pair, it first checks for an exact match (fast, definitive), and only if that fails, it computes the fuzzy similarity score.

```python
def find_duplicates(rows, key_fields, threshold=0.8):
    duplicates = []

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            row_a = rows[i]
            row_b = rows[j]

            # Exact match check
            exact = all(
                row_a.get(f, "").strip().lower() == row_b.get(f, "").strip().lower()
                for f in key_fields
            )

            if exact:
                duplicates.append({
                    "row_a": i + 1, "row_b": j + 1,
                    "match_type": "exact", "similarity": 1.0,
                    "fields_compared": key_fields,
                })
                continue

            # Fuzzy match check
            scores = []
            for f in key_fields:
                scores.append(jaccard_similarity(row_a.get(f, ""), row_b.get(f, "")))

            avg_score = sum(scores) / len(scores) if scores else 0.0
            if avg_score >= threshold:
                duplicates.append({
                    "row_a": i + 1, "row_b": j + 1,
                    "match_type": "fuzzy",
                    "similarity": round(avg_score, 3),
                    "fields_compared": key_fields,
                })

    return duplicates
```

Two design details to notice:

- **`range(i + 1, len(rows))`** ensures each pair is compared only once. Without `i + 1`, you would compare (A, B) and (B, A).
- **Averaging scores across key fields** means both the name and email must be similar, not just one of them. A record where only the email matches but the name is completely different would score below threshold.

**Predict:** With 7 records, how many pair comparisons does this nested loop make? (Hint: it is the combination formula n*(n-1)/2.)

## Step 4: Load CSV Data

**What to do:** Write a function that reads a CSV file using Python's `csv.DictReader`.

**Why:** `csv.DictReader` handles quoting, escaping, and header parsing correctly. It is more robust than splitting on commas manually (which breaks on values like `"Smith, Jr."`).

```python
import csv

def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))
```

**Predict:** Why does the code read the entire file into a string first, then pass `text.splitlines()` to DictReader, instead of opening the file directly? (Hint: this is a pattern for testability -- you can pass any list of strings.)

## Step 5: Write the Report and CLI

**What to do:** Wire everything together in a `run()` function that loads data, finds duplicates, and writes a JSON report.

**Why:** The runner function follows the same pattern from earlier projects: load, process, write. The CLI parses the key fields from a comma-separated string.

```python
def run(input_path, output_path, key_fields, threshold=0.8):
    rows = load_csv(input_path)
    duplicates = find_duplicates(rows, key_fields, threshold)

    report = {
        "total_records": len(rows),
        "key_fields": key_fields,
        "threshold": threshold,
        "duplicate_pairs_found": len(duplicates),
        "duplicates": duplicates,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
```

**Predict:** What happens if the user specifies a very low threshold like 0.1? Would most records be flagged as duplicates? Why or why not?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Comparing (A,B) and (B,A) | Using `range(len(rows))` for both loops | Inner loop starts at `i + 1` |
| Not normalizing before comparing | "Alice" and "alice" treated as different | `.strip().lower()` in both exact and fuzzy comparisons |
| Threshold too low = false positives | Short strings have high bigram overlap | Use 0.8 as default; adjust based on data |
| Key field not in CSV | Typo in `--keys` argument | Validate that all key fields exist in the CSV headers |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
6 passed
```

Test from the command line:

```bash
python project.py --input data/sample_input.csv --output data/duplicates_report.json --keys name,email --threshold 0.8
```

Then inspect `data/duplicates_report.json` to see which pairs were flagged and their similarity scores.

## What You Learned

- **Character bigrams** break strings into overlapping pairs, capturing local structure that single-character comparison misses. "Jon" and "John" share meaningful patterns.
- **Jaccard similarity** (intersection over union) provides a clean 0-to-1 similarity metric using set operations you already know from Level 2.
- **O(n^2) comparison** is acceptable for small datasets but becomes a bottleneck at scale. In production, techniques like blocking (only comparing records that share a common attribute) reduce the number of comparisons.
