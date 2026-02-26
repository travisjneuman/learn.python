# 28 - Levels 0 to 2 Deep Guide (Beginner to Competent)
Home: [README](../README.md)

Path placeholder: `<repo-root>` means the folder containing this repository's `README.md`.

This guide is your exact execution protocol for levels 0, 1, and 2.

## Objective
Turn a beginner into a consistent builder of small, reliable Python tools.

## Required inputs
- [projects/level-0/README.md](../projects/level-0/README.md)
- [projects/level-1/README.md](../projects/level-1/README.md)
- [projects/level-2/README.md](../projects/level-2/README.md)
- [04_FOUNDATIONS.md](../04_FOUNDATIONS.md)

## Standard run pattern (copy/paste)
```bash
cd <repo-root>/projects/level-0/01-terminal-hello-lab
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

Expected output:
```text
... output_summary.json written ...
2 passed
```

## Per-project sequence (do not skip steps)
1. Read project README first.
2. Run baseline script.
3. Run tests.
4. Read `project.py` top to bottom.
5. Do one "alter" change.
6. Do one "break" change.
7. Fix and verify.
8. Record root cause notes.

## Break/fix drill examples
Choose one per project:
1. Remove or rename a required input line and verify safe handling.
2. Change a condition and verify tests catch bad behavior.
3. Change output key names and verify tests fail then fix correctly.

## Weekly completion target
- Minimum: 3 projects/week.
- Recommended: 5 projects/week.
- Accelerated: 7+ projects/week.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: mutate constants and inputs and observe output changes.
- Build: run every step in this doc exactly.
- Dissect: rewrite one project with simpler variable names and comments.
- Teach-back: explain one finished project in 5 minutes to notes/voice.

## Knowledge checkpoints
By end of level 0:
- variables, strings, input/output, loops, files.

By end of level 1:
- conditionals, dictionaries, validation, parsing.

By end of level 2:
- transforms, retries, small pipeline reasoning.

## Exit gate (must pass before level 3)
1. You can explain any line in one level-2 `project.py`.
2. You can add one new test and keep all tests green.
3. You can induce one failure and recover in under 20 minutes.
4. You can explain why your fix is correct.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Python Tutor](https://pythontutor.com/)
- [Exercism Python](https://exercism.org/tracks/python)

## Next

[Next: 29_LEVEL_3_TO_5_DEEP_GUIDE.md →](./29_LEVEL_3_TO_5_DEEP_GUIDE.md)
