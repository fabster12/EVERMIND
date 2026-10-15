# Image Board — EverMind VP Pitch (8 minutes)

This is the plan, before any build. Review this before character export,
narration, or `scenes.json` — a wrong beat here costs a sentence to fix;
the same mistake found after rendering costs a re-render.

**Audience: VPs, to sell the concept.** Not the Phase 1 gate deck. This
means money, risk and time saved lead; `output_schema` and Pydantic
validators do not belong on screen. Technical correctness is proven by the
actual capstone build, not by this video — the video sells *why it's
worth building*.

**Format decisions, carried through to the shot plan below:**

| Decision | Why |
| --- | --- |
| 8 minutes, not 10 | Your instruction. VPs are a harder audience to hold than a classroom — every scene below is cut tight on purpose |
| 6 parts (Remotion/HyperFrames pattern) | Each part renders alone; fixing one scene costs ~1-2 min, not a full re-render |
| Character: "Mind," chest-up, floating | See `CHARACTER_SHEET_PROMPT.md`. On screen in every part as the throughline — VPs remember a person explaining, not a slide deck |
| Real numbers throughout | 45 / 59 / 15 / 31, from `proposal.md`. A VP distrusts round numbers in a pitch; exact ones read as "this was actually built," not "this is a mockup" |
| No jargon on screen | "disposition," "`output_schema`," "Pydantic" stay out. "Decides: new, duplicate, or not our job" stays in |

---

## Structure at a glance

| Part | Title | Scenes | Runtime | Carries |
| --- | --- | --- | --- | --- |
| 1 | The Cost of Forgetting | 1–3 | 0:00–1:15 | The problem, felt not explained |
| 2 | What Actually Happens Today | 4–5 | 1:15–2:30 | The 20-minute tax, repeated |
| 3 | Introducing EverMind | 6–8 | 2:30–4:15 | The three-way decision, live |
| 4 | Why a Human Still Approves | 9–11 | 4:15–5:45 | The trust argument — this is the pitch's spine |
| 5 | What It Costs To Not Do This | 12–14 | 5:45–7:00 | The business case, in numbers |
| 6 | The Ask | 15–16 | 7:00–8:00 | What we need from this room |

16 scenes, ~30s average — tighter than the Sage FR reference's 17 scenes
in 7.8 min, because a VP pitch earns a faster cut than an internal
explainer.

---

## Part 1 · The Cost of Forgetting (0:00–1:15)

**Scene 1 — Open on the character, no deck behind them.**
*Mind, pose NEUTRAL, centered on the EverMind indigo background, no logo
yet.*
> "Every support team has a knowledge base. And every knowledge base has
> the same quiet problem: it only knows what somebody thought to write
> down."

**Scene 2 — The forgetting, visualized.**
*A single question mark appears, is answered by a small human silhouette,
then fades to nothing. Beat. The same question mark reappears a week
later. Pose: CONCERNED, watching it happen, arm toward the fading mark.*
> "Someone answers it. Once. By hand. And then it's gone — not written
> down, not remembered. Next week, somebody asks it again."

**Scene 3 — Cost, stated as time, not abstraction.**
*A simple counter: "20 minutes." Then "× every repeat." No chart yet —
just the number, large, gold on indigo.*
> "Twenty minutes, every time, forever. That's not a training problem.
> That's a memory problem."

---

## Part 2 · What Actually Happens Today (1:15–2:30)

**Scene 4 — The real data, shown as real data.**
*A screen-capture-style panel: `query_log.json`, 59 entries, scrolling
past. Pose: POINTING, at the panel.*
> "We looked at fifty-nine real questions a support team's knowledge base
> couldn't answer. Some were genuinely new. Some were the same question,
> asked three different ways. A few, honestly, weren't questions the base
> should ever answer."

**Scene 5 — The reviewer's actual burden.**
*A stack of 59 sticky notes, overlapping, illegible — visual chaos. Pose:
CONCERNED.*
> "Today, a person has to read every single one of these, decide which
> matter, and write the answer — from scratch, under deadline, from
> memory."

---

## Part 3 · Introducing EverMind (2:30–4:15) — the reveal

**Scene 6 — The name and the one-line pitch.**
*Logo/icon appears properly for the first time, full brand reveal. Pose:
REVEALING, both arms open.*
> "This is EverMind. It reads what the knowledge base missed, and it does
> the first pass — so a person reviews a decision, not fifty-nine blank
> pages."

