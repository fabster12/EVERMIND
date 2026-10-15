"""Build the benchmark review of proposal.md and architecture.png (.docx).

Usage:  python build_review_benchmark.py [output.docx]

What the Gate 1 proposal and architecture drawing were checked against, what
came back wrong, and what changed. Written after reviewing all four course
pairs in docs/reference/ - WA3922-CAP, WA3915, AIC-2101 and AIC-1102.

This is a working document for the group, not a gate deliverable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fedex_layout import (
    banner,
    body,
    bullets,
    callout,
    grid,
    h1,
    h2,
    labelled,
    meta_block,
    new_document,
)

OUT = Path(__file__).resolve().parent.parent / "docs" / "reviews" / "EverMind-Proposal-Review.docx"


def build(path):
    doc = new_document(footer_left="FedEx FDE Capstone  |  Group 1  |  Proposal benchmark review")

    banner(
        doc,
        "EverMind: proposal benchmark review",
        "proposal.md and architecture.png, checked against the four course guides",
    )

    meta_block(
        doc,
        [
            ("Reviewed", "openspec/changes/add-evermind-pipeline/proposal.md; docs/architecture.png"),
            ("Benchmarked against", "WA3922-CAP, WA3915, AIC-2101, AIC-1102 (lesson + lab guides)"),
            ("Outcome", "Both rewritten. Old versions in backup/2026-10-15-pre-benchmark/"),
            ("Length", "196 to 185 lines - did not grow"),
            ("Date", "15 October 2026"),
        ],
    )

    h1(doc, "The one thing that matters")
    body(
        doc,
        "The capstone lab guide says this outright, in a note in the Phase 2 escalation section:",
    )
    callout(
        doc,
        "From the WA3922-CAP lab guide.",
        "“One LlmAgent can call tools and emit an output_schema at the same time. In ADK 2.x "
        "the agent runs its tools during its reasoning and enforces the schema on its final "
        "answer... (ADK 1.x couldn’t do this and forced you to split the work across two "
        "agents joined by a SequentialAgent.) Reach for a workflow only when you have genuinely "
        "separate steps, not to work around a limit that’s gone. Both samples below are "
        "single agents.”",
    )
    body(
        doc,
        "Our diagram drew a three-agent SequentialAgent, and justified it by exactly that limit. "
        "We had designed around a constraint the course says was removed - and the lab names the "
        "workaround we had reinvented.",
    )
    body(
        doc,
        "The WA3915 note behind our reasoning is real: “Combining output_schema with tools is "
        "limited. Only some models support both at once.” Both statements are true. The "
        "pairing is model-dependent, which makes it a contingency to plan for, not a topology to "
        "commit to before the gate.",
    )
    body(
        doc,
        "The diagram now shows one agent. The split appears as a small dashed panel labelled "
        "“CONTINGENCY, NOT THE DESIGN” - planned, visibly not promised.",
    )

    h1(doc, "What else was missing")

    h2(doc, "The rubric was never referenced")
    body(
        doc,
        "The WA3922-CAP lesson guide lists six numbered success criteria and says: “Agree on "
        "these with your instructor at the approval gate. They are your rubric.” The proposal "
        "never mentioned them. The sign-off block now does, and names the six evaluation cases as "
        "the evidence for criterion 5.",
    )

    h2(doc, "The architectural answers were generic")
    body(
        doc,
        "The lab lists the exact questions the instructor asks under each concern. Several went "
        "unanswered:",
    )
    grid(
        doc,
        ["What the lab says the instructor asks", "Before", "Now"],
        [
            ["How do you prevent unnecessary tool access?", "not addressed",
             "Three read-only functions; no write function implemented or imported anywhere."],
            ["When a tool call fails, how does the agent degrade instead of crashing?",
             "not addressed",
             "Fails closed - the candidate is queued as a refusal rather than crashing the batch."],
            ["How will you know it is giving valuable responses in production?", "not addressed",
             "Reviewer accept and reject rates are the production quality signal."],
            ["Is the whole environment recreatable from code?", "not addressed",
             "Rebuilds from the committed fixture generator; recovery is re-running the batch."],
            ["Container, virtual machine, or serverless?", "“Agent Engine”",
             "A scheduled job, with the reason: no request path and no scaling pressure."],
        ],
        widths=[6.6, 3.4, 6.6],
    )

    h2(doc, "Two requirements we met but never named")
    bullets(
        doc,
        [
            ("The answer key. ",
             "The lab says to keep the expected results “in a separate file the agent never "
             "reads”. We had exactly that in the labelled query log, and never used the "
             "words. Now stated explicitly - it is what turns the eval set from impression into "
             "evidence."),
            ("The failure path. ",
             "Phase 3 requires one, and it is the most repeated requirement in the capstone "
             "materials. It was a table row like any other. It is now called out as the case "
             "that matters: the agent declines rather than invents."),
        ],
    )

    h1(doc, "What the two files look like now")
    labelled(
        doc, "proposal.md",
        "Problem (with why an agent, not one model call) - Solution (inputs, decisions, output "
        "shape) - Scope - The demonstration data - Risks, guards and the eval case that proves "
        "each - Build sketch with honest sizing - How we will prove it works - The six "
        "architectural considerations - Team - Backup idea - Sign-off.",
    )
    labelled(
        doc, "architecture.png",
        "Fixtures, then grouping, then one LlmAgent with three read-only tools, then the output "
        "schema with the cite-or-reject rule, then a risk-to-guard band, then human approval. The "
        "escalation contingency sits bottom-left, deliberately quiet.",
    )
    body(
        doc,
        "Three visual bugs were fixed while redrawing: “Pydantic” was misspelled, an "
        "arrow ran through its own caption, and a caption collided with the escalation box.",
    )

    h1(doc, "One judgement call to check")
    body(
        doc,
        "The handout asks for one to two pages. The proposal is about four printed. I kept it "
        "that way deliberately: the six architectural answers alone are a page, and the lab’s "
        "own sample projects are worked out in comparable depth.",
    )
    body(
        doc,
        "If the instructor is strict on length, the architecture table moves to design.md with a "
        "one-line pointer left behind. That lands the proposal at two pages and takes a minute.",
    )

    h1(doc, "Not touched")
    body(
        doc,
        "design.md, tasks.md and the four delta specs were left alone, as asked. They still treat "
        "the agent topology as an open question, which is now consistent with the proposal and "
        "the drawing rather than contradicting them.",
    )

    callout(
        doc,
        "The short version.",
        "The proposal was already well written. What it got wrong was benchmarking: it planned "
        "around an ADK limit the capstone says is gone, it never referenced the rubric it will be "
        "marked against, and it answered the architecture questions in general terms rather than "
        "the specific ones the instructor is given to ask. All three are now fixed, and the "
        "document is shorter than before.",
    )

    doc.save(str(path))
    return path


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    print("wrote", build(out))
