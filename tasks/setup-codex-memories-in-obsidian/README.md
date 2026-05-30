# Setup Codex Memories in Obsidian

Status: backlog

**Status:** ready
**Priority:** medium
**Created:** 2026-05-28
**Kanban:** `t_6ad170a9` — Setup Codex memories in Obsidian (`ready`, currently unassigned so it stays as a reference card until explicitly assigned)

## What we are trying to do
Set up a durable Codex memory workflow using an Obsidian-readable Markdown vault, so Codex can preserve project goals, decisions, references, and session context across runs while remaining repo-centric and inspectable.

## Why it matters
Codex is most useful when it can carry forward decisions, goals, and codebase context without relying on fragile chat history. Obsidian gives the human a readable graph/search interface; Markdown gives agents a simple source of truth; MCP and/or Codex hooks give Codex a way to read and write memory during work.

This should become part of the broader Self-OS pattern: durable notes, taskOS tasks, Kanban execution, and future reusable Hermes skills.

## Current state
The user provided a community-tested guide based on Dan Mac's thread with three approaches:

1. **Basic Memory + MCP** — recommended first path for quick cross-tool memory.
2. **Structured Obsidian vault + `AGENTS.md` + Codex hooks** — deeper native integration with full control.
3. **Native Codex memories + Obsidian pointed at `~/.codex/memories/`** — minimal setup, mainly read-only from Obsidian.

Hermes already has Codex, Obsidian, MCP, taskOS, and Kanban workflows. The missing piece is a concrete implementation plan and a verified setup for the current environment.

## Desired outcome
A working Codex memory vault that can be opened in Obsidian, read by Codex at session start, and used as a durable place for project notes, decisions, goals, and reference material. The task should produce exact commands, file paths, templates, and verification steps tailored to the user's Linux/Hermes/Self-OS setup, with room to adapt for desktop Codex app usage later.

## Recommended path
Start with **Approach 1: Basic Memory + MCP** because it is cross-tool and lowest friction, then add the structured vault conventions from Approach 2. Keep Approach 3 as a temporary/minimal fallback for native Codex-generated memory browsing.

## Proposed vault layout
```text
~/Documents/Obsidian/Ideaverse/Codex/
├── AGENTS.md
├── projects/
├── decisions/
├── memory/
│   ├── goals.md
│   └── index.md
├── templates/
├── reference/
└── .codex/
    ├── hooks.json
    └── session-start.sh
```

## Acceptance criteria
- [ ] Decide the canonical vault path for this machine and/or the user's desktop Obsidian setup.
- [ ] Create the Obsidian-readable Codex memory vault folder structure.
- [ ] Add `memory/goals.md` and `memory/index.md` starter files.
- [ ] Add `AGENTS.md` with vault structure, note conventions, session-start behavior, and note-creation rules.
- [ ] Add ADR/template files for decisions and project notes.
- [ ] Configure Basic Memory MCP for Codex, or document the exact command if desktop/app setup must be done by the user.
- [ ] Verify `codex mcp list` shows `basic-memory` where possible.
- [ ] Configure Codex hooks in `~/.codex/config.toml` and `.codex/hooks.json`, if supported by the installed Codex version.
- [ ] Add optional `.codex/session-start.sh` that prints goals, recent notes, and recent git commits.
- [ ] Enable or document native Codex memories as fallback: `~/.codex/memories/` opened or symlinked into Obsidian.
- [ ] Add safe credential handling notes, especially for Basic Memory Cloud API keys.
- [ ] Run a smoke test: start Codex from the vault and confirm it reads goals/index or can query Basic Memory.
- [ ] Update this task with the final chosen approach, exact paths, and verification output.

## Known decisions
- Status starts as `ready` per user request.
- Approach 1 is the recommended first implementation path.
- Approach 2 should be captured as the deeper structured-vault design even if not fully enabled on day one.
- Approach 3 is useful as a minimal fallback but should not be the only long-term memory strategy.
- Notes should be plain Markdown and inspectable in Obsidian.
- Filenames should use kebab-case.
- Wikilinks should connect related notes.
- Status values in notes: `active`, `completed`, `archived`, `deprecated`.

## Open questions
- Should the canonical Obsidian vault live under `/root/Documents/...`, `/data/Self-OS/...`, or the user's desktop machine?
- Should Basic Memory run local-only or use Basic Memory Cloud for easier Codex app access?
- Should this become a reusable Hermes skill after the first setup is verified?
- Should the vault be git-backed, and if so, where should it be hosted?
- Should project-specific Codex memory live in one global Codex vault or per-project folders?

## Future documents to create
- [ ] docs/idea.md
- [ ] docs/setup-plan.md
- [ ] docs/agents-template.md
- [ ] docs/hooks-template.md
- [ ] docs/verification-log.md