**Scene 7 — The sticky-note chaos resolves into three clean piles.**
*Callback to Scene 5's chaos — the same 59 notes now sort themselves,
live, into three labeled piles: "New," "Already answered," "Not ours to
answer." Pose: PRESENTING, sweeping across the three piles.*
> "It groups the questions that mean the same thing. Fifteen of these
> fifty-nine turn out to be one question asked five different ways —
> that's fifteen reviews that collapse into one."

**Scene 8 — One drafted answer, shown with its source.**
*A single drafted answer card appears, with a visible citation link to a
source document. Pose: THINKING, graph line bright, then settling.*
> "For a genuine gap, it doesn't just flag the question — it drafts the
> answer, and shows exactly which document it came from."

---

## Part 4 · Why a Human Still Approves (4:15–5:45) — the trust argument

This is the part a VP actually needs to believe. Spend the time here.

**Scene 9 — The claim, stated plainly, no hedging.**
*Mind, pose NEUTRAL, direct address — no graphics, just the character.
This is the one scene that should feel like eye contact.*
> "Here's the part that matters most: EverMind never publishes anything.
> Not once. Not automatically, not under any setting."

**Scene 10 — The mechanism, shown structurally, not as a promise.**
*A simple diagram: the system writes to one box labeled "Draft queue."
An arrow from a human figure, separately, to the knowledge base. No line
connects the system directly to the knowledge base — show the absence of
that line as the point.*
> "It isn't a policy we're asking you to trust. There's no code path that
> lets it. The only thing it ever writes is a list for a person to read."

**Scene 11 — The approval, warmly, as the payoff.**
*A human hand/silhouette clicks "approve" on the drafted card from Scene
8. The card moves into the knowledge base visual. Pose: APPROVING.*
> "A person reads it, checks the source, and decides. That's the only way
> anything this system finds ever reaches a customer."

---

## Part 5 · What It Costs To Not Do This (5:45–7:00) — the business case

**Scene 12 — Reframe the 20 minutes from Scene 3, now with scale.**
*The "20 minutes" number returns, multiplied visibly: "× 59 questions
this month alone."*
> "Fifty-nine questions, one month, one team. That repeats every month,
> on every team with a knowledge base — which is every support
> organization you have."

**Scene 13 — What stays exactly the same.**
*Side-by-side: "knowledge base" box, unchanged, with a small padlock icon.
Pose: NEUTRAL, gesturing at the unchanged box.*
> "Nothing about your knowledge base changes. No migration, no new
> system of record. This reads what you already have and hands a person
> a head start."

**Scene 14 — The honest limit, stated before anyone asks.**
*A drafted answer with NO source attached — shown explicitly declining.*
> "And when it can't find a real answer, it says so. It doesn't guess.
> An answer with no source isn't a weak answer here — it's one the
> system refuses to produce."

---

## Part 6 · The Ask (7:00–8:00)

**Scene 15 — What exists today, honestly.**
*Pose: NEUTRAL, calm, closing register begins.*
> "This is a working capstone project, built from real support questions,
> with every decision it makes already defined and tested against known
> answers — not a concept on a slide."

**Scene 16 — The ask, and the close.**
*Pose: CLOSING. Logo lingers. Fade.*
> "We're not asking you to change how your team works. We're asking for
> the chance to run this against one real knowledge base, and show you
> the twenty minutes back. That's EverMind."

---

## What this board deliberately leaves out

- **No architecture, no `LlmAgent`, no tool names.** A VP does not buy a
  topology. If asked, that conversation happens after this video, in the
  design document.
- **No mention of ADK, Gemini, or the model.** Technology choice is not
  the pitch; outcome is. Naming it invites a VP to compare vendors instead
  of approving a concept.
- **No fabricated ROI dollar figure.** The proposal has real counts (45 /
  59 / 15 / 31) but no cost-per-ticket number on record. Inventing one for
  a VP pitch and having it challenged in the room is worse than the 20-
  minutes framing, which is stated as a given in `proposal.md`'s own
  problem statement and needs no invented backing.

## Next steps, in order

1. Generate and approve the character sheet (`CHARACTER_SHEET_PROMPT.md`)
   → `docs/brand/mind-character-sheet.png`.
2. Export and crop the 8 poses into `presentation/assets/`.
3. Write `presentation/scenes.json` from this board — one entry per scene
   above, matching the Sage FR schema (`kind`, `part`, `narration`).
4. Narrate, measure, build, snapshot for review **before** any full-length
   render — exactly the Sage FR order in that project's `README.md`.
