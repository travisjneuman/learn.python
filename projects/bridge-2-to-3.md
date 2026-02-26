# Bridge Exercise: Level 2 to Level 3

You have completed Level 2. You can work with data structures, clean data, handle errors, and write solid tests. Level 3 introduces **logging**, **classes**, and **project structure** (packages, CLI arguments). This bridge exercise introduces logging and a simple class before you encounter them in full projects.

---

## What Changes in Level 3

In Level 2, you used `print()` for output and functions for everything. In Level 3, you will:
- Replace `print()` with `logging` for diagnostic output
- Organize related functions into **classes**
- Structure your code into **packages** (folders with `__init__.py`)

---

## Part 1: Logging Instead of Print

### Why logging?

`print()` always shows output. Logging lets you control what shows up based on severity level. In production, you want to see errors but not debug messages.

### Exercise

Create `bridge_2_to_3.py`:

```python
import logging

# Set up logging: show INFO and above, include timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def process_records(records):
    """Process a list of dicts, returning only valid ones.

    Logs a warning for each invalid record (missing 'name' key).
    """
    valid = []
    for i, record in enumerate(records):
        if "name" not in record:
            logger.warning("Record %d is missing 'name' key: %s", i, record)
            continue
        logger.debug("Processing record %d: %s", i, record["name"])
        valid.append(record)

    logger.info("Processed %d records: %d valid, %d skipped",
                len(records), len(valid), len(records) - len(valid))
    return valid
```

**Key ideas:**
- `logger.debug()` -- detailed info, hidden by default
- `logger.info()` -- normal operational messages
- `logger.warning()` -- something unexpected but not fatal
- `logger.error()` -- something broke

Run it:

```python
from bridge_2_to_3 import process_records

data = [
    {"name": "Alice", "score": 95},
    {"score": 80},  # missing name
    {"name": "Bob", "score": 88},
]
result = process_records(data)
print(result)
```

You will see the warning about record 1 missing 'name', plus an info summary.

---

## Part 2: A Simple Class

### Why classes?

When several functions all operate on the same data, a class groups them together. Think of it as a bundle of data and the functions that work on that data.

### Exercise

Add this to `bridge_2_to_3.py`:

```python
class ScoreTracker:
    """Track scores for a group of students."""

    def __init__(self):
        self._scores = {}
        logger.info("ScoreTracker initialized")

    def add_score(self, name, score):
        """Add a score for a student. Overwrites previous score."""
        if not isinstance(score, (int, float)):
            raise TypeError(f"Score must be a number, got {type(score).__name__}")
        self._scores[name] = score
        logger.debug("Added score for %s: %s", name, score)

    def average(self):
        """Return the average score across all students."""
        if not self._scores:
            return 0.0
        return sum(self._scores.values()) / len(self._scores)

    def top_student(self):
        """Return the name of the student with the highest score."""
        if not self._scores:
            return None
        return max(self._scores, key=self._scores.get)

    def summary(self):
        """Return a dict summarizing the tracked scores."""
        return {
            "count": len(self._scores),
            "average": round(self.average(), 2),
            "top": self.top_student(),
        }
```

### Test it

Create `test_bridge_2_to_3.py`:

```python
import pytest
from bridge_2_to_3 import process_records, ScoreTracker


def test_process_valid_records():
    records = [{"name": "A"}, {"name": "B"}]
    result = process_records(records)
    assert len(result) == 2


def test_process_skips_invalid():
    records = [{"name": "A"}, {"score": 5}, {"name": "C"}]
    result = process_records(records)
    assert len(result) == 2


def test_tracker_average():
    tracker = ScoreTracker()
    tracker.add_score("Alice", 90)
    tracker.add_score("Bob", 80)
    assert tracker.average() == 85.0


def test_tracker_top_student():
    tracker = ScoreTracker()
    tracker.add_score("Alice", 90)
    tracker.add_score("Bob", 95)
    assert tracker.top_student() == "Bob"


def test_tracker_empty_average():
    tracker = ScoreTracker()
    assert tracker.average() == 0.0


def test_tracker_bad_score():
    tracker = ScoreTracker()
    with pytest.raises(TypeError):
        tracker.add_score("Alice", "ninety")
```

Run: `pytest test_bridge_2_to_3.py -v`

---

## You Are Ready

If you can use `logging` instead of `print()`, create a class with `__init__` and methods, and test both, you are ready for Level 3.

---

| [Level 2 Projects](level-2/README.md) | [Home](../README.md) | [Level 3 Projects](level-3/README.md) |
|:---|:---:|---:|
