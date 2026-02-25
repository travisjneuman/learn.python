"""
Spaced Repetition Flashcard Runner — Leitner Box System

Usage:
    python practice/flashcards/review-runner.py              # review all due cards
    python practice/flashcards/review-runner.py --level 0    # review level 0 only
    python practice/flashcards/review-runner.py --stats      # show review statistics
    python practice/flashcards/review-runner.py --reset      # reset all progress

No external dependencies — uses only Python standard library.
"""

import json
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---

SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / ".review-state.json"

# Leitner box intervals (in days)
BOX_INTERVALS = {
    1: 0,    # every session
    2: 2,    # every 2 days
    3: 4,    # every 4 days
    4: 8,    # every 8 days
    5: 16,   # every 16 days
}

MAX_NEW_CARDS_PER_SESSION = 10
MAX_REVIEW_CARDS_PER_SESSION = 30


# --- State Management ---

def load_state():
    """Load review progress from disk."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"cards": {}, "sessions": 0, "last_review": None}


def save_state(state):
    """Save review progress to disk."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def reset_state():
    """Delete all progress."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    print("Progress reset. All cards moved back to box 1.")


# --- Card Loading ---

def load_deck(path):
    """Load a single flashcard deck from JSON."""
    with open(path) as f:
        return json.load(f)


def load_all_decks(level_filter=None):
    """Load all flashcard decks, optionally filtered by level."""
    decks = []
    for path in sorted(SCRIPT_DIR.glob("level-*-cards.json")):
        if level_filter is not None:
            # Extract level from filename: level-00-cards.json -> "00"
            level_str = path.stem.replace("level-", "").replace("-cards", "")
            if level_str != str(level_filter) and level_str != f"0{level_filter}":
                continue
        decks.append(load_deck(path))
    return decks


# --- Card Selection ---

def get_due_cards(decks, state):
    """Get cards that are due for review based on Leitner box intervals."""
    now = datetime.now()
    due = []
    new = []

    for deck in decks:
        for card in deck.get("cards", []):
            card_id = card["id"]
            card_state = state["cards"].get(card_id)

            if card_state is None:
                # New card — never seen before
                new.append((card, deck["deck"]))
            else:
                box = card_state.get("box", 1)
                last_seen = datetime.fromisoformat(card_state["last_seen"])
                interval = BOX_INTERVALS.get(box, 16)
                next_due = last_seen + timedelta(days=interval)

                if now >= next_due:
                    due.append((card, deck["deck"]))

    return due, new


# --- Quiz Engine ---

def show_card(card, deck_name, card_num, total, state):
    """Show a single flashcard and get response."""
    card_id = card["id"]
    card_state = state["cards"].get(card_id, {})
    box = card_state.get("box", 1)

    print(f"\n{'='*60}")
    print(f"  Card {card_num}/{total}  |  {deck_name}  |  Box {box}/5")
    print(f"{'='*60}")
    print()
    print(f"  {card['front']}")
    print()

    # Show difficulty indicator
    diff = card.get("difficulty", 1)
    diff_label = {1: "Easy", 2: "Medium", 3: "Hard"}.get(diff, "?")
    print(f"  Difficulty: {diff_label}")
    print()

    input("  Press Enter to reveal the answer...")
    print()
    print(f"  ANSWER:")
    print()
    for line in card["back"].split("\n"):
        print(f"    {line}")
    print()

    if card.get("concept_ref"):
        print(f"  Reference: {card['concept_ref']}")
        print()

    # Get self-assessment
    while True:
        response = input("  Did you know it? (y/n/q to quit): ").strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        elif response in ("q", "quit"):
            return None
        else:
            print("  Please enter y, n, or q.")


def update_card_state(state, card_id, correct):
    """Update a card's box based on whether the answer was correct."""
    now = datetime.now().isoformat()

    if card_id not in state["cards"]:
        state["cards"][card_id] = {
            "box": 1,
            "last_seen": now,
            "correct": 0,
            "incorrect": 0,
        }

    card_state = state["cards"][card_id]
    card_state["last_seen"] = now

    if correct:
        card_state["correct"] = card_state.get("correct", 0) + 1
        card_state["box"] = min(card_state.get("box", 1) + 1, 5)
    else:
        card_state["incorrect"] = card_state.get("incorrect", 0) + 1
        card_state["box"] = 1  # Back to box 1


# --- Statistics ---

