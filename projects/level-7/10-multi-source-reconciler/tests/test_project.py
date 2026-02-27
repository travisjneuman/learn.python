"""Tests for Multi-Source Reconciler."""

from __future__ import annotations

import json

import pytest

from project import (
    compare_records,
    index_by_key,
    reconcile,
    report_to_dict,
    run,
)


class TestIndexByKey:
    def test_basic_indexing(self) -> None:
        records = [{"id": "a", "v": 1}, {"id": "b", "v": 2}]
        idx = index_by_key(records, "id")
        assert idx["a"]["v"] == 1
        assert len(idx) == 2

    def test_missing_key_skipped(self) -> None:
        records = [{"other": "x"}]
        idx = index_by_key(records, "id")
        assert len(idx) == 0


class TestCompareRecords:
    def test_identical_records(self) -> None:
        left = {"_key": "1", "name": "a", "price": 10}
        right = {"_key": "1", "name": "a", "price": 10}
        diffs = compare_records(left, right, ["name", "price"])
        assert len(diffs) == 0

    def test_field_mismatch(self) -> None:
        left = {"_key": "1", "name": "a", "price": 10}
        right = {"_key": "1", "name": "a", "price": 20}
        diffs = compare_records(left, right, ["name", "price"])
        assert len(diffs) == 1
        assert diffs[0].field_name == "price"


class TestReconcile:
    def test_all_match(self) -> None:
        left = [{"id": "1", "v": "x"}, {"id": "2", "v": "y"}]
        right = [{"id": "1", "v": "x"}, {"id": "2", "v": "y"}]
        report = reconcile(left, right, "id", ["v"])
        assert report.matched == 2
        assert report.mismatched == 0

    def test_left_only_and_right_only(self) -> None:
        left = [{"id": "1", "v": "x"}, {"id": "3", "v": "z"}]
        right = [{"id": "1", "v": "x"}, {"id": "2", "v": "y"}]
        report = reconcile(left, right, "id", ["v"])
        assert "3" in report.left_only
        assert "2" in report.right_only

    @pytest.mark.parametrize("left_count,right_count", [(0, 0), (5, 5), (3, 7)])
    def test_various_sizes(self, left_count: int, right_count: int) -> None:
        left = [{"id": str(i), "v": i} for i in range(left_count)]
        right = [{"id": str(i), "v": i} for i in range(right_count)]
        report = reconcile(left, right, "id", ["v"])
        common = min(left_count, right_count)
        assert report.matched == common

    def test_mismatched_values_detected(self) -> None:
        left = [{"id": "1", "v": "old"}]
        right = [{"id": "1", "v": "new"}]
        report = reconcile(left, right, "id", ["v"])
        assert report.mismatched == 1
        assert len(report.mismatches) == 1


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "key_field": "sku",
        "compare_fields": ["price", "stock"],
        "left": [
            {"sku": "A1", "price": 10, "stock": 5},
            {"sku": "A2", "price": 20, "stock": 0},
        ],
        "right": [
            {"sku": "A1", "price": 10, "stock": 3},
            {"sku": "A3", "price": 30, "stock": 8},
        ],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["mismatched"] == 1   # A1 stock differs
    assert "A2" in summary["left_only"]
    assert "A3" in summary["right_only"]
