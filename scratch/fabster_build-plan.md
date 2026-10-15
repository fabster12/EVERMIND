# Build plan — how we actually build EverMind

Working note, not authoritative. The authority is
`src/openspec/changes/add-evermind-pipeline/`: the proposal, the specs,
and `tasks.md`. This file is how to *drive* those, and what lands where.

---

## 1. Yes — the empty folders are the plan

All four have a `.gitkeep` and nothing else. That is deliberate: the shape
was committed before the code so the structure is reviewed at the gate, not
invented on Tuesday afternoon. Each has a different job, and keeping them
apart is a decision, not tidiness.

| Folder | Fills up on | With | Needs a key? |
| --- | --- | --- | --- |
| `src/evermind/` | Tue (tasks 2.3-2.5) | The agent package — the thing that ships | to run |
| `src/tests/` | Tue-Wed (3.1-3.6) | Deterministic tests, mocked backends | **no** |
| `src/evals/` | Thu (4.1-4.3) | Eval set against the live model | yes |
| `src/out/` | every run | `review_queue.json` — **gitignored** | — |

### Why `tests/` and `evals/` are separate

They fail for different reasons, and a suite that mixes them tells you
nothing. `tests/` asks *is the orchestration correct?* — mocked, offline,
deterministic, green on any laptop. `evals/` asks *is the model's output
good?* — live calls, non-deterministic, fails when the model drifts or the
prompt is weak. `pyproject.toml` already enforces the split:
`testpaths = ["src/tests"]`, so a bare `uv run pytest` never touches
`evals/`.

### Why `out/` is gitignored

It is the pipeline's only output and it regenerates on every run. More to
the point, `contracts/knowledge-base/contract.md` says it is the *only*
thing the system may write — that asymmetry is risk R5, the main safety
property of the design.

### Expected contents of `src/evermind/`

From `design.md`, not yet committed to:

```
__init__.py
agent.py          root LlmAgent + instruction
tools.py          3 read-only lookups over the fixtures
schemas.py        FAQCandidate + the cite-or-reject validator
guardrails.py     input cap, citation cross-check, injection handling
grouping.py       deterministic, runs before any model call
pipeline.py       run_pipeline() -> writes out/review_queue.json
```

`grouping.py` is plain Python on purpose: it is the main cost lever (one
set of model calls per *group*, not per question), unit-testable with no
backend, and the stability requirement is far easier to meet in code than
in a prompt.

---

## 2. How to command Claude to build it

### The rule

**One task per prompt, and point at the spec — not at the feature.**

"Implement grouping" invites invention. "Implement task 2.3, the behaviour
is in `specs/gap-triage/spec.md`" hands over the acceptance criteria,
including the scenarios that assert something must *not* happen.

### The template

> Implement task **2.3** from
> `src/openspec/changes/add-evermind-pipeline/tasks.md`.
>
> The behaviour it must satisfy is in
> `specs/gap-triage/spec.md`, requirement *"Logged questions are grouped
> before any are processed"*.
>
> Write the test in `src/tests/` **first**, transcribed from the scenario,
> then the implementation in `src/evermind/`.
>
> Do not change any spec. If the spec is wrong or cannot be satisfied,
> stop and say so rather than editing it.
>
> Verify with the task's own verify line and show me the output.

That last constraint is the important one. Code that quietly rewrites its
spec to go green is precisely the failure this whole process exists to
prevent.

### The week, as prompts

| Task | Prompt, in one line | Lands in |
| --- | --- | --- |
| 2.1 | "Run `tools/build_fixtures.py` twice, show me there is no git diff" | `src/fixtures/` (exists) |
| 2.2 | "Smallest ADK agent carrying one tool **and** an `output_schema`, run it against our model, write the ADR" | `docs/decisions/` |
| 2.3 | the template above | `grouping.py` + test |
| 2.4 | "Task 2.4, three read-only lookups; spec is `evidence-retrieval`. No write path anywhere" | `tools.py` + tests |
| 2.5 | "Task 2.5, one group end to end, happy path only" | `pipeline.py` |
| 3.1-3.4 | one prompt each, spec named each time | `schemas.py`, `guardrails.py` |
| 3.5 | "Task 3.5, full batch writing the queue; spec is `review-queue`" | `out/review_queue.json` |
| 4.1-4.3 | "Task 4.1, eval set covering all six paths in `design.md`" | `src/evals/` |

### Three prompts worth having ready

**When it drifts off-spec**

> That is not what `specs/<x>/spec.md` says. Re-read the requirement and
> the scenario, and tell me where your implementation differs before
> changing anything.

**The check that matters most, after any run**

> Hash the three fixture files, run the full pipeline, hash them again.
> They must be byte-identical. This is R5 and it is what a reviewer will
> ask us to demonstrate.

**Before committing anything generated**

> Show me the diff and explain any file you touched that was not named in
> the task.

---

## 3. Order, and what blocks what

```
Mon 19   Gate 1 sign-off              <- nothing below starts first
Tue 20   2.1 .. 2.5   src/evermind/   agent, tools, grouping, one group E2E
Wed 21   3.1 .. 3.6   src/tests/      all dispositions, validation, guardrails
Thu 22   4.1 .. 4.6   src/evals/      eval set, regression, peer review, deck
Fri 23   5.1 .. 5.4                   Go/No-Go, zip, handoff - 09:00
```

`tasks.md` line 20 is explicit: **no task starts before 1.1 is complete.**
No agent code before the instructor signs off. That is why all four
folders are still empty today, and it is a capstone rule, not a
preference.

---

## 4. Loose ends this plan does not resolve

**ADR numbering collides.** `tasks.md` 2.2 reserves
`docs/decisions/0001-agent-topology.md`, and `scratch/0001-...overlay.md`
also claims 0001. Renumber the scratch drafts to 0002 and 0003 when they
move, and let topology keep 0001 — `tasks.md` names it.

**The frontend is out of scope in writing.** `proposal.md` line 71 lists
*"a review UI"* under **Out**, and `build_design_evermind.py:201` says the
same. The user+admin app we discussed is in no spec, no task, and no
design document. Nothing here builds it. Either move it into scope with a
capability spec and tasks, or present it at the gate as a demo harness
over the queue file — but not silently.

**The design document still says three agents.** `TODO.md` item 1,
confirmed present in the PDF (page 4, section 5), not only the `.docx`.
Fix before Monday: the generator is the single source, five lines.
