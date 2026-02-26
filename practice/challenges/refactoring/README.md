# Refactoring Challenges

[Home](../../../README.md) · [Challenges](../README.md)

## Overview

These exercises give you working but messy code. The code does what it is supposed to do, but it is hard to read, maintain, and extend. Your job is to make it better without changing its behavior.

## Prerequisites

Complete **Level 3** before attempting these exercises. You should understand functions, error handling, file I/O, and testing well enough to restructure code confidently.

## Exercises

| # | Exercise | What you practice |
|---|----------|-------------------|
| 01 | [Spaghetti Calculator](./01_spaghetti_calculator/) | Extract functions, rename variables, add error handling, add type hints |
| 02 | [Monolithic Report](./02_monolithic_report/) | Decompose a god function, add logging, make output configurable |
| 03 | [Copy-Paste API](./03_copy_paste_api/) | DRY refactoring, extract helpers, add retry logic, extract config |

## The Golden Rule of Refactoring

**Tests must pass before AND after every change.**

Each exercise includes tests. Before you touch any code:
1. Run the tests. They should all pass.
2. Make one small refactoring change.
3. Run the tests again. They should still pass.
4. Repeat.

If the tests break, your refactoring changed behavior. Undo and try again.

## General Refactoring Goals

- Functions should do one thing and be under 30 lines
- Variable and function names should describe their purpose
- No copy-pasted blocks — extract shared logic into functions
- Reduce nesting depth (aim for 2 levels max)
- Add type hints to function signatures
- Replace magic numbers and strings with named constants
- The code should read top-to-bottom like a narrative
