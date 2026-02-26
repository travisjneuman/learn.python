# Bridge Exercise: Level 8 to Level 9

You have completed Level 8. You can build dashboards, generate reports, aggregate data, and create text-based visualizations. Level 9 introduces **software architecture patterns**, **design principles**, **dependency injection**, and **interface design**. This bridge exercise connects dashboard-style code with architectural thinking.

---

## What Changes in Level 9

In Level 8, you built working programs that solved specific problems. In Level 9, you will:
- Separate **concerns** so each module has one job
- Design **interfaces** (abstract classes) so components can be swapped
- Use **dependency injection** instead of hardcoding dependencies
- Apply patterns like **Strategy**, **Repository**, and **Observer**

---

## Part 1: From Hardcoded to Pluggable

### The problem

In Level 8, your dashboard code might look like this:

```python
def generate_report(data):
    # hardcoded to always use JSON
    return json.dumps(data)
```

What if you want text output? CSV? You change the function. In Level 9, you design the code so output format is **pluggable**.

### Exercise

Create `bridge_8_to_9.py`:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import csv
import io
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# --- Interface (Abstract Base Class) ---

class ReportFormatter(ABC):
    """Interface for report formatters.

    Any class that implements format() can be used as a formatter.
    This is the Strategy pattern.
    """

    @abstractmethod
    def format(self, title, data):
        """Format data into a report string."""
        ...


# --- Concrete Implementations ---

class JsonFormatter(ReportFormatter):
    def format(self, title, data):
        return json.dumps({"title": title, "data": data}, indent=2)


class CsvFormatter(ReportFormatter):
    def format(self, title, data):
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class TextFormatter(ReportFormatter):
    def format(self, title, data):
        lines = [f"=== {title} ===", ""]
        for row in data:
            lines.append("  ".join(f"{k}: {v}" for k, v in row.items()))
        lines.append(f"\nTotal records: {len(data)}")
        return "\n".join(lines)
```

**New concepts introduced:**
- **ABC (Abstract Base Class)**: defines an interface that subclasses must implement.
- **@abstractmethod**: forces subclasses to provide this method (crashes if they don't).
- **Strategy pattern**: different formatters (strategies) implement the same interface.
- You can swap formatters without changing the code that uses them.

---

## Part 2: Dependency Injection

### Exercise

Build a report generator that accepts its formatter as a dependency.

Add to `bridge_8_to_9.py`:

```python
@dataclass
class DataStore:
    """Simple in-memory data store (simulates a database).

    This is the Repository pattern — data access is behind a clean interface.
    """

    _records: list = None

    def __post_init__(self):
        if self._records is None:
            self._records = []

    def add(self, record):
        self._records.append(record)

    def all(self):
        return list(self._records)

    def filter(self, **criteria):
        """Filter records by matching key-value pairs."""
        result = self._records
        for key, value in criteria.items():
            result = [r for r in result if r.get(key) == value]
        return result

    def count(self):
        return len(self._records)


class ReportGenerator:
    """Generates reports using injected dependencies.

    The formatter and data store are passed in, not hardcoded.
    This is dependency injection.
    """

    def __init__(self, store: DataStore, formatter: ReportFormatter):
        self.store = store
        self.formatter = formatter

    def full_report(self, title="Full Report"):
        """Generate a report of all records."""
        data = self.store.all()
        return self.formatter.format(title, data)

    def filtered_report(self, title="Filtered Report", **criteria):
        """Generate a report of filtered records."""
        data = self.store.filter(**criteria)
        return self.formatter.format(title, data)
```

**New concepts introduced:**
- **Dependency Injection**: `ReportGenerator` does not create its own formatter or store — they are passed in from outside. This makes the class flexible and testable.
- **Repository pattern**: `DataStore` hides how data is stored. You could replace it with a real database later without changing `ReportGenerator`.
- **Separation of concerns**: storage, formatting, and orchestration are independent.

---

## Part 3: Tests

Create `test_bridge_8_to_9.py`:

```python
import json
import pytest
from bridge_8_to_9 import (
    DataStore,
    JsonFormatter,
    CsvFormatter,
    TextFormatter,
    ReportGenerator,
)


@pytest.fixture
def store():
    s = DataStore()
    s.add({"name": "Alice", "role": "engineer", "score": 95})
    s.add({"name": "Bob", "role": "designer", "score": 88})
    s.add({"name": "Charlie", "role": "engineer", "score": 72})
    return s


def test_store_count(store):
    assert store.count() == 3


def test_store_filter(store):
    engineers = store.filter(role="engineer")
    assert len(engineers) == 2


def test_json_formatter(store):
    gen = ReportGenerator(store, JsonFormatter())
    report = gen.full_report("Test Report")
    parsed = json.loads(report)
    assert parsed["title"] == "Test Report"
    assert len(parsed["data"]) == 3


def test_csv_formatter(store):
    gen = ReportGenerator(store, CsvFormatter())
    report = gen.full_report()
    lines = report.strip().split("\n")
    assert "name" in lines[0]  # header row
    assert len(lines) == 4  # header + 3 records


def test_text_formatter(store):
    gen = ReportGenerator(store, TextFormatter())
    report = gen.full_report("My Report")
    assert "My Report" in report
    assert "Alice" in report
    assert "Total records: 3" in report


def test_filtered_report(store):
    gen = ReportGenerator(store, JsonFormatter())
    report = gen.filtered_report("Engineers", role="engineer")
    parsed = json.loads(report)
    assert len(parsed["data"]) == 2


def test_swap_formatter(store):
    """Demonstrate that formatters are interchangeable."""
    json_gen = ReportGenerator(store, JsonFormatter())
    text_gen = ReportGenerator(store, TextFormatter())

    json_report = json_gen.full_report("R")
    text_report = text_gen.full_report("R")

    # Same data, different format
    assert json_report.startswith("{")
    assert text_report.startswith("===")
```

Run: `pytest test_bridge_8_to_9.py -v`

---

## You Are Ready

If you can define an abstract interface with ABC, implement the Strategy pattern with interchangeable classes, use dependency injection to keep components loosely coupled, and test each component independently, you are ready for Level 9.

---

| [Level 8 Projects](level-8/README.md) | [Home](../README.md) | [Level 9 Projects](level-9/README.md) |
|:---|:---:|---:|
