# Greenfield Project Roadmap and Gate Checklist

## Purpose

Use this guide for any new project. It combines spec-driven delivery, AI-assisted engineering, agent design, testing, release governance, and the FDE capstone rules.

Core sequence: **plan -> build -> evidence -> Go/No-Go**.

## Roles

Assign one owner per role; everyone still contributes code.

- **Lead:** Owns the plan, scope, approval presentation, and final Go/No-Go decision.
- **Repository owner:** Owns Git and branches, protects `.env`, verifies a clean checkout, and produces the runnable release artifact.
- **Evaluation owner:** Owns the test/eval suite, failure-path coverage, regression evidence, and peer-review record.
- **Deck owner:** Owns the demonstration deck, release evidence slide, and timed rehearsal.

For a team of five, the fifth member is a second developer and evaluation backup.

## Recommended Project Layout

Adapt names to the problem, but keep equivalent responsibilities and files. Items marked **if applicable** are required only when that capability is used.

```text
project/
	README.md                         # setup, run, test, and demo instructions
	AGENTS.md                         # instructions and boundaries for coding agents
	MEMORY.md                         # durable context and decisions across sessions
	TODO.md                           # small, visible task list and handoff items
	pyproject.toml                    # Python dependencies and tool configuration
	uv.lock                           # reproducible dependency versions
	.env.example                      # variable names only; never secrets
	.gitignore                        # excludes .env, .venv, caches, artifacts
	openspec/
		changes/<change-name>/
			proposal.md                   # Gate 1 plan and approval request
			design.md                     # approved technical design
			tasks.md                      # ordered implementation tasks
			specs/<capability>/spec.md    # behavioral acceptance criteria
	<agent_package>/
		__init__.py
		agent.py                        # root ADK agent and output_schema
		tools.py                        # local tools and tool contracts
		schemas.py                      # Pydantic input/output models
		guardrails.py                   # callbacks, policy checks, or plugins
		state.py                         # session/state handling, if applicable
	servers/<server-name>/server.py   # MCP server, if applicable
	tests/                            # unit and integration tests
	evals/                            # evaluation sets and expected outcomes
	contracts/<external-system>/       # black-box boundary, if brownfield
		contract.md
	docs/
		architecture.md
		adr/                             # numbered architecture decision records
		risk-register.md
		rapid-peer-review.md
		go-no-go.md
		operations.md
	.github/
		workflows/ci.yml                # automated test/eval checks
		pull_request_template.md
		CODEOWNERS                      # if team review ownership is needed
		skills/rapid-peer-review.md      # reusable structured review instructions
```

## Gate 0: Problem Framing

**Goal:** choose a valuable, bounded problem before designing a solution.

### Required artifacts

- A one-sentence problem statement and named user or customer.
- A measurable target outcome and baseline, where one exists.
- A scope statement listing both included and explicitly excluded work.
- One or two backup ideas.

### Checklist

- [ ] The problem is repetitive or costly enough to justify change.
- [ ] The result is a decision, an action, or a structured result, not merely a chat response.
- [ ] The task has a human owner and clear user pain.
- [ ] Constraints, dependencies, data sources, and assumptions are recorded.
- [ ] For a brownfield project, the existing system is named and treated as an unchanged black box.
- [ ] For an agent project, one model call alone would not solve the task; it requires a tool, session state, or a bounded sub-agent delegation.
- [ ] The default design is a single agent; multi-agent design has not been promised prematurely.

**Exit criterion:** the lead can explain the problem, value, boundaries, and likely delivery risk in under two minutes.

## Gate 1: Plan Approval

**Goal:** gain approval before implementation begins. No agent code is written before this gate is approved.

### Required artifacts

- `openspec/changes/<change-name>/proposal.md`: the one-to-two-page plan and approval request.
- An architecture answer covering security, reliability, performance efficiency, cost effectiveness, operational excellence, and deployment.
- **For brownfield work:** `contracts/<external-system>/contract.md`, naming the unchanged black-box system, its input/output contract, ownership, and prohibited modifications.

### Checklist

