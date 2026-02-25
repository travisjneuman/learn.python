"""Tests for Architecture Decision Log.

Covers: CRUD operations, status transitions, observer pattern, search, and superseding.
"""

from __future__ import annotations

import pytest

from project import ADR, ADRLog, ADRStatus


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def log() -> ADRLog:
    return ADRLog()


@pytest.fixture
def populated_log(log: ADRLog) -> ADRLog:
    log.create("Use PostgreSQL", "Need relational DB", "Use PG", "Need expertise", tags=["db"])
    log.create("Use REST API", "Need public API", "Use REST", "Simple tooling", tags=["api"])
    log.create("Add Redis cache", "High latency", "Use Redis", "Need Redis ops", tags=["cache"])
    return log


# --- Create and retrieve ------------------------------------------------

class TestCRUD:
    def test_create_returns_adr(self, log: ADRLog) -> None:
        adr = log.create("Title", "ctx", "dec", "cons")
        assert adr.adr_id == 1
        assert adr.status == ADRStatus.PROPOSED

    def test_auto_incrementing_ids(self, log: ADRLog) -> None:
        a1 = log.create("First", "c", "d", "c")
        a2 = log.create("Second", "c", "d", "c")
        assert a2.adr_id == a1.adr_id + 1

    def test_get_existing(self, populated_log: ADRLog) -> None:
        adr = populated_log.get(1)
        assert adr is not None
        assert adr.title == "Use PostgreSQL"

    def test_get_nonexistent(self, log: ADRLog) -> None:
        assert log.get(999) is None


# --- Status transitions -------------------------------------------------

class TestStatusTransitions:
    def test_accept_adr(self, populated_log: ADRLog) -> None:
        adr = populated_log.update_status(1, ADRStatus.ACCEPTED)
        assert adr.status == ADRStatus.ACCEPTED

    def test_update_nonexistent_raises(self, log: ADRLog) -> None:
        with pytest.raises(KeyError, match="ADR 999"):
            log.update_status(999, ADRStatus.ACCEPTED)

    @pytest.mark.parametrize("status", [
        ADRStatus.ACCEPTED, ADRStatus.DEPRECATED, ADRStatus.REJECTED,
    ])
    def test_all_status_transitions(self, log: ADRLog, status: ADRStatus) -> None:
        adr = log.create("T", "c", "d", "c")
        updated = log.update_status(adr.adr_id, status)
        assert updated.status == status


# --- Observer pattern ---------------------------------------------------

class TestObserver:
    def test_observer_called_on_change(self, log: ADRLog) -> None:
        events: list[tuple[int, str, str]] = []
        log.on_status_change(
            lambda adr, old, new: events.append((adr.adr_id, old.value, new.value))
        )
        adr = log.create("T", "c", "d", "c")
        log.update_status(adr.adr_id, ADRStatus.ACCEPTED)
        assert len(events) == 1
        assert events[0] == (adr.adr_id, "proposed", "accepted")


# --- Search and filtering -----------------------------------------------

class TestSearchFilter:
    def test_search_by_title(self, populated_log: ADRLog) -> None:
        results = populated_log.search("PostgreSQL")
        assert len(results) == 1

    def test_search_case_insensitive(self, populated_log: ADRLog) -> None:
        results = populated_log.search("postgresql")
        assert len(results) == 1

    def test_filter_by_tag(self, populated_log: ADRLog) -> None:
        results = populated_log.filter_by_tag("api")
        assert len(results) == 1

    def test_filter_by_status(self, populated_log: ADRLog) -> None:
        results = populated_log.filter_by_status(ADRStatus.PROPOSED)
        assert len(results) == 3


# --- Superseding --------------------------------------------------------

class TestSupersede:
    def test_supersede_marks_old(self, populated_log: ADRLog) -> None:
        populated_log.supersede(1, 2)
        old = populated_log.get(1)
        assert old is not None
        assert old.status == ADRStatus.SUPERSEDED
        assert old.superseded_by == 2

    def test_supersede_nonexistent_raises(self, log: ADRLog) -> None:
        log.create("A", "c", "d", "c")
        with pytest.raises(KeyError):
            log.supersede(1, 999)
