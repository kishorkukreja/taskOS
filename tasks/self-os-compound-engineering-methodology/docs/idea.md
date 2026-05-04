# Self-OS Compound Engineering Methodology — Idea Capture

Created: 2026-05-04
Status: captured
Repository: /data/taskOS
Task folder: /data/taskOS/tasks/self-os-compound-engineering-methodology

## Request source

- Source: direct user request in Telegram
- Captured by: Hermes
- Date: 2026-05-04

## User-provided source notes

User asked after reviewing EveryInc's compound-engineering plugin:

> Cool this is good, lets also add ce strategy to the list 
> Add all the skills
> Add the related content to self os too
> And add a task to taskos stating that we need to create tasks using this methodology strategy ideate brainstorm plan review work verify compound pulse

Source repository:

- https://github.com/EveryInc/compound-engineering-plugin/tree/main/plugins/compound-engineering

## What we are trying to do

Turn the compound-engineering plugin's workflow into a Self-OS-native methodology for creating and executing tasks.

The canonical methodology is:

**strategy → ideate → brainstorm → plan → review → work → verify → compound → pulse**

This should become the default way substantial Self-OS tasks are created, refined, routed, executed, verified, and folded back into durable knowledge.

## Why it matters

Self-OS is moving from passive knowledge capture into an active daily operating layer. That requires a repeatable method for converting raw ideas, links, screenshots, repos, and user requests into high-quality work. Without a methodology, tasks can become vague one-line TODOs that agents execute poorly.

This methodology adds guardrails:

- Strategy prevents random work.
- Ideation selects higher-leverage options.
- Brainstorming turns vague ideas into requirements.
- Planning makes work decomposable.
- Review catches mistakes before implementation.
- Work executes through the right agent/tooling path.
- Verification proves the work actually works.
- Compounding preserves reusable learnings.
- Pulse reports system health and next actions.

## Current state

- Self-OS canonical repo: `/data/Self-OS`.
- taskOS canonical repo: `/data/taskOS`.
- Related Self-OS content captured at: `/data/Self-OS/docs/compound-engineering-methodology.md`.
- Existing Self-OS operating contract: `/data/Self-OS/docs/self-os-operating-contract.md`.
- Existing Self-OS daily brief skill: `self-os-daily-brief`.
- Hermes Kanban setup is scheduled for Sunday 2026-05-10 and may become the routing layer for planner/worker/reviewer tasks.

## Desired outcome

A future implementation should create or adapt Self-OS skills and taskOS conventions so new substantial tasks use the methodology by default.

Desired end state:

- Self-OS docs include the canonical methodology.
- taskOS task templates encourage the same methodology.
- Relevant Hermes skills exist for each stage or for coherent grouped stages.
- Future task captures are richer than one-line TODOs.
- Daily/weekly Self-OS pulses report whether the methodology is being followed.

## Skills to create or adapt

### Core methodology skills

1. `self-os-strategy`
   - Adapted from `ce-strategy`.
   - Maintains Self-OS strategy, active tracks, metrics, constraints, and non-goals.

2. `self-os-ideate`
   - Adapted from `ce-ideate`.
   - Generates and evaluates grounded ideas before deeper brainstorming.

3. `self-os-brainstorm-to-prd`
   - Adapted from `ce-brainstorm`.
   - Converts vague ideas into requirements/PRD-ready docs.

4. `self-os-plan`
   - Adapted from `ce-plan`.
   - Produces task graphs, dependencies, acceptance criteria, and implementation plans.

5. `self-os-plan-review`
   - Adapted from `ce-doc-review` and `ce-code-review`.
   - Runs multi-lens review before work begins.

6. `self-os-work`
   - Adapted from `ce-work`.
   - Executes reviewed work through the right agent/tooling path.

7. `self-os-verify`
   - Adapted from verification patterns across `ce-work`, `ce-demo-reel`, `ce-test-browser`, and `ce-code-review`.
   - Collects proof that work is done.

8. `self-os-compound-learning`
   - Adapted from `ce-compound`.
   - Converts solved problems into skill updates, memories, wiki notes, or taskOS follow-ups.

