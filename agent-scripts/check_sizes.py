#!/usr/bin/env python3
"""Check file sizes and line lengths against the thresholds in the root AGENTS.md.

Usage:
    check_sizes.py [paths...]    # default: scan the whole repo

Exit codes: 0 = clean, 1 = at least one hard violation (file past its split threshold).
Warnings (file past warn threshold, or long lines) never fail the run on their own.
"""
import sys
from pathlib import Path

# suffix: (warn_lines, split_lines, max_line_length or None)
THRESHOLDS = {
    ".py": (300, 500, 100),
    ".js": (200, 400, 100),
    ".css": (400, 600, 100),
    ".html": (150, 300, None),
    ".md": (200, 400, None),
}

EXCLUDED_DIRS = {
    ".git", ".venv", "__pycache__", "migrations", "node_modules",
    "staticfiles", "vendor", "media", ".mypy_cache", ".pytest_cache",
}


def iter_files(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_file():
            yield path
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and not (EXCLUDED_DIRS & set(child.parts)):
                    yield child


def check(path):
    """Return (warnings, violations) message lists for one file."""
    rule = THRESHOLDS.get(path.suffix)
    if rule is None:
        return [], []
    warn_at, split_at, max_len = rule
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"{path}: unreadable ({exc})"], []

    warnings, violations = [], []
    if len(lines) >= split_at:
        violations.append(f"{path}: {len(lines)} lines — past split threshold "
                          f"({split_at}); split into a package of smaller files")
    elif len(lines) >= warn_at:
        warnings.append(f"{path}: {len(lines)} lines — approaching split "
                        f"threshold (warn {warn_at}, split {split_at})")

    if max_len is not None:
        long = [i + 1 for i, line in enumerate(lines) if len(line) > max_len]
        if long:
            shown = ", ".join(map(str, long[:5])) + (", …" if len(long) > 5 else "")
            warnings.append(f"{path}: {len(long)} line(s) over {max_len} chars "
                            f"(lines {shown})")
    return warnings, violations


def main(argv):
    targets = argv or ["."]
    all_warnings, all_violations = [], []
    for path in iter_files(targets):
        warnings, violations = check(path)
        all_warnings += warnings
        all_violations += violations

    for msg in all_warnings:
        print(f"WARN  {msg}")
    for msg in all_violations:
        print(f"FAIL  {msg}")
    if not all_warnings and not all_violations:
        print("check_sizes: clean")
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
