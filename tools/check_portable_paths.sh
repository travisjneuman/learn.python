#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Keep docs portable: avoid user-specific absolute home paths.
if rg -n --glob '*.md' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR" >/dev/null; then
  echo "non-portable absolute user path found in markdown docs"
  rg -n --glob '*.md' --glob '!PythonBootcamp/**' '/Users/|[A-Za-z]:\\Users\\' "$ROOT_DIR"
  exit 1
fi

echo "portable path contract verified"
