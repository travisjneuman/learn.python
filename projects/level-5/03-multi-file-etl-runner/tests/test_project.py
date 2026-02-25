"""Tests for Multi File ETL Runner."""
from pathlib import Path
import pytest
from project import transform_row, merge_append, merge_deduplicate, merge_update, run_etl, run

def test_transform_row():
    row = {"  Name  ": "  Alice  ", "AGE": "30"}
    result = transform_row(row)
    assert result["name"] == "Alice"
    assert result["age"] == "30"

def test_merge_append():
    assert len(merge_append([{"a": 1}], [{"a": 2}])) == 2

def test_merge_deduplicate():
    existing = [{"id": "1", "name": "Alice"}]
    new = [{"id": "1", "name": "Alice2"}, {"id": "2", "name": "Bob"}]
    result = merge_deduplicate(existing, new, "id")
    assert len(result) == 2
    assert result[0]["name"] == "Alice"  # original kept

def test_merge_update():
    existing = [{"id": "1", "name": "Alice"}]
    new = [{"id": "1", "name": "Alice2"}, {"id": "2", "name": "Bob"}]
    result = merge_update(existing, new, "id")
    assert len(result) == 2
    assert result[0]["name"] == "Alice2"  # updated

@pytest.mark.parametrize("strategy", ["append", "deduplicate", "update"])
def test_run_etl_all_strategies(tmp_path: Path, strategy):
    f1 = tmp_path / "a.csv"
    f1.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")
    f2 = tmp_path / "b.csv"
    f2.write_text("id,name\n2,Bobby\n3,Charlie\n", encoding="utf-8")
    data, log = run_etl([f1, f2], strategy, "id")
    assert len(data) >= 3 or strategy != "append"
    assert len(log) == 2

def test_run_integration(tmp_path: Path):
    src = tmp_path / "sources"
    src.mkdir()
    (src / "data1.csv").write_text("id,val\n1,a\n2,b\n", encoding="utf-8")
    (src / "data2.csv").write_text("id,val\n3,c\n", encoding="utf-8")
    output = tmp_path / "out.json"
    report = run(src, output, "append")
    assert report["total_records"] == 3
