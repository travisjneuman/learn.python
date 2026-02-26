# Level 8 / Project 02 - Query Cache Layer
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

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
Extend this project in a meaningful way — add a feature that addresses a real use case.

## Break it (required)
Introduce a subtle bug and see if your tests catch it. If they don't, write a test that would.

## Fix it (required)
Review your code critically — is there a design pattern that would improve it?

## Explain it (teach-back)
Could you explain the architectural trade-offs to a colleague?

## Mastery check
You can move on when you can:
- explain why OrderedDict.move_to_end is O(1),
- describe the tradeoff between eager and lazy TTL expiration,
- implement a cache warming strategy,
- calculate hit rate and explain what a "good" rate looks like.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

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
