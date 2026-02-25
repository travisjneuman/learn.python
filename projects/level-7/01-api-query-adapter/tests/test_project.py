"""Tests for API Query Adapter.

Validates adapter functions, the registry pattern, filtering,
and end-to-end query merging with mock API data.
"""

from __future__ import annotations

import json

import pytest

from project import (
    UnifiedRecord,
    adapt_api_a,
    adapt_api_b,
    adapt_api_c,
    adapt_response,
    filter_records,
    query_all_sources,
    run,
    MOCK_API_A,
    MOCK_API_B,
)


class TestAdapters:
    def test_api_a_adapter(self) -> None:
        records = adapt_api_a(MOCK_API_A)
        assert len(records) == 2
        assert records[0].source == "api_a"
        assert records[0].id == "A-001"

    def test_api_b_adapter(self) -> None:
        records = adapt_api_b(MOCK_API_B)
        assert records[0].name == "Bolt Pack"
        assert records[0].value == 3.49

    def test_api_c_adapter(self) -> None:
        records = adapt_api_c([{"sku": "X", "title": "Y", "amount": 1.0, "date": "2025-01-01"}])
        assert records[0].id == "X"

    @pytest.mark.parametrize("source", ["api_a", "api_b", "api_c"])
    def test_all_adapters_return_unified(self, source: str) -> None:
        mock_data = {
            "api_a": MOCK_API_A,
            "api_b": MOCK_API_B,
            "api_c": [{"sku": "X", "title": "Y", "amount": 1.0, "date": "t"}],
        }
        records = adapt_response(source, mock_data[source])
        assert all(isinstance(r, UnifiedRecord) for r in records)


class TestQueryEngine:
    def test_unknown_source_raises(self) -> None:
        with pytest.raises(ValueError, match="No adapter"):
            adapt_response("unknown_api", [])

    def test_query_all_merges_sources(self) -> None:
        records = query_all_sources()
        assert len(records) == 5  # 2 + 2 + 1

    def test_filter_by_min_value(self) -> None:
        records = query_all_sources()
        filtered = filter_records(records, min_value=5.0)
        assert all(r.value >= 5.0 for r in filtered)

    def test_filter_by_source(self) -> None:
        records = query_all_sources()
        filtered = filter_records(records, source="api_a")
        assert all(r.source == "api_a" for r in filtered)


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "sources": {
            "api_a": [{"item_id": "T1", "item_name": "Test", "price": 5.0, "ts": "2025-01-01"}],
        }
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["total_records"] == 1
    assert out.exists()