- [ ] The plan identifies the task and who experiences the current pain.
- [ ] Inputs, output shape, and decisions made by the solution are explicit.
- [ ] In-scope work, exclusions, and brownfield boundary are explicit.
- [ ] Each anticipated failure or incorrect decision has a defined guard or escalation path.
- [ ] The build sketch lists the expected constructs and why they are needed.
- [ ] `proposal.md` records the expected agent package, output schema, tools/MCP server, session/state, guardrails, evaluation approach, and deployment boundary, marking unused capabilities as not applicable.
- [ ] The deployment target is considered as a Google Cloud design decision; live deployment is not assumed.
- [ ] The approval decision, approver, and any conditions are recorded.

**Exit criterion:** plan is signed off by the accountable reviewer. If redirected, choose a prepared backup idea and repeat this gate.

## Gate 2: Specification and Project Foundation

**Goal:** establish an implementable source of truth and a reproducible repository.

### Required artifacts

- `README.md`, `PRD.md`, `ARCHITECTURE.md`, `RULES.md`, `ROADMAP.md`, `CHANGELOG.md`, and `CONTRIBUTING.md` as appropriate to project size.
- `MEMORY.md` for durable decisions across sessions and `TODO.md` for visible task/handoff tracking when the project spans multiple sessions or contributors.
- `pyproject.toml`, `uv.lock`, `.gitignore`, and `.env.example`.
- `openspec/changes/<change-name>/design.md`, `tasks.md`, and `specs/<capability>/spec.md` when the proposal needs implementation detail.
- `docs/adr/NNNN-<decision>.md` for each non-obvious architecture, boundary, security, or policy decision.
- `.github/workflows/ci.yml` and `pull_request_template.md`; use `CODEOWNERS` when review ownership is needed.
- Documented local commands for `uv sync`, tests/evals, and the agent application launch command.

### Checklist

- [ ] Follow the spec lifecycle: Explore -> Propose -> Apply -> Verify -> Archive.
- [ ] Verification records how implementation was checked against the acceptance criteria; archiving merges approved delta specs into the active source of truth and preserves the completed change for audit.
- [ ] Specifications describe observable behavior and acceptance criteria rather than prescribing implementation details.
- [ ] Architectural decisions, data flow, interfaces, and open questions are documented.
- [ ] Each ADR records Status, Context, Decision, and Consequences.
- [ ] Repository instructions give contributors and coding agents the same constraints and conventions.
- [ ] Configuration is separated from code; secrets are excluded from Git.
- [ ] `.gitignore` excludes `.env`, `.venv`, Python caches, coverage/build output, and local credentials.
- [ ] `.env.example` lists every required environment variable with a safe placeholder and no secret values.
- [ ] GitHub branch protection requires a pull request and passing CI before `main` is merged, where repository settings are available.
- [ ] CI installs locked dependencies and runs the documented test/eval command on every pull request.
- [ ] Optional AI-assisted CI diagnostics are limited to organization-approved tooling, least-privilege credentials, and non-secret logs; they do not replace required test or human-review gates.
- [ ] A clean checkout can install dependencies and run the application/tests using documented commands.
- [ ] Change history and decisions have a durable home to prevent specification drift.

**Exit criterion:** a new contributor can set up the project, understand the first change, and run its baseline verification without private knowledge.

## Gate 3: Architecture, Safety, and Contracts

**Goal:** make the design safe, testable, and small enough to implement.

### Required artifacts

- `docs/architecture.md`: components, data flow, trust boundaries, and external dependencies.
- `docs/risk-register.md`: risk, likelihood, impact, guard, owner, and verification.
- `<agent_package>/schemas.py` and `<agent_package>/agent.py` for validated input/output contracts.
- `TOOL_CLASSIFICATION.md` and `MCP_PERMISSIONS.md`, or equivalent sections in `docs/architecture.md`, for agent tools/MCP servers.
- `SCHEMA_TEMPLATES.md`, or documented examples alongside each tool contract, for model-facing tool descriptions and input/output examples.
- **If applicable:** `servers/<server-name>/server.py`, `hooks/pretooluse.py`, and MCP-server tests.

