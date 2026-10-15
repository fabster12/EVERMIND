# Character Sheet Prompt — "Mind", the EverMind presenter

Save the generated sheet to `docs/brand/mind-character-sheet.png` (per
your instruction — the brand folder, not here). Everything *derived* from
it — the cropped poses, the shot plan, the video build — stays in
`presentation/`.

Colors below are sampled directly from `docs/brand/evermind-icon.jpg`,
not guessed: background `#1E1E54`, line/accent `#D39F32`.

Paste the MAIN PROMPT into Gemini first. Review the full sheet before
requesting individual poses — catching a drift at the sheet stage is one
regeneration; catching it after eight separate pose exports is eight.

---

## MAIN PROMPT (character sheet, all poses)

```
Create a character sheet for "Mind", a presenter character for a corporate
explainer video about an AI knowledge-management system. The character
must visually continue an existing logo: a human head shown in profile,
drawn as a single outlined line, with a small rising line-graph (three dots
connected by two segments, trending up-right) glowing inside the head where
a brain would be. Build a simple, friendly, full character around that
exact head.

STYLE
Flat vector illustration. Clean geometric shapes, no gradients, no
realistic rendering, no 3D, no shading beyond a single soft drop shadow.
One consistent outline weight across every pose. Plain white background
for the sheet itself. The same character must be unmistakably the same
individual in every pose.

COLOR PALETTE (strict, no other colors)
- Deep indigo #1E1E54 — head outline, body, simple rounded torso
- Warm gold #D39F32 — the head's profile-line accent, the internal graph
  line and its three dots, antenna tip if used, mouth line
- White #FFFFFF — eye white, page background
- Light grey — soft drop shadow only, nothing else

ANATOMY
- Head: a human profile silhouette (the nose, brow and jaw bump of a real
  face in outline, not a circle or a robot dome), drawn as a single indigo
  line, facing slightly toward the viewer rather than full side-on, so one
  eye is visible
- Inside the head, faintly visible as if through translucent skin: the
  small gold rising line-graph from the logo (three dots, two upward
  segments), positioned where the temple/forehead is
- One visible eye: white with a small indigo pupil, calm and attentive,
  not cartoonish-large
- Mouth: a short gold line when closed, a small gold oval when open
- No hair, no ears needed, no robot visor, no antenna — this is a person-
  shaped presence, not a machine
- Simple rounded-rectangle indigo torso/shoulders, narrower than the head
- Two simple rounded-capsule arms that pivot at the shoulder
- NO LEGS — floats just above the ground on a soft oval shadow, same
  device as a classic explainer-video mascot
- Proportions: head and shoulders only need to read clearly — this is a
  presenter who appears chest-up in most shots, so leg absence is never
  an issue to compensate for

PERSONALITY TO CONVEY
Calm, precise, quietly confident — a system that understands itself and is
glad to explain it plainly, not a mascot clown or a childish robot. Think
"the clearest person in the room during a technical review," not
"enthusiastic cartoon sidekick." Warm enough to hold a room of VPs for
eight minutes; serious enough that a VP takes the content seriously.

POSES REQUIRED — arrange as a labelled grid, 4 across x 2 down:
1. NEUTRAL — facing forward, calm, mouth closed, hands unseen or relaxed
2. OPENING — one hand raised slightly, mouth open, "let me show you"
3. POINTING — arm extended to the side as if gesturing at a screen or
   chart just out of frame, other hand still, confident
4. CONCERNED — head tilted slightly down, eye narrowed a touch, mouth a
   flat gold line — this is the "here is the problem" pose, not sad, just
   serious
5. REVEALING — both arms open and sweeping outward/up, mouth open, as if
   presenting something just appeared — this is the "here is the answer"
   pose, the opposite energy of pose 4
6. APPROVING — one hand making a small checkmark or thumbs-level gesture,
   slight smile, calm — this is the "a human approved this" pose, central
   to the pitch, must read as endorsement, not celebration
7. THINKING — one hand near the chin, head tilted, the internal graph line
   slightly brighter/larger than at rest, as if visibly working
8. CLOSING — standing straight, both hands loosely open at the sides as if
   inviting a question, warm and settled, mouth in a gentle closed curve

OUTPUT
One image containing all 8 poses in a labelled grid, each pose clearly
separated, all on plain white, all at the same scale and the same
three-quarter viewing angle (never full profile, never full front — the
head must always read as the logo's profile silhouette with one eye
visible). Add a small swatch strip at the bottom showing the three
palette colors with their hex codes: #1E1E54, #D39F32, #FFFFFF.
```

---

## FOLLOW-UP PROMPTS (individual assets)

Run one at a time once the sheet is approved:

```
Using the exact same character, style, palette and three-quarter angle as
the sheet, render ONLY the <POSE NAME> pose. Transparent background. No
label text, no swatches, no grid. Centered, full character including the
shadow, same scale as the sheet.
```

Replace `<POSE NAME>` with: NEUTRAL, OPENING, POINTING, CONCERNED,
REVEALING, APPROVING, THINKING, CLOSING.

Save each to `presentation/assets/mind-<pose>.png` once exported (the
sheet itself stays in `docs/brand/`, per your instruction — these cropped
working poses belong with the video build).

---

## IF THE MODEL DRIFTS

| Problem | Correction |
|---|---|
| Grew legs | "No legs. The character floats above an oval shadow, like the rest of the sheet." |
| Went 3D / glossy | "Flat vector only. No gradients, no highlights, no metallic or glass shading." |
| Became a robot (visor, antenna, metal plates) | "This is a person-shaped presence, not a robot. Remove any visor, antenna, or mechanical seams. Keep the human profile head from the logo." |
| Wrong colors appeared (blue, teal, black) | "Use only #1E1E54 indigo and #D39F32 gold, plus white. No other colors anywhere." |
| Head stopped matching the logo profile | "The head must be the exact profile silhouette from the reference logo — forehead curve, nose, jaw — not a circle or oval." |
| Internal graph line disappeared or moved | "Keep the three-dot rising graph line visible inside the head, in the temple/forehead area, in gold." |
| Poses look like different characters | "Keep head size, torso shape, arm thickness and palette identical to pose 1 across every pose." |
| Went full side-on or full front-on | "Three-quarter angle only, matching the sheet, in every pose." |
| Too cute / oversized eye | "Smaller, calmer eye. A composed adult presenter, not a toy character." |

---

## Where the sheet and poses go

```
docs/brand/
  mind-character-sheet.png     <- the full 8-pose sheet, as you asked

presentation/assets/
  mind-neutral.png             <- cropped individual poses, once approved
  mind-opening.png
  mind-pointing.png
  mind-concerned.png
  mind-revealing.png
  mind-approving.png
  mind-thinking.png
  mind-closing.png
```

See `presentation/IMAGE_BOARD.md` for which pose is used in which scene.
