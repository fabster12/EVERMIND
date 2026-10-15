# `scratch/` — working notes and staging

Scribbles, drafts, and decisions that are not yet where they belong.

Nothing here is authoritative. When a file in here settles, it moves:

| This kind of file | Ends up in |
| --- | --- |
| An ADR that has been agreed | `docs/decisions/NNNN-*.md` |
| Build planning | `src/openspec/changes/add-evermind-pipeline/tasks.md` |
| Behaviour we commit to | `src/openspec/changes/.../specs/` |
| A note nobody needs after the gate | deleted |

## This folder is committed, not ignored

Deliberate. A decision only your laptop can see is not a decision the group
made, and the instructor reads the reasoning as well as the result.

**So no credentials in here, ever.** Real values go in `.env`, which is
gitignored; the names go in `.env.example`. `scripts/push.sh` scans every
staged file and refuses to commit anything matching a key pattern, but the
scan is a backstop, not permission to paste a key and hope.

The parent repo (`fabster12/FDE`) has a `scribbles/` folder with live lab
keys committed in it. That is the thing this warning exists to prevent
happening twice.
