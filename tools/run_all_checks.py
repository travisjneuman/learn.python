"""
Python CI check runner — runs all curriculum contract checks.

Python replacement for run_all_curriculum_checks.sh. Works on Windows
without bash or ripgrep.

Usage:
    python tools/run_all_checks.py
    python tools/run_all_checks.py --verbose
"""

import importlib.util
import sys
import time
from pathlib import Path

TOOLS_DIR = Path(__file__).parent

CHECKS = [
    ("markdown links", "check_markdown_links.py"),
    ("root doc contract", "check_root_docs.py"),
    ("project README contract", "check_project_contract.py"),
    ("portable paths", "check_portable_paths.py"),
]


def load_and_run(script_path: Path) -> bool:
    """Import a check script and run its main check function."""
    spec = importlib.util.spec_from_file_location("check_module", script_path)
    if spec is None or spec.loader is None:
        print(f"  could not load {script_path.name}")
        return False

    module = importlib.util.module_from_spec(spec)

    # Capture exit calls
    original_exit = sys.exit

    exit_code = 0

    def mock_exit(code=0):
        nonlocal exit_code
        exit_code = code if isinstance(code, int) else 1

    sys.exit = mock_exit
    try:
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()
    except SystemExit as e:
        exit_code = e.code if isinstance(e.code, int) else 1
    finally:
        sys.exit = original_exit

    return exit_code == 0


def main() -> None:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    passed = 0
    failed = 0
    total = len(CHECKS)

    print(f"\nRunning {total} curriculum checks...\n")

    for i, (name, script_name) in enumerate(CHECKS, 1):
        script_path = TOOLS_DIR / script_name
        if not script_path.exists():
            print(f"[{i}/{total}] {name} — SKIP (script not found)")
            continue

        print(f"[{i}/{total}] {name}")
        start = time.time()
        success = load_and_run(script_path)
        elapsed = time.time() - start

        if success:
            passed += 1
            if verbose:
                print(f"  PASS ({elapsed:.1f}s)")
        else:
            failed += 1
            print(f"  FAIL ({elapsed:.1f}s)")

        print()

    # Summary
    print("=" * 50)
    if failed == 0:
        print(f"All {passed} checks passed")
    else:
        print(f"{failed} of {total} checks failed")
    print("=" * 50)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
