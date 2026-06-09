# Idea: Add no-mistakes to Codex and Claude Code Setup

Source: https://github.com/kunchenguid/no-mistakes
Wiki capture: /data/Self-OS/wikis/ai-research-os/raw/repos/2026-06-09-kunchenguid-no-mistakes.md
Wiki commit: 62ad593d6b1ed2bf16dd3f2f23d7eef19283a3fe
Captured: 2026-06-09

## Source summary

`no-mistakes` is a local Git gate for AI-generated or AI-assisted code. Instead of pushing a branch directly to `origin`, a developer pushes to a local `no-mistakes` remote. The tool creates a disposable worktree, runs a validation pipeline, and only forwards upstream / opens a PR after checks pass.

Pipeline:

```text
intent → rebase → review → test → document → lint → push → pr → ci
```

It supports Claude Code, Codex, Rovo Dev, OpenCode, Pi, and ACP targets. `no-mistakes init` installs a `/no-mistakes` skill into both `.claude/skills/no-mistakes/SKILL.md` and `.agents/skills/no-mistakes/SKILL.md`.

## Why this matters for Self-OS

Kishor's workflow already assumes AI coding agents can ship useful work but need strict review and validation. `no-mistakes` could formalize that final gate:

- Codex/Claude Code can implement work.
- `no-mistakes` validates the committed branch in a disposable worktree.
- GitHub PR remains the canonical review surface.
- Human approval remains required for judgment-heavy findings.

This is especially relevant for Night Shift implementation, where the next morning should start from a PR/diff that has already passed a structured local quality gate.

## Key operational details

### Install choices

Official installer:

```bash
NO_MISTAKES_TELEMETRY=0 \
  curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh
```

Potentially safer install from docs:

```bash
go install github.com/kunchenguid/no-mistakes/cmd/no-mistakes@latest
```

The docs say `go install` builds without an embedded telemetry website ID, so telemetry is off by default unless configured later.

### Repo setup

```bash
no-mistakes doctor
cd /path/to/repo
no-mistakes init
```

After initialization, verify:

```text
.claude/skills/no-mistakes/SKILL.md
.agents/skills/no-mistakes/SKILL.md
```

### Agent invocation

Validate existing committed work:

```text
/no-mistakes
```

Task-first mode:

```text
/no-mistakes <task>
```

In task-first mode, the agent should inspect `git status`, preserve unrelated work, commit only task-owned changes on a feature branch, then run the gate with a rich `--intent`.

### Repo config

Use explicit commands to avoid agent guessing:

```yaml
agent: codex
commands:
  test: "<repo test command>"
  lint: "<repo lint command>"
  format: "<repo format command>"
```

Claude-specific pilot can use `agent: claude` in a repo where Claude Code is preferred.

## Open questions

- Which repo should be the pilot: SupplyChainSignals, Self-OS tooling, or a smaller test repo?
- Should global default be `agent: codex`, `agent: claude`, or `agent: auto`?
- Should `no-mistakes` become mandatory before Night Shift PRs, or only available as an optional gate?
- Should telemetry be disabled globally via environment or avoided via `go install`?
- How should this interact with existing Hermes multi-agent PR review?

## Definition of done

A small pilot repo has `no-mistakes` initialized, both Claude/Codex-visible skill paths present, explicit test/lint commands configured, and one harmless branch has been gated or the blocker is documented.
