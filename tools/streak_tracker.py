"""
Streak Tracker — Daily Coding Streak

Tracks consecutive days of coding activity. Records activity when you
run grade.py, take a quiz, or review flashcards. Builds a streak to
motivate consistent daily practice.

Usage:
    python tools/streak_tracker.py            # show current streak
    python tools/streak_tracker.py record     # manually record today's activity

No external dependencies — uses only Python standard library.
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STREAK_FILE = REPO_ROOT / "data" / "streak.json"

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_streak():
    """Load streak data from disk."""
    if STREAK_FILE.exists():
        with open(STREAK_FILE) as f:
            return json.load(f)
    return {
        "current_streak": 0,
        "longest_streak": 0,
        "last_active_date": None,
        "history": [],
    }


def save_streak(data):
    """Save streak data to disk."""
    STREAK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STREAK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_activity(activity_type="manual"):
    """Record today's coding activity and update the streak.

    Args:
        activity_type: What triggered the activity (grade, quiz,
            flashcard, manual).

    Returns:
        The current streak count after recording.
    """
    data = load_streak()
    today = date.today().isoformat()

    # Already recorded today — just return current streak
    if data["last_active_date"] == today:
        return data["current_streak"]

    last = data.get("last_active_date")
    if last:
        last_date = date.fromisoformat(last)
        diff = (date.today() - last_date).days

        if diff == 1:
            # Consecutive day — extend streak
            data["current_streak"] += 1
        elif diff > 1:
            # Streak broken — reset
            data["current_streak"] = 1
        # diff == 0 handled above
    else:
        # First ever activity
        data["current_streak"] = 1

    data["last_active_date"] = today
    data["longest_streak"] = max(data["longest_streak"], data["current_streak"])

    # Record in history
    data["history"].append({
        "date": today,
        "activity_type": activity_type,
    })

    save_streak(data)
    return data["current_streak"]


def get_streak():
    """Return the current streak count."""
    data = load_streak()
    # Check if streak is still active (last activity was today or yesterday)
    last = data.get("last_active_date")
    if last:
        diff = (date.today() - date.fromisoformat(last)).days
        if diff > 1:
            # Streak has lapsed
            data["current_streak"] = 0
            save_streak(data)
    return data.get("current_streak", 0)


def get_longest_streak():
    """Return the longest streak ever achieved."""
    data = load_streak()
    return data.get("longest_streak", 0)


def print_streak():
    """Print current streak status."""
    current = get_streak()
    data = load_streak()
    longest = data.get("longest_streak", 0)
    last = data.get("last_active_date", "never")
    total_days = len(data.get("history", []))

    print(f"\n{'='*50}")
    print(f"  {BOLD}Coding Streak{RESET}")
    print(f"{'='*50}")
    print()

    # Streak display with fire visual
    if current >= 7:
        color = GREEN
        streak_label = "ON FIRE!"
    elif current >= 3:
        color = YELLOW
        streak_label = "Building momentum"
    elif current >= 1:
        color = YELLOW
        streak_label = "Keep it going"
    else:
        color = RED
        streak_label = "Start a new streak today"

    print(f"  Current streak: {color}{BOLD}{current} day(s){RESET}  {streak_label}")
    print(f"  Longest streak: {BOLD}{longest} day(s){RESET}")
    print(f"  Total active days: {total_days}")
    print(f"  Last active: {last}")
    print()

    # Show last 7 days as a visual calendar
    print(f"  Last 7 days:")
    history_dates = {e["date"] for e in data.get("history", [])}
    today = date.today()
    row = "  "
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        if d.isoformat() in history_dates:
            row += f" {GREEN}#{RESET}"
        else:
            row += f" {RED}-{RESET}"
    print(row)
    labels = "  "
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        labels += f" {d.strftime('%a')[0]}"
    print(labels)
    print()


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if args and args[0] == "record":
        streak = record_activity("manual")
        print(f"Activity recorded. Current streak: {streak} day(s).")
        return

    print_streak()


if __name__ == "__main__":
    main()
