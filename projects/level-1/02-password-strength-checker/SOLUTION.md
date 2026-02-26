# Solution: Level 1 / Project 02 - Password Strength Checker

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Password Strength Checker.

Score passwords based on length, character variety, and common patterns.
Assign a strength rating from 'weak' to 'strong'.

Concepts: string methods (isupper, isdigit), boolean conditions, scoring.
"""


import argparse
import json
from pathlib import Path


# WHY a module-level list: Common passwords are data, not logic.  Keeping
# them in a named constant at the top makes the list easy to find, update,
# and eventually load from a file.
COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "abc123", "letmein",
    "admin", "welcome", "monkey", "dragon", "master",
]


# WHY check_length: Length is the single most important factor in
# password strength.  Short passwords can be brute-forced in seconds.
# Separating this into its own function makes the scoring composable.
def check_length(password: str) -> int:
    """Score based on password length.

    WHY different thresholds? -- Short passwords are trivially
    crackable.  Each length tier earns more points.
    """
    length = len(password)
    # WHY 16/12/8 thresholds: Security research shows that 8 characters
    # is the minimum for reasonable security, 12 is good, and 16+ is
    # very strong.  The tiered scoring rewards longer passwords.
    if length >= 16:
        return 3
    elif length >= 12:
        return 2
    elif length >= 8:
        return 1
    return 0


# WHY check_character_variety: Mixing character types (upper, lower,
# digit, special) exponentially increases the keyspace an attacker
# must search.  Returning a dict of booleans lets the caller see
# exactly which classes are missing.
def check_character_variety(password: str) -> dict:
    """Check which character classes are present."""
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    # WHY a manual loop instead of any(): At Level 1, an explicit loop
    # is easier to follow and debug.  The any() approach is shown in
    # the alternative below.
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            # WHY else for special: Any character that is not upper,
            # lower, or digit is a "special" character (!, @, #, etc.).
            has_special = True

    return {
        "uppercase": has_upper,
        "lowercase": has_lower,
        "digit": has_digit,
        "special": has_special,
    }


# WHY check_common: Common passwords are cracked in milliseconds by
# dictionary attacks.  Even a long common password like "letmein123"
# is weak because attackers try known passwords first.
def check_common(password: str) -> bool:
    """Return True if the password is in the common passwords list.

    WHY lowercase comparison? -- Users might type 'Password' or
    'PASSWORD' which are just as weak as 'password'.
    """
    # WHY .lower(): Case-insensitive comparison catches "Password",
    # "PASSWORD", "pAsSwOrD" — all equally weak.
    return password.lower() in COMMON_PASSWORDS


# WHY score_password: This is the orchestrator — it calls each
# individual check, combines the scores, and maps the total to a
# human-readable strength label.
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
    # WHY sum with generator: Counting True values by summing booleans
    # is a Pythonic pattern — True == 1, False == 0.
    variety_score = sum(1 for v in variety.values() if v)
    is_common = check_common(password)
    # WHY 0 if common: A common password gets no bonus point, which
    # drags its total score down regardless of other factors.
    common_score = 0 if is_common else 1

    total = length_score + variety_score + common_score

    # WHY threshold mapping: Clear boundaries (7+, 5+, 3+) make the
    # labels predictable and easy to explain to users.
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


# WHY process_file: Separating file reading from scoring logic means
# score_password() can be tested with plain strings, and the file
# reading is isolated.
def process_file(path: Path) -> list[dict]:
    """Read passwords from a file (one per line) and score each."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    # WHY list comprehension with filter: Skip blank lines so empty
    # lines in the file do not produce meaningless zero-score results.
    return [score_password(line.strip()) for line in lines if line.strip()]


# WHY parse_args: argparse provides --input and --output flags with
# automatic help text, making the script flexible without hardcoded paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Encapsulating top-level logic in main() keeps the module
# importable.  Other code can import score_password() without running
# the full script.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Separate scoring functions (`check_length`, `check_character_variety`, `check_common`) | Each function tests one criterion and returns a clear result, making the system composable and each piece independently testable | One monolithic `score_password()` function — harder to test and modify individual rules |
| Return a detailed dict from `score_password()` | Callers can see the breakdown (length score, variety, common status) and display rich feedback | Return only the total score or strength label — loses diagnostic detail |
| Case-insensitive common password check | "PASSWORD" and "Password" are just as weak as "password"; attackers try all case variations | Case-sensitive comparison — would miss obvious weak passwords |
| Threshold-based strength labels | Clear, predictable boundaries that users can understand and reason about | Percentage-based scoring — harder to explain thresholds to users |

## Alternative approaches

### Approach B: Using `any()` with generator expressions

```python
def check_character_variety_pythonic(password: str) -> dict:
    """Check character classes using any() — more concise."""
    # WHY any(): any() short-circuits as soon as it finds one True,
    # making it both readable and efficient for "does at least one
    # character match this condition?" checks.
    return {
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(not c.isalnum() for c in password),
    }
```

**Trade-off:** The `any()` approach is more Pythonic and concise — four lines instead of a loop with four flags. However, it iterates over the password up to four times (once per check), while the manual loop iterates only once. For short passwords this does not matter, but the manual loop is easier to trace through mentally when learning. Use `any()` once you are comfortable with generator expressions.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Empty password (blank line in file) | `check_length` returns 0, `check_character_variety` returns all False, total score is 1 (not common) — labeled "very weak" | The list comprehension in `process_file()` skips blank lines; add an explicit empty-password guard if accepting interactive input |
| Very long password (1000+ characters) | Works correctly — `len()`, `isupper()`, and `isdigit()` handle strings of any length | No special handling needed; Python strings have no practical length limit |
| Password is literally `"password"` | `check_common()` catches it and withholds 1 point, pushing the score lower | The common password list is checked case-insensitively |
| Password contains Unicode (e.g., emojis, accented letters) | `isupper()`/`islower()`/`isdigit()` work correctly on Unicode; emojis fall into "special" | No extra handling needed; Python 3 string methods are Unicode-aware |

## Key takeaways

1. **Multi-criteria scoring systems decompose into independent checks.** Each check (length, variety, common) is a pure function that takes input and returns a result. Combining them in `score_password()` is just addition — this composable pattern appears in everything from credit scoring to search ranking.
2. **Booleans are integers in Python.** `True == 1` and `False == 0`, so `sum(1 for v in variety.values() if v)` counts how many character classes are present. This shorthand appears constantly in Python codebases.
3. **This scoring pattern connects to real-world password policies** used by registration forms and password managers. The next step would be adding sequential-character detection and dictionary word checks, which you will encounter in later levels.
