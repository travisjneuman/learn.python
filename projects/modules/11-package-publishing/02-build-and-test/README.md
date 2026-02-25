# Module 11 / Project 02 — Build and Test

Home: [README](../../../../README.md) · Module: [Package Publishing](../README.md)

## Focus

- Building a wheel and sdist with `python -m build`
- Installing your package locally with `pip install -e .`
- Testing the installed package
- Understanding dist/ contents

## Why this project exists

Before publishing a package, you need to build it and verify it works when installed. This project walks through the build process and explains what the output files are.

## Run

```bash
cd projects/modules/11-package-publishing/02-build-and-test

# Step 1: Build the package from project 01
cd ../01-package-structure
python -m build

# Step 2: Look at what was built
ls dist/

# Step 3: Install locally in editable mode
pip install -e .

# Step 4: Test the installed package
pytest tests/ -v

# Step 5: Use it from anywhere
python -c "from mymath import add; print(add(10, 20))"
```

## Expected output

```text
# After build:
dist/
  mymath_demo-0.1.0-py3-none-any.whl
  mymath_demo-0.1.0.tar.gz

# After pytest:
tests/test_calculator.py::test_add PASSED
tests/test_calculator.py::test_subtract PASSED
...
6 passed

# After import:
30
```

## Project files

This project is a guide — the code lives in project 01. The script below automates the build-and-test workflow.

## Alter it

1. Modify a function in project 01, rebuild, and verify the change shows up when imported.
2. Build without `--wheel` to get only an sdist. Compare the file sizes.
3. Install the wheel directly with `pip install dist/mymath_demo-0.1.0-py3-none-any.whl` instead of editable mode.

## Break it

1. Delete `pyproject.toml` and try to build. What error do you get?
2. Install in non-editable mode (`pip install .`) and then change a function. Does the change show up? Why not?
3. Try to import `mymath` without installing it (from a different directory).

## Fix it

1. Restore `pyproject.toml` and rebuild.
2. Reinstall with `-e` flag for editable mode, which picks up changes automatically.
3. Add the `src` directory to `PYTHONPATH` as a temporary workaround.

## Explain it

1. What is the difference between a wheel (.whl) and an sdist (.tar.gz)?
2. What does "editable mode" (`pip install -e .`) do differently from a normal install?
3. Why does `python -m build` create both a wheel and an sdist?
4. What is inside a wheel file? (Hint: it's a zip file — try renaming to .zip and opening it.)

## Mastery check

You can move on when you can:
- build a package from pyproject.toml,
- install it locally in editable mode,
- run tests against the installed package,
- explain wheel vs sdist.

---

## Related Concepts

- [How Imports Work](../../../../concepts/how-imports-work.md)
- [Virtual Environments](../../../../concepts/virtual-environments.md)
- [Quiz: How Imports Work](../../../../concepts/quizzes/how-imports-work-quiz.py)

## Next

[Project 03 — Publish to PyPI](../03-publish-to-pypi/)
