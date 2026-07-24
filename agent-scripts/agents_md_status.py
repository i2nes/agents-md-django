#!/usr/bin/env python3
"""Enforce the AGENTS.md-everywhere rule.

Default mode — every directory in the repo must contain an AGENTS.md, except
the fixed exclusion list below (machine-generated or vendored directories).
Missing files are FAILs. This list is the single source of truth for the rule.

--for mode — given changed file paths, list every AGENTS.md on the path from
the repo root down to each file. This is the end-of-task review list: read each
one and update it if the directory's purpose or conventions changed.

The repo root is the nearest ancestor of the start directory containing .git
(or the start directory itself if none); nothing outside it is ever considered.

Usage:
    agents_md_status.py [repo_root]
    agents_md_status.py --for file1 [file2 ...]

Exit codes: 0 = clean, 1 = missing AGENTS.md (default mode only).
"""
import sys
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".venv", "__pycache__", "migrations", "node_modules",
    "staticfiles", "vendor", "media", ".claude",
}


def find_repo_root(start):
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def required_dirs(root):
    yield root
    for path in sorted(root.rglob("*")):
        if path.is_dir() and not (EXCLUDED_DIRS & set(path.relative_to(root).parts)):
            yield path


def report_missing(root):
    missing = [d for d in required_dirs(root) if not (d / "AGENTS.md").is_file()]
    for directory in missing:
        print(f"FAIL  {directory}: no AGENTS.md — every non-excluded directory "
              f"must have one")
    if not missing:
        print("agents_md_status: every directory has an AGENTS.md")
    return 1 if missing else 0


def report_for(files):
    root = find_repo_root(Path.cwd())
    seen = []
    for raw in files:
        path = Path(raw).resolve()
        if root not in path.parents and path != root:
            print(f"NOTE  {raw}: outside repo root {root}, skipped")
            continue
        chain = [d for d in reversed(path.parents) if d == root or root in d.parents]
        if path.is_dir():
            chain.append(path)
        for directory in chain:
            candidate = directory / "AGENTS.md"
            if candidate.is_file() and candidate not in seen:
                seen.append(candidate)
    if seen:
        print("AGENTS.md files to review for the changed paths:")
        for candidate in seen:
            print(f"  {candidate.relative_to(root)}")
    else:
        print("No AGENTS.md found on the path of the given files.")
    return 0


def main(argv):
    if argv and argv[0] == "--for":
        return report_for(argv[1:])
    return report_missing(find_repo_root(Path(argv[0]) if argv else Path.cwd()))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
