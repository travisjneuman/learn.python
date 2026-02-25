"""
Publish Guide — Interactive walkthrough for publishing to TestPyPI.

This script does NOT actually publish anything. It walks you through
each step, checks if prerequisites are met, and gives you the exact
commands to run.

Run this script and follow the instructions.
"""

import os
import shutil
import subprocess
import sys


PACKAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "01-package-structure")


def check_tool(name):
    """Check if a command-line tool is available."""
    return shutil.which(name) is not None


def check_dist():
    """Check if built distribution files exist."""
    dist_dir = os.path.join(PACKAGE_DIR, "dist")
    if not os.path.exists(dist_dir):
        return []
    return os.listdir(dist_dir)


def main():
    print("=" * 60)
    print("  Publishing to TestPyPI — Interactive Guide")
    print("=" * 60)
    print()

    # ── Step 1: Check prerequisites ──────────────────────────
    print("STEP 1: Checking prerequisites...\n")

    # Check for build tool.
    try:
        subprocess.run(
            [sys.executable, "-m", "build", "--version"],
            capture_output=True,
            check=True,
        )
        print("  [OK] python -m build is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  [MISSING] python -m build")
        print("  Install it: pip install build")
        print()

    # Check for twine.
    if check_tool("twine"):
        print("  [OK] twine is available")
    else:
        print("  [MISSING] twine")
        print("  Install it: pip install twine")

    print()

    # ── Step 2: Check for built files ────────────────────────
    print("STEP 2: Checking for built package...\n")

    dist_files = check_dist()
    if dist_files:
        print("  [OK] Found built files:")
        for f in dist_files:
            print(f"    - {f}")
    else:
        print("  [NOT FOUND] No built files in dist/")
        print("  Build first:")
        print(f"    cd {os.path.abspath(PACKAGE_DIR)}")
        print("    python -m build")

    print()

    # ── Step 3: TestPyPI account ─────────────────────────────
    print("STEP 3: TestPyPI account\n")
    print("  If you haven't already:")
    print("  1. Go to https://test.pypi.org/account/register/")
    print("  2. Create a free account")
    print("  3. Go to https://test.pypi.org/manage/account/token/")
    print("  4. Create an API token (scope: Entire account)")
    print("  5. Save the token somewhere safe (starts with 'pypi-')")
    print()

    # ── Step 4: Upload command ───────────────────────────────
    print("STEP 4: Upload to TestPyPI\n")
    print("  Run this command:")
    print(f"    cd {os.path.abspath(PACKAGE_DIR)}")
    print("    twine upload --repository testpypi dist/*")
    print()
    print("  When prompted:")
    print("    Username: __token__")
    print("    Password: <paste your API token>")
    print()

    # ── Step 5: Install from TestPyPI ────────────────────────
    print("STEP 5: Verify the upload\n")
    print("  Install your package from TestPyPI:")
    print("    pip install --index-url https://test.pypi.org/simple/ mymath-demo")
    print()
    print("  Test it:")
    print('    python -c "from mymath import add; print(add(1, 2))"')
    print()

    # ── Step 6: Version bump ─────────────────────────────────
    print("STEP 6: Publishing updates\n")
    print("  To publish a new version:")
    print("  1. Edit pyproject.toml — change version (e.g., 0.1.0 → 0.1.1)")
    print("  2. Delete old builds: rm -rf dist/")
    print("  3. Rebuild: python -m build")
    print("  4. Upload: twine upload --repository testpypi dist/*")
    print()

    print("=" * 60)
    print("  Guide complete! Follow the steps above to publish.")
    print("=" * 60)


if __name__ == "__main__":
    main()
