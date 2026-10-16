# Image Board — EverMind VP Pitch (6 minutes)

Revision 2 — cut from 8 to 6 minutes, added screenshots/diagram/code and a
reworded OpenSpec beat. The 8-minute version is kept at
`IMAGE_BOARD.md.bak-8min` for reference; nothing below depends on it.

This is the plan, before `scenes.json`. Review before narration or build —
a wrong beat here costs a sentence; the same mistake after rendering costs
a re-render.

**Audience: VPs, to sell the concept.** Money, risk, and time saved lead.
`output_schema` and Pydantic validators do not belong on screen *as
jargon* — but the code mockup in Part 3 shows them as evidence of rigor,
labelled in plain language, which is different from naming them in the
narration.

**Format, carried through below:**

| Decision | Why |
| --- | --- |
| 6 minutes, 13 scenes, 5 parts | Your instruction. Tighter than the 8-min cut — Part 4 (trust) kept in full; Parts 1 and 5 compressed |
| Character "Mind" present throughout | Poses confirmed delivered: neutral, opening, pointing, concerned, revealing, approving, thinking, closing — all 8 used below |
| Fake screenshots, clearly mockups | VS Code panel + terminal/JSON output, styled real, built from `proposal.md`'s actual field names — not claiming to be a running system. See `ASSETS_TO_GENERATE.md` |
| OpenSpec reworded | VPs don't need the word "OpenSpec." They need "we didn't start coding from a guess" — see Scene 9 |
| Real numbers throughout | 45 / 59 / 15 / 31, from `proposal.md`. Exact numbers read as "this was built," not "this is a mockup" |

---

## Structure at a glance

| Part | Title | Scenes | Runtime | Carries |
| --- | --- | --- | --- | --- |
| 1 | The Cost of Forgetting | 1–2 | 0:00–0:45 | The problem, felt not explained |
| 2 | Introducing EverMind | 3–5 | 0:45–2:00 | The three-way decision, live, with the diagram |
| 3 | How It's Actually Built | 6–8 | 2:00–3:30 | Screenshots, code, the planning process — the "this is real" beat |
| 4 | Why a Human Still Approves | 9–11 | 3:30–5:00 | The trust argument — the pitch's spine, unchanged from rev 1 |
| 5 | The Ask | 12–13 | 5:00–6:00 | Business case, compressed, then close |

13 scenes, ~28s average.

---

## Part 1 · The Cost of Forgetting (0:00–0:45)

**Scene 1 — Open on the character.**
*Mind, pose NEUTRAL, centered, no logo yet.*
> "Every support team has a knowledge base. And every knowledge base has
> the same quiet problem: it only knows what somebody thought to write
> down."

**Scene 2 — The forgetting, visualized, cost stated immediately.**
*A question mark appears, is answered by a human silhouette, fades.
Reappears. Then: "20 minutes. Every repeat." Pose: CONCERNED.*
> "Someone answers it by hand. It's not written down. Next week, somebody
> asks it again — another twenty minutes, gone, forever."

*(Scenes 2 and 3 from rev 1 merged — the chart of accumulating cost moved
to Scene 12, where it does more work next to the real fixture numbers.)*

---

## Part 2 · Introducing EverMind (0:45–2:00)

**Scene 3 — The name and the one-line pitch.**
*Logo reveal. Pose: REVEALING.*
> "This is EverMind. It reads what the knowledge base missed, and does the
> first pass — so a person reviews a decision, not a pile of raw
> questions."

**Scene 4 — The concept diagram, moving.**
*Full-screen animated diagram (see `ASSETS_TO_GENERATE.md` for build spec):
boxes for "Questions log," "Group similar," "Check: new / duplicate / not
ours," "Draft with source," "Human approves," "Knowledge base" — each box
lighting up in sequence as a line traces through them. This is the
"concept in diagram, moving" ask. Pose: Mind stands beside the diagram,
pose POINTING, tracking the active box.*
> "Here's the whole idea in one picture. Questions come in, get grouped,
> get sorted into three outcomes, and only ever reach your knowledge base
> after a person signs off."

**Scene 5 — One drafted answer, with its source.**
*A single drafted-answer card appears, citation visible. Pose: THINKING,
graph line bright, then settling.*
> "For a genuine gap, it doesn't just flag the question — it drafts the
> answer, and shows exactly which document it came from."

---

## Part 3 · How It's Actually Built (2:00–3:30) — new in rev 2

This is the "prove it's real, not a slide" section. Three beats: what we
planned before coding, what the plan looks like as code, what it actually
outputs.

