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

Every open project must use one of these statuses:

- `backlog` — captured or shaped, but not actively being worked.
- `in-progress` — actively being touched now.
- `blocked` — cannot move without a decision, dependency, review, or renewed attention.

Terminal status:

- `done` — complete and no longer open.

Weekly audit rule: nothing stays `in-progress` if it has not been touched in 7 days. The status audit proposes stale `in-progress` tasks for downgrade to `blocked` so drift becomes visible instead of invisible.

Human review contract:

- Weekly audit results are sent to Telegram for review before status changes are applied.
- If there is no reply within 48 hours, the original audit result is kept and applied.
- If a status change is challenged, Hermes should push back until the evidence/rationale is strong enough that both sides agree, then make the shift.

Run manually:

```bash
# Propose changes and save a pending review file.
python3 scripts/status_audit.py --repo /data/taskOS --propose --review-hours 48

# Apply expired pending proposals.
python3 scripts/status_audit.py --repo /data/taskOS --finalize-pending --commit
```

## Current tasks

- `tasks/oauth-mcp-server/` — implement Claude-compatible OAuth for the Hermes MCP server.
