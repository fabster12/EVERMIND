<img src="docs/brand/evermind-icon.jpg" alt="" width="96" align="right">

# EverMind

**A support knowledge base only answers what somebody thought to write
down.** Every question it misses is answered by a human once and then
forgotten, so the same gap costs the same twenty minutes again next week.

EverMind reads the log of questions the knowledge base could not answer,
groups the ones that mean the same thing, and decides for each group: a
genuine gap, a rephrasing of something that already exists, or a question
the knowledge base should not answer. Genuine gaps come back as a drafted
answer with its sources attached, for a person to approve. **It never
publishes anything itself.**

FedEx FDE Training Program capstone, Netherlands cohort · Group 1 ·
Greenfield — every component is new, including the knowledge base.

![Unanswered questions are grouped, drafted with sources, and held for a person to approve.](docs/brand/evermind-banner.jpg)

| | |
| --- | --- |
| **Status** | Phase 1 plan awaiting sign-off. No agent code is written before the gate. |
| **Gate** | Monday 19 October 2026, AMSA Schiphol |
| **Delivery** | Friday 23 October 2026, 09:00 |

---

## Start here

| If you want | Read |
| --- | --- |
| **To set it up and run it** | **[`START-HERE.md`](START-HERE.md)** — uv, credentials, daily git |
| The short version | [`docs/gate1/FedEx-Capstone-Summary-Group1.pdf`](docs/gate1/) — 3 pages |
| The full design | [`docs/gate1/FedEx-Capstone-Design-EverMind.pdf`](docs/gate1/) — 7 pages |
| The plan we are approving | [`src/openspec/changes/add-evermind-pipeline/proposal.md`](src/openspec/changes/add-evermind-pipeline/proposal.md) |
| What the system must *do* | [`src/openspec/changes/add-evermind-pipeline/specs/`](src/openspec/changes/add-evermind-pipeline/specs/) — 21 scenarios |
| What is still open | [`TODO.md`](TODO.md) |
| Where every file lives | [`STRUCTURE.md`](STRUCTURE.md) — and [`src/STRUCTURE.md`](src/STRUCTURE.md) for the project itself |

## Layout

The project splits in two: **`src/` is the thing we are building**,
everything else is about building it. Annotated file-by-file in
[`STRUCTURE.md`](STRUCTURE.md).

```
EVERMIND/
├── src/                 THE PROJECT - this is what ships
│   ├── openspec/        the spec-driven plan and the behavioural specs
│   ├── contracts/       the data contract and the ownership boundary
│   ├── fixtures/        the invented knowledge base - three JSON files
│   ├── evermind/        the agent package          (empty until Tuesday)
│   ├── tests/           unit tests, mocked backends (empty until Tuesday)
│   ├── evals/           the eval set                (empty until Thursday)
│   └── out/             review_queue.json - the only file written (gitignored)
│
├── docs/                what people read
│   ├── gate1/           the two Phase 1 deliverables (.pdf and .md)
│   ├── reviews/         how the artifacts were benchmarked, and what changed
│   ├── decisions/       ADRs - 0000 is the template
│   ├── course/          the training team's handout
│   └── architecture.png the architecture drawing
│
├── notes/               working material: the original brief, lab notes,
│                        the roadmap, and reference/ (gitignored, 36 MB)
├── tools/               document and fixture generators
│   └── packaging/       zip builder and the Word-to-PDF converter
│                        (zips go to a dist/ created on demand, not committed)
└── README.md · STRUCTURE.md · TODO.md · .gitignore · .env.example
```

### What each part of `src/` is

**`openspec/`** — the plan, in the spec-driven format from AIC-2101. A
*change* is one unit of work that eventually gets archived; ours is
`add-evermind-pipeline`. It holds four artifacts, each with a different job:

| | |
| --- | --- |
| `proposal.md` | **Why.** The problem, the solution, what is in and out of scope, the risks, and the sign-off block. This is the document the instructor approves. |
| `design.md` | **How.** The technical approach and trade-offs. Expected to change as we build. |
| `tasks.md` | **In what order.** 28 tasks, each with a line saying how to verify it without reading code. |
| `specs/` | **What it must do.** Four capabilities as Given/When/Then scenarios — behaviour, not implementation, so they still hold if the internals are replaced. |

