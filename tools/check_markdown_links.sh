#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

missing=0
while IFS=: read -r file line match; do
  target=$(printf '%s' "$match" | sed -E 's/^\]\(\.\///; s/\)$//')
  dir=$(dirname "$file")
  if [[ ! -f "$dir/$target" ]]; then
    echo "missing link target: $file:$line -> ./$target"
    missing=1
  fi
done < <(rg -n -o --glob '*.md' --glob '!PythonBootcamp/**' '\]\(\./[^)]+\.md\)' "$ROOT_DIR")

if [[ "$missing" -ne 0 ]]; then
  echo "markdown link check failed"
  exit 1
fi

echo "markdown relative links verified"
