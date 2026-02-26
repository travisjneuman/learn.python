"""
XP Tracker — Gamification Progress System

Tracks experience points earned through learning activities. Awards XP
for completing projects, passing quizzes, reviewing flashcards, solving
challenges, and finishing bridge exercises.

Usage:
    python tools/xp_tracker.py status          # show current XP and milestone
    python tools/xp_tracker.py history          # show recent XP history
    python tools/xp_tracker.py history --limit 5  # show last 5 entries

No external dependencies — uses only Python standard library.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = REPO_ROOT / "data" / "xp_config.json"
PROGRESS_FILE = REPO_ROOT / "data" / "xp_progress.json"

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_config():
    """Load XP configuration (point values and milestones)."""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def load_progress():
    """Load XP progress data. Returns empty structure if no file exists."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"total_xp": 0, "history": []}


def save_progress(progress):
    """Save XP progress data to disk."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def award_xp(activity_type, details=""):
    """Award XP for a completed activity.

    Args:
        activity_type: One of project_completion, quiz_pass,
            flashcard_review, challenge_solved, bridge_completed.
        details: Description of the activity (e.g., project name).

    Returns:
        The number of XP awarded, or 0 if activity_type is unknown.
    """
    config = load_config()
    xp_values = config.get("xp_values", {})
    xp = xp_values.get(activity_type, 0)

    if xp == 0:
        return 0

    progress = load_progress()
    progress["total_xp"] = progress.get("total_xp", 0) + xp
    progress["history"].append({
        "timestamp": datetime.now().isoformat(),
        "activity_type": activity_type,
        "xp_earned": xp,
        "details": details,
    })
    save_progress(progress)
    return xp


def get_total_xp():
    """Return total accumulated XP."""
    progress = load_progress()
    return progress.get("total_xp", 0)


def get_current_milestone():
    """Return the current milestone based on total XP.

    Returns:
        A dict with name, xp threshold, and emoji, or None if no
        milestone has been reached.
    """
    config = load_config()
    milestones = config.get("milestones", [])
    total = get_total_xp()

    current = None
    for ms in milestones:
        if total >= ms["xp"]:
            current = ms
    return current


def get_next_milestone():
    """Return the next milestone to reach.

    Returns:
        A dict with name, xp threshold, and emoji, or None if all
        milestones have been reached.
    """
    config = load_config()
    milestones = config.get("milestones", [])
    total = get_total_xp()

    for ms in milestones:
        if total < ms["xp"]:
            return ms
    return None


def get_xp_history(limit=None):
    """Return XP history entries, most recent first.

    Args:
        limit: Maximum number of entries to return. None for all.
    """
    progress = load_progress()
    history = list(reversed(progress.get("history", [])))
    if limit is not None:
        history = history[:limit]
    return history


def print_status():
    """Print current XP status and milestone progress."""
    total = get_total_xp()
    current = get_current_milestone()
    next_ms = get_next_milestone()

    print(f"\n{'='*50}")
    print(f"  {BOLD}XP Status{RESET}")
    print(f"{'='*50}")
    print()
    print(f"  Total XP: {GREEN}{total:,}{RESET}")

    if current:
        print(f"  Milestone: {current['emoji']} {BOLD}{current['name']}{RESET}")
    else:
        print(f"  Milestone: (none yet)")

    if next_ms:
        remaining = next_ms["xp"] - total
        pct = total / next_ms["xp"] * 100
        bar_len = 30
        filled = int(bar_len * min(pct, 100) / 100)
        bar = "#" * filled + "-" * (bar_len - filled)
        print()
        print(f"  Next: {next_ms['emoji']} {next_ms['name']} ({next_ms['xp']:,} XP)")
        print(f"  Progress: [{bar}] {pct:.0f}%")
        print(f"  Remaining: {remaining:,} XP")
    else:
        print(f"\n  {GREEN}All milestones reached!{RESET}")

    print()


def print_history(limit=10):
    """Print recent XP history."""
    history = get_xp_history(limit)
    if not history:
        print("\n  No XP history yet. Start learning to earn XP!")
        return

    print(f"\n{'='*50}")
    print(f"  {BOLD}Recent XP History{RESET} (last {len(history)})")
    print(f"{'='*50}")
    print()

    for entry in history:
        ts = entry["timestamp"][:16].replace("T", " ")
        activity = entry["activity_type"].replace("_", " ")
        xp = entry["xp_earned"]
        details = entry.get("details", "")
        detail_str = f" — {details}" if details else ""
        print(f"  {CYAN}{ts}{RESET}  +{xp:3d} XP  {activity}{detail_str}")

    print()


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return

    command = args[0]

    if command == "status":
        print_status()
    elif command == "history":
        limit = 10
        if "--limit" in args:
            idx = args.index("--limit")
            if idx + 1 < len(args):
                limit = int(args[idx + 1])
        print_history(limit)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python tools/xp_tracker.py status|history")


if __name__ == "__main__":
    main()
