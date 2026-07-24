#!/usr/bin/env python3
"""Check that HTML templates keep HTML, CSS, and JS in separate files.

Flags (FAIL): inline <script> bodies, <style> blocks.
Flags (WARN): style="..." attributes, on*="..." event handlers.
Allowed: <script src=...>, <script type="application/json"> (data islands,
e.g. Django's json_script), and all htmx hx-* attributes.

Usage:
    check_templates.py [paths...]    # default: scan the whole repo

Exit codes: 0 = clean, 1 = at least one FAIL.
"""
import re
import sys
from pathlib import Path

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "staticfiles", "vendor", "media"}

RE_SCRIPT_OPEN = re.compile(r"<script\b([^>]*)>", re.IGNORECASE)
RE_STYLE_BLOCK = re.compile(r"<style\b", re.IGNORECASE)
RE_STYLE_ATTR = re.compile(r"""\sstyle\s*=\s*["']""", re.IGNORECASE)
RE_ON_HANDLER = re.compile(r"""\son[a-z]+\s*=\s*["']""", re.IGNORECASE)


def script_is_allowed(attrs):
    return "src=" in attrs.lower() or "application/json" in attrs.lower()


def check(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    warnings, violations = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for match in RE_SCRIPT_OPEN.finditer(line):
            if not script_is_allowed(match.group(1)):
                violations.append(f"{path}:{i}: inline <script> — move JS to a "
                                  f"static .js file")
        if RE_STYLE_BLOCK.search(line):
            violations.append(f"{path}:{i}: <style> block — move CSS to a "
                              f"static .css file")
        if RE_STYLE_ATTR.search(line):
            warnings.append(f"{path}:{i}: style= attribute — use a class instead")
        if RE_ON_HANDLER.search(line):
            warnings.append(f"{path}:{i}: on*= handler — use addEventListener "
                            f"in a .js file (or htmx)")
    return warnings, violations


def iter_templates(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix == ".html":
            yield path
        elif path.is_dir():
            for child in sorted(path.rglob("*.html")):
                if not (EXCLUDED_DIRS & set(child.parts)):
                    yield child


def main(argv):
    all_warnings, all_violations = [], []
    for path in iter_templates(argv or ["."]):
        warnings, violations = check(path)
        all_warnings += warnings
        all_violations += violations

    for msg in all_warnings:
        print(f"WARN  {msg}")
    for msg in all_violations:
        print(f"FAIL  {msg}")
    if not all_warnings and not all_violations:
        print("check_templates: clean")
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
