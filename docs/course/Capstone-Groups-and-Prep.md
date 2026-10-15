# Capstone Groups and Preparation

> Converted from `Capstone-Groups-and-Prep.pdf` (the handout issued by the
> training team). Content is reproduced as published; the only addition is the
> note on Group 1 membership marked **[Group 1 note]** below.

FedEx FDE Training Program, Netherlands cohort
Capstone week: Monday 19 to Friday 23 October 2026, AMSA Schiphol, Prestwickweg 1
Presentations and graduation: Friday 23 October

## Groups

| Group 1 | Group 2 | Group 3 |
| --- | --- | --- |
| Fabian William Bakker | Szymon Duraj | Paul Horsley |
| ~~Rafael Del Hoyo~~ * | Deepu James | Luis Ruiz |
| Siva Prasada Reddy Sogalapalli | Maciej Kucia | Mateusz Smet |
| Yasin Durgun | Neil Weber | Vijay Kumar Jupalli |
| | Ross Luker | |

| Group 4 | Group 5 | Group 6 |
| --- | --- | --- |
| Pratik Patel | Milan Zbirkovsky | Ufuk Celikeloglu |
| Daniel Vink | Brendan Earley | Marc Lemmens |
| Luis Eduardo Garcia | Kamalakannan Kumar | Said Hirsi |
| Sandro Fornasier | Quynh Chi Vo | Uatilla Almeida |
| | Vikram Mahawal | |

Each group has four or five members. Agree the four roles described below
before Monday.

> **[Group 1 note]** \* Rafael Del Hoyo is no longer participating. Group 1 is
> three members, so the four roles are covered by three people: evaluation is
> shared between Siva and Fabian rather than held by a dedicated owner. See
> `FedEx-Capstone-Summary-Group1.docx`.

## Before the Capstone Starts

Arrive on Monday 19 October ready to pass the Phase 1 approval gate. Phase 1
is 1.5 hours. No agent code is written until the instructor signs off the plan.

### 1. Agree on a problem

- A repetitive, rule-bound task that ends in a decision or a structured
  result. If one model call would solve it, it is too weak.
- Genuinely agentic: calls at least one tool, reads or writes session state,
  or delegates to a sub-agent.
- Decide greenfield or brownfield. Brownfield wraps an existing system as a
  black box that stays untouched.
- Bring one or two backup ideas in case the first is redirected.

### 2. Draft the description and plan (one to two pages)

- **Problem:** what task, who feels the pain today.
- **Solution:** inputs, output shape, decisions the agent makes.
- **Scope:** what is in and what is explicitly out. Brownfield names the
  existing system.
- **Risks:** where the agent can be wrong and the guard for each.
- **Build sketch:** the ADK constructs you expect to use and why. Single agent
  first. Do not promise a multi-agent system.
- OpenSpec is fine if you want the plan in a familiar format.

### 3. Prepare answers to the six architecture questions

- Security, reliability, performance efficiency, cost effectiveness,
  operational excellence, deployment.
- Deployment target is Google Cloud. Treat it as a design question. You will
  not deploy live.

### 4. Read the two sample projects

- Field Report Triage (greenfield) and Pricing Quote Wrapper (brownfield) in
  the lab guide.
- They include the rapid-peer-review skill and the Go/No-Go checklist template
  you will reuse.

### 5. Assign roles (one person each, everyone still codes)

- **Lead.** Owns the plan document, presents it at the approval gate, keeps
  scope in check during the build, and makes the final Go/No-Go call at the
  showcase.
- **Repository owner.** Owns the git repo and branching, keeps `.env` out of
  it, runs the clean-checkout test (`uv sync`, `adk web`) before every
  milestone, and produces the final zip.
- **Evaluation owner.** Owns the eval set or test suite: main path plus at
  least one failure path, the brownfield regression check if applicable, and
  runs the code review into `docs/rapid-peer-review.md`.
- **Deck owner.** Owns the five-minute presentation: the problem, the ADK
  design decisions, the evidence from evaluation, and the Go/No-Go slide.
  Times the rehearsal.
- **Groups of five:** the fifth member is a second developer and backs up the
  evaluation owner.

### 6. Know the deliverables

- Pydantic `output_schema` with validated output.
- An eval set or test suite covering the main path and at least one failure
  path.
- Code review written to `docs/rapid-peer-review.md` with all Fails resolved
  (RAPID ITC.009).
- A Go, No-Go or Conditional Go decision backed by at least two sentences of
  cited evidence (RAPID ITC.004).
- Five-minute presentation, deck, and a runnable repo zip, delivered by
  9:00 AM on Friday 23 October.

### 7. Logistics for the onsite week

- A laptop that can run the lab. FedEx guest WiFi onboarding on the first
  morning.
- AMSA Schiphol, Prestwickweg 1, 1118 LC Schiphol. Class 09:00 to 13:00,
  office hours 14:00 to 16:00 Monday to Thursday.
