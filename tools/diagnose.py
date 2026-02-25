"""
Diagnostic Assessment Tool — Find Your Starting Point

Interactive assessments that help learners identify where to begin
or find knowledge gaps after completing a level.

Usage:
    python tools/diagnose.py                   # list available diagnostics
    python tools/diagnose.py gate-a            # setup readiness check
    python tools/diagnose.py level-0           # terminal/IO readiness
    python tools/diagnose.py level-1           # functions readiness
    python tools/diagnose.py level-2           # collections readiness
    python tools/diagnose.py level-3           # file automation readiness

No external dependencies — uses only Python standard library.
"""

import json
import sys
from pathlib import Path

DIAG_DIR = Path(__file__).parent / "diagnostics"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_diagnostic(name):
    """Load a diagnostic assessment by name."""
    path = DIAG_DIR / f"{name}-diagnostic.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def list_diagnostics():
    """List all available diagnostic assessments."""
    print(f"\n{BOLD}Available Diagnostic Assessments{RESET}\n")
    if not DIAG_DIR.exists():
        print("  No diagnostics directory found.")
        return

    for path in sorted(DIAG_DIR.glob("*-diagnostic.json")):
        diag = load_diagnostic(path.stem.replace("-diagnostic", ""))
        if diag:
            name = path.stem.replace("-diagnostic", "")
            print(f"  {CYAN}{name:15s}{RESET} — {diag.get('title', 'No title')}")
            print(f"                  {diag.get('description', '')}")
            print(f"                  Questions: {len(diag.get('questions', []))}")
            print()

    print(f"Run with: python tools/diagnose.py <name>")
    print()


def ask_question(q, num, total):
    """Ask a single diagnostic question and return whether it was correct."""
    print(f"\n{'-'*50}")
    print(f"  Question {num}/{total}")
    print(f"{'-'*50}")
    print()
    print(f"  {q['question']}")
    print()

    # Show code block if present
    if "code" in q:
        for line in q["code"].split("\n"):
            print(f"    {line}")
        print()

    # Show options for multiple choice
    if q.get("type") == "multiple_choice":
        for key, text in q["options"].items():
            print(f"    {key}) {text}")
        print()
        answer = input("  Your answer: ").strip().lower()
        correct = answer == q["answer"].lower()
    elif q.get("type") == "short_answer":
        answer = input("  Your answer: ").strip()
        # Accept any of the valid answers (case-insensitive)
        valid = q.get("accept", [q["answer"]])
        correct = answer.lower() in [v.lower() for v in valid]
    elif q.get("type") == "true_false":
        answer = input("  True or False: ").strip().lower()
        correct = answer in ("true", "t") if q["answer"] else answer in ("false", "f")
    else:
        answer = input("  Your answer: ").strip()
        correct = answer.lower() == str(q["answer"]).lower()

    if correct:
        print(f"  {GREEN}Correct!{RESET}")
    else:
        print(f"  {RED}Not quite.{RESET} The answer is: {q['answer']}")

    if "explanation" in q:
        print(f"  {CYAN}{q['explanation']}{RESET}")

    return correct


def run_diagnostic(name):
    """Run a diagnostic assessment and provide recommendations."""
    diag = load_diagnostic(name)
    if not diag:
        print(f"Diagnostic '{name}' not found.")
        list_diagnostics()
        return

    questions = diag.get("questions", [])
    if not questions:
        print("No questions in this diagnostic.")
        return

    print(f"\n{'='*50}")
    print(f"  {BOLD}{diag['title']}{RESET}")
    print(f"{'='*50}")
    print(f"  {diag.get('description', '')}")
    print(f"  Questions: {len(questions)}")
    print(f"  Estimated time: {len(questions) * 1} minutes")
    print()
    input("  Press Enter to start...")

    correct_count = 0
    topic_scores = {}  # track scores by topic/tag

    for i, q in enumerate(questions, 1):
        result = ask_question(q, i, len(questions))
        if result:
            correct_count += 1

        # Track by topic
        for tag in q.get("tags", []):
            if tag not in topic_scores:
                topic_scores[tag] = {"correct": 0, "total": 0}
            topic_scores[tag]["total"] += 1
            if result:
                topic_scores[tag]["correct"] += 1

    # Results
    total = len(questions)
    pct = correct_count / total * 100 if total > 0 else 0

    print(f"\n{'='*50}")
    print(f"  {BOLD}Results{RESET}")
    print(f"{'='*50}")
    print(f"  Score: {correct_count}/{total} ({pct:.0f}%)")
    print()

    # Score bar
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = "#" * filled + "-" * (bar_len - filled)
    color = GREEN if pct >= 80 else YELLOW if pct >= 50 else RED
    print(f"  {color}[{bar}] {pct:.0f}%{RESET}")
    print()

    # Topic breakdown
    if topic_scores:
        print(f"  {BOLD}Topic Breakdown:{RESET}")
        for topic, scores in sorted(topic_scores.items()):
            t_pct = scores["correct"] / scores["total"] * 100
            status = GREEN + "strong" if t_pct >= 80 else YELLOW + "review" if t_pct >= 50 else RED + "weak"
            print(f"    {topic:25s} {scores['correct']}/{scores['total']} — {status}{RESET}")
        print()

    # Recommendation
    thresholds = diag.get("thresholds", {})
    if pct >= thresholds.get("skip", 85):
        rec = diag.get("recommendations", {}).get("skip", "You're ready to skip ahead!")
        print(f"  {GREEN}{BOLD}Recommendation: {rec}{RESET}")
    elif pct >= thresholds.get("ready", 60):
        rec = diag.get("recommendations", {}).get("ready", "You're ready to start this level!")
        print(f"  {YELLOW}{BOLD}Recommendation: {rec}{RESET}")
    else:
        rec = diag.get("recommendations", {}).get("review", "Review the concepts before starting.")
        print(f"  {RED}{BOLD}Recommendation: {rec}{RESET}")

    # Weak topics → concept references
    weak_topics = [t for t, s in topic_scores.items() if s["correct"] / s["total"] < 0.5]
    if weak_topics:
        print(f"\n  {BOLD}Review these concepts:{RESET}")
        concept_map = diag.get("concept_map", {})
        for topic in weak_topics:
            ref = concept_map.get(topic, "")
            if ref:
                print(f"    - {topic}: {ref}")
            else:
                print(f"    - {topic}")

    print()


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if not args:
        list_diagnostics()
        return

    name = args[0]
    run_diagnostic(name)


if __name__ == "__main__":
    main()
