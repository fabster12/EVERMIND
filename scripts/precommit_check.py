#!/usr/bin/env python3
"""Refuse a commit that would publish a credential.

Run from scripts/push.sh and scripts/push.ps1 against the staged tree.
Exit 0 means safe to commit; exit 1 means stop, and the reason is printed.

The pattern list is the one already proven in tools/packaging/build_packages.py,
which scans the share zips for the same thing. Kept as a copy rather than an
import because this file has to run before any project dependency is
installed - a fresh clone must be able to push safely.

Each pattern is assembled from fragments rather than written out whole. If the
literals appeared here, this file would trip its own scan.
"""

import re
import subprocess
import sys

SECRET_PATTERNS = [
    (b"voc" + rb"-[0-9a-f]{20}", "Vocareum lab key"),
    (b"sk-" + b"svcacct", "OpenAI service account key"),
    (b"sk-" + b"ant-", "Anthropic API key"),
    (b"ghp" + rb"_[A-Za-z0-9]{36}", "GitHub personal access token"),
    (b"github" + rb"_pat_[A-Za-z0-9_]{20}", "GitHub fine-grained token"),
    (b"GITHUB_" + rb"TOKEN=\S", "populated GITHUB_TOKEN"),
    (b"AIza" + rb"[0-9A-Za-z_-]{35}", "Google API key"),
    (rb"-----BEGIN [A-Z ]*PRIVATE KEY", "private key"),
]

# Never commit these, whatever .gitignore says. Someone will eventually run
# `git add -f .env` to "just test something".
FORBIDDEN_PATHS = (".env",)

# A staged binary this large is not worth scanning; it is also not something
# anyone pastes a key into.
MAX_SCAN_BYTES = 4_000_000


def staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def staged_blob(path):
    """The staged content, not the working copy - they can differ."""
    r = subprocess.run(["git", "show", ":" + path], capture_output=True)
    return r.stdout if r.returncode == 0 else b""


def main():
    problems = []

    for path in staged_files():
        name = path.rsplit("/", 1)[-1]
        if name in FORBIDDEN_PATHS:
            problems.append("%s is staged - it holds real values, never commit it" % path)
            continue

        blob = staged_blob(path)
        if len(blob) > MAX_SCAN_BYTES:
            continue

        for pattern, label in SECRET_PATTERNS:
            m = re.search(pattern, blob)
            if m:
                line = blob[: m.start()].count(b"\n") + 1
                problems.append("%s:%d looks like a %s" % (path, line, label))

    if problems:
        sys.stderr.write("\nBlocked: staged changes look like they contain credentials.\n\n")
        for p in problems:
            sys.stderr.write("  - %s\n" % p)
        sys.stderr.write(
            "\nNothing was committed. Remove the value, put it in .env (gitignored),\n"
            "and reference it by name in .env.example.\n\n"
            "If this is a false positive - a fixture or documentation example -\n"
            "commit it with plain git:  git commit -m \"...\" && git push\n\n"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