def show_stats(state, decks):
    """Display review statistics."""
    total_cards = sum(len(d.get("cards", [])) for d in decks)
    reviewed = len(state.get("cards", {}))
    sessions = state.get("sessions", 0)

    # Count cards per box
    box_counts = {i: 0 for i in range(1, 6)}
    total_correct = 0
    total_incorrect = 0

    for card_state in state.get("cards", {}).values():
        box = card_state.get("box", 1)
        box_counts[box] = box_counts.get(box, 0) + 1
        total_correct += card_state.get("correct", 0)
        total_incorrect += card_state.get("incorrect", 0)

    total_attempts = total_correct + total_incorrect

    print(f"\n{'='*50}")
    print(f"  Flashcard Review Statistics")
    print(f"{'='*50}")
    print()
    print(f"  Sessions completed: {sessions}")
    print(f"  Cards seen: {reviewed}/{total_cards}")
    print(f"  Cards not started: {total_cards - reviewed}")
    print()

    if total_attempts > 0:
        accuracy = total_correct / total_attempts * 100
        print(f"  Total reviews: {total_attempts}")
        print(f"  Accuracy: {accuracy:.1f}%")
        print()

    print(f"  Cards by Leitner Box:")
    for box_num in range(1, 6):
        count = box_counts[box_num]
        bar = "#" * count
        interval = BOX_INTERVALS[box_num]
        label = f"every {interval}d" if interval > 0 else "every session"
        print(f"    Box {box_num} ({label:>14s}): {count:3d} {bar}")

    unseen = total_cards - reviewed
    if unseen > 0:
        print(f"    New (not started)  : {unseen:3d} {'.' * min(unseen, 50)}")

    print()

    # Per-deck breakdown
    print(f"  Per-Deck Breakdown:")
    for deck in decks:
        deck_cards = deck.get("cards", [])
        deck_seen = sum(1 for c in deck_cards if c["id"] in state.get("cards", {}))
        mastered = sum(
            1 for c in deck_cards
            if state.get("cards", {}).get(c["id"], {}).get("box", 0) >= 4
        )
        print(f"    {deck['deck']:40s} {deck_seen:2d}/{len(deck_cards):2d} seen, {mastered} mastered")

    print()
    last = state.get("last_review")
    if last:
        print(f"  Last review: {last}")
    print()


# --- Main ---

def run_review(level_filter=None):
    """Main review session."""
    state = load_state()
    decks = load_all_decks(level_filter)

    if not decks:
        if level_filter is not None:
            print(f"No flashcard deck found for level {level_filter}.")
        else:
            print("No flashcard decks found.")
        return

    due_cards, new_cards = get_due_cards(decks, state)

    # Prioritize due reviews, then add new cards
    review_queue = due_cards[:MAX_REVIEW_CARDS_PER_SESSION]
    remaining_slots = MAX_REVIEW_CARDS_PER_SESSION - len(review_queue)
    new_to_add = new_cards[:min(MAX_NEW_CARDS_PER_SESSION, remaining_slots)]
    review_queue.extend(new_to_add)

    if not review_queue:
        print("\nNo cards due for review right now.")
        print(f"You have {len(new_cards)} new cards available.")
        next_due = None
        now = datetime.now()
        for card_state in state.get("cards", {}).values():
            box = card_state.get("box", 1)
            last_seen = datetime.fromisoformat(card_state["last_seen"])
            interval = BOX_INTERVALS.get(box, 16)
            card_due = last_seen + timedelta(days=interval)
            if next_due is None or card_due < next_due:
                next_due = card_due
        if next_due and next_due > now:
            diff = next_due - now
            hours = diff.total_seconds() / 3600
            if hours < 24:
                print(f"Next review due in {hours:.1f} hours.")
            else:
                print(f"Next review due in {diff.days} day(s).")
        return

    random.shuffle(review_queue)

    print(f"\n{'='*50}")
    print(f"  Flashcard Review Session")
    print(f"{'='*50}")
    print(f"  Due for review: {len(due_cards)}")
    print(f"  New cards: {len(new_to_add)}")
    print(f"  Total this session: {len(review_queue)}")
    if level_filter is not None:
        print(f"  Filter: Level {level_filter}")
    print()
    input("  Press Enter to start...")

    correct_count = 0
    total_count = 0

    for i, (card, deck_name) in enumerate(review_queue, 1):
        result = show_card(card, deck_name, i, len(review_queue), state)

        if result is None:  # quit
            print(f"\n  Quitting early. Reviewed {total_count} cards.")
            break

        total_count += 1
        if result:
            correct_count += 1
            print("  Correct! Card moves up one box.")
        else:
            print("  Reviewing again soon. Card moves to box 1.")

        update_card_state(state, card["id"], result)

    # Session summary
    state["sessions"] = state.get("sessions", 0) + 1
    state["last_review"] = datetime.now().isoformat()
    save_state(state)

    if total_count > 0:
        accuracy = correct_count / total_count * 100
        print(f"\n{'='*50}")
        print(f"  Session Complete!")
        print(f"{'='*50}")
        print(f"  Reviewed: {total_count} cards")
        print(f"  Correct: {correct_count}/{total_count} ({accuracy:.0f}%)")
        print(f"  Session #{state['sessions']}")
        print()

        remaining_due = len(due_cards) - min(len(due_cards), MAX_REVIEW_CARDS_PER_SESSION)
        remaining_new = len(new_cards) - len(new_to_add)
        if remaining_due > 0:
            print(f"  {remaining_due} more cards still due. Run again to continue.")
        if remaining_new > 0:
            print(f"  {remaining_new} new cards waiting to be introduced.")
        print()


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--reset" in args:
        confirm = input("Reset all progress? This cannot be undone. (yes/no): ")
        if confirm.strip().lower() == "yes":
            reset_state()
        return

    level_filter = None
    if "--level" in args:
        idx = args.index("--level")
        if idx + 1 < len(args):
            level_filter = args[idx + 1]

    if "--stats" in args:
        state = load_state()
        decks = load_all_decks(level_filter)
        show_stats(state, decks)
        return

    run_review(level_filter)


if __name__ == "__main__":
    main()
