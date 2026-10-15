# `src/` — the project

This is the thing we are building. Everything outside `src/` is about
building it: documents, generators, notes, packaging.

The repository-wide map is in [`../STRUCTURE.md`](../STRUCTURE.md).

---

## The whole tree

```text
src/
├── openspec/                                  The plan, in the spec-driven format from AIC-2101
│   └── changes/
│       └── add-evermind-pipeline/             One unit of work. Verb-led slug, like a branch name
│           ├── proposal.md                    WHY. Problem, solution, scope, risks, sign-off block
│           ├── design.md                      HOW. Technical approach and trade-offs. Expected to change
│           ├── tasks.md                       IN WHAT ORDER. 28 tasks, each with a verify line
│           └── specs/                         WHAT IT MUST DO. Behaviour as Given/When/Then
│               ├── gap-triage/spec.md         Grouping, the three-way decision, refusals, injection
│               ├── evidence-retrieval/spec.md Where evidence may come from, and when there is none
│               ├── candidate-drafting/spec.md Cite-or-reject, and declining when unsupported
│               └── review-queue/spec.md       The write boundary, completeness, traceability
│
├── contracts/
│   └── knowledge-base/
│       └── contract.md                        Exact data shapes, who owns what, and what we may never write
│
├── fixtures/                                  The invented knowledge base. Not samples - this IS the system
│   ├── faq_store.json                         45 published entries, six topics. What we grow. Read-only
│   ├── sources.json                           15 documents, 31 passages. The only evidence a draft may cite
│   └── query_log.json                         59 unanswered questions, each labelled with its right answer
│
├── evermind/                                  THE AGENT PACKAGE - empty until Tuesday
│   └── .gitkeep                               (no agent code is written before the plan is approved)
│
├── tests/                                     Deterministic tests. Mocked backends, no API key, no network
│   └── .gitkeep
│
├── evals/                                     Model evaluation against the labelled data
│   └── .gitkeep
│
└── out/                                       GITIGNORED. review_queue.json - the pipeline's only output
    └── .gitkeep
```

---

## `openspec/` — the plan

The spec-driven lifecycle from AIC-2101: **explore → propose → apply →
verify → archive.** A *change* is one unit of work that eventually gets
archived, so it is named like a branch — `add-evermind-pipeline`, a verb
phrase, not a product name.

Four artifacts, deliberately separate because they answer different
questions and age at different rates:

| File | Answers | Changes |
| --- | --- | --- |
| `proposal.md` | Why are we doing this? | Frozen once signed off |
| `design.md` | How will we build it? | Often, as we learn |
| `tasks.md` | In what order? | Daily, as items are ticked |
| `specs/` | What must it do? | Rarely — behaviour outlives implementation |

### Why `specs/` is not the same as `design.md`

This is the distinction the OpenSpec labs spend the most time on, and the
one easiest to get wrong.

```
Implementation (belongs in design.md):
    The drafting agent has no tools. An after_tool_callback records
    every passage id into session.state, and the Pydantic validator
    rejects a draft with no citation.

Behaviour (belongs in specs/):
    Every citation MUST name a passage that was retrieved for that
    group during that run. A draft that cites nothing MUST be
    rejected before it reaches the reviewer.
```

The test: **rename the validator, swap the framework, restructure the
agent — does the statement still hold?** The first breaks. The second
survives any rewrite, which is what makes it worth writing down.

Specs use RFC 2119 keywords (MUST, MUST NOT, SHOULD) and Given/When/Then
scenarios with concrete values. 21 scenarios across the four capabilities.

Several deliberately assert that something does **not** happen: no answer
without evidence, no retrieval for a refused question, no new entry after a
full run, no evidence leaking between groups. A system that drafts a
plausible answer from nothing passes every happy-path test ever written.

### After the gate

When the change is built and verified, it is archived: the delta specs
merge into `openspec/specs/` (which becomes the living description of what
the system does) and the change folder moves to `openspec/changes/archive/`
with a timestamp. Neither directory exists yet — nothing has been
implemented.

## `contracts/` — the boundary

A contract writes down the shape of every file the system touches, who owns
it, and **what the system may never do to it**.

Usually a contract describes someone else's system — the brownfield
black-box rule. Ours is greenfield, so the contract describes our own data.
It exists anyway, for one asymmetry:

> **The pipeline reads three files and writes exactly one — and the one it
> writes is not the knowledge base.**

