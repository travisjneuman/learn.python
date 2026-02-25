"""
Challenge: Batch Processor
Difficulty: Intermediate
Concepts: generators, itertools, chunking, configurable processing
Time: 30 minutes

Implement a batch processor that processes items in configurable-size chunks.

1. `batch(iterable, size)` -- generator that yields lists of `size` items from the iterable.
   The last batch may be smaller if items don't divide evenly.

2. `process_batches(items, size, func)` -- apply `func` to each batch and return
   a flat list of results.

Examples:
    >>> list(batch([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    >>> process_batches([1, 2, 3, 4], 2, lambda b: [x * 2 for x in b])
    [2, 4, 6, 8]
"""


def batch(iterable, size: int):
    """Yield successive batches of `size` items from iterable. Implement this generator."""
    # Hint: Collect items into a temporary list; when it reaches `size`, yield it and start fresh.
    pass


def process_batches(items: list, size: int, func) -> list:
    """Process items in batches using func, return flat list of results. Implement this function."""
    # Hint: Use batch() to get chunks, apply func to each, then flatten the results.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Even batches
    assert list(batch([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]], "Even batches failed"

    # Test 2: Uneven last batch
    assert list(batch([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]], "Uneven batch failed"

    # Test 3: Batch size larger than list
    assert list(batch([1, 2], 5)) == [[1, 2]], "Large batch size failed"

    # Test 4: Empty iterable
    assert list(batch([], 3)) == [], "Empty iterable failed"

    # Test 5: batch is a generator
    gen = batch([1, 2, 3], 2)
    assert hasattr(gen, "__next__"), "batch should be a generator"

    # Test 6: process_batches basic
    result = process_batches([1, 2, 3, 4], 2, lambda b: [x * 2 for x in b])
    assert result == [2, 4, 6, 8], "process_batches basic failed"

    # Test 7: process_batches with transformation
    result = process_batches(["a", "b", "c"], 2, lambda b: [s.upper() for s in b])
    assert result == ["A", "B", "C"], "process_batches transform failed"

    # Test 8: Batch size of 1
    assert list(batch([1, 2, 3], 1)) == [[1], [2], [3]], "Batch size 1 failed"

    print("All tests passed!")
