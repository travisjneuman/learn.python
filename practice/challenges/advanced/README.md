# Advanced Coding Challenges

15 self-contained Python challenges for Level 6+ learners. Each file includes a
docstring explaining the problem, a function stub with type hints, and test cases
you can run directly.

## How to Use

1. Open a challenge file.
2. Read the docstring carefully — it describes the problem and constraints.
3. Implement the function(s) marked with `# YOUR CODE HERE`.
4. Run the file to execute the built-in tests:

```bash
python 01_generator_pipeline.py
```

All tests use `assert`, so silence means success. If a test fails you will see
an `AssertionError` with a descriptive message.

## Challenge Index

| #  | File                          | Topic                        | Level |
|----|-------------------------------|------------------------------|-------|
| 01 | `01_generator_pipeline.py`    | Generator chaining           | 6     |
| 02 | `02_custom_context_manager.py`| Context managers             | 6     |
| 03 | `03_async_web_scraper.py`     | asyncio concurrency          | 7     |
| 04 | `04_metaclass_registry.py`    | Metaclass auto-registration  | 8     |
| 05 | `05_type_narrowing.py`        | TypeGuard & type narrowing   | 7     |
| 06 | `06_decorator_stack.py`       | Composable decorators        | 6     |
| 07 | `07_dataclass_validation.py`  | Dataclass __post_init__      | 6     |
| 08 | `08_protocol_interfaces.py`   | Structural subtyping         | 7     |
| 09 | `09_async_producer_consumer.py`| asyncio.Queue patterns      | 8     |
| 10 | `10_descriptor_protocol.py`   | Custom descriptors           | 8     |
| 11 | `11_coroutine_scheduler.py`   | Cooperative scheduling       | 9     |
| 12 | `12_generic_repository.py`    | Generics with TypeVar        | 7     |
| 13 | `13_event_system.py`          | Pub/sub with weakrefs        | 8     |
| 14 | `14_ast_code_analyzer.py`     | AST module introspection     | 9     |
| 15 | `15_functional_pipeline.py`   | Functional composition       | 7     |

## Difficulty Guide

- **Level 6** — Solid intermediate: generators, context managers, decorators,
  dataclasses.
- **Level 7** — Advanced patterns: protocols, generics, type narrowing, asyncio
  basics, functional programming.
- **Level 8** — Expert territory: metaclasses, descriptors, producer/consumer,
  event systems.
- **Level 9** — Near-mastery: AST manipulation, cooperative schedulers.
- **Level 10** — (see elite-track for Level 10 challenges)

## Tips

- Read the type hints — they tell you exactly what the function should accept
  and return.
- Start with Level 6 challenges even if you think you are ready for higher
  levels. They build foundational patterns used in later challenges.
- If stuck, re-read the relevant concept doc linked in the docstring.
- Write your own additional test cases to build confidence.
