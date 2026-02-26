"""
AI Code Review — Optional educational code review using Claude API.

Reads a project file and its README, then sends both to Claude for a
learning-focused review: strengths, areas for improvement, and next steps.

Usage:
    python tools/ai_review.py projects/level-3/01-package-layout-starter/project.py

Requires:
    - ANTHROPIC_API_KEY environment variable
    - pip install anthropic

No external dependencies beyond the anthropic SDK.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def find_readme(project_file: Path) -> str | None:
    """Look for a README.md in the same directory or parent directory."""
    candidates = [
        project_file.parent / "README.md",
        project_file.parent.parent / "README.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8", errors="replace")
    return None


def build_review_prompt(code: str, readme: str | None, filename: str) -> str:
    """Build the educational review prompt for Claude."""
    context_section = ""
    if readme:
        context_section = f"""
## Project README (for context)

```markdown
{readme}
```
"""

    return f"""You are a friendly, encouraging Python tutor reviewing a student's code.
The student is learning Python through a structured curriculum. Your job is to
help them grow — not to criticize.

## File under review: {filename}

```python
{code}
```
{context_section}

Please provide a review with these sections:

### Strengths
What the student did well (be specific — point to actual lines or patterns).

### Areas for Improvement
Concrete suggestions ranked by importance. For each:
- What to change
- Why it matters
- A short code example showing the improvement

### Suggested Next Steps
2-3 specific things the student should practice or learn next based on this code.

Keep your tone supportive and educational. Use plain language."""


def run_review(file_path: str) -> None:
    """Run the AI review on a given file."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set.\n")
        print("To use AI code review, you need a Claude API key:")
        print("  1. Sign up at https://console.anthropic.com/")
        print("  2. Create an API key")
        print("  3. Set the environment variable:")
        print("     export ANTHROPIC_API_KEY=sk-ant-...")
        print("     (or add it to your .env file)")
        sys.exit(1)

    target = Path(file_path).resolve()
    if not target.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    if not target.suffix == ".py":
        print(f"Expected a .py file, got: {target.suffix}")
        sys.exit(1)

    code = target.read_text(encoding="utf-8", errors="replace")
    if not code.strip():
        print(f"File is empty: {file_path}")
        sys.exit(1)

    readme = find_readme(target)
    prompt = build_review_prompt(code, readme, target.name)

    try:
        import anthropic
    except ImportError:
        print("The 'anthropic' package is not installed.\n")
        print("Install it with:")
        print("  pip install anthropic")
        sys.exit(1)

    print(f"\nReviewing: {target.relative_to(REPO_ROOT) if target.is_relative_to(REPO_ROOT) else target}")
    if readme:
        print(f"Context:   README.md found")
    print(f"Sending to Claude for review...\n")
    print("-" * 60)

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    review_text = message.content[0].text
    print(review_text)
    print("-" * 60)
    print(f"\nTokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="AI-powered educational code review using Claude API.",
    )
    parser.add_argument(
        "file", type=str,
        help="path to the Python file to review (e.g. projects/level-3/01-.../project.py)",
    )
    args = parser.parse_args()
    run_review(args.file)


if __name__ == "__main__":
    main()
