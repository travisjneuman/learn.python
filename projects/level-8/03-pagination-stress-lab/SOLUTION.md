# Solution: Level 8 / Project 03 - Pagination Stress Lab

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Pagination Stress Lab -- test pagination logic with various page sizes and edge cases."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from typing import Any, Iterator, TypeVar

T = TypeVar("T")


# --- Domain types -------------------------------------------------------

# WHY __post_init__ validation? -- Dataclasses auto-generate __init__ but
# don't validate. __post_init__ runs immediately after construction,
# preventing impossible states (page 0, negative page size) from existing.
@dataclass
class PageRequest:
    page: int = 1
    page_size: int = 10

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError(f"Page must be >= 1, got {self.page}")
        if self.page_size < 1:
            raise ValueError(f"Page size must be >= 1, got {self.page_size}")


@dataclass
class PageResponse:
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
            "items": self.items, "page": self.page,
            "page_size": self.page_size, "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_next": self.has_next, "has_previous": self.has_previous,
        }


@dataclass
class PaginationStats:
    total_requests: int = 0
    empty_pages: int = 0
    boundary_hits: int = 0
    out_of_range: int = 0
    items_served: int = 0


# --- Offset Paginator ---------------------------------------------------

class OffsetPaginator:
    """WHY offset-based? -- This is the most common pagination in REST APIs
    (LIMIT/OFFSET in SQL). The client specifies a page number, and the
    server slices the data. Simple, but vulnerable to page drift if items
    are inserted/deleted between requests."""

    def __init__(self, data: list[Any]) -> None:
        self._data = data

    @property
    def total_items(self) -> int:
        return len(self._data)

    def total_pages(self, page_size: int) -> int:
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        # WHY max(1, ...)? -- Even an empty dataset has 1 page (the empty page).
        # This prevents "0 of 0 pages" confusion in the UI.
        return max(1, math.ceil(len(self._data) / page_size))

    def get_page(self, request: PageRequest) -> PageResponse:
        total_pg = self.total_pages(request.page_size)
        # WHY (page - 1) * page_size? -- Pages are 1-indexed for humans
        # but slices are 0-indexed. Subtracting 1 converts between them.
        offset = (request.page - 1) * request.page_size
        items = self._data[offset : offset + request.page_size]
        return PageResponse(
            items=items, page=request.page, page_size=request.page_size,
            total_items=self.total_items, total_pages=total_pg,
        )

    def iter_pages(self, page_size: int) -> Iterator[PageResponse]:
        """WHY a generator? -- Yielding pages one at a time avoids loading
        all pages into memory simultaneously. For bulk export or ETL
        pipelines, this is essential."""
        total_pg = self.total_pages(page_size)
        for page_num in range(1, total_pg + 1):
            yield self.get_page(PageRequest(page=page_num, page_size=page_size))


# --- Cursor Paginator ---------------------------------------------------

@dataclass
class CursorPage:
    items: list[Any]
    next_cursor: int | None
    has_more: bool


class CursorPaginator:
    """WHY cursor-based as an alternative? -- Cursor pagination avoids the
    "page drift" problem: if rows are inserted while a user is paginating
    with offsets, they might see duplicates or miss items. Cursors point
    to a stable position in the dataset."""

    def __init__(self, data: list[Any]) -> None:
        self._data = data

    def get_page(self, cursor: int = 0, limit: int = 10) -> CursorPage:
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
    """WHY stress testing pagination? -- Off-by-one errors, empty last pages,
    and total-count mismatches are among the most common API bugs. Testing
    with adversarial page sizes (1, size+1) catches edge cases that normal
    usage never exercises."""
    if page_sizes is None:
        page_sizes = [1, 2, 5, 10, 25, 100, len(data), len(data) + 1]

    paginator = OffsetPaginator(data)
    stats = PaginationStats()
    results: list[dict[str, Any]] = []

    for ps in page_sizes:
        if ps < 1:
            continue
        total_pg = paginator.total_pages(ps)
        # WHY total_pg + 2? -- We test one page beyond the last to verify
        # that out-of-range requests return empty results gracefully
        # rather than raising exceptions.
        for page_num in range(1, total_pg + 2):
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
                "page_size": ps, "page": page_num,
                "items_count": len(response.items),
                "has_next": response.has_next, "has_previous": response.has_previous,
            })

    # WHY verify the invariant separately? -- Iterating all pages and
    # checking that total items collected == dataset size catches
    # duplicates and missing items that individual page tests miss.
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Pagination stress testing lab")
    parser.add_argument("--items", type=int, default=47)
    parser.add_argument("--page-sizes", nargs="*", type=int, default=None)
    args = parser.parse_args(argv)
    data = [f"item_{i:04d}" for i in range(1, args.items + 1)]
    output = stress_test_paginator(data, page_sizes=args.page_sizes)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Both offset and cursor paginators | Offset is simpler for most APIs; cursor avoids page drift on mutable datasets | Only offset -- misses the lesson about why cursor pagination exists |
| `math.ceil` for total_pages | Correctly handles partial last pages (47 items / 10 = 5 pages, not 4) | Integer division + conditional -- more code for the same result |
| Generator-based `iter_pages` | Memory-efficient iteration; processes one page at a time | Return `list[PageResponse]` -- simpler API but loads all pages into memory |
| Stress test beyond-range pages | Verifies graceful handling of page > total_pages | Only test valid pages -- misses the most common real-world edge case |

## Alternative approaches

### Approach B: Keyset pagination with database-style WHERE clause

```python
def keyset_paginate(data: list[dict], sort_key: str, after_value: Any, limit: int):
    """Pagination using WHERE sort_key > after_value ORDER BY sort_key LIMIT n.
    More efficient than OFFSET for large datasets because the database
    can use an index to jump directly to the starting point."""
    filtered = [row for row in data if row[sort_key] > after_value]
    filtered.sort(key=lambda r: r[sort_key])
    page = filtered[:limit]
    next_cursor = page[-1][sort_key] if len(page) == limit else None
    return page, next_cursor
```

**Trade-off:** Keyset pagination is the most efficient approach for database-backed APIs (it avoids the O(n) cost of OFFSET). However, it requires a unique, sortable column and doesn't support "jump to page 5" -- only "next page" navigation.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| 47 items with page_size=10 | Last page has only 7 items; `math.ceil(47/10)=5` pages | The slice `data[40:50]` naturally returns 7 items -- Python slicing handles it |
| page_size larger than dataset | `math.ceil(3/100)=1` page with all 3 items | Works correctly; stress test includes `len(data)+1` to verify this |
| Requesting page 0 or negative | Off-by-one; offset becomes negative, returning wrong items | `__post_init__` validation raises ValueError for page < 1 |