The split matters: a spec that says *"the validator rejects an uncited
draft"* breaks when you rename the validator. One that says *"a draft with
no citation MUST NOT reach a reviewer"* survives any rewrite. Implementation
detail belongs in `design.md`; `specs/` stays at the behaviour level.

**`contracts/`** — the data contract. It writes down the shape of every file
the system touches, who owns it, and crucially **what the system may never
do to it**. Normally a contract describes someone else's system that you
must not break; ours describes our own data, and exists for the asymmetry it
records: *the pipeline reads three files and writes exactly one, and the one
it writes is not the knowledge base.* That boundary is the main safety
property of the whole design, so it is written down rather than assumed.

**`fixtures/`** — the demonstration data. Not test samples — **this IS the
system**. There is no FedEx data anywhere. Three JSON files generated from
one seed by `tools/build_fixtures.py`, so anyone rebuilds them byte-for-byte:

| File | Contents |
| --- | --- |
| `faq_store.json` | 45 published entries across six topics — the knowledge base we grow |
| `sources.json` | 15 documents, 31 passages — the only evidence a draft may cite |
| `query_log.json` | 59 unanswered questions, **each labelled with the outcome it should produce** |

That labelling is the point. The answer key lives in a file the agent never
reads, which turns testing from *"does this look reasonable?"* into *"did it
get the right answer?"* Three of the genuine gaps are **deliberately
unsupported** by any source — any system drafts when the evidence is in
front of it; those three test whether it declines when it is not.

**`evermind/`** — the agent package. The actual Python: the agent, its
tools, the output schema, the guardrails. Empty until Tuesday, because the
capstone rule is that no agent code is written before the plan is approved.
It is named after the project because that is what you will `import`.

**`tests/`** — deterministic unit tests with mocked backends. These run
without an API key and without a network: call a tool, assert on what comes
back, including the error path. Kept separate from `evals/` on purpose —
these answer *"is the orchestration correct?"*, which is a different
question from *"is the model's output good?"* Mixing them gives you a suite
that fails for two unrelated reasons.

**`evals/`** — the evaluation set, run against the live model. Built from
the labelled query log, covering the ordinary path, a gap with no supporting
source, a duplicate, a refusal, an adversarial input, and the regression
check that a full run leaves the knowledge base byte-for-byte unchanged.
This is the evidence behind Friday's Go/No-Go decision.

**`out/`** — where the pipeline writes `review_queue.json`, its single
output. Gitignored: regenerated on every run.

## Why `.docx` is not committed

Every Word document here is generated by a script in `tools/`. The `.pdf`
and `.md` are what people read and are committed; the `.docx` regenerates
identically. Keeping all three invites someone to read a stale one.

## Regenerating everything

```bash
pip install python-docx pillow            # the only dependencies

python tools/build_fixtures.py            # src/fixtures/*.json (deterministic)
python tools/build_diagram.py             # docs/architecture.png
python tools/build_design_evermind.py     # docs/gate1/...Design-EverMind.docx
python tools/build_summary_group1.py      # docs/gate1/...Summary-Group1.docx
python tools/build_review_benchmark.py    # docs/reviews/...Review.docx

# .docx -> .pdf. Needs Microsoft Word; drives it over COM.
powershell -ExecutionPolicy Bypass -File tools/packaging/to_pdf.ps1

# the two share packages, integrity-checked and scanned for credentials
python tools/packaging/build_packages.py
```

Every script overwrites its own output, so re-running is safe.

**Do not change `SEED` in `build_fixtures.py` once the eval set exists.**
The tests assert against specific ids; reshuffling them breaks the suite
silently.

## Team

Four roles across three people — Rafael Del Hoyo is no longer
participating, so evaluation is shared rather than dropped.

| Role | Owner |
| --- | --- |
| Lead | Yasin Durgun |
| Repository owner | Fabian William Bakker |
| Evaluation owner | Siva Prasada Reddy Sogalapalli and Fabian William Bakker |
| Deck owner | *to be agreed Monday* |

Everyone codes. Siva originated the idea.

## Secrets

`.env` is gitignored and must stay that way. `.env.example` carries variable
**names only**, never values. Both share packages are scanned for credential
patterns before they are written.