9. `self-os-product-pulse`
   - Adapted from `ce-product-pulse`.
   - Creates Self-OS operating pulse reports.

### Supporting skills

10. `self-os-session-research`
    - Adapted from `ce-sessions`, `ce-session-inventory`, and `ce-session-extract`.
    - Finds decisions, attempts, and unresolved context across prior agent sessions.

11. `self-os-pr-feedback-resolver`
    - Adapted from `ce-resolve-pr-feedback`.
    - Resolves PR review comments systematically.

12. `self-os-demo-reel`
    - Adapted from `ce-demo-reel`.
    - Creates visual proof for UI/CLI/product changes, storing generated media outside Self-OS unless explicitly requested.

13. `self-os-optimize-loop`
    - Adapted from `ce-optimize`.
    - Runs metric-driven prompt/workflow/system optimization loops.

14. `agent-native-architecture-review`
    - Adapted from `ce-agent-native-architecture` and `ce-agent-native-audit`.
    - Reviews whether Self-OS and related systems are truly agent-native.

15. `self-os-simplify-code`
    - Adapted from `ce-simplify-code`.
    - Simplifies recently changed code while preserving behavior.

## Constraints and guardrails

- Do not blindly copy EveryInc plugin internals; adapt the methodology to Self-OS/Hermes/taskOS.
- Keep Self-OS as the durable Markdown system of record.
- Keep taskOS as the operational backlog for future specs/PRDs/issues/implementation plans.
- Use branch/PR for interpreted implementation work.
- Use direct commit to master only for raw captures and simple docs/tasks where appropriate.
- Do not store secrets.
- Do not let unconstrained agents implement vague ideas.
- Prefer GitHub PR UI for code review.
- Media/demo artifacts should be stored outside Self-OS unless explicitly requested.

## Acceptance criteria

- [ ] A canonical Self-OS methodology doc exists and is linked from the operating contract or Self-OS map.
- [ ] taskOS has a task template or guidance that includes strategy → ideate → brainstorm → plan → review → work → verify → compound → pulse.
- [ ] The first batch of skills is created or adapted:
  - [ ] `self-os-strategy`
  - [ ] `self-os-brainstorm-to-prd`
  - [ ] `self-os-plan`
  - [ ] `self-os-plan-review`
  - [ ] `self-os-product-pulse`
  - [ ] `self-os-compound-learning`
- [ ] The remaining supporting skills are triaged and either created, deferred, or folded into the core skills.
- [ ] Daily/weekly Self-OS pulse reports include methodology adherence signals.
- [ ] Future substantial task captures in taskOS are not one-line TODOs; they include sufficient context for strategy/ideation/planning/review.

## Likely files, repos, or services involved

- `/data/Self-OS/docs/compound-engineering-methodology.md` — captured methodology and skill backlog.
- `/data/Self-OS/docs/self-os-operating-contract.md` — should reference the methodology once implemented.
- `/data/Self-OS/docs/self-os-map.md` — should reference the methodology if/when the map exists.
- `/data/taskOS/tasks/` — task folders should eventually adopt this methodology.
- `~/.hermes/skills/self-os/` — likely location for user-local Self-OS skills.
- Hermes Kanban — future routing layer for strategy/planner/reviewer/worker/pulse tasks.

## Known decisions

- Include `ce-strategy` in the adapted skill list.
- Add all identified Self-OS skill candidates to the adoption list.
- The methodology is not generic; it should be adapted to Self-OS, taskOS, Hermes, and Kishor's Day Shift/Night Shift model.

## Open questions

- Should each methodology stage become its own Hermes skill, or should some stages be grouped into fewer operator skills?
- Should taskOS enforce this with templates, a validation script, or a `task-ingestor` skill patch?
- Should the Sunday Kanban setup create lanes/profiles that map directly to this methodology?
- Should `self-os-product-pulse` become part of the existing daily brief or a separate weekly pulse?

## Future documents to create

- `docs/spec.md` — exact technical design for methodology adoption.
- `docs/prd.md` — product requirements and user workflow.
- `docs/issues.md` — implementation issue breakdown.
- `docs/implementation-plan.md` — bite-sized execution plan.
