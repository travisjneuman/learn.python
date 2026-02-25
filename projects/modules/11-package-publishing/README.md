# Module 11 — Package Publishing

Home: [README](../../../README.md) · Modules: [Index](../README.md)

## Prerequisites

- Level 3 complete (you understand packages, `__init__.py`, project structure)

## What you will learn

- How to structure a Python package for distribution
- `pyproject.toml` configuration
- Building wheels and sdists
- Installing your own package locally
- Publishing to TestPyPI

## Why package publishing matters

Every library you install with `pip` was once someone's local project. Learning to package and publish your code means you can share tools with your team, contribute to open source, and distribute your own utilities. Even if you never publish publicly, understanding packaging helps you organize larger projects.

## Install dependencies

```bash
cd projects/modules/11-package-publishing
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Projects

| # | Project | Focus |
|---|---------|-------|
| 01 | [Package Structure](./01-package-structure/) | src layout, pyproject.toml, `__init__.py`, entry points |
| 02 | [Build and Test](./02-build-and-test/) | build wheel, install locally, test the installed package |
| 03 | [Publish to PyPI](./03-publish-to-pypi/) | TestPyPI workflow, versioning, README rendering |

## Related concepts

- [concepts/how-imports-work.md](../../../concepts/how-imports-work.md)
- [concepts/virtual-environments.md](../../../concepts/virtual-environments.md)
