"""Level 1 project: Password Strength Checker.

Score passwords based on length, character variety, and common patterns.
Assign a strength rating from 'weak' to 'strong'.

Concepts: string methods (isupper, isdigit), boolean conditions, scoring.
"""


import argparse
import json
from pathlib import Path


# Common weak passwords to check against.
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "abc123", "letmein",
    "admin", "welcome", "monkey", "dragon", "master",
]


def check_length(password: str) -> int:
    """Score based on password length.

    WHY different thresholds? -- Short passwords are trivially
    crackable.  Each length tier earns more points.
    """
    length = len(password)
    if length >= 16:
        return 3
    elif length >= 12:
        return 2
    elif length >= 8:
        return 1
    return 0


def check_character_variety(password: str) -> dict:
    """Check which character classes are present.

    Returns a dict of booleans so the caller can see exactly
    which classes are missing.
    """
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special = True

    return {
        "uppercase": has_upper,
        "lowercase": has_lower,
        "digit": has_digit,
        "special": has_special,
    }


def check_common(password: str) -> bool:
    """Return True if the password is in the common passwords list.

    WHY lowercase comparison? -- Users might type 'Password' or
    'PASSWORD' which are just as weak as 'password'.
    """
    return password.lower() in COMMON_PASSWORDS


def score_password(password: str) -> dict:
    """Calculate a full strength assessment for a password.

    Scoring:
    - Length: 0-3 points
    - Each character class present: 1 point each (max 4)
    - Not a common password: 1 point
    - Max possible: 8 points
    """
    length_score = check_length(password)
    variety = check_character_variety(password)
    variety_score = sum(1 for v in variety.values() if v)
    is_common = check_common(password)
    common_score = 0 if is_common else 1

    total = length_score + variety_score + common_score

    # Map total score to a strength label.
    if total >= 7:
        strength = "strong"
    elif total >= 5:
        strength = "moderate"
    elif total >= 3:
        strength = "weak"
    else:
        strength = "very weak"

    return {
        "password": password,
        "length": len(password),
        "length_score": length_score,
        "variety": variety,
        "variety_score": variety_score,
        "is_common": is_common,
        "total_score": total,
        "strength": strength,
    }


def process_file(path: Path) -> list[dict]:
    """Read passwords from a file (one per line) and score each."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    return [score_password(line.strip()) for line in lines if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = process_file(Path(args.input))

    print("=== Password Strength Report ===\n")
    for r in results:
        print(f"  {r['password']:<25} => {r['strength'].upper():<12} (score: {r['total_score']}/8)")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n  Output written to {output_path}")


if __name__ == "__main__":
    main()