### Checklist

- [ ] Inputs, outputs, state, error handling, and ownership boundaries are defined.
- [ ] Structured outputs use a validated schema; agent projects use a Pydantic `output_schema`.
- [ ] The root agent in `<agent_package>/agent.py` references the output schema and only the approved tools/sub-agents.
- [ ] Sensitive data, credentials, retention, access control, and audit needs are addressed.
- [ ] External tools have narrow contracts, least privilege, timeouts, retries, and logging.
- [ ] Every MCP server exposes only task-required tools; its inputs, outputs, permissions, and denied operations are documented.
- [ ] Each tool description states when it should and should not be used, and its schema includes valid and invalid examples so the agent can select it reliably.
- [ ] Tools are classified as read-only, bounded write, or high-impact action.
- [ ] High-impact actions require an appropriate confirmation, policy check, or human handoff.
- [ ] Prompt injection, unsafe output, tool misuse, and unsupported requests have input/output guardrails.
- [ ] Guardrail behavior is implemented in `<agent_package>/guardrails.py` or a documented callback/plugin module, with tests for block, allow, and escalation behavior.
- [ ] Logging, caching, and quality-gate callbacks/plugins are separated from policy guardrails, have documented lifecycle hooks, and have their own tests when used.
- [ ] A sub-agent is added only when it has an independently bounded responsibility, toolset, and evaluation approach.
- [ ] Expected latency, token/cost budget, scale, and operational telemetry are defined.

**Exit criterion:** design reviewers can state what the system may do, may not do, and how incorrect behavior is contained.

## Gate 4: Thin Vertical Slice

**Goal:** prove the smallest end-to-end workflow before broadening scope.

### Required artifacts

- A runnable entry point such as `run_<workflow>.py` or the documented ADK launch command.
- `<agent_package>/agent.py`, `tools.py`, `schemas.py`, and optional `state.py`/`guardrails.py`.
- `tests/test_<workflow>.py` for deterministic logic and integration contracts.
- `data/` fixtures plus an example input and expected structured output.

### Checklist

- [ ] The primary user path runs end to end locally.
- [ ] Output validates against its schema.
- [ ] The entry point, agent package, tests, and fixtures work using only the commands in `README.md`.
- [ ] Deterministic business logic is separated from model decisions where practical.
- [ ] Validation, calculations, and deterministic routing have unit tests independent of model/agent integration tests.
- [ ] Session/state handling is explicit when needed.
- [ ] Tool calls handle unavailable dependencies and malformed responses.
- [ ] Logs or traces identify the request, decision path, tool calls, failures, and cost-relevant usage.
- [ ] Code is reviewed for structure, clarity, configuration safety, and maintainability.

**Exit criterion:** the team can demonstrate a correct primary outcome from a clean environment.

## Gate 5: Evaluation, Guardrails, and Quality Evidence

**Goal:** demonstrate behavior rather than asserting it.

### Required artifacts

- `evals/<agent>.evalset.json` and/or `tests/test_<workflow>.py` with expected outcomes.
- `test_config.json` or an equivalent documented eval configuration.
- `tests/test_<agent>_eval.py` for a repeatable evaluation run; include timeout handling and progress/heartbeat logging for long-running model calls.
- A named failure-path case; for brownfield projects, a regression fixture and expected result.
- `docs/rapid-peer-review.md`.
- `.github/skills/rapid-peer-review.md` when the team uses a reusable AI-assisted review workflow.

### Checklist

- [ ] Tests/evaluations cover the primary path and at least one defined failure path.
- [ ] The eval set contains valid, invalid, boundary, and tool-failure inputs as applicable.
- [ ] Agent evaluation checks task success, schema validity, tool correctness, policy compliance, latency, and cost where applicable.
- [ ] Guardrail tests prove that unsafe or unauthorized requests are blocked or escalated without making the prohibited tool call.
- [ ] Edge cases and adversarial/unsafe requests are represented when relevant.
- [ ] Brownfield behavior remains compatible with the external black-box system.
- [ ] Automated verification runs in CI or a repeatable local command.
- [ ] Peer review is documented in `docs/rapid-peer-review.md`.
- [ ] The peer-review skill or checklist examines correctness, safety, tests, secrets, dependency/configuration changes, and user-visible behavior.
- [ ] Every peer-review Fail is resolved, satisfying RAPID ITC.009.

