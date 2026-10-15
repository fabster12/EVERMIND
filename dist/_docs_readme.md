# EverMind — Group 1 capstone, review package

FedEx FDE Training Program, Netherlands cohort
Phase 1 approval gate, Monday 19 October 2026

Everything here is readable. Nothing needs to be run. If you want the code
and the data files, ask for `EverMind-Group1-Tech.zip`.

---

## Read these two first

| File | Pages | What it is |
| --- | --- | --- |
| `FedEx-Capstone-Summary-Group1.pdf` | 3 | The short version. Problem, scope, risks, team, week plan. Written for someone who has not read anything else. |
| `FedEx-Capstone-Design-EverMind.pdf` | 7 | The full design, following the course template section for section. This is what gets signed off. |

Both are also here as `.md` if you prefer to read or comment in plain text.

## What EverMind is

A support knowledge base only answers what somebody thought to write down.
Every question it misses is answered by a human once and then forgotten, so
the same gap costs the same twenty minutes again next week.

EverMind reads the log of questions the knowledge base could not answer,
groups the ones that mean the same thing, and decides for each group: a
genuine gap, a rephrasing of something that already exists, or a question the
knowledge base should not answer. Genuine gaps come back as a drafted answer
with its sources attached, for a person to approve. It never publishes
anything itself.

Greenfield — everything is new, including the knowledge base.

## The Gate 1 plan

`openspec/changes/add-evermind-pipeline/` follows the OpenSpec workflow from
AIC-2101. Four artifacts, each with its own job:

| File | What it answers |
| --- | --- |
| `proposal.md` | Why we are doing this, what changes, what is in and out of scope, the risks, and **what is still open**. The approval box is at the bottom. |
| `design.md` | How we expect to build it, and the six architecture considerations. Decisions marked **OPEN** are deliberately unresolved — see below. |
| `tasks.md` | 28 ordered tasks, Monday to Friday, each with a line saying how to verify it without reading code. |
| `specs/` | Four delta specs — what the system must *do*, as Given/When/Then scenarios. The most important artifact here. |

The four spec folders:

| Capability | Covers |
| --- | --- |
| `gap-triage/` | Grouping questions, the three-way decision, refusals, and treating logged text as data rather than instruction. |
| `evidence-retrieval/` | Where evidence may come from, and what happens when there is none. |
| `candidate-drafting/` | The cite-or-reject rule, and declining to answer when unsupported. |
| `review-queue/` | The write boundary, completeness, and traceability. |

Written as behaviour, not implementation: every scenario still holds if the
internals are replaced.

## What is deliberately still open

Three decisions are **not** made in these documents, and that is on purpose.
Gate 1 approves the problem and the boundaries; the internals should be
settled against working code.

1. **One agent or several.** The handout says single agent first. There is a
   known ADK constraint that may force a split. Task 2.2 establishes which,
   on Tuesday morning, and records the answer as a decision record.
2. **How questions are grouped.** Deterministic matching or embeddings,
   measured against the labelled data.
3. **The confidence threshold** for the uncertain queue, calibrated on the
   deliberately ambiguous cases in the data.

## Also in here

| File | What it is |
| --- | --- |
| `contracts/knowledge-base/contract.md` | The data contract: shapes of the three data files, who owns what, and the one file the pipeline writes. |
| `docs/architecture.png` | The architecture drawing (also inside both PDFs). |
| `docs/openspec-alignment-review.md` | How these artifacts were checked against the OpenSpec labs, what was wrong before, and what changed. Written for us, included because it shows the reasoning. |
| `docs/decisions/0000-template.md` | The ADR template we will use during the build. Nygard format. |
| `docs/Capstone-Groups-and-Prep.md` | The training team's handout, converted to Markdown, with a note on Group 1 membership. |

## The demonstration data

Three data files make up an invented knowledge base — 45 published entries,
15 source documents, 59 unanswered questions. They are in the tech package
rather than this one, because they are machine data.

The point worth knowing: **every logged question is labelled with the outcome
the system should produce.** That turns testing from "does this look
reasonable" into "did it get the right answer".

## Two things open for Monday

- **Deck owner** is unassigned. Yasin leads, Fabian has the repo, Siva and
  Fabian share evaluation.
- **Two review questions**, at the end of the summary: whether a fully
  synthetic knowledge base is acceptable as the demonstration domain, and
  whether leaving the agent topology open until Tuesday is the right call.
