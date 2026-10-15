#!/usr/bin/env bash
# Stage everything, commit, push. Message optional.
#
#   ./scripts/push.sh "fix the citation validator"
#   ./scripts/push.sh                 <- message generated from the diff
#
# Refuses to commit anything that looks like a credential. See
# scripts/precommit_check.py for what it blocks and how to override.

set -euo pipefail

cd "$(dirname "$0")/.."

PY=$(command -v python3 || command -v python || true)
if [ -z "$PY" ]; then
    echo "python not found on PATH - needed for the credential scan." >&2
    exit 1
fi

git add -A

if git diff --cached --quiet; then
    echo "Nothing to commit. Working tree is clean."
    # Still push: a previous run may have committed without reaching the remote.
    if [ -n "$(git log '@{u}..HEAD' --oneline 2>/dev/null || echo unpushed)" ]; then
        echo "Local commits are ahead of the remote - pushing those."
    else
        exit 0
    fi
else
    "$PY" scripts/precommit_check.py || exit 1

    MSG="${1:-}"
    if [ -z "$MSG" ]; then
        MSG=$("$PY" scripts/commit_message.py)
        echo "No message given, using: $MSG"
    fi

    git commit -q -m "$MSG"
    echo "Committed: $MSG"
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
    git push
else
    echo "Branch '$BRANCH' has no upstream yet - setting it."
    git push -u origin HEAD
fi

echo "Pushed $BRANCH."
