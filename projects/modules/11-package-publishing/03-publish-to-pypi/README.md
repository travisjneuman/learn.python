# Module 11 / Project 03 — Publish to PyPI

Home: [README](../../../../README.md) · Module: [Package Publishing](../README.md)

## Focus

- TestPyPI vs real PyPI
- Creating a PyPI account and API token
- Uploading with `twine`
- Versioning strategy
- README rendering on PyPI

## Why this project exists

TestPyPI is a safe practice ground for package publishing. You can upload, install, and iterate without polluting the real Python Package Index. This project walks through the full publish workflow.

## Run

```bash
cd projects/modules/11-package-publishing/03-publish-to-pypi

# Follow the step-by-step guide below.
# The publish_guide.py script walks you through each step interactively.
python publish_guide.py
```

## Step-by-step publishing guide

### 1. Create a TestPyPI account

Go to https://test.pypi.org/account/register/ and create a free account.

### 2. Create an API token

Go to https://test.pypi.org/manage/account/token/ and create a token with scope "Entire account" (for your first upload).

### 3. Build your package

```bash
cd ../01-package-structure
python -m build
```

### 4. Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: paste your API token (starts with `pypi-`)

### 5. Verify it works

```bash
pip install --index-url https://test.pypi.org/simple/ mymath-demo
python -c "from mymath import add; print(add(1, 2))"
```

### 6. Iterate

To upload a new version:
1. Change `version` in `pyproject.toml` (e.g., 0.1.0 → 0.1.1)
2. Delete old builds: `rm -rf dist/`
3. Rebuild: `python -m build`
4. Upload: `twine upload --repository testpypi dist/*`

## Expected output

```text
Uploading mymath_demo-0.1.0-py3-none-any.whl
Uploading mymath_demo-0.1.0.tar.gz

View at:
https://test.pypi.org/project/mymath-demo/0.1.0/
```

## Alter it

1. Update the version to 0.2.0, add a new function, rebuild, and upload again.
2. Add a longer description in pyproject.toml and verify it renders on TestPyPI.
3. Try using a `.pypirc` config file instead of typing credentials each time.

## Break it

1. Try to upload the same version twice. What error do you get?
2. Upload a package with a broken README (invalid markdown). Check the rendering.
3. Try to install from TestPyPI when the package has dependencies not on TestPyPI.

## Fix it

1. Bump the version number and re-upload.
2. Fix the README and upload a new version.
3. Use `--extra-index-url https://pypi.org/simple/` to fall back to real PyPI for dependencies.

## Explain it

1. Why does TestPyPI exist separately from real PyPI?
2. What is the difference between `twine upload` and `pip upload`?
3. Why should you use API tokens instead of your username/password?
4. What is semantic versioning and why does it matter for published packages?

## Mastery check

You can move on when you can:
- publish a package to TestPyPI,
- install your published package in a fresh environment,
- bump the version and publish an update,
- explain the full publish workflow.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Go back to [Module index](../README.md) or continue to [Module 12 — Cloud Deployment](../../12-cloud-deploy/).
