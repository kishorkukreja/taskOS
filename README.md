# taskOS

Git-controlled backlog for ideas, tasks, and implementation candidates we may want to pick up later.

This repo is intentionally separate from Self-OS wikis. Self-OS is the knowledge base; taskOS is the operational backlog for future work.

## Purpose

- Capture tasks before they become formal specs, PRDs, or GitHub issues.
- Preserve context, constraints, decisions, and acceptance criteria while the idea is fresh.
- Make every task independently pick-up-able by Hermes, Claude, Codex, or another coding agent.
- Support a later progression:

```
idea/task capture -> docs/idea.md -> spec.md -> prd.md -> issues.md -> implementation plan -> Codex execution
```

## Structure

```
taskOS/
├── README.md
├── tasks/
│   └── <task-slug>/
│       ├── README.md
│       └── docs/
│           └── idea.md
├── ideas/
└── templates/
```

## Task folder convention

Each task gets its own folder under `tasks/`.

Required starting files:

- `README.md` — task status and quick summary.
- `docs/idea.md` — full context dump of what we are trying to do.

Future optional files:

- `docs/spec.md` — engineering specification.
- `docs/prd.md` — product requirements document.
- `docs/issues.md` — implementation issue breakdown.
- `docs/implementation-plan.md` — bite-sized execution plan for Codex/Hermes.
- `research/` — references, links, prior art.
- `artifacts/` — logs, screenshots, examples.

## Status values

Use one of:

- `captured` — idea saved, not yet shaped.
- `ready-for-spec` — enough context to draft a spec/PRD.
- `specified` — spec/PRD exists.
- `ready-for-issues` — ready to split into implementation issues.
- `ready-for-implementation` — issues/plan ready for Codex or another coding agent.
- `in-progress`
- `blocked`
- `done`

## Current tasks

- `tasks/oauth-mcp-server/` — implement Claude-compatible OAuth for the Hermes MCP server.
