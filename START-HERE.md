<img src="docs/brand/evermind-icon.jpg" alt="" width="72" align="right">

# Start here

Setup, in order. If you have just cloned this repo, start at step 1 and
stop when something fails — do not skip ahead, the later steps assume the
earlier ones worked.

What EverMind *is*, and why, is in [`README.md`](README.md). This file is
only how to get it running.

---

## 1. Install `uv` — once per machine

`uv` is the package manager the course uses. It replaces `pip`, `venv` and
`pyenv` in one tool, and it is what makes everyone's install identical.

```powershell
# Windows
winget install --id astral-sh.uv -e
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then **open a new terminal** (the installer edits `PATH`) and check:

```
uv --version
```

---

## 2. Set up the project

### If `pyproject.toml` already exists — the normal case

```
uv sync
```

That is the whole setup. It reads `pyproject.toml`, creates `.venv/`, and
installs the exact versions recorded in `uv.lock`. Everyone gets the same
tree, which is the point of committing the lock.

Run everything through `uv run` afterwards, never a bare `python` — that
would use your system interpreter and miss the project's packages:

```
uv run python -c "import google.adk; print('ok')"
uv run pytest src/tests
```

### If `pyproject.toml` does NOT exist yet — first time only

**One person does this once, commits the result, and nobody repeats it.**
`uv sync` has nothing to read until it exists.

```
uv init --python 3.12
uv add "google-adk>=2.1.0,<3" pydantic
uv add --dev pytest
```

`uv add` writes to `pyproject.toml` and updates `uv.lock` in one step, so
no separate `uv sync` is needed after it.

Two things in that first command are deliberate:

- **`--python 3.12`** — the course labs run 3.12, and `uv` will fetch that
  interpreter for you whatever your system Python is. Newer releases are
  not worth the risk: ADK pulls a large dependency tree, and a resolver
  failure across six laptops on Tuesday morning is an expensive way to
  discover a package has not caught up yet.
- **`>=2.1.0,<3`** — the pin, and the reasoning, is in
  [`scratch/0002-pin-google-adk-2-1.md`](scratch/0002-pin-google-adk-2-1.md).
  Short version: on 2.0.0 the Dev UI Traces tab shows zero spans, and the
  tab is how we show tool calls in the demo.

Then commit both files:

```
./scripts/push.sh "Add pyproject.toml and uv.lock"
```

---

## 3. Credentials

```
cp .env.example .env      # Windows: copy .env.example .env
```

Fill in `GEMINI_API_KEY` with your Vocareum lab key (`voc-...`), from the
lab portal. `GOOGLE_GEMINI_BASE_URL` and `ADK_MODEL` are already set.

`.env` is gitignored and must stay that way. `.env.example` carries names
with no values. `scripts/push.sh` scans every staged file and refuses to
commit anything that looks like a key — but do not rely on it; the parent
repo already has live keys in its history, which is what that scan exists
to stop happening again.

Check it works:

```
uv run python -c "import os;from dotenv import load_dotenv;load_dotenv();print('key set:', bool(os.getenv('GEMINI_API_KEY')))"
```

---

## 4. Daily git

Use the helpers rather than raw git. They scan for credentials before
committing, and they generate a message from the diff when you do not give
one, so the log does not fill up with "update".

```bash
./scripts/pull.sh                      # rebase, autostash - run this first
./scripts/push.sh "what you changed"   # stage, commit, push
./scripts/push.sh                      # same, message generated
```

```powershell
.\scripts\pull.ps1
.\scripts\push.ps1 "what you changed"
```

**Pull before you start working.** Six people on one branch; a rebase on a
clean tree is painless, a rebase after a day of edits is not.

---

## 5. Running things

Nothing below exists yet — the agent is not written until the Phase 1 gate
is signed off on Monday 19 October. Listed so you know what is coming.

| What | Command |
| --- | --- |
| The pipeline | `uv run run_pipeline.py` |
| The ADK Dev UI | `uv run adk web` |
| The review app | `uv run uvicorn app.server:app --reload` |
| Unit tests | `uv run pytest src/tests` |
| Evals (needs a key) | `uv run pytest src/evals` |

What already works today, and needs only `python-docx` and `pillow`:

```
python tools/build_fixtures.py        # regenerates src/fixtures/*.json
python tools/build_diagram.py         # regenerates docs/architecture.png
```

---

## If something breaks

| Symptom | Cause | Fix |
| --- | --- | --- |
| `uv: command not found` | `PATH` not reloaded | Open a new terminal |
| `No pyproject.toml found` | Nobody has run step 2 yet | See "first time only" |
| `ModuleNotFoundError` on a package you know is installed | Ran bare `python` | Use `uv run python` |
| Dev UI Traces tab is empty | ADK 2.0.0 | `uv sync` — the pin is `>=2.1.0` |
| Push refused, "looks like a credential" | A real key is staged | Move it to `.env`, see step 3 |
| `rebase stopped` | Same lines changed both sides | Fix the marked files, `git rebase --continue` |

---

## Where things live

[`STRUCTURE.md`](STRUCTURE.md) is the annotated map, file by file. The
short version:

| | |
| --- | --- |
| `src/` | **the project** — agent, specs, contracts, fixtures, tests |
| `app/` | the review frontend (not built yet) |
| `docs/` | what people read: the gate documents, the diagram |
| `tools/` | generators for everything in `docs/` |
| `scripts/` | the git helpers from step 4 |
| `scratch/` | drafts and ADRs, committed but not authoritative |
| `notes/` | the brief, the roadmap, course material |
