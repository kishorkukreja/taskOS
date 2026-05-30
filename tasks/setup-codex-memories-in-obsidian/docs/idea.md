# Idea Notes — Setup Codex Memories in Obsidian

**Source:** User-provided guide and follow-up confirmation — 2026-05-28

## Raw source interpretation
The user wants a taskOS task and a referenced Kanban task, both in `ready` status, to set up Codex persistent memory using an Obsidian vault. The provided guide is based on Dan Mac's thread and three community-tested approaches.

## Core idea
Codex should have durable memory that is:

- readable and editable as Markdown,
- visible in Obsidian,
- accessible across Codex app/CLI and other tools where possible,
- structured enough for goals, project context, decisions, and reference material,
- safe around credentials and local files.

## Three approaches to preserve

### Approach 1 — Basic Memory + MCP
Recommended first path.

Benefits:
- Easiest setup.
- Works with Codex app and CLI.
- Shares notes across tools such as Claude Code, Cursor, and Obsidian.
- Plain Markdown remains the source of truth.

Reference commands:

```bash
codex mcp add basic-memory bash -c "uvx basic-memory mcp"
codex mcp list
```

Project-scoped variant:

```bash
codex mcp add basic-memory bash -c "uvx basic-memory mcp --project your-project-name"
```

Cloud variant:

```toml
[mcp_servers.basic-memory]
url = "https://cloud.basicmemory.com/mcp"
bearer_token_env_var = "BASIC_MEMORY_API_KEY"
```

Credential note: never write `BASIC_MEMORY_API_KEY` into taskOS, wiki, or committed files. Store it in shell/profile secret storage only.

### Approach 2 — Structured Obsidian vault + AGENTS.md + Codex hooks
Deepest integration, zero external tools, full control.

Vault structure:

```text
projects/       # One folder per active project
decisions/      # Architecture/design decision records
memory/         # Persistent context Codex reads across sessions
  goals.md      # Current priorities and focus areas
  index.md      # Map of everything in the vault
templates/      # Note templates with YAML frontmatter
reference/      # Codebase knowledge, API docs, architecture maps
```

`AGENTS.md` should encode:
- vault structure,
- note conventions,
- status values: `active`, `completed`, `archived`, `deprecated`,
- kebab-case filenames,
- wikilinks,
- rules for decision records and project notes,
- startup behavior: read `memory/goals.md`, check `memory/index.md`, inspect recent git commits.

Codex hooks should load memory at session start:

```toml
[features]
codex_hooks = true
```

Example `.codex/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "cat memory/goals.md memory/index.md",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Richer startup script:

```bash
#!/bin/bash
echo "## Current Goals"
cat memory/goals.md
echo ""
echo "## Recently Modified Notes"
find . -name "*.md" -mtime -2 -not -path "./.codex/*" | head -20
echo ""
echo "## Recent Changes"
git log --oneline -10 2>/dev/null || echo "No git history"
```

### Approach 3 — Native Codex memories + Obsidian
Minimal fallback.

Enable in `~/.codex/config.toml`:

```toml
[features]
memories = true

[memories]
generate_memories = true
use_memories = true
```

Note: the provided text had `generate_memures`; treat that as a typo and verify the actual Codex config key before writing it.

Memory files live in:

```text
~/.codex/memories/
├── memory_summary.md
├── MEMORY.md
├── raw_memories.md
├── rollout_summaries/
└── skills/
```

Obsidian options:
- Open `~/.codex/memories/` as a separate vault.
- Or symlink it into an existing vault:

```bash
ln -s ~/.codex/memories/ ~/your-vault/codex-memories
```

This is mainly for browsing/searching generated Codex memories. Persistent instructions should live in `AGENTS.md`.

## Tailoring for this environment
Known current environment:
- Linux host.
- taskOS canonical repo: `/data/taskOS`.
- Self-OS canonical repo: `/data/Self-OS`.
- Hermes profiles exist, including `programmer`, which routes coding via Codex.
- Obsidian skill expects `OBSIDIAN_VAULT_PATH` if configured, otherwise defaults to `~/Documents/Obsidian Vault`.

Recommended implementation choice:
1. Create a dedicated Codex memory vault under a clear Obsidian path.
2. Use Basic Memory MCP if `codex mcp` is available and auth/setup permits.
3. Add `AGENTS.md` and hooks as repo-visible files inside the vault.
4. Add native Codex memories as a linked/read-only reference if the installed Codex supports it.

## Daily usage pattern
At session start:
- Ask Codex: “What are our current goals?”
- Ask Codex: “What decisions have we made about X?”
- Codex reads `memory/goals.md`, `memory/index.md`, or Basic Memory notes.

After work:
- Ask Codex to create an ADR in `/decisions/`.
- Ask Codex to update `/memory/index.md`.
- Review/refine the result in Obsidian.

## Kanban reference
A Kanban card should be created for implementation and referenced from the taskOS README once the card ID is known.

## Source memory context
The user prefers repo-centric, durable Markdown workflows; operational knowledge should become tasks or skills; and code/agent workflows should be verified with explicit commands before being marked complete.
