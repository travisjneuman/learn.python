"""Tests for Pagination Stress Lab.

Covers: offset pagination, cursor pagination, edge cases, and stress invariants.
"""

from __future__ import annotations

import pytest

from project import (
    CursorPaginator,
    OffsetPaginator,
    PageRequest,
    PageResponse,
    stress_test_paginator,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def sample_data() -> list[str]:
    return [f"item_{i}" for i in range(1, 48)]  # 47 items


@pytest.fixture
def paginator(sample_data: list[str]) -> OffsetPaginator:
    return OffsetPaginator(sample_data)


# --- PageRequest validation ---------------------------------------------

class TestPageRequest:
    def test_valid_request(self) -> None:
        req = PageRequest(page=1, page_size=10)
        assert req.page == 1

    @pytest.mark.parametrize("page,page_size", [
        (0, 10),   # page too low
        (-1, 10),  # negative page
        (1, 0),    # zero page size
        (1, -5),   # negative page size
    ])
    def test_invalid_request_raises(self, page: int, page_size: int) -> None:
        with pytest.raises(ValueError):
            PageRequest(page=page, page_size=page_size)


# --- Offset pagination --------------------------------------------------

class TestOffsetPaginator:
    def test_first_page(self, paginator: OffsetPaginator) -> None:
        response = paginator.get_page(PageRequest(page=1, page_size=10))
        assert len(response.items) == 10
        assert response.has_next is True
        assert response.has_previous is False

    def test_last_page_partial(self, paginator: OffsetPaginator) -> None:
        """47 items / 10 per page = 5 pages, last page has 7 items."""
        response = paginator.get_page(PageRequest(page=5, page_size=10))
        assert len(response.items) == 7
        assert response.has_next is False

    def test_beyond_last_page_returns_empty(self, paginator: OffsetPaginator) -> None:
        response = paginator.get_page(PageRequest(page=99, page_size=10))
        assert response.is_empty
        assert response.has_next is False

    @pytest.mark.parametrize("page_size", [1, 5, 10, 47, 100])
    def test_iter_pages_collects_all_items(
        self, sample_data: list[str], page_size: int,
    ) -> None:
        """Iterating all pages should yield exactly all items, no duplicates."""
        pag = OffsetPaginator(sample_data)
        collected: list[str] = []
        for page in pag.iter_pages(page_size):
            collected.extend(page.items)
        assert collected == sample_data

    def test_total_pages_calculation(self, paginator: OffsetPaginator) -> None:
        assert paginator.total_pages(10) == 5
        assert paginator.total_pages(47) == 1
        assert paginator.total_pages(1) == 47


# --- Cursor pagination --------------------------------------------------

class TestCursorPaginator:
    def test_first_page(self, sample_data: list[str]) -> None:
        cpag = CursorPaginator(sample_data)
        page = cpag.get_page(cursor=0, limit=10)
        assert len(page.items) == 10
        assert page.has_more is True
        assert page.next_cursor == 10

    def test_last_page(self, sample_data: list[str]) -> None:
        cpag = CursorPaginator(sample_data)
        page = cpag.get_page(cursor=40, limit=10)
        assert len(page.items) == 7
        assert page.has_more is False
        assert page.next_cursor is None

    def test_negative_cursor_raises(self, sample_data: list[str]) -> None:
        cpag = CursorPaginator(sample_data)
        with pytest.raises(ValueError, match="Cursor must be >= 0"):
            cpag.get_page(cursor=-1, limit=10)


# --- Stress test --------------------------------------------------------

class TestStressTest:
    def test_stress_verification_all_pass(self) -> None:
        data = list(range(100))
        result = stress_test_paginator(data, page_sizes=[1, 7, 25, 100])
        for v in result["verification"]:
            assert v["matches_total"] is True

    def test_empty_dataset(self) -> None:
        result = stress_test_paginator([], page_sizes=[5])
        assert result["data_size"] == 0
