# Assets to generate — diagram, code mockup, terminal mockup

Exact content for the three new visuals `IMAGE_BOARD.md` rev 2 calls for
(Scenes 4, 6, 7, 8). Each is built as an HTML/CSS composition — same
approach as the rest of the video, not a separate image tool — so it
animates natively inside HyperFrames and needs no external screenshot
step. Every field name and number below is copied from `proposal.md`, not
invented.

---

## 1. Concept diagram (Scene 4) — moving

**Build as:** one HTML composition, six boxes in a horizontal flow, each
with a `data-active` CSS class that HyperFrames keyframes on/off in
sequence, plus a connecting line that draws itself (stroke-dashoffset
animation) ahead of the active box.

```
[Questions log] -> [Group similar] -> [New / duplicate / not ours?]
                                              |
                                              v
                                    [Draft, with source]
                                              |
                                              v
                                    [Human approves] -> [Knowledge base]
```

**Box labels, exact text:**

| Box | Label | Sub-label (smaller, under) |
| --- | --- | --- |
| 1 | Questions log | "59 unanswered questions" |
| 2 | Group similar | "same question, asked differently" |
| 3 | Three-way check | "new · already answered · not ours" |
| 4 | Draft, with source | "cites a real document, or declines" |
| 5 | Human approves | "the only way anything moves forward" |
| 6 | Knowledge base | "unchanged until a person says so" |

**Color:** boxes 1–4 in indigo `#1E1E54` outline, gold `#D39F32` fill on
`data-active`. Box 5 (the human step) gets a visually distinct treatment —
a thin gold border, no fill — so the human gate reads as categorically
different from the automated boxes either side of it. Box 6 is drawn with
a small padlock glyph to foreshadow Scene 10's "nothing writes here
automatically."

**Timing:** each box activates for ~1.2s, overlapping narration from
Scene 4's script. Final frame holds all six lit, full flow visible, for
the last ~2s of the scene.

---

## 2. VS Code mockup (Scene 7)

**Build as:** an HTML composition styled to match VS Code's Dark+ theme
exactly — title bar, activity bar icons (static, decorative), file tree,
tab bar, editor with real syntax highlighting (use Prism.js or Shiki,
already permitted CDN sources), minimap optional.

**File tree shown (left panel), matching the real `src/` layout:**

```
EVERMIND
└── src
    └── evermind
        ├── agent.py
        ├── tools.py
        ├── schemas.py      <- open, highlighted in the tree
        └── guardrails.py
```

**Open file:** `schemas.py`. **Exact code content** (this is the mockup —
real field names and constraints from `proposal.md`, illustrative
implementation, never claimed as the shipped file):

```python
from pydantic import BaseModel, Field
from typing import Literal

class FAQCandidate(BaseModel):
    """One reviewable decision for one group of similar questions."""

    gap_id: str
    representative_question: str
    cluster_size: int

    disposition: Literal[
        "HUMAN_REVIEW",
        "DUPLICATE_OF_EXISTING",
        "REJECT_OUT_OF_SCOPE",
    ]

    proposed_answer: str | None = Field(
        default=None, max_length=150,
        description="Only set when disposition is HUMAN_REVIEW.",
    )
    source_citations: list[str] = Field(default_factory=list)

    confidence: float = Field(ge=0.0, le=1.0)
    reason: str

    def model_post_init(self, __context) -> None:
        # An answer with no citation is not a weak answer.
        # It is not a valid object, and never reaches a reviewer.
        if self.proposed_answer and not self.source_citations:
            raise ValueError("an answer must cite at least one source")
```

**On-screen annotation** (a small callout box overlaying the editor, not
part of the code itself): *"Every field is checked before a draft can
exist — this isn't a style guide, it's enforced."*

**Status bar text** (bottom of the mock window, decorative):
`Python 3.12 · EverMind · src/evermind/schemas.py`

---

## 3. Terminal / JSON output mockup (Scene 8)

**Build as:** an HTML composition styled as a dark terminal panel
(monospace, green/white-on-black or VS Code's integrated-terminal dark
theme — match whichever reads better against Scene 7's editor for visual
continuity).

**Sequence, typed-on animation (character-by-character or fast line-reveal):**

```
$ run the review batch

Grouping 59 questions ... 12 groups found
Checking against the knowledge base ... 
Retrieving supporting sources ...
Drafting candidates ...

Wrote 12 candidates to review_queue.json
```

**Then, below, a single formatted JSON object fades/scrolls in** (this is
the payoff shot — hold it longer than the lines above):

```json
{
  "gap_id": "GAP-Q005",
  "representative_question": "If I ship DDP, who gets the duty bill?",
  "cluster_size": 3,
  "disposition": "HUMAN_REVIEW",
  "proposed_answer": "Under DDP terms, the shipper is billed for duty, tax and the associated handling fee.",
  "source_citations": ["SRC-02-P2"],
  "confidence": 0.87,
  "reason": "Supported by one trusted source; no conflicting guidance found."
}
```

**Not invented.** This is a real fixture: `query_log.json` has
`Q-005` — *"If I ship DDP, who gets the duty bill?"* — labelled
`expected_disposition: HUMAN_REVIEW`, `expected_source: SRC-02`. The cited
passage `SRC-02-P2` in `sources.json` reads *"Under DDP terms the shipper
is billed for duty, tax and the associated handling fee"* — the
`proposed_answer` above is that passage, lightly reworded, which is
exactly the cite-or-reject behaviour the system is supposed to produce.
`gap_id: GAP-Q005` is a readable label built from the real query id,
since the pipeline's actual gap-id scheme doesn't exist until Tuesday.

This mockup is therefore not an invented example — it's what the system
*should* output for a question that is already in the fixtures, which is
a stronger claim for the pitch than a number made up for the slide.

**On-screen annotation:** *"One decision. One source. Ready to check in
under a minute."*

---

## Build order

1. Diagram first — it's reused conceptually in Scene 10 (same visual
   language, different emphasis), so get the box/line style right once.
2. VS Code mock — static-ish, lowest risk.
3. Terminal mock — depends on the diagram's color language for the
   JSON syntax highlighting to feel like the same product.

All three are plain HTML/CSS/JS compositions dropped into
`presentation/assets/` as `.html` files, referenced from `scenes.json`
exactly the way the character PNGs are — no separate screenshot tool, no
headless browser step outside the normal HyperFrames render pipeline.
