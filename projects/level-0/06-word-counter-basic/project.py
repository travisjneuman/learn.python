"""Level 0 project: Word Counter Basic.

Type or paste text, then see word count, line count, character count,
and the most frequent words.

Concepts: string splitting, counting with dicts, sorting, text analysis.
"""


def count_words(text: str) -> int:
    """Count the number of words in a string.

    WHY split()? -- Calling split() with no arguments splits on any
    whitespace (spaces, tabs, newlines) and ignores leading/trailing
    whitespace automatically.
    """
    return len(text.split())


def count_lines(text: str) -> int:
    """Count the number of lines in a string.

    WHY splitlines()? -- It handles all line-ending styles
    (\\n, \\r\\n, \\r) so the count is correct on any OS.
    """
    if not text:
        return 0
    return len(text.splitlines())


def count_characters(text: str) -> int:
    """Count the total number of characters (including spaces)."""
    return len(text)


def word_frequencies(text: str) -> dict[str, int]:
    """Build a dictionary mapping each word to its frequency.

    WHY lowercase? -- So "The" and "the" count as the same word.
    This is called normalisation.
    """
    freq = {}
    for word in text.lower().split():
        # Strip common punctuation from the edges of each word.
        cleaned = word.strip(".,!?;:\"'()-")
        if cleaned:
            # If the word is already in the dict, add 1; otherwise start at 1.
            if cleaned in freq:
                freq[cleaned] += 1
            else:
                freq[cleaned] = 1
    return freq


def top_words(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Return the top-n most frequent words as (word, count) pairs.

    WHY sorted with key? -- sorted() can sort by any criterion.
    Using key=lambda item: item[1] sorts by the count (second element).
    reverse=True puts the highest counts first.
    """
    items = list(freq.items())
    items.sort(key=lambda item: item[1], reverse=True)
    return items[:n]


def analyse_text(text: str) -> dict[str, int | list[dict[str, str | int]]]:
    """Run all analyses and return a summary dict."""
    freq = word_frequencies(text)
    top = top_words(freq, 5)

    return {
        "lines": count_lines(text),
        "words": count_words(text),
        "characters": count_characters(text),
        "unique_words": len(freq),
        "top_words": [{"word": w, "count": c} for w, c in top],
    }


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== Word Counter ===")
    print("Type or paste text below. Enter a blank line when done.\n")

    lines = []
    while True:
        line = input()
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
