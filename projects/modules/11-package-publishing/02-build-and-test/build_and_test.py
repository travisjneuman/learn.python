"""
Build and Test — Automates the package build-and-test workflow.

This script walks you through building a Python package and testing it.
Run it to see each step of the process with explanations.

NOTE: This script assumes you have already completed project 01
and have the mymath package in ../01-package-structure/
"""

import os
import subprocess
import sys


PACKAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "01-package-structure")


def run_command(description, command, cwd=None):
    """Run a shell command and print its output."""
    print(f"\n{'=' * 60}")
    print(f"STEP: {description}")
    print(f"COMMAND: {' '.join(command)}")
    print(f"{'=' * 60}\n")

    result = subprocess.run(
        command,
        cwd=cwd or PACKAGE_DIR,
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        # Build tools often write to stderr even for non-errors.
        print(result.stderr)

    if result.returncode != 0:
        print(f"[WARNING] Command exited with code {result.returncode}")
    else:
        print("[OK] Command succeeded")

    return result.returncode == 0


def main():
    print("Package Build & Test Workflow")
    print("=" * 60)
    print(f"Package directory: {os.path.abspath(PACKAGE_DIR)}")
    print()

    # Step 1: Build the package.
    # This creates a wheel (.whl) and source distribution (.tar.gz)
    # in the dist/ directory.
    run_command(
        "Build the package (creates wheel + sdist)",
        [sys.executable, "-m", "build"],
    )

    # Step 2: List the built files.
    dist_dir = os.path.join(PACKAGE_DIR, "dist")
    if os.path.exists(dist_dir):
        print(f"\n{'=' * 60}")
        print("BUILT FILES:")
        print(f"{'=' * 60}\n")
        for filename in os.listdir(dist_dir):
            filepath = os.path.join(dist_dir, filename)
            size_kb = os.path.getsize(filepath) / 1024
            print(f"  {filename} ({size_kb:.1f} KB)")

    # Step 3: Install in editable mode.
    # Editable mode means changes to source files are reflected
    # immediately without reinstalling.
    run_command(
        "Install package in editable mode (pip install -e .)",
        [sys.executable, "-m", "pip", "install", "-e", "."],
    )

    # Step 4: Run the tests.
    run_command(
        "Run tests against the installed package",
        [sys.executable, "-m", "pytest", "tests/", "-v"],
    )

    # Step 5: Verify the package can be imported.
    run_command(
        "Verify the package works",
        [sys.executable, "-c", "from mymath import add, mean; print(f'add(10, 20) = {add(10, 20)}'); print(f'mean([1,2,3]) = {mean([1,2,3])}')"],
    )

    print(f"\n{'=' * 60}")
    print("BUILD AND TEST COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
