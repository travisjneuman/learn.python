# ============================================================
# BUG HUNT #4 — Key and Attribute Errors
# ============================================================
# This program processes a list of user profiles fetched from
# an API. It should:
#   1. Print each user's display name.
#   2. Count users by their account type.
#   3. Find the most recently active user.
#
# Some profiles have missing fields. The code doesn't handle
# that. Find and fix the bugs.
# ============================================================

from datetime import datetime

users = [
    {"username": "alice", "display_name": "Alice M.", "type": "admin", "last_login": "2025-03-15"},
    {"username": "bob", "type": "member", "last_login": "2025-06-01"},
    {"username": "charlie", "display_name": "Charlie K.", "type": "admin", "last_login": "2025-07-20"},
    {"username": "diana", "display_name": "Diana P.", "last_login": "2025-01-10"},
    {"username": "eve", "display_name": None, "type": "member", "last_login": None},
]


def print_display_names(users):
    """Print each user's display name."""
    for user in users:
        print(f"  {user['display_name']}")


def count_by_type(users):
    """Return a dict counting users by account type."""
    counts = {}
    for user in users:
        user_type = user["type"]
        counts[user_type] = counts[user_type] + 1
    return counts


def most_recent_user(users):
    """Return the username of the most recently active user."""
    latest = None
    latest_user = None
    for user in users:
        login_date = datetime.strptime(user["last_login"], "%Y-%m-%d")
        if latest is None or login_date > latest:
            latest = login_date
            latest_user = user.username
    return latest_user


if __name__ == "__main__":
    print("=== Display Names ===")
    print_display_names(users)

    print("\n=== Users by Type ===")
    try:
        counts = count_by_type(users)
        for user_type, count in counts.items():
            print(f"  {user_type}: {count}")
    except (KeyError, TypeError) as e:
        print(f"  Error: {e}")

    print("\n=== Most Recent Login ===")
    try:
        recent = most_recent_user(users)
        print(f"  {recent}")
    except (TypeError, ValueError, AttributeError) as e:
        print(f"  Error: {e}")
