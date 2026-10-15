# OpenSpec: the flow, and the prompts that drive it

Working note. Three parts:

1. [The flow](#1-the-flow) — the pasted explainer, kept as-is
2. [Where we already are](#2-where-we-already-are) — what exists, and
   whether it still matches `proposal.md` (checked 15 Oct)
3. [Prompts](#3-prompts) — what to ask Claude at each step, and what the
   earlier prompt most likely was

---

## 1. The flow

Think of OpenSpec as **"describe first, build later."**

```
Proposal  ->  Specs  ->  Design (if needed)  ->  ADRs (if needed)
          ->  Tasks  ->  Implement  ->  Archive
```

**Step 1 — Proposal.** What problem are we solving? High level.
*Add customer notifications.*

**Step 2 — Specs.** What must the system do? Usually the first thing after
the proposal. You do not care *how* yet.

```
WHEN an order ships
THEN send an email notification

WHEN email delivery fails
THEN retry 3 times
```

> Proposal = what project?
> Specs = what must happen?

**Step 3 — Design (optional).** How might we build this?

```
Notification Service -> Email Provider -> Retry Queue
```

**Step 4 — ADRs (only if needed).** While designing you hit questions:
RabbitMQ or Azure Service Bus? Postgres or Mongo? Now write an ADR.

```
ADR-001
Decision: Use Azure Service Bus
Reason:   Already approved by company.
```

ADRs come *out of* design discussions. Not every proposal needs one.

**Step 5 — Tasks.** Only once requirements and architecture are clear.
Convert everything into work items.

**Step 6 — Implement.** Run the Apply step; work through the tasks.

### Folder shape

```
changes/
└── add-notifications/
    ├── proposal.md
    ├── specs/
    │   └── notifications.md
    ├── design.md
    ├── tasks.md
    └── adrs/
        └── ADR-001-use-service-bus.md
```

### ELI5

Building a treehouse. **Proposal:** let's build a treehouse. **Specs:** must
hold 2 kids, must have a ladder, must have a roof. **Design:** how do we
build it, where does the ladder go? **ADR:** wood not metal, because
cheaper. **Tasks:** buy wood, build floor, ladder, roof. **Build:** start
hammering.

### The thing most people get wrong

```
WRONG:  Proposal -> Tasks -> Code
RIGHT:  Proposal -> Specs -> Design -> ADRs (if needed) -> Tasks -> Code
```

The specs define **what**, the ADRs explain **why**, the tasks describe
**what to build next**.

---

## 2. Where we already are

Everything through step 5 exists, in
`src/openspec/changes/add-evermind-pipeline/`:

| Artifact | Lines | State |
| --- | --- | --- |
| `proposal.md` | 185 | Current. One `LlmAgent` (line 106) |
| `specs/` (4 capabilities, 14 requirements, 21 scenarios) | 372 | Current |
| `design.md` | 206 | Two decisions still marked **OPEN** |
| `tasks.md` | 126 | 28 tasks, Monday to Friday |
| `adrs/` | — | **Does not exist.** Two drafts are in `scratch/` |

### Do they still match the proposal? Checked 15 Oct

**Mostly yes.** Specifically:

- **Topology.** `grep` for `SequentialAgent|three agents|three specialists`
  across `specs/`, `tasks.md` and `proposal.md` returns **nothing**. The
  three-agent wording exists only in `tools/build_design_evermind.py` and
  the document it generates — `TODO.md` item 1, still open.
- **Specs cover the proposal's scope.** The four capabilities map onto the
  four things the proposal says are in scope: grouping and disposition
  (`gap-triage`), retrieval (`evidence-retrieval`), drafting with citations
  (`candidate-drafting`), the queue and the write boundary
  (`review-queue`). Nothing in scope is unspecified.
- **Risks R1-R5 each have a spec requirement behind them.** R5 ("publishes
  unreviewed") is `review-queue`: *"The knowledge base is never modified by
  the system… This MUST hold structurally rather than by policy."*

### Two things that no longer match

**1. `design.md` reasoning is stale, though not wrong.** Topology is marked
OPEN, so it does not contradict the proposal — but it presents the
three-agent split as "the lesson guide's own recommendation" with no
counterweight, and predates two facts we now have: ADK 2.x removed the
limit, and `gemini-3.5-flash` on our proxy accepted tools + `responseSchema`
in one call (15 Oct, HTTP 200 with a `functionCall`). That OPEN can close.
`TODO.md` item 2.

**2. The frontend is out of scope in writing.** `proposal.md` line 71 lists
**"a review UI"** under **Out**. We have since decided to build one. That is
a real conflict: an instructor reads the proposal, then sees an app.

Two honest ways to fix it, neither of which is "quietly build it anyway":

- Move "a review UI" from **Out** to **In**, add a capability spec for it,
  and let the gate approve the thing we are actually building. Costs one
  spec file.
- Leave scope alone and present the app as **a demo harness over the queue
  file, not part of the pipeline**. Defensible — it reads
  `review_queue.json` and writes only the overlay — but then it must not
  appear in the specs at all.

Either is fine. Deciding neither is not: the gap is the kind of thing a
reviewer finds in thirty seconds.

### What is missing from the flow

- `adrs/` does not exist in the change folder. ADRs 0001 and 0002 are drafts
  in `scratch/`. Note the project already has `docs/decisions/` with a
  Nygard template, so there are two plausible homes — pick one. The folder
  example above puts them in the change; our repo structure puts them in
  `docs/`. **Suggest `docs/decisions/`**, because they outlive the change
  and the change folder gets archived.
- Nothing is archived yet (step 7) — correct, since nothing is built.

---

## 3. Prompts

### What was probably used before

The four artifacts were produced on 15 Oct in one restructure —
`TODO.md` records it as *"Restructured Gate 1 into the four OpenSpec
artifacts… Previously one file doing all four jobs."* So the earlier prompt
was not a from-scratch generation; it was a **split**. Something close to:

> We have one document doing four jobs. Restructure it into the OpenSpec
> format from AIC-2101: `proposal.md` (why), `design.md` (how),
> `tasks.md` (in what order), and `specs/` as delta specs with
> Given/When/Then scenarios. Keep behaviour in the specs and
> implementation in the design — a spec should survive renaming the
> validator.

That last sentence is the load-bearing one, and it is worth reusing: it is
the distinction the OpenSpec labs spend the most time on.

### Step 2 — Specs from a proposal

> Read `src/openspec/changes/add-evermind-pipeline/proposal.md`. Write
> delta specs under `specs/<capability>/spec.md`, one folder per
> capability. Use RFC 2119 keywords and Given/When/Then scenarios with
> concrete values from `src/fixtures/`.
>
> Behaviour only — no class names, no function names, no framework. The
> test: if we rename the validator or swap ADK for something else, does
> the statement still hold? If not, it belongs in `design.md`.
>
> Include scenarios that assert something does **not** happen.

### Step 3 — Design

> Read the proposal and the specs. Write `design.md`: how we build it, and
> the trade-offs. Mark anything genuinely undecided as **OPEN** with what
> would settle it. Do not restate the specs — if a sentence would survive
> a rewrite of the implementation, it belongs in `specs/`.

### Step 4 — ADRs

> In `design.md` we marked X as OPEN. [Evidence/constraint] now settles it.
> Write an ADR in `docs/decisions/`, Nygard format, following
> `docs/decisions/0000-template.md`. Status Proposed. **At least one
> negative consequence is required** — if it has no cost, it was not a
> decision.

### Step 5 — Tasks

> Read the proposal, specs and design. Write `tasks.md`: ordered work
> items grouped by day, Mon 19 to Fri 23 Oct. Each task gets a **verify**
> line stating how to confirm it without reading code. No task may require
> a spec that does not exist.

### Step 6 — Implement

> Implement task 2.3 from `tasks.md`. The behaviour it must satisfy is in
> `specs/gap-triage/spec.md`, "Logged questions are grouped before any are
> processed". Write the test first, from the scenario. Do not change any
> spec — if the spec is wrong, stop and say so.

The constraint in the last sentence is what keeps the flow intact: code
that quietly rewrites its spec to pass is the failure mode this whole
process exists to prevent.

### Step 7 — Archive

> The change is built and verified. Merge the delta specs into
> `src/openspec/specs/` as the living description, move the change folder
> to `changes/archive/2026-10-23-add-evermind-pipeline/`, and leave the
> ADRs in `docs/decisions/`.

---

## 4. So can Claude just build it?

Yes — and the specs are what make that safe rather than reckless. Three
things to hold to:

**One task per prompt, not "build the project".** Each task in `tasks.md`
is sized for one sitting and carries its own verify line. A prompt that
says "implement EverMind" produces something plausible that satisfies
nothing in particular.

**Point at the spec, not at the feature.** "Implement grouping" invites
invention. "Implement task 2.3; the behaviour is in
`specs/gap-triage/spec.md`" gives it the acceptance criteria, including the
scenarios that assert something must *not* happen.

**Tests come from scenarios, and the spec does not move.** 21 scenarios are
already written. A generated test that asserts what the code happens to do
is worthless; a test transcribed from a scenario written before the code is
evidence. If the code cannot satisfy the spec, the answer is to stop and
discuss — never to edit the spec until it passes.

Our capstone rule sits on top of all of this: **no agent code before the
gate on Monday 19 October.** Steps 1-5 are done or nearly done. Step 6
starts Tuesday.
