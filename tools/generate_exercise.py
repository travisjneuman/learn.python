"""
Exercise Variation Generator — Create new practice exercises using Claude API.

Generates a complete exercise with README, starter code, and test file,
tailored to a specific curriculum level and topic.

Usage:
    python tools/generate_exercise.py --level 3 --topic "file handling" --output practice/generated/
    python tools/generate_exercise.py --level 0 --topic "string methods"
    python tools/generate_exercise.py --level 7 --topic "async HTTP requests" --output practice/generated/

Requires:
    - ANTHROPIC_API_KEY environment variable
    - pip install anthropic

Output directory defaults to practice/generated/ if not specified.
"""

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

LEVEL_DESCRIPTIONS = {
    0: "Absolute beginner. Variables, print, input, basic if/else, simple for loops, functions. No imports beyond builtins.",
    1: "Beginner. File I/O, string methods, basic data structures (lists, dicts), csv module, simple error handling.",
    2: "Early intermediate. Classes, list comprehensions, pathlib, json module, basic testing with pytest.",
    3: "Intermediate. Package structure, imports, logging, argparse, type hints, virtual environments.",
    4: "Solid intermediate. Decorators, context managers, generators, itertools, functools, dataclasses.",
    5: "Upper intermediate. HTTP requests, API consumption, regex, datetime, advanced testing (mocking, fixtures).",
    6: "Lower advanced. SQL/databases, SQLAlchemy ORM, data modeling, migrations, connection management.",
    7: "Advanced. REST API design, FastAPI, authentication, pagination, caching, integration testing.",
    8: "Upper advanced. Concurrency (asyncio, threading), performance profiling, fault tolerance, monitoring.",
    9: "Expert. System design, architecture patterns, observability, deployment strategies, security.",
    10: "Master. Enterprise patterns, governance, compliance, mentorship, cross-team coordination.",
}


def build_generation_prompt(level: int, topic: str) -> str:
    """Build the prompt for Claude to generate an exercise."""
    level_desc = LEVEL_DESCRIPTIONS.get(level, f"Level {level} (intermediate)")

    return f"""You are a Python curriculum designer creating a practice exercise.

## Target Level: {level}
Level description: {level_desc}

## Topic: {topic}

Generate a complete exercise with three files. Return your response as a JSON object
with exactly these keys: "readme", "starter", "tests"

### Requirements for each file:

**readme** (markdown string): A README.md with:
- Exercise title and difficulty
- Clear problem description
- Input/output examples
- Hints section (progressive, don't give away the answer)
- Stretch goals for students who finish early

**starter** (python string): A project.py starter file with:
- Module docstring explaining the task
- Function stubs with docstrings and type hints
- # TODO comments guiding the student
- NO implementation (just `pass` or `raise NotImplementedError`)
- Appropriate for level {level} — do not use concepts above this level

**tests** (python string): A test_project.py file with:
- pytest tests covering the main requirements
- At least 5 test functions
- Edge cases appropriate for the level
- Clear test names that describe expected behavior
- Tests should pass when the student correctly implements the stubs

Return ONLY valid JSON with these three keys. No markdown code fences around the JSON."""


def parse_generated_files(response_text: str) -> dict:
    """Parse Claude's response into the three files."""
    # Try direct JSON parse first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from markdown code fences
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    print("Failed to parse Claude's response as JSON.")
    print("Raw response (first 500 chars):")
    print(response_text[:500])
    sys.exit(1)


def write_exercise(output_dir: Path, files: dict, level: int, topic: str) -> Path:
    """Write the generated exercise files to disk."""
    # Create a slug from the topic
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    exercise_dir = output_dir / f"level-{level}-{slug}"
    exercise_dir.mkdir(parents=True, exist_ok=True)

    readme_path = exercise_dir / "README.md"
    readme_path.write_text(files["readme"], encoding="utf-8")

    starter_path = exercise_dir / "project.py"
    starter_path.write_text(files["starter"], encoding="utf-8")

    tests_dir = exercise_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    test_path = tests_dir / "test_project.py"
    test_path.write_text(files["tests"], encoding="utf-8")

    return exercise_dir


def run_generate(level: int, topic: str, output: str) -> None:
    """Generate an exercise using Claude API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set.\n")
        print("To use the exercise generator, you need a Claude API key:")
        print("  1. Sign up at https://console.anthropic.com/")
        print("  2. Create an API key")
        print("  3. Set the environment variable:")
        print("     export ANTHROPIC_API_KEY=sk-ant-...")
        print("     (or add it to your .env file)")
        sys.exit(1)

    if level < 0 or level > 10:
        print(f"Level must be 0-10, got: {level}")
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("The 'anthropic' package is not installed.\n")
        print("Install it with:")
        print("  pip install anthropic")
        sys.exit(1)

    output_dir = Path(output).resolve() if output else REPO_ROOT / "practice" / "generated"

    prompt = build_generation_prompt(level, topic)

    print(f"Generating exercise:")
    print(f"  Level: {level}")
    print(f"  Topic: {topic}")
    print(f"  Output: {output_dir}")
    print(f"\nSending to Claude...\n")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text
    files = parse_generated_files(response_text)

    # Validate required keys
    for key in ("readme", "starter", "tests"):
        if key not in files:
            print(f"Missing '{key}' in generated output.")
            sys.exit(1)

    exercise_dir = write_exercise(output_dir, files, level, topic)

    print(f"Exercise generated successfully!\n")
    print(f"  {exercise_dir}/")
    print(f"    README.md      — Exercise description")
    print(f"    project.py     — Starter code with stubs")
    print(f"    tests/")
    print(f"      test_project.py — pytest tests")
    print(f"\nTo start working:")
    print(f"  cd {exercise_dir}")
    print(f"  # Read the README, then implement project.py")
    print(f"  python -m pytest tests/ -v")
    print(f"\nTokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate practice exercises using Claude API.",
    )
    parser.add_argument(
        "--level", type=int, required=True,
        help="curriculum level (0-10)",
    )
    parser.add_argument(
        "--topic", type=str, required=True,
        help='exercise topic (e.g. "file handling", "list comprehensions")',
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="output directory (default: practice/generated/)",
    )
    args = parser.parse_args()
    run_generate(args.level, args.topic, args.output)


if __name__ == "__main__":
    main()
