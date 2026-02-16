#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail=0
project_count=0

echo "checking project python comment/docstring contract..."

for project_file in "$ROOT_DIR"/projects/level-*/[0-9][0-9]-*/project.py; do
  [[ -f "$project_file" ]] || continue
  ((project_count+=1))

  # Must start with a module docstring (first non-empty line is triple-quote).
  first_non_empty="$(awk 'NF {print; exit}' "$project_file")"
  if [[ "$first_non_empty" != '"""'* ]]; then
    echo "missing module docstring at top: ${project_file#$ROOT_DIR/}"
    fail=1
  fi

  comment_lines="$(awk '/^\s*#/ {n++} END{print n+0}' "$project_file")"
  if [[ "$comment_lines" -lt 3 ]]; then
    echo "too few comment lines in ${project_file#$ROOT_DIR/}: $comment_lines (min 3)"
    fail=1
  fi

done

if [[ "$project_count" -ne 165 ]]; then
  echo "unexpected project.py count: expected 165, found $project_count"
  fail=1
fi

test_count=0
for test_file in "$ROOT_DIR"/projects/level-*/[0-9][0-9]-*/tests/test_project.py; do
  [[ -f "$test_file" ]] || continue
  ((test_count+=1))

  first_non_empty="$(awk 'NF {print; exit}' "$test_file")"
  if [[ "$first_non_empty" != '"""'* ]]; then
    echo "missing test module docstring at top: ${test_file#$ROOT_DIR/}"
    fail=1
  fi

  comment_lines="$(awk '/^\s*#/ {n++} END{print n+0}' "$test_file")"
  if [[ "$comment_lines" -lt 2 ]]; then
    echo "too few comment lines in ${test_file#$ROOT_DIR/}: $comment_lines (min 2)"
    fail=1
  fi
done

if [[ "$test_count" -ne 165 ]]; then
  echo "unexpected test_project.py count: expected 165, found $test_count"
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "project python comment/docstring contract check failed"
  exit 1
fi

echo "project python comment/docstring contract verified"
