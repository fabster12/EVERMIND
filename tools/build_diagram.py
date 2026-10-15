"""Draw the EverMind architecture diagram as a PNG.

Usage:  python build_diagram.py [output.png]

The diagram carries what the Phase 1 reviewer is checking, in their order:

  1. the inputs, and that no FedEx system is read
  2. one LlmAgent that calls tools AND emits the output_schema - the ADK 2.x
     shape both capstone samples use
  3. the output schema, concretely enough to validate
  4. a risk-to-guard band, because the gate asks "the risks are real and
     have guards"
  5. the human approval step, outside the agent
  6. the escalation path, shown small and dashed - a contingency, not the
     design. The WA3915 guide flags output_schema-plus-tools as
     model-dependent, so the fallback is planned but not promised.

The previous version drew a three-agent SequentialAgent as the design. That
over-committed before the gate and contradicted the capstone lab, which is
explicit that ADK 2.x removed the limit that used to force the split.

Rendered at 3x and downsampled: clean edges and readable text in Word and in
print, with no anti-aliasing library.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "architecture.png"

S = 3                      # supersampling factor
W, H = 1240, 880           # final size in px

PURPLE = (0x4D, 0x14, 0x8C)
ORANGE = (0xFF, 0x66, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
INK = (0x1A, 0x1A, 0x1A)
GREY = (0x59, 0x59, 0x59)
LIGHT = (0x76, 0x76, 0x76)
TINT = (0xF2, 0xEE, 0xF7)
FIXTURE = (0xEC, 0xEC, 0xF1)
RULE = (0xD9, 0xD2, 0xE4)
GREEN = (0x1E, 0x7A, 0x3C)
GREEN_BG = (0xF0, 0xF7, 0xF2)
AMBER = (0xB5, 0x6E, 0x00)
RED = (0xB3, 0x26, 0x1E)

FONTS = "C:/Windows/Fonts/"


def _f(name, size):
    return ImageFont.truetype(FONTS + name, int(size * S))


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill, anchor=anchor)


def box(d, x, y, w, h, fill, outline, width=2, radius=8, dash=False):
    xy = [x * S, y * S, (x + w) * S, (y + h) * S]
    if dash:
        d.rounded_rectangle(xy, radius=radius * S, fill=fill)
        _dashed_rect(d, x, y, w, h, outline, width)
    else:
        d.rounded_rectangle(xy, radius=radius * S, fill=fill,
                            outline=outline, width=width * S)


def _dashed_rect(d, x, y, w, h, colour, width, dash=9, gap=6):
    edges = [((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)),
             ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))]
    for (x1, y1), (x2, y2) in edges:
        length = max(abs(x2 - x1), abs(y2 - y1))
        steps = int(length // (dash + gap)) or 1
        dx, dy = (x2 - x1) / steps, (y2 - y1) / steps
        frac = dash / (dash + gap)
        for i in range(steps):
            sx, sy = x1 + dx * i, y1 + dy * i
            d.line([sx * S, sy * S, (sx + dx * frac) * S, (sy + dy * frac) * S],
                   fill=colour, width=width * S)


def arrow(d, x1, y1, x2, y2, colour=PURPLE, width=3, head=10):
    d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=colour, width=width * S)
    ang = math.atan2(y2 - y1, x2 - x1)
    for sign in (+1, -1):
        a = ang + sign * math.radians(26)
        d.line([x2 * S, y2 * S,
                (x2 - head * math.cos(a)) * S, (y2 - head * math.sin(a)) * S],
               fill=colour, width=width * S)


def build(path):
    img = Image.new("RGB", (W * S, H * S), WHITE)
    d = ImageDraw.Draw(img)

    f_title = _f("arialbd.ttf", 19)
    f_sub = _f("arial.ttf", 11)
    f_zone = _f("arialbd.ttf", 11)
    f_box = _f("arialbd.ttf", 12)
    f_sm = _f("arial.ttf", 9.5)
    f_xs = _f("arial.ttf", 8.5)
    f_lbl = _f("arialbd.ttf", 9.5)
    f_mono = _f("consolab.ttf", 9)
    f_monos = _f("consola.ttf", 8.5)

    # ---- title -----------------------------------------------------------
    text(d, (40, 24), "EverMind - agent architecture", f_title, PURPLE)
    text(d, (40, 50), "One LlmAgent calls read-only tools and emits a validated schema. "
                      "Grouping is deterministic; publishing is human.", f_sub, GREY)
    d.line([40 * S, 74 * S, (W - 40) * S, 74 * S], fill=ORANGE, width=3 * S)

    # ---- fixture layer ---------------------------------------------------
    box(d, 40, 96, 236, 286, FIXTURE, LIGHT, width=2, dash=True)
    text(d, (56, 107), "SEEDED FIXTURES", f_zone, GREY)
    text(d, (56, 123), "build_fixtures.py, one seed", f_xs, LIGHT)

    for i, (title, line1, line2) in enumerate([
        ("faq_store.json", "45 entries. The knowledge", "base we grow. Read-only."),
        ("query_log.json", "59 unanswered questions,", "each labelled - the key."),
        ("sources.json", "15 docs, 31 passages. The", "only citable evidence."),
    ]):
        y = 146 + i * 78
        box(d, 58, y, 200, 64, WHITE, LIGHT, width=2)
        text(d, (72, y + 10), title, f_box, INK)
        text(d, (72, y + 29), line1, f_xs, GREY)
        text(d, (72, y + 43), line2, f_xs, GREY)

    text(d, (158, 392), "No FedEx system is read. The fixtures are the system.", f_xs, GREY, anchor="ma")

    # ---- deterministic pre-step -----------------------------------------
    box(d, 310, 120, 168, 96, WHITE, PURPLE, width=2)
    text(d, (325, 132), "Grouping", f_box, PURPLE)
    text(d, (325, 152), "Plain Python, before", f_xs, GREY)
    text(d, (325, 166), "any model call.", f_xs, GREY)
    text(d, (325, 184), "59 questions -> ~12", f_xs, INK)
    text(d, (325, 198), "groups. Unit-tested.", f_xs, GREY)

    arrow(d, 278, 230, 306, 190, PURPLE)
    arrow(d, 394, 220, 394, 252, PURPLE)
    text(d, (406, 229), "one group at a time", f_xs, GREY)

    # ---- the agent -------------------------------------------------------
    ax, ay_, aw, ah = 310, 256, 470, 240
    box(d, ax, ay_, aw, ah, TINT, PURPLE, width=2)
    text(d, (ax + 16, ay_ + 12), "LlmAgent  -  evermind", f_zone, PURPLE)
    text(d, (ax + 16, ay_ + 29), "Calls tools during reasoning, enforces the schema on its "
                                 "final answer.", f_xs, GREY)

    text(d, (ax + 16, ay_ + 54), "TOOLS  (read-only)", f_lbl, PURPLE)
    tools = [
        ("search_faq_db(q)", "Does an entry already answer this?"),
        ("classify_scope(q)", "Should we answer it at all?"),
        ("search_sources(topic)", "Retrieve citable passages."),
    ]
    for i, (sig, why) in enumerate(tools):
        y = ay_ + 74 + i * 42
        box(d, ax + 16, y, aw - 32, 36, WHITE, RULE, width=2, radius=6)
        text(d, (ax + 28, y + 7), sig, f_mono, INK)
        text(d, (ax + 28, y + 21), why, f_xs, GREY)

    text(d, (ax + 16, ay_ + 206), "No write function exists in the package, so no model",
         f_xs, GREY)
    text(d, (ax + 16, ay_ + 220), "decision can publish. Least privilege by construction.",
         f_xs, GREY)

    # ---- output schema ---------------------------------------------------
    ox, oy, ow, oh = 812, 256, 388, 240
    box(d, ox, oy, ow, oh, WHITE, PURPLE, width=2)
    text(d, (ox + 16, oy + 12), "output_schema  -  FAQCandidate", f_zone, PURPLE)
    text(d, (ox + 16, oy + 29), "Pydantic model. Validated, never free text.", f_xs, GREY)

    fields = [
        ("disposition", "HUMAN_REVIEW | DUPLICATE | REJECT"),
        ("proposed_answer", "<=150 words, None unless gap"),
        ("source_citations", ">=1 whenever an answer exists"),
        ("confidence", "0.0-1.0"),
        ("reason", "required on refuse / duplicate"),
    ]
    for i, (f, c) in enumerate(fields):
        y = oy + 52 + i * 28
        text(d, (ox + 16, y), f, f_mono, INK)
        text(d, (ox + 150, y + 1), c, f_xs, GREY)

    box(d, ox + 16, oy + 196, ow - 32, 30, (0xFD, 0xF3, 0xF2), RED, width=2, radius=6)
    text(d, (ox + 28, oy + 203), "Cite-or-reject: an answer with no citation is not a weak",
         f_xs, RED)
    text(d, (ox + 28, oy + 215), "answer, it is an invalid object. It never reaches a reviewer.",
         f_xs, RED)

    arrow(d, ax + aw + 1, 376, ox - 1, 376, PURPLE)
    text(d, (796, 362), "emits", f_xs, GREY, anchor="ma")

    # ---- risks -> guards -------------------------------------------------
    ry = 540
    box(d, 310, ry, 890, 108, WHITE, PURPLE, width=2)
    text(d, (326, ry + 11), "EACH RISK HAS A BUILT GUARD, AND AN EVAL CASE THAT PROVES IT",
         f_zone, PURPLE)
    risks = [
        ("R1  Invents an answer", "Cite-or-reject validator.", "Failure path"),
        ("R2  Duplicate flood", "Grouping + existing check.", "Edge case"),
        ("R3  Answers what it shouldn't", "Scope check before retrieval.", "Policy case"),
        ("R4  Injection in the log", "Text is data, not instruction.", "Adversarial"),
        ("R5  Publishes unreviewed", "No write path exists.", "Regression"),
    ]
    for i, (risk, guard, ev) in enumerate(risks):
        x = 326 + i * 176
        text(d, (x, ry + 34), risk, f_lbl, INK)
        text(d, (x, ry + 52), guard, f_xs, GREY)
        text(d, (x, ry + 72), ev, f_xs, AMBER)

    arrow(d, 755, 496 + 1, 755, ry - 1, PURPLE)

    # ---- human approval --------------------------------------------------
    hy = 700
    box(d, 310, hy, 890, 100, GREEN_BG, GREEN, width=2)
    text(d, (326, hy + 12), "HUMAN APPROVAL  -  the only way an entry is published",
         f_zone, GREEN)
    text(d, (326, hy + 34),
         "The agent's one output is out/review_queue.json: every group, with its citations and audit trail.",
         f_sm, INK)
    text(d, (326, hy + 52),
         "A reviewer accepts, edits or rejects. Publishing is a separate human step, so an unreviewed draft",
         f_sm, INK)
    text(d, (326, hy + 70),
         "cannot reach the knowledge base. Rejections are logged - evidence about where the agent is weak.",
         f_sm, INK)
    text(d, (326, hy + 86),
         "Re-running a batch is safe: group ids are stable, so a retry does not queue the same work twice.",
         f_xs, GREY)

    arrow(d, 755, ry + 108 + 1, 755, hy - 1, GREEN)

    # ---- escalation contingency -----------------------------------------
    ey = 438
    box(d, 40, ey, 236, 192, (0xFA, 0xFA, 0xFB), LIGHT, width=2, dash=True)
    text(d, (56, ey + 11), "CONTINGENCY, NOT THE DESIGN", f_zone, LIGHT)
    text(d, (56, ey + 30), "ADK 2.x lets one agent call", f_xs, LIGHT)
    text(d, (56, ey + 44), "tools and emit a schema, and", f_xs, LIGHT)
    text(d, (56, ey + 58), "both capstone samples do.", f_xs, LIGHT)
    text(d, (56, ey + 78), "But WA3915 notes the pairing", f_xs, LIGHT)
    text(d, (56, ey + 92), "is model-dependent. If ours", f_xs, LIGHT)
    text(d, (56, ey + 106), "will not carry both, we split:", f_xs, LIGHT)

    for i, lab in enumerate(["Tool agent", "Format agent"]):
        x = 58 + i * 108
        box(d, x, ey + 124, 96, 30, FIXTURE, LIGHT, width=2, radius=6)
        text(d, (x + 48, ey + 134), lab, f_xs, LIGHT, anchor="ma")
    arrow(d, 155, ey + 139, 164, ey + 139, LIGHT, width=2, head=7)

    text(d, (56, ey + 164), "A known exit, not a promise", f_xs, LIGHT)
    text(d, (56, ey + 178), "to build a multi-agent system.", f_xs, LIGHT)

    # ---- footnote ---------------------------------------------------------
    text(d, (40, 852), "Group 1  |  FedEx FDE Capstone  |  Phase 1 approval gate", f_xs, LIGHT)
    text(d, (W - 40, 852), "Greenfield: every component above is new. All data synthetic.",
         f_xs, LIGHT, anchor="ra")

    img = img.resize((W, H), Image.LANCZOS)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(path), "PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    print("wrote", build(out))
