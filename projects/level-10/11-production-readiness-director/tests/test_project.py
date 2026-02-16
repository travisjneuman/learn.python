"""Advanced test module with heavy comments.

Coverage goals:
- input loading integrity,
- transformation correctness,
- summary metrics and diagnostics fields.
"""

# Path gives portable temporary-file path handling.
from pathlib import Path

# Import advanced helper functions under test.
from project import build_records, build_summary, load_items


def test_load_items_removes_blank_lines(tmp_path: Path) -> None:
    """Loader should normalize whitespace and drop empty rows."""
    # Arrange: mixed raw text including blank and padded lines.
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha\n\n beta \n", encoding="utf-8")

    # Act: call loader.
    items = load_items(sample)

    # Assert: only normalized non-empty values remain.
    assert items == ["alpha", "beta"]


def test_build_records_contains_normalized_field() -> None:
    """Transform should expose normalized values for downstream joins."""
    # Arrange: values with spaces/casing differences.
    source_items = ["High Latency", "Disk Full"]

    # Act: transform into structured records.
    records = build_records(source_items)

    # Assert: normalized field uses lowercase underscore style.
    assert records[0]["normalized"] == "high_latency"
    assert records[1]["normalized"] == "disk_full"


def test_build_summary_reports_elapsed_ms_field() -> None:
    """Summary must include elapsed_ms for run diagnostics."""
    # Arrange: deterministic input set.
    records = build_records(["one", "two", "three"])

    # Act: include explicit elapsed metric.
    summary = build_summary(records, elapsed_ms=17)

    # Assert: both record count and elapsed metric are preserved.
    assert summary["record_count"] == 3
    assert summary["elapsed_ms"] == 17
