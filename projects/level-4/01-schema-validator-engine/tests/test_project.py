"""Tests for Schema Validator Engine.

Covers: required-field enforcement, type checking, range validation,
extra-field detection, and full-run integration.
"""

from pathlib import Path
import json
import pytest

from project import validate_record, validate_all, load_schema, load_records, run

# -- sample schema used across tests --

SAMPLE_SCHEMA = {
    "fields": {
        "name": {"type": "string", "required": True},
        "age": {"type": "integer", "required": True, "min": 0, "max": 150},
        "email": {"type": "string", "required": False},
    }
}


# -- validate_record tests --

@pytest.mark.parametrize(
    "record, expected_error_count",
    [
        ({"name": "Alice", "age": 30}, 0),
        ({"name": "Bob", "age": 25, "email": "bob@example.com"}, 0),
        ({"age": 30}, 1),                          # missing required 'name'
        ({"name": "X"}, 1),                         # missing required 'age'
        ({"name": 123, "age": 30}, 1),              # wrong type for 'name'
        ({"name": "A", "age": -5}, 1),              # age below min
        ({"name": "A", "age": 200}, 1),             # age above max
        ({"name": "A", "age": 30, "extra": 1}, 1),  # unexpected field
    ],
)
def test_validate_record_parametrized(record: dict, expected_error_count: int) -> None:
    errors = validate_record(record, SAMPLE_SCHEMA)
    assert len(errors) == expected_error_count


def test_validate_record_multiple_errors() -> None:
    """A record with several problems should collect all errors at once."""
    record = {"age": "not_a_number"}  # missing 'name' + wrong type for 'age'
    errors = validate_record(record, SAMPLE_SCHEMA)
    assert len(errors) >= 2


def test_validate_all_report_structure() -> None:
    records = [
        {"name": "Alice", "age": 30},
        {"name": "Bob"},  # missing age
    ]
    report = validate_all(records, SAMPLE_SCHEMA)
    assert report["total"] == 2
    assert report["valid"] == 1
    assert report["invalid"] == 1
    assert len(report["errors"]) == 1
    assert report["errors"][0]["record_index"] == 1


def test_full_run_writes_report(tmp_path: Path) -> None:
    """Integration test: schema + records files in, report file out."""
    schema_file = tmp_path / "schema.json"
    schema_file.write_text(json.dumps(SAMPLE_SCHEMA), encoding="utf-8")

    records_file = tmp_path / "records.json"
    records_file.write_text(
        json.dumps([
            {"name": "Alice", "age": 30},
            {"name": 42, "age": 30},
        ]),
        encoding="utf-8",
    )

    output_file = tmp_path / "report.json"
    report = run(schema_file, records_file, output_file)

    assert output_file.exists()
    assert report["valid"] == 1
    assert report["invalid"] == 1


def test_load_records_rejects_non_array(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text('{"not": "an array"}', encoding="utf-8")
    with pytest.raises(ValueError, match="JSON array"):
        load_records(bad_file)
