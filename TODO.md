# TODO

Open items and handoff notes. Newest first. Tick items off rather than
deleting them, so the reasoning survives until the change is archived.

---

## 1. The design document still says three agents — FIX FIRST

**Status:** open · **Raised:** 15 Oct 2026 · **Do:** Friday 16 Oct, before
anything else

### What is wrong

`proposal.md` and `docs/architecture.png` were rewritten on 15 October to
show **one `LlmAgent`** that calls tools and emits the output schema. The
7-page design document was explicitly out of scope for that review, so it
was left alone — and it still presents **a `SequentialAgent` of three
specialists as the design**.

The two documents now contradict each other. An instructor reading both
sees two different architectures.

| File | Says | Correct? |
| --- | --- | --- |
| `src/openspec/changes/add-evermind-pipeline/proposal.md` | One agent, split as fallback | yes |
| `docs/architecture.png` | One agent, contingency panel | yes |
| `src/openspec/changes/add-evermind-pipeline/design.md` | Topology marked **OPEN** | partly — see item 2 |
| **`FedEx-Capstone-Design-EverMind.docx` / `.pdf`** | **Three agents, as the design** | **no** |

### Why it is wrong

The WA3922-CAP lab guide, in the Phase 2 escalation section:

> One LlmAgent can call tools and emit an output_schema at the same time. In
> ADK 2.x the agent runs its tools during its reasoning and enforces the
> schema on its final answer. (ADK 1.x couldn't do this and forced you to
> split the work across two agents joined by a SequentialAgent.) Reach for a
> workflow only when you have genuinely separate steps, not to work around a
> limit that's gone. **Both samples below are single agents.**

We designed around a limit the course says was removed — and the lab names
the exact workaround we had reinvented.

The WA3915 caveat we were citing is still true: *"Combining output_schema
with tools is limited. Only some models support both at once."* Both
statements hold. That makes the split **a contingency to plan for, not a
topology to commit to before the gate** — which is also what the capstone
handout asks for: *"Single agent first. Do not promise a multi-agent
system."*

### What to change

Edit `tools/build_design_evermind.py`, then rebuild. Do not edit the
`.docx` by hand — it is generated, and a hand edit is lost on the next run.

- [ ] **Section 5, opening line** (~line 307): "A SequentialAgent of three
      specialists, with deterministic clustering in front" → one `LlmAgent`
      that calls three read-only tools and emits the schema, with
      deterministic grouping in front.
- [ ] **Section 5, heading** (~line 318): "Why three agents and not one" →
      "Why one agent, and when we would split". Rewrite the paragraph: ADK
      2.x supports the combination, both capstone samples are single agents,
      and the WA3915 caveat is the reason we have a planned exit rather than
      the reason we start split.
- [ ] **Section 5, step table** (~line 327): the three-row Triage / Research
      / Drafting table becomes a short contingency note. Keep the fallback
      visible — it is good planning — but as an escalation, not the design.
- [ ] **ADK constructs table** (~line 349): drop the `SequentialAgent` row
      and `LlmAgent x3` → one `LlmAgent` with `output_schema`. Keep the
      three `FunctionTool`s, `ToolContext`/`session.state`, the callbacks
      and the plugin. Mark sub-agents and A2A **not applicable for now**.
- [ ] **Section 7, Reliability** (~line 459): "Splitting the pipeline into
      three agents is itself a reliability decision" — remove. Replace with
      the validator as the reliability boundary, and the batch/retry
      argument that is already in the proposal.
- [ ] Rebuild and convert:
      `python tools/build_design_evermind.py` then
      `powershell -ExecutionPolicy Bypass -File tools/packaging/to_pdf.ps1`
- [ ] **Verify:** `grep -n "SequentialAgent\|three agents\|three specialists" tools/build_design_evermind.py`
      returns nothing outside a contingency note, and the rebuilt PDF is
      still 7 pages or fewer.
- [ ] Rebuild the share packages afterwards: `python tools/packaging/build_packages.py`
      (both zips carry the design PDF).

---

## 2. `design.md` carries the old reasoning

**Status:** open · **Do:** same sitting as item 1 · **Size:** two sentences

`src/openspec/changes/add-evermind-pipeline/design.md` marks the topology
**OPEN**, so it does not contradict the proposal the way the `.docx` does.
But its reasoning predates the review: it presents the split as "the lesson
guide's own recommendation" with no counterweight, and it does not know ADK
2.x removed the limit.

- [ ] In *Agent topology — OPEN*, add that ADK 2.x supports tools and
      `output_schema` on one agent and that both capstone samples are single
      agents, so the single agent is the starting point and the split is the
      exit if our model will not carry both.
- [ ] Keep the fallback table. It is useful: if the single agent fails on
      Tuesday morning, nobody spends the afternoon rediscovering the fix.

---

## 3. The summary `.docx` was stale when EVERMIND was assembled

**Status:** open · **Do:** any time Word is closed · **Size:** one command

`FedEx-Capstone-Summary-Group1.docx` still says "FAQ Foundry". It was locked
by an open Word window (PID 30572) through the whole rename, so every
rebuild failed with `PermissionError`.

The `.md` and `.pdf` are current, and `.docx` is no longer committed at all
(see `.gitignore`), so nothing stale ships. Regenerate it when you next need
to edit in Word.

- [ ] Close Word.
- [ ] `python tools/build_summary_group1.py`
- [ ] Confirm: `grep -c EverMind` on the rebuilt file, and no `~$` lock file
      left in the folder.

---

## 4. Proposal length — a judgement call to confirm

**Status:** needs a decision Monday · **Owner:** Yasin, at the gate

The handout asks for "one to two pages". `proposal.md` is about four
printed. That was deliberate: the six architectural answers alone run a
page, and the lab's own sample projects are worked out in comparable depth.

- [ ] If the instructor is strict on length: move the architecture
      considerations table into `design.md` and leave a one-line pointer.
      That lands the proposal at two pages and takes a minute. Do not
      pre-emptively cut it — the content is required somewhere, and it reads
      better where it is.

---

## 5. Smaller items

- [ ] **Deck owner is unassigned.** Agree Monday morning. Yasin leads,
      Fabian has the repo, Siva and Fabian share evaluation.
- [ ] **Fixture counts are load-bearing and untested.** The proposal and the
      contract both cite 45 / 59 / 15 / 31. Verified by hand today, but
      nothing asserts the documents match the data. If the seed changes the
      docs go quietly wrong. Worth a CI check during the build, not before
      the gate.
- [ ] **Credentials in git history.** `scribbles/FDE01.md` is tracked and
      pushed (commit `7d795da`) with live lab keys in it. The repo is
      private, so it is not urgent, but scrubbing it needs a history rewrite
      and a force-push. Fabian's call, not something to do mid-capstone.

---

## Done

- **15 Oct** — Renamed FAQ Foundry → EverMind across all documents, the
  change folder, the diagram and the packages.
- **15 Oct** — Restructured Gate 1 into the four OpenSpec artifacts
  (`proposal.md`, `design.md`, `tasks.md`, four delta specs with 21
  Given/When/Then scenarios). Previously one file doing all four jobs.
- **15 Oct** — Benchmarked `proposal.md` and `architecture.png` against all
  four course guides; rewrote both. Findings in
  `docs/EverMind-Proposal-Review.pdf`.
- **15 Oct** — Simplified the instructor summary: removed the premature
  technical commitments, made the architecture table business-oriented.
  4 pages → 3.
- **15 Oct** — Two share packages in `dist/`, split docs from tech, both
  integrity-checked and scanned for credentials.
