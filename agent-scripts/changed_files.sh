#!/usr/bin/env bash
# List files added, modified, deleted, or untracked in the working tree,
# and optionally the diff against a base ref.
#
# Usage:
#   changed_files.sh              # working tree status (staged + unstaged + untracked)
#   changed_files.sh <base-ref>   # also: name-status diff of base-ref...HEAD
#   changed_files.sh --names      # bare file names only (pipe into other checks)
#
# Example end-of-task combo:
#   agents_md_status.py --for $(changed_files.sh --names)
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "changed_files: not inside a git repository" >&2
    exit 1
fi

if [[ "${1:-}" == "--names" ]]; then
    { git diff --name-only HEAD 2>/dev/null || git diff --name-only --cached
      git ls-files --others --exclude-standard
    } | sort -u
    exit 0
fi

echo "== Working tree (A=added M=modified D=deleted R=renamed ?=untracked) =="
git status --porcelain

if [[ -n "${1:-}" ]]; then
    echo
    echo "== Diff ${1}...HEAD =="
    git diff --name-status "${1}...HEAD"
fi
