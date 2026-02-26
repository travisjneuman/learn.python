# ============================================================
# BUG HUNT #5 — File Handling Bugs
# ============================================================
# This program manages a simple note-taking system. It should:
#   1. Create a notes file if it doesn't exist.
#   2. Append new notes with timestamps.
#   3. Read and display all notes.
#   4. Count the total number of notes.
#
# Run this and watch the file operations fail in subtle ways.
# ============================================================

import os
from datetime import datetime

NOTES_FILE = "my_notes.txt"


def create_notes_file():
    """Create the notes file if it doesn't exist."""
    if not os.path.exists(NOTES_FILE):
        f = open(NOTES_FILE, "r")
        f.write("# My Notes\n")
        f.close()


def add_note(text):
    """Append a timestamped note to the file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    f = open(NOTES_FILE, "w")
    f.write(f"[{timestamp}] {text}\n")


def read_notes():
    """Read and display all notes from the file."""
    with open(NOTES_FILE, "r", encoding="ascii") as f:
        content = f.read()
    print(content)


def count_notes():
    """Count lines that look like notes (start with '[')."""
    count = 0
    for line in open(NOTES_FILE):
        if line.startswith("["):
            count += 1
    return count


if __name__ == "__main__":
    create_notes_file()
    add_note("First note: learning Python!")
    add_note("Second note: debugging is fun")
    add_note("Third note: cafe time ☕")

    print("=== All Notes ===")
    read_notes()

    print(f"\nTotal notes: {count_notes()}")
    # Expected: 3 notes

    # Cleanup
    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)