**Exit criterion:** evidence supports every acceptance criterion, or an unmet criterion is explicitly recorded as a release condition.

## Gate 6: Release Go/No-Go

**Goal:** make an evidence-based delivery decision.

### Required artifacts

- `docs/go-no-go.md`: completed Go/No-Go checklist under RAPID ITC.004.
- Test/evaluation result summary, peer-review outcome, and CI run reference.
- Release artifact and, when needed, rollback or contingency plan.

### Checklist

- [ ] Acceptance criteria are marked pass, fail, or conditionally accepted.
- [ ] The result includes counts for tests/evaluations run, passed, and failed.
- [ ] `docs/go-no-go.md` cites the exact commands and CI run/test output used as evidence.
- [ ] `docs/go-no-go.md` includes the control reference, date, decision maker, acceptance-criteria status, peer-review rating, test/eval counts, decision, rationale, and named conditions.
- [ ] The peer-review rating is recorded and all Fails are resolved.
- [ ] The decision is exactly one of Go, No-Go, or Conditional Go.
- [ ] The rationale contains at least two sentences citing acceptance, review, and test/evaluation evidence.
- [ ] Conditional-Go or No-Go conditions have named owners and resolution dates.
- [ ] Repository owner has completed the clean-checkout test (for example, `uv sync` and the documented application launch command).
- [ ] The runnable repository ZIP or equivalent release artifact has been produced.

**Exit criterion:** the accountable lead records the final Go/No-Go decision with evidence, satisfying RAPID ITC.004.

## Gate 7: Demonstration and Operations

**Goal:** hand over a solution that is explainable and supportable.

### Required artifacts

- A five-minute demonstration deck and rehearsal agenda.
- Operational handoff notes in `docs/operations.md`: ownership, monitoring, escalation, known limitations, and next changes.
- Release ZIP containing source, docs, tests/evals, lock file, and `.env.example`, but excluding `.env`, `.venv`, and generated artifacts.

### Checklist

- [ ] The presentation explains the problem, ADK/design decisions, evaluation evidence, and Go/No-Go decision.
- [ ] The deck has been timed and rehearsed.
- [ ] A teammate can unzip the release artifact, follow `README.md`, run `uv sync`, launch the application, and execute tests/evals without private files or undocumented steps.
- [ ] Deployment/environment assumptions and cloud design considerations are documented.
- [ ] `docs/operations.md` states whether deployment is local-only, cloud-designed, or live; it records scaling limits, quotas, prerequisites, and deferred deployment work.
- [ ] Monitoring covers quality drift, latency, cost, tool failure, and safety-policy failures as applicable.
- [ ] `docs/operations.md` defines per-request token/cost tracking, latency/error thresholds, tool-call failure handling, and policy-breach escalation for every production-bound agent capability.
- [ ] Rollback, escalation, and ownership are named.
- [ ] Future work becomes a new proposed spec rather than undocumented scope growth.

**Exit criterion:** a reviewer can understand the value, reproduce the evidence, and identify who owns the solution after delivery.

## Course Coverage Map

- **AIC-1102:** Context-rich development, scaffolding, custom configuration, debugging/refactoring, code review, test generation, CI/CD, cloud workflow, MCP tool design/security, and structured reasoning.
- **AIC-2101:** Behavior contracts, Explore/Propose/Apply/Verify/Archive, specification quality, debugging against specs, and preventing spec drift.
- **WA3915:** ADK architecture, structured output, tools, nested agents, sessions/state, callbacks/plugins, guardrails, evaluations, workflows, A2A, testing, and deployment.
- **WA3922-CAP:** Approved plan before build, greenfield/brownfield boundaries, reusable peer review, evidence-based Go/No-Go, team roles, runnable artifact, and presentation.