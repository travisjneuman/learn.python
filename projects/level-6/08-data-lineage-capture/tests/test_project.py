"""Tests for Data Lineage Capture.

Validates lineage recording, chain retrieval, and the full
three-step pipeline using in-memory SQLite.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from project import (
    LineageEntry,
    get_lineage_chain,
    init_db,
    record_lineage,
    run,
    step_ingest,
    step_normalize,
    step_publish,
)


@pytest.fixture()
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    init_db(c)
    yield c
    c.close()


SAMPLE_RECORDS = [
    {"key": "order-1", "value": "100"},
    {"key": "order-2", "value": "200"},
]


class TestLineageRecording:
    def test_record_returns_id(self, conn: sqlite3.Connection) -> None:
        lid = record_lineage(conn, LineageEntry(
            record_key="k1", step_name="ingest",
            source="file", destination="staging",
        ))
        assert isinstance(lid, int)
        assert lid > 0

    def test_chain_builds_incrementally(self, conn: sqlite3.Connection) -> None:
        lid1 = record_lineage(conn, LineageEntry(
            record_key="k1", step_name="step1",
            source="a", destination="b",
        ))
        record_lineage(conn, LineageEntry(
            record_key="k1", step_name="step2",
            source="b", destination="c", parent_id=lid1,
        ))
        chain = get_lineage_chain(conn, "k1")
        assert len(chain) == 2
        assert chain[0]["step"] == "step1"
        assert chain[1]["parent_id"] == lid1

    @pytest.mark.parametrize("key", ["alpha", "beta", "gamma"])
    def test_chains_isolated_by_key(self, conn: sqlite3.Connection, key: str) -> None:
        record_lineage(conn, LineageEntry(
            record_key=key, step_name="ingest",
            source="src", destination="dst",
        ))
        chain = get_lineage_chain(conn, key)
        assert len(chain) == 1
        assert chain[0]["source"] == "src"


class TestPipelineSteps:
    def test_ingest_creates_lineage(self, conn: sqlite3.Connection) -> None:
        results = step_ingest(conn, SAMPLE_RECORDS)
        assert len(results) == 2
        assert all(r["stage"] == "raw" for r in results)

    def test_full_pipeline_three_steps(self, conn: sqlite3.Connection) -> None:
        step_ingest(conn, SAMPLE_RECORDS)
        step_normalize(conn, SAMPLE_RECORDS)
        step_publish(conn, SAMPLE_RECORDS)

        chain = get_lineage_chain(conn, "order-1")
        assert len(chain) == 3
        steps = [c["step"] for c in chain]
        assert steps == ["ingest", "normalize", "publish"]


def test_run_end_to_end(tmp_path) -> None:
    inp = tmp_path / "data.json"
    inp.write_text(json.dumps(SAMPLE_RECORDS), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["records_processed"] == 2
    assert summary["pipeline_steps"] == 3
    # 2 records x 3 steps = 6 lineage entries
    assert summary["total_lineage_entries"] == 6
    assert out.exists()
