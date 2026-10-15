Build EverMind by working through src/openspec/changes/add-evermind-pipeline/tasks.md
in order, starting at task 2.1.

Read these first and treat them as authoritative:
  - proposal.md        why, and what is in and out of scope
  - specs/*/spec.md    what it must do - 21 Given/When/Then scenarios
  - design.md          how, including the decisions marked OPEN
  - contracts/knowledge-base/contract.md   what we may never write

For each task, in this order:
  1. Say which task you are on and name the spec requirement it satisfies.
  2. Write the test in src/tests/ FIRST, transcribed from the scenario.
  3. Implement in src/evermind/ until the test passes.
  4. Run the task's own verify line and show me the output.
  5. Stop and report before starting the next task.

Rules:
  - Do not change any spec. If a spec is wrong or cannot be satisfied,
    stop and tell me - never edit it to make a test pass.
  - Do not build anything not named ut of
    scope per proposal.md line 71.
  - The pipeline writes src/out/revie.
    After any full run, hash the three fixtures before and after and
    show me they are byte-identical.
  - Run everything with uv run. Never bare python.
  - src/evals/ needs a live key and