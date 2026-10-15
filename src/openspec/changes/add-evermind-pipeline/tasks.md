# Tasks: EverMind

**Change:** `add-evermind-pipeline`

Ordered. Each task names how to verify it without reading the code, per the
OpenSpec lab's rule that a task is too broad if you cannot check it
independently.

Dependencies run backend-first: nothing that consumes a tool is built before
the tool exists.

---

## Monday 19 — Gate 1

- [ ] **1.1** Present the proposal at the Phase 1 gate.
      *Verify:* the approval record in `proposal.md` is filled in with a
      decision, an approver and a date.

> No task below starts before 1.1 is complete.

## Tuesday 20 — Foundation

- [ ] **2.1** Commit the fixture generator and its output.
      *Verify:* `python tools/build_fixtures.py` twice in a row produces no
      git diff; the three fixture files are committed.

- [ ] **2.2** Settle the agent topology question.
      Build the smallest possible agent that carries both a tool and a
      structured output schema, and run it against the model we are using.
      *Verify:* `docs/decisions/0001-agent-topology.md` exists, states the
      decision as an affirmative action, and cites what was observed.
      *This task exists to answer an open question, so either outcome is a
      pass. What fails is not having asked.*

- [ ] **2.3** Implement grouping over a logged batch.
      *Verify:* running it twice over the fixture log produces identical
      groups and identifiers; the three transit-time rephrasings land in one
      group; the packaging question does not join them.

- [ ] **2.4** Implement the three read-only lookups: existing-entry search,
      scope classification, source retrieval.
      *Verify:* each returns expected results for a known fixture input, and
      none has a write path — `grep` for any write call in the package
      returns nothing.

- [ ] **2.5** One group end to end, happy path only.
      *Verify:* a single genuine gap produces a candidate with at least one
      citation.

## Wednesday 21 — Behaviour

- [ ] **3.1** Triage disposition for all three outcomes.
      *Verify:* a duplicate names its matching entry; a refusal carries a
      reason; a genuine gap proceeds. No refused group triggers retrieval.

- [ ] **3.2** Record retrieved passage identifiers per group, per run.
      *Verify:* after a run, the passages retrieved for a group can be read
      back, and contain nothing retrieved for another group.

- [ ] **3.3** Cite-or-reject validation.
      *Verify:* a draft with no citation is rejected; a draft citing a
      passage that was not retrieved is rejected; a draft over 150 words is
      rejected.

- [ ] **3.4** The no-evidence path.
      *Verify:* the fine-art insurance fixture produces no answer text, low
      confidence, and a record that no supporting evidence exists.

- [ ] **3.5** Full batch run writing the review queue.
      *Verify:* every group in the batch appears exactly once in
      `out/review_queue.json`, refusals and duplicates included.

- [ ] **3.6** Guardrails: input size cap and audit logging.
      *Verify:* an oversized group is capped rather than sent; the log shows
      one line per model and tool call with latency and token count.

## Thursday 22 — Evidence

- [ ] **4.1** Eval set covering all six paths in `design.md`.
      *Verify:* `AgentEvaluator` runs green; each case maps to a named
      scenario in a delta spec.

- [ ] **4.2** Write-path regression test.
      *Verify:* the knowledge base checksum is identical before and after a
      full run, asserted in CI rather than checked by hand.

- [ ] **4.3** Idempotency test.
      *Verify:* the same batch run twice produces candidates with identical
      identifiers.

- [ ] **4.4** Peer review using the RAPID ITC.009 skill.
      *Verify:* `docs/rapid-peer-review.md` exists with every Fail resolved
      or explicitly accepted with a reason.

- [ ] **4.5** Record the remaining ADRs for decisions actually made.
      *Verify:* `docs/decisions/` contains a numbered ADR for each
      non-obvious structural choice, each with at least one negative
      consequence stated. An ADR listing only benefits is incomplete.

- [ ] **4.6** Draft and rehearse the deck, timed to five minutes.
      *Verify:* a timed run-through lands under five minutes.

## Friday 23 — Delivery

- [ ] **5.1** Go/No-Go decision per RAPID ITC.004.
      *Verify:* `docs/go-no-go.md` records the decision with at least two
      sentences of cited evidence from the eval runs.

- [ ] **5.2** Release zip.
      *Verify:* a teammate unzips it on a clean machine, follows the README,
      runs the tests, and needs nothing that is not in the zip. `.env` is
      absent; `.env.example` is present.

- [ ] **5.3** Operational handoff notes.
      *Verify:* `docs/operations.md` names ownership, monitoring, known
      limitations and next changes — including that the corpus is synthetic.

- [ ] **5.4** Deliver zip and deck by 09:00.

## After the gate

- [ ] **6.1** Archive the change: merge the delta specs into `openspec/specs/`
      and move this folder to `openspec/changes/archive/`.
      *Verify:* `openspec/specs/` describes current behaviour; the active
      changes directory is empty.
