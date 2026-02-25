#!/usr/bin/env bash
set -euo pipefail

command -v rg >/dev/null 2>&1 || { echo "ripgrep (rg) not found. Install: https://github.com/BurntSushi/ripgrep#installation" >&2; exit 1; }

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECTS_DIR="$ROOT_DIR/projects"

fail=0

projects_index="$PROJECTS_DIR/README.md"
if [[ ! -f "$projects_index" ]]; then
  echo "missing projects index: projects/README.md"
  exit 1
fi

if [[ "$(sed -n '2p' "$projects_index")" != "Home: [README](../README.md)" ]]; then
  echo "bad projects index home link"
  fail=1
fi

for level in 0 1 2 3 4 5 6 7 8 9 10; do
  if ! rg -F -- "- [level-$level](./level-$level/README.md)" "$projects_index" >/dev/null; then
    echo "missing level link in projects index: level-$level"
    fail=1
  fi
done

for level in 0 1 2 3 4 5 6 7 8 9 10; do
  level_readme="$PROJECTS_DIR/level-$level/README.md"
  if [[ ! -f "$level_readme" ]]; then
    echo "missing level readme: projects/level-$level/README.md"
    fail=1
    continue
  fi

  if [[ "$(sed -n '2p' "$level_readme")" != "Home: [README](../../README.md)" ]]; then
    echo "bad home line: projects/level-$level/README.md"
    fail=1
  fi

  project_link_count="$(rg -n '^- \[[0-9][0-9]-[^]]+\]\(\./[0-9][0-9]-[^)]+/README\.md\) - ' "$level_readme" | wc -l | tr -d ' ')"
  if [[ "$project_link_count" -ne 15 ]]; then
    echo "bad project link count in projects/level-$level/README.md: expected 15, got $project_link_count"
    fail=1
  fi

  # Validate each linked project README exists.
  while IFS= read -r rel; do
    target="$PROJECTS_DIR/level-$level/$rel"
    if [[ ! -f "$target" ]]; then
      echo "missing linked project README in level-$level index: $rel"
      fail=1
    fi
  done < <(rg -o '^- \[[0-9][0-9]-[^]]+\]\(\./([0-9][0-9]-[^)]+/README\.md)\)' -r '$1' "$level_readme")

  if ! rg -n '^## Next$' "$level_readme" >/dev/null; then
    echo "missing ## Next in projects/level-$level/README.md"
    fail=1
  fi

  if [[ "$level" -lt 10 ]]; then
    next_level=$((level + 1))
    if ! rg -F -- "- Continue to [level-$next_level](../level-$next_level/README.md)." "$level_readme" >/dev/null; then
      echo "missing continue link in projects/level-$level/README.md"
      fail=1
    fi
  fi

  if ! rg -F -- "- Return to [projects index](../README.md)." "$level_readme" >/dev/null; then
    echo "missing return link in projects/level-$level/README.md"
    fail=1
  fi
done

if [[ "$fail" -ne 0 ]]; then
  echo "level index contract check failed"
  exit 1
fi

echo "level index contract verified"
