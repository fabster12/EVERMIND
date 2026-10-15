# EverMind — VP pitch video

An 8-minute video selling the EverMind concept to VPs. **Separate from the
Phase 1 gate deliverables** — this is not the 5-minute instructor
presentation; it exists to get leadership buy-in on the idea.

Modeled on the build in `C:\SRC\FDX\ARCHIVAL\55_SAGE_FR\video\` — same
tool (HyperFrames: HTML/CSS compositions rendered frame-by-frame through
headless Chrome to MP4, not raw canvas-to-ffmpeg), same six-part structure
so one scene re-renders in ~1-2 minutes instead of the whole film, same
review gate (snapshot every scene before a full render).

## Read these in order

1. **`CHARACTER_SHEET_PROMPT.md`** — the Gemini prompt for "Mind," the
   presenter character. Built from `docs/brand/evermind-icon.jpg`'s actual
   sampled colors (`#1E1E54` / `#D39F32`), not a new palette.
2. **`IMAGE_BOARD.md`** — the full 16-scene plan, 6 parts, before any
   build. What's on screen, what's said, and why each beat is there. Read
   this before writing `scenes.json` — it's the thing to argue with now,
   while changing it costs a sentence.

## Status

| Step | State |
| --- | --- |
| Character prompt | done — awaiting your Gemini generation |
| Image board / scene plan | done — awaiting your review |
| Character sheet image | not yet generated |
| `scenes.json` | not started |
| Narration | not started |
| Build / render | not started |

## Folder layout (fills in as the build progresses)

```
presentation/
├── README.md                    this file
├── CHARACTER_SHEET_PROMPT.md    the Gemini prompt
├── IMAGE_BOARD.md               the 16-scene plan
├── scenes.json                  not yet written
├── assets/                      cropped character poses, logo, UI shots
├── audio/                       narration .wav per scene, once recorded
├── shots/                       any screen captures used as backdrops
├── renders/                     final .mp4 / .srt output
└── snapshots/                   one still per scene - the review gate
```

The character sheet itself (`mind-character-sheet.png`) goes in
`docs/brand/`, per instruction — it's a brand asset, not a video working
file. Everything derived from it for the video lives here.

## Why this is a separate track from the capstone build

The capstone rule — no agent code before the Phase 1 gate — does not apply
here; nothing in this folder is agent code. But the content does lean on
real numbers from `src/openspec/changes/add-evermind-pipeline/proposal.md`
(45 / 59 / 15 / 31, the three-way disposition), so if that document
changes before the gate, re-check `IMAGE_BOARD.md` scenes 4, 7 and 12
against it.
