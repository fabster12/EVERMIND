# Data contract: the EverMind knowledge base

**Change:** `add-evermind-pipeline`
**Status:** Proposed at Gate 1, to be confirmed at Gate 3
**Owner:** Group 1 — this is our data, not an external system's

EverMind is greenfield: there is no existing system behind any of this.
The three fixture files described below *are* the knowledge base, generated
by `tools/build_fixtures.py` from seed `20261019` and committed to the repo.

This contract exists anyway, for a reason the Gate 3 checklist makes
explicit: inputs, outputs, state and ownership boundaries have to be defined
whether or not someone else owns them. Writing the shape down is also what
lets the fixture generator and the agent code be built in parallel by
different people.

## Ownership and access

| File | Produced by | EverMind may | Must never |
| --- | --- | --- | --- |
| `fixtures/faq_store.json` | `build_fixtures.py` | read, via `search_faq_db()` | write, append, or modify |
| `fixtures/query_log.json` | `build_fixtures.py` | read a batch | write, acknowledge, or delete entries |
| `fixtures/sources.json` | `build_fixtures.py` | read, via `search_sources()` | write or modify |
| `out/review_queue.json` | EverMind | write | — this is our only output |

The asymmetry is the point: **the pipeline writes exactly one file, and it is
not the knowledge base.** Publishing an approved candidate into
`faq_store.json` is a separate human-triggered step, deliberately outside the
pipeline. No component of EverMind imports a function that writes to it,
so there is no code path by which a model decision can publish.

## Shapes

### `faq_store.json` — the knowledge base

```json
{
  "generated_seed": 20261019,
  "entries": [
    {
      "faq_id": "FAQ-001",
      "topic": "shipping",
      "question": "How long does international shipping take?",
      "answer": "Transit time depends on the service level selected...",
      "status": "published"
    }
  ]
}
```

45 entries across six topics: shipping, tracking, customs, packaging,
billing, returns. `faq_id` is stable across regeneration — the eval set
asserts against specific ids, so the seed must not change casually.

### `sources.json` — the citable evidence

```json
{
  "documents": [
    {
      "doc_id": "SRC-01",
      "topic": "customs",
      "title": "Customs Documentation Standard",
      "version": "2026-09-01",
      "passages": [
        {"passage_id": "SRC-01-P1", "text": "A commercial invoice must..."}
      ]
    }
  ]
}
```

15 documents, 31 passages. A draft may cite **only** a `passage_id` from this
file, and only one the research agent actually retrieved in that run. The
corpus deliberately does not cover every genuine gap — see below.

### `query_log.json` — the questions that went unanswered

```json
{
  "queries": [
    {
      "query_id": "Q-017",
      "query_text": "If I ship DDP, who gets the duty bill?",
      "timestamp": "2026-10-09T14:23:00Z",
      "locale": "en-GB",
      "session_id": "S-4471",
      "expected_disposition": "HUMAN_REVIEW",
      "topic": "customs",
      "expected_source": "SRC-02",
      "cluster_hint": "SRC-02"
    }
  ]
}
```

`query_text` is **untrusted input**. It is treated as data at every step; one
fixture is a prompt injection verbatim.

## The labels, and why they matter

59 logged questions, each carrying the disposition it should produce. Those
labels are what make the eval set assertable rather than impressionistic.

| Expected disposition | Count | What it exercises |
| --- | --- | --- |
| `HUMAN_REVIEW` | 29 | Genuine gaps. 26 have a supporting source; **3 deliberately do not** — the failure-path fixture behind E2. |
| `DUPLICATE_OF_EXISTING` | 15 | Rephrasings of published entries, each naming its `expected_faq_id`. |
| `REJECT_OUT_OF_SCOPE` | 10 | Account-specific requests, a complaint, commercial negotiation, an unrelated question, and one prompt injection. |
| `LOW_CONFIDENCE` | 5 | Genuinely ambiguous. Either disposition is defensible; what is asserted is that confidence is low, not which way it went. |

Genuine gaps repeat 2–5 times with light rephrasing, so clustering has real
work to do rather than a trivial one-to-one mapping.

Three design notes worth stating, because each is a fixture choice an
instructor may ask about:

1. **The unsupported gaps are the most important fixture in the set.** Any
   system can draft when the evidence is there. E2 asserts the system
   declines when it is not.
2. **`LOW_CONFIDENCE` is not a fourth disposition** in the schema. It is a
   fixture label meaning "assert `confidence < 0.5`, do not assert the
   branch." Pretending these cases have one right answer would be dishonest
   about the task.
3. **The injection fixture is in the normal log**, not a separate adversarial
   file, because that is where it would arrive in reality.

## Regeneration and stability

```bash
python tools/build_fixtures.py          # writes fixtures/, deterministic
```

Same seed, same bytes — verified. Changing `SEED` reshuffles ids and will
break eval cases that name specific ones; treat the seed as frozen once the
eval set exists.

The generator is committed and the generated files are committed too. That is
deliberate: a reviewer should be able to read the fixtures without running
anything, and CI should fail if a regeneration produces a diff.

## Checks at Gate 3

- [ ] `search_faq_db()` and `search_sources()` are read-only; no write
      function is implemented or imported anywhere in `evermind/`.
- [ ] A full batch run leaves all three fixture checksums unchanged (**E4**).
- [ ] Every `passage_id` in a candidate's citations appears in that run's
      `state['retrieved_passages']`.
- [ ] Regenerating fixtures produces no diff against the committed copies.
- [ ] The injection fixture produces no anomalous tool call (**E6**).
