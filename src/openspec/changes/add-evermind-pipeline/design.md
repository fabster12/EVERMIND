# Design: EverMind

**Change:** `add-evermind-pipeline`
**Status:** Draft — written at Gate 1, confirmed against working code at Gate 3

This is the *how*. The delta specs under `specs/` say what the system must
do and stay true if the internals are replaced; this document records the
implementation choices and is expected to change as we build.

Decisions marked **OPEN** are deliberately unresolved at Gate 1. Each becomes
an ADR in `docs/decisions/` once settled against working code.

---

## Agent topology — OPEN

The capstone handout is explicit: *"Single agent first. Do not promise a
multi-agent system."* We start with one agent and split only if a constraint
forces it.

There is a known constraint. The ADK lesson guide warns that combining a
structured output schema with tool use depends on model support, and advises
retrieving facts in application code before passing them to a schema-bound
step. If that constraint bites on the model we use, the natural split is:

| Step | Responsibility | Why it might be separate |
| --- | --- | --- |
| Triage | Decide gap / duplicate / out of scope | Needs tools; needs no schema |
| Research | Retrieve supporting passages | Needs tools; needs no schema |
| Drafting | Write the grounded answer | Needs a schema; needs no tools — which also makes it unable to cite what it never read |

That is an attractive shape, and it is the lesson guide's own
recommendation. It is not yet a decision. **Tuesday's first task is to
establish empirically whether one agent can carry both tools and a
structured schema on our model.** The answer becomes
`docs/decisions/0001-agent-topology.md` either way, with the measurement
that settled it.

We are recording the fallback here so that if the single agent fails on
Tuesday morning, nobody spends Tuesday afternoon rediscovering the fix.

## Grouping approach — OPEN

Two candidates:

| Approach | For | Against |
| --- | --- | --- |
| Deterministic string similarity | Reproducible, free, testable without a model, no backend dependency | Misses paraphrases that share no vocabulary |
| Embedding similarity | Handles genuine paraphrase | Costs a call per question, and group membership can shift between runs |

The spec requires stable group identifiers across runs, which deterministic
similarity satisfies trivially and embeddings satisfy only with care. We
start deterministic and measure the miss rate against the labelled fixtures;
the fixtures are built with light rephrasing specifically so this is
measurable. Outcome becomes `docs/decisions/0002-grouping-approach.md`.

## Component sketch

```
fixtures/ ──► grouping ──► triage ──► retrieval ──► drafting ──► validation ──► out/review_queue.json
                                │                                     │
                                └── duplicate / out of scope ──────────┘
```

Grouping is ordinary code, not a model call. That is deliberate on three
counts: it is the main cost lever (one set of calls per group, not per
question), it is unit-testable without a backend, and the spec's stability
requirement is far easier to meet in code than in a prompt.

Validation sits after drafting rather than inside it. A model asked to
self-check its own citations is marking its own homework; a separate check
that compares cited identifiers against retrieved identifiers either passes
or does not.

## Expected constructs

Listed as expectation, not commitment. The Gate 1 checklist asks for this,
and marks unused capabilities as not applicable.

| Element | Plan |
| --- | --- |
| Agent package | `evermind/` — `agent.py`, `tools.py`, `schemas.py`, `guardrails.py`, `grouping.py` |
| Output schema | A Pydantic model for the candidate, carrying the cite-or-reject validator |
| Tools | Read-only lookups over the fixtures: existing-entry search, scope classification, source retrieval |
| MCP server | **Not applicable** — nothing to expose to other clients |
| Session / state | Retrieved passage identifiers and the triage verdict, scoped per group |
| Guardrails | Input size cap, citation cross-check, injection handling |
| Sub-agents | **OPEN** — see *Agent topology* above |
| A2A / remote agents | **Not applicable** — no ownership boundary justifies distribution |
| Response caching | **Not applicable** — the lab's latest-text-only cache is unsafe for this, and the lesson guide says so |
| Evaluation | An eval set over the labelled fixtures, run in CI |
| Deployment | Design only; Google Cloud as a design question. Nothing deployed live. |

## Why this needs an agent at all

Worth stating because Gate 0 asks for it, and because "it uses an LLM" is
not an answer.

