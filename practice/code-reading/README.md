# Code Reading Exercises

[Home](../../README.md) · [Practice](../README.md)

## Overview

These exercises develop a skill that many courses neglect: reading and understanding code written by someone else. In professional work you spend far more time reading code than writing it. Each exercise gives you a complete program and asks you to analyze it, find issues, extend it, and test it.

## Prerequisites

Complete **Level 2** before attempting these exercises. You should be comfortable with functions, files, lists, dicts, and basic error handling.

## Exercises

| # | Exercise | What you practice |
|---|----------|-------------------|
| 01 | [Mystery Function](./01_mystery_function/) | Trace execution, infer purpose, write docstrings and tests |
| 02 | [Find the Bugs](./02_find_the_bugs/) | Identify 4 subtle defects in a data processing pipeline |
| 03 | [Add a Feature](./03_add_a_feature/) | Understand a working TODO app, then extend it with 3 features |

## How to Work Through Each Exercise

1. **Read the code** in `codebase.py` without running it. Take notes.
2. **Answer the comprehension questions** in `README.md`.
3. **Complete the tasks** described in the README (trace, fix, extend, test).
4. Run `python -m pytest tests/` to verify your work.

## How to Approach Code Reading

1. **Skim first.** Read the imports, class/function names, and docstrings (if any). Get the shape of the code before reading line by line.
2. **Trace with real data.** Pick a concrete input and follow it through the code on paper or in your head.
3. **Ask "why?" at every branch.** Every `if`, `for`, and `try` exists for a reason. What case does it handle?
4. **Look for patterns.** Is this a pipeline? A state machine? A recursive processor? Naming the pattern helps you predict what comes next.
5. **Note what confuses you.** Confusion is signal. The confusing part is where the interesting logic lives.

## Why Code Reading Matters

- You will join teams with thousands of lines of existing code.
- Debugging starts with reading, not writing.
- Code reviews require you to understand code you did not write.
- Learning from others' code accelerates your own skill growth.
