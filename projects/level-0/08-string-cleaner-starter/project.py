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
        # Keep letters, digits, and spaces.
        if char.isalnum() or char == " ":
            cleaned.append(char)
    # Join the list back into a single string.
    return "".join(cleaned)


def collapse_spaces(text: str) -> str:
    """Replace multiple consecutive spaces with a single space.

    WHY a while loop? -- We keep replacing double-spaces until none
    remain.  This is a simple approach that handles any number of
    consecutive spaces.
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
    result = strip_whitespace(text)
    result = normalise_case(result)
    result = remove_special_characters(result)
    result = collapse_spaces(result)
    return result


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
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
        print(f"  BEFORE: {text!r}")
        print(f"  AFTER:  {cleaned!r}")
        print()
        count += 1

    print(f"Cleaned {count} strings. Goodbye!")