- **Tool calls are required.** Deciding whether an answer already exists
  means querying the knowledge base. Drafting a grounded answer means
  retrieving passages first. Neither is model knowledge.
- **State is read and written across steps.** Passage identifiers recorded
  during retrieval are read back during validation. The citation guard
  depends on that persistence.
- **Control flow branches.** A group dispositioned duplicate or out of scope
  skips retrieval and drafting entirely.
- **It ends in a decision.** Every group leaves with a disposition and a
  reason, not a conversation.

## Evaluation approach

The labelled fixtures make this assertable rather than impressionistic.
Every logged question carries the disposition it should produce, so a test
asks *"did it get the right answer?"* rather than *"does this look
reasonable?"*

| Path | What it asserts | Spec it exercises |
| --- | --- | --- |
| Ordinary | A supported gap produces a cited answer within the length limit | `candidate-drafting` |
| Failure | An unsupported gap produces no answer and low confidence | `evidence-retrieval`, `candidate-drafting` |
| Edge | A rephrasing of a published entry is returned as a duplicate | `gap-triage` |
| Policy | An account-specific question is refused, with no retrieval performed | `gap-triage` |
| Adversarial | An embedded instruction is refused, not obeyed | `gap-triage` |
| Regression | A full run leaves the knowledge base byte-for-byte unchanged | `review-queue` |

Deterministic unit tests — grouping, validation, routing — run separately
from model evaluations with mocked backends, keeping orchestration
correctness apart from live-model quality scores.

## Architecture considerations

Deployment target is Google Cloud. These are design answers; nothing is
deployed live.

### Security

No real customer data, no real FedEx content, no credentials at any point.
Every fixture is generated by a seeded script committed to the repo, so a
clean checkout runs the deterministic tests with no secrets and no network.

Logged questions are untrusted text, and one fixture is a prompt injection
verbatim — an eval case rather than a footnote. Two things contain it:
nothing in the pipeline can write anywhere, and every draft is read by a
human before it becomes an entry.

Secrets stay out of git: `.env` gitignored, `.env.example` with names only,
model credentials from the environment and from Secret Manager in a hosted
pilot. Tool arguments can themselves be sensitive, so the audit log is
redacted by the same policy as the prompts.

### Reliability

Validation is the reliability boundary: an uncited or malformed candidate
fails before it reaches a reviewer rather than after. Tool failures return a
typed error the agent must handle.

The job is batch, not interactive. A failed run is retried over the same log
with no user-visible effect, and the spec's idempotency requirement means a
retry cannot double-queue work.

### Performance efficiency

Bulk text never enters a prompt. Grouping reduces 59 logged questions to
roughly a dozen groups before any model call, and retrieval returns passages
rather than whole documents. An input size cap stops one pathological group
exhausting the context window.

Latency is not a constraint — nothing waits on this. The figure that matters
is a day's questions processed inside an overnight window.

### Cost effectiveness

Grouping is the main lever: one set of calls per *group* rather than per
question turns ~59 would-be calls into ~12. That is an order of magnitude
from design, not from tuning.

Triage short-circuits duplicates and refusals before the more expensive
steps run — roughly half the fixture log never reaches drafting. If the
topology splits into three steps, cost per group rises accordingly; that
trade-off is part of the ADR, measured rather than assumed.

### Operational excellence

Every model and tool call is logged with latency and token count, and the
passages behind each draft are recorded. That is what makes approval real
rather than ceremonial — the reviewer can trace a claim to its source.

The eval set is the regression gate and runs in CI. Reviewer decisions are
themselves signal: a rejected draft is evidence about where the system is
weak, and feeding that back is the natural next change.

Known limitation to record at handover: the corpus is static and synthetic,
so the eval set proves behaviour against fixtures, not against real content.

### Deployment

Design only, targeting Google Cloud: the agent packaged for Agent Engine,
fixtures as read-only assets, secrets in Secret Manager, traces to Cloud
Trace, and the eval suite as a build-time gate.

In a real deployment this is a scheduled overnight job over the previous
day's unanswered questions, writing to an approval queue. It is deliberately
not in any live request path: a failure delays a draft and degrades nothing
a user sees. The queue is the integration point, and it is human-operated.

Nothing is deployed live during the capstone.
