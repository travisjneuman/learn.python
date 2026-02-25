# How to Use This Curriculum

This guide walks you through how the curriculum is organized, what order to follow, and how to pace yourself.

---

## Reading Order

Start with these four documents, in this order:

1. **[START_HERE.md](./START_HERE.md)** -- Install Python and run your first script in under 10 minutes.
2. **[00_COMPUTER_LITERACY_PRIMER.md](./00_COMPUTER_LITERACY_PRIMER.md)** -- What a terminal, file, and program are. Skip this if you already know.
3. **[01_ROADMAP.md](./01_ROADMAP.md)** -- The full program overview: every level, every milestone.
4. **[03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md)** -- Detailed setup instructions for Windows, Mac, and Linux.

After that, follow the "Next" link at the bottom of every document. The entire curriculum is a single click chain -- you never have to figure out what comes next.

## Reference-Only Documents

These documents are not meant to be read front-to-back. Use them when you need to look something up:

- **[02_GLOSSARY.md](./02_GLOSSARY.md)** -- Definitions of key terms. Come back here when you encounter unfamiliar words.
- **[13_SAMPLE_DATABASE_SCHEMAS.md](./13_SAMPLE_DATABASE_SCHEMAS.md)** -- Example database schemas used in SQL-related projects. Relevant starting at Level 6.
- **[concepts/](./concepts/)** -- Concept guides on variables, loops, functions, etc. Read these when a project references them or when you need a refresher.

---

## Time Estimates

How long each section takes depends on your pace and prior experience. These are rough estimates for someone working through the material carefully, including the "Alter it / Break it / Fix it" exercises.

| Section | Estimated Hours |
|---------|----------------|
| Level 00 (Absolute Beginner) | ~5 hours |
| Level 0 (Terminal, Files, Basic I/O) | ~15 hours |
| Level 1 (Input, CSV, JSON, Paths) | ~20 hours |
| Level 2 (Data Structures, Cleaning) | ~20 hours |
| Level 3 (Packages, Logging, TDD) | ~25 hours |
| Level 4 (Schema Validation, Pipelines) | ~25 hours |
| Level 5 (Scheduling, Monitoring) | ~25 hours |
| Level 6 (SQL, ETL, Idempotency) | ~30 hours |
| Level 7 (APIs, Caching, Observability) | ~30 hours |
| Level 8 (Dashboards, Concurrency) | ~30 hours |
| Level 9 (Architecture, SLOs, Security) | ~35 hours |
| Level 10 (Enterprise, Production Readiness) | ~35 hours |
| Elite Track (Algorithms, Distributed Systems) | ~40 hours |
| Each Expansion Module (12 available) | ~10-20 hours |
| **Total** | **~400-500 hours** |

---

## Weekly Pacing Suggestions

| Hours per Week | Approximate Duration |
|----------------|---------------------|
| 5 hours/week | ~2 years |
| 10 hours/week | ~1 year |
| 20 hours/week | ~6 months |
| Full-time (40 hours/week) | ~3 months |

There is no rush. Consistent practice matters more than speed. It is better to spend 5 hours per week for two years than to cram for a month and burn out.

---

## What to Do When You Are Stuck

Getting stuck is normal. Here is a process that works:

1. **Read the error message.** Python error messages tell you exactly what went wrong and on which line. Read it from the bottom up.
2. **Re-read the concept doc.** Every project links to related concept guides. Go back and re-read the relevant section.
3. **Add `print()` statements.** Print the value of variables before the line that breaks. See what the data actually looks like.
4. **Check the [FAQ](./FAQ.md).** Common problems and solutions are collected there.
5. **Search the error message.** Copy the last line of the traceback and search for it online. Someone has hit the same error before.
6. **Open an issue.** If you think the curriculum itself has a bug (broken test, missing file, unclear instructions), [open an issue](https://github.com/travisjneuman/learn.python/issues) on GitHub.

---

## How to Track Your Progress

Run the progress tracker from the repository root:

```bash
python tools/progress.py
```

You can also manually update [PROGRESS.md](./PROGRESS.md) as you complete projects.

---

## Choosing a Learning Mode

The curriculum supports three modes. Pick the one that fits how you learn:

- **Play-First** -- Open a project, tinker, break things, figure it out. Read the concept doc when you get stuck.
- **Structured** -- Read the concept doc, take the quiz, then do the projects in order. Use checklists and mastery gates.
- **Hybrid (Recommended)** -- Follow the structured path on weekdays. Explore expansion modules and challenges on weekends. Review flashcards daily.

---

| [← Prev](README.md) | [Home](README.md) | [Next →](START_HERE.md) |
|:---|:---:|---:|