| File | We may | We must never |
| --- | --- | --- |
| `fixtures/faq_store.json` | read | write, append, modify |
| `fixtures/query_log.json` | read a batch | write, acknowledge, delete |
| `fixtures/sources.json` | read | write, modify |
| `out/review_queue.json` | **write** | — this is our only output |

That is the main safety property of the whole design, so it is written down
rather than assumed. Publishing an approved candidate is a separate,
human-triggered step that lives outside the pipeline. No module imports a
function that writes to the knowledge base, so there is no code path by
which a model decision can publish.

## `fixtures/` — the demonstration data

**Not test samples. This IS the system.** There is no FedEx data anywhere
in this project. All three files are generated by `tools/build_fixtures.py`
from a single seed (`20261019`), so anyone rebuilds them byte-for-byte.

| File | Contents |
| --- | --- |
| `faq_store.json` | 45 published entries across shipping, tracking, customs, packaging, billing, returns |
| `sources.json` | 15 documents, 31 citable passages — deliberately does *not* cover every gap |
| `query_log.json` | 59 questions the base could not answer |

### Why the query log is the interesting one

Every logged question carries the outcome the system is supposed to
produce:

```json
{
  "query_id": "Q-017",
  "query_text": "If I ship DDP, who gets the duty bill?",
  "expected_disposition": "HUMAN_REVIEW",
  "expected_source": "SRC-02"
}
```

**That `expected_` field is the whole point.** The answer key lives in a
file the agent never reads, which turns testing from *"does this output
look reasonable?"* into *"did it get the right answer?"* — the difference
between evidence and opinion.

| Expected outcome | Count | What it exercises |
| --- | --- | --- |
| `HUMAN_REVIEW` | 29 | Genuine gaps. 26 have a supporting source; **3 deliberately do not** |
| `DUPLICATE_OF_EXISTING` | 15 | Rephrasings of published entries |
| `REJECT_OUT_OF_SCOPE` | 10 | Account specifics, a complaint, commercial terms, one prompt injection |
| `LOW_CONFIDENCE` | 5 | Genuinely ambiguous — we assert confidence is low, not which way it went |

Those **three unsupported gaps** are the most important records in the set.
Any system drafts an answer when the evidence is in front of it; those three
test whether it declines when it is not.

`query_text` is untrusted input at every step. One record is a prompt
injection verbatim, sitting in the normal log rather than a separate
adversarial file — because that is where it would arrive in reality.

**Do not change `SEED` once the eval set exists.** Tests assert against
specific ids; reshuffling them breaks the suite silently.

## `evermind/` — the agent package

The actual Python. Named after the project because that is what you will
`import`.

Empty until Tuesday: the capstone rule is that no agent code is written
before the Phase 1 plan is signed off.

Expected shape, from `design.md` — not yet committed to:

```text
evermind/
    __init__.py
    agent.py          the root LlmAgent and its instruction
    tools.py          three read-only lookups over the fixtures
    schemas.py        the FAQCandidate model and its cite-or-reject validator
    guardrails.py     input cap, citation cross-check, injection handling
    grouping.py       deterministic, runs before any model call
```

`grouping.py` is plain Python on purpose: it is the main cost lever (one set
of model calls per group instead of per question), it is unit-testable
without a backend, and the spec's stability requirement is far easier to
meet in code than in a prompt.

## `tests/` and `evals/` — kept apart deliberately

They answer different questions, and mixing them gives you a suite that
fails for two unrelated reasons.

| | `tests/` | `evals/` |
| --- | --- | --- |
| Asks | Is the orchestration correct? | Is the model's output good? |
| Runs against | Mocked backends | The live model |
| Needs an API key | No | Yes |
| Deterministic | Yes | No |
| Fails when | The code is wrong | The model drifts, or the prompt is weak |

**`tests/`** — call each tool function and assert on its return value,
including the error path. Construct the output schema and prove its
validators reject bad values. These run on any machine with no setup.

**`evals/`** — built from the labelled query log, covering the ordinary
path, a gap with no supporting source, a duplicate, a refusal, an
adversarial input, and the regression check that a full run leaves the
knowledge base byte-for-byte unchanged. This is the evidence behind Friday's
Go/No-Go decision.

## `out/` — the single output

Where the pipeline writes `review_queue.json`: one candidate per group, with
citations and the audit trail, for a human to work through.

Gitignored — regenerated on every run.

**This is the only directory the agent writes to.** That is not a
convention, it is the design: see `contracts/knowledge-base/contract.md`.
