# Module 09 / Project 04 — CI with GitHub Actions

Home: [README](../../../../README.md)

## Focus

Creating a GitHub Actions workflow that lints, tests, and builds a Docker image on every push.

## Why this project exists

Continuous Integration (CI) catches bugs before they reach production. Instead of relying on developers to remember to run tests, a CI pipeline runs them automatically on every push. If linting fails, tests fail, or the Docker build breaks, GitHub marks the commit with a red X. This project teaches you to write a GitHub Actions workflow from scratch.

## Run

### Run the app and tests locally first

```bash
cd projects/modules/09-docker-deployment/04-ci-github-actions

# Run the app
python app.py

# In another terminal, run tests
pytest tests/ -v

# Run the linter
ruff check .
```

### Trigger the CI pipeline

The GitHub Actions workflow runs automatically when you push this code to a GitHub repository:

1. Create a repository on GitHub (or use an existing one).
2. Push this project's code to the repository.
3. Go to the "Actions" tab on GitHub to see the pipeline run.

The pipeline runs three jobs in sequence:

```
lint  -->  test  -->  build
```

If any job fails, the remaining jobs are skipped.

### View results on GitHub

1. Go to your repository on GitHub.
2. Click the **Actions** tab.
3. Click on the latest workflow run to see each job's output.
4. Green checkmarks mean success. Red X marks mean failure.

## Expected output

### Local test output

```
tests/test_app.py::test_read_root PASSED
tests/test_app.py::test_health_check PASSED
tests/test_app.py::test_add PASSED
tests/test_app.py::test_add_invalid_input PASSED
tests/test_app.py::test_greet PASSED
tests/test_app.py::test_greet_uppercase PASSED
```

### GitHub Actions

The Actions tab shows three jobs: "lint", "test", and "build", each with a green checkmark.

## Alter it

1. Add a new `GET /multiply/{a}/{b}` endpoint and a corresponding test. Push and verify the CI passes.
2. Add a step to the "test" job that prints the Python version: `run: python --version`.
3. Change the workflow to only run on pushes to the `main` branch (modify the `on.push.branches` field).

## Break it

1. Introduce a deliberate ruff lint error: add an unused import (`import os`) to `app.py`. Push and watch the lint job fail.
2. Change the expected value in `test_add` so the assertion fails. Push and watch the test job fail. Does the build job still run?
3. Add an invalid instruction to the Dockerfile (e.g., `RUN nonexistent_command`). Push and watch the build job fail.

## Fix it

1. Remove the unused import. The lint job should pass again.
2. Restore the correct assertion. The test job should pass.
3. Remove the invalid Dockerfile instruction. The build job should pass.

## Explain it

1. What triggers the CI workflow? Where is this configured?
2. What does `needs: lint` do in the test job? What happens if you remove it?
3. Why does the workflow install Python with `actions/setup-python` instead of using the pre-installed version?
4. Why does the build job only build the Docker image without pushing it to a registry?

## Mastery check

You can move on when you can:

- write a basic GitHub Actions workflow from scratch,
- explain the relationship between jobs, steps, and actions,
- describe what `needs` does and how it controls execution order,
- interpret the Actions tab on GitHub to diagnose a failed pipeline.

---

## Related Concepts

- [The Terminal Deeper](../../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Virtual Environments](../../../../concepts/virtual-environments.md)
- [Quiz: The Terminal Deeper](../../../../concepts/quizzes/the-terminal-deeper-quiz.py)

## Next

Continue to [05-production-config](../05-production-config/).