**Scene 6 — The planning process, VP-worded.**
*A simple document stack animates into place: "What problem" →
"What it must do" → "How we'll build it" → "What order." Pose: Mind,
pose NEUTRAL, gesturing at the stack as it builds.*
> "Before writing a line of code, we wrote down exactly what this system
> must do — and what it must never do — and had that reviewed before the
> build started. Same discipline any engineering organization uses before
> committing resources: agree the requirements, then build to them."
>
> *(This is the OpenSpec beat, reworded. No mention of "OpenSpec,"
> "proposal.md," or "specs/" on screen or in narration — see
> `ASSETS_TO_GENERATE.md` for exactly what text appears in the stack.)*

**Scene 7 — Fake VS Code screenshot: the code mockup.**
*A styled, realistic VS Code window — dark theme, file tree on the left
showing a plausible project layout, an editor pane with syntax-highlighted
Python matching the proposal's actual field names. Pose: Mind small,
corner of frame, pose POINTING at the screen.*
> "What a reviewed decision looks like in code: every answer the system
> drafts has to carry its source, its confidence, and a reason — or it
> doesn't get created at all."
>
> *(Exact mock code is in `ASSETS_TO_GENERATE.md` — a `FAQCandidate`
> class with the real field names from `proposal.md`, clearly a mockup,
> never claimed as the actual shipped file.)*

**Scene 8 — Fake terminal/JSON screenshot: the output.**
*A styled terminal panel showing a realistic run: a progress line, then a
formatted JSON `FAQCandidate` object — `disposition: "HUMAN_REVIEW"`, a
drafted answer, a `source_citations` array. Pose: Mind, pose REVEALING.*
> "And this is what comes out the other side — one reviewable decision
> per gap, ready for a person to check in under a minute."

---

## Part 4 · Why a Human Still Approves (3:30–5:00) — unchanged from rev 1

This is the part a VP actually needs to believe. Full length kept.

**Scene 9 — The claim, stated plainly.**
*Mind, pose NEUTRAL, direct address, no graphics.*
> "Here's the part that matters most: EverMind never publishes anything.
> Not once. Not automatically, not under any setting."

**Scene 10 — The mechanism, shown structurally.**
*Diagram: the system writes to one box, "Draft queue." A separate arrow,
from a human figure only, reaches the knowledge base. No line connects the
system directly to it — the absence is the point.*
> "It isn't a policy we're asking you to trust. There's no path in the
> code that lets it. The only thing it ever writes is a list for a person
> to read."

**Scene 11 — The approval, as the payoff.**
*A human hand/silhouette approves the Scene 5 card; it moves into the
knowledge base visual. Pose: APPROVING.*
> "A person reads it, checks the source, and decides. That's the only way
> anything this system finds ever reaches a customer."

---

## Part 5 · The Ask (5:00–6:00) — compressed from rev 1's Parts 5–6

**Scene 12 — Scale and the honest limit, combined.**
*The "20 minutes" from Scene 2 returns: "× 59 questions, one month, one
team." Then, immediately after: a drafted card with NO source attached,
explicitly declining. Pose: CONCERNED, then NEUTRAL.*
> "Fifty-nine questions, one team, one month — and that repeats on every
> team you have. When it can't find a real answer, it says so. An answer
> with no source isn't a weak answer here — it's one the system refuses
> to produce."

**Scene 13 — The ask, and the close.**
*Pose: CLOSING. Logo lingers. Fade.*
> "This is a working project, built from real support questions, with
> every decision it makes already defined and tested against known
> answers. We're asking for the chance to run it against one real
> knowledge base, and show you the twenty minutes back. That's EverMind."

---

## What this board still deliberately leaves out

- **No "OpenSpec," "ADK," "Gemini," or model name**, anywhere on screen or
  in narration. Scene 6 describes the *discipline* ("agree requirements,
  then build"), never the tool name — a VP doesn't buy a process name, and
  naming the specific framework invites a vendor-comparison tangent this
  pitch doesn't need.
- **No fabricated ROI dollar figure.** Scene 12 uses the 20-minutes figure
  that's actually in `proposal.md`'s own problem statement.
- **The code and terminal mockups are never claimed as the live system.**
  Both are built to *look* real and to carry the actual field names from
  `proposal.md`, which is what makes them credible — but nothing in the
  narration says "here it is running." See `ASSETS_TO_GENERATE.md` for the
  exact text in each, so no one can later say the video overclaimed.

## Next steps, in order

1. ~~Character sheet~~ — done, approved.
2. ~~Cropped poses~~ — done, all 8 present in `presentation/assets/`.
3. Build the three new visual assets per `ASSETS_TO_GENERATE.md`: the
   moving concept diagram, the VS Code mockup, the terminal/JSON mockup.
4. Write `presentation/scenes.json` from this board.
5. Narrate (Kokoro, voice `am_michael`, confirmed working), measure, build,
   snapshot for review **before** any full-length render.
