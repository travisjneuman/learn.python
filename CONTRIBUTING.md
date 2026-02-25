# Contributing to learn.python

Thanks for your interest in improving this curriculum. Whether you are fixing a typo, reporting a broken test, or proposing a new project, your contribution helps every learner who comes after you.

## How to Report Issues

Use the [issue templates](https://github.com/travisjneuman/learn.python/issues/new/choose) to report:

- **Bug reports** — broken links, failing tests, code errors
- **Feature requests** — new projects, modules, or curriculum improvements
- **Curriculum feedback** — unclear explanations, typos, suggested rewrites

## How to Submit a Pull Request

1. Fork the repository
2. Create a branch from `main` (`git checkout -b your-branch-name`)
3. Make your changes
4. Run tests if applicable (`python -m pytest`)
5. Open a pull request against `main`

Keep pull requests focused. One fix or one feature per PR is easier to review than a grab bag of changes.

## Code Style

This is an educational repository. Writing style matters as much as code style.

- **Plain language first.** Explain concepts the way you would to a friend who has never coded.
- **Hands-on before theory.** Show the code, then explain why it works.
- **No jargon without explanation.** If you use a technical term, define it on first use.
- **Python code** should pass `ruff check` and `black --check`.

## Project Structure Conventions

Follow the existing structure for the level you are contributing to:

**level-00 (Absolute Beginner)**
```
project-name/
  exercise.py
  TRY_THIS.md
```

**level-0 through level-10 and expansion modules**
```
project-name/
  README.md
  project.py
  tests/
  notes.md
```

## Testing Expectations

- Projects from Level 0 onward should include pytest tests in a `tests/` directory.
- Tests should verify actual behavior, not hard-code expected outputs.
- Run `python -m pytest tests/` from the project directory to confirm tests pass.

## Curriculum Consistency

- Follow the existing level sequence. Do not introduce concepts out of order.
- Match the format of neighboring documents and projects.
- Every document should have navigation links (Previous / Home / Next) at the bottom.
- New projects should include a README explaining what the learner builds and why.

## Questions?

Open an issue. There are no silly questions in a learning repo.
