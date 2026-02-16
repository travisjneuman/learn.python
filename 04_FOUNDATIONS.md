# 04 — Foundations (Learn the logic, not just syntax)

## Purpose
Before automating Excel/SQL/SolarWinds, you must be able to:
- read code you didn’t write
- debug errors without guessing
- break problems into steps

Primary study backbone:
- Automate the Boring Stuff (3rd edition), Ch. 1–11 citeturn0search12turn0search19

Secondary reference:
- Python official tutorial (venv chapter is also useful later) citeturn0search1

---

## Daily workflow (beginner-friendly)
Each learning session:
1. **Read** (20–30 min)
2. **Type the code yourself** (do not copy-paste)
3. **Change it** (make it break, then fix it)
4. **Write a micro script** (30–120 lines)
5. **Write 5 bullet notes**: what was confusing + what clicked

---

## Core skills and the “why” (you are building muscle memory)

### 1) Variables and types
What to learn:
- numbers (int/float), strings, booleans, None
Why it matters:
- “5” (text) is not 5 (a number). Mixing them causes bugs.

Micro exercise:
- parse a text number `"42"` into an int and add 10
- format results into a string message

### 2) Flow control
What to learn:
- if/elif/else
Why it matters:
- automation is “if condition then action else other action”

Micro exercise:
- if severity is CRITICAL, print “page me” else “log only”

### 3) Loops
What to learn:
- for, while
Why it matters:
- you process rows, files, servers, alerts, tickets… in loops

Micro exercise:
- loop through a list of filenames and print a report line per file

### 4) Lists and dictionaries (critical)
Why it matters:
- lists: rows, ordered collections
- dicts: records like {"customer": "KION", "status": "Critical"}

Micro exercise:
- build a list of dicts representing 5 “alerts” and filter critical ones

### 5) Functions (SME accelerator)
Goal behavior:
- never write the same logic twice
- functions are *named chunks* you can test

Micro exercise:
- write `normalize_status(text: str) -> str` that maps variants to standard values

### 6) Debugging
What to learn:
- read tracebacks (error line, error type, message)
- use the debugger (breakpoints)
Why it matters:
- SMEs don’t “guess”; they reduce uncertainty fast.

Micro exercise:
- intentionally create a `KeyError`, then fix by using `.get()` or validation

### 7) Files and paths
What to learn:
- open/read/write
- use pathlib for Windows-safe paths
Why it matters:
- reporting starts with files and ends with files.

Micro exercise:
- read a text file, count lines, write a summary file

---

## Minimum mastery checklist (before moving on)
You can confidently:
- write a function with inputs/outputs
- loop through records and filter them
- read/write files
- explain what a traceback is telling you

Next: **[09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md)**
