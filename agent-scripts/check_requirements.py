#!/usr/bin/env python3
"""Check that requirements.in and requirements.txt exist and are in sync.

In sync means: every package named in requirements.in appears (pinned) in
requirements.txt, and requirements.txt is not older than requirements.in.
Recompile with:  pip-compile requirements.in

Usage:
    check_requirements.py [repo_root]    # default: current directory

Exit codes: 0 = in sync, 1 = missing file or out of sync.
"""
import re
import sys
from pathlib import Path

RE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_names(path):
    names = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith(("-", "--")):
            continue
        match = RE_NAME.match(line)
        if match:
            names.add(normalize(match.group(0)))
    return names


def main(argv):
    root = Path(argv[0]) if argv else Path(".")
    req_in = root / "requirements.in"
    req_txt = root / "requirements.txt"

    problems = []
    if not req_in.is_file():
        problems.append(f"FAIL  {req_in} is missing — dependencies must be "
                        f"declared there")
    if not req_txt.is_file():
        problems.append(f"FAIL  {req_txt} is missing — run: pip-compile "
                        f"requirements.in")
    if problems:
        print("\n".join(problems))
        return 1

    missing = parse_names(req_in) - parse_names(req_txt)
    if missing:
        problems.append(f"FAIL  in requirements.in but not requirements.txt: "
                        f"{', '.join(sorted(missing))} — run pip-compile")
    if req_in.stat().st_mtime > req_txt.stat().st_mtime:
        problems.append("WARN  requirements.in is newer than requirements.txt — "
                        "recompile if you changed it")

    if problems:
        print("\n".join(problems))
        return 1 if any(p.startswith("FAIL") for p in problems) else 0
    print("check_requirements: in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
