# Generators and Iterators

A generator is a function that produces values one at a time instead of building an entire list in memory. It uses `yield` instead of `return`. This is how Python handles large datasets without running out of memory.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/generators-and-iterators.md) | [Quiz](quizzes/generators-and-iterators-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/generators-and-iterators.md) |

<!-- modality-hub-end -->

This concept is covered in two parts:

1. **[Part 1: Iterators](./generators-and-iterators-part1.md)** — The iterator protocol, memory efficiency, file reading, and `itertools` basics
2. **[Part 2: Generators](./generators-and-iterators-part2.md)** — `yield`, generator expressions, pipelines, `yield from`, and `send()`/`throw()`

## Practice

- [Level 2 / 07 Config File Merger](../projects/level-2/07-config-file-merger/README.md)
- [Module 05 Async Python](../projects/modules/05-async-python/) — generators are the foundation of async
- [Module 07 Data Analysis](../projects/modules/07-data-analysis/) — processing large datasets
- [Elite Track / 01 Algorithms Complexity Lab](../projects/elite-track/01-algorithms-complexity-lab/README.md)

**Quick check:** [Take the quiz](quizzes/generators-and-iterators-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [Generator expressions (Python docs)](https://docs.python.org/3/reference/expressions.html#generator-expressions)
- [itertools — Functions creating iterators](https://docs.python.org/3/library/itertools.html)
- [PEP 255 — Simple Generators](https://peps.python.org/pep-0255/)
- [PEP 380 — Syntax for Delegating to a Subgenerator (yield from)](https://peps.python.org/pep-0380/)

---

| [← Prev](context-managers-explained.md) | [Home](../README.md) | [Next →](comprehensions-explained.md) |
|:---|:---:|---:|
