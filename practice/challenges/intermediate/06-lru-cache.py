"""
Challenge: LRU Cache
Difficulty: Intermediate
Concepts: dictionaries, doubly-linked lists, O(1) operations, data structures
Time: 45 minutes

Implement a Least Recently Used (LRU) cache with a fixed capacity.
- `get(key)` returns the value if present (and marks it as recently used), or -1 if not found.
- `put(key, value)` inserts or updates a key-value pair. If the cache exceeds
  capacity, evict the least recently used item.

Both get and put should run in O(1) average time.

Examples:
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)       # returns "a"
    cache.put(3, "c")  # evicts key 2
    cache.get(2)       # returns -1
"""


class LRUCache:
    """LRU Cache with O(1) get and put. Implement this class."""

    def __init__(self, capacity: int):
        # Hint: Use an OrderedDict, or a dict + doubly-linked list for O(1) move-to-end.
        pass

    def get(self, key):
        """Return value for key (mark as recently used) or -1 if not found."""
        pass

    def put(self, key, value) -> None:
        """Insert or update key-value pair. Evict LRU item if over capacity."""
        pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic put and get
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a", "Basic get failed"
    assert cache.get(2) == "b", "Basic get 2 failed"

    # Test 2: Eviction
    cache.put(3, "c")  # evicts key 1 (least recently used after get(1), get(2))
    # After get(1), get(2): order is 1, 2. So key 1 is LRU.
    # Wait -- get(1) was called first, then get(2). So 1 is older. Evict 1.
    assert cache.get(1) == -1, "Evicted key should return -1"
    assert cache.get(3) == "c", "New key should be present"

    # Test 3: Access updates recency
    cache2 = LRUCache(2)
    cache2.put(1, "a")
    cache2.put(2, "b")
    cache2.get(1)  # makes 1 most recent, 2 is now LRU
    cache2.put(3, "c")  # evicts key 2
    assert cache2.get(2) == -1, "Key 2 should be evicted"
    assert cache2.get(1) == "a", "Key 1 should still be present"

    # Test 4: Update existing key
    cache3 = LRUCache(2)
    cache3.put(1, "a")
    cache3.put(1, "b")  # update, not new entry
    assert cache3.get(1) == "b", "Updated value failed"

    # Test 5: Capacity of 1
    cache4 = LRUCache(1)
    cache4.put(1, "a")
    cache4.put(2, "b")  # evicts 1
    assert cache4.get(1) == -1, "Capacity 1 eviction failed"
    assert cache4.get(2) == "b", "Capacity 1 current failed"

    print("All tests passed!")
