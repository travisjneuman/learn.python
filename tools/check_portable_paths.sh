#!/usr/bin/env bash
set -euo pipefail

command -v rg >/dev/null 2>&1 || { echo "ripgrep (rg) not found. Install: https://github.com/BurntSushi/ripgrep#installation" >&2; exit 1; }

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Keep docs portable: avoid user-specific absolute home paths.
fail=0

if rg -n --glob '*.md' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR" >/dev/null; then
  echo "non-portable absolute user path found in markdown docs"
  rg -n --glob '*.md' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR"
  fail=1
fi

if rg -n --glob '*.py' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR" >/dev/null; then
  echo "non-portable absolute user path found in Python files"
  rg -n --glob '*.py' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR"
  fail=1
fi

if [[ "$fail" -eq 1 ]]; then
  exit 1
fi

echo "portable path contract verified"
