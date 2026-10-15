# ADR 0001: Approved answers go to an overlay, not the knowledge base

> Draft, in `scratch/`. Move to `docs/decisions/` when the group agrees.

## Status

Proposed

<!-- One of: Proposed | Accepted | Superseded by ADR NNNN -->

## Context

The review loop only pays for itself if an approved answer reaches the bot:
a question the bot could not answer is queued, an admin reviews and edits
it, and the bot should answer it next time. That last arrow needs a file
the lookup tool reads.

Two candidates. Writing the approved entry into `fixtures/faq_store.json`
makes the knowledge base visibly grow, 45 entries to 46, which demonstrates
well. But `contracts/knowledge-base/contract.md` says the pipeline may never
write that file, and the regression test asserts all three fixtures are
byte-identical after a full run — the evidence behind risk R5. Adding a
second writer means amending the contract and narrowing that test four days
before delivery.

## Decision

We will write approved entries to `src/out/published.json`, an overlay the
lookup tool reads alongside `faq_store.json`, with an overlay entry winning
on conflict. The fixtures stay read-only to every component.

## Consequences

- The byte-identical fixture test keeps covering the whole system with no
  carve-out, so R5 stays provable by the simplest possible check — the one
  a reviewer will actually ask us to run.
- The contract needs no amendment, and `out/` is already the only directory
  anything writes to.
- Approvals survive a fixture rebuild. `build_fixtures.py` regenerates from
  seed `20261019`; had we written into `faq_store.json`, a rebuild would
  silently discard every approval.
- **The demo is weaker.** "The knowledge base grew" is a better five-minute
  story than "a second file now also has an answer in it", and the growth
  is not visible in the fixture counts the documents quote.
- **Two stores to search.** `search_faq_db` must read both and apply the
  precedence rule, and the duplicate check must consider overlay entries or
  the same gap gets drafted twice.
- `out/` is gitignored, so approvals are local to whoever ran the app. Fine
  for a capstone; it would not be in production.
