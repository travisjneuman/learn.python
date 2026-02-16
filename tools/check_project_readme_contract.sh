#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

project_readmes=(
  "$ROOT_DIR"/projects/level-*/[0-9][0-9]-*/README.md
)

count=0
fail=0

required_headings=(
  "## Run (copy/paste)"
  "## Expected terminal output"
  "## Expected artifacts"
  "## Alter it (required)"
  "## Break it (required)"
  "## Fix it (required)"
  "## Explain it (teach-back)"
  "## Mastery check"
  "## Next"
)

for file in "${project_readmes[@]}"; do
  [[ -f "$file" ]] || continue
  ((count+=1))

  # Contract: home link line exists and is standardized.
  if ! sed -n '2p' "$file" | rg '^Home: \[README\]\(\.\./\.\./\.\./README\.md\)$' >/dev/null; then
    echo "bad home link: $file"
    fail=1
  fi

  # Contract: each required section exists.
  for heading in "${required_headings[@]}"; do
    if ! rg -F -n "$heading" "$file" >/dev/null; then
      echo "missing heading '$heading': $file"
      fail=1
    fi
  done

  # Contract: command-path placeholder note is present for portability.
  if ! rg -F -n "Use \`<repo-root>\` as the folder containing this repository's \`README.md\`." "$file" >/dev/null; then
    echo "missing <repo-root> note: $file"
    fail=1
  fi

  # Contract: Next section points back to level index.
  if ! rg -n '^Go back to \[Level [0-9]+ index\]\(\.\./README\.md\)\.$' "$file" >/dev/null; then
    echo "bad next link format: $file"
    fail=1
  fi

done

if [[ "$count" -ne 165 ]]; then
  echo "unexpected project README count: expected 165, found $count"
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "project README contract check failed"
  exit 1
fi

echo "project README contract verified (count=$count)"
