# ADR 0002: Pin `google-adk>=2.1.0,<3`

> Draft, in `scratch/`. Move to `docs/decisions/` when the group agrees.

## Status

Proposed

## Context

Six people install on their own laptops on Tuesday morning. Without a pin
they resolve to whatever is current that day, and two constraints make the
version material rather than cosmetic.

The WA3915 lab guide: *"The Dev UI Traces waterfall requires ADK 2.1.0 or
later. On 2.0.0 the tab shows zero spans."* Traces are how the demo shows
tool calls and how the cost discussion is evidenced.

WA3922-CAP: one `LlmAgent` can call tools and emit an `output_schema`
together in 2.x, where 1.x forced a `SequentialAgent` split. `TODO.md`
item 1 records that we designed around that removed limit once already.

The WA3915 caveat — *"only some models support both at once"* — is
model-dependent, so it needed testing rather than assuming. On 15 October,
`gemini-3.5-flash` through the Vocareum proxy was sent one request carrying
both a `functionDeclarations` tool and a `responseSchema`. It returned
HTTP 200 with a `functionCall`. Our model carries both.

## Decision

We will pin `google-adk>=2.1.0,<3` in `pyproject.toml` and commit `uv.lock`.

## Consequences

- The Traces tab works for everyone, so the demo and the cost numbers rest
  on the same evidence on every laptop.
- `uv sync` from a clean checkout resolves identically, which is the
  clean-checkout test the handout asks for.
- The single-agent topology is now supported by a result on our own model,
  not only by a course quote. That is what `design.md` marks OPEN and what
  `tasks.md` task 2.2 exists to establish.
- **A 3.0 release during the week is unavailable to us**, pin or not. The
  upper bound makes that a deliberate choice rather than a surprise.
- **The REST test is not an ADK test.** It proves the model accepts the
  pairing; it does not prove ADK's `output_schema` plumbing behaves the
  same way. Task 2.2 still runs Tuesday, now as a confirmation rather than
  an open question.
- Anyone already on 2.0.0 must re-sync. The failure is silent — an empty
  Traces tab, not an error — so it is worth saying out loud on Tuesday.
