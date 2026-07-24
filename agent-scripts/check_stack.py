#!/usr/bin/env python3
"""Check stack conformity: no npm artifacts, .venv present.

FAIL on any npm/Node artifact (package.json, lockfiles, node_modules) — the
stack is Django + Tailwind standalone CLI + htmx + vanilla JS, no npm ever.
WARN if .venv is missing at the repo root.

Usage:
    check_stack.py [repo_root]    # default: current directory

Exit codes: 0 = clean, 1 = npm artifact found.
"""
import sys
from pathlib import Path

NPM_ARTIFACTS = [
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "node_modules", ".npmrc",
]
EXCLUDED_DIRS = {".git", ".venv", "staticfiles", "media"}


def find_artifacts(root):
    found = []
    for name in NPM_ARTIFACTS:
        for path in root.rglob(name):
            if not (EXCLUDED_DIRS & set(path.relative_to(root).parts[:-1])):
                found.append(path)
    return found


def main(argv):
    root = Path(argv[0]) if argv else Path(".")
    failed = False

    for path in find_artifacts(root):
        print(f"FAIL  {path}: npm/Node artifact — the no-npm rule forbids this; "
              f"remove it or get an approved Exception first")
        failed = True

    if not (root / ".venv").is_dir():
        print("WARN  .venv missing at repo root — create it: python3 -m venv .venv")

    if not failed:
        print("check_stack: clean")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
