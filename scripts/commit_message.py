#!/usr/bin/env python3
"""Describe the staged changes in one line.

Used by scripts/push.* when no message is given. A generated line that says
what changed beats "update" - which is what a six-person group produces at
5pm on the fourth day otherwise.

    Update src/evermind/tools.py
    Update 4 files in src/evermind
    Add 2 files, update 3 in app
    Update 7 files across app, scripts, src

Prints exactly one line to stdout. Never fails: if git says something
unexpected, falls back to a plain description rather than blocking a push.
"""

import subprocess
import sys

MAX_DIRS = 3


def staged():
    """[(status, path)] for the staged tree. R and C carry a second path."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        capture_output=True, text=True, check=True,
    ).stdout
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0][0]
        path = parts[-1]  # for R/C this is the destination, which is what we want
        rows.append((status, path))
    return rows


def directory(path):
    return path.rsplit("/", 1)[0] if "/" in path else "(root)"


def top_level(path):
    return path.split("/", 1)[0] if "/" in path else "(root)"


def describe(rows):
    if not rows:
        return "Update files"

    added = [p for s, p in rows if s == "A"]
    deleted = [p for s, p in rows if s == "D"]
    changed = [p for s, p in rows if s not in ("A", "D")]

    # One file: name it. Most informative line we can produce.
    if len(rows) == 1:
        status, path = rows[0]
        verb = {"A": "Add", "D": "Delete", "R": "Rename"}.get(status, "Update")
        return "%s %s" % (verb, path)

    dirs = sorted({directory(p) for _, p in rows})
    tops = sorted({top_level(p) for _, p in rows})

    # Adds or deletes are worth calling out - they change the shape of the
    # tree, and that is what someone scanning the log is looking for.
    clauses = []
    if added:
        clauses.append("add %d file%s" % (len(added), "" if len(added) == 1 else "s"))
    if deleted:
        clauses.append("delete %d file%s" % (len(deleted), "" if len(deleted) == 1 else "s"))
    if changed:
        clauses.append("update %d file%s" % (len(changed), "" if len(changed) == 1 else "s"))

    if len(dirs) == 1:
        where = "in %s" % dirs[0]
    elif len(tops) <= MAX_DIRS:
        where = "across %s" % ", ".join(tops)
    else:
        where = "across %d directories" % len(tops)

    head = clauses[0][0].upper() + clauses[0][1:]
    rest = (", " + ", ".join(clauses[1:])) if len(clauses) > 1 else ""
    return "%s%s %s" % (head, rest, where)


def main():
    try:
        print(describe(staged()))
    except Exception:
        # A push must not fail because the message generator was surprised.
        print("Update files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
