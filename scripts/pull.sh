#!/usr/bin/env bash
# Pull the latest, keeping history readable and uncommitted work safe.
#
#   ./scripts/pull.sh
#
# --rebase replays your commits on top of the remote instead of creating a
# merge bubble - with six people on one branch, merge-pull turns the log into
# something nobody reads. --autostash shelves uncommitted work first and
# restores it after, so a dirty tree is not a reason to refuse.

set -euo pipefail

# Pause before the window closes (e.g. double-clicked rather than run from
# an already-open terminal) so the output stays readable. Fires on every
# exit path, success or failure.
trap 'sleep 8' EXIT

cd "$(dirname "$0")/.."

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if ! git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
    echo "Branch '$BRANCH' has no upstream - nothing to pull from."
    echo "Push it first:  ./scripts/push.sh"
    exit 0
fi

if ! git pull --rebase --autostash; then
    echo >&2
    echo "Rebase stopped - the same lines changed on both sides." >&2
    echo >&2
    echo "  Fix the marked files, then:  git add <file> && git rebase --continue" >&2
    echo "  Or back out entirely:        git rebase --abort" >&2
    echo >&2
    echo "Your uncommitted work is in the stash either way: git stash list" >&2
    exit 1
fi

echo "Up to date with origin/$BRANCH."
