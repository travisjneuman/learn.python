"""
Spaced Repetition Flashcard Engine — SM-2 Algorithm

Implements the SuperMemo SM-2 algorithm for optimal review scheduling.
Uses a 0-5 quality rating scale for more precise interval calculations
than the simpler Leitner box system. Includes ANSI-colored output.
Stores progress in data/flashcard_progress.json.

WHEN TO USE THIS:
    Prefer this runner for precise, research-backed review scheduling.
    The SM-2 algorithm adjusts intervals based on your self-rated recall
    quality (0-5), producing more accurate spacing than Leitner boxes.

SEE ALSO:
    practice/flashcards/review-runner.py — Uses the simpler Leitner 5-box
    model with yes/no self-assessment. Stores progress in
    practice/flashcards/.review-state.json. Use this if you prefer simplicity.

Usage:
    python tools/spaced_repetition.py                  # review due cards
    python tools/spaced_repetition.py --level 0        # review level 0 only
    python tools/spaced_repetition.py --review         # spaced repetition mode (default)
    python tools/spaced_repetition.py --random         # random/casual practice
    python tools/spaced_repetition.py --stats          # show review statistics
    python tools/spaced_repetition.py --due            # show count of due cards
    python tools/spaced_repetition.py --reset          # reset all progress

No external dependencies — uses only Python standard library.
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FLASHCARD_DIR = REPO_ROOT / "practice" / "flashcards"
DATA_DIR = REPO_ROOT / "data"
PROGRESS_FILE = DATA_DIR / "flashcard_progress.json"

# SM-2 defaults
DEFAULT_EASINESS = 2.5
MIN_EASINESS = 1.3
MAX_NEW_PER_SESSION = 10
MAX_REVIEW_PER_SESSION = 30

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


# --- SM-2 Algorithm ---

def sm2_update(card_state: dict, quality: int) -> dict:
    """
    Apply SM-2 algorithm update.

    quality: 0-5 rating
      0 - complete blackout
      1 - incorrect, remembered on seeing answer
      2 - incorrect, answer seemed easy to recall
      3 - correct with serious difficulty
      4 - correct with some hesitation
      5 - perfect response

    Returns updated card state dict.
    """
    ef = card_state.get("easiness", DEFAULT_EASINESS)
    interval = card_state.get("interval", 0)
    repetitions = card_state.get("repetitions", 0)

    # Update easiness factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ef < MIN_EASINESS:
        ef = MIN_EASINESS

    if quality < 3:
        # Failed: reset repetitions, short interval
        repetitions = 0
        interval = 1
    else:
        # Passed: increase interval
        repetitions += 1
        if repetitions == 1:
            interval = 1
        elif repetitions == 2:
            interval = 6
        else:
            interval = round(interval * ef)

    now = datetime.now().isoformat()
    next_review = (datetime.now() + timedelta(days=interval)).isoformat()

    return {
        "easiness": round(ef, 2),
        "interval": interval,
        "repetitions": repetitions,
        "quality": quality,
        "last_review": now,
        "next_review": next_review,
        "correct": card_state.get("correct", 0) + (1 if quality >= 3 else 0),
        "incorrect": card_state.get("incorrect", 0) + (1 if quality < 3 else 0),
        "total_reviews": card_state.get("total_reviews", 0) + 1,
    }


# --- State Management ---

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"cards": {}, "sessions": 0, "last_session": None}


def save_progress(state: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(state, f, indent=2)


# --- Card Loading ---

def load_all_decks(level_filter: str | None = None) -> list[dict]:
    decks = []
    for path in sorted(FLASHCARD_DIR.glob("*-cards.json")):
        if level_filter is not None:
            # Filter by level or module name
            stem = path.stem.replace("-cards", "")
            if level_filter not in stem:
                continue
        try:
            with open(path, encoding="utf-8") as f:
                decks.append(json.load(f))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            continue
    return decks


def get_all_cards(decks: list[dict]) -> list[tuple[dict, str]]:
    """Get all cards with their deck names."""
    cards = []
    for deck in decks:
        deck_name = deck.get("deck", "Unknown")
        for card in deck.get("cards", []):
            cards.append((card, deck_name))
    return cards


# --- Card Selection ---

def get_due_cards(
    all_cards: list[tuple[dict, str]], state: dict
) -> tuple[list[tuple[dict, str]], list[tuple[dict, str]]]:
    """Split cards into due-for-review and new (never seen)."""
    now = datetime.now()
    due = []
    new = []

    for card, deck_name in all_cards:
        card_id = card["id"]
        card_state = state["cards"].get(card_id)

        if card_state is None:
            new.append((card, deck_name))
        else:
            next_review_str = card_state.get("next_review")
            if next_review_str:
                next_review = datetime.fromisoformat(next_review_str)
                if now >= next_review:
                    due.append((card, deck_name))
            else:
                due.append((card, deck_name))

    return due, new


# --- Quiz Engine ---

def show_card(card: dict, deck_name: str, num: int, total: int, state: dict) -> int | None:
    """Show a flashcard and get quality rating. Returns 0-5 or None to quit."""
    card_id = card["id"]
    card_state = state["cards"].get(card_id, {})
    interval = card_state.get("interval", 0)
    ef = card_state.get("easiness", DEFAULT_EASINESS)

    print(f"\n{'='*60}")
    print(f"  Card {num}/{total}  |  {deck_name}  |  Interval: {interval}d  |  EF: {ef:.1f}")
    print(f"{'='*60}")
    print()
    print(f"  {card['front']}")
    print()

    diff = card.get("difficulty", 1)
    diff_label = {1: "Easy", 2: "Medium", 3: "Hard"}.get(diff, "?")
    print(f"  {DIM}Difficulty: {diff_label}{RESET}")
    print()

    input("  Press Enter to reveal the answer...")
    print()
    print(f"  {BOLD}ANSWER:{RESET}")
    print()
    for line in card["back"].split("\n"):
        print(f"    {line}")
    print()

    if card.get("concept_ref"):
        print(f"  {DIM}Reference: {card['concept_ref']}{RESET}")
        print()

    # Get self-assessment on SM-2 scale
    print(f"  Rate your recall:")
    print(f"    {RED}0{RESET} = total blackout    {RED}1{RESET} = wrong, recognized answer")
    print(f"    {YELLOW}2{RESET} = wrong, seemed easy {GREEN}3{RESET} = correct, hard recall")
    print(f"    {GREEN}4{RESET} = correct, hesitation {GREEN}5{RESET} = perfect recall")
    print(f"    {DIM}q = quit{RESET}")
    print()

    while True:
        response = input("  Your rating (0-5 or q): ").strip().lower()
        if response in ("q", "quit"):
            return None
        try:
            rating = int(response)
            if 0 <= rating <= 5:
                return rating
        except ValueError:
            pass
        print("  Please enter a number 0-5 or q to quit.")


# --- Statistics ---

def show_stats(state: dict, decks: list[dict]) -> None:
    all_cards = get_all_cards(decks)
    total_cards = len(all_cards)
    reviewed = len(state.get("cards", {}))
    sessions = state.get("sessions", 0)

    # Calculate statistics
    total_correct = 0
    total_incorrect = 0
    total_reviews = 0
    ef_values = []
    interval_buckets = {"1d": 0, "2-6d": 0, "7-14d": 0, "15-30d": 0, "30d+": 0}

    for card_state in state.get("cards", {}).values():
        total_correct += card_state.get("correct", 0)
        total_incorrect += card_state.get("incorrect", 0)
        total_reviews += card_state.get("total_reviews", 0)
        ef_values.append(card_state.get("easiness", DEFAULT_EASINESS))

        interval = card_state.get("interval", 1)
        if interval <= 1:
            interval_buckets["1d"] += 1
        elif interval <= 6:
            interval_buckets["2-6d"] += 1
        elif interval <= 14:
            interval_buckets["7-14d"] += 1
        elif interval <= 30:
            interval_buckets["15-30d"] += 1
        else:
            interval_buckets["30d+"] += 1

    print(f"\n{'='*55}")
    print(f"  {BOLD}Spaced Repetition Statistics (SM-2){RESET}")
    print(f"{'='*55}")
    print()
    print(f"  Sessions completed: {sessions}")
    print(f"  Cards seen: {reviewed}/{total_cards}")
    print(f"  Cards not started: {total_cards - reviewed}")
    print()

    if total_reviews > 0:
        accuracy = total_correct / (total_correct + total_incorrect) * 100
        print(f"  Total reviews: {total_reviews}")
        print(f"  Accuracy: {accuracy:.1f}%")
        if ef_values:
            avg_ef = sum(ef_values) / len(ef_values)
            print(f"  Average easiness: {avg_ef:.2f}")
        print()

    print(f"  {BOLD}Cards by interval:{RESET}")
    for bucket, count in interval_buckets.items():
        bar = "#" * count
        print(f"    {bucket:>8s}: {count:3d} {bar}")

    unseen = total_cards - reviewed
    if unseen > 0:
        print(f"    {'new':>8s}: {unseen:3d} {'.' * min(unseen, 50)}")

    print()

    # Due cards count
    due, new = get_due_cards(all_cards, state)
    print(f"  {BOLD}Queue:{RESET}")
    print(f"    Due for review: {len(due)}")
    print(f"    New cards available: {len(new)}")
    print()

    # Per-deck breakdown
    print(f"  {BOLD}Per-Deck Breakdown:{RESET}")
    for deck in decks:
        deck_cards = deck.get("cards", [])
        deck_seen = sum(
            1 for c in deck_cards if c["id"] in state.get("cards", {})
        )
        mastered = sum(
            1 for c in deck_cards
            if state.get("cards", {}).get(c["id"], {}).get("interval", 0) >= 21
        )
        print(
            f"    {deck['deck']:40s} "
            f"{deck_seen:2d}/{len(deck_cards):2d} seen, {mastered} mastered"
        )

    print()
    last = state.get("last_session")
    if last:
        print(f"  Last session: {last}")
    print()


# --- Review Session ---

def run_review(level_filter: str | None = None, mode: str = "review") -> None:
    state = load_progress()
    decks = load_all_decks(level_filter)

    if not decks:
        print("No flashcard decks found.")
        return

    all_cards = get_all_cards(decks)

    if mode == "random":
        # Random mode: just pick random cards
        review_queue = list(all_cards)
        random.shuffle(review_queue)
        review_queue = review_queue[:MAX_REVIEW_PER_SESSION]
        print(f"\n{BOLD}Random Practice Mode{RESET}")
        print(f"  Cards: {len(review_queue)}")
    else:
        # Spaced repetition mode
        due, new = get_due_cards(all_cards, state)
        review_queue = due[:MAX_REVIEW_PER_SESSION]
        remaining_slots = MAX_REVIEW_PER_SESSION - len(review_queue)
        new_to_add = new[:min(MAX_NEW_PER_SESSION, remaining_slots)]
        review_queue.extend(new_to_add)

        if not review_queue:
            print("\nNo cards due for review right now.")
            print(f"You have {len(new)} new cards available.")
            # Show next due time
            now = datetime.now()
            next_due = None
            for cs in state.get("cards", {}).values():
                nr = cs.get("next_review")
                if nr:
                    dt = datetime.fromisoformat(nr)
                    if dt > now and (next_due is None or dt < next_due):
                        next_due = dt
            if next_due:
                diff = next_due - now
                hours = diff.total_seconds() / 3600
                if hours < 24:
                    print(f"Next review due in {hours:.1f} hours.")
                else:
                    print(f"Next review due in {diff.days} day(s).")
            return

        random.shuffle(review_queue)

        print(f"\n{BOLD}Spaced Repetition Session (SM-2){RESET}")
        print(f"  Due for review: {len(due)}")
        print(f"  New cards: {len(new_to_add)}")
        print(f"  Total this session: {len(review_queue)}")

    if level_filter:
        print(f"  Filter: {level_filter}")
    print()
    input("  Press Enter to start...")

    correct_count = 0
    total_count = 0

    for i, (card, deck_name) in enumerate(review_queue, 1):
        quality = show_card(card, deck_name, i, len(review_queue), state)

        if quality is None:
            print(f"\n  Quitting early. Reviewed {total_count} cards.")
            break

        total_count += 1
        if quality >= 3:
            correct_count += 1
            print(f"  {GREEN}Correct!{RESET} Rating: {quality}")
        else:
            print(f"  {RED}Needs review.{RESET} Rating: {quality}")

        # Update SM-2 state
        card_id = card["id"]
        card_state = state["cards"].get(card_id, {})
        state["cards"][card_id] = sm2_update(card_state, quality)

    # Save session
    state["sessions"] = state.get("sessions", 0) + 1
    state["last_session"] = datetime.now().isoformat()
    save_progress(state)

    if total_count > 0:
        accuracy = correct_count / total_count * 100
        print(f"\n{'='*50}")
        print(f"  {BOLD}Session Complete!{RESET}")
        print(f"{'='*50}")
        print(f"  Reviewed: {total_count} cards")
        print(f"  Correct: {correct_count}/{total_count} ({accuracy:.0f}%)")
        print(f"  Session #{state['sessions']}")
        print()


def show_due_count(level_filter: str | None = None) -> None:
    state = load_progress()
    decks = load_all_decks(level_filter)
    all_cards = get_all_cards(decks)
    due, new = get_due_cards(all_cards, state)
    print(f"Due for review: {len(due)}")
    print(f"New cards: {len(new)}")
    print(f"Total available: {len(due) + len(new)}")


# --- Main ---

def main() -> None:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--reset" in args:
        confirm = input("Reset all SM-2 progress? This cannot be undone. (yes/no): ")
        if confirm.strip().lower() == "yes":
            if PROGRESS_FILE.exists():
                PROGRESS_FILE.unlink()
            print("SM-2 progress reset.")
        return

    level_filter = None
    if "--level" in args:
        idx = args.index("--level")
        if idx + 1 < len(args):
            level_filter = args[idx + 1]

    if "--stats" in args:
        state = load_progress()
        decks = load_all_decks(level_filter)
        show_stats(state, decks)
        return

    if "--due" in args:
        show_due_count(level_filter)
        return

    mode = "random" if "--random" in args else "review"
    run_review(level_filter, mode)


if __name__ == "__main__":
    main()
