# Level 8 / Project 02 - Query Cache Layer
Home: [README](../../../README.md)

## Focus
- LRU (Least Recently Used) cache with OrderedDict
- TTL (Time-To-Live) expiration with lazy invalidation
- Cache statistics: hit rate, evictions, expirations
- Decorator pattern for transparent function caching

## Why this project exists
Every production system uses caching — from database query results to API responses.
This project builds an LRU cache from scratch so you understand eviction policies, TTL
management, and hit-rate metrics before using tools like Redis or functools.lru_cache.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/02-query-cache-layer
python project.py --capacity 5 --ttl 10
pytest -q
```

## Expected terminal output
```text
{
  "queries_executed": 10,
  "cache_stats": {"hits": 4, "misses": 6, ...},
  ...
}
7 passed
```

## Expected artifacts
- Console output with cache stats
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `max_memory_bytes` limit that evicts entries when total value size exceeds a threshold.
2. Implement a `get_or_compute(key, factory_fn)` method that combines lookup and population.
3. Add a `--stats-file` CLI flag that writes cache statistics to a JSON file.

## Break it (required)
1. Set TTL to 0 — does every `get` immediately expire?
2. Store `None` as a cache value — can the cache distinguish "miss" from "cached None"?
3. Use a non-hashable type as a key in the `@cached` decorator.

## Fix it (required)
1. Handle TTL=0 as "no caching" or raise a clear error.
2. Use a sentinel value instead of `None` to distinguish misses from cached nulls.
3. Add a test for the None-value edge case.

## Explain it (teach-back)
1. Why does the LRU cache use `OrderedDict` instead of a regular `dict`?
2. What is "lazy expiration" and why is it used instead of a background timer?
3. How does the `@cached` decorator build its cache key? What could go wrong?
4. In production, when would you choose an in-process LRU cache vs. Redis?

## Mastery check
You can move on when you can:
- explain why OrderedDict.move_to_end is O(1),
- describe the tradeoff between eager and lazy TTL expiration,
- implement a cache warming strategy,
- calculate hit rate and explain what a "good" rate looks like.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../01-dashboard-kpi-assembler/README.md) | [Home](../../../README.md) | [Next →](../03-pagination-stress-lab/README.md) |
|:---|:---:|---:|
