# Contributing to learn.python

Thanks for your interest in improving this curriculum. Whether you are fixing a typo, reporting a broken test, or proposing a new project, your contribution helps every learner who comes after you.

## How to Report Issues

Use the [issue templates](https://github.com/travisjneuman/learn.python/issues/new/choose) to report:

- **Bug reports** — broken links, failing tests, code errors
- **Feature requests** — new projects, modules, or curriculum improvements
- **Curriculum feedback** — unclear explanations, typos, suggested rewrites

## Development Setup

After cloning or forking, install the pre-commit hooks so that linting and formatting run automatically on every commit:

```bash
pip install pre-commit
pre-commit install
```

This adds a Git hook that runs [ruff](https://docs.astral.sh/ruff/) (lint + format) before each commit. If ruff finds fixable issues it will apply the fixes automatically — just re-stage the changed files and commit again.

You can also run the hooks manually against all files at any time:

```bash
pre-commit run --all-files
```

## How to Submit a Pull Request

1. Fork the repository
2. Create a branch from `main` (`git checkout -b your-branch-name`)
3. Install pre-commit hooks (see **Development Setup** above)
4. Make your changes
5. Run tests if applicable (`python -m pytest`)
6. Open a pull request against `main`

Keep pull requests focused. One fix or one feature per PR is easier to review than a grab bag of changes.

## Code Style

This is an educational repository. Writing style matters as much as code style.

- **Plain language first.** Explain concepts the way you would to a friend who has never coded.
- **Hands-on before theory.** Show the code, then explain why it works.
- **No jargon without explanation.** If you use a technical term, define it on first use.
- **Python code** should pass `ruff check` and `ruff format --check`. (If you installed the pre-commit hooks, this happens automatically.)

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

## Contributor Recognition

Every accepted pull request earns you a spot in [CONTRIBUTORS.md](./CONTRIBUTORS.md). When your PR is merged, add your name to the contributors table (or we will add it for you).

Significant contributions — new projects, modules, or major curriculum improvements — are highlighted in the contributor notes.

## Translations

We welcome translations of the curriculum into other languages. Translation work is coordinated in the `translations/` directory. See `translations/TRANSLATING.md` (when available) for guidelines on translating documents, maintaining parity with the English source, and getting credit for your work.

If you want to start a translation for a new language, open an issue first so we can coordinate.

## Questions?

Open an issue. There are no silly questions in a learning repo.
