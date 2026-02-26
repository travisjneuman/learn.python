# Bridge Exercise: Level 3 to Level 4

You have completed Level 3. You can use logging, write classes, organize code into packages, and work with command-line arguments. Level 4 introduces **data validation with schemas**, **configuration management**, and **multi-step data pipelines**. This bridge exercise connects package organization to structured data validation.

---

## What Changes in Level 4

In Level 3, you trusted that data coming into your functions was well-formed. In Level 4, you will:
- **Validate data** against schemas before processing
- Build **pipelines** that chain multiple processing steps
- Use **dataclasses** to define structured data types
- Handle **configuration files** that control program behavior

---

## Part 1: Dataclasses for Structured Data

### Why dataclasses?

In Level 3, you wrote classes with `__init__`, `__repr__`, and other boilerplate. Dataclasses generate all of that for you.

### Exercise

Create `bridge_3_to_4.py`:

```python
from dataclasses import dataclass, field
from datetime import date
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@dataclass
class Task:
    """A project task with validation."""

    title: str
    priority: int  # 1 (highest) to 5 (lowest)
    due_date: date
    tags: list[str] = field(default_factory=list)
    completed: bool = False

    def __post_init__(self):
        """Validate fields after creation."""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.priority < 1 or self.priority > 5:
            raise ValueError(f"Priority must be 1-5, got {self.priority}")

    def is_overdue(self):
        """Check if the task is past its due date and not completed."""
        return not self.completed and self.due_date < date.today()
```

**New concepts introduced:**
- `@dataclass` generates `__init__`, `__repr__`, and `__eq__` automatically.
- Type annotations (`title: str`) document what each field expects.
- `__post_init__` runs after the auto-generated `__init__`, perfect for validation.
- `field(default_factory=list)` avoids the mutable default argument trap.

### Try it

```python
from bridge_3_to_4 import Task
from datetime import date

task = Task(
    title="Learn dataclasses",
    priority=2,
    due_date=date(2024, 12, 31),
    tags=["python", "learning"],
)
print(task)
# Task(title='Learn dataclasses', priority=2, due_date=..., tags=[...], completed=False)
```

---

## Part 2: A Validation Pipeline

### Exercise

Build a pipeline that reads task data, validates it, and filters by criteria.

Add to `bridge_3_to_4.py`:

```python
import json
from pathlib import Path


def load_tasks(filepath):
    """Load tasks from a JSON file and validate each one.

    Returns a tuple: (valid_tasks, errors)
    """
    path = Path(filepath)
    raw_data = json.loads(path.read_text())
    valid_tasks = []
    errors = []

    for i, item in enumerate(raw_data):
        try:
            task = Task(
                title=item["title"],
                priority=item["priority"],
                due_date=date.fromisoformat(item["due_date"]),
                tags=item.get("tags", []),
                completed=item.get("completed", False),
            )
            valid_tasks.append(task)
        except (ValueError, KeyError, TypeError) as e:
            errors.append({"index": i, "data": item, "error": str(e)})
            logger.warning("Task %d invalid: %s", i, e)

    logger.info("Loaded %d tasks (%d valid, %d invalid)",
                len(raw_data), len(valid_tasks), len(errors))
    return valid_tasks, errors


def filter_tasks(tasks, priority=None, tag=None, overdue_only=False):
    """Filter tasks by criteria.

    Args:
        priority: only tasks with this priority level
        tag: only tasks with this tag
        overdue_only: only overdue tasks
    """
    result = tasks

    if priority is not None:
        result = [t for t in result if t.priority == priority]

    if tag is not None:
        result = [t for t in result if tag in t.tags]

    if overdue_only:
        result = [t for t in result if t.is_overdue()]

    return result
```

**New concepts introduced:**
- Separating **loading** from **validation** from **filtering** (pipeline stages).
- Returning both valid results and errors (instead of crashing on the first bad item).
- `date.fromisoformat()` parses "2024-12-31" into a date object.
- List comprehensions for filtering with multiple criteria.

---

## Part 3: Tests

Create `test_bridge_3_to_4.py`:

```python
import json
import pytest
from datetime import date
from bridge_3_to_4 import Task, load_tasks, filter_tasks


def test_task_creation():
    task = Task("Do laundry", 3, date(2024, 12, 31))
    assert task.title == "Do laundry"
    assert task.completed is False


def test_task_empty_title():
    with pytest.raises(ValueError, match="empty"):
        Task("", 3, date(2024, 12, 31))


def test_task_bad_priority():
    with pytest.raises(ValueError, match="1-5"):
        Task("Task", 0, date(2024, 12, 31))


def test_task_default_tags():
    task = Task("Task", 1, date(2024, 12, 31))
    assert task.tags == []


def test_load_tasks(tmp_path):
    data = [
        {"title": "A", "priority": 1, "due_date": "2024-12-31"},
        {"title": "B", "priority": 2, "due_date": "2025-06-15", "tags": ["work"]},
        {"title": "", "priority": 1, "due_date": "2024-01-01"},  # invalid
    ]
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data))

    valid, errors = load_tasks(f)
    assert len(valid) == 2
    assert len(errors) == 1


def test_filter_by_priority(tmp_path):
    data = [
        {"title": "A", "priority": 1, "due_date": "2025-12-31"},
        {"title": "B", "priority": 3, "due_date": "2025-12-31"},
        {"title": "C", "priority": 1, "due_date": "2025-12-31"},
    ]
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data))

    valid, _ = load_tasks(f)
    high_priority = filter_tasks(valid, priority=1)
    assert len(high_priority) == 2


def test_filter_by_tag(tmp_path):
    data = [
        {"title": "A", "priority": 1, "due_date": "2025-12-31", "tags": ["work"]},
        {"title": "B", "priority": 2, "due_date": "2025-12-31", "tags": ["home"]},
    ]
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(data))

    valid, _ = load_tasks(f)
    work = filter_tasks(valid, tag="work")
    assert len(work) == 1
    assert work[0].title == "A"
```

Run: `pytest test_bridge_3_to_4.py -v`

---

## You Are Ready

If you can use `@dataclass` with validation, load and validate structured data from JSON, and build filter pipelines with list comprehensions, you are ready for Level 4.

---

| [Level 3 Projects](level-3/README.md) | [Home](../README.md) | [Level 4 Projects](level-4/README.md) |
|:---|:---:|---:|
