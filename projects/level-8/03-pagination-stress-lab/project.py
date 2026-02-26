"""Pagination Stress Lab — test pagination logic with various page sizes and edge cases.

Design rationale:
    Pagination is deceptively tricky: off-by-one errors, empty last pages,
    total-count mismatches, and cursor vs. offset strategies all create bugs
    in production. This lab builds a paginator from scratch and stress-tests
    it with adversarial inputs.

Concepts practised:
    - offset-based and cursor-based pagination
    - dataclasses for page metadata
    - edge case handling (empty collections, page > total)
    - generator-based page iteration
    - property validation
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from typing import Any, Generic, Iterator, TypeVar

T = TypeVar("T")


# --- Domain types -------------------------------------------------------

# WHY __post_init__ validation? -- Dataclasses auto-generate __init__ but
# don't validate arguments. __post_init__ runs immediately after __init__,
# making it the idiomatic place to enforce invariants (page >= 1) without
# writing a manual constructor. This prevents impossible states at creation.
@dataclass
class PageRequest:
    """Parameters for a single page request."""
    page: int = 1
    page_size: int = 10

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError(f"Page must be >= 1, got {self.page}")
        if self.page_size < 1:
            raise ValueError(f"Page size must be >= 1, got {self.page_size}")


@dataclass
class PageResponse:
    """A single page of results with navigation metadata."""
    items: list[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "items": self.items,
            "page": self.page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_previous": self.has_previous,
        }


@dataclass
class PaginationStats:
    """Accumulated stats from a pagination stress run."""
    total_requests: int = 0
    empty_pages: int = 0
    boundary_hits: int = 0  # first or last page
    out_of_range: int = 0
    items_served: int = 0


# --- Paginator ----------------------------------------------------------

class OffsetPaginator:
    """Offset-based paginator over an in-memory collection.

    Slices the data list using (page - 1) * page_size as the offset.
    This is the most common pagination strategy in REST APIs.
    """

    def __init__(self, data: list[Any]) -> None:
        self._data = data

    @property
    def total_items(self) -> int:
        return len(self._data)

    def total_pages(self, page_size: int) -> int:
        """Calculate total pages for a given page size."""
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        return max(1, math.ceil(len(self._data) / page_size))

    def get_page(self, request: PageRequest) -> PageResponse:
        """Fetch a single page of results."""
        total_pg = self.total_pages(request.page_size)
        offset = (request.page - 1) * request.page_size
        items = self._data[offset : offset + request.page_size]

        return PageResponse(
            items=items,
            page=request.page,
            page_size=request.page_size,
            total_items=self.total_items,
            total_pages=total_pg,
        )

    def iter_pages(self, page_size: int) -> Iterator[PageResponse]:
        """Yield all pages in order — useful for bulk processing."""
        total_pg = self.total_pages(page_size)
        for page_num in range(1, total_pg + 1):
            yield self.get_page(PageRequest(page=page_num, page_size=page_size))


# --- Cursor-based pagination --------------------------------------------

@dataclass
class CursorPage:
    """A page of results using cursor-based (keyset) pagination."""
    items: list[Any]
    next_cursor: int | None  # index of next item, or None if at end
    has_more: bool


class CursorPaginator:
    """Cursor-based paginator — avoids the "page drift" problem of offset pagination.

    Instead of page numbers, the client sends a cursor (an index into the data).
    This is more efficient for large datasets and immune to insertion/deletion drift.
    """

    def __init__(self, data: list[Any]) -> None:
        self._data = data

    def get_page(self, cursor: int = 0, limit: int = 10) -> CursorPage:
        """Fetch items starting from *cursor* up to *limit* items."""
        if cursor < 0:
            raise ValueError("Cursor must be >= 0")
        if limit < 1:
            raise ValueError("Limit must be >= 1")

        items = self._data[cursor : cursor + limit]
        next_pos = cursor + limit
        has_more = next_pos < len(self._data)

        return CursorPage(
            items=items,
            next_cursor=next_pos if has_more else None,
            has_more=has_more,
        )


# --- Stress testing -----------------------------------------------------

def stress_test_paginator(
    data: list[Any],
    page_sizes: list[int] | None = None,
) -> dict[str, Any]:
    """Run a stress test over the paginator with various page sizes.

    Tests boundary conditions: first page, last page, beyond-range pages,
    single-item pages, and page sizes larger than the dataset.
    """
    if page_sizes is None:
        page_sizes = [1, 2, 5, 10, 25, 100, len(data), len(data) + 1]

    paginator = OffsetPaginator(data)
    stats = PaginationStats()
    results: list[dict[str, Any]] = []

    for ps in page_sizes:
        if ps < 1:
            continue
        total_pg = paginator.total_pages(ps)

        # Test each page
        for page_num in range(1, total_pg + 2):  # +2 to test beyond-range
            stats.total_requests += 1
            request = PageRequest(page=page_num, page_size=ps)
            response = paginator.get_page(request)

            if response.is_empty:
                stats.empty_pages += 1
            if page_num == 1 or page_num == total_pg:
                stats.boundary_hits += 1
            if page_num > total_pg:
                stats.out_of_range += 1
            stats.items_served += len(response.items)

            results.append({
                "page_size": ps,
                "page": page_num,
                "items_count": len(response.items),
                "has_next": response.has_next,
                "has_previous": response.has_previous,
            })

    # Verify invariant: all items seen exactly once per page_size
    verification: list[dict[str, Any]] = []
    for ps in page_sizes:
        if ps < 1:
            continue
        all_items: list[Any] = []
        for page in paginator.iter_pages(ps):
            all_items.extend(page.items)
        verification.append({
            "page_size": ps,
            "items_collected": len(all_items),
            "matches_total": len(all_items) == len(data),
        })

    return {
        "data_size": len(data),
        "page_sizes_tested": page_sizes,
        "stats": {
            "total_requests": stats.total_requests,
            "empty_pages": stats.empty_pages,
            "boundary_hits": stats.boundary_hits,
            "out_of_range": stats.out_of_range,
            "items_served": stats.items_served,
        },
        "verification": verification,
        "sample_results": results[:10],
    }


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pagination stress testing lab")
    parser.add_argument("--items", type=int, default=47, help="Number of items in dataset")
    parser.add_argument(
        "--page-sizes", nargs="*", type=int, default=None,
        help="Page sizes to test (default: auto)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    data = [f"item_{i:04d}" for i in range(1, args.items + 1)]
    output = stress_test_paginator(data, page_sizes=args.page_sizes)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
